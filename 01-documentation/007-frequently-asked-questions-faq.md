# Sıkça Sorulan Sorular (SSS)

> **İpucu:** Henüz yapmadıysanız, [LlamaIndex'i kurun](/python/framework/getting_started/installation) ve [başlangıç eğitimini](/python/framework/getting_started/starter_example) tamamlayın. Tanımadığınız terimlerle karşılaşırsanız, [üst düzey kavramlar](/python/framework/getting_started/concepts) bölümüne göz atın.

Bu bölümde, [başlangıç örneği](/python/framework/getting_started/starter_example) için yazdığınız koddan yola çıkarak, bu kodu kendi kullanım durumunuza göre özelleştirmenin en yaygın yollarını göstereceğiz:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

---

## **"Dökümanlarımı daha küçük parçalara (chunks) ayırmak istiyorum"**

```python
# Global ayarlar
from llama_index.core import Settings

Settings.chunk_size = 512

# Yerel ayarlar
from llama_index.core.node_parser import SentenceSplitter

index = VectorStoreIndex.from_documents(
    documents, transformations=[SentenceSplitter(chunk_size=512)]
)
```

---

## **"Farklı bir vektör deposu (vector store) kullanmak istiyorum"**

Öncelikle kullanmak istediğiniz vektör deposunu kurun. Örneğin, vektör deposu olarak Chroma kullanmak için pip ile kurabilirsiniz:

```bash
pip install llama-index-vector-stores-chroma
```

Mevcut tüm entegrasyonlar hakkında daha fazla bilgi edinmek için [LlamaHub](https://llamahub.ai) adresine göz atın.

Ardından bunu kodunuzda kullanabilirsiniz:

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

`StorageContext`, dökümanların, gömmelerin (embeddings) ve indekslerin saklandığı depolama arka ucunu tanımlar. [Depolama](/python/framework/module_guides/storing) ve [bunun nasıl özelleştirileceği](/python/framework/module_guides/storing/customization) hakkında daha fazla bilgi edinebilirsiniz.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

---

## **"Sorgulama yaptığımda daha fazla bağlam (context) getirmek istiyorum"**

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

`as_query_engine`, indeks üzerinde varsayılan bir `retriever` (getirici) ve `query engine` (sorgu motoru) oluşturur. `retriever` ve `query engine` yapılarını anahtar kelime argümanları (keyword arguments) geçerek yapılandırabilirsiniz. Burada, getiriciyi varsayılan 2 yerine en benzer 5 dökümanı döndürecek şekilde yapılandırıyoruz. [Getiriciler (retrievers)](/python/framework/module_guides/querying/retriever/retrievers) ve [sorgu motorları (query engines)](/python/framework/module_guides/querying/retriever) hakkında daha fazla bilgi edinebilirsiniz.

---

## **"Farklı bir LLM kullanmak istiyorum"**

```python
# Global ayarlar
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(
    model="mistral",
    request_timeout=60.0,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)

# Yerel ayarlar
index.as_query_engine(
    llm=Ollama(
        model="mistral",
        request_timeout=60.0,
        # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
        context_window=8000,
    )
)
```

[LLM'leri özelleştirme](/python/framework/module_guides/models/llms) hakkında daha fazla bilgi edinebilirsiniz.

---

## **"Farklı bir yanıt modu (response mode) kullanmak istiyorum"**

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(response_mode="tree_summarize")
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

[Sorgu motorları](/python/framework/module_guides/querying) ve [yanıt modları](/python/framework/module_guides/deploying/query_engine/response_modes) hakkında daha fazla bilgi edinebilirsiniz.

---

## **"Yanıtın akış (stream) şeklinde gelmesini istiyorum"**

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("Yazar büyürken ne yaptı?")
response.print_response_stream()
```

[Yanıt akışı (streaming responses)](/python/framework/module_guides/deploying/query_engine/streaming) hakkında daha fazla bilgi edinebilirsiniz.

---

## **"Soru-Cevap yerine bir sohbet robotu (chatbot) istiyorum"**

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_chat_engine()
response = query_engine.chat("Yazar büyürken ne yaptı?")
print(response)

response = query_engine.chat("Hımm ilginç, bana biraz daha anlat.")
print(response)
```

[Sohbet motoru (chat engine)](/python/framework/module_guides/deploying/chat_engines/usage_pattern) hakkında daha fazla bilgi edinebilirsiniz.

---

## Sonraki Adımlar

- Yapılandırabileceğiniz (neredeyse) her şeyin kapsamlı bir dökümünü mü istiyorsunuz? [LlamaIndex'i Anlama](/python/framework/understanding) bölümüyle başlayın.
- Belirli modüller hakkında daha derinlemesine bilgi mi istiyorsunuz? [Bileşen kılavuzlarını](/python/framework/module_guides) inceleyin.