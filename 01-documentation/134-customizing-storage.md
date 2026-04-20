# Saklamayı Özelleştirme (Customizing Storage)

Varsayılan olarak LlamaIndex karmaşıklıkları gizler ve verilerinizi 5 satırdan kısa bir kodla sorgulamanıza olanak tanır:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Dökümanları özetle.")
```

Arka planda LlamaIndex; alınan dökümanların (yani `Node` nesneleri), embedding vektörlerinin ve indeks meta verilerinin nerede saklanacağını özelleştirmenize olanak tanıyan değiştirilebilir (swappable) bir **saklama katmanını** (storage layer) da destekler.

![](./../../_static/storage/storage.png)

### Düşük Seviye API (Low-Level API)

Bunu yapmak için üst düzey API yerine:

```python
index = VectorStoreIndex.from_documents(documents)
```

daha ince ayarlı kontrol sağlayan daha düşük düzeyli bir API kullanırız:

```python
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.node_parser import SentenceSplitter

# ayrıştırıcıyı oluştur ve dökümanı node'lara ayır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# varsayılan depoları kullanarak saklama bağlamını (storage context) oluştur
storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore(),
    vector_store=SimpleVectorStore(),
    index_store=SimpleIndexStore(),
)

# döküman deposunu oluştur (veya yükle) ve node'ları ekle
storage_context.docstore.add_documents(nodes)

# indeksi oluştur
index = VectorStoreIndex(nodes, storage_context=storage_context)

# indeksi kaydet
index.storage_context.persist(persist_dir="<kayit_dizini>")

# aynı klasöre birden fazla indeks kaydetmek için index_id de ayarlanabilir
index.set_index_id("<index_id>")
index.storage_context.persist(persist_dir="<kayit_dizini>")

# indeksi daha sonra yüklemek için saklama bağlamını kurduğunuzdan emin olun
# bu, kaydedilmiş depoları kayit_dizini'nden yükleyecektir
storage_context = StorageContext.from_defaults(persist_dir="<kayit_dizini>")

# ardından indeks nesnesini yükleyin
from llama_index.core import load_index_from_storage

loaded_index = load_index_from_storage(storage_context)

# birden fazla indeks içeren bir kayit_dizini'nden bir indeksi yüklüyorsanız
loaded_index = load_index_from_storage(storage_context, index_id="<index_id>")

# bir kayıt dizininden birden fazla indeksi yüklüyorsanız
loaded_indicies = load_index_from_storage(
    storage_context, index_ids=["<index_id>", ...]
)
```

Farklı döküman depoları, indeks depoları ve vektör depoları başlatmak için tek satırlık bir değişiklikle temel depolamayı özelleştirebilirsiniz.
Daha fazla detay için [Döküman Depoları (Document Stores)](/python/framework/module_guides/storing/docstores), [Vektör Depoları (Vector Stores)](/python/framework/module_guides/storing/vector_stores) ve [İndeks Depoları (Index Stores)](/python/framework/module_guides/storing/index_stores) kılavuzlarına bakın.

### Vektör Deposu Entegrasyonları ve Saklama

Vektör deposu entegrasyonlarımızın çoğu, tüm indeksi (vektörler + metin) vektör deposunun kendisinde saklar. Bu, vektör deposu zaten barındırıldığı ve verileri bizim indeksimizde kalıcı hale getirdiği için, yukarıda gösterildiği gibi indeksi açıkça kalıcı hale getirmek zorunda kalmamak gibi büyük bir avantaj sağlar.

Bu uygulamayı destekleyen vektör depoları şunlardır:

-   AzureAISearchVectorStore
-   ChatGPTRetrievalPluginClient
-   CassandraVectorStore
-   ChromaVectorStore
-   EpsillaVectorStore
-   DocArrayHnswVectorStore
-   DocArrayInMemoryVectorStore
-   JaguarVectorStore
-   LanceDBVectorStore
-   MetalVectorStore
-   MilvusVectorStore
-   MyScaleVectorStore
-   OpensearchVectorStore
-   PineconeVectorStore
-   QdrantVectorStore
-   TablestoreVectorStore
-   RedisVectorStore
-   UpstashVectorStore
-   WeaviateVectorStore

Pinecone kullanan küçük bir örnek aşağıdadır:

```python
import pinecone
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Pinecone indeksi oluşturma
api_key = "api_key"
pinecone.init(api_key=api_key, environment="us-west1-gcp")
pinecone.create_index(
    "quickstart", dimension=1536, metric="euclidean", pod_type="p1"
)
index = pinecone.Index("quickstart")

# vektör deposunu oluştur
vector_store = PineconeVectorStore(pinecone_index=index)

# saklama bağlamını oluştur
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# dökümanları yükle
documents = SimpleDirectoryReader("./data").load_data()

# dökümanları/vektörleri pinecone'a ekleyecek olan indeksi oluştur
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Verilerin halihazırda yüklü olduğu mevcut bir vektör deponuz varsa, ona bağlanabilir ve doğrudan bir `VectorStoreIndex` oluşturabilirsiniz:

```python
index = pinecone.Index("quickstart")
vector_store = PineconeVectorStore(pinecone_index=index)
loaded_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
```