---
title: Qdrant Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

#### Bir Qdrant İstemcisi Oluşturma

```bash
%pip install llama-index-vector-stores-qdrant llama-index-readers-file llama-index-embeddings-fastembed llama-index-llms-openai
```

```python
import logging
import sys
import os


import qdrant_client
from IPython.display import Markdown, display
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings


Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
```

Eğer ilk kez çalıştırıyorsanız, şu komutları kullanarak bağımlılıkları yükleyin:

```bash
!pip install -U qdrant_client fastembed
```

LLM kimlik doğrulaması (authentication) için OpenAI anahtarınızı ayarlayın

OpenAI API anahtarını OPENAI\_API\_KEY ortam değişkenine (environment variable) ayarlamak için bunları takip edin:

1. Terminal Kullanarak

```bash
export OPENAI_API_KEY=api_anahtarinizi_buraya_yazin
```

2. Jupyter Notebook'ta IPython Sihirli Komutunu (Magic Command) Kullanarak

```bash
%env OPENAI_API_KEY=<API_ANAHTARINIZ>
```

3. Python Betiği (Script) Kullanarak

```python
import os


os.environ["OPENAI_API_KEY"] = "api_anahtarinizi_buraya_yazin"
```

Not: Genel olarak API anahtarları gibi hassas bilgilerin betiklere (script) sabit olarak kodlanması yerine ortam değişkenleri (environment variables) olarak ayarlanması önerilir.

```python
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Belgeleri yükleyin

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

#### VectorStoreIndex'i (Vektör Deposu İndeksi) Oluşturun

```python
client = qdrant_client.QdrantClient(
    # Hızlı ve hafif denemeler için :memory: modunu kullanabilirsiniz,
    # bu mod, Qdrant'ın herhangi bir yere dağıtılmasını gerektirmez
    # ancak qdrant-client >= 1.1.1 sürümüne ihtiyaç duyar
    # location=":memory:"
    # aksi takdirde Qdrant örnek (instance) adresini url ile ayarlayın:
    # url="http://<ana_bilgisayar>:<baglanti_noktasi>"
    # aksi takdirde ana bilgisayar (host) ve bağlantı noktası (port) ile ayarlayın:
    host="localhost",
    port=6333
    # Qdrant Cloud için API ANAHTARINI ayarlayın
    # api_key="<qdrant-api-key>",
)
```

```python
vector_store = QdrantVectorStore(client=client, collection_name="paul_graham")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
```

#### İndeksi Sorgulama

```python
# Daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar üniversiteden önce yazma ve programlama üzerine çalıştı.**

```python
# Daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query(
    "Yazar, Viaweb'deki görevinden sonra ne yaptı?"
)
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, Viaweb'deki zamanından sonra müşteriler için projeler yürüten bir grup adına serbest (freelance) çalışmak üzere anlaşmalar yaptı.**

#### Asenkron (Asynchronously) VectorStoreIndex Oluşturma

```python
# Aynı olay döngüsüne (event-loop) bağlanmak için,
# notebook'ta asenkron olayların (async events) çalışmasına izin verir


import nest_asyncio


nest_asyncio.apply()
```

```python
aclient = qdrant_client.AsyncQdrantClient(
    # Hızlı ve hafif denemeler için :memory: modunu kullanabilirsiniz,
    # bu mod, Qdrant'ın herhangi bir yere dağıtılmasını gerektirmez
    # ancak qdrant-client >= 1.1.1 sürümüne ihtiyaç duyar
    location=":memory:"
    # aksi takdirde Qdrant örnek (instance) adresini şununla ayarlayın:
    # uri="http://<ana_bilgisayar>:<baglanti_noktasi>"
    # Qdrant Cloud için API ANAHTARINI ayarlayın
    # api_key="<qdrant-api-key>",
)
```

```python
vector_store = QdrantVectorStore(
    collection_name="paul_graham",
    client=client,
    aclient=aclient,
    prefer_grpc=True,
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    use_async=True,
)
```

#### Asenkron İndeks Sorgulama (Async Query Index)

```python
query_engine = index.as_query_engine(use_async=True)
response = await query_engine.aquery("Yazar büyürken neler yaptı?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar; kısa hikayeler yazdı ve programlama üzerinde çalıştı, özellikle 9. sınıfta Fortran'ın eski bir sürümünü kullanarak bir IBM 1401 bilgisayarında programlar yazdı. Daha sonra, 1980 yılı civarında TRS-80 ile mikro bilgisayarlara geçiş yaptı, basit oyunlar, programlar ve bir kelime işlemci (word processor) yazdı.**

```python
# Daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine(use_async=True)
response = await query_engine.aquery(
    "Yazar Viaweb'deki görevinden sonra ne yaptı?"
)
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, Viaweb'deki zamanının ardından Y Combinator'ın kurucu ortaklarından (co-found) biri oldu.**

## Hibrit Arama (Hybrid Search)

Bir qdrant indeksi oluştururken hibrit aramayı etkinleştirebilirsiniz. Burada, hibrit erişim için hızlı bir şekilde seyrek (sparse) ve yoğun (dense) bir indeks oluşturmak amacıyla Qdrant'ın BM25 özelliklerinden yararlanıyoruz.

```python
from qdrant_client import QdrantClient, AsyncQdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore


client = QdrantClient(host="localhost", port=6333)
aclient = AsyncQdrantClient(host="localhost", port=6333)


vector_store = QdrantVectorStore(
    client=client,
    aclient=aclient,
    collection_name="paul_graham_hybrid",
    enable_hybrid=True,
    fastembed_sparse_model="Qdrant/bm25",
)


index = VectorStoreIndex.from_documents(
    documents,
    storage_context=StorageContext.from_defaults(vector_store=vector_store),
)


# 2 seyrek, 2 yoğun veri çekin ve toplamda 3 hibrit sonuca filtreleyin
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid",
    sparse_top_k=2,
    similarity_top_k=2,
    hybrid_top_k=3,
)


response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

## Kaydetme ve Yükleme

Bir indeksi geri yüklemek için çoğu durumda doğrudan vektör deposu (vector store) nesnesinin kendisini kullanarak geri yükleme yapabilirsiniz. İndeks, Qdrant tarafından otomatik olarak kaydedilir.

```python
loaded_index = VectorStoreIndex.from_vector_store(
    vector_store,
    # Gömme modeli (Embedding model), orijinal gömme modeliyle eşleşmelidir
    # embed_model=Settings.embed_model
)
```
