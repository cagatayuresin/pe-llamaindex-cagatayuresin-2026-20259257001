# LlamaIndex ile Vektör Deposu Olarak ApertureDB

---
title: LlamaIndex ile Vektör Deposu Olarak ApertureDB
 | LlamaIndex OSS Belgeleri
---

**Not: Bu örnek, bir ApertureDB örneğine (instance) erişiminiz olduğunu ve geçerli bir APERTUREDB_KEY anahtarınızın bulunduğunu varsayar. [Ücretsiz bir hesap](https://cloud.aperturedata.io/) için kaydolun veya [yerel kurulum](https://docs.aperturedata.io/Setup/server/Local) yapmayı düşünün.**

Bu not defteri, ApertureDB'nin LlamaIndex çerçevesi içinde bir vektör deposu olarak kullanılmasına ve anlamsal arama (semantic search) yapılmasına yönelik örnekler içermektedir.

### Bağımlılıkları pip ile kurun

```bash
%pip install llama-index llama-index-llms-openai llama-index-embeddings-openai llama-index-vector-stores-ApertureDB
```

### Veriyi indirin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Bağımlılıkları içe aktarın

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext


from llama_index.core.vector_stores import MetadataFilters
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.vector_stores.ApertureDB import ApertureDBVectorStore
from llama_index.core import Document


import logging


logging.basicConfig(level=logging.ERROR)
```

### ApertureDBVectorStore Oluşturun

```python
adb_vector_store = ApertureDBVectorStore(dimensions=1536)
```

### Veriyi Vektör Deposuna ekleyin.

Bu işlem sadece bir kez yapılmalıdır; oluşturulan gömmeler (embeddings) ve metaveriler tekrar tekrar sorgulanabilir.

```python
storage_context = StorageContext.from_defaults(
    vector_store=adb_vector_store, graph_store=SimpleGraphStore()
)


documents: Document = SimpleDirectoryReader("./data/paul_graham/").load_data()
index: VectorStoreIndex = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### Vektör Deposunu saf Anlamsal arama ile sorgulayın.

```python
index = VectorStoreIndex.from_vector_store(vector_store=adb_vector_store)


query_engine = index.as_query_engine()




def run_queries(query_engine):
    query_str = [
        "Yazar büyürken neler yaptı?",
        "Yazar Viaweb'deki zamanından sonra ne yaptı?",
    ]
    for qs in query_str:
        response = query_engine.query(qs)
        print(f"Sorgu: {qs}")
        print(f"Yanıt: {response.response}")
        print("===" * 20)




run_queries(query_engine)
```

```text
Sorgu='Yazar büyürken neler yaptı?'
Yanıt='Yazar üniversiteden önce yazma ve programlama üzerine çalıştı.'
============================================================
Sorgu='Yazar Viaweb'deki zamanından sonra ne yaptı?'
Yanıt='Viaweb'deki zamanından sonra yazar, web uygulamalarıyla ilgili yeni bir proje üzerinde çalışmaya başladı. Web uygulamaları yapmak için bir web uygulaması oluşturma fikrine sahipti ve bu yeni girişime başlamak için Cambridge'e taşınmaya karar verdi. Başlangıçta Aspra adında bir şirket kurmayı planlasa da, sonunda odak noktasını değiştirdi ve projenin açık kaynaklı bir proje olarak yapılabilecek bir alt kümesi üzerinde çalışmaya karar verdi. Bu durum, onu ve meslektaşını Cambridge'de satın aldığı bir evde üzerinde çalışmaya başladıkları Arc adlı yeni bir Lisp lehçesi üzerinde çalışmaya yöneltti.'
============================================================
```

## Filtreleme ile arama

Metaveriye dayalı bir filtre belirtmenin gerekli olduğu durumlar olabilir; bu durum LLM için daha doğru bir bağlam sağlar. LlamaIndex, Doğal Dil tabanlı sorguya ek olarak uygulanacak koşulları belirtmenize olanak tanır.

### Özel metaverilerle belgeler ekleyin

Burada, sorgulama sırasında kullanılacak bazı önemli metaverilere sahip belgeler ekliyoruz.

```python
# Farklı bir tanımlayıcı kümesiyle (descriptor set) vektör deposunun başka bir örneğini oluşturun
adb_filterable_vector_store = ApertureDBVectorStore(
    dimensions=1536, descriptor_set="filterbale_embeddings"
)


# Filtrelenebilir vektör deposu ile yeni bir depolama bağlamı oluşturun
storage_context = StorageContext.from_defaults(
    vector_store=adb_filterable_vector_store, graph_store=SimpleGraphStore()
)


# Yeni bir indeks oluşturuyoruz.
documents = [
    Document(
        text="Van Halen grubu 1973'te kuruldu. Grup, Van Halen kardeşler Eddie Van Halen ve Alex Van Halen'ın adını almıştır. Ayrıca"
        " üçüncü bir üyeleri, ana vokalist David Lee Roth ve basta Michael Anthony vardı. Grup, enerjik performansları ve yenilikçi gitar çalışmalarıyla biliniyordu.",
        metadata={"members_start_year": 1974, "members_end_year": 1985},
    ),
    Document(
        text="Roth, solo kariyer yapmak için 1985'te gruptan ayrıldı. Yerine, daha önce Montrose grubunun ana vokalisti olan Sammy Hagar geldi. Hagar'ın"
        " Van Halen ile ilk albümü 5150, 1986'da yayınlandı ve ticari bir başarı yakaladı. Grup, 1980'lerin sonu ve 1990'ların başı boyunca başarılı albümler yayınlamaya devam etti.",
        metadata={"members_start_year": 1985, "members_end_year": 1996},
    ),
    Document(
        text="Eski Extreme vokalisti Gary Cherone, 1996'da Hagar'ın yerini aldı. Grup, 1998'de Van Halen III albümünü yayınladı ve bu albüm önceki albümleri kadar başarılı olmadı. Cherone 1999'da gruptan ayrıldı.",
        metadata={"members_start_year": 1996, "members_end_year": 1999},
    ),
]


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### Filtreli sorgu motoru.

Önceden uygulanan metaverilere dayanarak, buradaki sorgular Vektör Deposundaki ilgili DB sorgularına dönüştürülen ekstra filtrelemeler çalıştırır.

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    FilterOperator,
    FilterCondition,
)


adb_filterable_vector_store = ApertureDBVectorStore(
    dimensions=1536, descriptor_set="filterbale_embeddings"
)


index = VectorStoreIndex.from_vector_store(
    vector_store=adb_filterable_vector_store
)


year_ranges = [(1974, 1985), (1985, 1996), (1996, 1999)]
for start_year, end_year in year_ranges:
    filters = MetadataFilters(
        filters=[
            MetadataFilter(
                key="members_start_year",
                value=end_year - 1,
                operator=FilterOperator.LT,
            )
        ],
        condition=FilterCondition.AND,
    )


    query_engine = index.as_query_engine(filters=filters, similarity_top_k=3)
    response = query_engine.query(
        "Van Halen üyeleri kimlerdi? Sadece isimlerini listeleyin."
    )


    print(f"Yanıt: {response.response}, Kaynak Düğüm Sayısı: {len(response.source_nodes)}")
    for i, source_node in enumerate(response.source_nodes):
        print(f"İndeks={i}, Kaynak Düğüm={source_node}")
```
