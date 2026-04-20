# Vectara İndeksinden Otomatik Erişim (Auto-Retrieval from a Vectara Index)

---
title: Vectara İndeksinden Otomatik Erişim (Auto-Retrieval from a Vectara Index)
 | LlamaIndex OSS Belgeleri
---

Bu kılavuz, Vectara ile LlamaIndex'te **otomatik erişimin** (auto-retrieval) nasıl gerçekleştirileceğini gösterir.

Otomatik erişim ile, bir erişim sorgusunu Vectara'ya göndermeden önce yorumlarız; böylece sorgunun bazı metaveri filtrelemeleriyle birlikte daha kısa bir sorgu olarak potansiyel yeniden yazımlarını belirleriz.

Örneğin, "2022'deki gelir nedir" gibi bir sorgu, "gelir nedir" şeklinde yeniden yazılabilir ve yanına "doc.year = 2022" filtresi eklenebilir. Bunun bir örnek üzerinden nasıl çalıştığını görelim.

## Kurulum (Setup)

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i kurmanız gerekecektir 🦙.

```bash
!pip install llama_index llama-index-llms-openai llama-index-indices-managed-vectara
```

```text
Requirement already satisfied: llama_index in /Users/ofer/miniconda3/envs/langchain/lib/python3.11/site-packages (0.10.37)
... (diğer gereksinim mesajları) ...
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
from llama_index.core.schema import TextNode
from llama_index.core.indices.managed.types import ManagedIndexQueryMode
from llama_index.indices.managed.vectara import VectaraIndex
from llama_index.indices.managed.vectara import VectaraAutoRetriever


from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo


from llama_index.llms.openai import OpenAI
```

## Örnek Veri Tanımlama (Defining Some Sample Data)

Önce filmlerden oluşan bir veri kümesi tanımlıyoruz:

1. Her düğüm (node) bir filmi tanımlar.
2. `text` filmi tanımlarken, `metadata` yıl, yönetmen, puan veya tür gibi belirli metaveri alanlarını tanımlar.

Vectara'da, filtrelemenin gerçekleşebilmesi için bu metaveri alanlarını korpusunuzda (corpus) [filtrelenebilir öznitelikler](https://docs.vectara.com/docs/learn/metadata-search-filtering/filter-overview) olarak tanımlamanız gerekecektir.

```python
nodes = [
    TextNode(
        text=(
            "Orta Amerika'da bir adada neredeyse tamamlanmış bir tema parkını gezen pragmatik bir paleontolog, "
            + "bir güç kesintisinin parkın klonlanmış dinozorlarının serbest kalmasına neden olmasından sonra "
            + "bir çift çocuğu korumakla görevlendirilir."
        ),
        metadata={"year": 1993, "rating": 7.7, "genre": "science fiction"},
    ),
    TextNode(
        text=(
            "Rüya paylaşımı teknolojisini kullanarak kurumsal sırları çalan bir hırsıza, bir CEO'nun "
            + "zihnine bir fikir yerleştirme görevi verilir, ancak trajik geçmişi projeyi "
            + "ve ekibini felakete sürükleyebilir."
        ),
        metadata={
            "year": 2010,
            "director": "Christopher Nolan",
            "rating": 8.2,
        },
    ),
    TextNode(
        text="Barbie, dünyasını ve varlığını sorgulamasına neden olan bir kriz yaşar.",
        metadata={
            "year": 2023,
            "director": "Greta Gerwig",
            "genre": "fantasy",
            "rating": 9.5,
        },
    ),
    TextNode(
        text=(
            "Bir kovboy bebek, yeni bir uzay adamı aksiyon figürünün bir çocuğun yatak odasında "
            + "en iyi oyuncak olarak yerini almasıyla derin bir tehdit hisseder ve kıskançlık duyar."
        ),
        metadata={"year": 1995, "genre": "animated", "rating": 8.3},
    ),
    TextNode(
        text=(
            "Woody bir oyuncak koleksiyoncusu tarafından çalındığında, Buzz ve arkadaşları, "
            + "Woody'yi çetesi Jessie, Prospector ve Bullseye ile birlikte bir müze malı olmadan önce "
            + "kurtarmak için bir göreve çıkarlar."
        ),
        metadata={"year": 1999, "genre": "animated", "rating": 7.9},
    ),
    TextNode(
        text=(
            "Oyuncaklar, Andy üniversiteye gitmeden hemen önce yanlışlıkla tavan arası yerine "
            + "bir kreşe teslim edilir ve diğer oyuncakları terk edilmediklerine ikna edip "
            + "eve dönmelerini sağlamak Woody'ye kalır."
        ),
        metadata={"year": 2010, "genre": "animated", "rating": 8.3},
    ),
]
```

Ardından örnek verilerimizi Vectara İndeksimize yüklüyoruz.

```python
import os


os.environ["VECTARA_API_KEY"] = "<VECTARA_API_ANAHTARINIZ>"
os.environ["VECTARA_CORPUS_ID"] = "<VECTARA_KORPUS_ID_NİZ>"
os.environ["VECTARA_CUSTOMER_ID"] = "<VECTARA_MUSTERI_ID_NİZ>"


index = VectaraIndex(nodes=nodes)
```

## `VectorStoreInfo` Tanımlama (Defining the `VectorStoreInfo`)

Vectara İndeksimiz tarafından desteklenen metaveri filtrelerinin yapılandırılmış bir açıklamasını içeren bir `VectorStoreInfo` nesnesi tanımlıyoruz. Bu bilgi daha sonra otomatik erişim isteminde kullanılır ve LLM'nin belirli bir sorgu için kullanılacak metaveri filtrelerini çıkarmasını sağlar.

```python
vector_store_info = VectorStoreInfo(
    content_info="bir film hakkında bilgi",
    metadata_info=[
        MetadataInfo(
            name="genre",
            description="""
                Filmin türü.
                Şunlardan biri: ['science fiction', 'fantasy', 'comedy', 'drama', 'thriller', 'romance', 'action', 'animated']
            """,
            type="string",
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
            description="Film için 1-10 arası bir puan",
            type="float",
        ),
    ],
)
```

## Otomatik Erişimi Çalıştırma (Running auto-retrieval)

Şimdi bir `VectaraAutoRetriever` örneği oluşturalım ve `retrieve()` metodunu deneyelim:

```python
from llama_index.indices.managed.vectara import VectaraAutoRetriever
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo", temperature=0)


retriever = VectaraAutoRetriever(
    index,
    vector_store_info=vector_store_info,
    llm=llm,
    verbose=True,
)
```

```python
retriever.retrieve("Greta Gerwig tarafından yönetilen film")
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Kullanılan sorgu dizisi (query str): movie directed by Greta Gerwig
Kullanılan örtük filtreler: [('director', '==', 'Greta Gerwig')]
Nihai filtre dizisi: (doc.director == 'Greta Gerwig')


[NodeWithScore(node=TextNode(id_='935c2319f66122e1c4189ccf32164b362d4b6bc2af4ede77fc47fd126546ba8d', embedding=None, metadata={'lang': 'eng', 'offset': '0', 'len': '79', 'year': '2023', 'director': 'Greta Gerwig', 'genre': 'fantasy', 'rating': '9.5'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Barbie suffers a crisis that leads her to question her world and her existence.', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.61976165)]
```

```python
retriever.retrieve("puanı 8'in üzerinde olan bir film")
```

```text
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Kullanılan sorgu dizisi (query str): movie with rating above 8
Kullanılan örtük filtreler: [('rating', '>', 8)]
Nihai filtre dizisi: (doc.rating > '8')


[NodeWithScore(node=TextNode(id_='a55396c48ddb51e593676d37a18efa8da1cbab6fd206c9029ced924e386c12b5', embedding=None, metadata={'lang': 'eng', 'offset': '0', 'len': '129', 'year': '1995', 'genre': 'animated', 'rating': '8.3'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.5414715),
 NodeWithScore(node=TextNode(id_='b1e87de59678f3f1831327948a716f6e5a217c9b8cee4c08d5555d337825fca8', embedding=None, metadata={'lang': 'eng', 'offset': '0', 'len': '220', 'year': '2010', 'director': 'Christopher Nolan', 'rating': '8.2'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.50233454),
 NodeWithScore(node=TextNode(id_='935c2319f66122e1c4189ccf32164b362d4b6bc2af4ede77fc47fd126546ba8d', embedding=None, metadata={'lang': 'eng', 'offset': '0', 'len': '79', 'year': '2023', 'director': 'Greta Gerwig', 'genre': 'fantasy', 'rating': '9.5'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text='Barbie suffers a crisis that leads her to question her world and her existence.', start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.500028),
 NodeWithScore(node=TextNode(id_='a860d7045527b4659a1a1171f922e30bee754ddcf83e0ec8423238f9f634f118', embedding=None, metadata={'lang': 'eng', 'offset': '0', 'len': '209', 'year': '2010', 'genre': 'animated', 'rating': '8.3'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, text="The toys are mistakenly delivered to a day-care center instead of the attic right before Andy leaves for college, and it's up to Woody to convince the other toys that they weren't abandoned and to return home.", start_char_idx=None, end_char_idx=None, text_template='{metadata_str}\n\n{content}', metadata_template='{key}: {value}', metadata_seperator='\n'), score=0.47051564)]
```

`VectaraAutoRetriever` içinde standart `VectaraRetriever` argümanlarını da kullanabiliriz. Örneğin, sorgunun kendisinden gelen herhangi bir ek filtrelemeye eklenecek bir `filter` dahil etmek istersek, bunu aşağıdaki gibi yapabiliriz:
