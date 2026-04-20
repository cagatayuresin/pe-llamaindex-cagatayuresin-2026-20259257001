---
title: MongoDB Atlas + OpenAI RAG Örneği
 | LlamaIndex OSS Belgeleri
---

# MongoDB Atlas + OpenAI RAG Örneği

Bu örnek; MongoDB Atlas'ı vektör deposu olarak ve OpenAI'yi LLM ve gömme (embedding) sağlayıcısı olarak kullanarak bir Erişim Destekli Nesil (Retrieval-Augmented Generation - RAG) sisteminin nasıl kurulacağını göstermektedir.

```bash
!pip install llama-index
!pip install llama-index-vector-stores-mongodb
!pip install llama-index-embeddings-openai
!pip install pymongo
!pip install datasets
!pip install pandas
```

```python
%env OPENAI_API_KEY=OPENAI_API_ANAHTARINIZ
```

```python
from datasets import load_dataset
import pandas as pd


# https://huggingface.co/datasets/AIatMongoDB/embedded_movies
dataset = load_dataset("AIatMongoDB/embedded_movies")


# Veri setini bir pandas dataframe'ine dönüştür
dataset_df = pd.DataFrame(dataset["train"])


dataset_df.head(5)
```

|   | awards                                             | metacritic | rated  | fullplot                                          | title                 | writers                                            | languages  | plot                                              | plot\_embedding                                    | runtime | countries | genres                      | directors                             | cast                                               | type  | imdb                                        | poster                                              | num\_mflix\_comments |
| - | -------------------------------------------------- | ---------- | ------ | ------------------------------------------------- | --------------------- | -------------------------------------------------- | ---------- | ------------------------------------------------- | -------------------------------------------------- | ------- | --------- | --------------------------- | ------------------------------------- | -------------------------------------------------- | ----- | ------------------------------------------- | --------------------------------------------------- | -------------------- |
| 0 | {'nominations': 0, 'text': '1 win.', 'wins': 1}    | NaN        | None   | Young Pauline is left a lot of money when her ... | The Perils of Pauline | \[Charles W. Goddard (screenplay), Basil Dickey... | \[English] | Young Pauline is left a lot of money when her ... | \[0.00072939653, -0.026834568, 0.013515796, -0.... | 199.0   | \[USA]    | \[Action]                   | \[Louis J. Gasnier, Donald MacKenzie] | \[Pearl White, Crane Wilbur, Paul Panzer, Edwar... | movie | {'id': 4465, 'rating': 7.6, 'votes': 744}   | https\://m.media-amazon.com/images/M/MV5BMzgxOD...  | 0                    |
| 1 | {'nominations': 1, 'text': '1 nomination.', 'w\... | NaN        | TV-G   | As a penniless man worries about how he will m... | From Hand to Mouth    | \[H.M. Walker (titles)]                            | \[English] | A penniless young man tries to save an heiress... | \[-0.022837115, -0.022941574, 0.014937485, -0.0... | 22.0    | \[USA]    | \[Comedy, Short, Action]    | \[Alfred J. Goulding, Hal Roach]      | \[Harold Lloyd, Mildred Davis, 'Snub' Pollard, ... | movie | {'id': 10146, 'rating': 7.0, 'votes': 639}  | https\://m.media-amazon.com/images/M/MV5BNzE1OW\... | 0                    |
| 2 | {'nominations': 0, 'text': '1 win.', 'wins': 1}    | NaN        | None   | Michael "Beau" Geste leaves England in disgrac... | Beau Geste            | \[Herbert Brenon (adaptation), John Russell (ad... | \[English] | Michael "Beau" Geste leaves England in disgrac... | \[0.00023330493, -0.028511643, 0.014653289, -0.... | 101.0   | \[USA]    | \[Action, Adventure, Drama] | \[Herbert Brenon]                     | \[Ronald Colman, Neil Hamilton, Ralph Forbes, A... | movie | {'id': 16634, 'rating': 6.9, 'votes': 222}  | None                                                | 0                    |
| 3 | {'nominations': 0, 'text': '1 win.', 'wins': 1}    | NaN        | None   | A nobleman vows to avenge the death of his fat... | The Black Pirate      | \[Douglas Fairbanks (story), Jack Cunningham (a... | None       | Seeking revenge, an athletic young man joins t... | \[-0.005927917, -0.033394486, 0.0015323418, -0.... | 88.0    | \[USA]    | \[Adventure, Action]        | \[Albert Parker]                      | \[Billie Dove, Tempe Pigott, Donald Crisp, Sam ... | movie | {'id': 16654, 'rating': 7.2, 'votes': 1146} | https\://m.media-amazon.com/images/M/MV5BMzU0ND...  | 1                    |
| 4 | {'nominations': 1, 'text': '1 nomination.', 'w\... | NaN        | PASSED | The Uptown Boy, J. Harold Manners (Lloyd) is a... | For Heaven's Sake     | \[Ted Wilde (story), John Grey (story), Clyde B... | \[English] | An irresponsible young millionaire changes his... | \[-0.0059373598, -0.026604708, -0.0070914757, -... | 58.0    | \[USA]    | \[Action, Comedy, Romance]  | \[Sam Taylor]                         | \[Harold Lloyd, Jobyna Ralston, Noah Young, Jim... | movie | {'id': 16895, 'rating': 7.6, 'votes': 918}  | https\://m.media-amazon.com/images/M/MV5BMTcxMT...  | 0                    |

```python
# fullplot sütununun eksik olduğu veri noktalarını kaldırın
dataset_df = dataset_df.dropna(subset=["fullplot"])
print("\nKaldırma işleminden sonra her sütundaki eksik değerlerin sayısı:")
print(dataset_df.isnull().sum())


# Yeni OpenAI gömme modeli "text-embedding-3-small" ile yeni gömmeler oluşturacağımız için 
# veri setindeki her veri noktasından plot_embedding'i kaldırın
dataset_df = dataset_df.drop(columns=["plot_embedding"])


dataset_df.head(5)
```

```python
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=256)
llm = OpenAI()


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
    document["writers"] = json.dumps(document["writers"])
    document["languages"] = json.dumps(document["languages"])
    document["genres"] = json.dumps(document["genres"])
    document["cast"] = json.dumps(document["cast"])
    document["directors"] = json.dumps(document["directors"])
    document["countries"] = json.dumps(document["countries"])
    document["imdb"] = json.dumps(document["imdb"])
    document["awards"] = json.dumps(document["awards"])


    # Metin ve llm/gömme modelleri için hariç tutulan meta verilerle bir Belge (Document) nesnesi oluşturun
    llama_document = Document(
        text=document["fullplot"],
        metadata=document,
        excluded_llm_metadata_keys=["fullplot", "metacritic"],
        excluded_embed_metadata_keys=[
            "fullplot",
            "metacritic",
            "poster",
            "num_mflix_comments",
            "runtime",
            "rated",
        ],
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


for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding
```

MongoDB Atlas üzerinde veritabanınızın, koleksiyonunuzun ve vektör arama indeksinizin kurulu olduğundan emin olun, aksi takdirde aşağıdaki adım MongoDB üzerinde düzgün çalışmaz.

- Veritabanı kümesi (cluster) kurulumu ve URI alma konusunda yardım için, bir MongoDB kümesi kurmak üzere [bu kılavuza](https://www.mongodb.com/docs/guides/atlas/cluster/) ve bağlantı dizginizi almak için [bu kılavuza](https://www.mongodb.com/docs/guides/atlas/connection-string/) bakın.

- Başarılı bir şekilde bir küme oluşturduktan sonra, MongoDB Atlas kümesi içinde "+ Create Database" seçeneğine tıklayarak veritabanını ve koleksiyonu oluşturun. Veritabanı `movies` ve koleksiyon `movies_records` olarak adlandırılacaktır.

- `movies_records` koleksiyonu içinde bir vektör arama indeksi oluşturmak, MongoDB'den geliştirme ortamımıza verimli belge erişimi sağlamak için şarttır. Bunun için vektör arama indeksi oluşturma hakkındaki resmi [kılavuza](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/) bakın.

```python
import pymongo
from google.colab import userdata


mongo_uri = userdata.get("MONGO_URI")
if not mongo_uri:
    print("Ortam değişkenlerinde MONGO_URI ayarlanmadı")


mongo_client = pymongo.MongoClient(mongo_uri)
async_mongo_client = pymongo.AsyncMongoClient(mongo_uri)


DB_NAME = "movies"
COLLECTION_NAME = "movies_records"


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
vector_store.add(nodes)
```

```python
from llama_index.core import VectorStoreIndex, StorageContext


index = VectorStoreIndex.from_vector_store(vector_store)
```

```python
import pprint
from llama_index.core.response.notebook_utils import display_response


query_engine = index.as_query_engine(similarity_top_k=3)


query = "Noel sezonuna uygun romantik bir film önerin ve seçiminizi gerekçelendirin"


response = query_engine.query(query)
display_response(response)
pprint.pprint(response.source_nodes)
```

**`Final Yanıtı:`** "Romancing the Stone" (Amazon'da Sonsuz Aşk) filmi Noel sezonu için uygun bir romantik film olabilir. Bu, kaçırılan kız kardeşini kurtarmak için tehlikeli bir maceraya atılan bir romantizm yazarını takip eden romantik bir macera filmidir. Filmde romantizm, macera ve komedi unsurları bir arada bulunur ve bu da onu tatil sezonu için eğlenceli bir seçim haline getirir. Ek olarak, film olumlu eleştiriler almış ve ödüllere aday gösterilmiştir, bu da kalitesini gösterir.
