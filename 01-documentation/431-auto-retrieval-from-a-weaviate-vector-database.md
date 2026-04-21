# Bir Weaviate Vektör Veritabanından Otomatik Getirme (Auto-Retrieval)

---
title: Bir Weaviate Vektör Veritabanından Otomatik Getirme
 | LlamaIndex OSS Documentation
---

Bu kılavuz, LlamaIndex'te [Weaviate](https://weaviate.io/) ile **otomatik getirme** (auto-retrieval) işleminin nasıl gerçekleştirileceğini gösterir.

Weaviate vektör veritabanı, anlamsal arama için kullanılan bir sorgu dizisine ek olarak bir dizi [meta veri filtresini](https://weaviate.io/developers/weaviate/search/filters) destekler. Doğal dildeki bir sorgu verildiğinde, önce bir Büyük Dil Modeli (LLM) kullanarak vektör veritabanına iletilecek doğru sorgu dizisinin yanı sıra metin verisi filtrelerini çıkarırız (ikisinden biri boş da olabilir). Bu genel sorgu paketi daha sonra vektör veritabanında çalıştırılır.
 
 Bu, en iyi-k (top-k) anlamsal aramanın ötesinde daha dinamik ve ifade gücü yüksek getirme biçimlerine olanak tanır. Belirli bir sorgu için ilgili bağlam sadece bir meta veri etiketi üzerinde filtreleme gerektirebilir veya filtrelenmiş küme içinde filtreleme + anlamsal aramanın ortak bir kombinasyonunu ya da sadece ham anlamsal aramayı gerektirebilir.

## Kurulum

Önce içe aktarmaları tanımlıyoruz ve boş bir Weaviate koleksiyonu oluşturuyoruz.
 
 Bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```
%pip install llama-index-vector-stores-weaviate
```

```
!pip install llama-index weaviate-client
```

```
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

Meta veri filtrelerini çıkarmak için akıl yürütme yeteneklerinden dolayı GPT-4 kullanacağız. Kullanım durumunuza bağlı olarak `"gpt-3.5-turbo"` da işe yarayabilir.

```
# set up OpenAI
import os
import getpass
import openai


os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
openai.api_key = os.environ["OPENAI_API_KEY"]
```

```
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings


Settings.llm = OpenAI(model="gpt-4")
Settings.embed_model = OpenAIEmbedding()
```

Bu Not Defteri, Linux ve macOS üzerinde desteklenen [Gömülü (Embedded) modda](https://weaviate.io/developers/weaviate/installation/embedded) Weaviate kullanır.
 
 Weaviate'in tamamen yönetilen hizmeti olan [Weaviate Cloud Services (WCS)](https://weaviate.io/developers/weaviate/installation/weaviate-cloud-services)'i denemek isterseniz, yorum satırlarındaki kodu etkinleştirebilirsiniz.

```
import weaviate
from weaviate.embedded import EmbeddedOptions


# Connect to Weaviate client in embedded mode
client = weaviate.connect_to_embedded()


# Enable this code if you want to use Weaviate Cloud Services instead of Embedded mode.
"""
import weaviate


# cloud
cluster_url = ""
api_key = ""


client = weaviate.connect_to_wcs(cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)


# local
# client = weaviate.connect_to_local()
"""
```

## Bazı Örnek Verilerin Tanımlanması

Vektör veritabanına metin parçaları içeren bazı örnek düğümler ekliyoruz. Her bir `TextNode`'un sadece metni değil, aynı zamanda `category` ve `country` gibi meta verileri de içerdiğine dikkat edin. Bu meta veri alanları, alttaki vektör veritabanında bu şekilde dönüştürülecek ve saklanacaktır.

```
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text=(
            "Michael Jordan is a retired professional basketball player,"
            " widely regarded as one of the greatest basketball players of all"
            " time."
        ),
        metadata={
            "category": "Sports",
            "country": "United States",
        },
    ),
    TextNode(
        text=(
            "Angelina Jolie is an American actress, filmmaker, and"
            " humanitarian. She has received numerous awards for her acting"
            " and is known for her philanthropic work."
        ),
        metadata={
            "category": "Entertainment",
            "country": "United States",
        },
    ),
    TextNode(
        text=(
            "Elon Musk is a business magnate, industrial designer, and"
            " engineer. He is the founder, CEO, and lead designer of SpaceX,"
            " Tesla, Inc., Neuralink, and The Boring Company."
        ),
        metadata={
            "category": "Business",
            "country": "United States",
        },
    ),
    TextNode(
        text=(
            "Rihanna is a Barbadian singer, actress, and businesswoman. She"
            " has achieved significant success in the music industry and is"
            " known for her versatile musical style."
        ),
        metadata={
            "category": "Music",
            "country": "Barbados",
        },
    ),
    TextNode(
        text=(
            "Cristiano Ronaldo is a Portuguese professional footballer who is"
            " considered one of the greatest football players of all time. He"
            " has won numerous awards and set multiple records during his"
            " career."
        ),
        metadata={
            "category": "Sports",
            "country": "Portugal",
        },
    ),
]
```

## Weaviate Vektör Deposu ile Vektör İndeksi Oluşturma

Burada verileri vektör deposuna yüklüyoruz. Yukarıda belirtildiği gibi, her bir düğüm için hem metin hem de meta veriler Weaviate'teki karşılık gelen temsillere dönüştürülecektir. Artık bu veriler üzerinde Weaviate'ten anlamsal sorgular ve meta veri filtreleme çalıştırabiliriz.

```
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore


vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex_filter"
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

## `VectorIndexAutoRetriever` Tanımlama

Temel `VectorIndexAutoRetriever` modülümüzü tanımlıyoruz. Modül, vektör deposu koleksiyonunun yapılandırılmış bir açıklamasını ve desteklediği meta veri filtrelerini içeren `VectorStoreInfo` alır. Bu bilgi daha sonra LLM'in meta veri filtrelerini çıkardığı otomatik getirme isteminde (prompt) kullanılacaktır.

```
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo




vector_store_info = VectorStoreInfo(
    content_info="brief biography of celebrities",
    metadata_info=[
        MetadataInfo(
            name="category",
            type="str",
            description=(
                "Category of the celebrity, one of [Sports, Entertainment,"
                " Business, Music]"
            ),
        ),
        MetadataInfo(
            name="country",
            type="str",
            description=(
                "Country of the celebrity, one of [United States, Barbados,"
                " Portugal]"
            ),
        ),
    ],
)


retriever = VectorIndexAutoRetriever(
    index, vector_store_info=vector_store_info
)
```

## Bazı örnek veriler üzerinde çalıştırma

Bazı örnek veriler üzerinde çalıştırmayı deniyoruz. Meta veri filtrelerinin nasıl çıkarıldığına dikkat edin - bu daha kesin bir getirmeye yardımcı olur!

```
response = retriever.retrieve("Tell me about celebrities from United States")
```

```
print(response[0])
```

```
response = retriever.retrieve(
    "Tell me about Sports celebrities from United States"
)
```

```
print(response[0])
```
