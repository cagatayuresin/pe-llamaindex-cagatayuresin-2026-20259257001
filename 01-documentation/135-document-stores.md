# Döküman Depoları (Document Stores)

Döküman depoları (document stores), `Node` nesneleri olarak adlandırdığımız alınan döküman parçalarını içerir.

Daha fazla detay için [API Referansına](/python/framework-api-reference/storage/docstore) bakın.

### Basit Döküman Deposu (Simple Document Store)

Varsayılan olarak `SimpleDocumentStore`, `Node` nesnelerini bellekte (in-memory) saklar.
`docstore.persist()` (ve sırasıyla `SimpleDocumentStore.from_persist_path(...)`) çağrılarak diskte kalıcı hale getirilebilirler (ve diskten yüklenebilirler).

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/docstoredemo) ulaşabilirsiniz.

### MongoDB Döküman Deposu

Dökümanlar alındıkça (ingested) verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak MongoDB'yi destekliyoruz.

```python
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.core.node_parser import SentenceSplitter

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
docstore = MongoDocumentStore.from_uri(uri="<mongodb+srv://...>")
docstore.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=docstore)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Arka planda `MongoDocumentStore`, sabit bir MongoDB veritabanına bağlanır ve node'larınız için yeni koleksiyonlar başlatır (veya mevcut koleksiyonları yükler).

> Not: `MongoDocumentStore` başlatılırken `db_name` ve `namespace` değerlerini yapılandırabilirsiniz; aksi takdirde varsayılan olarak `db_name="db_docstore"` ve `namespace="docstore"` kullanılır.

`MongoDocumentStore` kullanırken veriler varsayılan olarak kalıcı hale getirildiği için `storage_context.persist()` (veya `docstore.persist()`) çağırmanın gerekli olmadığını unutmayın.

Mevcut bir `db_name` ve `collection_name` ile bir `MongoDocumentStore`'u yeniden başlatarak MongoDB koleksiyonunuza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/mongodocstoredemo) ulaşabilirsiniz.

### Redis Döküman Deposu

Dökümanlar alındıkça verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak Redis'i destekliyoruz.

```python
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.core.node_parser import SentenceSplitter

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
docstore = RedisDocumentStore.from_host_and_port(
    host="127.0.0.1", port="6379", namespace="llama_index"
)
docstore.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=docstore)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Arka planda `RedisDocumentStore`, bir Redis veritabanına bağlanır ve node'larınızı `{namespace}/docs` altında saklanan bir ad alanına (namespace) ekler.

> Not: `RedisDocumentStore` başlatılırken `namespace` değerini yapılandırabilirsiniz; aksi takdirde varsayılan olarak `namespace="docstore"` kullanılır.

Mevcut bir `host`, `port` ve `namespace` ile bir `RedisDocumentStore`'u yeniden başlatarak Redis istemcinize kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/redisdocstoreindexstoredemo) ulaşabilirsiniz.

### Firestore Döküman Deposu

Dökümanlar alındıkça verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak Firestore'u destekliyoruz.

```python
from llama_index.storage.docstore.firestore import FirestoreDocumentStore
from llama_index.core.node_parser import SentenceSplitter

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
docstore = FirestoreDocumentStore.from_database(
    project="proje-id",
    database="(default)",
)
docstore.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=docstore)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Arka planda `FirestoreDocumentStore`, Google Cloud'daki bir Firestore veritabanına bağlanır ve node'larınızı `{namespace}/docs` altında saklanan bir ad alanına ekler.

> Not: `FirestoreDocumentStore` başlatılırken `namespace` değerini yapılandırabilirsiniz; aksi takdirde varsayılan olarak `namespace="docstore"` kullanılır.

Mevcut bir `project`, `database` ve `namespace` ile bir `FirestoreDocumentStore`'u yeniden başlatarak Firestore veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/firestoredemo) ulaşabilirsiniz.

### Couchbase Döküman Deposu

Dökümanlar alındıkça verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak Couchbase'i destekliyoruz.

```python
from llama_index.storage.docstore.couchbase import CouchbaseDocumentStore
from llama_index.core.node_parser import SentenceSplitter

from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from datetime import timedelta

# couchbase istemcisi oluştur
auth = PasswordAuthenticator("DB_KULLANICI_ADI", "DB_PAROLA")
options = ClusterOptions(authenticator=auth)

cluster = Cluster("couchbase://localhost", options)

# Küme kullanım için hazır olana kadar bekle.
cluster.wait_until_ready(timedelta(seconds=5))

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
docstore = CouchbaseDocumentStore.from_couchbase_client(
    client=cluster,
    bucket_name="llama-index",
    scope_name="_default",
    namespace="default",
)
docstore.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=docstore)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Arka planda `CouchbaseDocumentStore`, bir Couchbase operasyonel veritabanına bağlanır ve node'larınızı belirtilen `{bucket_name}` ve `{scope_name}` altındaki `{namespace}_data` adlı bir koleksiyona ekler.

> Not: `CouchbaseIndexStore` başlatılırken `namespace`, `bucket` ve `scope` değerlerini yapılandırabilirsiniz. Varsayılan olarak kullanılan koleksiyon `docstore_data`'dır. Koleksiyon adının bir parçası olarak alfasayısal karakterlerin dışında sadece `-`, `_` ve `%` karakterlerine izin verilir. Depo, diğer özel karakterleri otomatik olarak `_` karakterine dönüştürecektir.

Mevcut bir `client`, `bucket_name`, `scope_name` ve `namespace` ile bir `CouchbaseDocumentStore`'u yeniden başlatarak Couchbase veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

### Tablestore Döküman Deposu

Dökümanlar alındıkça verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak Tablestore'u destekliyoruz.

```python
from llama_index.core import Document
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from llama_index.storage.docstore.tablestore import TablestoreDocumentStore

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
documents = [
    Document(text="Kedileri severim.", id_="1", metadata={"anahtar1": "değer1"}),
    Document(text="Mike köpekleri sever.", id_="2", metadata={"anahtar2": "değer2"}),
]
nodes = parser.get_nodes_from_documents(documents)

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
docs_store = TablestoreDocumentStore.from_config(
    endpoint="<tablestore_uc_noktasi>",
    instance_name="<tablestore_ornek_adi>",
    access_key_id="<tablestore_erisim_anahtari_id>",
    access_key_secret="<tablestore_erisim_anahtari_sirri>",
)
docs_store.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=docs_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Arka planda `TablestoreDocumentStore`, bir Tablestore veritabanına bağlanır ve node'larınızı `{namespace}_data` adlı bir tabloya ekler.

> Not: `TablestoreDocumentStore` başlatılırken `namespace` değerini yapılandırabilirsiniz.

Mevcut bir `endpoint`, `instance_name`, `access_key_id` ve `access_key_secret` ile bir `TablestoreDocumentStore`'u yeniden başlatarak Tablestore veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/tablestoredocstoredemo) ulaşabilirsiniz.

### Google AlloyDB Döküman Deposu

Dökümanlar alındıkça verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak [AlloyDB](https://cloud.google.com/products/alloydb)'yi destekliyoruz.

Bu eğitim senkron arayüzü göstermektedir. Tüm senkron yöntemlerin karşılık gelen asenkron yöntemleri mevcuttur.

```bash
pip install llama-index
pip install llama-index-alloydb-pg
pip install llama-index-llms-vertex
```

```python
from llama_index.core import SummaryIndex
from llama_index_alloydb_pg import AlloyDBEngine, AlloyDBDocumentStore

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# bağlantı havuzu için bir AlloyDB Engine oluştur
engine = AlloyDBEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    cluster=CLUSTER,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)

# AlloyDB'de yeni bir tablo başlat
engine.init_doc_store_table(
    table_name=TABLE_NAME,
)

doc_store = AlloyDBDocumentStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)

doc_store.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=doc_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

> Not: Yeni bir tablo başlatırken ve `AlloyDBDocumentStore` kurulumu yaparken `table_name` ile birlikte `schema_name` değerini de yapılandırabilirsiniz. Varsayılan olarak `schema_name` "public"tir.

Arka planda `AlloyDBDocumentStore`, Google Cloud'daki alloydb veritabanına bağlanır ve node'larınızı `schema_name` altındaki bir tabloya ekler.

Yeni bir tablo başlatmadan bir `AlloyDBEngine` ile `AlloyDBDocumentStore`'u yeniden başlatarak AlloyDB veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha detaylı bir kılavuza [buradan](/python/examples/docstore/alloydbdocstoredemo) ulaşabilirsiniz.

### Google Cloud SQL for PostgreSQL Döküman Deposu

Dökümanlar alındıkça verileri `Node` nesneleri olarak kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak [Cloud SQL for PostgreSQL](https://cloud.google.com/sql)'i destekliyoruz.

Bu eğitim senkron arayüzü göstermektedir. Tüm senkron yöntemlerin karşılık gelen asenkron yöntemleri mevcuttur.

```bash
pip install llama-index
pip install llama-index-cloud-sql-pg
```

```python
from llama_index.core import SummaryIndex
from llama_index_cloud_sql_pg import PostgresEngine, PostgresDocumentStore

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# bağlantı havuzu için bir Postgres Engine oluştur
engine = PostgresEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)

# cloud sql postgres'te yeni bir tablo başlat
engine.init_doc_store_table(
    table_name=TABLE_NAME,
)

doc_store = PostgresDocumentStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)

doc_store.add_documents(nodes)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(docstore=doc_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

> Not: Yeni bir tablo başlatırken ve `PostgresDocumentStore` kurulumu yaparken `table_name` ile birlikte `schema_name` değerini de yapılandırabilirsiniz. Varsayılan olarak `schema_name` "public"tir.

Arka planda `PostgresDocumentStore`, Google Cloud'daki cloud sql pg veritabanına bağlanır ve node'larınızı `schema_name` altındaki bir tabloya ekler.

Yeni bir tablo başlatmadan bir `PostgresEngine` ile `PostgresDocumentStore`'u yeniden başlatarak Postgres veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha detaylı bir kılavuza [buradan](/python/examples/docstore/cloudsqlpgdocstoredemo) ulaşabilirsiniz.