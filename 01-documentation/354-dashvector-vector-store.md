---
title: DashVector Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# DashVector Vektör Deposu

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-dashvector
```

```bash
!pip install llama-index
```

```python
import logging
import sys
import os


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

#### Bir DashVector Koleksiyonu Oluşturma

```python
import dashvector
```

```python
api_key = os.environ["DASHVECTOR_API_KEY"]
client = dashvector.Client(api_key=api_key)
```

```python
# boyutlar text-embedding-ada-002 içindir
client.create("llama-demo", dimension=1536)
```

```json
{"code": 0, "message": "", "requests_id": "82b969d2-2568-4e18-b0dc-aa159b503c84"}
```

```python
dashvector_collection = client.get("quickstart")
```

#### Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Belgeleri yükleme, DashVectorStore ve VectorStoreIndex oluşturma

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.dashvector import DashVectorStore
from IPython.display import Markdown, display
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```python
# meta veri filtresi olmadan başlat
from llama_index.core import StorageContext


vector_store = DashVectorStore(dashvector_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

```python
# Daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, okul dışında yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve IBM 1401 bilgisayarında programlar yazmayı denedi. Ayrıca bir mikrobilgisayar yaptı ve üzerinde programlama yapmaya başlayarak basit oyunlar ve bir kelime işlemci yazdı.**
