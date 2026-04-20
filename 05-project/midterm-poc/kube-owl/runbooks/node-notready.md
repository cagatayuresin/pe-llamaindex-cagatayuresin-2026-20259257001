# Node NotReady Troubleshooting Runbook

## Belirtiler
- Node durumu: NotReady
- Node üzerindeki pod'lar çalışmıyor veya evict ediliyor
- Yeni pod'lar bu node'a schedule edilemiyor
- kubectl get nodes çıktısında STATUS = NotReady
- Cluster kapasitesi düşmüş durumda

## Olası Nedenler
1. **kubelet Çalışmıyor:** Node üzerindeki kubelet servisi durmuş
2. **Network Plugin Sorunu:** CNI (Calico, Flannel, Cilium) çalışmıyor
3. **Disk Pressure:** Node'da disk dolmuş
4. **Memory Pressure:** Node'da yetersiz bellek
5. **PID Pressure:** Node'da çok fazla process var
6. **PLEG Sorunu:** Pod Lifecycle Event Generator sağlıksız
7. **Container Runtime:** Docker/containerd hata veriyor
8. **Network Bağlantısı:** Node'un API server ile iletişimi kopmuş

## Teşhis Adımları

### Adım 1: Node Durumlarını Kontrol Et
Komut: `kubectl get nodes`
Kontrol: STATUS sütununda NotReady olan node'ları tespit et

### Adım 2: Node Detaylarını İncele
Komut: `kubectl describe node <node-name>`
Kontrol:
- Conditions bölümü:
  - Ready: True/False
  - MemoryPressure: True/False
  - DiskPressure: True/False
  - PIDPressure: True/False
  - NetworkUnavailable: True/False
- Reason ve Message alanları (hata açıklamaları)
- LastHeartbeatTime (son heartbeat ne zaman?)
- Taints (NotReady taint eklenmiş mi?)

### Adım 3: Node Kaynak Kullanımı
Komut: `kubectl top nodes`
Kontrol: CPU ve Memory kullanım oranları

### Adım 4: Node Üzerindeki Pod'ları Kontrol Et
Komut: `kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-name>`
Kontrol: Evicted veya Terminating durumunda pod var mı?

### Adım 5: Events Kontrol Et
Komut: `kubectl get events --sort-by=.lastTimestamp`
Kontrol: NodeNotReady, NodeStatusUnknown, FailedNodeCondition event'leri

## Çözümler

### kubelet Sorunu İçin
- Node'a SSH ile bağlan
- kubelet durumunu kontrol et: `systemctl status kubelet`
- kubelet loglarını incele: `journalctl -u kubelet -f --lines=50`
- kubelet'i yeniden başlat: `systemctl restart kubelet`
- kubelet konfigürasyonunu kontrol et: `/var/lib/kubelet/config.yaml`

### Network Plugin (CNI) Sorunu İçin
- CNI pod'larını kontrol et: `kubectl get pods -n kube-system | grep calico` (veya flannel/cilium)
- CNI loglarını kontrol et
- CNI konfigürasyon dosyalarını kontrol et: `/etc/cni/net.d/`
- CNI binary'lerini kontrol et: `/opt/cni/bin/`
- Son çare: CNI plugin'ini yeniden kur

### Container Runtime Sorunu İçin
- Docker: `systemctl status docker` ve `docker info`
- containerd: `systemctl status containerd` ve `crictl info`
- Runtime'ı yeniden başlat: `systemctl restart containerd`

### Disk Pressure İçin (Ayrıntılı çözüm disk-pressure runbook'unda)
- Disk kullanımını kontrol et: `df -h`
- Gereksiz container image'larını temizle: `crictl rmi --prune`
- Eski logları temizle
- Evicted pod'ları temizle

### Memory Pressure İçin
- Memory kullanımını kontrol et: `free -h`
- Yüksek bellek tüketen process'leri bul: `top -o %MEM`
- Pod'ları diğer node'lara taşı (drain)
- Node'a daha fazla RAM ekle

### PLEG Sorunu İçin
- PLEG, pod lifecycle event'lerini takip eder
- Çok sayıda pod varsa yavaşlayabilir
- Container runtime'ı yeniden başlat
- Node üzerindeki pod sayısını azalt

### Node Erişilemezse
- Network bağlantısını kontrol et
- Firewall kurallarını kontrol et (6443 portu API server için)
- Node'un fiziksel durumunu kontrol et (cloud provider console'dan)
- IaaS provider'da instance durumunu kontrol et

## Acil Durum Prosedürü
1. Etkilenen iş yüklerini başka node'lara taşı:
   - `kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data`
2. Node'u onarılamıyorsa cluster'dan çıkar:
   - `kubectl delete node <node-name>`
3. Yeni node ekle (cloud provider ile veya kubeadm join ile)

## İlgili Komutlar
- `kubectl get nodes` — Node durumlarını listele
- `kubectl describe node <node-name>` — Node detayları
- `kubectl top nodes` — Node resource kullanımı
- `kubectl get pods --all-namespaces -o wide` — Tüm pod'ları node bazlı gör
- `kubectl get events --sort-by=.lastTimestamp` — Son event'ler
