---
title: Pinecone Vektör Deposu - Meta Veri Filtreleme
 | LlamaIndex OSS Belgeleri
---

# Pinecone Vektör Deposu - Meta Veri Filtreleme

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-pinecone
```

```bash
# !pip install llama-index>=0.9.31 pinecone-client>=3.0.0
```

```python
import logging
import sys
import os


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
import os


os.environ[
    "PINECONE_API_KEY"
] = "<Pinecone API anahtarınız, app.pinecone.io adresinden alınır>"
os.environ["OPENAI_API_KEY"] = "sk-..."
```

Bir Pinecone İndeksi oluşturun ve ona bağlanın

```python
from pinecone import Pinecone
from pinecone import ServerlessSpec


api_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=api_key)
```

```python
# gerekirse silin
# pc.delete_index("quickstart-index")
```

```python
# Boyutlar text-embedding-ada-002 içindir
pc.create_index(
    "quickstart-index",
    dimension=1536,
    metric="euclidean",
    spec=ServerlessSpec(cloud="aws", region="us-west-2"),
)
```

```python
pinecone_index = pc.Index("quickstart-index")
```

PineconeVectorStore ve VectorStoreIndex'i oluşturun

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
```

```python
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

```python
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index, namespace="test_05_14"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


Upserted vectors:   0%|          | 0/7 [00:00<?, ?it/s]
```

Meta veri filtrelerini tanımlayın

```python
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)


filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="theme", operator=FilterOperator.EQ, value="Fiction"
        ),
    ]
)
```

Meta veri filtreleri ile vektör deposundan veri getirin

```python
retriever = index.as_retriever(filters=filters)
retriever.retrieve("Inception ne hakkındadır?")
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='7fed3d0b-e2d7-432a-9231-3ac02130c00f', ... metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, ... text='Inception', ...), score=0.317687511),
 NodeWithScore(node=TextNode(id_='6b7bdb44-9dc2-48f6-b9cb-05dcaea4889b', ... metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, ... text="Harry Potter and the Sorcerer's Stone", ...), score=0.467440248)]
```

`AND` (VE) koşulu ile çoklu meta veri filtreleri

```python
from llama_index.core.vector_stores import FilterOperator, FilterCondition


filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Fiction"),
        MetadataFilter(key="year", value=1997, operator=FilterOperator.GT),
    ],
    condition=FilterCondition.AND,
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Harry Potter?")
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='7fed3d0b-e2d7-432a-9231-3ac02130c00f', ... metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, ... text='Inception', ...), score=0.470013738)]
```

`OR` (VEYA) koşulu ile çoklu meta veri filtreleri

```python
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

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='6b7bdb44-9dc2-48f6-b9cb-05dcaea4889b', ... metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, ... text="Harry Potter and the Sorcerer's Stone", ...), score=0.300355315),
 NodeWithScore(node=TextNode(id_='7fed3d0b-e2d7-432a-9231-3ac02130c00f', ... metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, ... text='Inception', ...), score=0.470002413)]
```

Pinecone'a özgü anahtar kelime argümanlarını (keyword arguments) kullanın

```python
retriever = index.as_retriever(
    vector_store_kwargs={"filter": {"theme": "Mafia"}}
)
retriever.retrieve("Inception ne hakkındadır?")
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='54f65cf7-a12f-4366-88fe-6239c71920d2', ... metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}, ... text='The Godfather', ...), score=0.86521795)]
```
