# Anyscale Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-anyscale
```

```python
!pip install llama-index
```

```python
# Anyscale API anahtarınızla başlatın
import os

os.environ["ANYSCALE_API_KEY"] = "your_token_here"
```

#### Anyscale embedding modellerini kullanma.

Anyscale, OpenAI uyumlu bir API üzerinden popüler açık kaynaklı embedding modellerine erişim sağlar.

```python
from llama_index.embeddings.anyscale import AnyscaleEmbedding

# Belirtecinizi özelleştirmek için şunu yapın
# aksi takdirde ortam değişkeninizden ANYSCALE_API_KEY'i arayacaktır
# embed_model = AnyscaleEmbedding(api_key="<anyscale_api_key>")

embed_model = AnyscaleEmbedding(
    model="thenlper/gte-large",  # veya desteklenen diğer modeller
)

embeddings = embed_model.get_text_embedding("Merhaba Anyscale!")

print(len(embeddings))
print(embeddings[:5])
```