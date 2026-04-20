# Bedrock Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-bedrock
```

```python
import os

from llama_index.embeddings.bedrock import BedrockEmbedding
```

```python
embed_model = BedrockEmbedding(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name="<aws-region>",
    profile_name="<aws-profile>",
)
```

```python
embedding = embed_model.get_text_embedding("merhaba dünya")
```

## Desteklenen Modelleri Listeleme

Amazon Bedrock'un LlamaIndex üzerinde desteklenen modellerinin listesini kontrol etmek için `BedrockEmbedding.list_supported_models()` yöntemini aşağıdaki gibi çağırın.

```python
from llama_index.embeddings.bedrock import BedrockEmbedding
import json

supported_models = BedrockEmbedding.list_supported_models()
print(json.dumps(supported_models, indent=2))
```

## Sağlayıcı: Amazon
Amazon Bedrock Titan embedding'leri.

```python
from llama_index.embeddings.bedrock import BedrockEmbedding

model = BedrockEmbedding(model_name="amazon.titan-embed-g1-text-02")
embeddings = model.get_text_embedding("merhaba dünya")
print(embeddings)
```

## Sağlayıcı: Cohere

### cohere.embed-english-v3

```python
model = BedrockEmbedding(model_name="cohere.embed-english-v3")
coherePayload = ["Bu bir test dökümanıdır", "Bu başka bir test dökümanıdır"]

embed1 = model.get_text_embedding("Bu bir test dökümanıdır")
print(embed1)

embeddings = model.get_text_embedding_batch(coherePayload)
print(embeddings)
```

### Cohere'den Çok Dilli (MultiLingual) Embedding'ler

```python
model = BedrockEmbedding(model_name="cohere.embed-multilingual-v3")
coherePayload = [
    "This is a test document",
    "తెలుగు అనేది ద్రావిడ భాషల కుటుంబానికి చెందిన భాష.",
    "Esto es una prueba de documento multilingüe.",
    "攻殻機動隊",
    "Combien de temps ça va prendre ?",
    "Документ проверен",
]
embeddings = model.get_text_embedding_batch(coherePayload)
print(embeddings)
```