---
title: Databricks Vektör Araması (Vector Search)
 | LlamaIndex OSS Belgeleri
---

# Databricks Vektör Araması

Databricks Vektör Araması, Databricks Zeka Platformu'na (Databricks Intelligence Platform) yerleşik olan ve yönetişim ile üretkenlik araçlarıyla entegre edilmiş bir vektör veritabanıdır. Belgelerin tamamına buradan ulaşabilirsiniz: <https://docs.databricks.com/en/generative-ai/vector-search.html>

`llama-index` ve `databricks-vectorsearch` paketlerini kurun. Vektör Araması python istemcisini kullanmak için bir Databricks çalışma zamanı (runtime) içinde olmanız gerekir.

```bash
%pip install llama-index llama-index-vector-stores-databricks
%pip install databricks-vectorsearch
```

Databricks bağımlılıklarını içe aktarın

```python
from databricks.vector_search.client import (
    VectorSearchIndex,
    VectorSearchClient,
)
```

LlamaIndex bağımlılıklarını içe aktarın

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
)
from llama_index.vector_stores.databricks import DatabricksVectorSearch
```

Örnek veriyi yükleyin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

Veriyi okuyun

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge sayısı: {len(documents)}")
print(f"İlk belge, kimlik: {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    "İlk belge, metin"
    f" ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

İndekse hizmet edecek bir Databricks Vektör Araması uç noktası (endpoint) oluşturun

```python
# Bir vektör arama uç noktası oluşturun
client = VectorSearchClient()
client.create_endpoint(
    name="llamaindex_dbx_vector_store_test_endpoint", endpoint_type="STANDARD"
)
```

Databricks Vektör Araması indeksini oluşturun ve belgelerden inşa edin

```python
# Bir vektör arama indeksi oluşturun
# Unity Catalog etkinleştirilmiş bir şema içine yerleştirilmelidir


# Databricks tarafından yönetilen bir indeks yerine, kendi kendine yönetilen gömmeleri 
# (yani LlamaIndex tarafından yönetilenleri) kullanacağız
databricks_index = client.create_direct_access_index(
    endpoint_name="llamaindex_dbx_vector_store_test_endpoint",
    index_name="benim_kataloğum.benim_şemam.benim_test_tablom",
    primary_key="benim_birincil_anahtarım",
    embedding_dimension=1536,  # kullanacağınız gömme modelinin boyutuyla eşleşmelidir
    embedding_vector_column="benim_gömme_vektör_sütunum",  # buna istediğiniz adı verebilirsiniz - LlamaIndex sınıfı tarafından algılanacaktır
    schema={
        "benim_birincil_anahtarım": "string",
        "benim_gömme_vektör_sütunum": "array<double>",
        "text": "string",  # bir sütun, aşağıda oluşturulan DatabricksVectorSearch örneğindeki text_column ile eşleşmelidir; bu ham düğüm metnini tutacaktır,
        "doc_id": "string",  # bir sütun, referans belge kimliğini içermelidir (bu LlamaIndex tarafından otomatik olarak doldurulacaktır)
        # düğümlerinizde olabilecek diğer meta verileri ekleyin (Databricks Vektör Araması meta veri filtrelemeyi destekler)
        # BU ALANLARIN META VERİ FİLTRELEME İÇİN KULLANILABİLMESİ İÇİN AÇIKÇA EKLENMESİ GEREKTİĞİNİ UNUTMAYIN
    },
)


databricks_vector_store = DatabricksVectorSearch(
    index=databricks_index,
    text_column="text",
    columns=None,  # META VERİ ALAN ADLARINIZI BURAYA DA KAYDETMELİSİNİZ
)  # Kendi kendine yönetilen gömmeler için text_column gereklidir
storage_context = StorageContext.from_defaults(
    vector_store=databricks_vector_store
)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

İndeksi sorgulayın

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden yapay zeka (AI) üzerine çalışmayı seçti?")


print(response.response)
```
