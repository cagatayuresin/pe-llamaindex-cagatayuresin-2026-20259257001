# Amazon Neptune - Neptune Analytics Vektör Deposu (Vector Store)

---
title: Amazon Neptune - Neptune Analytics Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-neptune
```

## Neptune Analytics Vektör Sarmalayıcısını (Wrapper) Başlatma

```python
from llama_index.vector_stores.neptune import NeptuneAnalyticsVectorStore


graph_identifier = "" # Grafik tanımlayıcısını buraya girin
embed_dim = 1536


neptune_vector_store = NeptuneAnalyticsVectorStore(
    graph_identifier=graph_identifier, embedding_dimension=1536
)
```

## Belgeleri Yükleme, VectorStoreIndex Oluşturma

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from IPython.display import Markdown, display
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```python
from llama_index.core import StorageContext


storage_context = StorageContext.from_defaults(
    vector_store=neptune_vector_store
)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Interleaf'te ne oldu?")
display(Markdown(f"<b>{response}</b>"))
```
