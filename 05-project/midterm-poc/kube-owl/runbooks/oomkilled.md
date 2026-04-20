# OOMKilled (Out of Memory) Troubleshooting Runbook

## Belirtiler
- Pod durumu: CrashLoopBackOff veya Terminated
- Last State Reason: OOMKilled
- Exit Code: 137
- Kernel loglarında "Memory cgroup out of memory" mesajı
- Container bellek kullanımı limit'e çok yakın
- Pod restart sayısı sürekli artıyor

## OOMKilled Nedir?
Kubernetes, container'ların belirli bir memory limit'i aşmasını engellemek için Linux cgroup'larını kullanır. Container bu limiti aştığında, Linux kernel OOM Killer (Out of Memory Killer) devreye girer ve container'daki ana process'i öldürür. Bu duruma OOMKilled denir.

## Teşhis Adımları

### Adım 1: OOMKilled Doğrulama
Komut: `kubectl describe pod <pod-name> -n <namespace>`
Kontrol:
- Last State → Reason: OOMKilled
- Exit Code: 137
- Containers → Resources → Limits → memory değeri

### Adım 2: Mevcut Memory Kullanımı
Komut: `kubectl top pod <pod-name> -n <namespace>`
Kontrol: MEMORY sütunundaki değeri limit ile karşılaştır

### Adım 3: Node Üzerindeki Toplam Kaynak Durumu
Komut: `kubectl top nodes`
Komut: `kubectl describe node <node-name>`
Kontrol: Allocatable vs Allocated memory oranı

### Adım 4: Container Logları
Komut: `kubectl logs <pod-name> -n <namespace> --previous`
Kontrol: Memory ile ilgili uyarılar, OutOfMemoryError, heap dump mesajları

## Çözümler

### Kısa Vadeli: Memory Limit Artırma
- Mevcut kullanımın 1.5-2 katı kadar limit ayarla
- Request'i limit'in %50-75'i olarak ayarla
- Komut: `kubectl set resources deployment/<name> -n <ns> --limits=memory=512Mi --requests=memory=256Mi`
- Dikkat: Node'da yeterli memory olduğundan emin ol

### JVM (Java) Uygulamaları İçin
- -Xmx değerini container memory limitinin %70-80'i olarak ayarla
- Örnek: Container limit 512Mi ise → -Xmx384m
- JVM metaspace ve native memory de hesaba kat
- GC loglarını aktif et: `-Xlog:gc*`
- Heap dump al: `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heap.hprof`

### Node.js Uygulamaları İçin
- `--max-old-space-size` flag'ini kullan
- Örnek: Container limit 512Mi ise → `--max-old-space-size=384`
- Memory leak tespiti için: `node --inspect` ve Chrome DevTools
- Event loop lag'ini monitor et

### Python Uygulamaları İçin
- tracemalloc modülünü kullanarak memory profiling yap
- Büyük veri setlerini chunk'lar halinde işle
- Generator kullanarak bellek tasarrufu yap
- gc modülü ile garbage collection'ı zorlayabilirsin

### Uzun Vadeli Çözümler
1. Memory leak araştır (profiling araçları kullan)
2. Vertical Pod Autoscaler (VPA) kur — otomatik limit ayarlama
3. Uygulama caching stratejisini gözden geçir
4. Gereksiz in-memory veri tutmaktan kaçın
5. Monitoring ile erken uyarı kur (Prometheus alert)

## İlgili Komutlar
- `kubectl get pods -n <namespace>` — Pod durumlarını listele
- `kubectl describe pod <pod-name> -n <namespace>` — Pod detayları
- `kubectl top pod -n <namespace>` — Resource kullanımı
- `kubectl logs <pod-name> -n <namespace> --previous` — Önceki container logları
- `kubectl get events -n <namespace> --sort-by=.lastTimestamp` — Son event'ler
