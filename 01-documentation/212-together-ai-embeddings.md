# Together AI Gömmeleri (Embeddings)

Bu not defteri, gömmeler (embeddings) için `Together AI`ın nasıl kullanılacağını gösterir. Together AI, pek çok son teknoloji gömme modeline erişim sağlar.

https://together.ai adresini ziyaret edin ve bir API anahtarı almak için kaydolun.

## Kurulum

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-together
```

```python
!pip install llama-index
```

```python
# API anahtarını doğrudan sınıfta veya ortam değişkenlerinde (env) ayarlayabilirsiniz
# import os
# os.environ["TOGETHER_API_KEY"] = "api-anahtarınız"

from llama_index.embeddings.together import TogetherEmbedding

embed_model = TogetherEmbedding(
    model_name="togethercomputer/m2-bert-80M-8k-retrieval", api_key="..."
)
```

## Gömmeleri Al (Get Embeddings)

```python
embeddings = embed_model.get_text_embedding("merhaba dünya")
```

```python
print(len(embeddings))
```

    768

```python
print(embeddings[:5])
```

    [-0.11657876, -0.012690996, 0.24342081, 0.32781482, 0.022501636]
