---
title: Deep Lake Vektör Deposu Hızlı Başlangıç
 | LlamaIndex OSS Belgeleri
---

# Deep Lake Vektör Deposu Hızlı Başlangıç

Deep Lake, pip kullanılarak kurulabilir.

```bash
%pip install llama-index-vector-stores-deeplake
```

```bash
!pip install llama-index
!pip install deeplake
```

Sırada, gerekli modülleri içe aktaralım ve gereken ortam değişkenlerini ayarlayalım:

```python
import os
import textwrap


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.deeplake import DeepLakeVectorStore


os.environ["OPENAI_API_KEY"] = "sk-********************************"
os.environ["ACTIVELOOP_TOKEN"] = "********************************"
```

Paul Graham'ın makalelerinden birini gömeceğiz ve yerel olarak saklanan bir Deep Lake Vektör Deposu'nda tutacağız. İlk olarak, verileri `data/paul_graham` adlı bir dizine indiriyoruz.

```python
import urllib.request


urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt",
    "data/paul_graham/paul_graham_essay.txt",
)
```

Artık kaynak veri dosyasından belgeler oluşturabiliriz.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(
    "Belge Kimliği (Document ID):",
    documents[0].doc_id,
    "Belge Hash'i:",
    documents[0].hash,
)
```

```text
Belge Kimliği (Document ID): a98b6686-e666-41a9-a0bc-b79f0d666bde Belge Hash'i: beaa54b3e9cea641e91e6975d2207af4f4200f4b2d629725d688f272372ce5bb
```

Son olarak, Deep Lake Vektör Deposu'nu oluşturalım ve verilerle dolduralım. `text (str)`, `metadata(json)`, `id (str, otomatik doldurulur)`, `embedding (float32)` tensorlarını oluşturan varsayılan bir tensor yapılandırması kullanıyoruz. [Tensor özelleştirilebilirliği hakkında daha fazlasını buradan öğrenin](https://docs.activeloop.ai/example-code/getting-started/vector-store/step-4-customizing-vector-stores).

```python
from llama_index.core import StorageContext


dataset_path = "./dataset/paul_graham"


# Belgeler üzerinde bir indeks oluşturun
vector_store = DeepLakeVectorStore(dataset_path=dataset_path, overwrite=True)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```text
Deep Lake veri kümesine veri yükleniyor.


100%|██████████| 22/22 [00:00<00:00, 684.80it/s]


Dataset(path='./dataset/paul_graham', tensors=['text', 'metadata', 'embedding', 'id'])


  tensor      htype      shape      dtype  compression
  -------    -------    -------    -------  -------
    text       text      (22, 1)      str     None
  metadata     json      (22, 1)      str     None
  embedding  embedding  (22, 1536)  float32   None
     id        text      (22, 1)      str     None
```

## Vektör Araması Yapma

Deep Lake, [bu öğreticilerde ayrıntılı olarak tartışılan](https://docs.activeloop.ai/example-code/tutorials/vector-store/vector-search-options) son derece esnek vektör araması ve hibrit arama seçenekleri sunar. Bu Hızlı Başlangıç kılavuzunda, varsayılan seçenekleri kullanan basit bir örnek gösteriyoruz.

```python
query_engine = index.as_query_engine()
response = query_engine.query(
    "Yazar ne öğrendi?",
)
```

```python
print(textwrap.fill(str(response), 100))
```

**Yazar, prestijli olmayan şeyler üzerinde çalışmanın iyi bir şey olabileceğini öğrendi; çünkü bu, gerçek bir şeyi keşfetmeye ve yanlış yoldan kaçınmaya yol açabilir. Yazar ayrıca cehaletin faydalı olabileceğini, çünkü bunun yeni ve beklenmedik bir şeyi keşfetmeye yol açabileceğini öğrendi. Ayrıca başkalarına örnek olmak için işin sevmediği kısımlarında bile çok çalışmanın önemini öğrendi. Yazar ayrıca istenmeyen tavsiyelerin değerini de öğrendi; örneğin Robert Morris'in, yazarın Y Combinator'ın yaptıkları son havalı şey olmadığından emin olması gerektiğini önermesi gibi beklenmedik şekillerde faydalı olabileceğini gördü.**

```python
response = query_engine.query("Yazar için zor bir an neydi?")
```

```python
print(textwrap.fill(str(response), 100))
```

**Yazar, IBM 1401 bilgisayarındaki programlarından biri sonlanmadığında zor bir an yaşadı. Veri merkezi yöneticisinin ifadesinin açıkça belirttiği gibi, bu teknik olduğu kadar sosyal bir hataydı.**

## Veritabanından öğeleri silme

Silinecek bir belgenin kimliğini bulmak için doğrudan temel Deep Lake veri kümesini sorgulayabilirsiniz.

```python
import deeplake


ds = deeplake.load(dataset_path)


idx = ds.id[0].numpy().tolist()
idx
```

```text
./dataset/paul_graham başarıyla yüklendi.


['42f8220e-673d-4c65-884d-5a48a1a15b03']
```

```python
index.delete(idx[0])
```
