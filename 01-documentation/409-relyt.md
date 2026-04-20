---
title: Relyt
 | LlamaIndex OSS Belgeleri
---

# Relyt

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/vector_stores/PGVectoRsDemo.ipynb)

Öncelikle muhtemelen bağımlılıkları (dependencies) kurmanız gerekecektir:

```bash
%pip install llama-index-vector-stores-relyt
```

```bash
%pip install llama-index "pgvecto_rs[sdk]"
```

Ardından, [resmi belgede (official document)](https://docs.relyt.cn/docs/vector-engine/use/) yer aldığı üzere relyt'i başlatın:

Günlükleyiciyi (logger) ayarlayın.

```python
import logging
import os
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

#### Bir pgvecto\_rs istemcisi oluşturma

```python
from pgvecto_rs.sdk import PGVectoRs


URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
    port=os.getenv("RELYT_PORT", "5432"),
    host=os.getenv("RELYT_HOST", "localhost"),
    username=os.getenv("RELYT_USER", "postgres"),
    password=os.getenv("RELYT_PASS", "mysecretpassword"),
    db_name=os.getenv("RELYT_NAME", "postgres"),
)


client = PGVectoRs(
    db_url=URL,
    collection_name="example",
    dimension=1536,  # OpenAI'nin text-embedding-ada-002'si kullanılıyor
)
```

#### OpenAI'yi kurma

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

#### Belgeleri yükleyin, PGVectoRs Deposu ve Vektör Deposu İndeksini (PGVectoRsStore and VectorStoreIndex) oluşturun

```python
from IPython.display import Markdown, display


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.relyt import RelytVectorStore
```

Veriyi İndirin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```python
# meta veri (metadata) filtresi olmadan başlatın
from llama_index.core import StorageContext


vector_store = RelytVectorStore(client=client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeks Sorgulayın (Query Index)

```python
# daha detaylı çıktılar için Günlüklemeyi (Logging) DEBUG olarak ayarlayın
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

**Yazar büyürken yazma ve programlama üzerine çalışmalar yürüttü. Kısa hikayeler yazdı ve bir IBM 1401 bilgisayarında da bazı programlar teşkil etmeye çalıştı. Sonrasında kendisine ait bir mikrobilgisayar edindiğinde yazılım programlamaya daha fazla ağırlık göstererek, birtakım çok basit oyunlar ve kelime işlemci (word processor) yazılımları ortaya koydu.**
