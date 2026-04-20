# CrashLoopBackOff Troubleshooting Runbook

## Belirtiler
- Pod durumu: CrashLoopBackOff
- Pod sürekli restart atıyor, RESTARTS sütunu artıyor
- Container başlatılıyor ve hemen kapanıyor
- Back-off süresi giderek artıyor (10s, 20s, 40s, 80s, 160s, 300s max)

## Teşhis Adımları

### Adım 1: Pod Durumunu Kontrol Et
Komut: `kubectl get pods -n <namespace>`
Kontrol: STATUS sütununda CrashLoopBackOff, RESTARTS sayısı

### Adım 2: Pod Detaylarını İncele
Komut: `kubectl describe pod <pod-name> -n <namespace>`
Kontrol:
- Last State → Reason alanı (OOMKilled, Error, ContainerCannotRun)
- Exit Code (137 = OOMKilled, 1 = Application Error, 127 = Command Not Found)
- Events bölümündeki son hatalar
- Container image ve tag bilgisi

### Adım 3: Container Loglarını Kontrol Et
Komut: `kubectl logs <pod-name> -n <namespace> --previous`
Not: `--previous` flag'i önceki (crash olan) container'ın loglarını getirir
Kontrol: Stack trace, bağlantı hataları, eksik environment variable'lar

### Adım 4: Resource Kullanımını Kontrol Et
Komut: `kubectl top pod <pod-name> -n <namespace>`
Kontrol: Memory kullanımı limit'e yakın mı?

### Adım 5: Event'leri Kontrol Et
Komut: `kubectl get events -n <namespace> --sort-by=.lastTimestamp`
Kontrol: OOMKilling, FailedMount, FailedScheduling gibi event'ler

## Çözümler

### Exit Code 137 (OOMKilled)
- Memory limit'i artır (mevcut kullanımın 1.5-2 katı önerilir)
- Request değerini de orantılı artır
- Komut: `kubectl set resources deployment/<name> -n <ns> --limits=memory=<value> --requests=memory=<value>`
- Uzun vadede: memory leak araştır, profiling yap
- JVM uygulamalarında: -Xmx değerini container limitinin %70-80'i olarak ayarla

### Exit Code 1 (Application Error)
- Logları incele, hata mesajını tespit et
- Image tag'ini kontrol et (yanlış versiyon olabilir)
- Environment variable'ları kontrol et (eksik olabilir)
- ConfigMap/Secret mount'larını kontrol et
- Veritabanı bağlantı string'ini doğrula

### Exit Code 127 (Command Not Found)
- Container image'ında gerekli binary var mı kontrol et
- Dockerfile'daki ENTRYPOINT/CMD doğru mu kontrol et
- Multi-stage build kullanıyorsan gerekli dosyaların kopyalandığından emin ol

### Exit Code 126 (Permission Denied)
- Dosya izinlerini kontrol et
- SecurityContext ayarlarını kontrol et
- ReadOnlyRootFilesystem kısıtlaması olabilir
