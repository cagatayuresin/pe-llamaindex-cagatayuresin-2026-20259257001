---
title: Lantern Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Lantern Vektör Deposu

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için [Postgresql](https://www.postgresql.org) ve [Lantern](https://github.com/lanterndata/lantern) veritabanının nasıl kullanılacağını göstereceğiz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-lantern
%pip install llama-index-embeddings-openai
```

```bash
!pip install psycopg2-binary llama-index asyncpg
```

```python
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.lantern import LanternVectorStore
import textwrap
import openai
```

### OpenAI Kurulumu

İlk adım OpenAI anahtarını yapılandırmaktır. Bu anahtar, indekse yüklenen belgeler için gömmeler (embeddings) oluşturmak amacıyla kullanılacaktır.

```python
import os


os.environ["OPENAI_API_KEY"] = "<anahtarınız>"
openai.api_key = "<anahtarınız>"
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükleme

`SimpleDirectoryReader` kullanarak `data/paul_graham/` dizininde saklanan belgeleri yükleyin

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

### Veritabanını Oluşturma

Yerel makinede (localhost) çalışan mevcut bir postgres kullanarak, kullanacağımız veritabanını oluşturun.

```python
import psycopg2


connection_string = "postgresql://postgres:postgres@localhost:5432"
db_name = "postgres"
conn = psycopg2.connect(connection_string)
conn.autocommit = True


with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")
```

```python
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings


# Gömme modeliyle küresel ayarları (global settings) yapılandırın
# Böylece sorgu dizeleri gömmelere dönüştürülecek ve HNSW indeksi kullanılacaktır
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
```

### İndeksi Oluşturma

Burada, daha önce yüklenen belgeleri kullanarak Postgres destekli bir indeks oluşturuyoruz. `LanternVectorStore` birkaç parametre alır.

```python
from sqlalchemy import make_url


url = make_url(connection_string)
vector_store = LanternVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai gömme boyutu
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
query_engine = index.as_query_engine()
```

### İndeksi Sorgulama

Artık indeksimizi kullanarak sorular sorabiliriz.

```python
response = query_engine.query("Yazar neler yaptı?")
```

```python
print(textwrap.fill(str(response), 100))
```

```python
response = query_engine.query("1980'lerin ortalarında neler oldu?")
```

```python
print(textwrap.fill(str(response), 100))
```

### Mevcut İndeksi Sorgulama

```python
vector_store = LanternVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai gömme boyutu
    m=16,  # HNSW M parametresi
    ef_construction=128,  # HNSW ef construction parametresi
    ef=64,  # HNSW ef arama parametresi
)


# HNSW parametreleri hakkında daha fazlasını buradan okuyun: https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine()
```

```python
response = query_engine.query("Yazar neler yaptı?")
```

```python
print(textwrap.fill(str(response), 100))
```

### Hibrit Arama (Hybrid Search)

Hibrit aramayı etkinleştirmek için şunları yapmanız gerekir:

1. `LanternVectorStore` oluştururken `hybrid_search=True` parametresini geçirin (ve isteğe bağlı olarak `text_search_config` parametresini istenen dille yapılandırın).
2. Sorgu motorunu oluştururken `vector_store_query_mode="hybrid"` parametresini geçirin (bu yapılandırma arka planda erişiciye iletilir). Ayrıca, seyrek metin aramasından (sparse text search) kaç sonuç almamız gerektiğini yapılandırmak için isteğe bağlı olarak `sparse_top_k` değerini ayarlayabilirsiniz (varsayılan olarak `similarity_top_k` ile aynı değer kullanılır).

```python
from sqlalchemy import make_url


url = make_url(connection_string)
hybrid_vector_store = LanternVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay_hybrid_search",
    embed_dim=1536,  # openai gömme boyutu
    hybrid_search=True,
    text_search_config="english",
)


storage_context = StorageContext.from_defaults(
    vector_store=hybrid_vector_store
)
hybrid_index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
hybrid_query_engine = hybrid_index.as_query_engine(
    vector_store_query_mode="hybrid", sparse_top_k=2
)
hybrid_response = hybrid_query_engine.query(
    "Paul Graham 'schtick' kelimesiyle kimi kastediyor?"
)
```

```python
print(hybrid_response)
```
