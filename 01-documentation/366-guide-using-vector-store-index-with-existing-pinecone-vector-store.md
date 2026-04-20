---
title: Rehber: Mevcut Pinecone Vektör Deposu ile Vector Store Index Kullanımı
 | LlamaIndex OSS Belgeleri
---

# Rehber: Mevcut Pinecone Vektör Deposu ile Vector Store Index Kullanımı

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-embeddings-openai
%pip install llama-index-vector-stores-pinecone
```

```bash
!pip install llama-index
```

```python
import os
import pinecone
```

```python
api_key = os.environ["PINECONE_API_KEY"]
pinecone.init(api_key=api_key, environment="eu-west1-gcp")
```

## Örnek "Mevcut" Pinecone Vektör Deposunu Hazırlama

### İndeks oluşturma

```python
indexes = pinecone.list_indexes()
print(indexes)
```

```text
['quickstart-index']
```

```python
if "quickstart-index" not in indexes:
    # boyutlar text-embedding-ada-002 içindir
    pinecone.create_index(
        "quickstart-index", dimension=1536, metric="euclidean", pod_type="p1"
    )
```

```python
pinecone_index = pinecone.Index("quickstart-index")
```

```python
pinecone_index.delete(deleteAll="true")
```

```text
{}
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

Örnek kitapları Pinecone indeksimize ekliyoruz (içerik alanı için gömmeler oluşturarak)

```python
import uuid
from llama_index.embeddings.openai import OpenAIEmbedding


embed_model = OpenAIEmbedding()
```

```python
entries = []
for book in books:
    vector = embed_model.get_text_embedding(book["content"])
    entries.append(
        {"id": str(uuid.uuid4()), "values": vector, "metadata": book}
    )
pinecone_index.upsert(entries)
```

```text
{'upserted_count': 4}
```

## "Mevcut" Pinecone Vektör Deposuna Karşı Sorgulama

```python
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.response.pprint_utils import pprint_source_node
```

Bir sınıf özelliğini "text" alanı olarak düzgün bir şekilde seçmelisiniz.

```python
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index, text_key="content"
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
Belge Kimliği (Document ID): 07e47f1d-cb90-431b-89c7-35462afcda28
Benzerlik (Similarity): 0.797243237
Metin (Text): yazar: Harper Lee başlık: Bülbülü Öldürmek yıl: 1960.0  Bülbülü 
Öldürmek, Harper Lee tarafından yayınlanan bir romandır......
```

Kalan alanlar meta veri olarak yüklenmelidir (`metadata` içinde)

```python
nodes[0].node.metadata
```

```text
{'author': 'Harper Lee', 'title': 'Bülbülü Öldürmek (To Kill a Mockingbird)', 'year': 1960.0}
```
