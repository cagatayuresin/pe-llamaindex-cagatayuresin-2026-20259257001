# Upstash Vector Store

---
title: Upstash Vector Store
 | LlamaIndex OSS Documentation
---

LlamaIndex'i Upstash Vector ile etkileşim kurmak için nasıl kullanacağımıza bakacağız!

```
! pip install -q llama-index upstash-vector
```

```
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.vector_stores import UpstashVectorStore
from llama_index.core import StorageContext
import textwrap
import openai
```

```
# OpenAI API'sini ayarlama
openai.api_key = "sk-..."
```

```
# Veri indirme
! mkdir -p 'data/paul_graham/'
! wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```
--2024-02-03 20:04:25--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 75042 (73K) [text/plain]
Saving to: ‘data/paul_graham/paul_graham_essay.txt’


data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    in 0.01s


2024-02-03 20:04:25 (5.96 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042]
```

Şimdi, LlamaIndex SimpleDirectoryReader'ı kullanarak belgeleri yükleyebiliriz

```
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


print("# Documents:", len(documents))
```

```
# Documents: 1
```

Upstash üzerinde bir indeks oluşturmak için <https://console.upstash.com/vector> adresini ziyaret edin, 1536 boyutlu ve `Cosine` (Kosinüs) mesafe metriğine sahip bir indeks oluşturun. URL'yi ve token'ı aşağıya kopyalayın

```
vector_store = UpstashVectorStore(url="https://...", token="...")


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Şimdi başarıyla bir indeks oluşturduk ve onu makaleden gelen vektörlerle doldurduk! Verilerin indekslenmesi bir saniye sürecek ve ardından sorgulamaya hazır olacak.

```
query_engine = index.as_query_engine()
res1 = query_engine.query("What did the author learn?")
print(textwrap.fill(str(res1), 100))


print("\n")


res2 = query_engine.query("What is the author's opinion on startups?")
print(textwrap.fill(str(res2), 100))
```

```
Yazar, üniversitede felsefe eğitiminin beklentilerini karşılamadığını öğrendi.
Diğer alanların fikirlerin çoğunu kapladığını ve felsefenin keşfetmesi beklenen nihai gerçekler
için çok az yer bıraktığını gördüler. Sonuç olarak, yapay zeka çalışmaya
geçmeye karar verdiler.




Yazarın girişimler (startups) hakkındaki görüşü, özellikle başlangıç aşamalarında yardıma ve
desteğe ihtiyaç duydukları yönündedir. Yazar, girişim kurucularının genellikle çaresiz olduğuna
ve şirketleşmek, bir şirketi yönetmenin inceliklerini anlamak gibi çeşitli zorluklarla karşılaştıklarına inanmaktadır.
Yazarın yatırım şirketi Y Combinator, girişimlere tohum finansmanı ve
kapsamlı destek sağlamayı, onlara başarılı olmaları için ihtiyaç duydukları rehberlik ve kaynakları sunmayı amaçlamaktadır.
```

### Meta Veri Filtreleme

Upstash vektör deposundan döndürülen düğümleri (node) filtrelemek için `VectorStoreQuery`'nizle birlikte `MetadataFilters` geçirebilirsiniz.

```
import os


from llama_index.vector_stores.upstash import UpstashVectorStore
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)


vector_store = UpstashVectorStore(
    url=os.environ.get("UPSTASH_VECTOR_URL") or "",
    token=os.environ.get("UPSTASH_VECTOR_TOKEN") or "",
)


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)


filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="author", value="Marie Curie", operator=FilterOperator.EQ
        )
    ],
)


retriever = index.as_retriever(filters=filters)


retriever.retrieve("What is inception about?")
```

Birden fazla `MetadataFilters`'ı `AND` veya `OR` koşuluyla da birleştirebiliriz

```
from llama_index.core.vector_stores import FilterOperator, FilterCondition


filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="theme",
            value=["Fiction", "Horror"],
            operator=FilterOperator.IN,
        ),
        MetadataFilter(key="year", value=1997, operator=FilterOperator.GT),
    ],
    condition=FilterCondition.AND,
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Harry Potter?")
```
