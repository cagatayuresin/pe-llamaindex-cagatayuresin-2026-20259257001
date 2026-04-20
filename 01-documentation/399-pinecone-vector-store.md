---
title: Pinecone Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Pinecone Vektör Deposu

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index llama-index-vector-stores-pinecone
```

```python
import logging
import sys
import os


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

#### Bir Pinecone İndeksi Oluşturma

```python
from pinecone import Pinecone, ServerlessSpec
```

```python
os.environ["PINECONE_API_KEY"] = "..."
os.environ["OPENAI_API_KEY"] = "sk-proj-..."


api_key = os.environ["PINECONE_API_KEY"]


pc = Pinecone(api_key=api_key)
```

```python
# gerekirse silin
# pc.delete_index("quickstart")
```

```python
# boyutlar text-embedding-ada-002 içindir


pc.create_index(
    name="quickstart",
    dimension=1536,
    metric="euclidean",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)


# Pod Tabanlı bir Pinecone indeksi oluşturmanız gerekiyorsa, alternatif olarak şunu yapabilirsiniz:
#
# from pinecone import Pinecone, PodSpec
#
# pc = Pinecone(api_key='xxx')
#
# pc.create_index(
#    name='my-index',
#    dimension=1536,
#    metric='cosine',
#    spec=PodSpec(
#      environment='us-east1-gcp',
#      pod_type='p1.x1',
#      pods=1
#    )
# )
```

```python
pinecone_index = pc.Index("quickstart")
```

#### Belgeleri yükleyin, PineconeVectorStore ve VectorStoreIndex'i oluşturun

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
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
# meta veri filtresi olmadan başlat
from llama_index.core import StorageContext


if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(f"OPENAI_API_KEY ortam değişkeni ayarlanmamış")


vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

İndeksin hazır olması bir dakika kadar sürebilir!

```python
# daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**"Yazar büyürken yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve ayrıca bir IBM 1401 bilgisayarında programlar yazmayı denedi. Daha sonra bir mikro bilgisayar edindi ve daha kapsamlı bir şekilde programlama yapmaya başlayarak basit oyunlar ve bir kelime işlemci yazdı."**

## Filtreleme

Ayrıca filtreler kullanarak doğrudan düğüm (node) listesi alabilirsiniz.

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
    FilterCondition,
)


filter = MetadataFilters(
    filters=[
        MetadataFilter(
            key="file_path",
            value="/Users/loganmarkewich/giant_change/llama_index/docs/examples/vector_stores/data/paul_graham/paul_graham_essay.txt",
            operator=FilterOperator.EQ,
        )
    ],
    condition=FilterCondition.AND,
)
```

Düğümleri doğrudan filtrelerle alabilirsiniz. Aşağıdaki işlem, filtreyle eşleşen tüm düğümleri döndürecektir.

```python
nodes = vector_store.get_nodes(filters=filter, limit=100)
print(len(nodes))
```

**22**

Filtreler ve top-k kullanarak da veri getirebilirsiniz.

```python
query_engine = index.as_query_engine(similarity_top_k=2, filters=filter)
response = query_engine.query("Yazar büyürken neler yaptı?")
print(len(response.source_nodes))
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2
```
