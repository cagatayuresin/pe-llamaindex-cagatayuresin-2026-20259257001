---
title: Lantern Vektör Deposu (Otomatik Erişici - Auto-Retriever)
 | LlamaIndex OSS Belgeleri
---

# Lantern Vektör Deposu (Otomatik Erişici - Auto-Retriever)

Bu kılavuz, LlamaIndex'te **otomatik erişme (auto-retrieval)** işleminin nasıl gerçekleştirileceğini göstermektedir.

Birçok popüler vektör veritabanı, semantik arama için kullanılan sorgu dizesine (query string) ek olarak bir dizi meta veri filtresini destekler. Doğal dildeki bir sorgu verildiğinde, önce LLM'yi kullanarak vektör veritabanına iletilecek doğru sorgu dizesinin yanı sıra bir dizi meta veri filtresini (her ikisi de boş olabilir) tahmin ederiz. Bu genel sorgu demeti (query bundle) daha sonra vektör veritabanına karşı yürütülür.

bu, top-k semantik aramanın ötesinde daha dinamik ve ifade gücü yüksek erişim biçimlerine olanak tanır. Belirli bir sorgu için ilgili bağlam; yalnızca bir meta veri etiketi üzerinden filtreleme yapmayı, filtrelenmiş set içinde filtreleme + semantik aramanın birleşik bir kombinasyonunu veya yalnızca doğrudan semantik aramayı gerektirebilir.

Bu örnekte Lantern ile bir demo gösteriyoruz, ancak otomatik erişme diğer birçok vektör veritabanıyla da (örneğin Pinecone, Chroma, Weaviate ve daha fazlası) uygulanmıştır.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-lantern
```

```bash
!pip install llama-index psycopg2-binary asyncpg
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
# OpenAI kurulumu
import os


os.environ["OPENAI_API_KEY"] = "<api-anahtarınız>"


import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
```

```python
import psycopg2
from sqlalchemy import make_url


connection_string = "postgresql://postgres:postgres@localhost:5432"


url = make_url(connection_string)


db_name = "postgres"
conn = psycopg2.connect(connection_string)
conn.autocommit = True
```

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.lantern import LanternVectorStore
```

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text=(
            "Michael Jordan, tüm zamanların en iyi basketbolcularından biri "
            "olarak kabul edilen emekli bir profesyonel basketbolcudur."
        ),
        metadata={
            "category": "Spor",
            "country": "Amerika Birleşik Devletleri",
        },
    ),
    TextNode(
        text=(
            "Angelina Jolie, Amerikalı bir aktris, film yapımcısı ve "
            "insani yardım görevlisidir. Oyunculuğuyla çok sayıda ödül almış "
            "ve hayırsever çalışmalarıyla tanınmıştır."
        ),
        metadata={
            "category": "Eğlence",
            "country": "Amerika Birleşik Devletleri",
        },
    ),
    TextNode(
        text=(
            "Elon Musk bir iş insanı, endüstriyel tasarımcı ve mühendistir. "
            "SpaceX, Tesla, Inc., Neuralink ve The Boring Company'nin kurucusu, "
            "CEO'su ve baş tasarımcısıdır."
        ),
        metadata={
            "category": "İş Dünyası",
            "country": "Amerika Birleşik Devletleri",
        },
    ),
    TextNode(
        text=(
            "Rihanna, Barbadoslu bir şarkıcı, oyuncu ve iş kadınıdır. Müzik "
            "endüstrisinde önemli bir başarı elde etmiştir ve çok yönlü müzik "
            "tarzıyla tanınır."
        ),
        metadata={
            "category": "Müzik",
            "country": "Barbados",
        },
    ),
    TextNode(
        text=(
            "Cristiano Ronaldo, tüm zamanların en iyi futbolcularından biri "
            "olarak kabul edilen Portekizli profesyonel bir futbolcudur. "
            "Kariyeri boyunca çok sayıda ödül kazanmış ve birçok rekor kırmıştır."
        ),
        metadata={
            "category": "Spor",
            "country": "Portekiz",
        },
    ),
]
```

## Lantern Vektör Deposu ile Vektör İndeksi Oluşturma

Burada verileri vektör deposuna yüklüyoruz. Yukarıda belirtildiği gibi, her bir düğüm (node) için hem metin hem de meta veriler Lantern'deki karşılık gelen temsillere dönüştürülecektir. Artık Lantern'deki bu veriler üzerinde semantik sorgular ve meta veri filtreleme çalıştırabiliriz.

```python
vector_store = LanternVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="famous_people",
    embed_dim=1536,  # openai gömme boyutu
    m=16,  # HNSW M parametresi
    ef_construction=128,  # HNSW ef construction parametresi
    ef=64,  # HNSW ef search parametresi
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```python
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

## `VectorIndexAutoRetriever` Tanımlama

Çekirdek `VectorIndexAutoRetriever` modülümüzü tanımlıyoruz. Modül, vektör deposu koleksiyonunun yapılandırılmış bir açıklamasını ve desteklediği meta veri filtrelerini içeren `VectorStoreInfo` nesnesini alır. Bu bilgi daha sonra LLM'nin meta veri filtrelerini tahmin ettiği otomatik erişme isteminde (prompt) kullanılacaktır.

```python
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo




vector_store_info = VectorStoreInfo(
    content_info="ünlülerin kısa biyografileri",
    metadata_info=[
        MetadataInfo(
            name="category",
            type="str",
            description=(
                "Ünlünün kategorisi, şunlardan biri: [Spor, Eğlence, İş Dünyası, Müzik]"
            ),
        ),
        MetadataInfo(
            name="country",
            type="str",
            description=(
                "Ünlünün ülkesi, şunlardan biri: [Amerika Birleşik Devletleri, Barbados, Portekiz]"
            ),
        ),
    ],
)
retriever = VectorIndexAutoRetriever(
    index, vector_store_info=vector_store_info
)
```

## Bazı Örnek Veriler Üzerinde Çalıştırma

Bazı örnek veriler üzerinde çalıştırmayı deniyoruz. Meta veri filtrelerinin nasıl tahmin edildiğine dikkat edin; bu, daha hassas bir erişime (retrieval) yardımcı olur!

```python
retriever.retrieve("Bana Amerika Birleşik Devletleri'nden iki ünlüden bahset")
```
