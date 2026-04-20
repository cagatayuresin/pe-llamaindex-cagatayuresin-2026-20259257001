# Saklama (Storing)

Verileri [yükledikten (loaded)](/python/framework/module_guides/loading) ve [indeksledikten (indexed)](/python/framework/module_guides/indexing) sonra, yeniden indeksleme zahmetinden ve maliyetinden kaçınmak için muhtemelen onları saklamak isteyeceksiniz. Varsayılan olarak, indekslenen verileriniz yalnızca bellekte (RAM) tutulur.

## Diske Kaydetme (Persisting to disk)

İndekslenmiş verilerinizi saklamanın en basit yolu, her İndeksin yerleşik `.persist()` metodunu kullanmaktır. Bu metod, tüm verileri belirtilen konumdaki diske yazar ve her tür indeks için çalışır.

```python
index.storage_context.persist(persist_dir="<kayit_dizini>")
```

İşte Birleştirilebilir Grafik (Composable Graph) için bir örnek:

```python
graph.root_index.storage_context.persist(persist_dir="<kayit_dizini>")
```

Daha sonra verileri yeniden yüklemekten ve yeniden indekslemekten şu şekilde kaçınabilirsiniz:

```python
from llama_index.core import StorageContext, load_index_from_storage

# depolama bağlamını (storage context) yeniden oluştur
storage_context = StorageContext.from_defaults(persist_dir="<kayit_dizini>")

# indeksi yükle
index = load_index_from_storage(storage_context)
```

> **Önemli:** Eğer indeksinizi özel `transformations`, `embed_model` vb. ile başlattıysanız, `load_index_from_storage` sırasında aynı seçenekleri geçmeniz veya bunları [global ayarlar](/python/framework/module_guides/supporting_modules/settings) olarak ayarlamış olmanız gerekir.

## Vektör Depolarını (Vector Stores) Kullanma

[İndeksleme](/python/framework/module_guides/indexing) bölümünde tartışıldığı gibi, en yaygın İndeks türlerinden biri VectorStoreIndex'tir. Bir VectorStoreIndex'te [gömmeleri (embeddings)](/python/framework/module_guides/indexing#embedding-nedir) oluşturmaya yönelik API çağrıları zaman ve maliyet açısından pahalı olabilir, bu nedenle her şeyi sürekli yeniden indekslemekten kaçınmak için onları saklamak isteyeceksiniz.

LlamaIndex; mimari, karmaşıklık ve maliyet açısından farklılık gösteren [çok sayıda vektör deposunu](/python/framework/module_guides/storing/vector_stores) destekler. Bu örnekte açık kaynaklı bir vektör deposu olan Chroma'yı kullanacağız.

Öncelikle chroma'yı kurmanız gerekecek:

```bash
pip install chromadb
```

Bir VectorStoreIndex'teki gömmeleri saklamak üzere Chroma'yı kullanmak için şunları yapmanız gerekir:

- Chroma istemcisini (client) başlatın
- Verilerinizi Chroma'da saklamak için bir Koleksiyon (Collection) oluşturun
- Chroma'yı bir `StorageContext` içinde `vector_store` olarak atayın
- VectorStoreIndex'inizi bu StorageContext'i kullanarak başlatın

İşte bu işlemin nasıl göründüğü ve verileri sorgulamaya dair kısa bir örnek:

```python
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# bazı dökümanları yükle
documents = SimpleDirectoryReader("./data").load_data()

# istemciyi başlat, verilerin kaydedileceği yolu ayarla
db = chromadb.PersistentClient(path="./chroma_db")

# koleksiyon oluştur
chroma_collection = db.get_or_create_collection("hizlibaslangic")

# bağlama vektör deposu olarak chroma'yı ata
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# indeksini oluştur
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# bir sorgu motoru oluştur ve sorgula
query_engine = index.as_query_engine()
response = query_engine.query("Hayatın anlamı nedir?")
print(response)
```

Eğer gömmelerinizi zaten oluşturduysanız ve sakladıysanız, dökümanlarınızı yüklemeden veya yeni bir VectorStoreIndex oluşturmadan onları doğrudan yüklemek isteyeceksiniz:

```python
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# istemciyi başlat
db = chromadb.PersistentClient(path="./chroma_db")

# koleksiyonu al
chroma_collection = db.get_or_create_collection("hizlibaslangic")

# bağlama vektör deposu olarak chroma'yı ata
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# saklanan vektörlerden indeksini yükle
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)

# bir sorgu motoru oluştur
query_engine = index.as_query_engine()
response = query_engine.query("llama2 nedir?")
print(response)
```

> **İpucu:** Bu depo (store) hakkında daha derinlere inmek isterseniz, [Chroma kullanımına dair daha kapsamlı bir örneğimiz](/python/examples/vector_stores/chromaindexdemo) mevcuttur.

### Sorgulamaya Hazırsınız!

Artık verileri yüklediniz, indekslediniz ve bu indeksi sakladınız; [verilerinizi sorgulamaya](/python/framework/module_guides/querying) hazırsınız.

## Döküman veya Node Ekleme

Zaten bir indeks oluşturduysanız, `insert` metodunu kullanarak indeksinize yeni dökümanlar ekleyebilirsiniz.

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex([])
for doc in documents:
    index.insert(doc)
```

Dökümanları yönetmeye dair daha fazla ayrıntı ve bir örnek notebook için [döküman yönetimi rehberine](/python/framework/module_guides/indexing/document_management) bakın.