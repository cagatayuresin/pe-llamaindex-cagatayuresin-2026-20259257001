# Basit Füzyon Erişicisi (Simple Fusion Retriever)

---
title: Basit Füzyon Erişicisi (Simple Fusion Retriever)
 | LlamaIndex OSS Belgeleri
---

Bu örnekte, birden fazla sorgu ve birden fazla indeksten gelen erişim sonuçlarını nasıl birleştirebileceğinizi inceliyoruz.

Getirilen düğümler, tüm sorgular ve indeksler genelinde en iyi k (top-k) sonucu olarak döndürülecek ve düğümlerin yinelenenleri (de-duplication) ayıklanacaktır.

```python
import os
import openai


os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = os.environ["OPENAI_API_KEY"]
```

## Kurulum (Setup)

Bu not defteri için, her biri ayrı bir indekste saklanan, belgelerimizdeki birbirine çok benzer iki sayfayı kullanacağız.

```python
from llama_index.core import SimpleDirectoryReader


documents_1 = SimpleDirectoryReader(
    input_files=["../../community/integrations/vector_stores.md"]
).load_data()
documents_2 = SimpleDirectoryReader(
    input_files=["../../module_guides/storing/vector_stores.md"]
).load_data()
```

```python
from llama_index.core import VectorStoreIndex


index_1 = VectorStoreIndex.from_documents(documents_1)
index_2 = VectorStoreIndex.from_documents(documents_2)
```

## İndeksleri Birleştirin! (Fuse the Indexes!)

Bu adımda, indekslerimizi tek bir erişicide birleştiriyoruz. Bu erişici aynı zamanda orijinal soruyla ilgili ek sorgular üreterek sorgumuzu genişletecek ve sonuçları bir araya getirecektir.

Bu düzenek 4 kez sorgulama yapacaktır: bir kez orijinal sorgunuzla ve 3 tane daha üretilen sorgu ile.

Varsayılan olarak, ek sorgular oluşturmak için aşağıdaki istemi (prompt) kullanır:

```python
QUERY_GEN_PROMPT = (
    "Sen, tek bir giriş sorgusuna dayanarak birden fazla arama sorgusu üreten yardımcı bir asistansın. "
    "Aşağıdaki giriş sorgusuyla ilgili, her satıra bir tane gelecek şekilde {num_queries} tane arama sorgusu oluştur:\n"
    "Sorgu (Query): {query}\n"
    "Sorgular (Queries):\n"
)
```

```python
from llama_index.core.retrievers import QueryFusionRetriever


retriever = QueryFusionRetriever(
    [index_1.as_retriever(), index_2.as_retriever()],
    similarity_top_k=2,
    num_queries=4,  # sorgu oluşturmayı devre dışı bırakmak için bunu 1 yapın
    use_async=True,
    verbose=True,
    # query_gen_prompt="...",  # burada sorgu oluşturma istemini geçersiz kılabiliriz
)
```

```python
# bir not defterinde çalıştırmak için iç içe geçmiş asenkron yapıyı uygula
import nest_asyncio


nest_asyncio.apply()
```

```python
nodes_with_scores = retriever.retrieve("Nasıl bir chroma vektör deposu kurarım?")
```

```text
Generated queries:
1. Bir chroma vektör deposu kurmak için gereken adımlar nelerdir?
2. Bir chroma vektör deposunu yapılandırmak için en iyi uygulamalar
3. Bir chroma vektör deposu kurarken karşılaşılan yaygın sorunların giderilmesi
```

```python
for node in nodes_with_scores:
    print(f"Puan (Score): {node.score:.2f} - {node.text[:100]}...")
```

```text
Score: 0.78 - # Vektör Depoları


Vektör depoları, alınan belge parçalarının gömme vektörlerini (ve bazen...
Score: 0.78 - # Vektör Depolarını Kullanma


LlamaIndex, vektör depoları / vektör veri... ile birden fazla entegrasyon noktası sunar...
```

## Bir Sorgu Motorunda Kullanın! (Use in a Query Engine!)

Şimdi, doğal dilde yanıtlar sentezlemek için erişicimizi bir sorgu motoruna bağlayabiliriz.

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine.from_args(retriever)
```

```python
response = query_engine.query(
    "Nasıl bir chroma vektör deposu kurarım? Bir örnek verebilir misiniz?"
)
```

```text
Generated queries:
1. Bir chroma vektör deposu nasıl kurulur?
2. Bir chroma vektör deposu oluşturmak için adım adım kılavuz.
3. Chroma vektör deposu kurulumu ve yapılandırması örnekleri.
```

```python
from llama_index.core.response.notebook_utils import display_response


display_response(response)
```

**`Nihai Yanıt (Final Response):`** Bir Chroma vektör deposu kurmak için şu adımları izlemeniz gerekir:

1. Gerekli kütüphaneleri içe aktarın:

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
```

2. Bir Chroma istemcisi (client) oluşturun:

```python
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")
```

3. Vektör deposunu oluşturun:

```python
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
```

Yukarıdaki adımları kullanarak bir Chroma vektör deposunun nasıl kurulacağına dair bir örnek aşağıdadır:

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore


# Bir Chroma istemcisi oluşturma
# EphemeralClient tamamen bellek içinde çalışır, PersistentClient ise diske de kaydeder
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")


# vektör deposunu oluştur
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
```

Bu örnek, bir Chroma istemcisinin nasıl oluşturulacağını, "quickstart" adında bir koleksiyonun nasıl oluşturulacağını ve ardından bu koleksiyonu kullanarak bir Chroma vektör deposunun nasıl inşa edileceğini gösterir.
