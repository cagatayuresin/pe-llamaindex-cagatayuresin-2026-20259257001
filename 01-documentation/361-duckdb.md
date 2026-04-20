---
title: DuckDB
 | LlamaIndex OSS Belgeleri
---

> [DuckDB](https://duckdb.org/docs/api/python/overview), hızlı bir işlem içi (in-process) analitik veritabanıdır. DuckDB, MIT lisansı altındadır.

Bu not defterinde, DuckDB'nin LlamaIndex'te bir Vektör deposu olarak nasıl kullanılacağını göstereceğiz.

DuckDB'yi şununla kurun:

Terminal penceresi

```bash
pip install duckdb
```

En son DuckDB sürümünü (>= 0.10.0) kullandığınızdan emin olun.

Kalıcılığa bağlı olarak DuckDB'yi farklı modlarda çalıştırabilirsiniz:

- `in-memory` (bellek içi), veritabanının bellekte oluşturulduğu varsayılan moddur; vektör deposunu başlatırken `database_name = ":memory:"` değerini ayarlayarak bunun kullanılmasını zorlayabilirsiniz.
- `persistence` (kalıcılık), bir veritabanı adı belirlenerek ve bir kalıcılık dizini (`database_name = "vektor_depom.duckdb"`) ayarlanarak kurulur; burada veritabanı varsayılan `persist_dir` dizininde veya belirlediğiniz dizinde kalıcı hale getirilir.

Oluşturulan vektör deposu ile şunları yapabilirsiniz:

- `.add` (ekle)
- `.get` (getir)
- `.update` (güncelle)
- `.upsert` (ekle veya güncelle)
- `.delete` (sil)
- `.peek` (göz at)
- `.query` (sorgula) - arama çalıştırmak için.

## Temel örnek

Bu temel örnekte, Paul Graham makalesini alıyoruz, parçalara ayırıyoruz, açık kaynaklı bir gömme (embedding) modeli kullanarak gömüyoruz, `DuckDBVectorStore` içine yüklüyoruz ve ardından sorguluyoruz.

Gömme modeli olarak OpenAI kullanacağız.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
!pip install llama-index
```

### Bir DuckDB İndeksi Oluşturma

```bash
!pip install duckdb
!pip install llama-index-vector-stores-duckdb
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from llama_index.core import StorageContext


from IPython.display import Markdown, display
```

```python
# OpenAI API Kurulumu
import os
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
```

Örnek veri kümesini indirin ve hazırlayın

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
documents = SimpleDirectoryReader("data/paul_graham/").load_data()


vector_store = DuckDBVectorStore()
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, üniversiteden önce okul dışında iki ana şey üzerinde çalıştığını belirtiyor: yazarlık ve programlama. Kısa hikayeler yazdığını ve ayrıca bir IBM 1401 bilgisayarında program yazmayı denediğini söylüyor. Daha sonra bir mikrobilgisayar aldı ve daha kapsamlı bir şekilde programlama yapmaya başladı.**

## Diske kalıcı olarak kaydetme örneği

Önceki örneği genişleterek, diske kaydetmek istiyorsanız, bir veritabanı adı ve kalıcılık dizini belirterek `DuckDBVectorStore`'u başlatmanız yeterlidir.

```python
# Diske kaydetme
documents = SimpleDirectoryReader("data/paul_graham/").load_data()


vector_store = DuckDBVectorStore("pg.duckdb", persist_dir="./persist/")
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
# Diskten yükleme
vector_store = DuckDBVectorStore.from_local("./persist/pg.duckdb")
index = VectorStoreIndex.from_vector_store(vector_store)
```

```python
# Veriyi Sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, üniversiteden önce okul dışında iki ana şey üzerinde çalıştığını belirtiyor: yazarlık ve programlama. Kısa hikayeler yazdığını ve ayrıca bir IBM 1401 bilgisayarında program yazmayı denediğini söylüyor. Daha sonra bir mikrobilgisayar aldı ve daha kapsamlı bir şekilde programlama yapmaya başladı.**

## Meta veri filtresi örneği

Arama alanını meta verilerle filtreleyerek daraltmak mümkündür. Aşağıda bunu uygulamada gösteren bir örnek bulunmaktadır.

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        **{
            "text": "Esaretin Bedeli (The Shawshank Redemption)",
            "metadata": {
                "yazar": "Stephen King",
                "tema": "Dostluk",
                "yıl": 1994,
                "ref_doc_id": "doc_1",
            },
        }
    ),
    TextNode(
        **{
            "text": "Baba (The Godfather)",
            "metadata": {
                "yönetmen": "Francis Ford Coppola",
                "tema": "Mafya",
                "yıl": 1972,
                "ref_doc_id": "doc_1",
            },
        }
    ),
    TextNode(
        **{
            "text": "Başlangıç (Inception)",
            "metadata": {
                "yönetmen": "Christopher Nolan",
                "tema": "Bilim Kurgu",
                "yıl": 2010,
                "ref_doc_id": "doc_2",
            },
        }
    ),
]


vector_store = DuckDBVectorStore()
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Meta veri filtrelerini tanımlayın.

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="tema", value="Mafya")]
)
```

`metadatafilter` seçeneğini kullanmak için indeksi bir erişici (retriever) olarak kullanın.

```python
retriever = index.as_retriever(filters=filters)
retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
```
