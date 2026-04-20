# Mixedbread AI Embedding'leri

Özel kodlama formatları (binary, int, float, base64, vb.), embedding boyutları (Matryoshka) ve bağlam istemleri (context prompts) ile MixedBread AI'nın embedding modellerinin yeteneklerini keşfedin.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-mixedbreadai
```

```python
!pip install llama-index
```

```python
import os
from llama_index.embeddings.mixedbreadai import MixedbreadAIEmbedding
```

```python
# API Anahtarı ve Embedding Başlatma

# Bir API anahtarı almak için https://www.mixedbread.ai/api-reference#quick-start-guide
# adresini ziyaret edebilirsiniz
mixedbread_api_key = os.environ.get("MXBAI_API_KEY", "api-anahtarınız")

# Embedding modellerimiz için lütfen
# https://www.mixedbread.ai/docs/embeddings/models#whats-new-in-the-mixedbread-embed-model-family
# adresini kontrol edin
model_name = "mixedbread-ai/mxbai-embed-large-v1"
```

```python
oven = MixedbreadAIEmbedding(api_key=mixedbread_api_key, model_name=model_name)

embeddings = oven.get_query_embedding("Ekmek neden bu kadar lezzetli?")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.01128387451171875, 0.031097412109375, -0.00606536865234375, 0.0291748046875, -0.038604736328125]

### Bağlamsal embedding için istem (prompt) kullanma

İstem (prompt), embedding'in sonraki görevlerde nasıl kullanılacağına dair modelin anlayışını geliştirebilir ve bu da performansı artırır. Deneylerimiz, alana özgü (domain specific) istemlerin performansı artırabildiğini göstermektedir.

```python
prompt_for_retrieval = (
    "Represent this sentence for searching relevant passages:"
)

contextual_oven = MixedbreadAIEmbedding(
    api_key=mixedbread_api_key,
    model_name=model_name,
    prompt=prompt_for_retrieval,
)

contextual_embeddings = contextual_oven.get_query_embedding(
    "Almanya'da hangi ekmek icat edildi?"
)

print(len(contextual_embeddings))
print(contextual_embeddings[:5])
```

    1024
    [-0.0235443115234375, -0.0152435302734375, 0.008392333984375, 0.00336456298828125, -0.044647216796875]

## Kuantizasyon (Quantization) ve Matryoshka desteği

Mixedbread AI embedding'leri, performansı büyük ölçüde korurken daha iyi depolama için embedding boyutunu küçültmek amacıyla kuantizasyonu ve matryoshka'yı destekler. Daha fazla bilgi için şu yazılara bakabilirsiniz:

- [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization)
- [64 bytes per embedding, yee-haw](https://www.mixedbread.ai/blog/binary-mrl).

### Farklı kodlama formatlarını kullanma

Varsayılan `encoding_format` değeri `float`'tur. Ayrıca `float16`, `binary`, `ubinary`, `int8`, `uint8`, `base64` formatlarını da destekliyoruz.

```python
# `binary` embedding türleri ile
binary_oven = MixedbreadAIEmbedding(
    api_key=mixedbread_api_key,
    model_name=model_name,
    encoding_format="binary",
)

binary_embeddings = binary_oven.get_text_embedding(
    "Ekmek küçük ama yine de doyurucu!"
)

print(len(binary_embeddings))
print(binary_embeddings[:5])
```

    128
    [-121.0, 96.0, -108.0, 111.0, 110.0]

### Farklı embedding boyutlarını kullanma

Mixedbread AI embedding modelleri, Matryoshka boyut kısaltmasını (truncation) destekler. Varsayılan boyut, modelin maksimum değerine ayarlanmıştır. Hangi modellerin Matryoshka'yı desteklediğini görmek için web sitemizi takip edin.

```python
# kısaltılmış boyut ile
half_oven = MixedbreadAIEmbedding(
    api_key=mixedbread_api_key,
    model_name=model_name,
    dimensions=512,  # 1024, `mxbai-embed-large-v1` modelinin maksimum değeridir
)

half_embeddings = half_oven.get_text_embedding(
    "Ekmeğimin daha iyi olan yarısını istiyorum."
)

print(len(half_embeddings))
print(half_embeddings[:5])
```

    512
    [-0.014221191, -0.013671875, -0.03314209, 0.025909424, -0.035095215]