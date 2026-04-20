---
title: Rehber: Mevcut Weaviate Vektör Deposu ile Vector Store Index Kullanımı
 | LlamaIndex OSS Belgeleri
---

# Rehber: Mevcut Weaviate Vektör Deposu ile Vector Store Index Kullanımı

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-weaviate
%pip install llama-index-embeddings-openai
```

```bash
!pip install llama-index
```

```python
import weaviate
```

```python
client = weaviate.Client("https://test-cluster-bbn8vqsn.weaviate.network")
```

## Örnek "Mevcut" Weaviate Vektör Deposunu Hazırlama

### Şema tanımlama

"Book" sınıfı için title (str), author (str), content (str) ve year (int) olmak üzere 4 özellikli bir şema oluşturuyoruz

```python
try:
    client.schema.delete_class("Book")
except:
    pass
```

```python
schema = {
    "classes": [
        {
            "class": "Book",
            "properties": [
                {"name": "title", "dataType": ["text"]},
                {"name": "author", "dataType": ["text"]},
                {"name": "content", "dataType": ["text"]},
                {"name": "year", "dataType": ["int"]},
            ],
        },
    ]
}


if not client.schema.contains(schema):
    client.schema.create(schema)
```

### Örnek veriyi tanımlama

4 adet örnek kitap oluşturuyoruz

```python
books = [
    {
        "title": "Bülbülü Öldürmek (To Kill a Mockingbird)",
        "author": "Harper Lee",
        "content": (
            "Bülbülü Öldürmek, Harper Lee tarafından yazılan ve 1960'ta "
            "yayınlanan bir romandır..."
        ),
        "year": 1960,
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "content": (
            "1984, George Orwell tarafından yazılan ve 1949'da yayınlanan "
            "bir distopik romandır..."
        ),
        "year": 1949,
    },
    {
        "title": "Muhteşem Gatsby (The Great Gatsby)",
        "author": "F. Scott Fitzgerald",
        "content": (
            "Muhteşem Gatsby, F. Scott Fitzgerald tarafından yazılan ve "
            "1925'te yayınlanan bir romandır..."
        ),
        "year": 1925,
    },
    {
        "title": "Aşk ve Gurur (Pride and Prejudice)",
        "author": "Jane Austen",
        "content": (
            "Aşk ve Gurur, Jane Austen tarafından yazılan ve 1813'te "
            "yayınlanan bir romandır..."
        ),
        "year": 1813,
    },
]
```

### Veri ekleme

Örnek kitapları Weaviate "Book" sınıfımıza ekliyoruz (içerik alanı için gömmeler oluşturarak)

```python
from llama_index.embeddings.openai import OpenAIEmbedding


embed_model = OpenAIEmbedding()
```

```python
with client.batch as batch:
    for book in books:
        vector = embed_model.get_text_embedding(book["content"])
        batch.add_data_object(
            data_object=book, class_name="Book", vector=vector
        )
```

## "Mevcut" Weaviate Vektör Deposuna Karşı Sorgulama

```python
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.response.pprint_utils import pprint_source_node
```

İstenen Weaviate sınıfıyla eşleşen bir "index_name" düzgün bir şekilde belirtmeli ve "text" alanı olarak bir sınıf özelliğini seçmelisiniz.

```python
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="Book", text_key="content"
)
```

```python
retriever = VectorStoreIndex.from_vector_store(vector_store).as_retriever(
    similarity_top_k=1
)
```

```python
nodes = retriever.retrieve("Kuşla ilgili olan o kitap hangisiydi?")
```

Erişilen düğümü inceleyelim. Kitap verilerinin, ana metin olarak "content" alanıyla birlikte LlamaIndex `Node` nesneleri olarak yüklendiğini görebiliriz.

```python
pprint_source_node(nodes[0])
```

```text
Belge Kimliği (Document ID): cf927ce7-0672-4696-8aae-7e77b33b9659
Benzerlik (Similarity): None
Metin (Text): yazar: Harper Lee başlık: Bülbülü Öldürmek yıl: 1960  Bülbülü 
Öldürmek, Harper Lee tarafından yayınlanan bir romandır......
```

Kalan alanlar meta veri olarak yüklenmelidir (`metadata` içinde)

```python
nodes[0].node.metadata
```

```text
{'author': 'Harper Lee', 'title': 'Bülbülü Öldürmek (To Kill a Mockingbird)', 'year': 1960}
```
