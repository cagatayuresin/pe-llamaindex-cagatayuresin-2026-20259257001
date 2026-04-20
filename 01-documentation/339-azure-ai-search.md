# Azure AI Search

---
title: Azure AI Search
 | LlamaIndex OSS Belgeleri
---

## Temel Örnek (Basic Example)

Bu not defterinde, bir Paul Graham makalesini alıyoruz, parçalara ayırıyoruz, bir Azure OpenAI gömme (embedding) modeli kullanarak gömüyoruz, bir Azure AI Search indeksine yüklüyoruz ve ardından sorguluyoruz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
!pip install llama-index
!pip install wget
%pip install llama-index-vector-stores-azureaisearch
%pip install azure-search-documents==11.5.1
%pip install llama-index-embeddings-azure-openai
%pip install llama-index-llms-azure-openai
```

```python
import logging
import sys
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from IPython.display import Markdown, display
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.settings import Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.vector_stores.azureaisearch import AzureAISearchVectorStore
from llama_index.vector_stores.azureaisearch import (
    IndexManagement,
    MetadataIndexFieldType,
)
```

## Azure OpenAI Kurulumu

```python
aoai_api_key = "AZURE_OPENAI_API_ANAHTARINIZ"
aoai_endpoint = "AZURE_OPENAI_UÇ_NOKTANIZ"
aoai_api_version = "2024-10-21"


llm = AzureOpenAI(
    model="AZURE_OPENAI_TAMAMLAMA_MODEL_ADINIZ",
    deployment_name="AZURE_OPENAI_TAMAMLAMA_DAĞITIM_ADINIZ",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)


# Kendi sohbet tamamlama modelinizin yanı sıra kendi gömme modelinizi de dağıtmanız gerekir
embed_model = AzureOpenAIEmbedding(
    model="AZURE_OPENAI_GÖMME_MODEL_ADINIZ",
    deployment_name="AZURE_OPENAI_GÖMME_DAĞITIM_ADINIZ",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)
```

## Azure AI Search Kurulumu

```python
search_service_api_key = "AZURE-SEARCH-HİZMETİ-ADMİN-ANAHTARINIZ"
search_service_endpoint = "AZURE-SEARCH-HİZMETİ-UÇ-NOKTANIZ"
search_service_api_version = "2024-07-01"
credential = AzureKeyCredential(search_service_api_key)




# Kullanılacak indeks adı
index_name = "llamaindex-vektor-demo"


# Bir indeks oluşturmayı göstermek için indeks istemcisini kullanın
index_client = SearchIndexClient(
    endpoint=search_service_endpoint,
    credential=credential,
)


# Mevcut indeksi kullanmayı göstermek için arama istemcisini kullanın
search_client = SearchClient(
    endpoint=search_service_endpoint,
    index_name=index_name,
    credential=credential,
)
```

## İndeks Oluşturma (Eğer mevcut değilse)

Eğer mevcut değilse "llamaindex-vektor-demo" adında bir vektör indeksi oluşturmayı gösterir. İndeks aşağıdaki alanlara sahiptir:

| Alan Adı (Field Name) | OData Tipi               |
| --------------------- | ------------------------ |
| id                    | `Edm.String`             |
| chunk                 | `Edm.String`             |
| embedding             | `Collection(Edm.Single)` |
| metadata              | `Edm.String`             |
| doc\_id               | `Edm.String`             |
| author                | `Edm.String`             |
| theme                 | `Edm.String`             |
| director              | `Edm.String`             |

```python
metadata_fields = {
    "author": "author",
    "theme": ("topic", MetadataIndexFieldType.STRING),
    "director": "director",
}


vector_store = AzureAISearchVectorStore(
    search_or_index_client=index_client,
    filterable_metadata_field_keys=metadata_fields,
    index_name=index_name,
    index_management=IndexManagement.CREATE_IF_NOT_EXISTS,
    id_field_key="id",
    chunk_field_key="chunk",
    embedding_field_key="embedding",
    embedding_dimensionality=1536,
    metadata_string_field_key="metadata",
    doc_id_field_key="doc_id",
    language_analyzer="en.lucene",
    vector_algorithm_type="exhaustiveKnn",
    # compression_type="binary" # "scalar" veya "binary" kullanma seçeneği. NOT: sıkıştırma sadece HNSW için desteklenir
)
```

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri yükleme

SimpleDirectoryReader kullanarak `data/paul_graham/` dizininde saklanan belgeleri yükleyin

```python
# Belgeleri yükle
documents = SimpleDirectoryReader("../data/paul_graham/").load_data()
storage_context = StorageContext.from_defaults(vector_store=vector_store)


Settings.llm = llm
Settings.embed_model = embed_model
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
# Veriyi Sorgula
query_engine = index.as_query_engine(similarity_top_k=3)
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar okul dışında yazma ve programlamaya odaklandı, kısa hikayeler yazdı ve 9. sınıfta bir IBM 1401 üzerinde programlama denemeleri yaptı. Daha sonra yazar mikro bilgisayarlarda programlamaya devam etti ve sonunda babasını bir TRS-80 almaya ikna etti, burada basit oyunlar ve bir kelime işlemci yazmaya başladı.**

```python
response = query_engine.query(
    "Yazar ne öğrendi?",
)
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, erken bilgisayarlarda programlama yapmayı, erken yapay zekanın sınırlamalarını, prestijli olmayan şeyler üzerinde çalışmanın önemini ve çevrimiçi makale yazmanın önemini öğrendi.**

## Mevcut İndeksi Kullanma

```python
index_name = "llamaindex-vektor-demo"


metadata_fields = {
    "author": "author",
    "theme": ("topic", MetadataIndexFieldType.STRING),
    "director": "director",
}
vector_store = AzureAISearchVectorStore(
    search_or_index_client=search_client,
    filterable_metadata_field_keys=metadata_fields,
    index_management=IndexManagement.VALIDATE_INDEX,
    id_field_key="id",
    chunk_field_key="chunk",
    embedding_field_key="embedding",
    embedding_dimensionality=1536,
    metadata_string_field_key="metadata",
    doc_id_field_key="doc_id",
)
```

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    [],
    storage_context=storage_context,
)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar için zor olan bir an neydi?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, annesinin kolon kanserinden kaynaklanan bir felç geçirdiği ve bunun sonucunda vefat ettiği zor bir an yaşadı.**

```python
response = query_engine.query("Yazar kimdir?")
display(Markdown(f"<b>{response}</b>"))
```

**Paul Graham**

```python
import time


query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("Interleaf'te ne oldu?")


start_time = time.time()


token_count = 0
for token in response.response_gen:
    print(token, end="")
    token_count += 1


time_elapsed = time.time() - start_time
tokens_per_second = token_count / time_elapsed


print(f"\n\nÇıktı {tokens_per_second} jeton/sn hızında akışla verildi")
```

```text
Şirket, Emacs'tan esinlenen bir betik dili ekledi ve betik dilini bir Lisp lehçesi haline getirdi.


Çıktı 64.01633939770672 jeton/sn hızında akışla verildi
```

## Mevcut indekse belge ekleme

```python
response = query_engine.query("Gökyüzü ne renk?")
display(Markdown(f"<b>{response}</b>"))
```

**Gökyüzünün rengi; günün saati, hava koşulları ve konum gibi faktörlere bağlı olarak değişir.**

```python
from llama_index.core import Document


index.insert_nodes([Document(text="Gökyüzü bugün çivit mavisi")])
```

```python
response = query_engine.query("Gökyüzü ne renk?")
display(Markdown(f"<b>{response}</b>"))
```

**Gökyüzünün rengi çivit mavisi.**

## Filtreleme (Filtering)

Filtreler, llama-index'in filtre sözdizimini (syntax) kullanmak için `filters` parametresi veya filtreleri doğrudan iletmek için `odata_filters` parametresi kullanılarak sorgulara uygulanabilir.

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="Esaretin Bedeli (The Shawshank Redemption)",
        metadata={
            "author": "Stephen King",
            "theme": "Dostluk",
        },
    ),
    TextNode(
        text="Baba (The Godfather)",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafya",
        },
    ),
    TextNode(
        text="Başlangıç (Inception)",
        metadata={
            "director": "Christopher Nolan",
        },
    ),
]
```

```python
index.insert_nodes(nodes)
```

```python
from llama_index.core.vector_stores.types import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator,
    FilterCondition,
)




filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Mafya", operator=FilterOperator.EQ)
    ],
    # birden fazla filtre uygulamak isterseniz AND, OR, NOT koşulunu kullanabilirsiniz
    # condition=FilterCondition.AND
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```

```python
[NodeWithScore(node=TextNode(id_='f0c299d8-1f59-4338-9c4e-06b99855ed23', embedding=None, metadata={'director': 'Francis Ford Coppola', 'theme': 'Mafya'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Baba (The Godfather)', mimetype='text/plain', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.8120511)]
```

Veya doğrudan `odata_filters` parametresini ileterek:

```python
odata_filters = "theme eq 'Mafya'"
retriever = index.as_retriever(
    vector_store_kwargs={"odata_filters": odata_filters}
)
retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```

## Sorgu Modu (Query Mode)

Dört sorgu modu desteklenir: DEFAULT (vektör araması), SPARSE, HYBRID ve SEMANTIC\_HYBRID.

### Vektör Araması Gerçekleştirme

```python
from llama_index.core.vector_stores.types import VectorStoreQueryMode


default_retriever = index.as_retriever(
    vector_store_query_mode=VectorStoreQueryMode.DEFAULT
)
response = default_retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")


# Yanıttaki her NodeWithScore üzerinden döngü kurun
for node_with_score in response:
    node = node_with_score.node  # TextNode nesnesi
    score = node_with_score.score  # Benzerlik puanı
    chunk_id = node.id_  # Parça (chunk) ID'si


    # Düğümden ilgili metaverileri ayıklayın
    file_name = node.metadata.get("file_name", "Bilinmiyor")
    file_path = node.metadata.get("file_path", "Bilinmiyor")


    # Düğümden metin içeriğini ayıklayın
    text_content = node.text if node.text else "İçerik mevcut değil"


    # Sonuçları kullanıcı dostu bir formatta yazdırın
    print(f"Puan (Score): {score}")
    print(f"Dosya Adı: {file_name}")
    print(f"Kimlik (Id): {chunk_id}")
    print("\nAyıklanan İçerik:")
    print(text_content)
    print("\n" + "=" * 40 + " Sonucun Sonu " + "=" * 40 + "\n")
```

```text
Puan (Score): 0.87485534
Dosya Adı: Bilinmiyor
Kimlik (Id): b4d2af4e-1de0-4cfe-8b18-629722bc12d7


Ayıklanan İçerik:
Inception (Başlangıç)


======================================== Sonucun Sonu ========================================


Puan (Score): 0.8120511
Dosya Adı: Bilinmiyor
Kimlik (Id): f0c299d8-1f59-4338-9c4e-06b99855ed23


Ayıklanan İçerik:
Baba (The Godfather)


======================================== Sonucun Sonu ========================================
```

### Hibrit Arama Gerçekleştirme (Hybrid Search)

```python
from llama_index.core.vector_stores.types import VectorStoreQueryMode


hybrid_retriever = index.as_retriever(
    vector_store_query_mode=VectorStoreQueryMode.HYBRID
)
hybrid_retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```

### Anlamsal Yeniden Sıralama ile Hibrit Arama Gerçekleştirme

Bu mod, arama uygunluğunu artırmak için hibrit arama sonuçlarına anlamsal yeniden sıralama (semantic reranking) ekler.

Daha fazla ayrıntı için lütfen bu bağlantıya bakın: <https://learn.microsoft.com/azure/search/semantic-search-overview>

```python
hybrid_retriever = index.as_retriever(
    vector_store_query_mode=VectorStoreQueryMode.SEMANTIC_HYBRID
)
hybrid_retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```
