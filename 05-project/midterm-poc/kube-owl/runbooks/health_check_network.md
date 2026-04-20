# Kubernetes Ağ ve İletişim (Network) Sağlık Kontrolü

Bu belge Kubernetes cluster içerisindeki ağ yapılandırmasının, Servis rotalarının (Service) ve dışarıya açılan kapıların (Ingress/NodePort) sağlığını kontrol etmek içindir.

## 1. Endpoint Bağlantılarının Tamlığı
Bir Kubernetes servisinin arkasında istekleri karşılayacak çalışan pod'lar olmalıdır. Pod'lar hazır değilse "Endpoints" listesi boş dönebilir, bu da trafik kesintisi (Downtime) veya 502/503 HTTP hatalarına yol açar.
```bash
kubectl get endpoints --all-namespaces
```
**Beklenen Durum:** Sizin dağıttığınız (`default` dahil diğer uygulama namespace'lerindeki) servislerin `ENDPOINTS` alanında ilgili pod IP'lerinin ve portların listelenmesi gerekir. Eğer `<none>` ise label eşleşmesi bozuk olabilir.

## 2. CoreDNS ve Servis Çözümlemesi (DNS Resolution)
Pod'ların kendi aralarında isim (Service Name) ile iletişim kurup kuramadıklarını anlayabilmek için DNS servisinin problemsiz olması gerekir.
```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
```
**Aksiyon:** Tüm coredns podlarının "Running" olduğunu ve restart atmadığını kontrol edin.
Loglarını `kubectl logs -n kube-system -l k8s-app=kube-dns --tail=20` ile kontrol ederek hata (error) olup olmadığına bakın.

## 3. Ingress Kontrolcü Durumu
Uygulamayı dış dünyaya açan Ingress Controller objesinin (Nginx, Traefik vb.) sağlığının kontrolü.
```bash
kubectl get ingress --all-namespaces
```
**Beklenen Durum:** Tüm geçerli ingress objelerinin ADDRESS sütununun yük dengeleyici (LoadBalancer) tarafından atanmış geçerli bir IP adresi veya hostname'e sahip olması beklenmektedir.

## 4. Genel Bağlantı Hataları Event'leri
Kubelet ve Ingress-Controller tarafından raporlanan network bazlı hataları görebilmek.
```bash
kubectl get events --all-namespaces | grep -i 'network\|ingress\|service'
```
**Aksiyon:** Yakın zamanlı ve uyarıcı (Warning) veya hata (Failed) kategorisinde event varsa spesifik servisi inceleyin.
