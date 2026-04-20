# Google AlloyDB for PostgreSQL - `AlloyDBVectorStore`

---
title: Google AlloyDB for PostgreSQL - `AlloyDBVectorStore`
 | LlamaIndex OSS Belgeleri
---

> [AlloyDB](https://cloud.google.com/alloydb), yüksek performans, sorunsuz entegrasyon ve etkileyici ölçeklenebilirlik sunan, tam olarak yönetilen bir ilişkisel veritabanı hizmetidir. AlloyDB, PostgreSQL ile %100 uyumludur. AlloyDB'nin LlamaIndex entegrasyonlarından yararlanarak yapay zeka destekli deneyimler oluşturmak için veritabanı uygulamanızı genişletin.

Bu not defteri, vektör gömmelerini (vector embeddings) `AlloyDBVectorStore` sınıfı ile saklamak için `AlloyDB for PostgreSQL`ün nasıl kullanılacağını kapsar.

Paket hakkında daha fazla bilgiyi [GitHub](https://github.com/googleapis/llama-index-alloydb-pg-python/) üzerinden edinebilirsiniz.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googleapis/llama-index-alloydb-pg-python/blob/main/samples/llama_index_vector_store.ipynb)

## Başlamadan önce (Before you begin)

Bu not defterini çalıştırmak için aşağıdakileri yapmanız gerekecektir:

- [Bir Google Cloud Projesi oluşturun](https://developers.google.com/workspace/guides/create-project)
- [AlloyDB API'sini etkinleştirin](https://console.cloud.google.com/flows/enableapi?apiid=alloydb.googleapis.com)
- [Bir AlloyDB kümesi (cluster) ve örneği (instance) oluşturun.](https://cloud.google.com/alloydb/docs/cluster-create)
- [Bir AlloyDB veritabanı oluşturun.](https://cloud.google.com/alloydb/docs/quickstart/create-and-connect)
- [Veritabanına bir Kullanıcı ekleyin.](https://cloud.google.com/alloydb/docs/database-users/about)

### 🦙 Kütüphane Kurulumu (Library Installation)

Entegrasyon kütüphanesi olan `llama-index-alloydb-pg`yi ve gömme hizmeti kütüphanesi olan `llama-index-embeddings-vertex`i kurun.

```bash
%pip install --upgrade --quiet llama-index-alloydb-pg llama-index-embeddings-vertex llama-index-llms-vertex llama-index
```

**Yalnızca Colab:** Çalışma zamanını (kernel) yeniden başlatmak için aşağıdaki hücrenin yorumunu kaldırın veya düğmeyi kullanın. Vertex AI Workbench için üstteki düğmeyi kullanarak terminali yeniden başlatabilirsiniz.

```python
# # Ortamınızın yeni paketlere erişebilmesi için kurulumlardan sonra çalışma zamanını otomatik olarak yeniden başlatın
# import IPython


# app = IPython.Application.instance()
# app.kernel.do_shutdown(True)
```

### 🔐 Kimlik Doğrulama (Authentication)

Google Cloud Projenize erişmek için bu not defterinde oturum açmış IAM kullanıcısı olarak Google Cloud'da kimlik doğrulaması yapın.

- Bu not defterini çalıştırmak için Colab kullanıyorsanız, aşağıdaki hücreyi kullanın ve devam edin.
- Vertex AI Workbench kullanıyorsanız, kurulum talimatlarına [buradan](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env) göz atın.

```python
from google.colab import auth


auth.authenticate_user()
```

### ☁ Google Cloud Projenizi Ayarlayın (Set Your Google Cloud Project)

Bu not defteri içinde Google Cloud kaynaklarından yararlanabilmek için Google Cloud projenizi ayarlayın.

Proje kimliğinizi (project ID) bilmiyorsanız aşağıdakileri deneyin:

- `gcloud config list` komutunu çalıştırın.
- `gcloud projects list` komutunu çalıştırın.
- Destek sayfasına bakın: [Proje kimliğini bulma](https://support.google.com/googleapi/answer/7014113).

```python
# @markdown Lütfen aşağıdaki değeri Google Cloud proje kimliğinizle doldurun ve ardından hücreyi çalıştırın.


PROJECT_ID = "proje-kimliginiz"  # @param {type:"string"}


# Proje kimliğini ayarla
!gcloud config set project {PROJECT_ID}
```

## Temel Kullanım (Basic Usage)

### AlloyDB veritabanı değerlerini ayarlayın

Veritabanı değerlerinizi [AlloyDB Örnekleri sayfasında](https://console.cloud.google.com/alloydb/clusters) bulabilirsiniz.

```python
# @title Değerlerinizi Buraya Girin { display-mode: "form" }
REGION = "us-central1"  # @param {type: "string"}
CLUSTER = "benim-kumem"  # @param {type: "string"}
INSTANCE = "benim-orneğim"  # @param {type: "string"}
DATABASE = "benim-veritabanim"  # @param {type: "string"}
TABLE_NAME = "vector_store"  # @param {type: "string"}
USER = "postgres"  # @param {type: "string"}
PASSWORD = "benim-sifrem"  # @param {type: "string"}
```

### AlloyDBEngine Bağlantı Havuzu (AlloyDBEngine Connection Pool)

AlloyDB'yi bir vektör deposu olarak kurmak için gerekenlerden ve argümanlardan biri bir `AlloyDBEngine` nesnesidir. `AlloyDBEngine`, AlloyDB veritabanınıza bir bağlantı havuzu (connection pool) yapılandırarak uygulamanızdan başarılı bağlantılar kurulmasını sağlar ve sektördeki en iyi uygulamaları takip eder.

`AlloyDBEngine.from_instance()` kullanarak bir `AlloyDBEngine` oluşturmak için yalnızca 5 şey sağlamanız gerekir:

1. `project_id`: AlloyDB örneğinin bulunduğu Google Cloud Projesinin proje kimliği.
2. `region`: AlloyDB örneğinin bulunduğu bölge (region).
3. `cluster`: AlloyDB kümesinin adı.
4. `instance`: AlloyDB örneğinin adı.
5. `database`: AlloyDB örneğinde bağlanılacak veritabanının adı.

Varsayılan olarak, veritabanı kimlik doğrulama yöntemi olarak [IAM veritabanı kimlik doğrulaması](https://cloud.google.com/alloydb/docs/connect-iam) kullanılacaktır. Bu kütüphane, ortamdan temin edilen [Uygulama Varsayılan Kimlik Bilgilerine (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials) ait IAM asıl kişisini (principal) kullanır.

İsteğe bağlı olarak, AlloyDB veritabanına erişmek için kullanıcı adı ve şifre kullanan [yerleşik veritabanı kimlik doğrulaması](https://cloud.google.com/alloydb/docs/database-users/about) da kullanılabilir. `AlloyDBEngine.from_instance()` metoduna isteğe bağlı `user` ve `password` argümanlarını sağlamanız yeterlidir:

- `user`: Yerleşik veritabanı kimlik doğrulaması ve oturum açma için kullanılacak veritabanı kullanıcısı.
- `password`: Yerleşik veritabanı kimlik doğrulaması ve oturum açma için kullanılacak veritabanı şifresi.

**Not:** Bu eğitim asenkron (async) arayüzü göstermektedir. Tüm asenkron metotların karşılık gelen senkron (sync) metotları vardır.

```python
from llama_index_alloydb_pg import AlloyDBEngine


engine = await AlloyDBEngine.afrom_instance(
    project_id=PROJECT_ID,
    region=REGION,
    cluster=CLUSTER,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)
```

### AlloyDB Omni için AlloyDBEngine

AlloyDB Omni için bir `AlloyDBEngine` oluşturmak üzere bir bağlantı URL'sine ihtiyacınız olacaktır. `AlloyDBEngine.from_connection_string` önce asenkron bir motor oluşturur ve ardından bunu bir `AlloyDBEngine`e dönüştürür. İşte `asyncpg` sürücüsü ile bir örnek bağlantı:

```python
# Kendi AlloyDB Omni bilgilerinizle değiştirin
OMNI_USER = "benim-omni-kullanicim"
OMNI_PASSWORD = ""
OMNI_HOST = "127.0.0.1"
OMNI_PORT = "5432"
OMNI_DATABASE = "benim-omni-db"


connstring = f"postgresql+asyncpg://{OMNI_USER}:{OMNI_PASSWORD}@{OMNI_HOST}:{OMNI_PORT}/{OMNI_DATABASE}"
engine = AlloyDBEngine.from_connection_string(connstring)
```

### Bir tabloyu başlatma (Initialize a table)

`AlloyDBVectorStore` sınıfı bir veritabanı tablosu gerektirir. `AlloyDBEngine` motoru, sizin için uygun şemaya sahip bir tablo oluşturmak üzere kullanılabilecek `init_vector_store_table()` yardımcı metoduna sahiptir.

```python
await engine.ainit_vector_store_table(
    table_name=TABLE_NAME,
    vector_size=768,  # VertexAI modeli (textembedding-gecko@latest) için vektör boyutu
)
```

#### İsteğe Bağlı İpucu: 💡

`table_name`i ilettiğiniz her yerde `schema_name`i de ileterek bir şema adı belirtebilirsiniz.

```python
SCHEMA_NAME = "benim_semam"


await engine.ainit_vector_store_table(
    table_name=TABLE_NAME,
    schema_name=SCHEMA_NAME,
    vector_size=768,
)
```

### Bir gömme (embedding) sınıf örneği oluşturun

Herhangi bir [Llama Index gömme modelini](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/) kullanabilirsiniz. `VertexTextEmbeddings`i kullanmak için Vertex AI API'sini etkinleştirmeniz gerekebilir. Üretim (production) için gömme modelinin sürümünü ayarlamanızı öneririz; [Metin gömme modelleri](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings) hakkında daha fazla bilgi edinin.

```bash
# Vertex AI API'sini etkinleştir
!gcloud services enable aiplatform.googleapis.com
```

```python
from llama_index.core import Settings
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex
import google.auth


credentials, project_id = google.auth.default()
Settings.embed_model = VertexTextEmbedding(
    model_name="textembedding-gecko@003",
    project=PROJECT_ID,
    credentials=credentials,
)


Settings.llm = Vertex(model="gemini-1.5-flash-002", project=PROJECT_ID)
```

### Varsayılan bir AlloyDBVectorStore başlatın

```python
from llama_index_alloydb_pg import AlloyDBVectorStore


vector_store = await AlloyDBVectorStore.create(
    engine=engine,
    table_name=TABLE_NAME,
    # schema_name=SCHEMA_NAME
)
```

### Veriyi indir (Download data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri yükle (Load documents)

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

## VectorStoreIndex ile Kullanım (Use with VectorStoreIndex)

[`VectorStoreIndex`](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/) kullanarak vektör deposundan bir indeks oluşturun.

#### Vektör Deposunu belgelerle başlatın

Bir Vektör Deposunu kullanmanın en basit yolu, bir dizi belgeyi yüklemek ve `from_documents` kullanarak bunlardan bir indeks oluşturmaktır.

```python
from llama_index.core import StorageContext, VectorStoreIndex


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
```

### İndeksi sorgulayın (Query the index)

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar ne yaptı?")
print(response)
```

## Özel bir Vektör Deposu Oluşturma (Create a custom Vector Store)

Bir Vektör Deposu, benzerlik aramalarını filtrelemek için ilişkisel verilerden yararlanabilir.

Özel metaveri sütunlarına sahip yeni bir tablo oluşturun. Bir Belgenin kimliği (id), içeriği (content), gömmesi (embedding) ve/veya metaverisi (metadata) için halihazırda özel sütunlara sahip olan mevcut bir tabloyu da yeniden kullanabilirsiniz.

```python
from llama_index_alloydb_pg import Column


# Tablo adını ayarla
TABLE_NAME = "vectorstore_custom"
# SCHEMA_NAME = "benim_semam"


await engine.ainit_vector_store_table(
    table_name=TABLE_NAME,
    # schema_name=SCHEMA_NAME,
    vector_size=768,  # VertexAI modeli: textembedding-gecko@003
    metadata_columns=[Column("len", "INTEGER")],
)




# AlloyDBVectorStore'u başlat
custom_store = await AlloyDBVectorStore.create(
    engine=engine,
    table_name=TABLE_NAME,
    # schema_name=SCHEMA_NAME,
    metadata_columns=["len"],
)
```

### Metaverili belgeler ekleyin (Add documents with metadata)

[Belge `metadata`sı (metaverisi)](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_documents/), LLM'e ve erişim sürecine daha fazla bilgi sağlayabilir. [Metaveri çıkarma ve ekleme](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_metadata_extractor/) için farklı yaklaşımlar hakkında daha fazla bilgi edinin.

```python
from llama_index.core import Document


fruits = ["elma", "armut", "portakal", "çilek", "muz", "kivi"]
documents = [
    Document(text=fruit, metadata={"len": len(fruit)}) for fruit in fruits
]


storage_context = StorageContext.from_defaults(vector_store=custom_store)
custom_doc_index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
```

### Metaveri filtresi ile belgeleri arayın (Search for documents with metadata filter)

Bir `filters` argümanı belirterek arama sonuçlarına ön filtreleme uygulayabilirsiniz.

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)


filters = MetadataFilters(
    filters=[
        MetadataFilter(key="len", operator=FilterOperator.GT, value="5"),
    ],
)


query_engine = custom_doc_index.as_query_engine(filters=filters)
res = query_engine.query("Bazı meyveleri listele")
print(str(res.source_nodes[0].text))
```

## Dizin (Index) Ekleme (Add a Index)

Bir vektör dizini (vector index) uygulayarak vektör arama sorgularını hızlandırın. [Vektör dizinleri](https://cloud.google.com/blog/products/databases/faster-similarity-search-performance-with-pgvector-indexes) hakkında daha fazla bilgi edinin.

```python
from llama_index_alloydb_pg.indexes import IVFFlatIndex


index = IVFFlatIndex()
await vector_store.aapply_vector_index(index)
```

`ScaNN` dizini oluşturma (yalnızca AlloyDB Omni'de mevcuttur), yeterli bakım çalışma belleği (maintenance work memory) gerektirir. Dizini uygulamadan önce `set_maintenance_work_mem` fonksiyonunu çağırarak `maintenance_work_mem` veritabanı bayrağını ayarlamanız gerekir.

```python
from llama_index_alloydb_pg.indexes import ScaNNIndex


VECTOR_SIZE = 768  # Gömme modelinizin vektör boyutuyla değiştirin
index = ScaNNIndex(name="benim_scann_dizinim")
await vector_store.aset_maintenance_work_mem(index.num_leaves, VECTOR_SIZE)
await vector_store.aapply_vector_index(index)
```

### Yeniden dizinleme (Re-index)

```python
await vector_store.areindex()  # Varsayılan dizin adını kullanarak yeniden dizinle
```

### Bir dizini kaldırın (Remove an index)

```python
await vector_store.adrop_vector_index()  # Varsayılan adı kullanarak dizini sil
```
