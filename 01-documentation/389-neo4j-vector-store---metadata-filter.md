---
title: Neo4j Vektör Deposu - Meta Veri Filtreleme
 | LlamaIndex OSS Belgeleri
---

# Neo4j Vektör Deposu - Meta Veri Filtreleme

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-neo4jvector
```

```bash
# !pip install llama-index>=0.9.31 neo4j
```

```python
import logging
import sys
import os


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

Bir Neo4j vektör İndeksi oluşturun ve ona bağlanın

```python
import os
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore


os.environ["OPENAI_API_KEY"] = "sk-..."


username = "neo4j"
password = "sifre"
url = "bolt://localhost:7687"
embed_dim = 1536  # Boyutlar text-embedding-ada-002 içindir


vector_store = Neo4jVectorStore(username, password, url, embed_dim)
```

VectorStoreIndex'i Oluşturun

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="The Shawshank Redemption (Esaretin Bedeli)",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
            "year": 1994,
        },
    ),
    TextNode(
        text="The Godfather (Baba)",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
            "year": 1972,
        },
    ),
    TextNode(
        text="Inception (Başlangıç)",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Fiction",
            "year": 2010,
        },
    ),
    TextNode(
        text="To Kill a Mockingbird (Bülbülü Öldürmek)",
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
        text="The Great Gatsby (Muhteşem Gatsby)",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "The American Dream",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter and the Sorcerer's Stone (Harry Potter ve Felsefe Taşı)",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Fiction",
            "year": 1997,
        },
    ),
]
```

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
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

Filtrelerle vektör deposundan veri getirin

```python
retriever = index.as_retriever(filters=filters)
retriever.retrieve("Inception (Başlangıç) ne hakkındadır?")
```

```python
# [NodeWithScore(node=TextNode(id_='814e5f2a-2150-4bae-8a59-fa728379e978', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, text='Inception'), score=0.9202238321304321),
#  NodeWithScore(node=TextNode(id_='fc1df8cc-f1d3-4a7b-8c21-f83b18463758', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, text="Harry Potter and the Sorcerer's Stone"), score=0.8823964595794678)]
```

`AND` koşulu ile çoklu Meta Veri Filtreleri

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

```python
# [NodeWithScore(node=TextNode(id_='814e5f2a-2150-4bae-8a59-fa728379e978', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, text='Inception'), score=0.8818434476852417)]
```

`OR` koşulu ile çoklu Meta Veri Filtreleri

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

```python
# [NodeWithScore(node=TextNode(id_='fc1df8cc-f1d3-4a7b-8c21-f83b18463758', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}, text="Harry Potter and the Sorcerer's Stone"), score=0.9242331385612488),
#  NodeWithScore(node=TextNode(id_='814e5f2a-2150-4bae-8a59-fa728379e978', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}, text='Inception'), score=0.8818434476852417)]
```
