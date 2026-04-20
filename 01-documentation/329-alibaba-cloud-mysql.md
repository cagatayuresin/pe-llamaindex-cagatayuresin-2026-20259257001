# Alibaba Cloud MySQL

---
title: Alibaba Cloud MySQL
 | LlamaIndex OSS Belgeleri
---

> Alibaba Cloud MySQL, [ApsaraDB RDS for MySQL](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/overview-3) olarak da adlandırılır. ApsaraDB RDS for MySQL, MySQL kaynak kodunun bir dalına (branch) dayanan ve yüksek performans sunan çevrimiçi bir veritabanı hizmetidir. ApsaraDB RDS for MySQL, Double 11 (Bekarlar Günü) sırasında büyük hacimli eşzamanlı trafiği yönetmiş olan kanıtlanmış bir çözümdür. ApsaraDB RDS for MySQL; beyaz liste (whitelist) yapılandırması, yedekleme ve kurtarma, Şeffaf Veri Şifreleme (TDE), veri taşıma ve örnek (instance), hesap ve veritabanı yönetimi gibi temel özellikler sunar. Daha fazla bilgi için bkz. [RDS MySQL Özelliklerine Genel Bakış](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/features).

Bu not defterini çalıştırmak için bulutta çalışan bir ApsaraDB RDS MySQL örneğine sahip olmanız, bir hesap oluşturmanız ve gerekli veritabanlarını oluşturmanız gerekir. [Bu bağlantıya](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases) başvurabilirsiniz.

Bu not defterinde, ApsaraDB RDS MySQL örneğinizde `llama_index_test` ve `llama_index_meta_test` adında veritabanları oluşturmamız gerekiyor.

## Kurulum (Setup)

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen `llama-index`in kurulu olduğundan emin olmanız gerekecektir:

```bash
!pip install llama-index
```

```bash
%pip install llama-index-vector-stores-alibabacloud-mysql
```

```bash
# gömme (embedding) ve llm modeli olarak dashscope'u seçin; test etmek için varsayılan openai veya diğer modelleri de kullanabilirsiniz
%pip install llama-index-embeddings-dashscope
%pip install llama-index-llms-dashscope
```

Dashscope gömme ve llm modelini yapılandırın; test etmek için varsayılan openai veya diğer modelleri de kullanabilirsiniz. Dashscope modelini kullanmayı seçerseniz, API anahtarınızı [buradan](https://modelstudio.console.aliyun.com/?tab=dashboard#/api-key) alabilir ve aşağıdaki kodda ayarlayabilirsiniz:

```bash
!export DASHSCOPE_API_KEY="api_anahtarınız"
```

## Örnek Veriyi İndir (Download example data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Alibaba Cloud MySQL kullanarak RAG Demosu (RAG Demo using Alibaba Cloud MySQL)

### Basit Sorgu (Simple Query)

#### Basit Sorgu için Veri Yükleme (Load Data for Simple Query)

```python
import os


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.alibabacloud_mysql.base import (
    AlibabaCloudMySQLVectorStore,
)


# Gömme (Embedding) modelini ayarla
from llama_index.core import Settings
from llama_index.embeddings.dashscope import DashScopeEmbedding


Settings.embed_model = DashScopeEmbedding(api_key=DASHSCOPE_API_KEY)


# llm modelini yapılandır
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels


dashscope_llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_MAX, api_key=DASHSCOPE_API_KEY
)


documents = SimpleDirectoryReader("data/paul_graham/").load_data()
print(f"Toplam belge: {len(documents)}")
print(f"İlk belge, kimlik: {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    f"İlk belge, metin ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)


print(
    """
#################
# basit vektör üretimi
#################"""
)
client = AlibabaCloudMySQLVectorStore.from_params(
    host="rm-***.mysql.***.rds.aliyuncs.com",
    port=3306,
    user="kullanici",
    password="sifre",
    database="llama_index_test",
    distance_method="COSINE",
)
storage_context = StorageContext.from_defaults(vector_store=client)
VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
```

#### Arama Testi ile AlibabaCloudMySQL Kullanarak Sorgulama (Query using AlibabaCloudMySQL with Search Test)

```python
import os


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")


from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.alibabacloud_mysql.base import (
    AlibabaCloudMySQLVectorStore,
)


# Gömme modelini ayarla
from llama_index.core import Settings
from llama_index.embeddings.dashscope import DashScopeEmbedding


embed_model = DashScopeEmbedding(api_key=DASHSCOPE_API_KEY)
# Küresel Ayarlar (Global Settings)
Settings.embed_model = embed_model


# llm modelini yapılandır
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels


dashscope_llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_MAX, api_key=DASHSCOPE_API_KEY
)


print(
    """
#################
# Arama Testi dahil Temel Sorgulama
#################
"""
)
client = AlibabaCloudMySQLVectorStore.from_params(
    host="rm-***.mysql.eu-west-1.rds.***.com",
    port=3306,
    user="kullanici",
    password="sifre",
    database="llama_index_test",
    distance_method="COSINE",
)
index = VectorStoreIndex.from_vector_store(
    vector_store=client, embed_model=embed_model
)


QUESTION = "Yazar büyürken neler yaptı?"
# Erişiciyi (Retriever) Ayarla
vector_retriever = index.as_retriever()
# arama
source_nodes = vector_retriever.retrieve(QUESTION)
# kaynak düğümleri kontrol et
print(f"Soru: {QUESTION}")
for node in source_nodes:
    print(f"---------------------------------------------")
    print("Arama Testi (Search Test)")
    print(f"---------------------------------------------")
    print(f"Puan (Score): {node.score:.3f}")
    print(node.get_content())
    print(f"---------------------------------------------")


# sorguyu çalıştır
query_engine = index.as_query_engine(llm=dashscope_llm)
res = query_engine.query(QUESTION)
print(f"Yanıt (Answer): {res.response}")
print(f"---------------------------------------------\n\n")
```

### Metaveri Filtreleme (Metadata Filtering)

#### Metaveri Filtreleme için Veri Yükleme (Load Data for Metadata Filtering)

```python
import os


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.alibabacloud_mysql.base import (
    AlibabaCloudMySQLVectorStore,
)


# Gömme modelini ayarla
from llama_index.core import Settings
from llama_index.embeddings.dashscope import DashScopeEmbedding


Settings.embed_model = DashScopeEmbedding(api_key=DASHSCOPE_API_KEY)


# llm modelini yapılandır
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels


dashscope_llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_MAX, api_key=DASHSCOPE_API_KEY
)


documents = SimpleDirectoryReader("data/paul_graham/").load_data()
print(f"Toplam belge: {len(documents)}")
print(f"İlk belge, kimlik: {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    f"İlk belge, metin ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)


print(
    """
#################
# Metaveri Filtreleme için bazı metaverilerle vektör üretimi
#################"""
)
client = AlibabaCloudMySQLVectorStore.from_params(
    host="rm-***.mysql.***.rds.aliyuncs.com",
    port=3306,
    user="kullanici",
    password="sifre",
    database="llama_index_meta_test",
    distance_method="COSINE",
)
storage_context = StorageContext.from_defaults(vector_store=client)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)


from llama_index.core import Document
import regex as re


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


# Dipnotları indekse yerleştirin
for f in footnotes:
    index.insert(f)
```

#### Arama Testi ile AlibabaCloudMySQL Kullanarak Sorgulama

```python
import os


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")


from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.alibabacloud_mysql.base import (
    AlibabaCloudMySQLVectorStore,
)


# Gömme modelini ayarla
from llama_index.core import Settings
from llama_index.embeddings.dashscope import DashScopeEmbedding


embed_model = DashScopeEmbedding(api_key=DASHSCOPE_API_KEY)
# Küresel Ayarlar
Settings.embed_model = embed_model


# llm modelini yapılandır
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels


dashscope_llm = DashScope(
    model_name=DashScopeGenerationModels.QWEN_MAX, api_key=DASHSCOPE_API_KEY
)


print(
    """
#################
# Arama Testi dahil Metaveri Filtreleme ile Sorgulama
#################
"""
)
client = AlibabaCloudMySQLVectorStore.from_params(
    host="rm-***.mysql.***.rds.aliyuncs.com",
    port=3306,
    user="kullanici",
    password="sifre",
    database="llama_index_meta_test",
    distance_method="COSINE",
)
index = VectorStoreIndex.from_vector_store(
    vector_store=client, embed_model=embed_model
)


from llama_index.core.vector_stores import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator,
    FilterCondition,
)


QUESTION = "Yazar uzaylılar ve lisp hakkında ne söyledi?"
print(f"---------------------------------------------")
print(f"Soru: {QUESTION}")
filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="is_footnote", value="true", operator=FilterOperator.EQ
        ),
        MetadataFilter(key="mark_id", value=0, operator=FilterOperator.GTE),
    ],
    condition=FilterCondition.AND,
)
print(f"---------------------------------------------")
for i in range(len(filters.filters)):
    print(f"Filtre[{i}]: {filters.filters[i]}")
print(f"Filtre Koşulu: {filters.condition}")
print(f"---------------------------------------------")
retriever = index.as_retriever(
    filters=filters,
)
result = retriever.retrieve(QUESTION)
for node in result:
    print("Arama Testi")
    print(f"---------------------------------------------")
    print(f"Puan: {node.score:.3f}")
    print(node.get_content())
    print(f"---------------------------------------------")


# Sadece belirli dipnotları arayan bir sorgu motoru oluşturun.
footnote_query_engine = index.as_query_engine(
    filters=filters,
    llm=dashscope_llm,
)


res = footnote_query_engine.query(QUESTION)
print(f"Yanıt: {res.response}")
print(f"---------------------------------------------\n\n")
```
