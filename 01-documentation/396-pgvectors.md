---
title: pgvecto.rs
 | LlamaIndex OSS Belgeleri
---

# pgvecto.rs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/vector_stores/PGVectoRsDemo.ipynb)

Öncelikle, muhtemelen bağımlılıkları yüklemeniz gerekecektir:

```bash
%pip install llama-index-vector-stores-pgvecto-rs
```

```bash
%pip install llama-index "pgvecto_rs[sdk]"
```

Ardından, [resmi belgenin önerdiği gibi](https://github.com/tensorchord/pgvecto.rs#installation) pgvecto.rs sunucusunu başlatın:

```bash
!docker run --name pgvecto-rs-demo -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d tensorchord/pgvecto-rs:latest
```

Günlükçüyü (logger) kurun.

```python
import logging
import os
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

#### Bir pgvecto_rs istemcisi oluşturma

```python
from pgvecto_rs.sdk import PGVectoRs


URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
    port=os.getenv("DB_PORT", "5432"),
    host=os.getenv("DB_HOST", "localhost"),
    username=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASS", "mysecretpassword"),
    db_name=os.getenv("DB_NAME", "postgres"),
)


client = PGVectoRs(
    db_url=URL,
    collection_name="example",
    dimension=1536,  # OpenAI’nın text-embedding-ada-002 modelini kullanırken
)
```

#### OpenAI Kurulumu

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

#### Belgeleri yükleyin, PGVectoRsStore ve VectorStoreIndex'i oluşturun

```python
from IPython.display import Markdown, display


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.pgvecto_rs import PGVectoRsStore
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```python
# meta veri filtresi olmadan başlat
from llama_index.core import StorageContext


vector_store = PGVectoRsStore(client=client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

```python
# daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```bash
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**"Yazar büyürken yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve ayrıca bir IBM 1401 bilgisayarında programlar yazmayı denedi. Daha sonra bir mikro bilgisayar edindi ve daha kapsamlı bir şekilde programlama yapmaya başlayarak basit oyunlar ve bir kelime işlemci yazdı."**
