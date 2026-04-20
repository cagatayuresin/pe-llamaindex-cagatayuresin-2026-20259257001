---
title: Pinecone Vektör Deposu - Hibrit Arama
 | LlamaIndex OSS Belgeleri
---

# Pinecone Vektör Deposu - Hibrit Arama

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-pinecone "transformers[torch]"
```

#### Bir Pinecone İndeksi Oluşturma

```python
from pinecone import Pinecone, ServerlessSpec
```

```python
import os


os.environ["PINECONE_API_KEY"] = "..."
os.environ["OPENAI_API_KEY"] = "sk-..."


api_key = os.environ["PINECONE_API_KEY"]


pc = Pinecone(api_key=api_key)
```

```python
# gerekirse silin
pc.delete_index("quickstart")
```

```python
# boyutlar text-embedding-ada-002 içindir
# NOT: hibrit arama için dotproduct metriğine ihtiyaç duyar


pc.create_index(
    name="quickstart",
    dimension=1536,
    metric="dotproduct",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)


# Pod Tabanlı bir Pinecone indeksi oluşturmanız gerekiyorsa, alternatif olarak şunu yapabilirsiniz:
#
# from pinecone import Pinecone, PodSpec
#
# pc = Pinecone(api_key='xxx')
#
# pc.create_index(
#    name='my-index',
#    dimension=1536,
#    metric='cosine',
#    spec=PodSpec(
#      environment='us-east1-gcp',
#      pod_type='p1.x1',
#      pods=1
#    )
# )
```

```python
pinecone_index = pc.Index("quickstart")
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Belgeleri yükleyin, PineconeVectorStore'u oluşturun

`add_sparse_vector=True` olduğunda, `PineconeVectorStore` her belge için seyrek vektörleri (sparse vectors) hesaplayacaktır.

Varsayılan olarak, seyrek vektörler için basit belirteç (token) frekansını kullanır. Ancak, özel bir seyrek gömme (sparse embedding) modeli de belirtebilirsiniz.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from IPython.display import Markdown, display
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
# veri yükleme (upsert) sırasında seyrek vektörleri hesaplamak için add_sparse_vector=True olarak ayarlayın
from llama_index.core import StorageContext


if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(f"OPENAI_API_KEY ortam değişkeni ayarlanmamış")


vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
    add_sparse_vector=True,
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```bash
huggingface/tokenizers: Mevcut süreç (process), paralellik zaten kullanıldıktan sonra çatallandı (fork). Kilitlenmeleri (deadlock) önlemek için paralellik devre dışı bırakılıyor...
Bu uyarıyı devre dışı bırakmak için şunlardan birini yapabilirsiniz:
  - Mümkünse çatallanmadan (fork) önce `tokenizers` kullanmaktan kaçının
  - TOKENIZERS_PARALLELISM=(true | false) ortam değişkenini açıkça ayarlayın


Upserted vectors:   0%|          | 0/22 [00:00<?, ?it/s]
```

#### İndeksi Sorgulama

İndeksin hazır olması için bir veya iki dakika beklemeniz gerekebilir.

```python
# daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine(vector_store_query_mode="hybrid")
response = query_engine.query("Viaweb'de ne oldu?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**"Paul Graham, paraya ihtiyacı olduğu için Viaweb'i kurdu. Şirket büyüdükçe büyük bir şirketi yönetmek istemediğini fark etti ve vizyonun bir alt kümesini açık kaynaklı bir proje olarak oluşturmaya karar verdi. Sonunda Viaweb, 1998 yazında Yahoo tarafından satın alındı; bu durum Paul Graham için büyük bir rahatlama oldu."**

## Seyrek gömme modelini değiştirme

```bash
%pip install llama-index-sparse-embeddings-fastembed
```

```python
# Vektör deposunu temizle
vector_store.clear()
```

```python
from llama_index.sparse_embeddings.fastembed import FastEmbedSparseEmbedding


sparse_embedding_model = FastEmbedSparseEmbedding(
    model_name="prithivida/Splade_PP_en_v1"
)


vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
    add_sparse_vector=True,
    sparse_embedding_model=sparse_embedding_model,
)
```

```bash
Fetching 5 files:   0%|          | 0/5 [00:00<?, ?it/s]
```

```python
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```bash
Upserted vectors:   0%|          | 0/22 [00:00<?, ?it/s]
```

Yükleme işlemleri için bir dakika bekleyin...

```python
response = query_engine.query("Viaweb'de ne oldu?")
display(Markdown(f"<b>{response}</b>"))
```

**"Paul Graham, paraya ihtiyacı olduğu için Viaweb'i başlattı. Bir uygulama oluşturucu ve ağ altyapısı oluşturmaya odaklanarak, yazılım ve hizmetler oluşturmak üzerine bir ekip topladı. Ancak yazın ortasında Paul, büyük bir şirketi yönetmek istemediğini fark etti ve odağını projenin bir alt kümesini açık kaynaklı bir proje olarak inşa etmeye kaydırmaya karar verdi. Bu durum, Arc adlı yeni bir Lisp lehçesinin geliştirilmesine yol açtı. Nihayetinde Viaweb, 1998 yazında Yahoo'ya satıldı; bu da Paul Graham'a rahatlık sağladı ve hayatının yeni bir evresine geçmesine izin verdi."**
