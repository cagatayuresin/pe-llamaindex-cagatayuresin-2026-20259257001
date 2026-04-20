# Kubernetes Node Sağlık Kontrolü (Health Check)

Bu belge, Kubernetes cluster'ındaki node'ların genel sağlık durumunu, kaynak (Resource) kullanımını ve stability (kararlılık) durumunu doğrulamak için izlenecek standart prosedürleri içerir.

## 1. Node Durum (Status) Kontrolü
Tüm node'ların `Ready` statüsünde olması beklenir. `NotReady` olan node'larda ağ kopukluğu veya kubelet çökmesi olabilir.
```bash
kubectl get nodes -o wide
```
**Beklenen Durum:** Tüm node'ların STATUS kolonu "Ready" olmalıdır.

## 2. Disk Pressure ve Memory Pressure
Node üzerindeki kaynaklar kritik seviyelere ulaştığında kubelet "pressure" uyarıları verir.
```bash
kubectl describe nodes | grep -i -E "Name:|DiskPressure|MemoryPressure|PIDPressure"
```
**Aksiyon:** Herhangi bir pressure durumu "True" ise, o node üzerindeki yüksek kaynak tüketen pod'ları inceleyin (`kubectl top pods --all-namespaces`).

## 3. Genel Kaynak Kullanımı Oranları
Node bazında CPU ve bellek (Memory) tüketimini kontrol edin.
```bash
kubectl top nodes
```
**Beklenen Durum:** CPU ve Memory kullanım oranlarının ortalama %80'in altında olması iyi bir sistem göstergesidir. %90+ kullanımlar kalıcıysa autoscale (Cluster Autoscaler) mekanizmalarının devreye girip girmediği kontrol edilmelidir.

## 4. Olaylar (Events) ve Hatalar
Son zamanlarda node seviyesinde yaşanan olağandışı olayların kontrolü.
```bash
kubectl get events --sort-by='.metadata.creationTimestamp' | grep Node
```
**Aksiyon:** Kubelet çökmesi, image çekme başarısızlıkları veya volume bağlama (attach)/koparma (detach) hataları arayın.
