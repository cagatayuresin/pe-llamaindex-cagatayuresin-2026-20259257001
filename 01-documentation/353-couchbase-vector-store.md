---
title: Couchbase Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

[Couchbase](https://couchbase.com/), tüm bulut, mobil, yapay zeka ve uç bilişim (edge computing) uygulamalarınız için eşsiz çok yönlülük, performans, ölçeklenebilirlik ve finansal değer sunan, ödüllü, dağıtık bir NoSQL bulut veritabanıdır. Couchbase, geliştiriciler için kodlama yardımı ve uygulamaları için vektör araması ile yapay zekayı kucaklar.

Vektör Araması (Vector Search), Couchbase'deki [Tam Metin Arama Servisi](https://docs.couchbase.com/server/current/learn/services-and-indexes/services/search-service.html)'nin (Search Service) bir parçasıdır.

Bu öğretici, Couchbase'de Vektör Aramasının nasıl kullanılacağını açıklamaktadır. Hem [Couchbase Capella](https://www.couchbase.com/products/capella/) hem de kendi yönettiğiniz (self-managed) Couchbase Sunucusu ile çalışabilirsiniz.

## Kurulum

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-couchbase llama-index
```

## Couchbase Bağlantısı Oluşturma

Başlangıçta Couchbase kümesine (cluster) bir bağlantı oluşturuyoruz ve ardından küme nesnesini Vektör Deposuna iletiyoruz.

Burada, kullanıcı adı ve parola kullanarak bağlanıyoruz. Kümenize desteklenen diğer yöntemlerle de bağlanabilirsiniz.

Couchbase kümesine bağlanma hakkında daha fazla bilgi için lütfen [Python SDK belgelerini](https://docs.couchbase.com/python-sdk/current/hello-world/start-using-sdk.html#connect) kontrol edin.

```python
COUCHBASE_CONNECTION_STRING = (
    "couchbase://localhost"  # veya TLS kullanılıyorsa "couchbases://localhost"
)
DB_USERNAME = "Administrator"
DB_PASSWORD = "P@ssword1!"
```

```python
from datetime import timedelta


from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions


auth = PasswordAuthenticator(DB_USERNAME, DB_PASSWORD)
options = ClusterOptions(auth)
cluster = Cluster(COUCHBASE_CONNECTION_STRING, options)


# Küme kullanıma hazır olana kadar bekle.
cluster.wait_until_ready(timedelta(seconds=5))
```

## Arama İndeksi (Search Index) Oluşturma

Şu anda, Arama indeksinin Couchbase Capella veya Sunucu kullanıcı arayüzünden (UI) ya da REST arayüzü kullanılarak oluşturulması gerekmektedir.

`testing` bucket'ı üzerinde `vector-index` adında bir Arama indeksi tanımlayalım.

Bu örnek için kullanıcı arayüzündeki Arama Servisi'nde bulunan İndeksi İçe Aktar (Import Index) özelliğini kullanalım.

İndeksi, `testing` bucket'ının `_default` kapsamındaki (scope) `_default` koleksiyonu üzerinde; vektör alanı `embedding` (1536 boyutlu) ve metin alanı `text` olarak ayarlanacak şekilde tanımlıyoruz. Ayrıca, değişen belge yapılarını hesaba katmak için belgedeki meta veriler altındaki tüm alanları dinamik bir eşleme (dynamic mapping) olarak indeksliyor ve saklıyoruz. Benzerlik metriği `dot_product` (nokta çarpımı) olarak ayarlanmıştır.

#### Tam Metin Arama servisine bir İndeks nasıl aktarılır?

- [Couchbase Sunucusu (Couchbase Server)](https://docs.couchbase.com/server/current/search/import-search-index.html)

  - Search -> Add Index -> Import adımlarını izleyin.
  - İçe Aktar (Import) ekranına aşağıdaki İndeks tanımını kopyalayın.
  - İndeksi oluşturmak için Create Index'e tıklayın.

- [Couchbase Capella](https://docs.couchbase.com/cloud/search/import-search-index.html)

  - İndeks tanımını yeni bir `index.json` dosyasına kopyalayın.
  - Belgelerdeki talimatları izleyerek dosyayı Capella'ya aktarın.
  - İndeksi oluşturmak için Create Index'e tıklayın.

#### İndeks Tanımı (İngilizce Anahtarlar Korunmuştur)

```json
{
 "name": "vector-index",
 "type": "fulltext-index",
 "params": {
  "doc_config": {
   "docid_prefix_delim": "",
   "docid_regexp": "",
   "mode": "type_field",
   "type_field": "type"
  },
  "mapping": {
   "default_analyzer": "standard",
   "default_datetime_parser": "dateTimeOptional",
   "default_field": "_all",
   "default_mapping": {
    "dynamic": true,
    "enabled": true,
    "properties": {
     "metadata": {
      "dynamic": true,
      "enabled": true
     },
     "embedding": {
      "enabled": true,
      "dynamic": false,
      "fields": [
       {
        "dims": 1536,
        "index": true,
        "name": "embedding",
        "similarity": "dot_product",
        "type": "vector",
        "vector_index_optimized_for": "recall"
       }
      ]
     },
     "text": {
      "enabled": true,
      "dynamic": false,
      "fields": [
       {
        "index": true,
        "name": "text",
        "store": true,
        "type": "text"
       }
      ]
     }
    }
   },
   "default_type": "_default",
   "docvalues_dynamic": false,
   "index_dynamic": true,
   "store_dynamic": true,
   "type_field": "_type"
  },
  "store": {
   "indexType": "scorch",
   "segmentVersion": 16
  }
 },
 "sourceType": "gocbcore",
 "sourceName": "testing",
 "sourceParams": {},
 "planParams": {
  "maxPartitionsPerPIndex": 103,
  "indexPartitions": 10,
  "numReplicas": 0
 }
}
```

Şimdi Couchbase kümesinde Vektör Araması için kullanmak istediğimiz bucket, kapsam (scope) ve koleksiyon adlarını ayarlayacağız.

Bu örnek için varsayılan kapsam ve koleksiyonları kullanıyoruz.

```python
BUCKET_NAME = "testing"
SCOPE_NAME = "_default"
COLLECTION_NAME = "_default"
SEARCH_INDEX_NAME = "vector-index"
```

```python
# Gerekli paketleri içe aktar
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.vector_stores.couchbase import CouchbaseSearchVectorStore
```

Bu öğretici için OpenAI gömmelerini (embeddings) kullanacağız.

```python
import os
import getpass


os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Anahtarı:")
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

#### Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükle

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
vector_store = CouchbaseSearchVectorStore(
    cluster=cluster,
    bucket_name=BUCKET_NAME,
    scope_name=SCOPE_NAME,
    collection_name=COLLECTION_NAME,
    index_name=SEARCH_INDEX_NAME,
)
```

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

## Temel Örnek (Basic Example)

Sorgu motoruna az önce indekslediğimiz makale hakkında bir soru soracağız.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Y Combinator'daki yatırımları nelerdi?")
print(response)
```

**Y Combinator'daki yatırımları, kurucu başına 6 bin dolardı; bu da tipik iki kuruculu bir durumda, %6 özkaynak karşılığında toplamda 12 bin dolar ediyordu.**

## Meta Veri Filtreleri (Metadata Filters)

Meta verilere dayanarak belgelerin nasıl filtreleneceğini görebilmek için meta veriye sahip bazı örnek belgeler oluşturacağız.

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="The Shawshank Redemption",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
        },
    ),
    TextNode(
        text="The Godfather",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
        },
    ),
    TextNode(
        text="Inception",
        metadata={
            "director": "Christopher Nolan",
        },
    ),
]
vector_store.add(nodes)
```

```python
# Meta veri filtresi
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="theme", value="Mafia")]
)


retriever = index.as_retriever(filters=filters)


retriever.retrieve("Inception ne hakkındadır?")
```

## Özel Filtreler ve Sorguyu Geçersiz Kılma (Custom Filters and overriding Query)

Couchbase şu anda LlamaIndex üzerinden yalnızca `ExactMatchFilters` desteği sunmaktadır. Ancak Couchbase; aralık filtreleri, coğrafi filtreler ve daha fazlasını içeren geniş bir filtreleme yelpazesini destekler. Bu filtreleri kullanmak için, `cb_search_options` parametresine sözlüklerden (dictionaries) oluşan bir liste olarak iletebilirsiniz. `search_options` içindeki farklı arama/sorgu olasılıkları [burada](https://docs.couchbase.com/server/current/search/search-request-params.html#query-object) bulunabilir.

```python
def custom_query(query, query_str):
    print("özel sorgu (custom query)", query)
    return query




query_engine = index.as_query_engine(
    vector_store_kwargs={
        "cb_search_options": {
            "query": {"match": "growing up", "field": "text"}
        },
        "custom_query": custom_query,
    }
)
response = query_engine.query("Y Combinator'daki yatırımları nelerdi?")
print(response)
```

**Y Combinator'daki yatırımları; Julian ile yaptığı anlaşmanın ($10k karşılığında %10) ve Robert'ın MIT lisansüstü öğrencilerinin yaz dönemi için ne aldığını ($6k) söylemesinin bir kombinasyonuna dayanıyordu. Kurucu başına $6k yatırım yaptı; bu da tipik iki kuruculu vakada, %6 karşılığında $12k ediyordu.**
