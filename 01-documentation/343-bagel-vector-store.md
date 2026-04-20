# Bagel Vektör Deposu (Vector Store)

---
title: Bagel Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-bagel
%pip install llama-index
%pip install bagelML
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
import os


# Çevre değişkenini ayarla
os.environ["BAGEL_API_KEY"] = getpass.getpass("Bagel API Anahtarı:")
```

```python
import bagel
from bagel import Settings
```

```python
server_settings = Settings(
    bagel_api_impl="rest", bagel_server_host="api.bageldb.ai"
)


client = bagel.Client(server_settings)


collection = client.get_or_create_cluster(
    "testing_embeddings_3", embedding_model="custom", dimension=1536
)
```

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.bagel import BagelVectorStore
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

```python
vector_store = BagelVectorStore(collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```python
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

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

```python
retriever.retrieve("ünlü")
```
