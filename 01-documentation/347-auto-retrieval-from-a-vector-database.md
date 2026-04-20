# Vektör Veritabanından Otomatik Erişme (Auto-Retrieval from a Vector Database)

---
title: Vektör Veritabanından Otomatik Erişme (Auto-Retrieval from a Vector Database)
 | LlamaIndex OSS Belgeleri
---

Bu kılavuz, LlamaIndex'te **otomatik erişmenin** (auto-retrieval) nasıl gerçekleştirileceğini göstermektedir.

Pek çok popüler vektör veritabanı, anlamsal arama (semantic search) için bir sorgu dizesine ek olarak bir dizi metaveri filtresini destekler. Doğal dilde bir sorgu verildiğinde, öncelikle bir dizi metaveri filtresini ve vektör veritabanına iletilecek doğru sorgu dizesini (her ikisi de boş olabilir) çıkarmak için LLM'i kullanırız. Bu genel sorgu paketi daha sonra vektör veritabanı üzerinde çalıştırılır.

Bu, top-k anlamsal aramanın ötesinde daha dinamik ve açıklayıcı erişim biçimlerine olanak tanır. Belirli bir sorgu için ilgili bağlam; yalnızca bir metaveri etiketi üzerinde filtreleme gerektirebilir veya filtrelenmiş set içinde filtreleme + anlamsal aramanın bir kombinasyonunu gerektirebilir ya da sadece ham anlamsal arama gerektirebilir.

Burada Chroma ile bir örnek gösteriyoruz, ancak otomatik erişme diğer birçok vektör veritabanıyla (örneğin Pinecone, Weaviate ve daha fazlası) da uygulanmaktadır.

## Kurulum (Setup)

Öncelikle içe aktarmaları ve boş bir Chroma koleksiyonunu tanımlıyoruz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-chroma
```

```bash
!pip install llama-index
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
import getpass


os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Anahtarı:")
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
```

```python
import chromadb
```

```python
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")
```

## Bazı Örnek Verilerin Tanımlanması

Vektör veritabanına metin parçaları içeren bazı örnek düğümler yerleştiriyoruz. Her `TextNode`un yalnızca metni değil, aynı zamanda `category` (kategori) ve `country` (ülke) gibi metaverileri de içerdiğine dikkat edin. Bu metaveri alanları, alt plandaki vektör veritabanında bu şekilde dönüştürülecek/saklanacaktır.

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
```

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text=(
            "Michael Jordan, emekli bir profesyonel basketbol oyuncusudur ve"
            " yaygın olarak tüm zamanların en iyi basketbolcularından biri"
            " olarak kabul edilir."
        ),
        metadata={
            "category": "Spor",
            "country": "Amerika Birleşik Devletleri",
        },
    ),
    TextNode(
        text=(
            "Angelina Jolie, Amerikalı bir aktris, film yapımcısı ve"
            " insancıl yardımseverdir. Oyunculuğuyla çok sayıda ödül almış"
            " ve hayırseverlik çalışmalarıyla tanınmaktadır."
        ),
        metadata={
            "category": "Eğlence",
            "country": "Amerika Birleşik Devletleri",
        },
    ),
    TextNode(
        text=(
            "Elon Musk, bir iş insanı, endüstriyel tasarımcı ve"
            " mühendistir. SpaceX, Tesla, Inc., Neuralink ve The Boring Company'nin"
            " kurucusu, CEO'su ve baş tasarımcısıdır."
        ),
        metadata={
            "category": "İş Dünyası",
            "country": "Amerika Birleşik Devletleri",
        },
    ),
    TextNode(
        text=(
            "Rihanna, Barbadoslu bir şarkıcı, aktris ve iş kadınıdır. Müzik"
            " endüstrisinde önemli bir başarı elde etmiştir ve çok yönlü"
            " müzik tarzıyla tanınır."
        ),
        metadata={
            "category": "Müzik",
            "country": "Barbados",
        },
    ),
    TextNode(
        text=(
            "Cristiano Ronaldo, tüm zamanların en iyi futbolcularından biri"
            " olarak kabul edilen Portekizli profesyonel bir futbolcudur. Kariyeri"
            " boyunca sayısız ödül kazanmış ve birçok rekor kırmıştır."
        ),
        metadata={
            "category": "Spor",
            "country": "Portekiz",
        },
    ),
]
```

## Chroma Vektör Deposu ile Vektör İndeksi Oluşturma

Burada verileri vektör deposuna yüklüyoruz. Yukarıda belirtildiği gibi, her düğüm için hem metin hem de metaveriler Chroma'da karşılık gelen temsillere dönüştürülecektir. Artık Chroma'dan gelen bu veriler üzerinde anlamsal sorgular ve metaveri filtrelemesi çalıştırabiliriz.

```python
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```python
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

## `VectorIndexAutoRetriever` Tanımlama

Temel `VectorIndexAutoRetriever` modülümüzü tanımlıyoruz. Modül, vektör deposu koleksiyonunun yapılandırılmış bir açıklamasını ve desteklediği metaveri filtrelerini içeren `VectorStoreInfo`yu alır. Bu bilgi daha sonra LLM'in metaveri filtrelerini çıkardığı otomatik erişme isteminde (prompt) kullanılacaktır.

```python
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo




vector_store_info = VectorStoreInfo(
    content_info="ünlülerin kısa biyografileri",
    metadata_info=[
        MetadataInfo(
            name="category",
            type="str",
            description=(
                "Ünlünün kategorisi, şunlardan biri: [Spor, Eğlence,"
                " İş Dünyası, Müzik]"
            ),
        ),
        MetadataInfo(
            name="country",
            type="str",
            description=(
                "Ünlünün ülkesi, şunlardan biri: [Amerika Birleşik Devletleri, Barbados,"
                " Portekiz]"
            ),
        ),
    ],
)
retriever = VectorIndexAutoRetriever(
    index, vector_store_info=vector_store_info
)
```

## Bazı Örnek Veriler Üzerinde Çalıştırma

Bazı örnek veriler üzerinde çalıştırmayı deniyoruz. Metaveri filtrelerinin nasıl çıkarıldığına dikkat edin - bu, daha hassas bir erişime yardımcı olur!

```python
retriever.retrieve("Bana Amerika Birleşik Devletleri'nden iki ünlü anlat")
```

```text
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Sorgu dizesi kullanılıyor: ünlüler
Sorgu dizesi kullanılıyor: ünlüler
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Filtreler kullanılıyor: {'country': 'United States'}
Filtreler kullanılıyor: {'country': 'United States'}
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:top_k kullanılıyor: 2
top_k kullanılıyor: 2


[NodeWithScore(node=TextNode(id_='b2ab3b1a-5731-41ec-b884-405016de5a34', embedding=None, metadata={'category': 'Eğlence', 'country': 'Amerika Birleşik Devletleri'}, ...), score=0.32621567877748514),
 NodeWithScore(node=TextNode(id_='e0104b6a-676a-4c83-95b7-b018cb8b39b2', embedding=None, metadata={'category': 'Spor', 'country': 'Amerika Birleşik Devletleri'}, ...), score=0.3734030955060519)]
```

```python
retriever.retrieve("Bana Amerika Birleşik Devletleri'nden Spor dünyasından ünlüler anlat")
```
