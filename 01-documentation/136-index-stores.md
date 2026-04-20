# İndeks Depoları (Index Stores)

İndeks depoları, hafif (lightweight) indeks meta verilerini (yani bir indeks oluştururken oluşturulan ek durum bilgilerini) içerir.

Daha fazla detay için [API Referansına](/python/framework-api-reference/storage/index_store) bakın.

### Basit İndeks Deposu (Simple Index Store)

Varsayılan olarak LlamaIndex, bellek içi bir anahtar-değer deposu tarafından desteklenen basit bir indeks deposu kullanır.
`index_store.persist()` (ve sırasıyla `SimpleIndexStore.from_persist_path(...)`) çağrılarak diskte kalıcı hale getirilebilirler (ve diskten yüklenebilirler).

### MongoDB İndeks Deposu

Döküman depolarına benzer şekilde, indeks deposunun saklama arka ucu olarak `MongoDB`'yi de kullanabiliriz.

```python
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.core import VectorStoreIndex

# indeks deposunu oluştur (veya yükle)
index_store = MongoIndexStore.from_uri(uri="<mongodb+srv://...>")

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(index_store=index_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# veya alternatif olarak, indeksi yükle
from llama_index.core import load_index_from_storage

index = load_index_from_storage(storage_context)
```

Arka planda `MongoIndexStore`, sabit bir MongoDB veritabanına bağlanır ve indeks meta verileriniz için yeni koleksiyonlar başlatır (veya mevcut koleksiyonları yükler).

> Not: `MongoIndexStore` başlatılırken `db_name` ve `namespace` değerlerini yapılandırabilirsiniz; aksi takdirde varsayılan olarak `db_name="db_docstore"` ve `namespace="docstore"` kullanılır.

`MongoIndexStore` kullanırken veriler varsayılan olarak kalıcı hale getirildiği için `storage_context.persist()` (veya `index_store.persist()`) çağırmanın gerekli olmadığını unutmayın.

Mevcut bir `db_name` ve `collection_name` ile bir `MongoIndexStore`'u yeniden başlatarak MongoDB koleksiyonunuza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/mongodocstoredemo) ulaşabilirsiniz.

### Redis İndeks Deposu

Redis'i, verileri dökümanlar alındıkça kalıcı hale getiren alternatif bir döküman deposu arka ucu olarak destekliyoruz.

```python
from llama_index.storage.index_store.redis import RedisIndexStore
from llama_index.core import VectorStoreIndex

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
index_store = RedisIndexStore.from_host_and_port(
    host="127.0.0.1", port="6379", namespace="llama_index"
)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(index_store=index_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# veya alternatif olarak, indeksi yükle
from llama_index.core import load_index_from_storage

index = load_index_from_storage(storage_context)
```

Arka planda `RedisIndexStore`, bir Redis veritabanına bağlanır ve node'larınızı `{namespace}/index` altında saklanan bir ad alanına (namespace) ekler.

> Not: `RedisIndexStore` başlatılırken `namespace` değerini yapılandırabilirsiniz; aksi takdirde varsayılan olarak `namespace="index_store"` kullanılır.

Mevcut bir `host`, `port` ve `namespace` ile bir `RedisIndexStore`'u yeniden başlatarak Redis istemcinize kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/redisdocstoreindexstoredemo) ulaşabilirsiniz.

### Couchbase İndeks Deposu

Couchbase, indeks deposu için saklama arka ucu olarak kullanılabilir.

```python
from llama_index.storage.index_store.couchbase import CouchbaseIndexStore
from llama_index.core import VectorStoreIndex

from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from datetime import timedelta

# couchbase istemcisini oluştur
auth = PasswordAuthenticator("DB_KULLANICI_ADI", "DB_PAROLA")
options = ClusterOptions(authenticator=auth)

cluster = Cluster("couchbase://localhost", options)

# Küme kullanım için hazır olana kadar bekle.
cluster.wait_until_ready(timedelta(seconds=5))

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
index_store = CouchbaseIndexStore.from_couchbase_client(
    client=cluster,
    bucket_name="llama-index",
    scope_name="_default",
    namespace="default",
)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(index_store=index_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# veya alternatif olarak, indeksi yükle
from llama_index.core import load_index_from_storage

index = load_index_from_storage(storage_context)
```

Arka planda `CouchbaseIndexStore`, bir Couchbase operasyonel veritabanına bağlanır ve node'larınızı belirtilen `{bucket_name}` ve `{scope_name}` altındaki `{namespace}_index` adlı bir koleksiyona ekler.

> Not: `CouchbaseIndexStore` başlatılırken `namespace`, `bucket` ve `scope` değerlerini yapılandırabilirsiniz. Varsayılan olarak kullanılan koleksiyon `index_store_data`'dır. Koleksiyon adının bir parçası olarak alfasayısal karakterlerin dışında sadece `-`, `_` ve `%` karakterlerine izin verilir. Depo, diğer özel karakterleri otomatik olarak `_` karakterine dönüştürecektir.

Mevcut bir `client`, `bucket_name`, `scope_name` ve `namespace` ile bir `CouchbaseIndexStore`'u yeniden başlatarak Couchbase istemcinize kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

### Tablestore İndeks Deposu

Döküman depolarına benzer şekilde, indeks deposunun saklama arka ucu olarak `Tablestore`'u da kullanabiliriz.

```python
from llama_index.storage.index_store.tablestore import TablestoreIndexStore
from llama_index.core import StorageContext, VectorStoreIndex

# indeks deposunu oluştur (veya yükle)
index_store = TablestoreIndexStore.from_config(
    endpoint="<tablestore_uc_noktasi>",
    instance_name="<tablestore_ornek_adi>",
    access_key_id="<tablestore_erisim_anahtari_id>",
    access_key_secret="<tablestore_erisim_anahtari_sirri>",
)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(index_store=index_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# veya alternatif olarak, indeksi yükle
from llama_index.core import load_index_from_storage

index = load_index_from_storage(storage_context)
```

Arka planda `TablestoreIndexStore`, bir Tablestore veritabanına bağlanır ve node'larınızı `{namespace}_data` adlı bir tabloya ekler.

> Not: `TablestoreIndexStore` başlatılırken `namespace` değerini yapılandırabilirsiniz.

Mevcut bir `endpoint`, `instance_name`, `access_key_id` ve `access_key_secret` ile bir `TablestoreIndexStore`'u yeniden başlatarak Tablestore veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha eksiksiz bir örneğe [buradan](/python/examples/docstore/tablestoredocstoredemo) ulaşabilirsiniz.

### Google AlloyDB İndeks Deposu

Döküman depolarına benzer şekilde, indeks deposunun saklama arka ucu olarak [`AlloyDB`](https://cloud.google.com/products/alloydb)'yi de kullanabiliriz.
Bu eğitim senkron arayüzü göstermektedir. Tüm senkron yöntemlerin karşılık gelen asenkron yöntemleri mevcuttur.

```bash
pip install llama-index
pip install llama-index-alloydb-pg
pip install llama-index-llms-vertex
```

```python
from llama_index_alloydb_pg import AlloyDBEngine, AlloyDBIndexStore
from llama_index.core import StorageContext, VectorStoreIndex

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
engine.init_index_store_table(
    table_name=TABLE_NAME,
)

index_store = AlloyDBIndexStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(index_store=index_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# veya alternatif olarak, indeksi yükle
from llama_index.core import load_index_from_storage

index = load_index_from_storage(storage_context)
```

> Not: Yeni bir tablo başlatırken ve `AlloyDBIndexStore` kurulumu yaparken `table_name` ile birlikte `schema_name` değerini de yapılandırabilirsiniz. Varsayılan olarak `schema_name` "public"tir.

Arka planda `AlloyDBIndexStore`, Google Cloud'daki alloydb veritabanına bağlanır ve node'larınızı `schema_name` altındaki bir tabloya ekler.

Yeni bir tablo başlatmadan bir `AlloyDBEngine` ile `AlloyDBIndexStore`'u yeniden başlatarak AlloyDB veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha detaylı bir kılavuza [buradan](/python/examples/docstore/alloydbdocstoredemo) ulaşabilirsiniz.

### Google Cloud SQL for PostgreSQL İndeks Deposu

Döküman depolarına benzer şekilde, indeks deposunun saklama arka ucu olarak [`Cloud SQL for PostgreSQL`](https://cloud.google.com/sql)'i de kullanabiliriz.
Bu eğitim senkron arayüzü göstermektedir. Tüm senkron yöntemlerin karşılık gelen asenkron yöntemleri mevcuttur.

```bash
pip install llama-index
pip install llama-index-cloud-sql-pg
```

```python
from llama_index_cloud_sql_pg import PostgresEngine, PostgresIndexStore
from llama_index.core import StorageContext, VectorStoreIndex

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
engine.init_index_store_table(
    table_name=TABLE_NAME,
)

index_store = PostgresIndexStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(index_store=index_store)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# veya alternatif olarak, indeksi yükle
from llama_index.core import load_index_from_storage

index = load_index_from_storage(storage_context)
```

> Not: Yeni bir tablo başlatırken ve `PostgresIndexStore` kurulumu yaparken `table_name` ile birlikte `schema_name` değerini de yapılandırabilirsiniz. Varsayılan olarak `schema_name` "public"tir.

Arka planda `PostgresIndexStore`, Google Cloud'daki cloud sql postgres veritabanına bağlanır ve node'larınızı `schema_name` altındaki bir tabloya ekler.

Yeni bir tablo başlatmadan bir `PostgresEngine` ile `PostgresIndexStore`'u yeniden başlatarak cloud sql postgres veritabanınıza kolayca yeniden bağlanabilir ve indeksi yeniden yükleyebilirsiniz.

Daha detaylı bir kılavuza [buradan](/python/examples/docstore/cloudsqlpgdocstoredemo) ulaşabilirsiniz.