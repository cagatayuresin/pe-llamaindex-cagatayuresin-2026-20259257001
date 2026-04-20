# Qdrant FastEmbed Embedding'leri

LlamaIndex, embedding oluşturma için [FastEmbed](https://qdrant.github.io/fastembed/)'i destekler.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-fastembed
```

```python
%pip install llama-index
```

Bu sağlayıcıyı kullanmak için `fastembed` paketinin kurulu olması gerekir.

```python
%pip install fastembed
```

Desteklenen modellerin listesi [burada](https://qdrant.github.io/fastembed/examples/Supported_Models/) bulunabilir.

```python
from llama_index.embeddings.fastembed import FastEmbedEmbedding

embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

    100%|██████████| 76.7M/76.7M [00:18<00:00, 4.23MiB/s]

```python
embeddings = embed_model.get_text_embedding("Gömülecek (embed edilecek) bazı metinler.")
print(len(embeddings))
print(embeddings[:5])
```

    384
    [-0.04166769981384277, 0.0018720313673838973, 0.02632238157093525, -0.036030545830726624, -0.014812108129262924]