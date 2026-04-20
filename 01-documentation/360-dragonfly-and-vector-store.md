---
title: Dragonfly ve Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Bu not defterinde, Dragonfly'ın Vektör Deposu ile kullanımına dair hızlı bir demo göstereceğiz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install -U llama-index llama-index-vector-stores-redis llama-index-embeddings-cohere llama-index-embeddings-openai
```

```python
import os
import getpass
import sys
import logging
import textwrap
import warnings


warnings.filterwarnings("ignore")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.redis import RedisVectorStore
```

### Dragonfly'ı Başlatın

Dragonfly'ı başlatmanın en kolay yolu Dragonfly docker imajını kullanmak veya bir [Dragonfly Cloud](https://www.dragonflydb.io/cloud) demo örneğine hızlıca kaydolmaktır.

Bu öğreticinin her adımını takip etmek için imajı aşağıdaki gibi başlatın:

Terminal penceresi

```bash
docker run -d -p 6379:6379 --name dragonfly docker.dragonflydb.io/dragonflydb/dragonfly
```

### OpenAI Kurulumu

Öncelikle openai api anahtarını ekleyerek başlayalım. Bu, gömmeler (embeddings) için openai'ye erişmemize ve chatgpt'yi kullanmamıza olanak tanıyacaktır.

```python
oai_api_key = getpass.getpass("OpenAI API Anahtarı:")
os.environ["OPENAI_API_KEY"] = oai_api_key
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Bir Veri Kümesini Okuyun

Burada, gömme haline getirilecek metni sağlamak, vektör deposunda saklamak ve LLM Soru-Cevap (QnA) döngümüz için bağlam bulmak amacıyla bir dizi Paul Graham makalesini kullanacağız.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print(
    "Belge Kimliği (Document ID):",
    documents[0].id_,
    "Belge Dosya Adı:",
    documents[0].metadata["file_name"],
)
```

### Varsayılan Vektör Deposunu Başlatın

Artık belgelerimiz hazır olduğuna göre, vektör deposunu **varsayılan** ayarlarla başlatabiliriz. Bu, vektörlerimizi Dragonfly'da saklamamıza ve gerçek zamanlı arama için bir indeks oluşturmamıza olanak tanıyacaktır.

```python
from llama_index.core import StorageContext
from redis import Redis


# istemci bağlantısı oluştur
redis_client = Redis.from_url("redis://localhost:6379")


# vektör deposu sarmalayıcısını (wrapper) oluştur
vector_store = RedisVectorStore(redis_client=redis_client, overwrite=True)


# depolama bağlamını (storage context) yükle
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# belgelerden ve depolama bağlamından indeksi oluştur ve yükle
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### Varsayılan Vektör Deposunu Sorgulayın

Artık verilerimiz indekste saklandığına göre, indekse yönelik sorular sorabiliriz.

İndeks, verileri bir LLM için bilgi tabanı (knowledge base) olarak kullanacaktır. `as_query_engine()` için varsayılan ayar, OpenAI gömmelerini ve dil modeli olarak GPT'yi kullanır. Bu nedenle, özelleştirilmiş veya yerel bir dil modeli seçmediğiniz sürece bir OpenAI anahtarı gereklidir.

Aşağıda, indeksimize karşı aramaları ve ardından bir LLM ile tam RAG akışını test edeceğiz.

```python
query_engine = index.as_query_engine()
retriever = index.as_retriever()
```

```python
result_nodes = retriever.retrieve("Yazar ne öğrendi?")
for node in result_nodes:
    print(node)
```

```python
response = query_engine.query("Yazar ne öğrendi?")
print(textwrap.fill(str(response), 100))
```

**Yazar, üniversitedeki felsefe derslerinin kendisi için sıkıcı olduğunu öğrendi ve bu da onu odağını yapay zeka (AI) çalışmalarına kaydırmaya yöneltti.**

```python
result_nodes = retriever.retrieve("Yazar için zor bir an neydi?")
for node in result_nodes:
    print(node)
```

**Hacker News (HN) ile ilgili acil sorunlarla ilgilenmek yazar için önemli bir stres kaynağıydı.**

```python
index.vector_store.delete_index()
```

### Özel bir İndeks Şeması Kullanın

Çoğu kullanım durumunda, temel indeks yapılandırmasını ve spesifikasyonunu özelleştirme yeteneğine ihtiyacınız vardır. Örneğin bu, etkinleştirmek istediğiniz belirli meta veri filtrelerini tanımlamak için kullanışlıdır.

Dragonfly ile bu, bir indeks şeması nesnesi (dosyadan veya sözlükten) tanımlamak ve bunu vektör deposu istemci sarmalayıcısına iletmek kadar basittir.

Bu örnek için şunları yapacağız:

1. Gömme modelini [Cohere](https://cohere.com/) olarak değiştireceğiz.
2. Belgenin `updated_at` zaman damgası (timestamp) için ek bir meta veri alanı ekleyeceğiz.
3. Mevcut `file_name` meta veri alanını indeksleyeceğiz.

```python
from llama_index.core.settings import Settings
from llama_index.embeddings.cohere import CohereEmbedding


# Cohere Anahtarını ayarla
co_api_key = getpass.getpass("Cohere API Anahtarı:")


Settings.embed_model = CohereEmbedding(api_key=co_api_key)
```

```python
from redisvl.schema import IndexSchema


custom_schema = IndexSchema.from_dict(
    {
        # temel indeks özelliklerini özelleştir
        "index": {
            "name": "paul_graham",
            "prefix": "essay",
            "key_separator": ":",
        },
        # indekslenen alanları özelleştir
        "fields": [
            # llamaindex için gerekli alanlar
            {"type": "tag", "name": "id"},
            {"type": "tag", "name": "doc_id"},
            {"type": "text", "name": "text"},
            # özel meta veri alanları
            {"type": "numeric", "name": "updated_at"},
            {"type": "tag", "name": "file_name"},
            # cohere gömmeleri için özel vektör alanı tanımı
            {
                "type": "vector",
                "name": "vector",
                "attrs": {
                    "dims": 1024,
                    "algorithm": "hnsw",
                    "distance_metric": "cosine",
                },
            },
        ],
    }
)
```

```python
from datetime import datetime


def date_to_timestamp(date_string: str) -> int:
    date_format: str = "%Y-%m-%d"
    return int(datetime.strptime(date_string, date_format).timestamp())


# belgeler arasında gezin ve yeni alanı ekle
for document in documents:
    document.metadata["updated_at"] = date_to_timestamp(
        document.metadata["last_modified_date"]
    )
```

```python
vector_store = RedisVectorStore(
    schema=custom_schema,  # özelleştirilmiş şemayı sağla
    redis_client=redis_client,
    overwrite=True,
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)


# belgelerden ve depolama bağlamından indeksi oluştur ve yükle
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### Vektör Deposunu Sorgulama ve Meta Veriye Göre Filtreleme

Artık Dragonfly'da indekslenen ek meta verilerimiz olduğuna göre, filtreli bazı sorgular deneyelim.

```python
from llama_index.core.vector_stores import (
    MetadataFilters,
    MetadataFilter,
    ExactMatchFilter,
)


retriever = index.as_retriever(
    similarity_top_k=3,
    filters=MetadataFilters(
        filters=[
            ExactMatchFilter(key="file_name", value="paul_graham_essay.txt"),
            MetadataFilter(
                key="updated_at",
                value=date_to_timestamp("2023-01-01"),
                operator=">=",
            ),
            MetadataFilter(
                key="text",
                value="öğrenmek (learn)",
                operator="text_match",
            ),
        ],
        condition="and",
    ),
)
```

```python
result_nodes = retriever.retrieve("Yazar ne öğrendi?")


for node in result_nodes:
    print(node)
```

### Belgeleri veya İndeksi Tamamen Silme

Bazen belgeleri veya tüm indeksi silmek faydalı olabilir. Bu, `delete` ve `delete_index` yöntemleri kullanılarak yapılabilir.

```python
document_id = documents[0].doc_id


print("Silmeden önceki belge sayısı", redis_client.dbsize())
vector_store.delete(document_id)
print("Sildikten sonraki belge sayısı", redis_client.dbsize())
```

Ancak indeks hala mevcuttur (ilişkili belgesi olmasa bile).

```python
vector_store.index_exists()
```

```python
# şimdi indeksi tamamen silelim
# bu, tüm belgeleri ve indeksi silecektir
vector_store.delete_index()
```

```python
print("Sildikten sonraki belge sayısı", redis_client.dbsize())
```
