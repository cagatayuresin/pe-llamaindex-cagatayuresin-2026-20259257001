---
title: ObjectBox Vektör Deposu Demosu
 | LlamaIndex OSS Belgeleri
---

# ObjectBox Vektör Deposu Demosu

Bu not defteri, LlamaIndex ile verimli, cihaz içi bir vektör deposu olarak [ObjectBox](https://objectbox.io/)'un kullanımını gösterecektir. Bir belge verildiğinde kullanıcının soru sorabildiği ve bir LLM'den doğal dilde ilgili cevaplar alabildiği basit bir RAG kullanım durumunu ele alacağız. RAG boru hattı (pipeline) aşağıdaki bileşenlerle yapılandırılacaktır:

- LlamaIndex'ten yerleşik bir [`SimpleDirectoryReader` okuyucusu](https://docs.llamaindex.ai/en/stable/examples/data_connectors/simple_directory_reader/)
- LlamaIndex'ten yerleşik bir [`SentenceSplitter` düğüm ayrıştırıcısı](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/sentence_splitter/)
- Gömme sağlayıcısı olarak [HuggingFace modelleri](https://docs.llamaindex.ai/en/stable/examples/embeddings/huggingface/)
- NoSQL ve vektör veri deposu olarak [ObjectBox](https://objectbox.io/)
- Uzak bir LLM hizmeti olarak Google'ın [Gemini](https://docs.llamaindex.ai/en/stable/examples/llm/gemini/) modeli

## 1) Bağımlılıkları Kurma

LlamaIndex ile birlikte kullanmak için HuggingFace ve Gemini entegrasyonlarını kuruyoruz.

```bash
!pip install llama_index_vector_stores_objectbox --quiet
!pip install llama-index --quiet
!pip install llama-index-embeddings-huggingface --quiet
!pip install llama-index-llms-gemini --quiet
```

## 2) Belgeleri İndirme

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## 3) RAG için Bir LLM Kurulumu (Gemini)

LLM olarak Google Gemini'nin bulut tabanlı API'sini kullanıyoruz. [Konsoldan](https://aistudio.google.com/app/apikey) bir API anahtarı alabilirsiniz.

```python
from llama_index.llms.gemini import Gemini
import getpass


gemini_key_api = getpass.getpass("Gemini API Anahtarı: ")
gemini_llm = Gemini(api_key=gemini_key_api)
```

## 4) RAG için Bir Gömme Modeli Kurulumu (HuggingFace `bge-small-en-v1.5`)

HuggingFace, [MTEB Liderlik Tablosu'ndan](https://huggingface.co/spaces/mteb/leaderboard) gözlemlenebilecek çeşitli gömme modellerine ev sahipliği yapmaktadır.

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


hf_embedding = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
embedding_dim = 384
```

## 5) Belgeleri ve Düğümleri Hazırlama

Bir RAG boru hattında ilk adım, verilen belgeleri okumaktır. Dizindeki dosya uzantısını kontrol ederek en iyi dosya okuyucusunu seçen `SimpleDirectoryReader`ı kullanıyoruz.

Ardından, `SimpleDirectoryReader` tarafından belgelerden okunan içeriklerden parçalar (metin alt dizileri) üretiyoruz. `SentenceSplitter`, metni `chunk_size` boyutundaki parçalara bölerken cümle sınırlarını koruyan bir metin bölücüdür.

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


reader = SimpleDirectoryReader("./data/paul_graham")
documents = reader.load_data()


node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
nodes = node_parser.get_nodes_from_documents(documents)
```

## 6) `ObjectBoxVectorStore` Yapılandırması

`ObjectBoxVectorStore` birkaç seçenekle başlatılabilir:

- `embedding_dim` (gerekli): Vektör veritabanının tutacağı gömmelerin boyutları
- `distance_type`: `COSINE`, `DOT_PRODUCT`, `DOT_PRODUCT_NON_NORMALIZED` ve `EUCLIDEAN` arasından seçim yapın
- `db_directory`: `.mdb` ObjectBox veritabanı dosyasının oluşturulması gereken dizinin yolu
- `clear_db`: `db_directory` üzerinde mevcut bir veritabanı dosyası varsa onu siler
- `do_log`: ObjectBox entegrasyonundan günlük kaydını (logging) etkinleştirir

```python
from llama_index.vector_stores.objectbox import ObjectBoxVectorStore
from llama_index.core import StorageContext, VectorStoreIndex, Settings
from objectbox import VectorDistanceType


vector_store = ObjectBoxVectorStore(
    embedding_dim,
    distance_type=VectorDistanceType.COSINE,
    db_directory="obx_data",
    clear_db=False,
    do_log=True,
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)


Settings.llm = gemini_llm
Settings.embed_model = hf_embedding


index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)
```

## 7) Belge ile Sohbet Etme

```python
query_engine = index.as_query_engine()
response = query_engine.query("Paul Graham kimdir?")
print(response)
```

## İsteğe Bağlı: `ObjectBoxVectorStore`u Erişici (Retriever) Olarak Yapılandırma

Bir LlamaIndex [erişicisi (retriever)](https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/), verilen bir sorguya göre bir vektör veritabanından benzer parçaları getirmekten sorumludur.

```python
retriever = index.as_retriever()
response = retriever.retrieve("Yazar büyürken neler yaptı?")


for node in response:
    print("Getirilen parça metni:\n", node.node.get_text())
    print("Getirilen parça meta verisi:\n", node.node.get_metadata_str())
    print("\n\n\n")
```

## İsteğe Bağlı: `delete_nodes` Kullanarak Tek Bir Sorguyla İlişkili Parçaları Kaldırma

Argüman olarak düğüm kimliklerini (node IDs) içeren bir liste sağlayarak vektör veritabanından parçaları (düğümleri) kaldırmak için `ObjectBoxVectorStore.delete_nodes` yöntemini kullanabiliriz.

```python
response = retriever.retrieve("Yazar büyürken neler yaptı?")


node_ids = []
for node in response:
    node_ids.append(node.node_id)
print(f"Kaldırılacak düğümler: {node_ids}")


print(f"Silme öncesi vektör sayısı: {vector_store.count()}")
vector_store.delete_nodes(node_ids)
print(f"Silme sonrası vektör sayısı: {vector_store.count()}")
```

## İsteğe Bağlı: Vektör Veritabanından Tek Bir Belgeyi Kaldırma

`ObjectBoxVectorStore.delete` yöntemi, `id_`si argüman olarak sağlanan tek bir belgeyle ilişkili parçaları (düğümleri) kaldırmak için kullanılabilir.

```python
document = documents[0]
print(f"Silinecek belge: {document.id_}")


print(f"Silme öncesi vektör sayısı: {vector_store.count()}")
vector_store.delete(document.id_)
print(f"Belge silme sonrası vektör sayısı: {vector_store.count()}")
```
