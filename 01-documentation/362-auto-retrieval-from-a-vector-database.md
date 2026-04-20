---
title: Bir Vektör Veritabanından Otomatik Erişme (Auto-Retrieval)
 | LlamaIndex OSS Belgeleri
---

# Bir Vektör Veritabanından Otomatik Erişme

Bu kılavuz, LlamaIndex'te **otomatik erişme (auto-retrieval)** işleminin nasıl gerçekleştirileceğini gösterir.

Birçok popüler vektör veritabanı, semantik arama için bir sorgu dizesine ek olarak bir dizi meta veri filtresini destekler. Doğal dilde bir sorgu verildiğinde, vektör veritabanına iletilecek doğru sorgu dizesinin yanı sıra bir dizi meta veri filtresini de çıkarsamak (infer) için önce LLM'i kullanırız (ikisi de boş olabilir). Bu genel sorgu paketi (bundle) daha sonra vektör veritabanına karşı yürütülür.

bu, top-k semantik aramanın ötesinde daha dinamik ve ifade gücü yüksek erişim biçimlerine olanak tanır. Belirli bir sorgu için ilgili bağlam; yalnızca bir meta veri etiketine göre filtreleme gerektirebilir veya filtrelenmiş set içinde filtreleme + semantik aramanın ortak bir kombinasyonunu gerektirebilir veya yalnızca ham semantik arama gerektirebilir.

Bu örnekte Elasticsearch'ü kullanıyoruz, ancak otomatik erişme diğer birçok vektör veritabanı (örneğin Pinecone, Weaviate ve daha fazlası) ile de uygulanmıştır.

## Kurulum

Önce içe aktarmaları tanımlıyoruz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-elasticsearch
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

## Örnek Veri Tanımlama

Vektör veritabanına metin parçaları içeren bazı örnek düğümler (nodes) ekliyoruz. Her `TextNode`'un yalnızca metni değil, aynı zamanda `category` ve `country` gibi meta verileri de içerdiğine dikkat edin. Bu meta veri alanları, alttaki vektör veritabanında bu şekilde dönüştürülecek/saklanacaktır.

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
```

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text=(
            "Bir grup bilim insanı dinozorları geri getirir ve ortalık "
            "karışır"
        ),
        metadata={"year": 1993, "rating": 7.7, "genre": "bilim kurgu"},
    ),
    TextNode(
        text=(
            "Leo DiCaprio bir rüya içindeki rüya içindeki rüya içinde "
            "kaybolur..."
        ),
        metadata={
            "year": 2010,
            "director": "Christopher Nolan",
            "rating": 8.2,
        },
    ),
    TextNode(
        text=(
            "Bir psikolog / dedektif, rüyalar içindeki rüyalar serisinde "
            "kaybolur ve Inception bu fikri yeniden kullanır"
        ),
        metadata={"year": 2006, "director": "Satoshi Kon", "rating": 8.6},
    ),
    TextNode(
        text=(
            "Bir grup normal boyutlardaki kadın son derece sevimlidir ve bazı "
            "erkekler onların peşinden koşar"
        ),
        metadata={"year": 2019, "director": "Greta Gerwig", "rating": 8.3},
    ),
    TextNode(
        text="Oyuncaklar canlanır ve bunu yaparken harika vakit geçirirler",
        metadata={"year": 1995, "genre": "animasyon"},
    ),
]
```

## Elasticsearch Vektör Deposu ile Vektör İndeksi Oluşturma

Burada verileri vektör deposuna yüklüyoruz. Yukarıda belirtildiği gibi, her düğüm için hem metin hem de meta veriler Elasticsearch'teki karşılık gelen gösterime dönüştürülecektir. Artık Elasticsearch'ten bu veriler üzerinde semantik sorgular ve meta veri filtreleme çalıştırabiliriz.

```python
vector_store = ElasticsearchStore(
    index_name="auto_retriever_movies", es_url="http://localhost:9200"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```python
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

## `VectorIndexAutoRetriever` Tanımlama

Temel `VectorIndexAutoRetriever` modülümüzü tanımlıyoruz. Modül, vektör deposu koleksiyonunun yapılandırılmış bir açıklamasını ve desteklediği meta veri filtrelerini içeren `VectorStoreInfo`'yu alır. Bu bilgi daha sonra LLM'in meta veri filtrelerini çıkarsadığı otomatik erişme prompt'unda (yönlendirme) kullanılacaktır.

```python
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo




vector_store_info = VectorStoreInfo(
    content_info="Bir filmin kısa özeti",
    metadata_info=[
        MetadataInfo(
            name="genre",
            description="Filmin türü",
            type="string veya list[string]",
        ),
        MetadataInfo(
            name="year",
            description="Filmin vizyona girdiği yıl",
            type="integer",
        ),
        MetadataInfo(
            name="director",
            description="Film yönetmeninin adı",
            type="string",
        ),
        MetadataInfo(
            name="rating",
            description="Film için 1-10 arası puan",
            type="float",
        ),
    ],
)
retriever = VectorIndexAutoRetriever(
    index, vector_store_info=vector_store_info
)
```

## Örnek Veriler Üzerinde Çalıştırma

Bazı örnek veriler üzerinde çalıştırmayı deniyoruz. Meta veri filtrelerinin nasıl çıkarıldığına dikkat edin - bu, daha hassas erişime yardımcı olur!

```python
retriever.retrieve(
    "Christopher Nolan tarafından çekilen ve 2020'den önce yapılan 2 film nedir?"
)
```

```python
retriever.retrieve("Andrei Tarkovsky hiç bilim kurgu filmi yönetti mi?")
```

```text
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Sorgu dizesi kullanılıyor: bilim kurgu
Sorgu dizesi kullanılıyor: bilim kurgu
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:Filtreler kullanılıyor: {'director': 'Andrei Tarkovsky'}
Filtreler kullanılıyor: {'director': 'Andrei Tarkovsky'}
INFO:llama_index.indices.vector_store.retrievers.auto_retriever.auto_retriever:top_k kullanılıyor: 2
top_k kullanılıyor: 2
INFO:elastic_transport.transport:POST http://localhost:9200/auto_retriever_movies/_search [status:200 duration:0.042s]
POST http://localhost:9200/auto_retriever_movies/_search [status:200 duration:0.042s]


[]
```
