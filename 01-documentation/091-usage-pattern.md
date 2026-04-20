# Kullanım Kalıbı (Usage Pattern)

## Başlarken

Her veri yükleyici, o yükleyicinin nasıl kullanılabileceğini gösteren bir "Kullanım" (Usage) bölümü içerir. Her yükleyiciyi kullanmanın merkezinde, yükleyici dosyasını uygulamanız içinde kullanabileceğiniz bir modüle indiren `download_loader` fonksiyonu yer alır.

Örnek kullanım:

```python
from llama_index.core import VectorStoreIndex, download_loader
from llama_index.readers.google import GoogleDocsReader

gdoc_ids = ["1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec"]
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
query_engine.query("Yazar hangi okula gitti?")
```