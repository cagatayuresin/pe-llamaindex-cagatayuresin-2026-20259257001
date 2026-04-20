# AwaDB Vektör Deposu (Vector Store)

---
title: AwaDB Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-embeddings-huggingface
%pip install llama-index-vector-stores-awadb
```

```bash
!pip install llama-index
```

## Bir AwaDB İndeksi Oluşturma

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

#### Belgeleri yükle, VectorStoreIndex'i oluştur

```python
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from IPython.display import Markdown, display
import openai


openai.api_key = ""
```

#### Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Veriyi Yükle

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.awadb import AwaDBVectorStore


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


vector_store = AwaDBVectorStore()
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)
```

#### İndeksi Sorgula

```python
# daha ayrıntılı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar büyürken kısa hikayeler yazdı, bir IBM 1401 üzerinde programlama denemeleri yaptı, babasını bir TRS-80 bilgisayar alması için ikna etti, basit oyunlar, model roketlerinin ne kadar yükseğe uçacağını tahmin eden bir program ve bir kelime işlemci yazdı. Ayrıca üniversitede felsefe okudu, yapay zekaya yöneldi ve web altyapısı oluşturma üzerinde çalıştı. Makaleler yazıp çevrimiçi yayınladı, her Perşembe akşamı bir grup arkadaşına akşam yemeği verdi, resim yaptı ve Cambridge'de bir bina satın aldı.**

```python
# daha ayrıntılı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query(
    "Yazar Y Combinator'daki zamanından sonra ne yaptı?"
)
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Y Combinator'daki zamanından sonra yazar makaleler yazdı, Lisp üzerinde çalıştı ve resim yaptı. Ayrıca Oregon'daki annesini ziyaret etti ve onun bir huzurevinden çıkmasına yardımcı oldu.**
