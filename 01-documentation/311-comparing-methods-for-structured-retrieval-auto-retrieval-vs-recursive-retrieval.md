# Yapılandırılmış Erişim Yöntemlerinin Karşılaştırılması (Otomatik Erişim ve Özyinelemeli Erişim)

---
title: Comparing Methods for Structured Retrieval (Auto-Retrieval vs. Recursive Retrieval)
 | LlamaIndex OSS Documentation
---

Basit bir RAG sisteminde, girdi belgeleri kümesi parçalara ayrılır, vektörleştirilir (embedding) ve bir vektör veritabanı koleksiyonuna aktarılır. Erişim işlemi (retrieval), vektör benzerliğine göre en iyi k (top-k) belgeyi getirir.

Belge seti çok büyükse bu yaklaşım başarısız olabilir; ham parçaları birbirinden ayırt etmek zor olabilir ve ilgili bağlamı içeren belgeleri filtreleyeceğinizin garantisi yoktur.

 Bu rehberde, daha yüksek hassasiyetli erişim için belgelerinizdeki yapıdan yararlanan daha gelişmiş sorgu algoritmaları olan **yapılandırılmış erişimi (structured retrieval)** inceliyoruz. Aşağıdaki iki yöntemi karşılaştırıyoruz:

- **Meta Veri Filtreleri + Otomatik Erişim (Auto-Retrieval)**: Her belgeyi doğru meta veri setiyle etiketleyin. Sorgu sırasında, anlamsal arama için sorgu dizgisini iletmenin yanı sıra meta veri filtrelerini de çıkarsamak (infer) için otomatik erişimi kullanın.
- **Belge Hiyerarşilerini Saklama (özetler -> ham parçalar) + Özyinelemeli Erişim (Recursive Retrieval)**: Belge özetlerini vektörleştirin ve bunları her belge için ham parçalar kümesiyle eşleştirin. Sorgu sırasında, belgeleri getirmeden önce ilk olarak özetleri getirmek için özyinelemeli erişimi kullanın.

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-openai
%pip install llama-index-vector-stores-weaviate
```

```python
!pip install llama-index
```

```python
import nest_asyncio


nest_asyncio.apply()
```

```python
import logging
import sys
from llama_index.core import SimpleDirectoryReader
from llama_index.core import SummaryIndex


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
wiki_titles = ["Michael Jordan", "Elon Musk", "Richard Branson", "Rihanna"]
wiki_metadatas = {
    "Michael Jordan": {
        "category": "Spor", # Sports
        "country": "Amerika Birleşik Devletleri", # United States
    },
    "Elon Musk": {
        "category": "İş Dünyası", # Business
        "country": "Amerika Birleşik Devletleri", # United States
    },
    "Richard Branson": {
        "category": "İş Dünyası", # Business
        "country": "Birleşik Krallık", # UK
    },
    "Rihanna": {
        "category": "Müzik", # Music
        "country": "Barbados",
    },
}
```

```python
from pathlib import Path


import requests


for title in wiki_titles:
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            # 'exintro': True,
            "explaintext": True,
        },
    ).json()
    page = next(iter(response["query"]["pages"].values()))
    wiki_text = page["extract"]


    data_path = Path("data")
    if not data_path.exists():
        Path.mkdir(data_path)


    with open(data_path / f"{title}.txt", "w") as fp:
        fp.write(wiki_text)
```

```python
# Tüm wiki belgelerini yükle
docs_dict = {}
for wiki_title in wiki_titles:
    doc = SimpleDirectoryReader(
        input_files=[f"data/{wiki_title}.txt"]
    ).load_data()[0]


    doc.metadata.update(wiki_metadatas[wiki_title])
    docs_dict[wiki_title] = doc
```

```python
from llama_index.llms.openai import OpenAI
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.core.node_parser import SentenceSplitter




llm = OpenAI("gpt-4")
callback_manager = CallbackManager([LlamaDebugHandler()])
splitter = SentenceSplitter(chunk_size=256)
```

## Meta Veri Filtreleri + Otomatik Erişim (Auto-Retrieval)

Bu yaklaşımda, her Belgeyi meta verilerle (kategori, ülke) etiketliyoruz ve bir Weaviate vektör veritabanında saklıyoruz.

Erişim zamanında, ilgili meta veri filtreleri kümesini çıkarsamak için "otomatik erişim" gerçekleştiriyoruz.

```python
## Weaviate Kurulumu
import weaviate


# bulut (cloud)
auth_config = weaviate.AuthApiKey(api_key="<api_anahtarınız>")
client = weaviate.Client(
    "https://llama-index-test-v0oggsoz.weaviate.network",
    auth_client_secret=auth_config,
)
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from IPython.display import Markdown, display
```

```python
# önce koleksiyondan öğeleri sil
client.schema.delete_class("LlamaIndex")
```

```python
from llama_index.core import StorageContext


# Dizini daha sonra yüklemek isterseniz, ona bir ad verdiğinizden emin olun!
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# NOT: manuel olarak bir index_name tanımlamayı da seçebilirsiniz.
# index_name = "test_prefix"
# vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)
```

```python
# şemanın oluşturulduğunu doğrula
class_schema = client.schema.get("LlamaIndex")
display(class_schema)
```

```json
{'class': 'LlamaIndex',
 'description': 'LlamaIndex Sınıfı',
 'invertedIndexConfig': {'bm25': {'b': 0.75, 'k1': 1.2},
  'cleanupIntervalSeconds': 60,
  'stopwords': {'additions': None, 'preset': 'en', 'removals': None}},
 'multiTenancyConfig': {'enabled': False},
 'properties': [{'dataType': ['text'],
   'description': 'Metin özelliği',
   'indexFilterable': True,
   'indexSearchable': True,
   'name': 'text',
   'tokenization': 'word'},
  {'dataType': ['text'],
   'description': 'Düğümün ref_doc_id değeri',
   'indexFilterable': True,
   'indexSearchable': True,
   'name': 'ref_doc_id',
   'tokenization': 'word'},
  {'dataType': ['text'],
   'description': 'node_info (JSON formatında)',
   'indexFilterable': True,
   'indexSearchable': True,
   'name': 'node_info',
   'tokenization': 'word'},
  {'dataType': ['text'],
   'description': 'Düğümün ilişkileri (JSON formatında)',
   'indexFilterable': True,
   'indexSearchable': True,
   'name': 'relationships',
   'tokenization': 'word'}],
 'replicationConfig': {'factor': 1},
 'shardingConfig': {'virtualPerPhysical': 128,
  'desiredCount': 1,
  'actualCount': 1,
  'desiredVirtualCount': 128,
  'actualVirtualCount': 128,
  'key': '_id',
  'strategy': 'hash',
  'function': 'murmur3'},
 'vectorIndexConfig': {'skip': False,
  'cleanupIntervalSeconds': 300,
  'maxConnections': 64,
  'efConstruction': 128,
  'ef': -1,
  'dynamicEfMin': 100,
  'dynamicEfMax': 500,
  'dynamicEfFactor': 8,
  'vectorCacheMaxObjects': 1000000000000,
  'flatSearchCutoff': 40000,
  'distance': 'cosine',
  'pq': {'enabled': False,
   'bitCompression': False,
   'segments': 0,
   'centroids': 256,
   'trainingLimit': 100000,
   'encoder': {'type': 'kmeans', 'distribution': 'log-normal'}}},
 'vectorIndexType': 'hnsw',
 'vectorizer': 'none'}
```

```python
index = VectorStoreIndex(
    [],
    storage_context=storage_context,
    transformations=[splitter],
    callback_manager=callback_manager,
)


# belgeleri dizine ekle
for wiki_title in wiki_titles:
    index.insert(docs_dict[wiki_title])
```

```text
**********
Trace: dizin_olusturma
**********
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: yerlestirme (insert)
**********
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: yerlestirme (insert)
**********
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: yerlestirme (insert)
**********
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: yerlestirme (insert)
**********
```

```python
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo




vector_store_info = VectorStoreInfo(
    content_info="ünlülerin kısa biyografileri",
    metadata_info=[
        MetadataInfo(
            name="category",
            type="str",
            description=(
                "Ünlünün kategorisi, şunlardan biri: [Spor, Eğlence,"
                " İş Dünyası, Müzik]"
            ),
        ),
        MetadataInfo(
            name="country",
            type="str",
            description=(
                "Ünlünün ülkesi, şunlardan biri: [Amerika Birleşik Devletleri, Barbados,"
                " Birleşik Krallık]"
            ),
        ),
    ],
)
retriever = VectorIndexAutoRetriever(
    index,
    vector_store_info=vector_store_info,
    llm=llm,
    callback_manager=callback_manager,
    max_top_k=10000,
)
```

```python
# NOT: "top-k değerini 10000'e ayarlama", tüm verileri döndürmek için bir hiledir.
# Şu anda otomatik erişim her zaman sabit bir top-k döndürecektir, tüm verileri getirmek için
# top-k değerinin None olmasına izin verilmesi için bir TODO bulunmaktadır.
# Yani teorik olarak LLM'nin bir None top-k değeri çıkarsaması mümkündür.
nodes = retriever.retrieve(
    "Amerika Birleşik Devletleri'nden bir ünlü hakkında bilgi ver, en iyi k değerini 10000 yap"
)
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Sorgu dizgisi kullanılıyor: Bir ünlü hakkında bilgi ver
Using query str: Tell me about a celebrity
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Filtreler kullanılıyor: [('ülke', '==', 'Amerika Birleşik Devletleri')]
Using filters: [('country', '==', 'United States')]
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:top_k kullanılıyor: 2
Using top_k: 2
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: sorgu (query)
    |_erişim (retrieve) -> 4.232108 saniye
**********
```

```python
print(f"Düğüm sayısı: {len(nodes)}")
for node in nodes[:10]:
    print(node.node.get_content())
```

```text
Düğüm sayısı: 2
Aralık 2023'te Yargıç Laurel Beeler, Musk'ın SEC için tekrar ifade vermesi gerektiğine karar verdi.

== Toplumsal algı ==

Girişimleri 2000'li yıllarda kendi sektörlerinde etkili olsa da Musk, ancak 2010'ların başında halka açık bir figür haline geldi. İşlerini korumak için inzivaya çekilmeyi tercih eden diğer milyarderlerin aksine, kendiliğinden ve tartışmalı açıklamalar yapan eksantrik biri olarak tanımlandı...
(Metin Elon Musk biyografisinden devam etmektedir)
```

```python
nodes = retriever.retrieve(
    "Amerika Birleşik Devletleri'ndeki popüler bir spor ünlüsünün çocukluğu hakkında bilgi ver"
)
for node in nodes:
    print(node.node.get_content())
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Sorgu dizgisi kullanılıyor: popüler bir spor ünlüsünün çocukluğu
Using query str: childhood of a popular sports celebrity
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Filtreler kullanılıyor: [('category', '==', 'Spor'), ('country', '==', 'Amerika Birleşik Devletleri')]
Using filters: [('category', '==', 'Sports'), ('country', '==', 'United States')]
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:top_k kullanılıyor: 2
Using top_k: 2
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: sorgu (query)
    |_erişim (retrieve) -> 3.546065 saniye
**********
(Michael Jordan biyografisinden ilgili kısımlar gelir)
```

```python
nodes = retriever.retrieve(
    "16 yaşında şirket kuran bir milyarderin üniversite hayatı hakkında bilgi ver"
)
for node in nodes:
    print(node.node.get_content())
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Sorgu dizgisi kullanılıyor: 16 yaşında şirket kuran bir milyarderin üniversite hayatı
Using query str: college life of a billionaire who started at company at the age of 16
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Filtreler kullanılıyor: []
Using filters: []
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:top_k kullanılıyor: 2
Using top_k: 2
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: sorgu (query)
    |_erişim (retrieve) -> 2.60008 saniye
**********
(Richard Branson veya Elon Musk hakkında bilgi gelir)
```

```python
nodes = retriever.retrieve("Birleşik Krallık'tan bir milyarderin çocukluğu hakkında bilgi ver")
for node in nodes:
    print(node.node.get_content())
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Sorgu dizgisi kullanılıyor: Birleşik Krallık'tan bir milyarderin çocukluğu
Using query str: childhood of a UK billionaire
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Filtreler kullanılıyor: [('category', '==', 'İş Dünyası'), ('country', '==', 'Birleşik Krallık')]
Using filters: [('category', '==', 'Business'), ('country', '==', 'United Kingdom')]
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:top_k kullanılıyor: 2
Using top_k: 2
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: sorgu (query)
    |_erişim (retrieve) -> 3.565899 saniye
**********
```

## Belge Özetleri Üzerinden Özyinelemeli Erişimci (Recursive Retriever) Oluşturma

```python
from llama_index.core.schema import IndexNode
```

```python
# üst düzey düğümleri ve vektör erişimcileri tanımla
nodes = []
vector_query_engines = {}
vector_retrievers = {}


for wiki_title in wiki_titles:
    # vektör dizini oluştur
    vector_index = VectorStoreIndex.from_documents(
        [docs_dict[wiki_title]],
        transformations=[splitter],
        callback_manager=callback_manager,
    )
    # sorgu motorlarını tanımla
    vector_query_engine = vector_index.as_query_engine(llm=llm)
    vector_query_engines[wiki_title] = vector_query_engine
    vector_retrievers[wiki_title] = vector_index.as_retriever()


    # özetleri kaydet
    out_path = Path("summaries") / f"{wiki_title}.txt"
    if not out_path.exists():
        # LLM tarafından oluşturulan özeti kullan
        summary_index = SummaryIndex.from_documents(
            [docs_dict[wiki_title]], callback_manager=callback_manager
        )


        summarizer = summary_index.as_query_engine(
            response_mode="tree_summarize", llm=llm
        )
        response = await summarizer.aquery(
            f"{wiki_title} için bir özet hazırla"
        )


        wiki_summary = response.response
        Path("summaries").mkdir(exist_ok=True)
        with open(out_path, "w") as fp:
            fp.write(wiki_summary)
    else:
        with open(out_path, "r") as fp:
            wiki_summary = fp.read()


    print(f"**{wiki_title} için özet: {wiki_summary}")
    node = IndexNode(text=wiki_summary, index_id=wiki_title)
    nodes.append(node)
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: dizin_olusturma
**********
**Michael Jordan için özet: Genellikle MJ olarak anılan Michael Jordan, spor tarihinin en büyük oyuncularından biri olarak kabul edilen, Amerika Birleşik Devletleri'nden emekli bir profesyonel basketbolcudur. NBA'de başta Chicago Bulls olmak üzere 15 sezon oynadı ve altı NBA şampiyonluğu kazandı. Emekli olduktan sonra başarılı bir iş adamı oldu, Charlotte Hornets'ın ortağı ve basketbol operasyonları başkanı ve NASCAR Cup Serisinde 23XI Racing'in sahibi oldu.

**Elon Musk için özet: Elon Musk, çok sayıda yüksek profilli teknoloji şirketini kuran ve yöneten, küresel olarak tanınan bir iş adamı ve yatırımcıdır. SpaceX'in kurucusu ve CEO'su, Tesla, Inc.'in CEO'su ve ürün mimarıdır. Musk ayrıca X Corp'un sahibi ve başkanıdır ve Boring Company'yi kurmuştur. Neuralink ve OpenAI'nin kurucu ortaklarındandır. Ağustos 2023 itibarıyla 200 milyar doları aşan servetiyle dünyanın en zengin insanıdır.

**Richard Branson için özet: 18 Temmuz 1950 doğumlu Richard Branson, İngiliz bir iş adamı, ticari astronot ve hayırseverdir. 1970'lerde havacılık, müzik ve uzay yolculuğu gibi çeşitli alanlarda 400'den fazla şirketi kontrol eden Virgin Group'u kurmuştur. 2000 yılında girişimciliğe hizmetlerinden dolayı şövalyelik unvanı almıştır. Haziran 2023 itibarıyla net serveti 3 milyar ABD dolarıdır.

**Rihanna için özet: Gerçek adı Robyn Rihanna Fenty olan Rihanna, dünyaca ünlü Barbadoslu şarkıcı, söz yazarı, oyuncu ve iş kadınıdır. Dünya çapında 250 milyondan fazla plak satarak tüm zamanların en çok satan müzik sanatçılarından biri olmuştur. Müzik kariyerinin yanı sıra kozmetik markası Fenty Beauty ve moda evi Fenty'yi kurarak iş dünyasına atılmıştır. 2023 itibarıyla 1,4 milyar dolarlık tahmini servetiyle en zengin kadın müzisyendir.
```

```python
# üst düzey erişimciyi tanımla
top_vector_index = VectorStoreIndex(
    nodes, transformations=[splitter], callback_manager=callback_manager
)
top_vector_retriever = top_vector_index.as_retriever(similarity_top_k=1)
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
**********
Trace: dizin_olusturma
**********
```

```python
# özyinelemeli erişimciyi tanımla
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer
```

```python
# not: her ajan bir sorgu motoru olarak kullanılabildiğinden `agents` sözlüğü `query_engine_dict` olarak geçirilebilir
recursive_retriever = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": top_vector_retriever, **vector_retrievers},
    # query_engine_dict=vector_query_engines,
    verbose=True,
)
```

```python
# özyinelemeli erişimciyi çalıştır
nodes = recursive_retriever.retrieve(
    "Amerika Birleşik Devletleri'nden bir ünlü hakkında bilgi ver"
)
for node in nodes:
    print(node.node.get_content())
```

```text
 [1;3;34mSorgu ID'si None ile erişiliyor: Amerika Birleşik Devletleri'nden bir ünlü hakkında bilgi ver
 [0mINFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
 [1;3;38;5;200mID ile düğüme erişildi: Michael Jordan
 [0m [1;3;34mMichael Jordan sorgu ID'si ile erişiliyor: Amerika Birleşik Devletleri'nden bir ünlü hakkında bilgi ver
 [0m [1;3;38;5;200mMetin düğümüne erişiliyor: 1999'da ESPN tarafından yapılan bir ankette Jordan, 20. yüzyılın en büyük Kuzey Amerikalı sporcusu seçildi...
(Jordan hakkında metin parçaları devam eder)
```

```python
nodes = recursive_retriever.retrieve(
    "16 yaşında şirket kuran bir milyarderin çocukluğu hakkında bilgi ver"
)
for node in nodes:
    print(node.node.get_content())
```

```text
 [1;3;34mSorgu ID'si None ile erişiliyor: 16 yaşında şirket kuran bir milyarderin çocukluğu hakkında bilgi ver
 [0mINFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
 [1;3;38;5;200mID ile düğüme erişildi: Richard Branson
 [0m [1;3;34mRichard Branson sorgu ID'si ile erişiliyor: 16 yaşında şirket kuran bir milyarderin çocukluğu hakkında bilgi ver
 [0m [1;3;38;5;200mMetin düğümüne erişiliyor: Buckinghamshire'daki özel bir okul olan Stowe School'a on altı yaşına kadar devam etti. Branson disleksiktir ve akademik performansı düşüktü; okulun son gününde müdürü Robert Drayson ona ya hapse gireceğini ya da milyoner olacağını söylemişti.
 [0m(Metin devam eder)
```
he said.
```
