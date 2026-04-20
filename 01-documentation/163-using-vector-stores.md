# Vektör Depolarını (Vector Stores) Kullanma

LlamaIndex, vektör depoları / vektör veritabanları ile birden fazla entegrasyon noktası sunar:

1. LlamaIndex, bir vektör deposunun kendisini bir indeks olarak kullanabilir. Diğer tüm indeksler gibi, bu indeks de dökümanları saklayabilir ve sorguları yanıtlamak için kullanılabilir.
2. LlamaIndex, diğer tüm veri bağlayıcılarına benzer şekilde vektör depolarından veri yükleyebilir. Bu veriler daha sonra LlamaIndex veri yapıları içinde kullanılabilir.

## Bir Vektör Deposunu İndeks Olarak Kullanma

LlamaIndex, `VectorStoreIndex` için depolama arka ucu olarak farklı vektör depolarını destekler.

-   Alibaba Cloud OpenSearch (`AlibabaCloudOpenSearchStore`). [Hızlı Başlangıç](https://help.aliyun.com/zh/open-search/vector-search-edition).
-   Amazon Neptune - Neptune Analytics (`NeptuneAnalyticsVectorStore`). [Neptune Analytics'te vektör benzerliği ile çalışma](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/vector-similarity.html).
-   CQL aracılığıyla Apache Cassandra® ve Astra DB (`CassandraVectorStore`). [Kurulum](https://cassandra.apache.org/doc/stable/cassandra/getting_started/installing.html) [Hızlı Başlangıç](https://docs.datastax.com/en/astra-serverless/docs/vector-search/overview.html)
-   Astra DB (`AstraDBVectorStore`). [Hızlı Başlangıç](https://docs.datastax.com/en/astra/home/astra.html).
-   AWS Document DB (`AWSDocDbVectorStore`). [Hızlı Başlangıç](https://docs.aws.amazon.com/documentdb/latest/developerguide/get-started-guide.html).
-   Azure AI Search (`AzureAISearchVectorStore`). [Hızlı Başlangıç](https://learn.microsoft.com/en-us/azure/search/search-get-started-vector)
-   Azure Cosmos DB Mongo vCore (`AzureCosmosDBMongoDBVectorSearch`). [Hızlı Başlangıç](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search?tabs=diskann)
-   Azure Cosmos DB NoSql (`AzureCosmosDBNoSqlVectorSearch`). [Hızlı Başlangıç](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search)
-   Chroma (`ChromaVectorStore`) [Kurulum](https://docs.trychroma.com/getting-started)
-   ClickHouse (`ClickHouseVectorStore`) [Kurulum](https://clickhouse.com/docs/en/install)
-   Couchbase (`CouchbaseSearchVectorStore`) [Kurulum](https://www.couchbase.com/products/capella/)
-   DashVector (`DashVectorStore`). [Kurulum](https://help.aliyun.com/document_detail/2510230.html).
-   DeepLake (`DeepLakeVectorStore`) [Kurulum](https://docs.deeplake.ai/en/latest/Installation.html)
-   DocArray (`DocArrayHnswVectorStore`, `DocArrayInMemoryVectorStore`). [Kurulum/Python İstemcisi](https://github.com/docarray/docarray#installation).
-   Elasticsearch (`ElasticsearchStore`) [Kurulum](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
-   Epsilla (`EpsillaVectorStore`) [Kurulum/Hızlı Başlangıç](https://epsilla-inc.gitbook.io/epsilladb/quick-start)
-   Faiss (`FaissVectorStore`). [Kurulum](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md).
-   PostgreSQL için Google AlloyDB (`AlloyDBVectorStore`). [Hızlı Başlangıç](https://github.com/googleapis/llama-index-alloydb-pg-python/blob/main/samples/llama_index_vector_store.ipynb).
-   PostgreSQL için Google Cloud SQL (`PostgresVectorStore`). [Hızlı Başlangıç](https://github.com/googleapis/llama-index-cloud-sql-pg-python/blob/main/samples/llama_index_vector_store.ipynb)
-   Hnswlib (`HnswlibVectorStore`). [Kurulum](https://github.com/nmslib/hnswlib?tab=readme-ov-file#bindings-installation).
-   txtai (`TxtaiVectorStore`). [Kurulum](https://neuml.github.io/txtai/install/).
-   Jaguar (`JaguarVectorStore`). [Kurulum](http://www.jaguardb.com/docsetup.html).
-   Lantern (`LanternVectorStore`). [Hızlı Başlangıç](https://docs.lantern.dev/get-started/overview).
-   MariaDB (`MariaDBVectorStore`). [MariaDB Vektör Genel Bakış](https://mariadb.com/kb/en/vector-overview/)
-   Milvus (`MilvusVectorStore`). [Kurulum](https://milvus.io/docs)
-   MongoDB Atlas (`MongoDBAtlasVectorSearch`). [Kurulum/Hızlı Başlangıç](https://www.mongodb.com/atlas/database).
-   MyScale (`MyScaleVectorStore`). [Hızlı Başlangıç](https://docs.myscale.com/en/quickstart/). [Kurulum/Python İstemcisi](https://docs.myscale.com/en/python-client/).
-   Neo4j (`Neo4jVectorIndex`). [Kurulum](https://neo4j.com/docs/operations-manual/current/installation/).
-   OceanBase (`OceanBaseVectorStore`). [OceanBase Genel Bakış](https://github.com/oceanbase/oceanbase). [Hızlı Başlangıç](/python/examples/vector_stores/oceanbasevectorstore). [Python İstemcisi](https://github.com/oceanbase/pyobvector)
-   Opensearch (`OpensearchVectorStore`) [Vektör veritabanı olarak Opensearch](https://opensearch.org/platform/search/vector-database.html). [Hızlı Başlangıç](https://opensearch.org/docs/latest/search-plugins/knn/index/)
-   Pinecone (`PineconeVectorStore`). [Kurulum/Hızlı Başlangıç](https://docs.pinecone.io/docs/quickstart).
-   Qdrant (`QdrantVectorStore`) [Kurulum](https://qdrant.tech/documentation/install/) [Python İstemcisi](https://qdrant.tech/documentation/install/#python-client)
-   LanceDB (`LanceDBVectorStore`) [Kurulum/Hızlı Başlangıç](https://lancedb.github.io/lancedb/basic/)
-   Redis (`RedisVectorStore`). [Kurulum](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/).
-   Relyt (`RelytVectorStore`). [Hızlı Başlangıç](https://docs.relyt.cn/docs/vector-engine/).
-   Supabase (`SupabaseVectorStore`). [Hızlı Başlangıç](https://supabase.github.io/vecs/api/).
-   Tablestore (`Tablestore`). [Tablestore Genel Bakış](https://www.aliyun.com/product/ots). [Hızlı Başlangıç](/python/examples/vector_stores/tablestoredemo). [Python İstemcisi](https://github.com/aliyun/aliyun-tablestore-python-sdk).
-   TiDB (`TiDBVectorStore`). [Hızlı Başlangıç](/python/examples/vector_stores/tidbvector). [Kurulum](https://tidb.cloud/ai). [Python İstemcisi](https://github.com/pingcap/tidb-vector-python).
-   TimeScale (`TimescaleVectorStore`). [Kurulum](https://github.com/timescale/python-vector).
-   Upstash (`UpstashVectorStore`). [Hızlı Başlangıç](https://upstash.com/docs/vector/overall/getstarted)
-   VectorX DB (`VectorXVectorStore`). [Hızlı Başlangıç](https://docs.vectorxdb.ai/quickstart)
-   Vertex AI Vektör Araması (`VertexAIVectorStore`). [Hızlı Başlangıç](https://cloud.google.com/vertex-ai/docs/vector-search/quickstart)
-   Volcengine MySQL (VolcengineMySQLVectorStore). [Hızlı Başlangıç](https://www.volcengine.com/docs/6313/1978527?lang=en)
-   Weaviate (`WeaviateVectorStore`). [Kurulum](https://weaviate.io/developers/weaviate/installation). [Python İstemcisi](https://weaviate.io/developers/weaviate/client-libraries/python).
-   WordLift (`WordliftVectorStore`). [Hızlı Başlangıç](https://docs.wordlift.io/llm-connectors/wordlift-vector-store/). [Python İstemcisi](https://pypi.org/project/wordlift-client/).
-   Zep (`ZepVectorStore`). [Kurulum](https://docs.getzep.com/deployment/quickstart/). [Python İstemcisi](https://docs.getzep.com/sdk/).
-   Zilliz (`MilvusVectorStore`). [Hızlı Başlangıç](https://zilliz.com/doc/quick_start)

Ayrıntılı bir API referansı [burada bulunabilir](/python/framework-api-reference/storage/vector_store).

LlamaIndex içindeki diğer herhangi bir indeks (ağaç, anahtar kelime tablosu, liste) gibi, `VectorStoreIndex` de herhangi bir döküman koleksiyonu üzerine inşa edilebilir. Girdi metin parçalarının (chunks) embedding'lerini saklamak için indeks içindeki vektör deposunu kullanırız.

İndeks oluşturulduktan sonra sorgulama için kullanılabilir.

**Varsayılan Vektör Depo İndeksi Oluşturma/Sorgulama**

Varsayılan olarak, `VectorStoreIndex`, varsayılan depolama bağlamının (storage context) bir parçası olarak başlatılan bellek içi bir `SimpleVectorStore` kullanır.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Dökümanları yükle ve indeksi oluştur
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectorStoreIndex.from_documents(documents)

# İndeksi sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken ne yaptı?")
```

**Özel Vektör Depo İndeksi Oluşturma/Sorgulama**

Özel bir vektör deposu üzerinde şu şekilde sorgulama yapabiliriz:

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.deeplake import DeepLakeVectorStore

# vektör deposunu oluştur ve depolama bağlamını özelleştir
storage_context = StorageContext.from_defaults(
    vector_store=DeepLakeVectorStore(dataset_path="<veri_seti_yolu>")
)

# Dökümanları yükle ve indeksi oluştur
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# İndeksi sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken ne yaptı?")
```

Aşağıda desteklediğimiz çeşitli vektör depolarının nasıl oluşturulacağına dair daha fazla örnek gösteriyoruz.

**Alibaba Cloud OpenSearch**

```python
from llama_index.vector_stores.alibabacloud_opensearch import (
    AlibabaCloudOpenSearchStore,
    AlibabaCloudOpenSearchConfig,
)

config = AlibabaCloudOpenSearchConfig(
    endpoint="***",
    instance_id="***",
    username="your_username",
    password="your_password",
    table_name="llama",
)

vector_store = AlibabaCloudOpenSearchStore(config)
```

**PostgreSQL için Google AlloyDB**

```bash
pip install llama-index
pip install llama-index-alloydb-pg
pip install llama-index-llms-vertex
gcloud services enable aiplatform.googleapis.com
```

```python
from llama_index_alloydb_pg import AlloyDBEngine, AlloyDBVectorStore
from llama_index.core import Settings
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex
import google.auth

# Kendi AlloyDB bilgilerinizle değiştirin
engine = AlloyDBEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    cluster=CLUSTER,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)

engine.init_vector_store_table(
    table_name=TABLE_NAME,
    vector_size=768,  # VertexAI modeli (textembedding-gecko@latest) için vektör boyutu
)

vector_store = AlloyDBVectorStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)
```

**Amazon Neptune - Neptune Analytics**

```python
from llama_index.vector_stores.neptune import NeptuneAnalyticsVectorStore

graph_identifier = ""
embed_dim = 1536

neptune_vector_store = NeptuneAnalyticsVectorStore(
    graph_identifier=graph_identifier, embedding_dimension=1536
)
```

**Apache Cassandra®**

```python
from llama_index.vector_stores.cassandra import CassandraVectorStore
import cassio

# CQL aracılığıyla bir Astra DB bulut örneği kullanmak için:
cassio.init(database_id="1234abcd-...", token="AstraCS:...")

# Bir Cassandra kümesi (cluster) için:
from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"])
cassio.init(session=cluster.connect(), keyspace="my_keyspace")

# Yukarıdaki `cassio.init(...)` işleminden sonra bir vektör deposu oluşturun:
vector_store = CassandraVectorStore(
    table="cass_v_table", embedding_dimension=1536
)
```

**Astra DB**

```python
from llama_index.vector_stores.astra_db import AstraDBVectorStore

astra_db_store = AstraDBVectorStore(
    token="AstraCS:xY3b...",  # Astra DB belirteciniz
    api_endpoint="https://012...abc-us-east1.apps.astra.datastax.com",  # Astra DB API uç noktanız
    collection_name="astra_v_table",  # Seçtiğiniz bir tablo adı
    embedding_dimension=1536,  # Kullanılan embedding modelinin boyutu
)
```

**Azure Bilişsel Arama (Azure Cognitive Search)**

```python
from azure.core.credentials import AzureKeyCredential
from llama_index.vector_stores.azureaisearch import AzureAISearchVectorStore

search_service_api_key = "AZURE-SEARCH-SERVIS-ADMIN-ANAHTARINIZ"
search_service_endpoint = "AZURE-SEARCH-SERVIS-UC-NOKTANIZ"
search_service_api_version = "2023-11-01"
credential = AzureKeyCredential(search_service_api_key)

# Kullanılacak indeks adı
index_name = "llamaindex-vector-demo"

client = SearchIndexClient(
    endpoint=search_service_endpoint,
    credential=credential,
)

vector_store = AzureAISearchVectorStore(
    search_or_index_client=client,
    index_name=index_name,
    embedding_dimensionality=1536,
)
```

**Azure CosmosDB Mongo vCore**

```python
import pymongo
import os
from llama_index.vector_stores.azurecosmosmongo import (
    AzureCosmosDBMongoDBVectorSearch,
)

# Bağlantı dizesini Azure CosmosDB MongoDB URI'nizle ayarlayın
connection_string = os.getenv("AZURE_COSMOSDB_MONGODB_URI_NIZ")
mongodb_client = pymongo.MongoClient(connection_string)

# Bir AzureCosmosDBMongoDBVectorSearch örneği oluşturun
vector_store = AzureCosmosDBMongoDBVectorSearch(
    mongodb_client=mongodb_client,
    db_name="demo_vectordb",
    collection_name="paul_graham_essay",
)
```

**Azure CosmosDB NoSql**

```python
from azure.cosmos import CosmosClient, PartitionKey
import os
from llama_index.vector_stores.azurecosmosnosql import (
    AzureCosmosDBNoSqlVectorSearch,
)

URL = os.getenv("AZURE_COSMOSDB_URI")
KEY = os.getenv("AZURE_COSMOSDB_KEY")
database_name = "test_database"
container_name = "test_container"
test_client = CosmosClient(URL, credential=KEY)

indexing_policy = {
    "indexingMode": "consistent",
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{"path": '/"_etag"/?'}],
    "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
}

vector_embedding_policy = {
    "vectorEmbeddings": [
        {
            "path": "/embedding",
            "dataType": "float32",
            "distanceFunction": "cosine",
            "dimensions": 1536,
        }
    ]
}

partition_key = PartitionKey(path="/id")
cosmos_container_properties_test = {"partition_key": partition_key}
cosmos_database_properties_test = {}

vector_store = AzureCosmosDBNoSqlVectorSearch(
    cosmos_client=test_client,
    vector_embedding_policy=vector_embedding_policy,
    indexing_policy=indexing_policy,
    database_name=database_name,
    container_name=container_name,
    cosmos_database_properties=cosmos_database_properties_test,
    cosmos_container_properties=cosmos_container_properties_test,
)
```

**Chroma**

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

# Bir Chroma istemcisi oluşturma
# EphemeralClient tamamen bellek içinde çalışır, PersistentClient disk üzerine de kaydeder
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")

# vektör deposunu oluştur
vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection,
)
```

**ClickHouse**

```python
import clickhouse_connect
from llama_index.vector_stores import ClickHouseVectorStore

# Bir ClickHouse istemcisi oluşturma
client = clickhouse_connect.get_client(
    host="KUME_HOSTUNUZ",
    port=8123,
    username="KULLANICI_ADINIZ",
    password="KUME_SIFRENIZ",
)

# vektör deposunu oluştur
vector_store = ClickHouseVectorStore(clickhouse_client=client)
```

**Couchbase**

```python
from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions

# Bir Couchbase Kümesi nesnesi oluşturun
auth = PasswordAuthenticator("VERITABANI_KULLANICI_ADI", "VERITABANI_SIFRESI")
options = ClusterOptions(auth)
cluster = Cluster("KUME_BAGLANTI_DIZESI", options)

# Küme kullanılmaya hazır olana kadar bekle.
cluster.wait_until_ready(timedelta(seconds=5))

# Vektör Deposunu Oluştur
vector_store = CouchbaseSearchVectorStore(
    cluster=cluster,
    bucket_name="BUCKET_ADI",
    scope_name="SCOPE_ADI",
    collection_name="COLLECTION_ADI",
    index_name="ARAMA_INDEKSI_ADI",
)
```

**DashVector**

```python
import dashvector
from llama_index.vector_stores.dashvector import DashVectorStore

# dashvector istemcisini başlat
client = dashvector.Client(
    api_key="your-dashvector-api-key",
    endpoint="your-dashvector-cluster-endpoint",
)

# bir DashVector koleksiyonu oluşturma
client.create("quickstart", dimension=1536)
collection = client.get("quickstart")

# vektör deposunu oluştur
vector_store = DashVectorStore(collection)
```

**DeepLake**

```python
import os
from llama_index.vector_stores.deeplake import DeepLakeVectorStore

os.environ["OPENAI_API_KEY"] = "OPENAI_API_ANAHTARINIZ"
os.environ["ACTIVELOOP_TOKEN"] = "ACTIVELOOP_BELIRTECINIZ"
dataset_path = "hub://adilkhan/paul_graham_essay"

# vektör deposunu oluştur
vector_store = DeepLakeVectorStore(dataset_path=dataset_path, overwrite=True)
```

**DocArray**

```python
from llama_index.vector_stores.docarray import (
    DocArrayHnswVectorStore,
    DocArrayInMemoryVectorStore,
)

# vektör deposunu oluştur
vector_store = DocArrayHnswVectorStore(work_dir="hnsw_index")

# alternatif olarak, bellek içi vektör deposunu oluşturun
vector_store = DocArrayInMemoryVectorStore()
```

**Elasticsearch**

Öncelikle, Elasticsearch'ü yerel olarak veya [Elastic cloud](https://cloud.elastic.co/registration?utm_source=llama-index&utm_content=documentation) üzerinde başlatabilirsiniz.

Elasticsearch'ü docker ile yerel olarak başlatmak için aşağıdaki komutu çalıştırın:

```bash
docker run -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.security.http.ssl.enabled=false" \
  -e "xpack.license.self_generated.type=trial" \
  docker.elastic.co/elasticsearch/elasticsearch:8.9.0
```

Ardından bağlanın ve LlamaIndex ile Elasticsearch'ü bir vektör veritabanı olarak kullanın

```python
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

vector_store = ElasticsearchStore(
    index_name="llm-project",
    es_url="http://localhost:9200",
    # Bulut bağlantı seçenekleri:
    # es_cloud_id="<cloud_id>",
    # es_user="elastic",
    # es_password="<password>",
)
```

Bu, erişim, sorgulama, silme, indeksi kalıcı hale getirme ve daha fazlası için bir sorgu arayüzü sağlamak üzere `VectorStoreIndex` ile birlikte kullanılabilir.

**Epsilla**

```python
from pyepsilla import vectordb
from llama_index.vector_stores.epsilla import EpsillaVectorStore

# Bir Epsilla istemcisi oluşturma
epsilla_client = vectordb.Client()

# vektör deposunu oluştur
vector_store = EpsillaVectorStore(client=epsilla_client)
```

**Not**: `EpsillaVectorStore`, `pyepsilla` kütüphanesine ve çalışan bir Epsilla vektör veritabanına bağlıdır.
Henüz kurulu değilse `pip/pip3 install pyepsilla` kullanın.
Çalışan bir Epsilla vektör veritabanı docker imajı aracılığıyla bulunabilir.
Eksiksiz talimatlar için şu dökümantasyona bakın:
https://epsilla-inc.gitbook.io/epsilladb/quick-start

**Faiss**

```python
import faiss
from llama_index.vector_stores.faiss import FaissVectorStore

# faiss indeksi oluştur
d = 1536
faiss_index = faiss.IndexFlatL2(d)

# vektör deposunu oluştur
vector_store = FaissVectorStore(faiss_index)

# güncelleme/silme işlevi gerekiyorsa FaissMapVectorStore'dan yararlanabilirsiniz

d = 1536
faiss_index = faiss.IndexFlatL2(d)
id_map_index = faiss.IndexIDMap2(faiss_index)
vector_store = FaissMapVectorStore(id_map_index)

...

# NOT: faiss indeksi bellek içi olduğundan, diske kaydetmek için
#       açıkça vector_store.persist() veya storage_context.persist() çağırmamız gerekir.
#       persist() isteğe bağlı persist_path argümanı alır. Belirtilmezse varsayılan yolları kullanır.
storage_context.persist()
```

**PostgreSQL için Google Cloud SQL**

```bash
pip install llama-index
pip install llama-index-cloud-sql-pg
pip install llama-index-llms-vertex
gcloud services enable aiplatform.googleapis.com
```

```python
from llama_index_cloud_sql_pg import PostgresEngine, PostgresVectorStore
from llama_index.core import Settings
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex
import google.auth

# Kendi Cloud SQL bilgilerinizle değiştirin
engine = PostgresEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)

engine.init_vector_store_table(
    table_name=TABLE_NAME,
    vector_size=768,  # VertexAI modeli (textembedding-gecko@latest) için vektör boyutu
)

vector_store = PostgresVectorStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)
```

**txtai**

```python
import txtai
from llama_index.vector_stores.txtai import TxtaiVectorStore

# txtai indeksi oluştur
txtai_index = txtai.ann.ANNFactory.create(
    {"backend": "numpy", "dimension": 512}
)

# vektör deposunu oluştur
vector_store = TxtaiVectorStore(txtai_index)
```

**Jaguar**

```python
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import VectorStoreQuery
from jaguardb_http_client.JaguarHttpClient import JaguarHttpClient
from llama_index.vector_stores.jaguar import JaguarVectorStore


# vektör deposu istemcisini oluştur
url = "http://127.0.0.1:8080/fwww/"
pod = "vdb"
store = "llamaindex_rag_store"
vector_index = "v"
vector_type = "cosine_fraction_float"
vector_dimension = 3

# jaguar deposu sunucusuna bağlanmak için jaguar API anahtarını tutan
# JAGUAR_API_KEY çevre değişkeni veya $HOME/.jagrc dosyası gerektirir
vector_store = JaguarVectorStore(
    pod, store, vector_index, vector_type, vector_dimension, url
)

# güvenlik kimlik doğrulaması için jaguar sunucusuna giriş yap
vector_store.login()

# arka uç sunucusunda bir vektör deposu oluştur
metadata_fields = "author char(32), category char(16)"
text_size = 1024
vector_store.create(metadata_fields, text_size)

# biraz metin sakla
node = TextNode(
    text="Return of King Lear",
    metadata={"author": "William", "category": "Tragedy"},
    embedding=[0.9, 0.1, 0.4],
)
vector_store.add(nodes=[node], use_node_metadata=True)

# bir sorgu yap
qembedding = [0.4, 0.2, 0.8]
vsquery = VectorStoreQuery(query_embedding=qembedding, similarity_top_k=1)
query_result = vector_store.query(vsquery)

# meta veri filtresi (where koşulu) ile bir sorgu yap
qembedding = [0.6, 0.1, 0.4]
vsquery = VectorStoreQuery(query_embedding=qembedding, similarity_top_k=3)
where = "author='Eve' or (author='Adam' and category='History')"
query_result = vector_store.query(vsquery, where=where)

# eski verileri görmezden gelen bir sorgu yap (zaman kesintisi ile)
qembedding = [0.3, 0.3, 0.8]
vsquery = VectorStoreQuery(query_embedding=qembedding, similarity_top_k=3)
args = "day_cutoff=180"  # sadece son 180 günlük veriyi ara
query_result = vector_store.query(vsquery, args=args)

# bir vektörün anormal olup olmadığını kontrol et
text = ("Rüzgar Gibi Geçti",)
embed_of_text = [0.7, 0.1, 0.2]
node = TextNode(text=text, embedding=embed_of_text)
true_or_false = vector_store.is_anomalous(node)

# llama_index RAG uygulaması
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex

question = "Yazar büyürken ne yaptı?"

storage_context = StorageContext.from_defaults(vector_store=vector_store)
embed_model = OpenAIEmbedding()
embed_of_question = [0.7, 0.1, 0.2]

db_documents = vector_store.load_documents(embed_of_question, 10)
index = VectorStoreIndex.from_documents(
    db_documents,
    embed_model=embed_model,
    storage_context=storage_context,
)

query_engine = index.as_query_engine()
print(f"Soru: {question}")
response = query_engine.query(question)
print(f"Cevap: {str(response)}")

# kaynakları temizlemek için çıkış yap
vector_store.logout()
```

**Not**: İstemci (jaguardb-http-client gerektirir) <--> Http Ağ Geçidi (Gateway) <--> JaguarDB Sunucusu
İstemci tarafının çalıştırması gerekir: "pip install -U jaguardb-http-client"

**MariaDB**

```python
from llama_index.vector_stores.mariadb import MariaDBVectorStore

vector_store = MariaDBVectorStore.from_params(
    host="localhost",
    port=3306,
    user="llamaindex",
    password="password",
    database="vectordb",
    table_name="llama_index_vectorstore",
    embed_dim=1536,  # OpenAI embedding boyutu
)
```

**Milvus**

-   Milvus İndeksi hem dökümanları hem de embedding'lerini saklama yeteneği sunar.

```python
import pymilvus
from llama_index.vector_stores.milvus import MilvusVectorStore

# vektör deposunu oluştur
vector_store = MilvusVectorStore(
    uri="https://localhost:19530", overwrite="True"
)
```

**Not**: `MilvusVectorStore`, `pymilvus` kütüphanesine bağlıdır.
Zaten kurulu değilse `pip install pymilvus` kullanın.
`grpcio` için wheel oluştururken takılırsanız, python 3.11 kullanıp kullanmadığınızı kontrol edin
(bilinen bir sorun vardır: https://github.com/milvus-io/pymilvus/issues/1308)
ve sürüm düşürmeyi deneyin.

**MongoDBAtlas**

```python
# Kurucuya (constructor) URI sağlayın veya çevre değişkeni kullanın
import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader

# mongo_uri = os.environ["MONGO_URI"]
mongo_uri = (
    "mongodb+srv://<username>:<password>@<host>?retryWrites=true&w=majority"
)
mongodb_client = pymongo.MongoClient(mongo_uri)
async_mongodb_client = pymongo.AsyncMongoClient(mongo_uri)

# depoyu oluştur
store = MongoDBAtlasVectorSearch(
    mongodb_client=mongodb_client, async_mongodb_client=async_mongodb_client
)
storage_context = StorageContext.from_defaults(vector_store=store)
uber_docs = SimpleDirectoryReader(
    input_files=["../data/10k/uber_2021.pdf"]
).load_data()

# indeksi oluştur
index = VectorStoreIndex.from_documents(
    uber_docs, storage_context=storage_context
)
```

**MyScale**

```python
import clickhouse_connect
from llama_index.vector_stores.myscale import MyScaleVectorStore

# Bir MyScale istemcisi oluşturma
client = clickhouse_connect.get_client(
    host="KUME_HOSTUNUZ",
    port=8443,
    username="KULLANICI_ADINIZ",
    password="KUME_SIFRENIZ",
)


# vektör deposunu oluştur
vector_store = MyScaleVectorStore(myscale_client=client)
```

**Neo4j**

-   Neo4j metinleri, meta verileri ve embedding'leri saklar ve meta veri biçiminde grafik verilerini döndürecek şekilde özelleştirilebilir.

```python
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore

# vektör deposunu oluştur
neo4j_vector = Neo4jVectorStore(
    username="neo4j",
    password="pleaseletmein",
    url="bolt://localhost:7687",
    embed_dim=1536,
)
```

**Pinecone**

```python
import pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Bir Pinecone indeksi oluşturma
api_key = "api_anahtarınız"
pinecone.init(api_key=api_key, environment="us-west1-gcp")
pinecone.create_index(
    "quickstart", dimension=1536, metric="euclidean", pod_type="p1"
)
index = pinecone.Index("quickstart")

# vektör deposunu oluştur
vector_store = PineconeVectorStore(pinecone_index=index)
```

**Qdrant**

```python
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore

# Bir Qdrant vektör deposu oluşturma
client = qdrant_client.QdrantClient(
    host="<qdrant-host>", api_key="<qdrant-api-key>", https=True
)
collection_name = "paul_graham"

# vektör deposunu oluştur
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
)
```

**Redis**

Öncelikle Redis-Stack'i başlatın (veya Redis sağlayıcısından url alın)

```bash
docker run --name redis-vecdb -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

Ardından bağlanın ve LlamaIndex ile Redis'i bir vektör veritabanı olarak kullanın

```python
from llama_index.vector_stores.redis import RedisVectorStore

vector_store = RedisVectorStore(
    index_name="llm-project",
    redis_url="redis://localhost:6379",
    overwrite=True,
)
```

Bu, erişim, sorgulama, silme, indeksi kalıcı hale getirme ve daha fazlası için bir sorgu arayüzü sağlamak üzere `VectorStoreIndex` ile birlikte kullanılabilir.

**SingleStore**

```python
from llama_index.vector_stores.singlestoredb import SingleStoreVectorStore
import os

# çevre değişkeninde singlestore db url'sini ayarlayabilir
# veya bunu SingleStoreVectorStore kurucusuna bir argüman olarak geçebilirsiniz
os.environ["SINGLESTOREDB_URL"] = "URL_YER_TUTUCUSU"
vector_store = SingleStoreVectorStore(
    table_name="embeddings",
    content_field="content",
    metadata_field="metadata",
    vector_field="vector",
    timeout=30,
)
```

**Tablestore**

```python
import tablestore
from llama_index.vector_stores.tablestore import TablestoreVectorStore

# vektör dışı alanların filtrelenmesini desteklemeyen bir vektör deposu oluştur
simple_vector_store = TablestoreVectorStore(
    endpoint="<uc_nokta>",
    instance_name="<ornek_adi>",
    access_key_id="<id>",
    access_key_secret="<secret>",
    vector_dimension=512,
)

# vektör dışı alanların filtrelenmesini destekleyen bir vektör deposu oluştur
vector_store_with_meta_data = TablestoreVectorStore(
    endpoint="<uc_nokta>",
    instance_name="<ornek_adi>",
    access_key_id="<id>",
    access_key_secret="<secret>",
    vector_dimension=512,
    # isteğe bağlı: vektör dışı alanları filtrelemek için özel meta veri eşlemesi kullanılır.
    metadata_mappings=[
        tablestore.FieldSchema(
            "type",  # vektör dışı alanlar
            tablestore.FieldType.KEYWORD,
            index=True,
            enable_sort_and_agg=True,
        ),
        tablestore.FieldSchema(
            "time",  # vektör dışı alanlar
            tablestore.FieldType.LONG,
            index=True,
            enable_sort_and_agg=True,
        ),
    ],
)
```

**TiDB**

```python
from llama_index.vector_stores.tidbvector import TiDBVectorStore

tidbvec = TiDBVectorStore(
    # bağlantı url formatı
    # - mysql+pymysql://root@34.212.137.91:4000/test
    connection_string="URL_YER_TUTUCUSU",
    table_name="llama_index_vectorstore",
    distance_strategy="cosine",
    vector_dimension=1536,
)
```

**Timescale**

```python
from llama_index.vector_stores.timescalevector import TimescaleVectorStore

vector_store = TimescaleVectorStore.from_params(
    service_url="TIMESCALE SERVIS URL'NIZ",
    table_name="paul_graham_essay",
)
```

**Upstash**

```python
from llama_index.vector_stores.upstash import UpstashVectorStore

vector_store = UpstashVectorStore(url="URL_NIZ", token="BELIRTECINIZ")
```

**VectorX DB**

```python
from vecx_llamaindex import VectorXVectorStore
from llama_index.core import StorageContext
import time

# Çakışmaları önlemek için zaman damgalı benzersiz bir indeks adı oluşturun
timestamp = int(time.time())
index_name = f"llamaindex_demo_{timestamp}"

# Embedding modelini ayarla
embed_model = OpenAIEmbedding()

# Embedding boyutunu al
dimension = 1536  # OpenAI'nin varsayılan embedding boyutu

# VectorX vektör deposunu başlat
vector_store = VectorXVectorStore.from_params(
    api_token=vecx_api_token,
    encryption_key=encryption_key,
    index_name=index_name,
    dimension=dimension,
    space_type="cosine",  # "cosine", "l2" veya "ip" olabilir
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)

query_engine = index.as_query_engine()

# Bir soru sor
response = query_engine.query("Python nedir?")

# Sadece AI ile ilgili dökümanlar içinde arama yapmak için filtreli bir erişici oluşturun
ai_filter = MetadataFilter(
    key="category", value="ai", operator=FilterOperator.EQ
)
ai_filters = MetadataFilters(filters=[ai_filter])

# Filtreli bir sorgu motoru oluşturun
filtered_query_engine = index.as_query_engine(filters=ai_filters)

# Genel bir soru sor ancak sadece AI dökümanlarını kullan
response = filtered_query_engine.query("Veriden öğrenme nedir?")
```

**Vertex AI Vektör Araması**

```python
from llama_index.vector_stores.vertexaivectorsearch import VertexAIVectorStore

vector_store = VertexAIVectorStore(
    project_id="[google-cloud-proje-id-niz]",
    region="[google-cloud-bolgeniz]",
    index_id="[indeks-kaynak-adiniz]",
    endpoint_id="[indeks-uc-nokta-adiniz]",
)
```

**Weaviate**

```python
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore

# bir Weaviate istemcisi oluşturma
resource_owner_config = weaviate.AuthClientPassword(
    username="<kullanici_adi>",
    password="<sifre>",
)
client = weaviate.Client(
    "https://<cluster-id>.semi.network/",
    auth_client_secret=resource_owner_config,
)

# vektör deposunu oluştur
vector_store = WeaviateVectorStore(weaviate_client=client)
```

**Zep**

Zep metinleri, meta verileri ve embedding'leri saklar. Hepsi arama sonuçlarında döndürülür.

```python
from llama_index.vector_stores.zep import ZepVectorStore

vector_store = ZepVectorStore(
    api_url="<api_url>",
    api_key="<api_key>",
    collection_name="<benzersiz_koleksiyon_adi>",  # Mevcut bir koleksiyon veya yeni bir tane olabilir
    embedding_dimensions=1536,  # İsteğe bağlı, yeni bir koleksiyon oluşturulurken gereklidir
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# Hem bir metin sorgusu hem de meta veri filtreleri kullanarak indeksi sorgula
filters = MetadataFilters(
    filters=[ExactMatchFilter(key="theme", value="Mafia")]
)
retriever = index.as_retriever(filters=filters)
result = retriever.retrieve("Inception ne hakkındadır?")
```

**Zilliz**

-   Zilliz Cloud (Milvus'un barındırılan sürümü), bazı ek argümanlarla Milvus İndeksini kullanır.

```python
import pymilvus
from llama_index.vector_stores.milvus import MilvusVectorStore


# vektör deposunu oluştur
vector_store = MilvusVectorStore(
    uri="foo.vectordb.zillizcloud.com",
    token="your_token_here",
    overwrite="True",
)
```

[Örnek not defterleri burada bulunabilir](https://github.com/jerryjliu/llama_index/tree/main/docs/examples/vector_stores).

## Veri Bağlayıcı Kullanarak Vektör Depolarından Veri Yükleme

LlamaIndex çok sayıda kaynaktan veri yüklemeyi destekler. Daha fazla ayrıntı ve API dökümantasyonu için [Veri Bağlayıcılarına](/python/framework/module_guides/loading/connector/modules) bakın.

AlloyDB hem dökümanı hem de vektörleri saklar.
Bu eğitim senkronize (synchronous) arayüzü göstermektedir. Tüm senkronize metotların karşılık gelen asenkronize (asynchronous) metotları vardır.
İşte AlloyDB'nin nasıl kullanılacağına dair bir örnek:

```bash
pip install llama-index
pip install llama-index-alloydb-pg
```

```python
from llama_index.core import SummaryIndex
from llama_index_alloydb_pg import AlloyDBEngine, AlloyDBReader

engine = AlloyDBEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    cluster=CLUSTER,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)
reader = AlloyDBReader.create_sync(
    engine,
    table_name=TABLE_NAME,
)
documents = reader.load_data()

index = SummaryIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("<sorgu_metni>")
display(Markdown(f"<b>{response}</b>"))
```

PostgreSQL için Google Cloud SQL hem dökümanı hem de vektörleri saklar.
Bu eğitim senkronize arayüzü göstermektedir. Tüm senkronize metotların karşılık gelen asenkronize metotları vardır.
İşte PostgreSQL için Cloud SQL'in nasıl kullanılacağına dair bir örnek:

```bash
pip install llama-index
pip install llama-index-cloud-sql-pg
```

```python
from llama_index.core import SummaryIndex
from llama_index_cloud_sql_pg import PostgresEngine, PostgresReader

engine = PostgresEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)
reader = PostgresReader.create_sync(
    engine,
    table_name=TABLE_NAME,
)
documents = reader.load_data()

index = SummaryIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("<sorgu_metni>")
display(Markdown(f"<b>{response}</b>"))
```

Chroma hem dökümanları hem de vektörleri saklar. İşte Chroma'nın nasıl kullanılacağına dair bir örnek:

```python
from llama_index.readers.chroma import ChromaReader
from llama_index.core import SummaryIndex

# Chroma okuyucu, kalıcı hale getirilmiş bir Chroma koleksiyonundan veri yükler.
# Bu, bir koleksiyon adı ve kalıcı bir dizin gerektirir.
reader = ChromaReader(
    collection_name="chroma_collection",
    persist_directory="examples/data_connectors/chroma_collection",
)

query_vector = [n1, n2, n3, ...]

documents = reader.load_data(
    collection_name="demo", query_vector=query_vector, limit=5
)
index = SummaryIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("<sorgu_metni>")
display(Markdown(f"<b>{response}</b>"))
```

Qdrant da hem dökümanları hem de vektörleri saklar. İşte Qdrant'ın nasıl kullanılacağına dair bir örnek:

```python
from llama_index.readers.qdrant import QdrantReader

reader = QdrantReader(host="localhost")

# query_vector, sorgunuzun bir embedding temsilidir
# Örnek query_vector
# query_vector = [0.3, 0.3, 0.3, 0.3, ...]

query_vector = [n1, n2, n3, ...]

# NOT: Gerekli argümanlar collection_name, query_vector'dır.
# Daha fazla ayrıntı için Python istemcisine bakın: https://github.com/qdrant/qdrant_client

documents = reader.load_data(
    collection_name="demo", query_vector=query_vector, limit=5
)
```

NOT: Weaviate, döküman ve vektör nesnelerinin hibrit bir yapısını saklayabildiğinden, kullanıcı dökümanları sorgulamak için ya açıkça `class_name` ve `properties` belirtmeyi seçebilir ya da ham bir GraphQL sorgusu belirtmeyi seçebilir. Kullanım için aşağıya bakın.

```python
# seçenek 1: class_name ve properties belirtin

# 1) class_name ve properties kullanarak veri yükle
documents = reader.load_data(
    class_name="<class_name>",
    properties=["property1", "property2", "..."],
    separate_documents=True,
)

# 2) örnek GraphQL sorgusu
query = """
{
    Get {
        <class_name> {
            <property1>
            <property2>
        }
    }
}
"""

documents = reader.load_data(graphql_query=query, separate_documents=True)
```

NOT: Hem Pinecone hem de Faiss veri yükleyicileri, ilgili veri kaynaklarının yalnızca vektörleri sakladığını; metin içeriğinin başka bir yerde saklandığını varsayar. Bu nedenle her iki veri yükleyici de kullanıcının `load_data` çağrısında bir `id_to_text_map` belirtmesini gerektirir.

Örneğin, Pinecone veri yükleyicisi `PineconeReader`'ın örnek kullanımı şöyledir:

```python
from llama_index.readers.pinecone import PineconeReader

reader = PineconeReader(api_key=api_key, environment="us-west1-gcp")

id_to_text_map = {
    "id1": "metin bloğu 1",
    "id2": "metin bloğu 2",
}

query_vector = [n1, n2, n3, ...]

documents = reader.load_data(
    index_name="quickstart",
    id_to_text_map=id_to_text_map,
    top_k=3,
    vector=query_vector,
    separate_documents=True,
)
```

[Örnek not defterleri burada bulunabilir](https://github.com/jerryjliu/llama_index/tree/main/docs/examples/data_connectors).

## Vektör Deposu Örnekleri

-   [Alibaba Cloud OpenSearch](/python/examples/vector_stores/alibabacloudopensearchindexdemo)
-   [Amazon Neptune - Neptune Analytics](/python/examples/vector_stores/amazonneptunevectordemo)
-   [Astra DB](/python/examples/vector_stores/astradbindexdemo)
-   [Asenkron İndeks Oluşturma (Async Index Creation)](/python/examples/vector_stores/asyncindexcreationdemo)
-   [Azure AI Search](/python/examples/vector_stores/azureaisearchindexdemo)
-   [Azure Cosmos DB](/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo)
-   [Cassandra](/python/examples/vector_stores/cassandraindexdemo)
-   [Chromadb](/python/examples/vector_stores/chromaindexdemo)
-   [Couchbase](/python/examples/vector_stores/couchbasevectorstoredemo)
-   [Dash](/python/examples/vector_stores/dashvectorindexdemo)
-   [Deeplake](/python/examples/vector_stores/deeplakeindexdemo)
-   [DocArray HNSW](/python/examples/vector_stores/docarrayhnswindexdemo)
-   [DocArray Bellek İçi (in-Memory)](/python/examples/vector_stores/docarrayinmemoryindexdemo)
-   [Espilla](/python/examples/vector_stores/epsillaindexdemo)
-   [PostgreSQL için Google AlloyDB](/python/examples/vector_stores/alloydbvectorstoredemo)
-   [PostgreSQL için Google Cloud SQL](/python/examples/vector_stores/cloudsqlpgvectorstoredemo)
-   [LanceDB](/python/examples/vector_stores/lancedbindexdemo)
-   [Lantern](/python/examples/vector_stores/lanternindexdemo)
-   [Milvus](/python/examples/vector_stores/milvusindexdemo)
-   [Milvus Asenkron API](/python/examples/vector_stores/milvusasyncapidemo)
-   [Milvus Tam Metin Araması (Full-Text Search)](/python/examples/vector_stores/milvusfulltextsearchdemo)
-   [Milvus Hibrit Arama (Hybrid Search)](/python/examples/vector_stores/milvushybridindexdemo)
-   [MyScale](/python/examples/vector_stores/myscaleindexdemo)
-   [Elasticsearch](/python/examples/vector_stores/elasticsearchindexdemo)
-   [FAISS](/python/examples/vector_stores/faissindexdemo)
-   [MongoDB Atlas](/python/examples/vector_stores/mongodbatlasvectorsearch)
-   [Neo4j](/python/examples/vector_stores/neo4jvectordemo)
-   [OpenSearch](/python/examples/vector_stores/opensearchdemo)
-   [Pinecone](/python/examples/vector_stores/pineconeindexdemo)
-   [Pinecone Hibrit Arama (Hybrid Search)](/python/examples/vector_stores/pineconeindexdemo-hybrid)
-   [PGvectoRS](/python/examples/vector_stores/pgvectorsdemo)
-   [Postgres](/python/examples/vector_stores/postgres)
-   [Redis](/python/examples/vector_stores/redisindexdemo)
-   [Qdrant](/python/examples/vector_stores/qdrantindexdemo)
-   [Qdrant Hibrit Arama (Hybrid Search)](/python/examples/vector_stores/qdrant_hybrid)
-   [Rockset](/python/examples/vector_stores/rocksetindexdemo)
-   [Simple](/python/examples/vector_stores/simpleindexdemo)
-   [Supabase](/python/examples/vector_stores/supabasevectorindexdemo)
-   [Tablestore](/python/examples/vector_stores/tablestoredemo)
-   [Tair](/python/examples/vector_stores/tairindexdemo)
-   [Tencent](/python/examples/vector_stores/tencentvectordbindexdemo)
-   [Timescale](/python/examples/vector_stores/timescalevector)
-   [Upstash](/python/examples/vector_stores/upstashvectordemo)
-   [VectorX DB](/python/examples/vector_stores/vectorxdbdemo)
-   [Weaviate](/python/examples/vector_stores/weaviateindexdemo)
-   [Weaviate Hibrit Arama (Hybrid Search)](/python/examples/vector_stores/weaviateindexdemo-hybrid)
-   [WordLift](/python/examples/vector_stores/wordliftdemo)
-   [Zep](/python/examples/vector_stores/zepindexdemo)