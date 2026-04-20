# Bagel Network

---
title: Bagel Network
 | LlamaIndex OSS Belgeleri
---

> [Bagel](https://docs.bageldb.ai/), Yapay Zeka için Açık Çıkarım (Open Inference) Verisidir. Dağıtık Makine Öğrenimi hesaplaması için tasarlanmıştır. Yapay zeka veri altyapısı harcamalarını on kat azaltır.

[![Discord](https://img.shields.io/discord/1073293645303795742) ](https://discord.gg/bA7B6r97)  

- [Web Sitesi](https://www.bageldb.ai/)
- [Belgeler](https://docs.bageldb.ai/)
- [Twitter](https://twitter.com/bageldb_ai)
- [Discord](https://discord.gg/bA7B6r97)

Bagel'i şununla kurun:

Terminal penceresi

```bash
pip install bagelML
```

Diğer tüm veritabanları gibi şunları yapabilirsiniz:

- `.add` (ekle)
- `.get` (getir)
- `.delete` (sil)
- `.update` (güncelle)
- `.upsert` (güncelle veya ekle)
- `.peek` (gözat)
- `.modify` (değiştir)
- ve `.find` benzerlik aramasını çalıştırır.

## Temel Örnek (Basic Example)

Bu temel örnekte, bir Paul Graham makalesini alıyoruz, parçalara ayırıyoruz, açık kaynaklı bir gömme (embedding) modeli kullanarak gömüyoruz, Bagel'e yüklüyoruz ve ardından sorguluyoruz.

```bash
%pip install llama-index-vector-stores-bagel
%pip install llama-index-embeddings-huggingface
%pip install bagelML
```

```python
# içe aktar
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.bagel import BagelVectorStore
from llama_index.core import StorageContext
from IPython.display import Markdown, display
import bagel
from bagel import Settings
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
# sunucu ayarlarını oluştur
server_settings = Settings(
    bagel_api_impl="rest", bagel_server_host="api.bageldb.ai"
)


# istemciyi oluştur
client = bagel.Client(server_settings)


# koleksiyon (küme) oluştur
collection = client.get_or_create_cluster(
    "testing_embeddings", embedding_model="custom", dimension=384
)


# gömme fonksiyonunu tanımla
embed_model = "local:BAAI/bge-small-en-v1.5"


# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


# BagelVectorStore'u kur ve veriyi yükle
vector_store = BagelVectorStore(collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)


query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
print(f"<b>{response}</b>")
```

## Oluştur - Ekle - Getir (Create - Add - Get)

```python
def create_add_get(client):
    """
    Oluştur, ekle ve getir
    """
    name = "testing"


    # Bir küme (cluster) al veya oluştur
    cluster = client.get_or_create_cluster(name)


    # Kümeye belgeler ekle
    resp = cluster.add(
        documents=[
            "Bu belge 1'dir",
            "Bu bidhan'dır",
        ],
        metadatas=[{"source": "google"}, {"source": "notion"}],
        ids=[str(uuid.uuid4()), str(uuid.uuid4())],
    )


    # Sayıyı yazdır
    print("belge sayısı:", cluster.count())


    # İlk öğeyi getir
    first_item = cluster.peek(1)
    if first_item:
        print("1. öğeyi getir")


    print(">> create_add_get tamamlandı !\n")
```

## Oluştur - Ekle - Metne Göre Bul (Create - Add - Find by Text)

```python
def create_add_find(client):
    """
    Oluştur, ekle ve bul
    """
    name = "testing"


    # Bir küme al veya oluştur
    cluster = client.get_or_create_cluster(name)


    # Kümeye belgeler ekle
    cluster.add(
        documents=[
            "Bu bir belgedir",
            "Bu Towhid'dir",
            "Bu bir metindir",
        ],
        metadatas=[
            {"source": "notion"},
            {"source": "notion"},
            {"source": "google-doc"},
        ],
        ids=[str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())],
    )


    # Kümede benzer sonuçlar için sorgu yap
    results = cluster.find(
        query_texts=["Bu"],
        n_results=5,
        where={"source": "notion"},
        where_document={"$contains": "is"},
    )


    print(results)
    print(">> create_add_find tamamlandı  !\n")
```

## Oluştur - Ekle - Gömmelere Göre Bul (Create - Add - Find by Embeddings)

```python
def create_add_find_em(client):
    """Oluştur, ekle ve gömmeleri bul"""
    name = "testing_embeddings"
    # Bagel sunucusunu sıfırla
    client.reset()


    # Bir küme al veya oluştur
    cluster = api.get_or_create_cluster(name)
    # Kümeye gömmeleri ve diğer verileri ekle
    cluster.add(
        embeddings=[
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
        ],
        metadatas=[
            {"uri": "img1.png", "style": "style1"},
            {"uri": "img2.png", "style": "style2"},
            {"uri": "img3.png", "style": "style1"},
            {"uri": "img4.png", "style": "style1"},
            {"uri": "img5.png", "style": "style1"},
            {"uri": "img6.png", "style": "style1"},
            {"uri": "img7.png", "style": "style1"},
            {"uri": "img8.png", "style": "style1"},
        ],
        documents=[
            "doc1",
            "doc2",
            "doc3",
            "doc4",
            "doc5",
            "doc6",
            "doc7",
            "doc8",
        ],
        ids=["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8"],
    )


    # Sonuçlar için kümeyi sorgula
    results = cluster.find(query_embeddings=[[1.1, 2.3, 3.2]], n_results=5)


    print("bulma sonucu:", results)
    print(">> create_add_find_em tamamlandı  !\n")
```

## Oluştur - Ekle - Değiştir - Güncelle (Create - Add - Modify - Update)

```python
def create_add_modify_update(client):
    """
    Oluştur, ekle, değiştir ve güncelle
    """
    name = "testing"
    new_name = "new_" + name


    # Bir küme al veya oluştur
    cluster = client.get_or_create_cluster(name)


    # Küme adını değiştir
    print("Önce:", cluster.name)
    cluster.modify(name=new_name)
    print("Sonra:", cluster.name)


    # Kümeye belgeler ekle
    cluster.add(
        documents=[
            "Bu belge 1'dir",
            "Bu bidhan'dır",
        ],
        metadatas=[{"source": "notion"}, {"source": "google"}],
        ids=["id1", "id2"],
    )


    # Güncellemeden önce belge metaverilerini getir
    print("Güncellemeden önce:")
    print(cluster.get(ids=["id1"]))


    # Belge metaverilerini güncelle
    cluster.update(ids=["id1"], metadatas=[{"source": "google"}])


    # Güncellemeden sonra belge metaverilerini getir
    print("Kaynağı güncelledikten sonra:")
    print(cluster.get(ids=["id1"]))


    print(">> create_add_modify_update tamamlandı !\n")
```

## Oluştur - Upsert (Create - Upsert)

```python
def create_upsert(client):
    """
    Oluştur ve upsert (güncelle veya ekle)
    """
    # Bagel sunucusunu sıfırla
    api.reset()


    name = "testing"


    # Bir küme al veya oluştur
    cluster = client.get_or_create_cluster(name)


    # Kümeye belgeler ekle
    cluster.add(
        documents=[
            "Bu belge 1'dir",
            "Bu bidhan'dır",
        ],
        metadatas=[{"source": "notion"}, {"source": "google"}],
        ids=["id1", "id2"],
    )


    # Kümedeki belgeleri upsert et
    cluster.upsert(
        documents=[
            "Bu bir belgedir",
            "Bu google'dır",
        ],
        metadatas=[{"source": "notion"}, {"source": "google"}],
        ids=["id1", "id3"],
    )


    # Kümedeki belge sayısını yazdır
    print("Belge sayısı:", cluster.count())
    print(">> create_upsert tamamlandı !\n")
```
