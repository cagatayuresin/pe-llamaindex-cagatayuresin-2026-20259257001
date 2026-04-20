# TextEmbed - Gömme Çıkarım Sunucusu (Embedding Inference Server)

Keval Dekivadiya tarafından sürdürülen TextEmbed, [Apache-2.0 Lisansı](https://opensource.org/licenses/Apache-2.0) altında lisanslanmıştır.

TextEmbed, vektör gömmelerini (embeddings) sunmak için tasarlanmış yüksek veri çıkışlı, düşük gecikmeli bir REST API'dir. Çok çeşitli sentence-transformer modellerini ve çerçevelerini destekleyerek doğal dil işlemedeki çeşitli uygulamalar için uygun hale getirir.

## Özellikler

- **Yüksek Veri Çıkışı ve Düşük Gecikme**: Çok sayıda isteği verimli bir şekilde işlemek için tasarlanmıştır.
- **Esnek Model Desteği**: Çeşitli sentence-transformer modelleriyle çalışır.
- **Ölçeklenebilir**: Daha büyük sistemlere kolayca entegre olur ve talebe göre ölçeklenir.
- **Toplu İşlem (Batch Processing)**: Daha iyi ve daha hızlı çıkarım için toplu işlemeyi destekler.
- **OpenAI Uyumlu REST API Uç Noktası**: OpenAI uyumlu bir REST API uç noktası sağlar.
- **Tek Satırlık Komutla Dağıtım**: Verimli dağıtım için tek bir komutla birden fazla modeli dağıtın.
- **Gömme Formatları Desteği**: Daha hızlı geri çağırma için binary, float16 ve float32 gömme formatlarını destekler.

## Başlarken

### Ön Koşullar

Python 3.10 veya daha yüksek bir sürümün kurulu olduğundan emin olun. Ayrıca gerekli bağımlılıkları kurmanız gerekecektir.

### PyPI üzerinden Kurulum

Gerekli bağımlılıkları kurun:

```python
!pip install -U textembed
```

### TextEmbed Sunucusunu Başlatma

İstediğiniz modellerle TextEmbed sunucusunu başlatın:

```python
!python -m textembed.server --models sentence-transformers/all-MiniLM-L12-v2 --workers 4 --api-key TextEmbed
```

### llama-index ile Örnek Kullanım

İşte llama-index ile başlamanıza yardımcı olacak basit bir örnek:

```python
from llama_index.embeddings.textembed import TextEmbedEmbedding

# TextEmbedEmbedding sınıfını başlatın
embed = TextEmbedEmbedding(
    model_name="sentence-transformers/all-MiniLM-L12-v2",
    base_url="http://0.0.0.0:8000/v1",
    auth_token="TextEmbed",
)

# Bir grup metin için gömmeleri alın
embeddings = embed.get_text_embedding_batch(
    [
        "Burada bardaktan boşalırcasına yağmur yağıyor!",
        "Hindistan zengin bir kültürel mirasa sahiptir.",
    ]
)

print(embeddings)
```

    [[0.07680495083332062, -0. ...044137585908174515]]

Daha fazla bilgi için lütfen [dokümantasyonu](https://github.com/kevaldekivadiya2415/textembed/blob/main/docs/setup.md) okuyun.
