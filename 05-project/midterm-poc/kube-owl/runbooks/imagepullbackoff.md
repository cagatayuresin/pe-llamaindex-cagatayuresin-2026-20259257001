# ImagePullBackOff Troubleshooting Runbook

## Belirtiler
- Pod durumu: ImagePullBackOff veya ErrImagePull
- Container başlatılamıyor, image çekilemiyor
- Pod READY sütununda 0/1 gösteriyor
- Events'te "Failed to pull image" mesajı var

## Olası Nedenler
1. **Yanlış Image Tag:** Belirtilen tag registry'de mevcut değil
2. **Registry Authentication:** Private registry için credentials eksik
3. **Network Sorunu:** Node'lar registry'ye erişemiyor
4. **Rate Limiting:** Docker Hub veya başka registry rate limit'e takılmış
5. **Registry Kapalı:** Registry sunucusu erişilemez durumda
6. **Typo:** Image adında yazım hatası var

## Teşhis Adımları

### Adım 1: Pod Durumunu Kontrol Et
Komut: `kubectl get pods -n <namespace>`
Kontrol: STATUS sütununda ImagePullBackOff veya ErrImagePull

### Adım 2: Pod Detaylarını İncele
Komut: `kubectl describe pod <pod-name> -n <namespace>`
Kontrol:
- Events bölümünde hata mesajı (tam hata metnini oku)
- Image adı ve tag'i
- ImagePullSecrets ayarı

### Adım 3: Image Adını Doğrula
- Registry'de image ve tag var mı kontrol et
- Tag'in doğru yazıldığından emin ol (büyük/küçük harf duyarlı)
- "latest" yerine spesifik tag kullanılması önerilir

### Adım 4: Registry Bağlantısını Test Et
- Node üzerinden registry'ye curl/wget ile bağlanmayı dene
- DNS çözümleme çalışıyor mu kontrol et
- Firewall kurallarını kontrol et

### Adım 5: Secret Kontrolü
Komut: `kubectl get secrets -n <namespace>`
Kontrol: Image pull secret tanımlı mı? Doğru secret adı kullanılıyor mu?

## Çözümler

### Yanlış Tag İçin
- Doğru tag'i belirle:
  - Registry UI'ından mevcut tag'leri kontrol et
  - `docker pull <image>:<tag>` ile lokal olarak test et
- Deployment'ı doğru tag ile güncelle:
  - `kubectl set image deployment/<name> <container>=<image>:<correct-tag> -n <ns>`

### Private Registry Authentication İçin
1. Docker registry secret oluştur:
   ```
   kubectl create secret docker-registry my-registry-secret \
     --docker-server=<registry-url> \
     --docker-username=<user> \
     --docker-password=<pass> \
     --docker-email=<email> \
     -n <namespace>
   ```
2. Deployment/Pod spec'ine imagePullSecrets ekle:
   ```yaml
   spec:
     imagePullSecrets:
       - name: my-registry-secret
   ```

### Network Sorunu İçin
- Node'ların DNS çözümleme yapabildiğini doğrula
- Proxy ayarlarını kontrol et (HTTP_PROXY, HTTPS_PROXY)
- Docker daemon'ın proxy ayarlarını kontrol et
- Air-gapped ortamda: image'ları önceden node'lara yükle

### Docker Hub Rate Limit İçin
- Authenticated pull kullan (ücretsiz hesap bile limiti artırır)
- Mirror/cache registry kur
- Sık kullanılan image'ları kendi registry'nize kopyalayın

### Registry Kapalıysa
- Registry servisinin çalıştığını doğrula
- Load balancer / ingress durumunu kontrol et
- SSL sertifika süresi dolmuş olabilir

## İlgili Komutlar
- `kubectl get pods -n <namespace>` — Pod durumlarını listele
- `kubectl describe pod <pod-name> -n <namespace>` — Pod detayları
- `kubectl get secrets -n <namespace>` — Secret'ları listele
- `kubectl get events -n <namespace> --sort-by=.lastTimestamp` — Son event'ler
