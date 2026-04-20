---
title: Chroma
 | LlamaIndex OSS Belgeleri
---

> [Chroma](https://docs.trychroma.com/getting-started), geliştirici üretkenliğine ve mutluluğuna odaklanan, yapay zeka odaklı (AI-native) açık kaynaklı bir vektör veritabanıdır. Chroma, Apache 2.0 lisansı altındadır.

[![Discord](https://img.shields.io/discord/1073293645303795742) ](https://discord.gg/MMeYNTmh3x)   [![Lisans](<https://img.shields.io/static/v1?label=license\&message=Apache 2.0\&color=white>) ](https://github.com/chroma-core/chroma/blob/master/LICENSE)   ![Entegrasyon Testleri](https://github.com/chroma-core/chroma/actions/workflows/chroma-integration-test.yml/badge.svg?branch=main)

- [Web Sitesi](https://www.trychroma.com/)
- [Belgeler](https://docs.trychroma.com/)
- [Twitter](https://twitter.com/trychroma)
- [Discord](https://discord.gg/MMeYNTmh3x)

Chroma tamamen tip tanımlı, tamamen test edilmiş ve tamamen belgelenmiştir.

Chroma'yı şununla kurun:

Terminal penceresi

```bash
pip install chromadb
```

Chroma çeşitli modlarda çalışır. LlamaIndex ile entegre edilmiş her bir mod için aşağıdaki örneklere bakın.

- `in-memory` (bellek içi) - bir python betiğinde veya jupyter not defterinde
- `in-memory with persistence` (kalıcılıkla bellek içi) - bir betikte veya not defterinde, diske kaydetme/yükleme özelliğiyle
- `in a docker container` (bir docker konteynerinde) - yerel makinenizde veya bulutta çalışan bir sunucu olarak

Diğer tüm veritabanları gibi şunları yapabilirsiniz:

- `.add` (ekle)
- `.get` (getir)
- `.update` (güncelle)
- `.upsert` (güncelle veya ekle)
- `.delete` (sil)
- `.peek` (gözat)
- ve `.query` benzerlik aramasını çalıştırır.

Tüm belgeleri [buradan](https://docs.trychroma.com/reference) inceleyebilirsiniz.

## Temel Örnek (Basic Example)

Bu temel örnekte, Paul Graham'ın bir makalesini alıyoruz, parçalara ayırıyoruz, açık kaynaklı bir gömme (embedding) modeli kullanarak gömüyoruz, Chroma'ya yüklüyoruz ve ardından sorguluyoruz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-chroma
%pip install llama-index-embeddings-huggingface
```

```bash
!pip install llama-index
```

#### Chroma İndeksi Oluşturma

```python
# içe aktar
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from IPython.display import Markdown, display
import chromadb
```

```python
# OpenAI kurulumu
import os
import getpass


os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Anahtarı:")
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# istemciyi ve yeni bir koleksiyonu oluştur
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")


# gömme fonksiyonunu tanımla
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")


# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


# ChromaVectorStore'u kur ve veriyi yükle
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)


# Veriyi Sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar büyürken yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve bir IBM 1401 bilgisayarında program yazmayı denedi. Daha sonra bir mikrobilgisayar edindi ve daha kapsamlı bir şekilde programlama yapmaya başladı.**

## Temel Örnek (Diske kaydetme dahil)

Önceki örneği genişleterek, diske kaydetmek isterseniz, Chroma istemcisini başlatmanız ve verilerin kaydedilmesini istediğiniz dizini iletmeniz yeterlidir.

`Dikkat`: Chroma verileri diske otomatik olarak kaydetmek için elinden geleni yapar, ancak birden fazla bellek içi istemci birbirinin işini bozabilir. En iyi uygulama olarak, her bir yol (path) için aynı anda yalnızca bir istemci çalıştırın.

```python
# diske kaydet


db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)


# diskten yükle
db2 = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db2.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)


# Kalıcı indeksten veri sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar büyürken yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve bir IBM 1401 bilgisayarında program yazmayı denedi. Daha sonra bir mikrobilgisayar edindi ve oyunlar ile bir kelime işlemci programlamaya başladı.**

## Temel Örnek (Docker Konteyneri kullanarak)

Ayrıca Chroma Sunucusunu ayrı bir Docker konteynerinde çalıştırabilir, ona bağlanmak için bir İstemci oluşturabilir ve ardından bunu LlamaIndex'e iletebilirsiniz.

Docker İmajını nasıl kopyalayacağınız, oluşturacağınız ve çalıştıracağınız aşağıda açıklanmıştır:

```bash
git clone git@github.com:chroma-core/chroma.git
docker-compose up -d --build
```

```python
# chroma istemcisini oluştur ve verilerimizi ekle
import chromadb


remote_db = chromadb.HttpClient()
chroma_collection = remote_db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)
```

```python
# Chroma Docker indeksinden veri sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar büyürken kısa hikayeler yazdı, bir IBM 1401'de programlama yaptı ve bir TRS-80 mikrobilgisayarında programlar yazdı. Ayrıca Harvard'da resim dersleri aldı ve bir ressamın fiili stüdyo asistanı olarak çalıştı. Ayrıca sanat galerilerini çevrimiçi hale getirmek için bir şirket kurmaya çalıştı ve çevrimiçi mağazalar oluşturmak için yazılım yazdı.**

## Güncelleme ve Silme (Update and Delete)

Gerçek bir uygulama yolunda ilerlerken, yalnızca veri eklemenin ötesine geçmek; verileri güncellemek ve silmek istersiniz.

Chroma, burada kayıt tutmayı (bookkeeping) basitleştirmek için kullanıcıların `ids` sağlamasına olanak tanır. `ids`, dosyanın adı veya `dosya_adi_paragrafNumarasi` gibi birleşik bir hash olabilir.

Çeşitli işlemlerin nasıl yapılacağını gösteren temel bir örnek aşağıdadır:

```python
doc_to_update = chroma_collection.get(limit=1)
doc_to_update["metadatas"][0] = {
    **doc_to_update["metadatas"][0],
    **{"author": "Paul Graham"},
}
chroma_collection.update(
    ids=[doc_to_update["ids"][0]], metadatas=[doc_to_update["metadatas"][0]]
)
updated_doc = chroma_collection.get(limit=1)
print(updated_doc["metadatas"][0])


# son belgeyi sil
print("önceki sayı", chroma_collection.count())
chroma_collection.delete(ids=[doc_to_update["ids"][0]])
print("sonraki sayı", chroma_collection.count())
```
