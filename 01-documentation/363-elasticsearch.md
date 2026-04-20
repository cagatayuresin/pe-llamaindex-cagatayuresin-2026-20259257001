---
title: Elasticsearch
 | LlamaIndex OSS Belgeleri
---

# Elasticsearch

> [Elasticsearch](http://www.github.com/elastic/elasticsearch), hem tam metin (full-text) hem de vektör aramalarını destekleyen bir arama veritabanıdır.

## Temel Örnek

Bu temel örnekte, bir Paul Graham makalesini alıyoruz, parçalara ayırıyoruz, açık kaynaklı bir gömme (embedding) modeli kullanarak gömüyoruz, Elasticsearch'e yüklüyoruz ve ardından sorguluyoruz. Farklı erişme stratejilerini kullanan bir örnek için [Elasticsearch Vektör Deposu](https://docs.llamaindex.ai/en/stable/examples/vector_stores/elasticsearchindexdemo/) sayfasına bakabilirsiniz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install -qU llama-index-vector-stores-elasticsearch llama-index-embeddings-huggingface llama-index
```

```python
# içe aktarma
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import StorageContext
```

```python
# OpenAI kurulumu
import os
import getpass


os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Anahtarı:")
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget -nv 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


# gömme fonksiyonunu tanımla
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


# indeksi tanımla
vector_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # diğer kimlik doğrulama seçenekleri için Elasticsearch Vektör Deposu'na bakın
    index_name="paul_graham_essay",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
# Veriyi Sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
print(response)
```

**Yazar, okul dışında yazarlık ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve bir IBM 1401 bilgisayarında programlar yazmayı denedi. Ayrıca bir mikrobilgisayar kiti oluşturdu ve onun üzerinde basit oyunlar ve bir kelime işlemci yazarak programlama yapmaya başladı.**
