---
title: Qdrant Vektör Deposu - Meta Veri Filtresi
 | LlamaIndex OSS Belgeleri
---

# Qdrant Vektör Deposu - Meta Veri Filtresi

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-qdrant
```

```bash
!pip install llama-index qdrant_client
```

Qdrant VectorStore (Vektör Deposu) İstemcisini Oluşturun

```python
import qdrant_client
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore


client = qdrant_client.QdrantClient(
    # Hızlı ve hafif denemeler için :memory: modunu kullanabilirsiniz,
    # bu mod, Qdrant'ın herhangi bir yere dağıtılmasını gerektirmez
    # ancak qdrant-client >= 1.1.1 sürümüne ihtiyaç duyar
    location=":memory:"
    # aksi takdirde Qdrant örnek (instance) adresini şununla ayarlayın:
    # uri="http://<ana_bilgisayar>:<baglanti_noktasi>"
    # Qdrant Cloud için API ANAHTARINI ayarlayın
    # api_key="<qdrant-api-key>",
)
```

QdrantVectorStore'u oluşturun ve bir Qdrant İndeksi yaratın

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="Esaretin Bedeli",
        metadata={
            "author": "Stephen King",
            "theme": "Arkadaşlık",
            "year": 1994,
        },
    ),
    TextNode(
        text="Baba",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafya",
            "year": 1972,
        },
    ),
    TextNode(
        text="Başlangıç",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Kurgu",
            "year": 2010,
        },
    ),
    TextNode(
        text="Bülbülü Öldürmek",
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
        text="Muhteşem Gatsby",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "Amerikan Rüyası",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter ve Felsefe Taşı",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Kurgu",
            "year": 1997,
        },
    ),
]
```

```python
import os


from llama_index.core import StorageContext




os.environ["OPENAI_API_KEY"] = "sk-..."




vector_store = QdrantVectorStore(
    client=client, collection_name="test_collection_1"
)
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
        MetadataFilter(key="theme", operator=FilterOperator.EQ, value="Mafya"),
    ]
)
```

Filtrelerle vektör deposundan veri çekin (retrieve)

```python
retriever = index.as_retriever(filters=filters)
retriever.retrieve("Başlangıç ne hakkındadır?")
```

```bash
[FieldCondition(key='theme', match=MatchValue(value='Mafya'), range=None, geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None)]










[NodeWithScore(node=TextNode(id_='050c085d-6d91-4080-9fd6-3f874a528970', embedding=None, metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafya', 'year': 1972}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='bfa890174187ddaed4876803691ed605463de599f5493f095a03b8d83364f1ef', text='Baba', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7620959333946706),
 NodeWithScore(node=TextNode(id_='11d0043a-aba3-4ffe-84cb-3f17988759be', embedding=None, metadata={'author': 'Harper Lee', 'theme': 'Mafya', 'year': 1960}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='3475334d04bbe4606cb77728d5dc0784f16c8db3f190f3692e6310906c821927', text='Bülbülü Öldürmek', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7340329162691743)]
```

`AND` (VE) koşulu ile Çoklu Meta Veri Filtreleri

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

```bash
[FieldCondition(key='theme', match=MatchValue(value='Kurgu'), range=None, geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None)]
[FieldCondition(key='theme', match=MatchValue(value='Kurgu'), range=None, geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None), FieldCondition(key='year', match=None, range=Range(lt=None, gt=1997.0, gte=None, lte=None), geo_bounding_box=None, geo_radius=None, geo_polygon=None, values_count=None)]










[NodeWithScore(node=TextNode(id_='1be42402-518f-4e88-9860-12cfec9f5ed2', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Kurgu', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='7937eb153ccc78a3329560f37d90466ba748874df6b0303b3b8dd3c732aa7688', text='Başlangıç', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7649987694994126)]
```

Qdrant'a özgü anahtar kelime argümanlarını (keyword arguments) kullanma

```python
retriever = index.as_retriever(
    vector_store_kwargs={"filter": {"theme": "Mafya"}}
)
retriever.retrieve("Başlangıç ne hakkındadır?")
```

```bash
[NodeWithScore(node=TextNode(id_='1be42402-518f-4e88-9860-12cfec9f5ed2', embedding=None, metadata={'director': 'Christopher Nolan', 'theme': 'Kurgu', 'year': 2010}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='7937eb153ccc78a3329560f37d90466ba748874df6b0303b3b8dd3c732aa7688', text='Başlangıç', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.841150534139415),
 NodeWithScore(node=TextNode(id_='ee4d3b32-7675-49bc-bc49-04011d62cf7c', embedding=None, metadata={'author': 'J.K. Rowling', 'theme': 'Kurgu', 'year': 1997}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, hash='1b24f5e9fb6f18cc893e833af8d5f28ff805a6361fc0838a3015c287510d29a3', text="Harry Potter ve Felsefe Taşı", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.7661930751179629)]
```
