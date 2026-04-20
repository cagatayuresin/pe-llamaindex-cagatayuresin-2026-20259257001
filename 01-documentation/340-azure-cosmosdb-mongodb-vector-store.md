# Azure Cosmos DB MongoDB Vektör Deposu

---
title: Azure Cosmos DB MongoDB Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için Azure Cosmos DB MongoDB vCore'un nasıl kullanılacağını göstereceğiz. Gömmeleri (embeddings) oluşturmak için Azure OpenAI kullanacağız.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-embeddings-openai
%pip install llama-index-vector-stores-azurecosmosmongo
%pip install llama-index-llms-azure-openai
```

```bash
!pip install llama-index
```

```python
import os
import json
import openai
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
```

### Azure OpenAI Kurulumu

İlk adım modelleri yapılandırmaktır. Bunlar, veritabanına yüklenen belgeler için gömmeler oluşturmak ve LLM tamamlamaları için kullanılacaktır.

```python
import os


# AzureOpenAI örneğini kurun
llm = AzureOpenAI(
    model_name=os.getenv("OPENAI_MODEL_COMPLETION"),
    deployment_name=os.getenv("OPENAI_MODEL_COMPLETION"),
    api_base=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_type=os.getenv("OPENAI_API_TYPE"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    temperature=0,
)


# OpenAIEmbedding örneğini kurun
embed_model = OpenAIEmbedding(
    model=os.getenv("OPENAI_MODEL_EMBEDDING"),
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_EMBEDDING"),
    api_base=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_type=os.getenv("OPENAI_API_TYPE"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)
```

```python
from llama_index.core import Settings


Settings.llm = llm
Settings.embed_model = embed_model
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri yükleme

SimpleDirectoryReader kullanarak `data/paul_graham/` dizininde saklanan belgeleri yükleyin.

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

```text
Belge Kimliği (Document ID): c432ff1c-61ea-4c91-bd89-62be29078e79
```

### İndeksi oluşturma

Burada bir Azure Cosmos DB MongoDB vCore kümesine bağlantı kuruyoruz ve bir vektör arama indeksi oluşturuyoruz.

```python
import pymongo
from llama_index.vector_stores.azurecosmosmongo import (
    AzureCosmosDBMongoDBVectorSearch,
)
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader


connection_string = os.environ.get("AZURE_COSMOSDB_MONGODB_URI")
mongodb_client = pymongo.MongoClient(connection_string)
store = AzureCosmosDBMongoDBVectorSearch(
    mongodb_client=mongodb_client,
    db_name="demo_vectordb",
    collection_name="paul_graham_essay",
)
storage_context = StorageContext.from_defaults(vector_store=store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### İndeksi sorgulama

Artık indeksimizi kullanarak sorular sorabiliriz.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar ne üzerinde çalışmayı seviyordu?")
```

```python
import textwrap


print(textwrap.fill(str(response), 100))
```

```text
Yazar, lisanüstü eğitimindeyken tezi dışındaki birden fazla proje üzerinde çalışmayı seviyordu;
bunlar arasında Lisp hackleme ve On Lisp yazma vardı. Sonunda, mezun olmak için sadece 5 hafta içinde
continuations uygulamaları üzerine bir doktora tezi yazdı. Daha sonra sanat okullarına başvurdu ve
RISD'deki BFA programına kabul edildi.
```

```python
response = query_engine.query("Yazar 2016 yazında ne yaptı?")
```

```python
print(textwrap.fill(str(response), 100))
```

```text
Yazar, 2016 yazında ailesiyle birlikte İngiltere'ye taşındı.
```
