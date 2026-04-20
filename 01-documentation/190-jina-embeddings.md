# Jina Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-jinaai
%pip install llama-index-llms-openai
```

```python
!pip install llama-index
```

Doğrudan llama-index ile gelmeyen diğer paketlere de ihtiyacınız olabilir:

```python
!pip install Pillow
```

Bu örnek için https://jina.ai/embeddings/ adresinden alabileceğiniz bir API anahtarına ihtiyacınız olacak.

```python
# API anahtarınızla başlatın
import os

jinaai_api_key = "JINAAI_API_ANAHTARINIZ"
os.environ["JINAAI_API_KEY"] = jinaai_api_key
```

## JinaAI API aracılığıyla Jina embedding modelleri ile metin ve sorguları gömme

`JinaEmbedding` sınıfını kullanarak metninizi ve sorgularınızı kodlayabilirsiniz (encode). Jina, çeşitli kullanım durumlarına uyarlanabilen bir dizi model sunar.

| Model | Boyut | Dil | MRL (matryoshka) | Bağlam (Context) |
| :---: | :---: | :---: | :---: | :---: |
| jina-embeddings-v3 | 1024 | Çok dilli (89 dil) | Evet | 8192 |
| jina-embeddings-v2-base-en | 768 | İngilizce | Hayır | 8192 |
| jina-embeddings-v2-base-de | 768 | Almanca & İngilizce | Hayır | 8192 |
| jina-embeddings-v2-base-es | 768 | İspanyolca & İngilizce | Hayır | 8192 |
| jina-embeddings-v2-base-zh | 768 | Çince & İngilizce | Hayır | 8192 |

**Önerilen Model: jina-embeddings-v3 :**

Jina AI'nın en yeni ve en yüksek performanslı embedding modeli olarak `jina-embeddings-v3`'ü öneriyoruz. Bu model, taban yapısının (backbone) üzerine eğitilmiş 5 adet göreve özel adaptöre (task-specific adapters) sahiptir ve çeşitli embedding kullanım durumlarını optimize eder.

Varsayılan olarak `JinaEmbedding` sınıfı `jina-embeddings-v3` kullanır.

**Göreve Özel Adaptörler (Task-Specific Adapters):**

Uçtaki (downstream) uygulamanızı optimize etmek için isteğinize `task` parametresini ekleyin:

+ **retrieval.query**: Erişim görevlerinde kullanıcı sorgularını veya sorularını kodlamak için kullanılır.
+ **retrieval.passage**: İndeksleme sırasında erişim görevlerinde büyük dökümanları kodlamak için kullanılır.
+ **classification**: Metin sınıflandırma görevleri için metni kodlamak amacıyla kullanılır.
+ **text-matching**: İki cümle arasındaki benzerliği ölçmek gibi benzerlik eşleştirme işlemleri için metni kodlamak amacıyla kullanılır.
+ **separation**: Kümeleme (clustering) veya yeniden sıralama (reranking) görevleri için kullanılır.

**Matryoshka Temsili Öğrenme (Matryoshka Representation Learning):**

`jina-embeddings-v3`, Matryoshka Temsili Öğrenmeyi destekleyerek kullanıcıların minimum performans kaybıyla embedding boyutunu kontrol etmelerine olanak tanır.
İstediğiniz boyutu seçmek için isteğinize `dimensions` parametresini ekleyin.
Varsayılan olarak **dimensions** 1024'e ayarlıdır, 256 ile 1024 arasında bir sayı önerilir.
Boyut ile performans arasındaki ipuçları için aşağıdaki tabloya bakabilirsiniz:

| Boyut | 32 | 64 | 128 | 256 | 512 | 768 | 1024 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Ortalama Erişim Performansı (nDCG@10) | 52.54 | 58.54 | 61.64 | 62.72 | 63.16 | 63.3 | 63.35 |

**Geniş Bağlamlı (Long-Context) Embedding Modellerinde Geç Parçalama (Late Chunking)**

`jina-embeddings-v3`, bağlamsal parça embedding'leri oluşturmak için modelin geniş bağlam yeteneklerinden yararlanma tekniği olan [Geç Parçalama (Late Chunking)](https://jina.ai/news/late-chunking-in-long-context-embedding-models/) yöntemini destekler. Bağlamsal parçalanmış temsili etkinleştirmek için isteğinize `late_chunking=True` ekleyin. True olarak ayarlandığında, Jina AI API girdi alanındaki tüm cümleleri birleştirecek ve bunları modele tek bir dizgi (string) olarak besleyecektir. Dahili olarak model, bu uzun birleştirilmiş dizgiyi gömer ve ardından geç parçalama gerçekleştirerek, girdi listesinin boyutuyla eşleşen bir embedding listesi döndürür.

```python
from llama_index.embeddings.jinaai import JinaEmbedding

text_embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-embeddings-v3",
    # pasaj (passage) embedding'lerini almak için `retrieval.passage` seçin
    task="retrieval.passage",
)

embeddings = text_embed_model.get_text_embedding("Gömülecek metin budur")
print("Metin boyutu:", len(embeddings))
print("Metin embedding sonucu:", embeddings[:5])

query_embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-embeddings-v3",
    # sorgu embedding'lerini almak için `retrieval.query` seçin veya istediğiniz görev türünü belirleyin
    task="retrieval.query",
    # `dimensions`, kullanıcıların minimum performans kaybıyla embedding boyutunu kontrol etmesine olanak tanır. varsayılan 1024'tür.
    # 256 ile 1024 arasında bir değer önerilir.
    dimensions=512,
)

embeddings = query_embed_model.get_query_embedding(
    "Gömülecek sorgu budur"
)
print("Sorgu boyutu:", len(embeddings))
print("Sorgu embedding sonucu:", embeddings[:5])
```

## JinaAI API aracılığıyla Jina CLIP ile görüntüleri ve sorguları gömme

Görüntülerinizi ve sorgularınızı da `JinaEmbedding` sınıfını kullanarak kodlayabilirsiniz.

```python
from llama_index.embeddings.jinaai import JinaEmbedding
from PIL import Image
import requests
from numpy import dot
from numpy.linalg import norm

embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-clip-v1",
)

image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStMP8S3VbNCqOQd7QQQcbvC_FLa1HlftCiJw&s"
im = Image.open(requests.get(image_url, stream=True).raw)
print("Görüntü:")
display(im)

image_embeddings = embed_model.get_image_embedding(image_url)
print("Görüntü boyutu:", len(image_embeddings))
print("Görüntü embedding sonucu:", image_embeddings[:5])

text_embeddings = embed_model.get_text_embedding(
    "Logo of a pink blue llama on dark background"
)
print("Metin boyutu:", len(text_embeddings))
print("Metin embedding sonucu:", text_embeddings[:5])

cos_sim = dot(image_embeddings, text_embeddings) / (
    norm(image_embeddings) * norm(text_embeddings)
)
print("Kosinüs benzerliği (Cosine similarity):", cos_sim)
```

## Toplu (Batch) Halde Gömme

Metinleri toplu olarak da gömebilirsiniz; toplu işlem boyutu, `embed_batch_size` parametresi ayarlanarak kontrol edilebilir (geçirilmezse varsayılan değer 10 olacaktır ve 2048'den büyük olmamalıdır).

```python
embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-embeddings-v3",
    embed_batch_size=16,
    task="retrieval.passage",
)

embeddings = embed_model.get_text_embedding_batch(
    ["Gömülecek metin budur", "Bir toplu işlemde daha fazla metin sağlanabilir"]
)

print(len(embeddings))
print(embeddings[0][:5])
```

## Jina AI Embedding'lerini kullanarak bir RAG boru hattı inşa edelim

#### Veriyi İndir

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### İçe Aktarmalar

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from llama_index.llms.openai import OpenAI
from llama_index.core.response.notebook_utils import display_source_node

from IPython.display import Markdown, display
```

#### Veriyi Yükle

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

#### İndeks İnşa Et

```python
your_openai_key = "OPENAI_ANAHTARINIZ"
llm = OpenAI(api_key=your_openai_key)
embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-embeddings-v3",
    embed_batch_size=16,
    task="retrieval.passage",
)

index = VectorStoreIndex.from_documents(
    documents=documents, embed_model=embed_model
)
```

#### Erişimciyi (Retriever) İnşa Et

```python
search_query_retriever = index.as_retriever()

search_query_retrieved_nodes = search_query_retriever.retrieve(
    "Tezden sonra ne oldu?"
)
```

```python
for n in search_query_retrieved_nodes:
    display_source_node(n, source_length=2000)
```