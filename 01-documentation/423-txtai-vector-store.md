# txtai Vector Store

---
title: txtai Vector Store
 | LlamaIndex OSS Documentation
---

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```
%pip install llama-index-vector-stores-txtai
```

```
!pip install llama-index
```

#### txtai İndeksi Oluşturma

```
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```
import txtai


# Create txtai ann index
txtai_index = txtai.ann.ANNFactory.create({"backend": "numpy"})
```

#### Belgeleri yükleme, VectorStoreIndex oluşturma

```
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.txtai import TxtaiVectorStore
from IPython.display import Markdown, display
```

Veri İndirme

```
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```
# load documents
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```
vector_store = TxtaiVectorStore(txtai_index=txtai_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```
# save index to disk
index.storage_context.persist()
```

```
# load index from disk
vector_store = TxtaiVectorStore.from_persist_dir("./storage")
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir="./storage"
)
index = load_index_from_storage(storage_context=storage_context)
```

#### İndeksi Sorgulama

```
# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
```

```
display(Markdown(f"<b>{response}</b>"))
```

```
# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query(
    "What did the author do after his time at Y Combinator?"
)
```

```
display(Markdown(f"<b>{response}</b>"))
```
