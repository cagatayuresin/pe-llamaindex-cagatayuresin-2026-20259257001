# Azure Cosmos DB NoSQL Vektör Deposu (Vector Store)

---
title: Azure Cosmos DB NoSQL Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için `AzureCosmosDBNoSqlVectorSearch`ün nasıl kullanılacağına dair hızlı bir demo göstereceğiz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-embeddings-openai
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
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
```

# Azure OpenAI Kurulumu

İlk adım, LLM ve gömme (embeddings) modelini yapılandırmaktır. Bu modeller, veritabanına yüklenen belgeler için gömmeler oluşturmak ve LLM tamamlamaları için kullanılacaktır.

```python
llm = AzureOpenAI(
    model="AZURE_OPENAI_MODEL",
    deployment_name="AZURE_OPENAI_DAĞITIM_ADI",
    azure_endpoint="AZURE_OPENAI_UC_NOKTASI",
    api_key="AZURE_OPENAI_ANAHTARI",
    api_version="AZURE_OPENAI_VERSIYONU",
)


embed_model = AzureOpenAIEmbedding(
    model="AZURE_OPENAI_GÖMME_MODELI",
    deployment_name="AZURE_OPENAI_GÖMME_MODELI_DAĞITIM_ADI",
    azure_endpoint="AZURE_OPENAI_UC_NOKTASI",
    api_key="AZURE_OPENAI_ANAHTARI",
    api_version="AZURE_OPENAI_VERSIYONU",
)
```

```python
from llama_index.core import Settings


Settings.llm = llm
Settings.embed_model = embed_model
```

# Belgeleri Yükleme

Bu örnekte, `SimpleDirectoryReader` tarafından işlenecek olan paul\_graham makalesini kullanacağız.

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader(
    input_files=[r"\docs\examples\data\paul_graham\paul_graham_essay.txt"]
).load_data()


print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

# İndeksi Oluşturma

Burada Cosmos DB NoSQL bağlantısını kuruyoruz ve bir vektör deposu indeksi oluşturuyoruz.

```python
from azure.cosmos import CosmosClient, PartitionKey
from llama_index.vector_stores.azurecosmosnosql import (
    AzureCosmosDBNoSqlVectorSearch,
)
from llama_index.core import StorageContext


# cosmos istemcisi oluştur
URI = "AZURE_COSMOSDB_URI_ADRESI"
KEY = "AZURE_COSMOSDB_ANAHTARI"
client = CosmosClient(URI, credential=KEY)


# vektör deposu özelliklerini belirt
indexing_policy = {
    "indexingMode": "consistent",
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{"path": '/"_etag"/?'}],
    "vectorIndexes": [{"path": "/embedding", "type": "quantizedFlat"}],
}


vector_embedding_policy = {
    "vectorEmbeddings": [
        {
            "path": "/embedding",
            "dataType": "float32",
            "distanceFunction": "cosine",
            "dimensions": 3072,
        }
    ]
}


partition_key = PartitionKey(path="/id")
cosmos_container_properties_test = {"partition_key": partition_key}
cosmos_database_properties_test = {}


# vektör deposunu oluştur
store = AzureCosmosDBNoSqlVectorSearch(
    cosmos_client=client,
    vector_embedding_policy=vector_embedding_policy,
    indexing_policy=indexing_policy,
    cosmos_container_properties=cosmos_container_properties_test,
    cosmos_database_properties=cosmos_database_properties_test,
    create_container=True,
)


storage_context = StorageContext.from_defaults(vector_store=store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

# İndeksi Sorgulama

Artık indeksimizi kullanarak sorular sorabiliriz.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar ne üzerinde çalışmayı seviyordu?")
```

```python
import textwrap


print(textwrap.fill(str(response), 100))
```
