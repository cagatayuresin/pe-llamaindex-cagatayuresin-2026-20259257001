---
title: MongoDB Atlas + Fireworks AI RAG Örneği
 | LlamaIndex OSS Belgeleri
---

# MongoDB Atlas + Fireworks AI RAG Örneği

Bu örnek, MongoDB Atlas'ı vektör deposu olarak ve Fireworks AI'yi LLM ve gömme (embedding) sağlayıcısı olarak kullanarak bir Erişim Destekli Nesil (Retrieval-Augmented Generation - RAG) sisteminin nasıl kurulacağını göstermektedir.

```bash
!pip install -q llama-index llama-index-vector-stores-mongodb llama-index-embeddings-fireworks==0.1.2 llama-index-llms-fireworks
!pip install -q pymongo datasets pandas
```

```python
# Fireworks.ai Anahtarını Ayarla
import os
import getpass


fw_api_key = getpass.getpass("Fireworks API Anahtarı:")
os.environ["FIREWORKS_API_KEY"] = fw_api_key
```

```python
from datasets import load_dataset
import pandas as pd


# https://huggingface.co/datasets/AIatMongoDB/whatscooking.restaurants
dataset = load_dataset("AIatMongoDB/whatscooking.restaurants")


# Veri setini bir pandas dataframe'ine dönüştür
dataset_df = pd.DataFrame(dataset["train"])


dataset_df.head(5)
```

|   | restaurant\_id | attributes                                          | cuisine  | DogsAllowed | embedding                                          | OutdoorSeating | borough       | address                                            | \_id                                 | name                   | menu                                               | TakeOut | location                                           | PriceRange | HappyHour | review\_count | sponsored | stars |
| - | -------------- | --------------------------------------------------- | -------- | ----------- | -------------------------------------------------- | -------------- | ------------- | -------------------------------------------------- | ------------------------------------ | ---------------------- | -------------------------------------------------- | ------- | -------------------------------------------------- | ---------- | --------- | ------------- | --------- | ----- |
| 0 | 40366661       | {'Alcohol': ''none'', 'Ambience': '{'romantic'...   | Tex-Mex  | None        | \[-0.14520384, 0.018315623, -0.018330636, -0.10... | True           | Manhattan     | {'building': '627', 'coord': \[-73.975980999999... | {'$oid': '6095a34a7c34416a90d3206b'} | Baby Bo'S Burritos     | None                                               | True    | {'coordinates': \[-73.97598099999999, 40.745132... | 1.0        | None      | 10            | NaN       | 2.5   |
| 1 | 40367442       | {'Alcohol': ''beer\_and\_wine'', 'Ambience': '{'... | American | True        | \[-0.11977468, -0.02157107, 0.0038846824, -0.09... | True           | Staten Island | {'building': '17', 'coord': \[-74.1350211, 40.6... | {'$oid': '6095a34a7c34416a90d3209e'} | Buddy'S Wonder Bar     | \[Grilled cheese sandwich, Baked potato, Lasagn... | True    | {'coordinates': \[-74.1350211, 40.6369042], 'ty... | 2.0        | None      | 62            | NaN       | 3.5   |
| 2 | 40364610       | {'Alcohol': ''none'', 'Ambience': '{'touristy'...   | American | None        | \[-0.1004329, -0.014882699, -0.033005167, -0.09... | True           | Staten Island | {'building': '37', 'coord': \[-74.138263, 40.54... | {'$oid': '6095a34a7c34416a90d31ff6'} | Great Kills Yacht Club | \[Mozzarella sticks, Mushroom swiss burger, Spi... | True    | {'coordinates': \[-74.138263, 40.546681], 'type... | 1.0        | None      | 72            | NaN       | 4.0   |
| 3 | 40365288       | {'Alcohol': None, 'Ambience': '{'touristy': Fa...   | American | None        | \[-0.11735515, -0.0397448, -0.0072645755, -0.09... | True           | Manhattan     | {'building': '842', 'coord': \[-73.970637000000... | {'$oid': '6095a34a7c34416a90d32017'} | Keats Restaurant       | \[French fries, Chicken pot pie, Mac & cheese, ... | True    | {'coordinates': \[-73.97063700000001, 40.751495... | 2.0        | True      | 149           | NaN       | 4.0   |
| 4 | 40363151       | {'Alcohol': None, 'Ambience': None, 'BYOB': No...   | Bakery   | None        | \[-0.096541286, -0.009661355, 0.04402167, -0.12... | True           | Manhattan     | {'building': '120', 'coord': \[-73.9998042, 40.... | {'$oid': '6095a34a7c34416a90d31fbd'} | Olive'S                | \[doughnuts, chocolate chip cookies, chocolate ... | True    | {'coordinates': \[-73.9998042, 40.7251256], 'ty... | 1.0        | None      | 7             | NaN       | 5.0   |

```python
from llama_index.core.settings import Settings
from llama_index.llms.fireworks import Fireworks
from llama_index.embeddings.fireworks import FireworksEmbedding


embed_model = FireworksEmbedding(
    embed_batch_size=512,
    model_name="nomic-ai/nomic-embed-text-v1.5",
    api_key=fw_api_key,
)
llm = Fireworks(
    temperature=0,
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    api_key=fw_api_key,
)


Settings.llm = llm
Settings.embed_model = embed_model
```

```python
import json
from llama_index.core import Document
from llama_index.core.schema import MetadataMode


# DataFrame'i bir JSON dizesi gösterimine dönüştür
documents_json = dataset_df.to_json(orient="records")
# JSON dizesini bir Python sözlük listesine yükle
documents_list = json.loads(documents_json)


llama_documents = []


for document in documents_list:
    # Meta veri değeri (str, int, float, None) tiplerinden biri olmalıdır
    document["name"] = json.dumps(document["name"])
    document["cuisine"] = json.dumps(document["cuisine"])
    document["attributes"] = json.dumps(document["attributes"])
    document["menu"] = json.dumps(document["menu"])
    document["borough"] = json.dumps(document["borough"])
    document["address"] = json.dumps(document["address"])
    document["PriceRange"] = json.dumps(document["PriceRange"])
    document["HappyHour"] = json.dumps(document["HappyHour"])
    document["review_count"] = json.dumps(document["review_count"])
    document["TakeOut"] = json.dumps(document["TakeOut"])
    # bu iki alan cevaplamak istediğimiz soruyla ilgili değil,
    # bu yüzden şimdilik atlıyorum
    del document["embedding"]
    del document["location"]


    # Metin ve llm/gömme modelleri için hariç tutulan meta verilerle bir Belge (Document) nesnesi oluşturun
    llama_document = Document(
        text=json.dumps(document),
        metadata=document,
        metadata_template="{key}=>{value}",
        text_template="Meta Veri: {metadata_str}\n-----\nİçerik: {content}",
    )


    llama_documents.append(llama_document)


# LLM ve Gömme modelinin girdi olarak ne aldığını gözlemleyelim
print(
    "\nLLM bunu görür: \n",
    llama_documents[0].get_content(metadata_mode=MetadataMode.LLM),
)
print(
    "\nGömme modeli bunu görür: \n",
    llama_documents[0].get_content(metadata_mode=MetadataMode.EMBED),
)
```

```python
from llama_index.core.node_parser import SentenceSplitter


parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(llama_documents)
# 25 bin düğüm yaklaşık 10 dakika sürer, bunu 2.5 bine indirgeyeceğiz
new_nodes = nodes[:2500]


# 25 bin belge olduğu için toplu işlem (batching) yapmamız gerekiyor.
# Neyse ki LlamaIndex gömme modelleri için iyi bir toplu işlem sunuyor
node_embeddings = embed_model(new_nodes)
```

```python
for idx, n in enumerate(new_nodes):
    n.embedding = node_embeddings[idx].embedding
    if "_id" in n.metadata:
        del n.metadata["_id"]
```

MongoDB Atlas üzerinde veritabanınızın, koleksiyonunuzun ve vektör arama indeksinizin kurulu olduğundan emin olun, aksi takdirde aşağıdaki adım MongoDB üzerinde düzgün çalışmaz.

- Veritabanı kümesi (cluster) kurulumu ve URI alma konusunda yardım için, bir MongoDB kümesi kurmak üzere [bu kılavuza](https://www.mongodb.com/docs/guides/atlas/cluster/) ve bağlantı dizginizi almak için [bu kılavuza](https://www.mongodb.com/docs/guides/atlas/connection-string/) bakın.

- Başarılı bir şekilde bir küme oluşturduktan sonra, MongoDB Atlas kümesi içinde "+ Create Database" seçeneğine tıklayarak veritabanını ve koleksiyonu oluşturun. Veritabanı `whatscooking` ve koleksiyon `restaurants` olarak adlandırılacaktır.

- MongoDB'den geliştirme ortamımıza verimli belge erişimi sağlamak için `restaurants` koleksiyonu içinde bir vektör arama indeksi oluşturmak şarttır. Bunun için vektör arama indeksi oluşturma hakkındaki resmi [kılavuza](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/) bakın.

```python
import pymongo
import os
import getpass


# MongoDB URI ayarla
mongo_uri = getpass.getpass("MONGO_URI:")
if not mongo_uri:
    print("MONGO_URI ayarlanmadı")


mongo_client = pymongo.MongoClient(mongo_uri)
async_mongo_client = pymongo.AsyncMongoClient(mongo_uri)


DB_NAME = "whatscooking"
COLLECTION_NAME = "restaurants"


db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]
```

```python
# Taze bir koleksiyonla çalıştığımızdan emin olmak için
# koleksiyondaki mevcut kayıtları silin
collection.delete_many({})
```

```python
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch


vector_store = MongoDBAtlasVectorSearch(
    mongodb_client=mongo_client,
    async_mongodb_client=async_mongo_client,
    db_name=DB_NAME,
    collection_name=COLLECTION_NAME,
    index_name="vector_index",
)
vector_store.add(new_nodes)
```

Şimdi burada arama indeksini doğru isimle oluşturduğunuzdan emin olun.

```python
from llama_index.core import VectorStoreIndex, StorageContext


index = VectorStoreIndex.from_vector_store(vector_store)
```

```bash
%pip install -q matplotlib
```

```python
import pprint
from llama_index.core.response.notebook_utils import display_response


query_engine = index.as_query_engine()


query = "arama sorgusu: İçinde alkol olmayan her şey"


response = query_engine.query(query)
display_response(response)
pprint.pprint(response.source_nodes)
```

**`Final Yanıtı:`** Sağlanan bağlama dayanarak, alkol servisi yapmayan iki restoran seçeneği şunlardır:

1. Brooklyn'deki "Academy Restauraunt"; Amerikan mutfağı sunmaktadır ve Mozzarella sticks, Cheeseburger, fırınlanmış patates, ekmek çubukları, Sezar salatası, tavuklu parmesan, Pigs in a blanket (milföyde sosis), tavuk çorbası, Mac & cheese, mantarlı İsviçre burgeri, köfteli spagetti ve patates püresi gibi çeşitli yemeklere sahiptir.

2. Manhattan'daki "Gabriel’S Bar & Grill"; İtalyan mutfağında uzmanlaşmıştır ve Peynirli Ravioli, Napoliten Pizza, çeşitli gelatolar, vejetaryen fırın ziti, vejetaryen brokoli pizzası, Lazanya, Buca Trio Platter, ıspanaklı ravioli, lor peynirli makarna, Spagetti, kızarmış kalamar ve Alfredo Pizza gibi yemekler sunmaktadır.

Her iki restoran da dış mekan oturma alanına sahiptir, çocuk dostudur ve gündelik kıyafet kuralına sahiptir. Ayrıca paket servis hizmeti sunarlar ve mutlu saatler (happy hour) promosyonları vardır.
