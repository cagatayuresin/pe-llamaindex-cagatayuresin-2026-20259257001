# Netmind AI Embedding'leri

Bu not defteri, embedding işlemleri için `Netmind AI`'nın nasıl kullanılacağını gösterir.

Bir API anahtarı almak için https://www.netmind.ai/ adresini ziyaret edin ve kaydolun.

## Kurulum

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-netmind
```

```python
!pip install llama-index
```

```python
# API anahtarını embedding modelinde veya ortam değişkenlerinde (env) ayarlayabilirsiniz
# import os
# os.environ["NETMIND_API_KEY"] = "api-anahtarınız"

from llama_index.embeddings.netmind import NetmindEmbedding

embed_model = NetmindEmbedding(
    model_name="BAAI/bge-m3", api_key="api-anahtarınız"
)
```

## Embedding'leri Al

```python
embeddings = embed_model.get_text_embedding("merhaba dünya")
```

```python
print(len(embeddings))
```

    1024

```python
print(embeddings[:5])
```

    [-0.04039396345615387, 0.03703497350215912, -0.02897450141608715, 0.016117244958877563, -0.03569157049059868]