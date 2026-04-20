---
title: Hologres
 | LlamaIndex OSS Belgeleri
---

# Hologres

> [Hologres](https://www.alibabacloud.com/help/en/hologres/), yüksek performanslı OLAP analizini ve yüksek QPS'li çevrimiçi hizmetleri destekleyebilen uçtan uca gerçek zamanlı bir veri ambarıdır.

Bu not defterini çalıştırmak için bulutta çalışan bir Hologres örneğine (instance) ihtiyacınız vardır. [Bu bağlantıyı](https://www.alibabacloud.com/help/en/hologres/getting-started/purchase-a-hologres-instance#task-1918224) takip ederek bir tane edinebilirsiniz.

Örneği oluşturduktan sonra, [Hologres konsolu](https://www.alibabacloud.com/help/en/hologres/user-guide/instance-list?spm=a2c63.p38356.0.0.79b34766nhwskN) üzerinden aşağıdaki yapılandırmaları belirleyebilmelisiniz:

```python
test_hologres_config = {
    "host": "<sunucu_adresi>",
    "port": 80,
    "user": "<kullanici_adi>",
    "password": "<parola>",
    "database": "<veritabani_adi>",
    "table_name": "<tablo_adi>",
}
```

Bu arada, `llama-index`'in kurulu olduğundan emin olmanız gerekir:

```bash
%pip install llama-index-vector-stores-hologres
```

```bash
!pip install llama-index
```

### Gerekli paket bağımlılıklarını içe aktarın:

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.hologres import HologresVectorStore
```

### Bazı örnek verileri yükleyin:

```bash
!mkdir -p 'data/paul_graham/'
!curl 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -o 'data/paul_graham/paul_graham_essay.txt'
```

### Veriyi okuyun:

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge sayısı: {len(documents)}")
print(f"İlk belge, kimlik (id): {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    "İlk belge metni"
    f" ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

```text
Toplam belge sayısı: 1
İlk belge, kimlik (id): 824dafc0-0aa1-4c80-b99c-33895cfc606a
İlk belge, hash: 8430b3bdb65ee0a7853463b71e7e1e20beee3a3ce15ef3ec714919f8653b2eb9
İlk belge metni (75014 karakter):
====================




Neler Üzerine Çalıştım


Şubat 2021


Üniversiteden önce, okul dışında çalıştığım iki ana konu yazarlık ve programlamaydı. Makale yazmazdım. O zamanlar başlangıç seviyesindeki yazarların ne yazması gerekiyorsa onları yazardım (hâlâ da muhtemelen öyledir): kısa hikayeler. Hikayelerim berbattı. Neredeyse hiç olay örgüsü yoktu, sadece güçlü hisleri olan karakterler vardı ve bunun onları derin kıldığını hayal ederdim ...
```

### AnalyticDB Vektör Deposu nesnesini oluşturun:

```python
hologres_store = HologresVectorStore.from_param(
    host=test_hologres_config["host"],
    port=test_hologres_config["port"],
    user=test_hologres_config["user"],
    password=test_hologres_config["password"],
    database=test_hologres_config["database"],
    table_name=test_hologres_config["table_name"],
    embedding_dimension=1536,
    pre_delete_table=True,
)
```

### Belgelerden İndeksi Oluşturun:

```python
storage_context = StorageContext.from_defaults(vector_store=hologres_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### İndeksi kullanarak sorgulama yapın:

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden yapay zeka (AI) üzerine çalışmayı seçti?")


print(response.response)
```

**Yazar, Mike adlı zeki bir bilgisayarı konu alan "The Moon is a Harsh Mistress" (Ay Zalim Bir Sevgilidir) adlı bilim kurgu romanının ve Terry Winograd'ın SHRDLU programını kullanımını sergileyen bir PBS belgeselinin etkisinden dolayı yapay zeka üzerine çalışmaya ilham almıştır. Bu deneyimler, yazarı zeki makineler yaratmanın yakın bir gerçeklik olduğuna inandırmış ve yapay zeka alanına olan ilgisini artırmıştır.**
