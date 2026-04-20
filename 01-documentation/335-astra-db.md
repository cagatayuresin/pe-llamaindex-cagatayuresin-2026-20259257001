# Astra DB

---
title: Astra DB
 | LlamaIndex OSS Belgeleri
---

> [DataStax Astra DB](https://docs.datastax.com/en/astra/home/astra.html), Apache Cassandra üzerine inşa edilmiş ve kullanımı kolay bir JSON API aracılığıyla erişilen, sunucusuz (serverless), vektör yetenekli bir veritabanıdır.

Bu not defterini çalıştırmak için bulutta çalışan bir DataStax Astra DB örneğine (instance) ihtiyacınız vardır (ücretsiz olarak [datastax.com](https://astra.datastax.com) adresinden edinebilirsiniz).

`llama-index` ve `astrapy` paketlerinin kurulu olduğundan emin olmalısınız:

```bash
%pip install llama-index-vector-stores-astra-db
%pip install llama-index-embeddings-openai
```

```bash
!pip install llama-index
!pip install "astrapy>=1.0"
```

### Lütfen veritabanı bağlantı parametrelerini ve gizli anahtarları sağlayın:

```python
import os
import getpass


api_endpoint = input(
    "\nLütfen Veritabanı Uç Noktası (Endpoint) URL'nizi girin (örneğin 'https://4bc...datastax.com'):"
)


token = getpass.getpass(
    "\nLütfen 'Veritabanı Yöneticisi' (Database Administrator) Belirtecinizi (Token) girin (örneğin 'AstraCS:...'):"
)


os.environ["OPENAI_API_KEY"] = getpass.getpass(
    "\nLütfen OpenAI API Anahtarınızı girin (örneğin 'sk-...'):"
)
```

### Gerekli paket bağımlılıklarını içe aktarın:

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.astra_db import AstraDBVectorStore
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

### Astra DB Vektör Deposu (Vector Store) nesnesini oluşturun:

```python
astra_db_store = AstraDBVectorStore(
    token=token,
    api_endpoint=api_endpoint,
    collection_name="astra_v_table",
    embedding_dimension=1536,
)
```

### Belgelerden İndeksi Oluşturun:

```python
embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")


storage_context = StorageContext.from_defaults(vector_store=astra_db_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)
```

### İndeksi kullanarak sorgulama yapın:

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden AI üzerinde çalışmayı seçti?")


print(response.response)
```
