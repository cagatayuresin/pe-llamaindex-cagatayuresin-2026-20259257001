---
title: Qdrant Vektör Deposu - Varsayılan Qdrant Filtreleri
 | LlamaIndex OSS Belgeleri
---

# Qdrant Vektör Deposu - Varsayılan Qdrant Filtreleri

Düz olarak `qdrant_client` SDK'sından sağlanan filtrelerin Eriştirici (Retriever) / Sorgu Motorunda (Query Engine) doğrudan nasıl kullanılacağına dair örnek:

```bash
%pip install llama-index-vector-stores-qdrant
```

```bash
!pip3 install llama-index qdrant_client
```

```python
import openai
import qdrant_client
from IPython.display import Markdown, display
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client.http.models import Filter, FieldCondition, MatchValue


client = qdrant_client.QdrantClient(location=":memory:")
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="りんごとは (Elma nedir)",
        metadata={"author": "Tanaka", "fruit": "apple", "city": "Tokyo"},
    ),
    TextNode(
        text="Was ist Apfel? (Elma nedir?)",
        metadata={"author": "David", "fruit": "apple", "city": "Berlin"},
    ),
    TextNode(
        text="Orange like the sun (Güneş gibi portakal)",
        metadata={"author": "Jane", "fruit": "orange", "city": "Hong Kong"},
    ),
    TextNode(
        text="Grape is... (Üzüm...)",
        metadata={"author": "Jane", "fruit": "grape", "city": "Hong Kong"},
    ),
    TextNode(
        text="T-dot > G-dot",
        metadata={"author": "George", "fruit": "grape", "city": "Toronto"},
    ),
    TextNode(
        text="6ix Watermelons (6 Karpuz)",
        metadata={
            "author": "George",
            "fruit": "watermelon",
            "city": "Toronto",
        },
    ),
]


openai.api_key = "YOUR_API_KEY"
vector_store = QdrantVectorStore(
    client=client, collection_name="fruit_collection"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)




# qdrant_client python kütüphanesindeki filtreleri doğrudan kullanın
# Daha detaylı bilgi almak için buradaki python örneklerini inceleyebilirsiniz: https://qdrant.tech/documentation/concepts/filtering/


filters = Filter(
    should=[
        Filter(
            must=[
                FieldCondition(
                    key="fruit",
                    match=MatchValue(value="apple"),
                ),
                FieldCondition(
                    key="city",
                    match=MatchValue(value="Tokyo"),
                ),
            ]
        ),
        Filter(
            must=[
                FieldCondition(
                    key="fruit",
                    match=MatchValue(value="grape"),
                ),
                FieldCondition(
                    key="city",
                    match=MatchValue(value="Toronto"),
                ),
            ]
        ),
    ]
)


retriever = index.as_retriever(vector_store_kwargs={"qdrant_filters": filters})


response = retriever.retrieve("Üzümleri kim yapar? (Who makes grapes?)")
for node in response:
    print("node", node.score)
    print("node", node.text)
    print("node", node.metadata)
```
