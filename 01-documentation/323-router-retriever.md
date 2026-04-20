# Yönlendirici Erişici (Router Retriever)

---
title: Yönlendirici Erişici (Router Retriever)
 | LlamaIndex OSS Belgeleri
---

Bu kılavuzda, verilen bir sorguyu yürütmek için bir veya daha fazla aday erişiciyi seçen özel bir yönlendirici erişici (router retriever) tanımlıyoruz.

Yönlendirici (`BaseSelector`) modülü, hangi temel erişim araçlarının kullanılacağına dair kararları dinamik olarak vermek için LLM'yi kullanır. Bu, çok çeşitli veri kaynakları arasından birini seçmek için yararlı olabilir. Ayrıca, çeşitli veri kaynakları genelinde erişim sonuçlarını toplamak için de yararlı olabilir (eğer bir çoklu seçici modülü kullanılırsa).

Bu not defteri, RouterQueryEngine not defterine çok benzer.

### Kurulum (Setup)

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i kurmanız gerekecektir 🦙.

```bash
%pip install llama-index-llms-openai
```

```bash
!pip install llama-index
```

```python
# NOT: Bu YALNIZCA jupyter not defterinde gereklidir.
# Detay: Jupyter perde arkasında bir olay döngüsü (event-loop) çalıştırır.
#        Bu, asenkron sorgular yapmak için bir olay döngüsü başlattığımızda iç içe geçmiş olay döngülerine neden olur.
#        Normalde buna izin verilmez, kolaylık sağlamak için nest_asyncio kullanıyoruz.
import nest_asyncio


nest_asyncio.apply()
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().handlers = []
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    SimpleKeywordTableIndex,
)
from llama_index.core import SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
```

```text
Not: 12 çekirdek algılandı ancak "NUMEXPR_MAX_THREADS" ayarlanmadı, bu nedenle 8 olan güvenli sınır uygulanıyor.
NumExpr varsayılan olarak 8 iş parçacığı (thread) kullanıyor.
```

### Veriyi İndir (Download Data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Veriyi Yükle (Load Data)

Önce bir Belgeyi (Document) bir dizi Düğüme (Node) nasıl dönüştüreceğimizi ve bir Belge Deposuna (DocumentStore) nasıl yerleştireceğimizi gösteriyoruz.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
# LLM + ayırıcıyı (splitter) başlat
llm = OpenAI(model="gpt-4")
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)
```

```python
# depolama bağlamını (storage context) başlat (varsayılan olarak bellek içindedir)
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)
```

```python
# tanımla
summary_index = SummaryIndex(nodes, storage_context=storage_context)
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
keyword_index = SimpleKeywordTableIndex(nodes, storage_context=storage_context)
```

```python
list_retriever = summary_index.as_retriever()
vector_retriever = vector_index.as_retriever()
keyword_retriever = keyword_index.as_retriever()
```

```python
from llama_index.core.tools import RetrieverTool


list_tool = RetrieverTool.from_defaults(
    retriever=list_retriever,
    description=(
        "Paul Graham'ın 'Neler Üzerine Çalıştım' (What I Worked On) hakkındaki denemesinden tüm bağlamı getirir. "
        "Soru yalnızca daha spesifik bir bağlam gerektiriyorsa kullanmayın."
    ),
)
vector_tool = RetrieverTool.from_defaults(
    retriever=vector_retriever,
    description=(
        "Paul Graham'ın 'Neler Üzerine Çalıştım' denemesinden spesifik bağlam getirmek için yararlıdır."
    ),
)
keyword_tool = RetrieverTool.from_defaults(
    retriever=keyword_retriever,
    description=(
        "Paul Graham'ın 'Neler Üzerine Çalıştım' denemesinden spesifik bağlam getirmek için yararlıdır "
        "(sorguda belirtilen varlıkları kullanarak)."
    ),
)
```

### Yönlendirme için Seçici Modülünü Tanımlama (Define Selector Module for Routing)

Her biri bazı farklı özelliklere sahip birkaç seçici mevcuttur.

LLM seçicileri, ayrıştırılan bir JSON çıktısı üretmek için LLM'yi kullanır ve ilgili indeksler sorgulanır.

Pydantic seçicileri (şu anda yalnızca varsayılan olan `gpt-4-0613` ve `gpt-3.5-turbo-0613` tarafından desteklenir), ham JSON'ı ayrıştırmak yerine pydantic seçim nesneleri üretmek için OpenAI Fonksiyon Çağırma (Function Call) API'sini kullanır.

Burada PydanticSingleSelector/PydanticMultiSelector kullanıyoruz ancak isterseniz LLM muadillerini de kullanabilirsiniz.

```python
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector
from llama_index.core.selectors import (
    PydanticMultiSelector,
    PydanticSingleSelector,
)
from llama_index.core.retrievers import RouterRetriever
from llama_index.core.response.notebook_utils import display_source_node
```

#### PydanticSingleSelector (Tekli Seçici)

```python
retriever = RouterRetriever(
    selector=PydanticSingleSelector.from_defaults(llm=llm),
    retriever_tools=[
        list_tool,
        vector_tool,
    ],
)
```

```python
# yazarın hayatıyla ilgili tüm bağlamı getirecektir
nodes = retriever.retrieve(
    "Yazarın hayatıyla ilgili tüm bağlamı bana verebilir misiniz?"
)
for node in nodes:
    display_source_node(node)
```

```text
Selecting retriever 0: Bu seçim, denemeden tüm bağlamın getirilmesinden bahsettiği için en alakalı olanıdır; bu, yazarın hayatı hakkındaki bilgileri de içerebilir..
```

**Düğüm Kimliği (Node ID):** 7d07d325-489e-4157-a745-270e2066a643\
**Benzerlik:** None\
**Metin:** What I Worked On

February 2021

Before college the two main things I worked on, outside of schoo…

**Düğüm Kimliği (Node ID):** 01f0900b-db83-450b-a088-0473f16882d7\
**Benzerlik:** None\
**Metin:** showed Terry Winograd using SHRDLU. I haven’t tried rereading The Moon is a Harsh Mistress, so I …

**Düğüm Kimliği (Node ID):** b2549a68-5fef-4179-b027-620ebfa6e346\
**Benzerlik:** None\
**Metin:** Science is an uneasy alliance between two halves, theory and systems. The theory people prove thi…

**Düğüm Kimliği (Node ID):** 4f1e9f0d-9bc6-4169-b3b6-4f169bbfa391\
**Benzerlik:** None\
**Metin:** been explored. But all I wanted was to get out of grad school, and my rapidly written dissertatio…

**Düğüm Kimliği (Node ID):** e20c99f9-5e80-4c92-8cc0-03d2a527131e\
**Benzerlik:** None\
**Metin:** stop there, of course, or you get merely photographic accuracy, and what makes a still life inter…

**Düğüm Kimliği (Node ID):** dbdf341a-f340-49f9-961f-16b9a51eea2d\
**Benzerlik:** None\
**Metin:** that big, bureaucratic customers are a dangerous source of money, and that there’s not much overl…

**Düğüm Kimliği (Node ID):** ed341d3a-9dda-49c1-8611-0ab40d04f08a\
**Benzerlik:** None\
**Metin:** about money, because I could sense that Interleaf was on the way down. Freelance Lisp hacking wor…

**Düğüm Kimliği (Node ID):** d69e02d3-2732-4567-a360-893c14ae157b\
**Benzerlik:** None\
**Metin:** a web app, is common now, but at the time it wasn’t clear that it was even possible. To find out,…

**Düğüm Kimliği (Node ID):** df9e00a5-e795-40a1-9a6b-8184d1b1e7c0\
**Benzerlik:** None\
**Metin:** have to integrate with any other software except Robert’s and Trevor’s, so it was quite fun to wo…

**Düğüm Kimliği (Node ID):** 38f2699b-0878-499b-90ee-821cb77e387b\
**Benzerlik:** None\
**Metin:** all too keenly aware of the near-death experiences we seemed to have every few months. Nor had I …

**Düğüm Kimliği (Node ID):** be04d6a9-1fc7-4209-9df2-9c17a453699a\
**Benzerlik:** None\
**Metin:** for a second still life, painted from the same objects (which hopefully hadn’t rotted yet).

Mean…

**Düğüm Kimliği (Node ID):** 42344911-8a7c-4e9b-81a8-0fcf40ab7690\
**Benzerlik:** None\
**Metin:** which I’d created years before using Viaweb but had never used for anything. In one day it got 30…

**Düğüm Kimliği (Node ID):** 9ec3df49-abf9-47f4-b0c2-16687882742a\
**Benzerlik:** None\
**Metin:** I didn’t know but would turn out to like a lot: a woman called Jessica Livingston. A couple days …

**Düğüm Kimliği (Node ID):** d0cf6975-5261-4fb2-aae3-f3230090fb64\
**Benzerlik:** None\
**Metin:** of readers, but professional investors are thinking “Wow, that means they got all the returns.” B…

**Düğüm Kimliği (Node ID):** 607d0480-7eee-4fb4-965d-3cb585fda62c\
**Benzerlik:** None\
**Metin:** to the “YC GDP,” but as YC grows this becomes less and less of a joke. Now lots of startups get t…

**Düğüm Kimliği (Node ID):** 730a49c9-55f7-4416-ab91-1d0c96e704c8\
**Benzerlik:** None\
**Metin:** So this set me thinking. It was true that on my current trajectory, YC would be the last thing I …

**Düğüm Kimliği (Node ID):** edbe8c67-e373-42bf-af98-276b559cc08b\
**Benzerlik:** None\
**Metin:** operators you need? The Lisp that John McCarthy invented, or more accurately discovered, is an an…

**Düğüm Kimliği (Node ID):** 175a4375-35ec-45a0-a90c-15611505096b\
**Benzerlik:** None\
**Metin:** Like McCarthy’s original Lisp, it’s a spec rather than an implementation, although like McCarthy’…

**Düğüm Kimliği (Node ID):** 0cb367f9-0aac-422b-9243-0eaa7be15090\
**Benzerlik:** None\
**Metin:** must tell readers things they don’t already know, and some people dislike being told such things…

**Düğüm Kimliği (Node ID):** 67afd4f1-9fa1-4e76-87ac-23b115823e6c\
**Benzerlik:** None\
**Metin:** 1960 paper.

But if so there’s no reason to suppose that this is the limit of the language that m…

```python
nodes = retriever.retrieve("Paul Graham, RISD'den sonra ne yaptı?")
for node in nodes:
    display_source_node(node)
```

```text
Selecting retriever 1: Soru, Paul Graham'ın 'Neler Üzerine Çalıştım' başlıklı denemesinden spesifik bir ayrıntı istiyor. Bu nedenle, spesifik bağlam getirmek için yararlı olan ikinci seçenek en alakalı olanıdır..
```

**Düğüm Kimliği (Node ID):** 22d20835-7de6-4cf7-92de-2bee339f3157\
**Benzerlik:** 0.8017176790752668\
**Metin:** that big, bureaucratic customers are a dangerous source of money, and that there’s not much overl…

**Düğüm Kimliği (Node ID):** bf818c58-5d5b-4458-acbc-d87cc67a36ca\
**Benzerlik:** 0.7935885352785799\
**Metin:** So this set me thinking. It was true that on my current trajectory, YC would be the last thing I …

#### PydanticMultiSelector (Çoklu Seçici)

```python
retriever = RouterRetriever(
    selector=PydanticMultiSelector.from_defaults(llm=llm),
    retriever_tools=[list_tool, vector_tool, keyword_tool],
)
```

```python
nodes = retriever.retrieve(
    "Yazarın Interleaf ve YC'deki zamanından kayda değer olaylar nelerdi?"
)
for node in nodes:
    display_source_node(node)
```

```text
Selecting retriever 1: Bu seçim, Interleaf ve YC'deki kayda değer olaylar hakkındaki soruyu yanıtlamak için gereken denemeden spesifik bağlamın getirilmesine olanak tanıdığı için alakalıdır..
Selecting retriever 2: Bu seçim, sorguda belirtilen 'Interleaf' ve 'YC' varlıklarını kullanarak spesifik bağlamın getirilmesine olanak tanıdığı için de alakalıdır..
> Sorgu başlatılıyor: Yazarın Interleaf ve YC'deki zamanından kayda değer olaylar nelerdi?
sorgu anahtar kelimeleri: ['interleaf', 'olaylar', 'kayda', 'değer', 'yc']
> Ayıklanan anahtar kelimeler: ['interleaf', 'yc']
```

**Düğüm Kimliği (Node ID):** fbdd25ed-1ecb-4528-88da-34f581c30782\
**Benzerlik:** None\
**Metin:** So this set me thinking. It was true that on my current trajectory, YC would be the last thing I …

**Düğüm Kimliği (Node ID):** 4ce91b17-131f-4155-b7b5-8917cdc612b1\
**Benzerlik:** None\
**Metin:** to the “YC GDP,” but as YC grows this becomes less and less of a joke. Now lots of startups get t…

**Düğüm Kimliği (Node ID):** 9fe6c152-28d4-4006-8a1a-43bb72655438\
**Benzerlik:** None\
**Metin:** stop there, of course, or you get merely photographic accuracy, and what makes a still life inter…

**Düğüm Kimliği (Node ID):** d11cd2e2-1dd2-4c3b-863f-246fe3856f49\
**Benzerlik:** None\
**Metin:** of readers, but professional investors are thinking “Wow, that means they got all the returns.” B…

**Düğüm Kimliği (Node ID):** 2bfbab04-cb71-4641-9bd9-52c75b3a9250\
**Benzerlik:** None\
**Metin:** must tell readers things they don’t already know, and some people dislike being told such things…

```python
nodes = retriever.retrieve(
    "Yazarın Interleaf ve YC'deki zamanından kayda değer olaylar nelerdi?"
)
for node in nodes:
    display_source_node(node)
```

```text
Selecting retriever 1: Bu seçim, Interleaf ve YC'deki kayda değer olaylar hakkındaki soruyu yanıtlamak için gereken denemeden spesifik bağlamın getirilmesine olanak tanıdığı için alakalıdır..
Selecting retriever 2: Bu seçim, sorguda belirtilen 'Interleaf' ve 'YC' varlıklarını kullanarak spesifik bağlamın getirilmesine olanak tanıdığı için de alakalıdır..
> Sorgu başlatılıyor: Yazarın Interleaf ve YC'deki zamanından kayda değer olaylar nelerdi?
sorgu anahtar kelimeleri: ['interleaf', 'yc', 'olaylar', 'kayda', 'değer']
> Ayıklanan anahtar kelimeler: ['interleaf', 'yc']
```

**Düğüm Kimliği (Node ID):** 49882a2c-bb95-4ff3-9df1-2a40ddaea408\
**Benzerlik:** None\
**Metin:** So this set me thinking. It was true that on my current trajectory, YC would be the last thing I …

**Düğüm Kimliği (Node ID):** d11aced1-e630-4109-8ec8-194e975b9851\
**Benzerlik:** None\
**Metin:** to the “YC GDP,” but as YC grows this becomes less and less of a joke. Now lots of startups get t…

**Düğüm Kimliği (Node ID):** 8aa6cc91-8e9c-4470-b6d5-4360ed13fefd\
**Benzerlik:** None\
**Metin:** stop there, of course, or you get merely photographic accuracy, and what makes a still life inter…

**Düğüm Kimliği (Node ID):** e37465de-c79a-4714-a402-fbd5f52800a2\
**Benzerlik:** None\
**Metin:** must tell readers things they don’t already know, and some people dislike being told such things…

**Düğüm Kimliği (Node ID):** e0ac7fb6-84fc-4763-bca6-b68f300ec7b7\
**Benzerlik:** None\
**Metin:** of readers, but professional investors are thinking “Wow, that means they got all the returns.” B…

```python
nodes = await retriever.aretrieve(
    "Yazarın Interleaf ve YC'deki zamanından kayda değer olaylar nelerdi?"
)
for node in nodes:
    display_source_node(node)
```

```text
Selecting retriever 1: Bu seçim, Interleaf ve YC'deki kayda değer olaylar hakkındaki soruyu yanıtlamak için gereken denemeden spesifik bağlamın getirilmesine olanak tanıdığı için alakalıdır..
Selecting retriever 2: Bu seçim, sorguda belirtilen 'Interleaf' ve 'YC' varlıklarını kullanarak spesifik bağlamın getirilmesine olanak tanıdığı için de alakalıdır..
> Sorgu başlatılıyor: Yazarın Interleaf ve YC'deki zamanından kayda değer olaylar nelerdi?
sorgu anahtar kelimeleri: ['olaylar', 'interleaf', 'yc', 'kayda', 'değer']
> Ayıklanan anahtar kelimeler: ['interleaf', 'yc']
message='OpenAI API response' path=https://api.openai.com/v1/embeddings processing_ms=25 request_id=95c73e9360e6473daab85cde93ca4c42 response_code=200
```

**Düğüm Kimliği (Node ID):** 76d76348-52fb-49e6-95b8-2f7a3900fa1a\
**Benzerlik:** None\
**Metin:** So this set me thinking. It was true that on my current trajectory, YC would be the last thing I …

**Düğüm Kimliği (Node ID):** 61e1908a-79d2-426b-840e-926df469ac49\
**Benzerlik:** None\
**Metin:** to the “YC GDP,” but as YC grows this becomes less and less of a joke. Now lots of startups get t…

**Düğüm Kimliği (Node ID):** cac03004-5c02-4145-8e92-c320b1803847\
**Benzerlik:** None\
**Metin:** stop there, of course, or you get merely photographic accuracy, and what makes a still life inter…

**Düğüm Kimliği (Node ID):** f0d55e5e-5349-4243-ab01-d9dd7b12cd0a\
**Benzerlik:** None\
**Metin:** of readers, but professional investors are thinking “Wow, that means they got all the returns.” B…

**Düğüm Kimliği (Node ID):** 1516923c-0dee-4af2-b042-3e1f38de7e86\
**Benzerlik:** None\
**Metin:** must tell readers things they don’t already know, and some people dislike being told such things…
