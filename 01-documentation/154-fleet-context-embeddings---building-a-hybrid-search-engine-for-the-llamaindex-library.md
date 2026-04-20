# Fleet Context Embedding'leri - LlamaIndex Kütüphanesi İçin Hibrit Bir Arama Motoru Oluşturma

Bu kılavuzda, LlamaIndex dökümantasyonu için embedding'leri indirmek üzere Fleet Context'i kullanacağız ve üzerine hibrit bir yoğun/seyrek (dense/sparse) vektör erişim motoru inşa edeceğiz.

<br><br>

## Ön Koşullar

```bash
!pip install llama-index
!pip install --upgrade fleet-context
```

```python
import os
import openai

os.environ["OPENAI_API_KEY"] = "sk-..." # API anahtarınızı buraya ekleyin!
openai.api_key = os.environ["OPENAI_API_KEY"]
```

<br><br>

## Fleet Context'ten Embedding'leri İndirme

LlamaIndex dökümantasyonunun tamamı (~12k parça, ~100mb içerik) için embedding'leri indirmek üzere Fleet Context'i kullanacağız. Bir parametre olarak kütüphane adını belirterek en popüler 1220 kütüphaneden herhangi biri için indirme yapabilirsiniz. Desteklenen kütüphanelerin tam listesini sayfanın en altındaki [buradan](https://fleet.so/context) görebilirsiniz.

Bunu yapıyoruz çünkü Fleet; sayfadaki konum (yeniden sıralama - re-ranking için), parça türü (sınıf/fonksiyon/nitelik vb.), üst bölüm ve daha fazlası dahil olmak üzere erişimi ve üretimi daha iyi hale getirecek pek çok önemli bilgiyi koruyan bir embedding hattı (pipeline) oluşturmuştur. Bu konuda daha fazla bilgiyi [Github sayfalarından](https://github.com/fleet-ai/context/tree/main) okuyabilirsiniz.

```python
from context import download_embeddings

df = download_embeddings("llamaindex")
```

**Çıktı**:

```shell
    100%|██████████| 83.7M/83.7M [00:03<00:00, 27.4MiB/s]
                                         id  \
    0  e268e2a1-9193-4e7b-bb9b-7a4cb88fc735
    1  e495514b-1378-4696-aaf9-44af948de1a1
    2  e804f616-7db0-4455-9a06-49dd275f3139
    3  eb85c854-78f1-4116-ae08-53b2a2a9fa41
    4  edfc116e-cf58-4118-bad4-c4bc0ca1495e
```

```python
# Bazı meta veri örneklerini göster
df["metadata"][0]
display(Markdown(f"{df['metadata'][8000]['text']}"))
```

**Çıktı**:

```shell
classmethod from_dict(data: Dict[str, Any], kwargs: Any) → Self classmethod from_json(data_str: str, kwargs: Any) → Self classmethod from_orm(obj: Any) → Model json(, include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None, exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None, by_alias: bool = False, skip_defaults: Optional[bool] = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Optional[Callable[[Any], Any]] = None, models_as_dict: bool = True*, dumps_kwargs: Any) → unicode Generate a JSON representation of the model, include and exclude arguments as per dict().
```

<br><br>

## LlamaIndex'te Hibrit Arama İçin Pinecone İndeksi Oluşturma

Hem seyrek vektörler (sparse vectors) hem de yoğun vektörler (dense vectors) ile hibrit erişim yapabilmek için bir Pinecone indeksi oluşturacağız ve vektörlerimizi oraya yükleyeceğiz (upsert). Devam etmeden önce bir [Pinecone hesabınız](https://pinecone.io) olduğundan emin olun.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().handlers = []
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
import pinecone

api_key = "..."  # Pinecone API anahtarınızı buraya ekleyin
pinecone.init(
    api_key=api_key, environment="us-east-1-aws"
)  # Veritabanı bölgenizi buraya ekleyin
```

```python
# Fleet Context, OpenAI'nin 1536 boyutlu text-embedding-ada-002 modelini kullanır.

# NOT: Pinecone hibrit arama için dotproduct benzerliği gerektirir
pinecone.create_index(
    "quickstart-fleet-context",
    dimension=1536,
    metric="dotproduct",
    pod_type="p1",
)

pinecone.describe_index(
    "quickstart-fleet-context"
)  # Pinecone'da bir indeks oluşturduğunuzdan emin olun
```

<br>

```python
from llama_index.vector_stores.pinecone import PineconeVectorStore

pinecone_index = pinecone.Index("quickstart-fleet-context")
vector_store = PineconeVectorStore(pinecone_index, add_sparse_vector=True)
```

<br><br>

## Pinecone'a Vektörleri Toplu Olarak Yükleme (Batch Upsert)

Pinecone, bir seferde 100 vektör yüklemeyi önerir. Veri formatını biraz değiştirdikten sonra bunu yapacağız.

```python
import random
import itertools


def chunks(iterable, batch_size=100):
    """Bir yinelenebilir nesneyi batch_size boyutunda parçalara ayıran yardımcı fonksiyon."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


# birçok (id, vector, metadata, sparse_values) çifti üreten üreteç (generator)
data_generator = map(
    lambda row: {
        "id": row[1]["id"],
        "values": row[1]["values"],
        "metadata": row[1]["metadata"],
        "sparse_values": row[1]["sparse_values"],
    },
    df.iterrows(),
)

# Yükleme (upsert) başına 100 vektör ile verileri yükle
for ids_vectors_chunk in chunks(data_generator, batch_size=100):
    print(f"{len(ids_vectors_chunk)} vektör yükleniyor...")
    pinecone_index.upsert(vectors=ids_vectors_chunk)
```

<br><br>

## LlamaIndex'te Pinecone Vektör Deposunu Oluşturma

Son olarak, LlamaIndex aracılığıyla Pinecone vektör deposunu oluşturacağız ve sonuçları almak için sorgulayacağız.

```python
from llama_index.core import VectorStoreIndex
from IPython.display import Markdown, display
```

```python
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
```

<br><br>

## İndeksinizi Sorgulayın!

```python
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=8
)
response = query_engine.query("Nasıl llama_index SimpleDirectoryReader kullanırım?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Çıktı**:

```shell
<b>Llama_index içinde SimpleDirectoryReader kullanmak için, onu llama_index kütüphanesinden içe aktarmanız gerekir. İçe aktarıldıktan sonra, dizin yolunu bir argüman olarak sağlayarak SimpleDirectoryReader sınıfının bir örneğini oluşturabilirsiniz. Ardından, dökümanları belirtilen dizinden yüklemek için SimpleDirectoryReader örneği üzerindeki `load_data()` metodunu kullanabilirsiniz.</b>
```