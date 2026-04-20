# BM25 Erişimcisi (BM25 Retriever)

---
title: BM25 Retriever
 | LlamaIndex OSS Documentation
---

Bu rehberde, dokümanları bm25 yöntemiyle arayan bir BM25 erişimcisi tanımlıyoruz. BM25 (Best Matching 25), terim frekansı doygunluğunu ve doküman uzunluğunu dikkate alarak TF-IDF'yi genişleten bir sıralama işlevidir. BM25, dokümanları sorgu terimlerinin tüm külliyat (corpus) genelindeki oluşumuna ve nadirliğine göre etkili bir şekilde sıralar.

Bu not defteri, RouterQueryEngine not defterine çok yakındır.

## Kurulum (Setup)

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index
%pip install llama-index-retrievers-bm25
```

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-proj-..."


from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
```

## Veriyi İndirme (Download Data)

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```text
--2024-07-05 10:10:09--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
raw.githubusercontent.com (raw.githubusercontent.com) çözülüyor... 185.199.111.133, 185.199.109.133, 185.199.108.133, ...
raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443 bağlanılıyor... bağlandı.
HTTP isteği gönderildi, yanıt bekleniyor... 200 OK
Uzunluk: 75042 (73K) [text/plain]
Kaydediliyor: ‘data/paul_graham/paul_graham_essay.txt’


data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    0.05s içinde


2024-07-05 10:10:09 (1.36 MB/s) - ‘data/paul_graham/paul_gra_essay.txt’ kaydedildi [75042/75042]
```

## Veriyi Yükleme (Load Data)

İlk olarak bir Belgenin (Document) bir dizi Düğüm (Node) haline nasıl dönüştürüleceğini ve bir Belge Deposuna (DocumentStore) nasıl ekleneceğini gösteriyoruz.

```python
from llama_index.core import SimpleDirectoryReader


# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```python
from llama_index.core.node_parser import SentenceSplitter


# düğüm ayrıştırıcıyı başlat
splitter = SentenceSplitter(chunk_size=512)


nodes = splitter.get_nodes_from_documents(documents)
```

## BM25 Erişimcisi + Disk Kalıcılığı (Disk Persistence)

Bir seçenek, `BM25Retriever`ı doğrudan düğümlerden oluşturmak ve diske kaydedip diskten geri yüklemektir.

```python
from llama_index.retrievers.bm25 import BM25Retriever
import Stemmer


# Erişimciyi oluşturmak için dizini, belge deposunu veya düğüm listesini geçirebiliriz
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=2,
    # İsteğe bağlı: Kelime kökü bulucuyu (stemmer) geçirebilir ve stopwords için dili ayarlayabiliriz.
    # Bu, sorgu + metin üzerindeki etkisiz kelimeleri kaldırmak ve kök bulmak için önemlidir.
    # Her ikisi için de varsayılan değer İngilizcedir (english).
    stemmer=Stemmer.Stemmer("english"),
    language="english",
)
```

```text
BM25S Belirteçleri Sayma (Count Tokens):   0%|          | 0/61 [00:00<?, ?it/s]






BM25S Skorları Hesaplama (Compute Scores):   0%|          | 0/61 [00:00<?, ?it/s]
```

```python
bm25_retriever.persist("./bm25_retriever")


loaded_bm25_retriever = BM25Retriever.from_persist_dir("./bm25_retriever")
```

```text
mmindex için yeni satırlar bulunuyor:   0%|          | 0.00/292k [00:00<?, ?B/s]
```

## BM25 Erişimcisi + Belge Deposu (Docstore) Kalıcılığı

Burada, düğümlerinizi tutmak için bir belge deposu (docstore) ile birlikte `BM25Retriever` kullanımını ele alıyoruz. Buradaki avantaj, belge deposunun uzak (mongodb, redis, vb.) olabilmesidir.

```python
# düğümleri saklamak için bir belge deposu (docstore) başlat
# ayrıca docstores için mongodb, redis, postgres vb. de mevcuttur
from llama_index.core.storage.docstore import SimpleDocumentStore


docstore = SimpleDocumentStore()
docstore.add_documents(nodes)
```

```python
from llama_index.retrievers.bm25 import BM25Retriever
import Stemmer


# Erişimciyi oluşturmak için dizini, belge deposunu veya düğüm listesini geçirebiliriz
bm25_retriever = BM25Retriever.from_defaults(
    docstore=docstore,
    similarity_top_k=2,
    # İsteğe bağlı: Kelime kökü bulucuyu (stemmer) geçirebilir ve stopwords için dili ayarlayabiliriz.
    # Bu, sorgu + metin üzerindeki etkisiz kelimeleri kaldırmak ve kök bulmak için önemlidir.
    # Her ikisi için de varsayılan değer İngilizcedir (english).
    stemmer=Stemmer.Stemmer("english"),
    language="english",
)
```

```text
BM25S Belirteçleri Sayma (Count Tokens):   0%|          | 0/61 [00:00<?, ?it/s]






BM25S Skorları Hesaplama (Compute Scores):   0%|          | 0/61 [00:00<?, ?it/s]
```

```python
from llama_index.core.response.notebook_utils import display_source_node


# belirli şirketlerden bağlam getirecektir
retrieved_nodes = bm25_retriever.retrieve(
    "Viaweb ve Interleaf'te neler oldu?"
)
for node in retrieved_nodes:
    display_source_node(node, source_length=5000)
```

**Düğüm ID (Node ID):** a1236ec0-7d41-4b52-950f-27199a1e28de\
**Benzerlik (Similarity):** 1.8383275270462036\
**Metin (Text):** I saw Florence at street level in every possible condition... (Paul Graham makalesi metni orijinal dilinde korunmuştur)

**Düğüm ID (Node ID):** 34259d5b-f0ea-436d-8f44-31d790cfbfb7\
**Benzerlik (Similarity):** 1.5173875093460083\
**Metin (Text):** This name didn’t last long before it was replaced by “software as a service,” but it was current for long enough... (Paul Graham makalesi metni orijinal dilinde korunmuştur)

```python
retrieved_nodes = bm25_retriever.retrieve("Yazar RISD'den sonra ne yaptı?")
for node in retrieved_nodes:
    display_source_node(node, source_length=5000)
```

## BM25 Erişimcisi + Meta Veri Filtreleme (MetadataFiltering)

```python
# Bazı meta verilerle Belgeyi başlat
from llama_index.core import Document


documents = [
    Document(text="Merhaba dünya!", metadata={"key": "1"}),
    Document(text="Merhaba dünya! 2", metadata={"key": "2"}),
    Document(text="Merhaba dünya! 3", metadata={"key": "3"}),
    Document(text="Merhaba dünya! 2.1", metadata={"key": "2"}),
]
```

```python
# Düğüm ayrıştırıcıyı başlat
from llama_index.core.node_parser import SentenceSplitter


from llama_index.core.storage.docstore import SimpleDocumentStore


splitter = SentenceSplitter(chunk_size=512)
nodes = splitter.get_nodes_from_documents(documents)


# Düğümleri belge deposuna (docstore) ekle
docstore = SimpleDocumentStore()
docstore.add_documents(nodes)
```

```python
# Meta veri filtrelerini tanımla
from llama_index.core.vector_stores.types import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator,
    FilterCondition,
)


filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="key",
            value="2",
            operator=FilterOperator.EQ,
        )
    ],
    condition=FilterCondition.AND,
)
```

```python
from llama_index.core.response.notebook_utils import display_source_node


from llama_index.retrievers.bm25 import BM25Retriever
import Stemmer


retrieved_nodes = BM25Retriever.from_defaults(
    docstore=docstore,
    similarity_top_k=3,
    filters=filters,  # Filtreleri buraya ekle
    stemmer=Stemmer.Stemmer("english"),
    language="english",
).retrieve("Merhaba dünya!")


for node in retrieved_nodes:
    display_source_node(node, source_length=5000)
```

## BM25 + Chroma ile Hibrit Erişimci (Hybrid Retriever)

Şimdi seyrek (sparse) ve yoğun (dense) erişim için bm25 ve chroma'yı birleştireceğiz.

Sonuçlar `QueryFusionRetriever` kullanılarak birleştirilir.

Erişimci ile tam bir `RetrieverQueryEngine` oluşturabiliriz.

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb


docstore = SimpleDocumentStore()
docstore.add_documents(nodes)


db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("dense_vectors")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)


storage_context = StorageContext.from_defaults(
    docstore=docstore, vector_store=vector_store
)


index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)
```

```python
import nest_asyncio


nest_asyncio.apply()


from llama_index.core.retrievers import QueryFusionRetriever


retriever = QueryFusionRetriever(
    [
        index.as_retriever(similarity_top_k=2),
        BM25Retriever.from_defaults(
            docstore=index.docstore, similarity_top_k=2
        ),
    ],
    num_queries=1,
    use_async=True,
)
```

```text
BM25S Belirteçleri Sayma (Count Tokens):   0%|          | 0/61 [00:00<?, ?it/s]






BM25S Skorları Hesaplama (Compute Scores):   0%|          | 0/61 [00:00<?, ?it/s]
```

```python
nodes = retriever.retrieve("Viaweb ve Interleaf'te neler oldu?")
for node in nodes:
    display_source_node(node, source_length=5000)
```

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine(retriever)
```

```python
response = query_engine.query("Yazar RISD'den sonra ne yaptı?")
print(response)
```

```text
Yazar, RISD'den ayrıldıktan sonra müşteriler için projeler yapan bir grupta serbest (freelance) işler yapmak üzere anlaştı.
```

### Vektör Deposu (Vector Store) ile Kaydetme ve Yükleme

Verilerimiz chroma'da ve düğümlerimiz belge depomuzda (docstore) olduğunda, kaydedebilir ve yeniden oluşturabiliriz!

Vektör deposu zaten chroma tarafından otomatik olarak kaydedilir, ancak belge depomuzu (docstore) kaydetmemiz gerekecektir.

```python
storage_context.docstore.persist("./docstore.json")


# veya, belge deposunu görmezden gelebilir ve sadece bm25 erişimcisini aşağıda gösterildiği gibi kalıcı hale getirebiliriz:
# bm25_retriever.persist("./bm25_retriever")
```

Şimdi dizinimizi yeniden yükleyebilir ve yeniden oluşturabiliriz.

```python
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("dense_vectors")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)


docstore = SimpleDocumentStore.from_persist_path("./docstore.json")


storage_context = StorageContext.from_defaults(
    docstore=docstore, vector_store=vector_store
)


index = VectorStoreIndex(nodes=[], storage_context=storage_context)
```
