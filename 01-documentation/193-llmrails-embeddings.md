# LLMRails Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-llm-rails
```

```python
!pip install llama-index
```

```python
# içe aktarmalar

from llama_index.embeddings.llm_rails import LLMRailsEmbedding
```

```python
# kimlik bilgilerini al ve embedding'leri oluştur

import os

api_key = os.environ.get("API_KEY", "api-anahtarınız")
model_id = os.environ.get("MODEL_ID", "model-id-niz")


embed_model = LLMRailsEmbedding(model_id=model_id, api_key=api_key)

embeddings = embed_model.get_text_embedding(
    "Burada bardaktan boşalırcasına yağmur yağıyor!"
)
```