# Chroma Vektör Deposu (Vector Store)

---
title: Chroma Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-chroma
```

```bash
!pip install llama-index
```

#### Chroma İndeksi Oluşturma

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
import os
import getpass


# os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Anahtarı:")
import openai


openai.api_key = "sk-"
```

```python
import chromadb
```

```python
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")
```

```python
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from IPython.display import Markdown, display
```

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="Esaretin Bedeli (The Shawshank Redemption)",
        metadata={
            "author": "Stephen King",
            "theme": "Dostluk",
            "year": 1994,
        },
    ),
    TextNode(
        text="Baba (The Godfather)",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafya",
            "year": 1972,
        },
    ),
    TextNode(
        text="Başlangıç (Inception)",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Kurgu",
            "year": 2010,
        },
    ),
    TextNode(
        text="Bülbülü Öldürmek (To Kill a Mockingbird)",
        metadata={
            "author": "Harper Lee",
            "theme": "Mafya",
            "year": 1960,
        },
    ),
    TextNode(
        text="1984",
        metadata={
            "author": "George Orwell",
            "theme": "Totalitarizm",
            "year": 1949,
        },
    ),
    TextNode(
        text="Muhteşem Gatsby (The Great Gatsby)",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "Amerikan Rüyası",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter ve Felsefe Taşı (Harry Potter and the Sorcerer's Stone)",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Kurgu",
            "year": 1997,
        },
    ),
]
```

```python
from llama_index.core import StorageContext




vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```python
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

## Tekli Tam Eşleşme Filtresi (One Exact Match Filter)

```python
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", operator=FilterOperator.EQ, value="Mafya"),
    ]
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```

```text
INFO:httpx:HTTP İsteği: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='...', metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafya', 'year': 1972}, text='Baba (The Godfather)', ...), score=0.6215522669166147),
 NodeWithScore(node=TextNode(id_='...', metadata={'author': 'Harper Lee', 'theme': 'Mafya', 'year': 1960}, text='Bülbülü Öldürmek (To Kill a Mockingbird)', ...), score=0.5873631114046581)]
```

## Çoklu Tam Eşleşme Metaveri Filtreleri (Multiple Exact Match Metadata Filters)

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Mafya"),
        MetadataFilter(key="year", value=1972),
    ]
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```

```text
INFO:httpx:HTTP İsteği: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='...', metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafya', 'year': 1972}, text='Baba (The Godfather)', ...), score=0.6215522669166147)]
```

## `AND` Koşulu ile Çoklu Metaveri Filtreleri

```python
from llama_index.core.vector_stores import FilterOperator, FilterCondition




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Kurgu"),
        MetadataFilter(key="year", value=1997, operator=FilterOperator.GT),
    ],
    condition=FilterCondition.AND,
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Harry Potter?")
```

```text
INFO:httpx:HTTP İsteği: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='...', metadata={'director': 'Christopher Nolan', 'theme': 'Kurgu', 'year': 2010}, text='Başlangıç (Inception)', ...), score=0.6250006485226994)]
```

## `OR` Koşulu ile Çoklu Metaveri Filtreleri

```python
from llama_index.core.vector_stores import FilterOperator, FilterCondition




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Kurgu"),
        MetadataFilter(key="year", value=1997, operator=FilterOperator.GT),
    ],
    condition=FilterCondition.OR,
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Harry Potter?")
```

```text
INFO:httpx:HTTP İsteği: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"


[NodeWithScore(node=TextNode(id_='...', metadata={'author': 'J.K. Rowling', 'theme': 'Kurgu', 'year': 1997}, text="Harry Potter ve Felsefe Taşı (Harry Potter and the Sorcerer's Stone)", ...), score=0.7405548668973673),
 NodeWithScore(node=TextNode(id_='...', metadata={'director': 'Christopher Nolan', 'theme': 'Kurgu', 'year': 2010}, text='Başlangıç (Inception)', ...), score=0.6250006485226994)]
```
