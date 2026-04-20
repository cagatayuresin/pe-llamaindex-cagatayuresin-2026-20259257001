---
title: Tair Vektör Deposu (Tair Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Tair Vektör Deposu (Tair Vector Store)

Bu not defterimizde (notebook); TairVectorStore/Tair Vektör Deposunun nasıl kullanılacağına ilişkin hızlı ve pratik bir tanıtım / demo örneğini sizlere sunacağız.

Eğer bu Not Defterini (Notebook) Colab ortamında açıyorsanız, muhtemelen LlamaIndex'i 🦙 sisteminize kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-tair
```

```bash
!pip install llama-index
```

```python
import os
import sys
import logging
import textwrap


import warnings


warnings.filterwarnings("ignore")


# huggingface uyarılarının/ikazlarının (warnings) önüne geçerek durdurun
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Hata ayıklama (debug) günlüklerini/verilerini görmek istiyorsanız yorum satırını kaldırarak aktif (uncomment) edebilirsiniz
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    Document,
)
from llama_index.vector_stores.tair import TairVectorStore
from IPython.display import Markdown, display
```

### OpenAI Ayarları (Setup OpenAI)

İşe ilk öncelikle openai lisans api anahtar atamasını / yapısını deklare edip ekleyerek (adding) başlayalım. Bu aşamadaki evre, openai'ın kendisinin yer aldığı gömme (embeddings) veya "chatgpt" işlevlerinin/işlemlerinin kullanımına yönelik olan erişim olanaklarını (access) bize tahsis edecektir / sağlayacaktır.

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-<sizin_anahtariniz_buraya_gelecek>"
```

### Veriyi İndirin (Download Data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Bir veri setini/kümesini okuyun/sisteme içeri atın (Read in a dataset)

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print(
    "Belge Kimliği (Document ID):",
    documents[0].doc_id,
    "Belge Özeti / Karma Değeri (Document Hash):",
    documents[0].doc_hash,
)
```

### Belgeleri baz alarak/belgelerden indeks inşa edin/oluşturun (Build index from documents)

Temel / arka uç sağlayıcısı (backend) bağlamında `TairVectorStore` verisini/mekanizmasını atayarak `GPTVectorStoreIndex` üzerinden vektörel dizilim/indeks inşa edelim. Buradaki `tair_url` kısmını / kod alanını, Tair kullanım nesnesinin/otorumunun kendisindeki mevcudiyeti olan yâni bizzat var eden asıl url bağlantısıyla (actual url) değiştirerek takdim edin (replace).

```python
from llama_index.core import StorageContext


tair_url = "redis://{kullaniciadi}:{sifre}@r-bp****************.redis.rds.aliyuncs.com:{port}"


vector_store = TairVectorStore(
    tair_url=tair_url, index_name="pg_essays", overwrite=True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = GPTVectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### Veriyi sorgulayın (Query the data)

Artık tam da şimdi (Now), edindiğimiz ve yığdığımız asıl dizin / indeksleri bizzat bilgi ve donanımımız olan bilgi tabanı (knowledge base) suretinde tatbikata sokup da (kullanıp) kendilerine rahatlıkla birtakım sorgular dahi atarcasına/sormasına meyledebilir (ask questions to it) / sorabiliriz.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neleri öğrenip ne çıkardı? (What did the author learn?)")
print(textwrap.fill(str(response), 100))
```

```python
response = query_engine.query("Yazarın zor duruma girdiği/yaşadığı zor bir an, yahut anı tablosu da neydi? (What was a hard moment for the author?)")
print(textwrap.fill(str(response), 100))
```

### Belgelerin silinmesi/kaldırılması (Deleting documents)

İndekste var olan (İndeks tablosundan) evraka/bir belgeye ait izi tümden silebilmek (to delete) veyahut da kaldırmak adına; bilakis (sadece/yegane formda) `delete` yordamını ve yahut fonksiyon evresindeki metodu kullanmalısınız (use `delete` method).

```python
document_id = documents[0].doc_id
document_id
```

```python
info = vector_store.client.tvs_get_index("pg_essays")
print("Belge / Evrak Adedi (Number of documents)", int(info["data_count"]))
```

```python
vector_store.delete(document_id)
```

```python
info = vector_store.client.tvs_get_index("pg_essays")
print("Belge / Evrak Adedi (Number of documents)", int(info["data_count"]))
```

### Dizin/indeks silinmesi/kaldırılması (Deleting index)

Halihazırda var edip bir döküme attığınız indekse ait o tekmil tüm form yapısını (entire index) bir sefere kalmıksızın silmek adına; doğrudan `delete_index` metoduna/evresine müracaat edip onu referans olarak kullanının (use method).

```python
vector_store.delete_index()
```

```python
print("İndeks varlığını / baki kalıp kalmadığını kontrol et / döküme al (Check index existence):", vector_store.client._index_exists())
```
