# Fireworks Embedding'leri

Bu kılavuz, [Fireworks Endpoints](https://readme.fireworks.ai/) aracılığıyla Fireworks Embedding'lerinin nasıl kullanılacağını gösterir.

Öncelikle LlamaIndex'i ve Fireworks bağımlılıklarını kuralım.

```python
%pip install llama-index-embeddings-fireworks
```

```python
!pip install llama-index
```

Artık Fireworks üzerinde embedding sorgulaması yapabiliriz.

```python
from llama_index.embeddings.fireworks import FireworksEmbedding

embed_model = FireworksEmbedding(api_key="API ANAHTARINIZ", embed_batch_size=10)
```

```python
# Temel embedding örneği
embeddings = embed_model.get_text_embedding("Ay'a nasıl yelken açarım?")
print(len(embeddings), embeddings[:10])
```

    768 [-0.67973792552948, 1.5226128101348877, -3.9547336101531982, 0.3112764358520508, -0.19723102450370789, 1.8839401006698608, -1.1595842838287354, -0.20612922310829163, 0.16740809381008148, -0.9071207046508789]