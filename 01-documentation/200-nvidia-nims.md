# NVIDIA NIM'ler (NIMs)

`llama-index-embeddings-nvidia` paketi, NVIDIA NIM çıkarım mikro hizmetindeki modellerle uygulama oluşturmak için LlamaIndex entegrasyonlarını içerir. NIM; topluluktan ve NVIDIA'dan sohbet, gömme (embedding) ve yeniden sıralama (re-ranking) modelleri gibi alanlardaki modelleri destekler. Bu modeller, NVIDIA tarafından NVIDIA hızlandırılmış altyapısında en iyi performansı sunacak şekilde optimize edilmiştir ve NVIDIA hızlandırılmış altyapısında tek bir komutla her yere dağıtılabilen, kullanımı kolay, önceden oluşturulmuş konteynerler olan NIM olarak sunulur.

NIM'lerin NVIDIA tarafından barındırılan sürümleri [NVIDIA API kataloğu](https://build.nvidia.com/) üzerinden test edilebilir. Testten sonra NIM'ler, NVIDIA AI Enterprise lisansı kullanılarak NVIDIA'nın API kataloğundan dışa aktarılabilir ve şirket içinde veya bulutta çalıştırılarak işletmelere fikri mülkiyetleri ve AI uygulamaları üzerinde sahiplik ve tam kontrol sağlar.

NIM'ler, model bazında konteyner imajları olarak paketlenir ve NVIDIA NGC Kataloğu aracılığıyla NGC konteyner imajları olarak dağıtılır. Özünde NIM'ler, bir yapay zeka modeli üzerinde çıkarım yapmak için kolay, tutarlı ve tanıdık API'ler sağlar.

## Kurulum

```python
%pip install --upgrade --quiet llama-index-embeddings-nvidia
```

## Kurulum ve Hazırlık

**Başlamak için:**

1. NVIDIA AI Foundation modellerini barındıran [NVIDIA](https://build.nvidia.com/) ile ücretsiz bir hesap oluşturun.

2. `Retrieval` (Geri getirme) sekmesini seçin, ardından istediğiniz modeli seçin.

3. `Input` (Giriş) altında `Python` sekmesini seçin ve `Get API Key` (API Anahtarı Al) düğmesine tıklayın. Ardından `Generate Key` (Anahtar Oluştur) düğmesine tıklayın.

4. Oluşturulan anahtarı kopyalayın ve `NVIDIA_API_KEY` olarak kaydedin. Buradan uç noktalara (endpoints) erişebiliyor olmalısınız.

```python
import getpass
import os

# os.environ['NVIDIA_API_KEY'] = '<anahtarınız>'  ## anahtarı silmek ve sıfırlamak için
if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    print("Geçerli NVIDIA_API_KEY zaten ortamda mevcut. Sıfırlamak için silin.")
else:
    nvapi_key = getpass.getpass("NVAPI Anahtarı (nvapi- ile başlar): ")
    assert nvapi_key.startswith(
        "nvapi-"
    ), f"{nvapi_key[:5]}... geçerli bir anahtar değil"
    os.environ["NVIDIA_API_KEY"] = nvapi_key
```

## NVIDIA API Kataloğu ile Çalışma

Bir gömme (embedding) modeli başlatırken, bir model ismi geçirerek (örneğin, `NV-Embed-QA`) bir model seçebilir veya herhangi bir parametre geçirmeyerek varsayılanı kullanabilirsiniz.

```python
from llama_index.embeddings.nvidia import NVIDIAEmbedding

embedder = NVIDIAEmbedding(model="NV-Embed-QA")
```

Bu model, aşağıdakiler dahil beklenen [`Embeddings`](https://docs.llamaindex.ai/en/stable/api_reference/embeddings/) yöntemlerini destekleyen, ince ayar yapılmış bir E5-large modelidir:

- `get_query_embedding`: Bir sorgu örneği için sorgu gömmesi oluşturur.

- `get_text_embedding_batch`: Arama yapmak istediğiniz belgelerin listesi için metin gömmeleri oluşturur.

- Ve yukarıdakilerin asenkron versiyonları.

## NVIDIA NIM'ler ile Çalışma

Barındırılan [NVIDIA NIM'lere](https://ai.nvidia.com) bağlanmanın yanı sıra, bu bağlayıcı yerel NIM örneklerine bağlanmak için de kullanılabilir. Bu, gerektiğinde uygulamalarınızı yerelleştirmenize yardımcı olur.

Yerel NIM örneklerinin nasıl kurulacağına ilişkin talimatlar için [NVIDIA NIM](https://developer.nvidia.com/nim) sayfasına bakın.

```python
from llama_index.embeddings.nvidia import NVIDIAEmbedding

# localhost:8080 adresinde çalışan bir gömme (embedding) NIM'ine bağlanın
embedder = NVIDIAEmbedding(base_url="http://localhost:8080/v1")
embedder.available_models
```

    /home/raspawar/Desktop/llama_index/llama-index-integrations/embeddings/llama-index-embeddings-nvidia/llama_index/embeddings/nvidia/base.py:161: UserWarning: Varsayılan model şu şekilde ayarlandı: NV-Embed-QA. 
    Model parametresini kullanarak modeli ayarlayın. 
    Kullanılabilir modelleri almak için available_models özelliğini kullanın.
      warnings.warn(

    [Model(id='NV-Embed-QA', base_model=None)]

### **Benzerlik (Similarity)**

Aşağıdaki veriler için benzerliğin hızlı bir testi verilmiştir:

**Sorgular:**

- Kamçatka'da hava nasıl?

- İtalya hangi yemekleriyle tanınır?

- Benim adım ne? Hatırlamadığına bahse girerim...

- Hayatın amacı nedir ki?

- Hayatın amacı eğlenmektir :D

**Metinler:**

- Kamçatka'nın havası soğuktur, kışlar uzun ve sert geçer.

- İtalya makarna, pizza, dondurma (gelato) ve espresso ile ünlüdür.

- Kişisel isimleri hatırlayamam, sadece bilgi sağlayabilirim.

- Hayatın amacı değişir, genellikle kişisel tatmin olarak görülür.

- Hayatın anlarının tadını çıkarmak gerçekten harika bir yaklaşımdır.

### Sorguları Gömme (Embed queries)

```python
print("\nSıralı Gömme (Sequential Embedding): ")
q_embeddings = [
    embedder.get_query_embedding("Kamçatka'da hava nasıl?"),
    embedder.get_query_embedding("İtalya hangi yemekleriyle tanınır?"),
    embedder.get_query_embedding(
        "Benim adım ne? Hatırlamadığına bahse girerim..."
    ),
    embedder.get_query_embedding("Hayatın amacı nedir ki?"),
    embedder.get_query_embedding("Hayatın amacı eğlenmektir :D"),
]
print("Boyut (Shape):", (len(q_embeddings), len(q_embeddings[0])))
```

### Belgeleri Gömme (Embed documents)

```python
print("\nToplu Belge Gömme (Batch Document Embedding): ")
d_embeddings = embedder.get_text_embedding_batch(
    [
        "Kamçatka'nın havası soğuktur, kışlar uzun ve sert geçer.",
        "İtalya makarna, pizza, dondurma (gelato) ve espresso ile ünlüdür.",
        "Kişisel isimleri hatırlayamam, sadece bilgi sağlayabilirim.",
        "Hayatın amacı değişir, genellikle kişisel tatmin olarak görülür.",
        "Hayatın anlarının tadını çıkarmak gerçekten harika bir yaklaşımdır.",
    ]
)
print("Boyut (Shape):", (len(d_embeddings), len(d_embeddings[0])))
```

Artık gömmelerimizi oluşturduğumuza göre, bir geri çağırma (retrieval) görevinde hangi belgelerin makul yanıtlar olarak tetikleneceğini görmek için sonuçlar üzerinde basit bir benzerlik kontrolü yapabiliriz:

```python
%pip install --upgrade --quiet matplotlib scikit-learn
```

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# q_embeddings ve d_embeddings arasındaki benzerlik matrisini hesaplayın
cross_similarity_matrix = cosine_similarity(
    np.array(q_embeddings),
    np.array(d_embeddings),
)

# Çapraz benzerlik matrisini çizdirme
plt.figure(figsize=(8, 6))
plt.imshow(cross_similarity_matrix, cmap="Greens", interpolation="nearest")
plt.colorbar()
plt.title("Çapraz Benzerlik Matrisi")
plt.xlabel("Sorgu Gömmeleri")
plt.ylabel("Belge Gömmeleri")
plt.grid(True)
plt.show()
```

Hatırlatmak gerekirse, sisteme gönderilen sorgular ve belgeler şunlardı:

**Sorgular:**

- Kamçatka'da hava nasıl?

- İtalya hangi yemekleriyle tanınır?

- Benim adım ne? Hatırlamadığına bahse girerim...

- Hayatın amacı nedir ki?

- Hayatın amacı eğlenmektir :D

**Metinler:**

- Kamçatka'nın havası soğuktur, kışlar uzun ve sert geçer.

- İtalya makarna, pizza, dondurma (gelato) ve espresso ile ünlüdür.

- Kişisel isimleri hatırlayamam, sadece bilgi sağlayabilirim.

- Hayatın amacı değişir, genellikle kişisel tatmin olarak görülür.

- Hayatın anlarının tadını çıkarmak gerçekten harika bir yaklaşımdır.

## Kırpma (Truncation)

Gömme modelleri genellikle, gömülebilecek maksimum giriş belirteci (token) sayısını belirleyen sabit bir bağlam penceresine sahiptir. Bu sınır, modelin maksimum giriş belirteci uzunluğuna eşit sert bir sınır veya gömmenin doğruluğunun azaldığı etkili bir sınır olabilir.

Modeller belirteçler üzerinde çalıştığı ve uygulamalar genellikle metinlerle çalıştığı için, bir uygulamanın girişinin modelin belirteç sınırları içinde kalmasını sağlamak zor olabilir. Varsayılan olarak, giriş çok büyükse bir istisna (exception) fırlatılır.

Buna yardımcı olmak için NVIDIA NIM'ler, giriş çok büyükse sunucu tarafında girişi kırpan bir `truncate` (kırp) parametresi sağlar.

`truncate` parametresinin üç seçeneği vardır:
 - "NONE": Varsayılan seçenek. Giriş çok büyükse bir istisna fırlatılır.
 - "START": Sunucu, girişi başlangıçtan (soldan) kırpar ve gerektiğinde belirteçleri atar.
 - "END": Sunucu, girişi sondan (sağdan) kırpar ve gerektiğinde belirteçleri atar.

```python
long_text = "AI is amazing, amazing is " * 100
```

```python
strict_embedder = NVIDIAEmbedding()
try:
    strict_embedder.get_query_embedding(long_text)
except Exception as e:
    print("Hata:", e)
```

```python
truncating_embedder = NVIDIAEmbedding(truncate="END")
truncating_embedder.get_query_embedding(long_text)[:5]
```
