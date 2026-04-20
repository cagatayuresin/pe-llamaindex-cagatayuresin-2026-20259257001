---
title: Epsilla Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Epsilla Vektör Deposu

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için [Epsilla](https://www.epsilla.com/)'nın nasıl kullanılacağını göstereceğiz.

Ön koşul olarak, çalışan bir Epsilla vektör veritabanına sahip olmanız (örneğin, docker imajımız aracılığıyla) ve `pyepsilla` paketini kurmanız gerekir. Belgelerin tamamını [buradan](https://epsilla-inc.gitbook.io/epsilladb/quick-start) görüntüleyebilirsiniz.

```bash
%pip install llama-index-vector-stores-epsilla
```

```bash
!pip/pip3 install pyepsilla
```

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
!pip install llama-index
```

```python
import logging
import sys


# Hata ayıklama günlüklerini görmek için yorum satırını kaldırın
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import SimpleDirectoryReader, Document, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.epsilla import EpsillaVectorStore
import textwrap
```

### OpenAI Kurulumu

Öncelikle OpenAI API anahtarını ekleyerek başlayalım. Bu anahtar, indekse yüklenen belgeler için gömmeler (embeddings) oluşturmak amacıyla kullanılacaktır.

```python
import openai
import getpass


OPENAI_API_KEY = getpass.getpass("OpenAI API Anahtarı:")
openai.api_key = OPENAI_API_KEY
```

### Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükleme

`SimpleDirectoryReader` kullanarak `/data/paul_graham` klasöründe saklanan belgeleri yükleyin.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge sayısı: {len(documents)}")
print(f"İlk belge, kimlik (id): {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
```

```text
Toplam belge sayısı: 1
İlk belge, kimlik (id): ac7f23f0-ce15-4d94-a0a2-5020fa87df61
İlk belge, hash: 4c702b4df575421e1d1af4b1fd50511b226e0c9863dbfffeccb8b689b8448f35
```

### İndeksi Oluşturma

Burada, önceden yüklenen belgeleri kullanarak Epsilla destekli bir indeks oluşturuyoruz. `EpsillaVectorStore` birkaç parametre alır:

- `client` (Any): Bağlanılacak Epsilla istemcisi.

- `collection_name` (str, isteğe bağlı): Hangi koleksiyonun kullanılacağı. Varsayılan olarak "llama_collection".

- `db_path` (str, isteğe bağlı): Veritabanının kalıcı hale getirileceği yol. Varsayılan olarak "/tmp/langchain-epsilla".

- `db_name` (str, isteğe bağlı): Yüklenen veritabanına bir ad verin. Varsayılan olarak "langchain_store".

- `dimension` (int, isteğe bağlı): Gömmelerin boyutu. Sağlanmazsa, koleksiyon oluşturma işlemi ilk ekleme (insert) sırasında yapılacaktır. Varsayılan olarak None.

- `overwrite` (bool, isteğe bağlı): Aynı ada sahip mevcut koleksiyonun üzerine yazılıp yazılmayacağı. Varsayılan olarak False.

Epsilla vektör veritabanı varsayılan olarak "localhost" ana makinesi ve "8888" portu ile çalışır.

```python
# Belgeler üzerinde bir indeks oluşturun
from pyepsilla import vectordb


client = vectordb.Client()
vector_store = EpsillaVectorStore(client=client, db_path="/tmp/llamastore")


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```text
[INFO] localhost:8888 adresine başarıyla bağlandı.
```

### Veriyi Sorgulama

Artık belgemiz indekste saklandığına göre, indekse karşı sorular sorabiliriz.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar kimdir?")
print(textwrap.fill(str(response), 100))
```

**Verilen bağlam bilgilerinin yazarı Paul Graham'dır.**

```python
response = query_engine.query("Yazar yapay zekayı (AI) nasıl öğrendi?")
print(textwrap.fill(str(response), 100))
```

**Yazar, yapay zekayı (AI) çeşitli kaynaklar aracılığıyla öğrendi. Bir kaynak, Heinlein'ın Mike adında zeki bir bilgisayarı konu alan "The Moon is a Harsh Mistress" (Ay Zalim Bir Sevgilidir) adlı romanıydı. Diğer bir kaynak, Terry Winograd'ın doğal dili anlayabilen bir program olan SHRDLU'yu kullandığını gösteren bir PBS belgeseliydi. Bu deneyimler yazarın yapay zekaya olan ilgisini artırdı ve onları o zamanlar yapay zekanın dili olarak kabul edilen Lisp'i kendi kendilerine öğrenmek de dahil olmak üzere bu konuda çalışmaya motive etti.**

Sırada, önceki verilerin üzerine yazmayı deneyelim.

```python
vector_store = EpsillaVectorStore(client=client, overwrite=True)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
single_doc = Document(text="Epsilla, kullandığımız vektör veritabanıdır.")
index = VectorStoreIndex.from_documents(
    [single_doc],
    storage_context=storage_context,
)


query_engine = index.as_query_engine()
response = query_engine.query("Yazar kimdir?")
print(textwrap.fill(str(response), 100))
```

**Verilen bağlamda yazar hakkında herhangi bir bilgi sağlanmamıştır.**

```python
response = query_engine.query("Hangi vektör veritabanı kullanılıyor?")
print(textwrap.fill(str(response), 100))
```

**Kullanılan vektör veritabanı Epsilla'dır.**

Daha sonra mevcut koleksiyona daha fazla veri ekleyelim.

```python
vector_store = EpsillaVectorStore(client=client, overwrite=False)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
for doc in documents:
    index.insert(document=doc)


query_engine = index.as_query_engine()
response = query_engine.query("Yazar kimdir?")
print(textwrap.fill(str(response), 100))
```

**Verilen bağlam bilgilerinin yazarı Paul Graham'dır.**

```python
response = query_engine.query("Hangi vektör veritabanı kullanılıyor?")
print(textwrap.fill(str(response), 100))
```

**Kullanılan vektör veritabanı Epsilla'dır.**
