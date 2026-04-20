# Databricks Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index
%pip install llama-index-embeddings-databricks
```

```python
import os
from llama_index.core import Settings
from llama_index.embeddings.databricks import DatabricksEmbedding
```

```python
# Gerekli model, API anahtarı ve servis uç noktası (serving endpoint) ile DatabricksEmbedding sınıfını kurun
os.environ["DATABRICKS_TOKEN"] = "<BELIRTECIM>"
os.environ["DATABRICKS_SERVING_ENDPOINT"] = "<UC_NOKTAM>"
embed_model = DatabricksEmbedding(model="databricks-bge-large-en")
Settings.embed_model = embed_model
```

```python
# Biraz metin gömün (embedding oluşturun)
embeddings = embed_model.get_text_embedding(
    "DatabricksEmbedding entegrasyonu harika çalışıyor."
)
```