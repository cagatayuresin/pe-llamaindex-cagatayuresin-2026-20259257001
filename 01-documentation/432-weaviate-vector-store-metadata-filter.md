# Weaviate Vektör Deposu Meta Veri Filtresi

---
title: Weaviate Vektör Deposu Meta Veri Filtresi
 | LlamaIndex OSS Documentation
---

Bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```
%pip install llama-index-vector-stores-weaviate
```

```
!pip install llama-index weaviate-client
```

#### Weaviate İstemcisi Oluşturma

```
import os
import openai


os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.environ["OPENAI_API_KEY"]
```

```
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```
import weaviate


# cloud
cluster_url = ""
api_key = ""


client = weaviate.connect_to_wcs(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)


# local
# client = weaviate.connect_to_local()
```

```
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/meta "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/meta "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://pypi.org/pypi/weaviate-client/json "HTTP/1.1 200 OK"
HTTP Request: GET https://pypi.org/pypi/weaviate-client/json "HTTP/1.1 200 OK"
```

#### Belgeleri yükleme, VectorStoreIndex oluşturma

```
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from IPython.display import Markdown, display
```

## Meta Veri Filtreleme

Hadi sahte bir belge ekleyelim ve sadece o belgenin döndürülmesi için filtrelemeyi deneyelim.

```
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="The Shawshank Redemption",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
            "year": 1994,
        },
    ),
    TextNode(
        text="The Godfather",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
            "year": 1972,
        },
    ),
    TextNode(
        text="Inception",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Fiction",
            "year": 2010,
        },
    ),
    TextNode(
        text="To Kill a Mockingbird",
        metadata={
            "author": "Harper Lee",
            "theme": "Mafia",
            "year": 1960,
        },
    ),
    TextNode(
        text="1984",
        metadata={
            "author": "George Orwell",
            "theme": "Totalitarianism",
            "year": 1949,
        },
    ),
    TextNode(
        text="The Great Gatsby",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "The American Dream",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter and the Sorcerer's Stone",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Fiction",
            "year": 1997,
        },
    ),
]
```

```
from llama_index.core import StorageContext


vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex_filter"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

```
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 404 Not Found"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 404 Not Found"
INFO:httpx:HTTP Request: POST https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema "HTTP/1.1 200 OK"
HTTP Request: POST https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/nodes "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/nodes "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/nodes "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/nodes "HTTP/1.1 200 OK"
```

```
retriever = index.as_retriever()
retriever.retrieve("What is inception?")
```

```
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='df310070-1480-46c1-8ec0-1052c172905e', embedding=[...], metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0),
 NodeWithScore(node=TextNode(id_='b9a4dffd-b9f1-4d83-9c13-f4402d1036b8', embedding=[...], metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="Harry Potter and the Sorcerer's Stone", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0)]
```

```
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", operator=FilterOperator.EQ, value="Mafia"),
    ]
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("What is inception about?")
```

```
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='34d778a1-b6bf-4a24-a1bf-ac659a9959ea', embedding=[...], metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='The Godfather', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0),
 NodeWithScore(node=TextNode(id_='344a05a6-45e0-42eb-ab8e-9ae890a98d9d', embedding=[...], metadata={'author': 'Harper Lee', 'theme': 'Mafia', 'year': 1960}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='To Kill a Mockingbird', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0)]
```

```
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Mafia"),
        MetadataFilter(key="year", value=1972),
    ]
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("What is inception?")
```

```
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"










[NodeWithScore(node=TextNode(id_='34d778a1-b6bf-4a24-a1bf-ac659a9959ea', embedding=[...], metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='The Godfather', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0)]
```

```
from llama_index.core.vector_stores import FilterOperator, FilterCondition




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Fiction"),
        MetadataFilter(key="year", value=1997, operator=FilterOperator.GT),
    ],
    condition=FilterCondition.OR,
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Harry Potter?")
```

```
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"
HTTP Request: GET https://llamaindex-pythonv4-dhqgeqxq.weaviate.network/v1/schema/LlamaIndex_filter "HTTP/1.1 200 OK"










[NodeWithScore(node=TextNode(id_='b9a4dffd-b9f1-4d83-9c13-f4402d1036b8', embedding=[...], metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="Harry Potter and the Sorcerer's Stone", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0),
 NodeWithScore(node=TextNode(id_='df310070-1480-46c1-8ec0-1052c172905e', embedding=[...], metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Inception', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=1.0)]
```
