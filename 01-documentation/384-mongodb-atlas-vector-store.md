---
title: MongoDB Atlas Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# MongoDB Atlas Vektör Deposu

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-mongodb
```

```bash
!pip install llama-index
```

```python
# Kurucuya (constructor) URI sağlayın veya ortam değişkeni kullanın
import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
```

Veriyi İndir

```bash
!mkdir -p 'data/10k/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf' -O 'data/10k/uber_2021.pdf'
```

```python
# mongo_uri = os.environ["MONGO_URI"]
mongo_uri = (
    "mongodb+srv://<kullaniciadi>:<sifre>@<host>?retryWrites=true&w=majority"
)
mongodb_client = pymongo.MongoClient(mongo_uri)
async_mongodb_client = pymongo.AsyncMongoClient(mongo_uri)


store = MongoDBAtlasVectorSearch(
    mongodb_client=mongodb_client, async_mongodb_client=async_mongodb_client
)
store.create_vector_search_index(
    dimensions=1536, path="embedding", similarity="cosine"
)
storage_context = StorageContext.from_defaults(vector_store=store)
uber_docs = SimpleDirectoryReader(
    input_files=["./data/10k/uber_2021.pdf"]
).load_data()
index = VectorStoreIndex.from_documents(
    uber_docs, storage_context=storage_context
)
```

```python
response = index.as_query_engine().query("Uber'in geliri ne kadardı?")
display(Markdown(f"<b>{response}</b>"))
```

**Uber'in 2021 yılı geliri 17.455 milyon dolardı.**

```python
from llama_index.core import Response


# Başlangıç boyutu
print(store._collection.count_documents({}))

# Bir ref_doc_id al
typed_response = (
    response if isinstance(response, Response) else response.get_response()
)
ref_doc_id = typed_response.source_nodes[0].node.ref_doc_id
print(store._collection.count_documents({"metadata.ref_doc_id": ref_doc_id}))

# Depo silme testi
if ref_doc_id:
    store.delete(ref_doc_id)
    print(store._collection.count_documents({}))
```
