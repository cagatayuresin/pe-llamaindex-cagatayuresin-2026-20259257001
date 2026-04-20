# Baseten Embedding'leri

Bu kılavuz, Baseten [kütüphanesindeki](https://www.baseten.co/library/tag/embedding/) yüksek performanslı açık kaynaklı embedding'lerin ve yeniden sıralayıcıların (rerankers) nasıl kullanılacağını göstermektedir. Öncelikle LlamaIndex'i ve Baseten bağımlılıklarını kurmamız gerekiyor.

```python
%pip install llama-index llama-index-embeddings-baseten
```

[Buradan](https://www.baseten.co/library/tag/embedding/) istediğiniz embedding ile seçtiğiniz özel bir uç nokta (endpoint) başlatın ve Baseten API anahtarınızı aşağıya yapıştırın.

```python
from llama_index.embeddings.baseten import BasetenEmbedding
```

```python
# Özel uç nokta (dedicated endpoint) kullanma
embed_model = BasetenEmbedding(
    model_id="BASETEN_MODEL_ID",  # 8 karakterlik dizge
    api_key="BASETEN_API_KEY",
)

# Tekil embedding
embedding = embed_model.get_text_embedding("Merhaba dünya!")

# Toplu (batch) embedding'ler
embeddings = embed_model.get_text_embedding_batch(
    ["Merhaba dünya!", "Hoşça kal dünya!"]
)
print(embeddings)
```

    [[-0.006763149984180927, ... -0.08139033801853657]]
