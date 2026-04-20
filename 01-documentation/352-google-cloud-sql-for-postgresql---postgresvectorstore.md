---
title: Google Cloud SQL for PostgreSQL - `PostgresVectorStore`
 | LlamaIndex OSS Belgeleri
---

> [Cloud SQL](https://cloud.google.com/sql), yüksek performans, sorunsuz entegrasyon ve etkileyici ölçeklenebilirlik sunan, tamamen yönetilen bir ilişkisel veritabanı servisidir. MySQL, PostgreSQL ve SQL Server veritabanı motorlarını sunar. Cloud SQL'in LlamaIndex entegrasyonlarından yararlanarak yapay zeka destekli deneyimler oluşturmak için veritabanı uygulamanızı genişletin.

Bu not defteri, vektör gömmelerini (vector embeddings) `PostgresVectorStore` sınıfı ile saklamak için `Cloud SQL for PostgreSQL`'in nasıl kullanılacağını göstermektedir.

Paket hakkında daha fazla bilgiyi [GitHub](https://github.com/googleapis/llama-index-cloud-sql-pg-python/) üzerinden edinebilirsiniz.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googleapis/llama-index-cloud-sql-pg-python/blob/main/samples/llama_index_vector_store.ipynb)

## Başlamadan Önce

Bu not defterini çalıştırmak için aşağıdakileri yapmanız gerekecektir:

- [Bir Google Cloud Projesi Oluşturun](https://developers.google.com/workspace/guides/create-project)
- [Cloud SQL Admin API'sini Etkinleştirin.](https://console.cloud.google.com/flows/enableapi?apiid=sqladmin.googleapis.com)
- [Bir Cloud SQL örneği (instance) oluşturun.](https://cloud.google.com/sql/docs/postgres/connect-instance-auth-proxy#create-instance)
- [Bir Cloud SQL veritabanı oluşturun.](https://cloud.google.com/sql/docs/postgres/create-manage-databases)
- [Veritabanına bir Kullanıcı ekleyin.](https://cloud.google.com/sql/docs/postgres/create-manage-users)

### 🦙 Kütüphane Kurulumu

Entegrasyon kütüphanesi olan `llama-index-cloud-sql-pg`'yi ve gömme servisi için gerekli olan `llama-index-embeddings-vertex` kütüphanesini kurun.

```bash
%pip install --upgrade --quiet llama-index-cloud-sql-pg llama-index-embeddings-vertex llama-index-llms-vertex llama-index
```

**Sadece Colab:** Çekirdeği (kernel) yeniden başlatmak için aşağıdaki hücrenin yorumunu kaldırın veya düğmeyi kullanın. Vertex AI Workbench için üstteki düğmeyi kullanarak terminali yeniden başlatabilirsiniz.

```python
# # Kurulumlardan sonra ortamınızın yeni paketlere erişebilmesi için çekirdeği otomatik olarak yeniden başlatın
# import IPython


# app = IPython.Application.instance()
# app.kernel.do_shutdown(True)
```

### 🔐 Kimlik Doğrulama (Authentication)

Google Cloud Projenize erişmek için bu not defterinde oturum açmış IAM kullanıcısı olarak Google Cloud'da kimlik doğrulaması yapın.

- Bu not defterini çalıştırmak için Colab kullanıyorsanız, aşağıdaki hücreyi kullanın ve devam edin.
- Vertex AI Workbench kullanıyorsanız, [buradaki](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env) kurulum talimatlarına göz atın.

```python
from google.colab import auth


auth.authenticate_user()
```

### ☁ Google Cloud Projenizi Ayarlayın

Bu not defteri içinde Google Cloud kaynaklarından yararlanabilmeniz için Google Cloud projenizi ayarlayın.

Proje kimliğinizi (project ID) bilmiyorsanız aşağıdakileri deneyebilirsiniz:

- `gcloud config list` komutunu çalıştırın.
- `gcloud projects list` komutunu çalıştırın.
- Destek sayfasına bakın: [Proje kimliğini bulma](https://support.google.com/googleapi/answer/7014113).

```python
# @markdown Lütfen aşağıdaki değeri Google Cloud proje kimliğinizle doldurun ve ardından hücreyi çalıştırın.


PROJECT_ID = "my-project-id"  # @param {type:"string"}


# Proje kimliğini ayarla
!gcloud config set project {PROJECT_ID}
```

## Temel Kullanım

### Cloud SQL veritabanı değerlerini ayarlayın

Veritabanı değerlerinizi [Cloud SQL Örnekleri sayfasında](https://console.cloud.google.com/sql?_ga=2.223735448.2062268965.1707700487-2088871159.1707257687) bulun.

```python
# @title Değerlerinizi Buraya Girin { display-mode: "form" }
REGION = "us-central1"  # @param {type: "string"}
INSTANCE = "my-primary"  # @param {type: "string"}
DATABASE = "my-database"  # @param {type: "string"}
TABLE_NAME = "vector_store"  # @param {type: "string"}
USER = "postgres"  # @param {type: "string"}
PASSWORD = "my-password"  # @param {type: "string"}
```

### PostgresEngine Bağlantı Havuzu (Connection Pool)

Cloud SQL'i bir vektör deposu olarak kurmak için gereken gereksinimlerden ve bağımsız değişkenlerden biri `PostgresEngine` nesnesidir. `PostgresEngine`, Cloud SQL veritabanınıza bir bağlantı havuzu yapılandırarak uygulamanızdan başarılı bağlantılar kurulmasını sağlar ve endüstri en iyi uygulamalarını takip eder.

`PostgresEngine.from_instance()` kullanarak bir `PostgresEngine` oluşturmak için yalnızca 4 şeye ihtiyacınız vardır:

1. `project_id` : Cloud SQL örneğinin bulunduğu Google Cloud Projesinin Proje Kimliği.
2. `region` : Cloud SQL örneğinin bulunduğu bölge (region).
3. `instance` : Cloud SQL örneğinin adı.
4. `database` : Cloud SQL örneğinde bağlanılacak veritabanının adı.

Varsayılan olarak, veritabanı kimlik doğrulama yöntemi olarak [IAM veritabanı kimlik doğrulaması](https://cloud.google.com/sql/docs/postgres/iam-authentication#iam-db-auth) kullanılacaktır. Bu kütüphane, ortamdan alınan [Uygulama Varsayılan Kimlik Bilgilerine (ADC)](https://cloud.google.com/docs/authentication/application-default-credentials) ait IAM asıl kişisini (principal) kullanır.

IAM veritabanı kimlik doğrulaması hakkında daha fazla bilgi için lütfen şuna bakın:

- [IAM veritabanı kimlik doğrulaması için bir örnek yapılandırma](https://cloud.google.com/sql/docs/postgres/create-edit-iam-instances)
- [IAM veritabanı kimlik doğrulaması ile kullanıcıları yönetme](https://cloud.google.com/sql/docs/postgres/add-manage-iam-users)

İsteğe bağlı olarak, Cloud SQL veritabanına erişmek için kullanıcı adı ve parolanın kullanıldığı [yerleşik veritabanı kimlik doğrulaması](https://cloud.google.com/sql/docs/postgres/built-in-authentication) da kullanılabilir. `PostgresEngine.from_instance()` metoduna isteğe bağlı `user` ve `password` bağımsız değişkenlerini sağlamanız yeterlidir:

- `user` : Yerleşik veritabanı kimlik doğrulaması ve oturum açma için kullanılacak veritabanı kullanıcısı.
- `password` : Yerleşik veritabanı kimlik doğrulaması ve oturum açma için kullanılacak veritabanı parolası.

**Not:** Bu öğretici asenkron (async) arayüzü göstermektedir. Tüm asenkron metodların karşılık gelen senkron (sync) metodları vardır.

```python
from llama_index_cloud_sql_pg import PostgresEngine


engine = await PostgresEngine.afrom_instance(
    project_id=PROJECT_ID,
    region=REGION,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)
```

### Bir Tablo Başlatın (Initialize)

`PostgresVectorStore` sınıfı bir veritabanı tablosu gerektirir. `PostgresEngine` motoru, sizin yerinize uygun şemaya sahip bir tablo oluşturmak için kullanılabilecek `init_vector_store_table()` yardımcı metoduna sahiptir.

```python
await engine.ainit_vector_store_table(
    table_name=TABLE_NAME,
    vector_size=768,  # VertexAI modeli (textembedding-gecko@latest) için vektör boyutu
)
```

#### İsteğe Bağlı İpucu: 💡

`table_name` değerini ilettiğiniz her yerde `schema_name` değerini de ileterek bir şema adı belirtebilirsiniz.

```python
SCHEMA_NAME = "my_schema"


await engine.ainit_vector_store_table(
    table_name=TABLE_NAME,
    schema_name=SCHEMA_NAME,
    vector_size=768,
)
```

### Gömme (Embedding) Sınıfı Örneği Oluşturun

Herhangi bir [Llama Index gömme modelini](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/) kullanabilirsiniz. `VertexTextEmbeddings` kullanmak için Vertex AI API'sini etkinleştirmeniz gerekebilir. Üretim ortamı için gömme modelinin sürümünü ayarlamanızı öneririz; [Metin gömme modelleri](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings) hakkında daha fazla bilgi edinebilirsiniz.

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

### Varsayılan bir PostgresVectorStore Başlatın

```python
from llama_index_cloud_sql_pg import PostgresVectorStore


vector_store = await PostgresVectorStore.create(
    engine=engine,
    table_name=TABLE_NAME,
    # schema_name=SCHEMA_NAME
)
```

### Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükle (Load Documents)

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

## VectorStoreIndex ile Kullanım

[`VectorStoreIndex`](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/) kullanarak vektör deposundan bir indeks oluşturun.

#### Belgelerle Vektör Deposunu Başlatın

Bir Vektör Deposunu kullanmanın en basit yolu, bir dizi belgeyi yüklemek ve `from_documents` kullanarak bunlardan bir indeks oluşturmaktır.

```python
from llama_index.core import StorageContext, VectorStoreIndex


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
```

### İndeksi Sorgula

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar ne yaptı?")
print(response)
```

## Özel bir Vektör Deposu Oluşturma (Custom Vector Store)

Bir Vektör Deposu, benzerlik aramalarını filtrelemek için ilişkisel verilerden yararlanabilir.

Özel meta veri sütunları olan yeni bir tablo oluşturun. Bir Belgenin kimliği (id), içeriği, gömmesi ve/veya meta verileri için zaten özel sütunlara sahip olan mevcut bir tabloyu da yeniden kullanabilirsiniz.

```python
from llama_index_cloud_sql_pg import Column


# Tablo adını ayarla
TABLE_NAME = "vectorstore_custom"
# SCHEMA_NAME = "my_schema"


await engine.ainit_vector_store_table(
    table_name=TABLE_NAME,
    # schema_name=SCHEMA_NAME,
    vector_size=768,  # VertexAI modeli: textembedding-gecko@003
    metadata_columns=[Column("len", "INTEGER")],
)




# PostgresVectorStore'u Başlat
custom_store = await PostgresVectorStore.create(
    engine=engine,
    table_name=TABLE_NAME,
    # schema_name=SCHEMA_NAME,
    metadata_columns=["len"],
)
```

### Meta veri ile belgeleri ekleyin

Belge [`metadata`](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_documents/) (meta verileri), LLM'ye ve erişim sürecine daha fazla bilgi sağlayabilir. [Meta veri çıkarma ve ekleme](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_metadata_extractor/) için farklı yaklaşımlar hakkında daha fazla bilgi edinebilirsiniz.

```python
from llama_index.core import Document


fruits = ["elma (apple)", "armut (pear)", "portakal (orange)", "çilek (strawberry)", "muz (banana)", "kivi (kiwi)"]
documents = [
    Document(text=fruit, metadata={"len": len(fruit)}) for fruit in fruits
]


storage_context = StorageContext.from_defaults(vector_store=custom_store)
custom_doc_index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
```

### Meta veri filtresi ile belgeleri arayın

`filters` bağımsız değişkenini belirterek arama sonuçlarına ön filtreleme uygulayabilirsiniz.

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

## Bir İndeks Ekle (Add a Index)

Vektör indeksi uygulayarak vektör arama sorgularını hızlandırın. [Vektör indeksleri](https://cloud.google.com/blog/products/databases/faster-similarity-search-performance-with-pgvector-indexes) hakkında daha fazla bilgi edinebilirsiniz.

```python
from llama_index_cloud_sql_pg.indexes import IVFFlatIndex


index = IVFFlatIndex()
await vector_store.aapply_vector_index(index)
```

### Yeniden İndeksleme (Re-index)

```python
await vector_store.areindex()  # Varsayılan indeks adını kullanarak yeniden indeksle
```

### Bir İndeksi Kaldır

```python
await vector_store.adrop_vector_index()  # Varsayılan adı kullanarak indeksi sil
```
