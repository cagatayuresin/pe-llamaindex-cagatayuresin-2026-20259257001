---
title: OceanBase Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# OceanBase Vektör Deposu

> [OceanBase Veritabanı](https://github.com/oceanbase/oceanbase), dağıtık bir ilişkisel veritabanıdır. Tamamen Ant Group tarafından geliştirilmiştir. OceanBase Veritabanı, ortak bir sunucu kümesi üzerine inşa edilmiştir. Paxos protokolü ve dağıtık yapısı sayesinde yüksek kullanılabilirlik ve doğrusal ölçeklenebilirlik sağlar. Belirli donanım mimarilerine bağımlı değildir.

Bu not defteri, LlamaIndex'te OceanBase vektör deposu işlevselliğinin nasıl kullanılacağını ayrıntılı olarak açıklamaktadır.

#### Kurulum

```bash
%pip install llama-index-vector-stores-oceanbase
%pip install llama-index
# Gömme ve LLM modeli olarak dashscope'u seçin; test etmek için varsayılan openai veya diğer modelleri de kullanabilirsiniz
%pip install llama-index-embeddings-dashscope
%pip install llama-index-llms-dashscope
```

#### Docker ile Bağımsız (Standalone) Bir OceanBase Sunucusu Dağıtın

```bash
%docker run --name=ob433 -e MODE=slim -p 2881:2881 -d oceanbase/oceanbase-ce:4.3.3.0-100000142024101215
```

#### ObVecClient Oluşturma

```python
from pyobvector import ObVecClient


client = ObVecClient()
client.perform_raw_text_sql(
    "ALTER SYSTEM ob_vector_memory_limit_percentage = 30"
)
```

DashScope gömme modelini ve LLM'yi yapılandırın.

```python
# Gömme modelini ayarla
import os
from llama_index.core import Settings
from llama_index.embeddings.dashscope import DashScopeEmbedding


# Küresel Ayarlar
Settings.embed_model = DashScopeEmbedding()


# LLM modelini yapılandır
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels


dashscope_llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_MAX,
    api_key=os.environ.get("DASHSCOPE_API_KEY", ""),
)
```

#### Belgeleri Yükleme

```python
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.oceanbase import OceanBaseVectorStore
```

Veriyi İndirme ve Yükleme

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
oceanbase = OceanBaseVectorStore(
    client=client,
    dim=1536,
    drop_old=True,
    normalize=True,
)


storage_context = StorageContext.from_defaults(vector_store=oceanbase)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

```python
# daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine(llm=dashscope_llm)
res = query_engine.query("Yazar büyürken neler yaptı?")
print(res.response)
```

**"Yazar büyürken okul dışında iki ana aktivite üzerinde çalıştı: yazma ve programlama. Özellikle olay örgüsünden yoksun ama güçlü duygulara sahip karakterler içeren kısa öyküler yazdı. Ayrıca genç yaşta, başlangıçta bir IBM 1401 bilgisayarında Fortran'ın erken bir sürümünü kullanarak programlamaya başladı; ancak delikli kart girişinin sınırlamaları ve işlenecek veri eksikliği nedeniyle bunu zorlayıcı buldu. Programlama yolculuğu, mikro bilgisayarların erişilebilir hale gelmesiyle gerçekten hız kazandı ve oyunlar, bir roket uçuş tahmincisi ve basit bir kelime işlemci gibi daha etkileşimli programlar yazmasına olanak tanıdı."**

#### Meta Veri Filtreleme

OceanBase Vektör Deposu, sorgu sırasında `=`, `>`, `<`, `!=`, `>=`, `<=`, `in`, `not in`, `like`, `IS NULL` formundaki meta veri filtrelemeyi destekler.

```python
from llama_index.core.vector_stores import (
    MetadataFilters,
    MetadataFilter,
)


query_engine = index.as_query_engine(
    llm=dashscope_llm,
    filters=MetadataFilters(
        filters=[
            MetadataFilter(key="book", value="paul_graham", operator="!="),
        ]
    ),
    similarity_top_k=10,
)


res = query_engine.query("Yazar ne öğrendi?")
print(res.response)
```

**'Empty Response' (Boş Yanıt)**

#### Belgeleri Silme

```python
oceanbase.delete(documents[0].doc_id)


query_engine = index.as_query_engine(llm=dashscope_llm)
res = query_engine.query("Yazar büyürken neler yaptı?")
print(res.response)
```

**'Empty Response' (Boş Yanıt)**
