# Weaviate Vektör Deposu - Hibrit Arama

---
title: Weaviate Vektör Deposu - Hibrit Arama
 | LlamaIndex OSS Documentation
---

Bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```
%pip install llama-index-vector-stores-weaviate
```

```
!pip install llama-index
```

```
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

## Weaviate İstemcisi Oluşturma

```
import os
import openai


os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.environ["OPENAI_API_KEY"]
```

```
import weaviate
```

```
# Bulut örneğine bağlanma
cluster_url = ""
api_key = ""


client = weaviate.connect_to_wcs(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)


# Yerel örneğe bağlanma
# client = weaviate.connect_to_local()
```

```
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core.response.notebook_utils import display_response
```

## Verileri İndirme

```
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Belgeleri yükleme

```
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

## WeaviateVectorStore ile VectorStoreIndex Oluşturma

```
from llama_index.core import StorageContext




vector_store = WeaviateVectorStore(weaviate_client=client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)


# NOT: Dilerseniz manuel olarak bir index_name de tanımlayabilirsiniz.
 # index_name = "test_prefix"
 # vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)
```

## Varsayılan Vektör Araması ile İndeksi Sorgulama

```
# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine(similarity_top_k=2)
response = query_engine.query("What did the author do growing up?")
```

```
display_response(response)
```

## Hibrit Arama ile İndeksi Sorgulama

bm25 ve vektör ile hibrit aramayı kullanın.
 `alpha` parametresi ağırlıklandırmayı belirler (alpha = 0 -> bm25, alpha=1 -> vektör araması).

### Varsayılan olarak, `alpha=0.75` kullanılır (vektör aramasına çok benzer)

```
# daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=2
)
response = query_engine.query(
    "What did the author do growing up?",
)
```

```
display_response(response)
```

### Bm25'i tercih etmek için `alpha=0.` ayarlayın

```
# daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=2, alpha=0.0
)
response = query_engine.query(
    "What did the author do growing up?",
)
```

```
display_response(response)
```
