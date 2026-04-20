# AnalyticDB

---
title: AnalyticDB
 | LlamaIndex OSS Belgeleri
---

> [AnalyticDB for PostgreSQL](https://www.alibabacloud.com/help/en/analyticdb-for-postgresql/product-overview/overview-product-overview), büyük hacimli verileri çevrimiçi olarak analiz etmek için tasarlanmış, büyük ölçüde paralel işlemeli (MPP) bir veri ambarı hizmetidir.

Bu not defterini çalıştırmak için bulutta çalışan bir AnalyticDB for PostgreSQL örneğine (instance) ihtiyacınız vardır (bir tane [common-buy.aliyun.com](https://common-buy.aliyun.com/?commodityCode=GreenplumPost\&regionId=cn-hangzhou\&request=%7B%22instance_rs_type%22%3A%22ecs%22%2C%22engine_version%22%3A%226.0%22%2C%22seg_node_num%22%3A%224%22%2C%22SampleData%22%3A%22false%22%2C%22vector_optimizor%22%3A%22Y%22%7D) adresinden alabilirsiniz).

Örneği oluşturduktan sonra, [API](https://www.alibabacloud.com/help/en/analyticdb-for-postgresql/developer-reference/api-gpdb-2016-05-03-createaccount) aracılığıyla veya örnek detay web sayfasındaki 'Hesap Yönetimi' (Account Management) bölümünden bir yönetici hesabı oluşturmalısınız.

`llama-index` paketinin kurulu olduğundan emin olmalısınız:

```bash
%pip install llama-index-vector-stores-analyticdb
```

```bash
!pip install llama-index
```

### Lütfen parametreleri sağlayın:

```python
import os
import getpass


# alibaba cloud ram ak (erişim anahtarı) ve sk (gizli anahtar):
alibaba_cloud_ak = ""
alibaba_cloud_sk = ""


# örnek bilgileri:
region_id = "cn-hangzhou"  # spesifik örneğin bölge kimliği
instance_id = "gp-xxxx"  # adb örnek kimliği
account = "test_account"  # API veya örnek detay web sayfasındaki 'Hesap Yönetimi' aracılığıyla oluşturulan örnek hesap adı
account_password = ""  # örnek hesap şifresi
```

### Gerekli paket bağımlılıklarını içe aktarın:

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.analyticdb import AnalyticDBVectorStore
```

### Bazı örnek verileri yükleyin:

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Veriyi okuyun:

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge: {len(documents)}")
print(f"İlk belge, kimlik (id): {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    "İlk belge, metin"
    f" ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

### AnalyticDB Vektör Deposu (Vector Store) nesnesini oluşturun:

```python
analytic_db_store = AnalyticDBVectorStore.from_params(
    access_key_id=alibaba_cloud_ak,
    access_key_secret=alibaba_cloud_sk,
    region_id=region_id,
    instance_id=instance_id,
    account=account,
    account_password=account_password,
    namespace="llama",
    collection="llama",
    metrics="cosine",
    embedding_dimension=1536,
)
```

### Belgelerden İndeksi Oluşturun:

```python
storage_context = StorageContext.from_defaults(vector_store=analytic_db_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### İndeksi kullanarak sorgulama yapın:

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden AI üzerinde çalışmayı seçti?")


print(response.response)
```

### Koleksiyonu silin:

```python
analytic_db_store.delete_collection()
```
