# Verileri Kalıcı Hale Getirme ve Yükleme (Persisting & Loading Data)

## Verileri Kalıcı Hale Getirme (Persisting Data)

Varsayılan olarak LlamaIndex verileri bellekte (in-memory) saklar ve istenirse bu veriler açıkça kalıcı hale getirilebilir:

```python
storage_context.persist(persist_dir="<kayit_dizini>")
```

Bu işlem, verileri belirtilen `persist_dir` (veya varsayılan olarak `./storage`) altında diske kaydedecektir.

Yükleme için indeks ID'lerini takip ettiğiniz sürece, birden fazla indeks aynı dizine kaydedilebilir ve oradan yüklenebilir.

Kullanıcı ayrıca, verileri varsayılan olarak kalıcı hale getiren alternatif saklama arka uçları (örneğin `MongoDB`) yapılandırabilir.
Bu durumda, `storage_context.persist()` çağırmak hiçbir işlem yapmaz.

## Verileri Yükleme (Loading Data)

Verileri yüklemek için kullanıcının aynı yapılandırmayı (örneğin aynı `persist_dir` veya vektör deposu istemcisini geçirmek) kullanarak saklama bağlamını (storage context) yeniden oluşturması yeterlidir.

```python
storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir="<kayit_dizini>"),
    vector_store=SimpleVectorStore.from_persist_dir(
        persist_dir="<kayit_dizini>"
    ),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir="<kayit_dizini>"),
)
```

Daha sonra aşağıda belirtilen bazı kolaylık fonksiyonları aracılığıyla `StorageContext`'ten belirli indeksleri yükleyebiliriz.

```python
from llama_index.core import (
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)

# tek bir indeksi yükle
# aynı dizine birden fazla indeks kaydedilmişse index_id belirtmek gerekir
index = load_index_from_storage(storage_context, index_id="<index_id>")

# saklama bağlamında sadece bir indeks varsa index_id belirtmeye gerek yoktur
index = load_index_from_storage(storage_context)

# birden fazla indeksi yükle
indices = load_indices_from_storage(storage_context)  # tüm indeksleri yükler
indices = load_indices_from_storage(
    storage_context, index_ids=[index_id1, ...]
)  # belirli indeksleri yükler

# birleştirilebilir grafiği (composable graph) yükle
graph = load_graph_from_storage(
    storage_context, root_id="<kok_id>"
)  # belirtilen root_id'ye sahip grafiği yükler
```

## Uzak Bir Arka Uç (Remote Backend) Kullanma

Varsayılan olarak LlamaIndex, dosyaları yüklemek ve kaydetmek için yerel bir dosya sistemi kullanır. Ancak, bir `fsspec.AbstractFileSystem` nesnesi geçirerek bunu geçersiz kılabilirsiniz.

İşte bir vektör deposu başlatan basit bir örnek:

```python
import dotenv
import s3fs
import os

dotenv.load_dotenv("../../../.env")

# dökümanları yükle
documents = SimpleDirectoryReader(
    "../../../examples/paul_graham_essay/data/"
).load_data()
print(len(documents))
index = VectorStoreIndex.from_documents(documents)
```

Buraya kadar her şey aynıydı. Şimdi bir S3 dosya sistemi başlatalım ve oradan kaydedip/yükleyelim.

```python
# s3fs kurulumu
AWS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"]
R2_ACCOUNT_ID = os.environ["R2_ACCOUNT_ID"]

assert AWS_KEY is not None and AWS_KEY != ""

s3 = s3fs.S3FileSystem(
    key=AWS_KEY,
    secret=AWS_SECRET,
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    s3_additional_kwargs={"ACL": "public-read"},
)

# Aynı StorageContext ile 2+ indeks kullanıyorsanız,
# indeksi uzak nesne deposuna (blob storage) kaydetmek için bunu çalıştırın
index.set_index_id("vector_index")

# indeksi s3'e kaydet
s3_bucket_name = "llama-index/storage_demo"  # {bucket_adi}/{index_adi}
index.storage_context.persist(persist_dir=s3_bucket_name, fs=s3)

# indeksi s3'ten yükle
index_from_s3 = load_index_from_storage(
    StorageContext.from_defaults(persist_dir=s3_bucket_name, fs=s3),
    index_id="vector_index",
)
```

Varsayılan olarak, bir dosya sistemi geçirmezseniz yerel bir dosya sistemi kullandığınız varsayılacaktır.