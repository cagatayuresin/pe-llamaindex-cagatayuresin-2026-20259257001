# ModelScope Embedding'leri

Bu not defterinde, LlamaIndex'te ModelScope Embedding'lerinin nasıl kullanılacağını gösteriyoruz. [ModelScope sitesine](https://www.modelscope.cn/) göz atın.

Bu not defterini Colab'da açıyorsanız, LlamaIndex'i 🦙 ve `modelscope` paketini kurmanız gerekecektir.

```python
!pip install llama-index-embeddings-modelscope
```

## Temel Kullanım

```python
import sys
from llama_index.embeddings.modelscope.base import ModelScopeEmbedding

model = ModelScopeEmbedding(
    model_name="iic/nlp_gte_sentence-embedding_chinese-base",
    model_revision="master",
)

rsp = model.get_query_embedding("Merhaba, kimsin?")
print(rsp)

rsp = model.get_text_embedding("Merhaba, kimsin?")
print(rsp)
```

#### Toplu (Batch) Embedding Oluşturma

```python
from llama_index.embeddings.modelscope.base import ModelScopeEmbedding

model = ModelScopeEmbedding(
    model_name="iic/nlp_gte_sentence-embedding_chinese-base",
    model_revision="master",
)

rsp = model.get_text_embedding_batch(
    ["Merhaba, kimsin?", "Ben bir öğrenciyim."]
)
print(rsp)
```