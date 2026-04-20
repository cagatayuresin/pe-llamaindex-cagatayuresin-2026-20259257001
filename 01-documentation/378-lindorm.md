---
title: Lindorm
 | LlamaIndex OSS Belgeleri
---

# Lindorm

> [Lindorm](https://www.alibabacloud.com/help/en/lindorm), bulutta yerel (cloud-native) çok modelli bir veritabanı servisidir. Her boyuttaki veriyi depolamanıza olanak tanır. Lindorm, büyük miktarda verinin düşük maliyetle depolanmasını ve işlenmesini ve kullandıkça öde (pay-as-you-go) faturalandırma yöntemini destekler. Apache HBase, Apache Cassandra, Apache Phoenix, OpenTSDB, Apache Solr ve SQL gibi birden fazla açık kaynaklı yazılımın açık standartlarıyla uyumludur.

Bu not defterini çalıştırmak için bulutta çalışan bir Lindorm örneğine (instance) ihtiyacınız vardır. [Bu bağlantıyı](https://alibabacloud.com/help/en/lindorm/latest/create-an-instance) takip ederek bir tane edinebilirsiniz.

Örneği oluşturduktan sonra, örnek [bilgilerinizi](https://www.alibabacloud.com/help/en/lindorm/latest/view-endpoints) alabilir ve LindormSearch'e bağlanmak ve kullanmak için [curl komutlarını](https://www.alibabacloud.com/help/en/lindorm/latest/connect-and-use-the-search-engine-with-the-curl-command) çalıştırabilirsiniz.

## Kurulum

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen `llama-index` kurulu olduğundan emin olmanız gerekecektir:

```bash
!pip install llama-index
```

```bash
!pip install opensearch-py
```

```bash
%pip install llama-index-vector-stores-lindorm
```

```bash
# Gömme (embedding) ve LLM modeli olarak dashscope'u seçin, varsayılan openai veya diğer modelleri de test etmek için kullanabilirsiniz
%pip install llama-index-embeddings-dashscope
%pip install llama-index-llms-dashscope
```

Gerekli paket bağımlılıklarını içe aktarın:

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.lindorm import (
    LindormVectorStore,
    LindormVectorClient,
)
from llama_index.core import VectorStoreIndex, StorageContext
```

Dashscope gömme ve LLM modelini yapılandırın, ayrıca varsayılan openai veya diğer modelleri de test etmek için kullanabilirsiniz

```python
# Gömme (Embedding) modelini ayarla
from llama_index.core import Settings
from llama_index.embeddings.dashscope import DashScopeEmbedding


# Küresel Ayarlar (Global Settings)
Settings.embed_model = DashScopeEmbedding()
```

```python
# llm modelini yapılandır
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels


dashscope_llm = DashScope(model_name=DashScopeGenerationModels.QWEN_MAX)
```

## Örnek veriyi indir:

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Veriyi Yükle:

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge: {len(documents)}")
print(f"İlk belge, id: {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    "İlk belge, metin"
    f" ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

## Lindorm Vektör Deposu nesnesini oluşturun:

```python
# sadece jupyter notebook için
import nest_asyncio


nest_asyncio.apply()


# lindorm örnek bilgileri
host = "ld-bp******jm*******-proxy-search-pub.lindorm.aliyuncs.com"
port = 30070
username = "kullanici_adiniz"
password = "sifreniz"




# VectorStore uygulamasını (impl) gösteren indeks
index_name = "lindorm_rag_test"


# lindorm aramasının uzantı parametresi, sorgulanacak küme birimi sayısı; 1 ile method.parameters.nlist (ivfpq parametresi) arasında olmalıdır; varsayılan değer yoktur.
nprobe = "2"


# lindorm aramasının uzantı parametresi, genellikle geri çağırma (recall) doğruluğunu artırmak için kullanılır, ancak performans yükünü artırır; 1 ile 200 arasında olmalıdır; varsayılan: 10.
reorder_factor = "10"


# LindormVectorClient, vektör araması etkinleştirilmiş tek bir indeks için mantığı kapsüller
client = LindormVectorClient(
    host,
    port,
    username,
    password,
    index=index_name,
    dimension=1536,  # gömme modelinizin boyutuyla eşleşmelidir
    nprobe=nprobe,
    reorder_factor=reorder_factor,
    # filter_type="pre_filter/post_filter(default)"
)


# vektör deposunu başlat
vector_store = LindormVectorStore(client)
```

## Belgelerden İndeksi Oluşturun:

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# örnek verilerimizi ve az önce oluşturduğumuz istemciyi kullanarak bir indeks başlatın
index = VectorStoreIndex.from_documents(
    documents=documents, storage_context=storage_context, show_progress=True
)
```

## Depoyu Sorgulama:

### Arama Testi

```python
# Erişiciyi (Retriever) Ayarla
vector_retriever = index.as_retriever()
# arama yap
source_nodes = vector_retriever.retrieve("Yazar büyürken neler yaptı?")
# kaynak düğümleri kontrol et
for node in source_nodes:
    # print(node.metadata)
    print(f"---------------------------------------------")
    print(f"Skor: {node.score:.3f}")
    print(node.get_content())
    print(f"---------------------------------------------\n\n")
```

### Temel Sorgulama

```python
# sorguyu çalıştır
query_engine = index.as_query_engine(llm=dashscope_llm)
# query_engine = index.as_query_engine()
res = query_engine.query("Yazar büyürken neler yaptı?")
res.response
```

**"Yazar büyürken, okul dışında iki ana aktivite üzerinde çalıştı: yazarlık ve programlama. Makaleler yerine kısa hikayeler yazdı ve erken programlama girişimleri, sınırlı girdi yöntemlerinin ve karmaşık matematiksel bilgi eksikliğinin getirdiği zorluklara rağmen Fortran diliyle bir IBM 1401 bilgisayar kullanmayı içeriyordu."**

### Meta Veri Filtreleme

Lindorm Vektör Deposu artık sorgu zamanında tam eşleşme `anahtar=değer` çiftleri ve `>`, `<`, `>=`, `<=` şeklindeki aralık filtreleri biçiminde meta veri filtrelemeyi desteklemektedir.

```python
from llama_index.core import Document
from llama_index.core.vector_stores import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator,
    FilterCondition,
)
import regex as re
```

```python
# Metni paragraflara ayırın.
text_chunks = documents[0].text.split("\n\n")


# Her dipnot için bir belge oluşturun
footnotes = [
    Document(
        text=chunk,
        id=documents[0].doc_id,
        metadata={
            "is_footnote": bool(re.search(r"^\s*\[\d+\]\s*", chunk)),
            "mark_id": i,
        },
    )
    for i, chunk in enumerate(text_chunks)
    if bool(re.search(r"^\s*\[\d+\]\s*", chunk))
]
```

```python
# Dipnotları indekse ekleyin
for f in footnotes:
    index.insert(f)
```

```python
retriever = index.as_retriever(
    filters=MetadataFilters(
        filters=[
            MetadataFilter(
                key="is_footnote", value="true", operator=FilterOperator.EQ
            ),
            MetadataFilter(
                key="mark_id", value=0, operator=FilterOperator.GTE
            ),
        ],
        condition=FilterCondition.AND,
    ),
)


result = retriever.retrieve("Yazar uzaylılar ve lisp hakkında ne dedi?")


print(result)
```

```python
# Sadece belirli dipnotları arayan bir sorgu motoru oluşturun.
footnote_query_engine = index.as_query_engine(
    filters=MetadataFilters(
        filters=[
            MetadataFilter(
                key="is_footnote", value="true", operator=FilterOperator.EQ
            ),
            MetadataFilter(
                key="mark_id", value=0, operator=FilterOperator.GTE
            ),
        ],
        condition=FilterCondition.AND,
    ),
    llm=dashscope_llm,
)


res = footnote_query_engine.query(
    "Yazar uzaylılar ve lisp hakkında ne dedi?"
)
res.response
```

**"Yazar, yeterince gelişmiş herhangi bir uzaylı medeniyetinin Pisagor teoremi gibi temel matematiksel kavramlardan haberdar olacağını ve daha az kesinlikle de olsa McCarthy'nin 1960 tarihli makalesinde açıklanan Lisp diline de aşina olacaklarını öne sürüyor."**

### Hibrit Arama (Hybrid Search)

Lindorm araması hibrit aramayı destekler; sorgu dizesinin minimum arama ayrıntı seviyesinin bir belirteç (token) olduğuna dikkat edin.

```python
from llama_index.core.vector_stores.types import VectorStoreQueryMode


retriever = index.as_retriever(
    vector_store_query_mode=VectorStoreQueryMode.HYBRID
)


result = retriever.retrieve("Yazar uzaylılar ve lisp hakkında ne dedi?")


print(result)
```

```python
query_engine = index.as_query_engine(
    llm=dashscope_llm, vector_store_query_mode=VectorStoreQueryMode.HYBRID
)
res = query_engine.query("Yazar uzaylılar ve lisp hakkında ne dedi?")
res.response
```

**"Yazar, yeterince gelişmiş herhangi bir uzaylı medeniyetinin Pisagor teoremi gibi temel matematiksel kavramları bileceğine inanıyor. Ayrıca, biraz daha az kesinlik taşısa da, bu uzaylıların McCarthy'nin 1960 tarihli makalesinde tartışılan bir programlama dili olan Lisp'e aşina olacakları fikrini ifade ediyor. Bu düşünce deneyi, icat edilen ve keşfedilen fikirler arasındaki ayrımı keşfetmenin bir yolu olarak hizmet ediyor."**
