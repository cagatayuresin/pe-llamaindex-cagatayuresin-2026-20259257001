---
title: DocArray Hnsw Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# DocArray Hnsw Vektör Deposu

[DocArrayHnswVectorStore](https://docs.docarray.org/user_guide/storing/index_hnswlib/), [DocArray](https://github.com/docarray/docarray) tarafından sağlanan, tamamen yerel olarak çalışan ve küçük ile orta ölçekli veri kümeleri için en uygun olan hafif bir Belge İndeksi (Document Index) uygulamasıdır. Vektörleri `hnswlib` içinde diskte saklar ve diğer tüm verileri `SQLite` içinde tutar.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-docarray
```

```bash
!pip install llama-index
```

```python
import os
import sys
import logging
import textwrap


import warnings


warnings.filterwarnings("ignore")


# huggingface uyarılarını durdur
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Hata ayıklama günlüklerini görmek için yorum satırını kaldırın
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    Document,
)
from llama_index.vector_stores.docarray import DocArrayHnswVectorStore
from IPython.display import Markdown, display
```

```python
import os


os.environ["OPENAI_API_KEY"] = "<openai anahtarınız>"
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(
    "Belge Kimliği (Document ID):",
    documents[0].doc_id,
    "Belge Hash'i:",
    documents[0].doc_hash,
)
```

```text
Belge Kimliği (Document ID): 07d9ca27-ded0-46fa-9165-7e621216fd47 Belge Hash'i: 77ae91ab542f3abb308c4d7c77c9bc4c9ad0ccd63144802b7cbe7e1bb3a4094e
```

## Başlatma ve İndeksleme

```python
from llama_index.core import StorageContext


vector_store = DocArrayHnswVectorStore(work_dir="hnsw_index")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = GPTVectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

## Sorgulama

```python
# Daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
print(textwrap.fill(str(response), 100))
```

**Yazar büyürken kısa hikayeler yazdı, bir IBM 1401 üzerinde programlama yaptı ve babasına kendisine bir TRS-80 mikrobilgisayar alması için ısrar etti. Basit oyunlar, model roketlerinin ne kadar yükseğe uçacağını tahmin eden bir program ve bir kelime işlemci yazdı. Ayrıca üniversitede felsefe okudu ancak bundan sıkıldıktan sonra yapay zekaya (AI) geçti. Daha sonra Harvard'da sanat dersleri aldı ve sanat okullarına başvurdu, sonunda RISD'ye devam etti.**

```python
response = query_engine.query("Yazar için zor bir an neydi?")
print(textwrap.fill(str(response), 100))
```

**Yazar için zor bir an, o zamanki yapay zeka (AI) programlarının bir aldatmaca olduğunu ve yapabildikleriyle doğal dili gerçekten anlamak arasında aşılamaz bir uçurum olduğunu fark etmesiydi.**

## Filtrelerle Sorgulama

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="Esaretin Bedeli (The Shawshank Redemption)",
        metadata={
            "yazar": "Stephen King",
            "tema": "Dostluk",
        },
    ),
    TextNode(
        text="Baba (The Godfather)",
        metadata={
            "yönetmen": "Francis Ford Coppola",
            "tema": "Mafya",
        },
    ),
    TextNode(
        text="Başlangıç (Inception)",
        metadata={
            "yönetmen": "Christopher Nolan",
        },
    ),
]
```

```python
from llama_index.core import StorageContext


vector_store = DocArrayHnswVectorStore(work_dir="hnsw_filters")
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = GPTVectorStoreIndex(nodes, storage_context=storage_context)
```

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="tema", value="Mafya")]
)


retriever = index.as_retriever(filters=filters)
retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```

```python
# oluşturulan indeksleri kaldır
import os, shutil


hnsw_dirs = ["hnsw_filters", "hnsw_index"]
for dir in hnsw_dirs:
    if os.path.exists(dir):
        shutil.rmtree(dir)
```
