---
title: Faiss Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Faiss Vektör Deposu

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-faiss
```

```bash
!pip install llama-index
```

#### Bir Faiss İndeksi Oluşturma

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
import faiss


# text-ada-embedding-002 boyutları
d = 1536
faiss_index = faiss.IndexFlatL2(d)
```

#### Belgeleri yükleyin, VectorStoreIndex'i oluşturun

```python
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.faiss import FaissVectorStore
from IPython.display import Markdown, display
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
# indeksi diske kaydet
index.storage_context.persist()
```

```python
# indeksi diskten yükle
vector_store = FaissVectorStore.from_persist_dir("./storage")
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir="./storage"
)
index = load_index_from_storage(storage_context=storage_context)
```

#### İndeksi Sorgulama

```python
# daha ayrıntılı çıktılar için Logging seviyesini DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

```python
# daha ayrıntılı çıktılar için Logging seviyesini DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query(
    "Yazar Y Combinator'daki zamanından sonra neler yaptı?"
)
```

```python
display(Markdown(f"<b>{response}</b>"))
```
