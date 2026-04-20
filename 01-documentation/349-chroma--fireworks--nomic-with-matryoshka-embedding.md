# Matruşka (Matryoshka) Gömme ile Chroma + Fireworks + Nomic

---
title: Matruşka (Matryoshka) Gömme ile Chroma + Fireworks + Nomic
 | LlamaIndex OSS Belgeleri
---

Bu örnek, ChromaIndex örneğinden uyarlanmıştır ve Fireworks.ai üzerinde Nomic'in Matruşka (Matryoshka) gömmesinin nasıl kullanılacağını göstermektedir.

## Chroma

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

Chroma çeşitli modlarda çalışır. LangChain ile entegre edilmiş her bir mod için aşağıdaki örneklere bakın.

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

Tüm belgeleri [buradan](https://docs.trychroma.com/reference/Collection) inceleyebilirsiniz.

## Nomic

Nomic, maliyet hassasiyetinize bağlı olarak değişken gömme (embedding) boyutları döndürebilen yeni bir gömme modeli olan `nomic-ai/nomic-embed-text-v1.5`i yayınladı. Daha fazla bilgi için lütfen model sayfasını [buradan](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) ve web sitelerini [buradan](https://home.nomic.ai/) inceleyin.

## Fireworks.ai

Fireworks, önde gelen açık kaynaklı (OSS) model çıkarım (inference) sağlayıcısıdır. Bu örnekte hem nomic modelini çalıştırmak hem de sorgu motoru olarak `mixtral-8x7b-instruct` modelini kullanmak için Fireworks'ü kullanacağız. Fireworks hakkında daha fazla bilgi için lütfen web sitelerini [buradan](https://fireworks.ai) inceleyin.

## Temel Örnek (Basic Example)

Bu temel örnekte, Paul Graham'ın bir makalesini alıyoruz, parçalara ayırıyoruz, açık kaynaklı bir gömme modeli kullanarak gömüyoruz, Chroma'ya yüklüyoruz ve ardından sorguluyoruz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install -q llama-index-vector-stores-chroma llama-index-llms-fireworks llama-index-embeddings-fireworks==0.1.2
```

```text
Not: Güncellenmiş paketleri kullanmak için çekirdeği (kernel) yeniden başlatmanız gerekebilir.
```

```bash
%pip install -q llama-index
```

#### Chroma İndeksi Oluşturma

```bash
!pip install llama-index chromadb --quiet
!pip install -q chromadb
!pip install -q pydantic==1.10.11
```

```python
# içe aktar
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.llms.fireworks import Fireworks
from IPython.display import Markdown, display
import chromadb
```

```python
# Fireworks.ai Anahtarını kur
import getpass


fw_api_key = getpass.getpass("Fireworks API Anahtarı:")
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from llama_index.llms.fireworks import Fireworks
from llama_index.embeddings.fireworks import FireworksEmbedding


llm = Fireworks(
    temperature=0, model="accounts/fireworks/models/mixtral-8x7b-instruct"
)


# istemciyi ve yeni bir koleksiyonu oluştur
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")


# gömme fonksiyonunu tanımla
embed_model = FireworksEmbedding(
    model_name="nomic-ai/nomic-embed-text-v1.5",
)


# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


# ChromaVectorStore'u kur ve veriyi yükle
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)


# Veriyi Sorgula
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, büyürken öncelikle yazma ve programlama üzerine çalıştı. Pek iyi olmadığını itiraf ettiği kısa hikayeler yazarak işe başladı ve dokuzuncu sınıfta bir IBM 1401 üzerinde programlama yapmayı denedi. Ancak, girdi verisi eksikliği nedeniyle onunla ne yapacağını bilemediği için bunu kafa karıştırıcı buldu. Programlama ile ilgili ilk önemli deneyimi, doğrudan masasının başında kullanabildiği ve anında yanıt alabildiği mikrobilgisayarların gelişiyle oldu. Kendi mikrobilgisayarını yaptı ve daha sonra babasını bir TRS-80 almaya ikna etti. Basit oyunlar, model roketlerin ne kadar yükseğe uçacağını tahmin eden bir program ve bir kelime işlemci yazdı. Programlamaya olan ilgisine rağmen, başlangıçta üniversitede felsefe okumayı planladı ancak sonunda yapay zekaya (AI) geçti.**

## Temel Örnek (Diske kaydetme dahil) ve yeniden boyutlandırılabilir gömmeler

Önceki örneği genişleterek, diske kaydetmek isterseniz, Chroma istemcisini başlatmanız ve verilerin kaydedilmesini istediğiniz dizini iletmeniz yeterlidir.

`Dikkat`: Chroma verileri diske otomatik olarak kaydetmek için elinden geleni yapar, ancak birden fazla bellek içi istemci birbirinin işini bozabilir. En iyi uygulama olarak, her bir yol (path) için aynı anda yalnızca bir istemci çalıştırın.

Ayrıca gömmeleri 128 boyuta indireceğiz. Bu, veritabanı tarafında maliyet bilincine sahip olduğunuz durumlar için yararlıdır.

```python
# diske kaydet

db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


embed_model = FireworksEmbedding(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    api_base="https://api.fireworks.ai/inference/v1",
    dimensions=128,
)
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


# Kalıcı indeksten (persisted index) veri sorgula
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```
