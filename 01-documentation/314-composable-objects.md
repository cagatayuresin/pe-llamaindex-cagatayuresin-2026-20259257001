# Birleştirilebilir Nesneler (Composable Objects)

---
title: Composable Objects
 | LlamaIndex OSS Documentation
---

Bu not defterinde, birden fazla nesneyi tek bir üst düzey dizinde nasıl birleştirebileceğinizi gösteriyoruz.

Bu yaklaşım, bir `IndexNode` nesnesinin `obj` alanının şunlardan birini işaret etmesiyle çalışır:

- sorgu motoru (query engine)
- erişimci (retriever)
- sorgu hattı (query pipeline)
- başka bir düğüm!

```python
object = IndexNode(index_id="nesnem", obj=sorgu_motoru, text="bu nesne hakkında bazı metinler")
```

## Veri Hazırlığı (Data Setup)

```python
%pip install llama-index-storage-docstore-mongodb
%pip install llama-index-vector-stores-qdrant
%pip install llama-index-storage-docstore-firestore
%pip install llama-index-retrievers-bm25
%pip install llama-index-storage-docstore-redis
%pip install llama-index-storage-docstore-dynamodb
%pip install llama-index-readers-file pymupdf
```

```bash
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "./llama2.pdf"
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/1706.03762.pdf" -O "./attention.pdf"
```

```python
from llama_index.core import download_loader


from llama_index.readers.file import PyMuPDFReader


llama2_docs = PyMuPDFReader().load_data(
    file_path="./llama2.pdf", metadata=True
)
attention_docs = PyMuPDFReader().load_data(
    file_path="./attention.pdf", metadata=True
)
```

## Erişimci Kurulumu (Retriever Setup)

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

```python
from llama_index.core.node_parser import TokenTextSplitter


nodes = TokenTextSplitter(
    chunk_size=1024, chunk_overlap=128
).get_nodes_from_documents(llama2_docs + attention_docs)
```

```python
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.docstore.firestore import FirestoreDocumentStore
from llama_index.storage.docstore.dynamodb import DynamoDBDocumentStore


docstore = SimpleDocumentStore()
docstore.add_documents(nodes)
```

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


client = QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore("composable", client=client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex(nodes=nodes)
vector_retriever = index.as_retriever(similarity_top_k=2)
bm25_retriever = BM25Retriever.from_defaults(
    docstore=docstore, similarity_top_k=2
)
```

## Nesneleri Birleştirme (Composing Objects)

Burada `IndexNode`'ları oluşturuyoruz. Metin alanının, üst düzey dizin tarafından düğümü dizinlemek için kullanılan alan olduğunu unutmayın.

Vektör dizini için metin vektörleştirilir (embed); anahtar kelime dizini için metin, anahtar kelimeler için kullanılır.

Bu örnekte, her zaman tüm düğümleri getirdiği için teknik olarak erişim için metne ihtiyaç duymayan `SummaryIndex` kullanılmaktadır.

```python
from llama_index.core.schema import IndexNode


vector_obj = IndexNode(
    index_id="vector", obj=vector_retriever, text="Vektör Erişimcisi"
)
bm25_obj = IndexNode(
    index_id="bm25", obj=bm25_retriever, text="BM25 Erişimcisi"
)
```

```python
from llama_index.core import SummaryIndex


summary_index = SummaryIndex(objects=[vector_obj, bm25_obj])
```

## Sorgulama (Querying)

Sorgulama yaptığımızda, tüm nesneler getirilecek ve nihai bir cevap oluşturmak için düğümleri üretmek için kullanılacaktır.

`tree_summarize` modunu `aquery()` ile kullanmak, eşzamanlı yürütme (concurrent execution) ve daha hızlı yanıtlar sağlar.

```python
query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize", verbose=True
)
```

```python
response = await query_engine.aquery(
    "Transformer modellerinde dikkat (attention) mekanizması nasıl çalışır?"
)
```

```
[1;3;38;2;11;159;203mRetrieval entering vector: VectorIndexRetriever
[0m[1;3;38;2;11;159;203mRetrieval entering bm25: BM25Retriever
[0m
```

```python
print(str(response))
```

```text
Transformer'lardaki dikkat (attention) mekanizması, bir sorguyu ve bir dizi anahtar-değer çiftini bir çıktı ile eşleyerek çalışır. Çıktı, değerlerin ağırlıklı toplamı olarak hesaplanır ve burada ağırlıklar sorgu ile anahtarlar arasındaki benzerlik tarafından belirlenir. Transformer modelinde dikkat üç farklı şekilde kullanılır:


1. Kodlayıcı-kod çözücü (Encoder-decoder) dikkati: Sorgular önceki kod çözücü katmanından gelir ve bellek anahtarları ile değerleri kodlayıcının çıktısından gelir. Bu, kod çözücüdeki her konumun girdi dizisindeki tüm konumlara dikkat etmesini sağlar.


2. Kodlayıcıdaki özdikkat (Self-attention): Bir özdikkat katmanında, tüm anahtarlar, değerler ve sorgular, kodlayıcıdaki önceki katmanın çıktısı olan aynı yerden gelir. Kodlayıcıdaki her konum, kodlayıcının önceki katmanındaki tüm konumlara dikkat edebilir.


3. Kod çözücüdeki özdikkat (Self-attention): Kodlayıcıya benzer şekilde, kod çözücüdeki özdikkat katmanları, kod çözücüdeki her konumun o konuma kadar olan tüm konumlara dikkat etmesini sağlar. Ancak, özyinelemeli (auto-regressive) özelliği korumak için kod çözücüde sola doğru bilgi akışı engellenir.


Genel olarak, transformer'lardaki dikkat, modelin farklı konumlardaki farklı temsil alt alanlarından gelen bilgilere ortaklaşa dikkat etmesini sağlayarak, modelin girdi dizisinin farklı bölümleri arasındaki bağımlılıkları ve ilişkileri yakalama yeteneğini geliştirir.
```

```python
response = await query_engine.aquery(
    "Llama 2 mimarisi neye dayanmaktadır?"
)
```

```
[1;3;38;2;11;159;203mRetrieval entering vector: VectorIndexRetriever
[0m[1;3;38;2;11;159;203mRetrieval entering bm25: BM25Retriever
[0m
```

```python
print(str(response))
```

```text
Llama 2'nin mimarisi transformer modeline dayanmaktadır.
```

```python
response = await query_engine.aquery(
    "Transformer'lardaki dikkat mekanizmasından önce ne kullanılıyordu?"
)
```

```
[1;3;38;2;11;159;203mRetrieval entering vector: VectorIndexRetriever
[0m[1;3;38;2;11;159;203mRetrieval entering bm25: BM25Retriever
[0m
```

```python
print(str(response))
```

```text
Transformer'lardaki dikkat mekanizmasından önce, uzun kısa süreli bellek (LSTM) ve geçitli özyinelemeli sinir ağları (GRU) gibi özyinelemeli sinir ağları (RNN) yaygın olarak kullanılıyordu. Bu modeller, dil modelleme ve makine çevirisi de dahil olmak üzere dizi modelleme ve dönüştürme problemlerinde geniş çapta kullanılmıştır.
```

## Kaydetme ve Yükleme Üzerine Not

Nesneler teknik olarak seri hale getirilebilir (serializable) olmadığından, kaydederken ve yüklerken yükleme sırasında da sağlanmaları gerekir.

İşte bu kurulumu nasıl kaydedip yükleyebileceğime dair bir örnek.

### Kaydetme (Save)

```python
# qdrant zaten otomatik olarak kaydedilir!
# burada sadece belge deposunu (docstore) kaydetmemiz gerekiyor


# bm25 için belge deposu düğümlerimizi kaydedin
docstore.persist("./docstore.json")
```

### Yükleme (Load)

```python
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


docstore = SimpleDocumentStore.from_persist_path("./docstore.json")


client = QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore("composable", client=client)
```

```python
index = VectorStoreIndex.from_vector_store(vector_store)
vector_retriever = index.as_retriever(similarity_top_k=2)
bm25_retriever = BM25Retriever.from_defaults(
    docstore=docstore, similarity_top_k=2
)
```

```python
from llama_index.core.schema import IndexNode


vector_obj = IndexNode(
    index_id="vector", obj=vector_retriever, text="Vektör Erişimcisi"
)
bm25_obj = IndexNode(
    index_id="bm25", obj=bm25_retriever, text="BM25 Erişimcisi"
)
```

```python
# özet dizinine (summary index) normal düğümler eklemiş olsaydık, bunu da kaydedip yükleyebilirdik
# summary_index.persist("./summary_index.json")
# summary_index = load_index_from_storage(storage_context, objects=objects)


from llama_index.core import SummaryIndex


summary_index = SummaryIndex(objects=[vector_obj, bm25_obj])
```
