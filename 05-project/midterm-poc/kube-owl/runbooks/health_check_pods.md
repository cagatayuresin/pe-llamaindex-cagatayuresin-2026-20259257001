# Kubernetes Pod Kararlılık/Sağlık Kontrolü (Health Check)

Bu belge, Kubernetes cluster'ındaki farklı componentlerin ve mikroservislerin (Pod'ların) stabil çalışıp çalışmadığını belirlemek için yapılan temel kontrolleri anlatır.

## 1. CrashLoop veya Container Oluşturma Hataları
Tüm namespace'lerde çalışmayan, restart loop'una girmiş pod'ların tespiti.
```bash
kubectl get pods --all-namespaces | grep -v 'Running\|Completed'
```
**Beklenen Durum:** `Pending`, `CrashLoopBackOff`, `ErrImagePull` veya `ImagePullBackOff` durumunda sürekli kalan pod'ların olmaması gerekir. Kısa süreli pending durumları normal olabilir.

## 2. Yakın Zamanda Aşırı Restart Atan Pod'lar
Pod'lar genel olarak "Running" durumunda olsa bile arka planda OOMKilled (Out Of Memory) veya panic sebebiyle sürekli yeniden başlıyor olabilir.
```bash
kubectl get pods --all-namespaces -o jsonpath="{range .items[*]}{.metadata.namespace}{'\t'}{.metadata.name}{'\t'}{.status.containerStatuses[*].restartCount}{'\n'}{end}" | awk '$3 > 2'
```
**Aksiyon:** Restart sayısı son birkaç saat içinde çok artmışsa uygulamanın neden çöktüğünü (loglarını ve OOM durumunu) inceleyin. `kubectl describe pod <pod-name> -n <ns>` komutunda "Last State" içerisinde "OOMKilled" ifadesi aranabilir.

## 3. Kaynak Tüketimi (Resource Consumption)
Limitlerine (Limits) ulaşmak üzere olan veya limitsiz (Unbound) yapılandırma nedeniyle diğer servisleri etkileyen pod'ların kontrolü.
```bash
kubectl top pods --all-namespaces
```
**Aksiyon:** Her bir namespace için en çok kaynak yiyen servisi tespit edip uygulamanın monitoring ekranlarından (Prometheus vb.) normal tüketim eğrisinde olup olmadığını doğrulayın.

## 4. Kritik Container Log Anormallikleri
Rastgele alınan kritik servislerin tail (kuyruk) loglarını okuyarak anormallik arama.
```bash
kubectl logs -l app=<kritik-servis-ad> -n <namespace> --tail=50
```
**Aksiyon:** Sürekli basılan `Error`, `Exception` veya `Timeout` loglarının kontrolü.
