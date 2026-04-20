# Disk Pressure Troubleshooting Runbook

## Belirtiler
- Node condition: DiskPressure = True
- Pod'lar node'dan evict ediliyor
- Yeni pod'lar schedule edilemiyor
- "Eviction threshold met" event'leri
- kubelet "attempting to reclaim ephemeral-storage" logları
- Image pull işlemleri başarısız olabiliyor

## Disk Pressure Nedir?
Kubernetes kubelet, node üzerindeki disk kullanımını sürekli izler. Disk kullanımı belirli eşik değerlerini aştığında DiskPressure durumu aktif olur ve kubelet, düşük öncelikli pod'ları evict ederek disk alanı açmaya çalışır.

Varsayılan eviction eşikleri:
- nodefs.available < %15 (soft eviction)
- nodefs.available < %10 (hard eviction)
- imagefs.available < %15

## Teşhis Adımları

### Adım 1: Node Durumunu Kontrol Et
Komut: `kubectl get nodes`
Kontrol: Node durumu (DiskPressure taint olabilir)

### Adım 2: Node Detaylarını İncele
Komut: `kubectl describe node <node-name>`
Kontrol:
- Conditions → DiskPressure: True/False
- Allocatable → ephemeral-storage değeri
- Events bölümünde FreeDiskSpaceFailed, EvictionThreshold, Evicted mesajları

### Adım 3: Node Kaynak Kullanımı
Komut: `kubectl top nodes`
Node'a SSH ile bağlanıp: `df -h`
Kontrol: Disk kullanım oranları, /var/lib/kubelet ve /var/lib/containerd dizinleri

### Adım 4: Evict Edilen Pod'ları Kontrol Et
Komut: `kubectl get pods --all-namespaces --field-selector status.phase=Failed`
Komut: `kubectl get pods --all-namespaces | grep Evicted`
Kontrol: Evicted durumunda pod var mı?

### Adım 5: Node Üzerindeki Disk Tüketimini Analiz Et
Node'a SSH ile bağlan:
- `du -sh /var/lib/kubelet/*` — kubelet'in kullandığı alan
- `du -sh /var/lib/containerd/*` — Container runtime storage
- `du -sh /var/log/*` — Log dosyaları
- `df -h` — Genel disk kullanımı

## Çözümler

### Acil: Disk Alanı Açma
1. **Evicted pod'ları temizle:**
   ```
   kubectl get pods --all-namespaces --field-selector status.phase=Failed -o json | \
     kubectl delete -f -
   ```

2. **Kullanılmayan container image'larını temizle:**
   Node üzerinde: `crictl rmi --prune`
   veya Docker: `docker system prune -af`

3. **Eski container loglarını temizle:**
   Node üzerinde: `find /var/log/containers -name "*.log" -mtime +7 -delete`
   Dikkat: Aktif container loglarını silme!

4. **Geçici dosyaları temizle:**
   Node üzerinde: `rm -rf /tmp/large-files`

### Orta Vade: Log Rotation Ayarlama
1. Container runtime log rotation'ı yapılandır:
   ```
   # /etc/containerd/config.toml
   [plugins."io.containerd.grpc.v1.cri"]
     max_container_log_line_size = 16384
   ```

2. kubelet log rotation ayarları:
   ```
   # kubelet config
   containerLogMaxSize: "10Mi"
   containerLogMaxFiles: 5
   ```

3. Sistem logları için logrotate yapılandır

### Uzun Vade: Kalıcı Çözümler

#### Disk Boyutunu Artırma
- Cloud provider'da disk resize et (EBS, Persistent Disk, Managed Disk)
- Yeni bir disk ekleyip mount et
- Node pool'u daha büyük disklerle yeniden oluştur

#### PersistentVolume Kullanımı
- Uygulama verilerini PV/PVC'ye taşı
- EmptyDir yerine PersistentVolume kullan
- Storage class'ları doğru yapılandır

#### Image Yönetimi
- Gereksiz yere büyük image'lar kullanma
- Multi-stage build ile image boyutunu küçült
- Image pull policy'yi IfNotPresent olarak ayarla
- Düzenli image garbage collection ayarla:
  ```
  # kubelet config
  imageGCHighThresholdPercent: 85
  imageGCLowThresholdPercent: 80
  ```

#### Monitoring ve Alerting
- Prometheus ile disk kullanımını monitor et
- DiskPressure olmadan ÖNCE alert kur (%70-80 eşiğinde)
- Grafana dashboard'larında disk trend'lerini takip et

## Pod Eviction Sırası
DiskPressure durumunda kubelet pod'ları şu sırayla evict eder:
1. BestEffort (resource request/limit olmayan) pod'lar
2. Burstable (kısmi request/limit) pod'lar
3. Guaranteed (request = limit) pod'lar son evict edilir

**İpucu:** Kritik pod'ları Guaranteed QoS class'ına koyarak DiskPressure'da en son evict edilmelerini sağlayabilirsin.

## İlgili Komutlar
- `kubectl get nodes` — Node durumlarını listele
- `kubectl describe node <node-name>` — Node detayları (conditions)
- `kubectl top nodes` — Node resource kullanımı
- `kubectl get pods --all-namespaces --field-selector status.phase=Failed` — Failed pod'lar
- `kubectl get events --sort-by=.lastTimestamp` — Son event'ler
