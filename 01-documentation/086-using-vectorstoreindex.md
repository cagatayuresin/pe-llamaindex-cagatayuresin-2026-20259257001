# VectorStoreIndex Kullanımı

Vektör Depoları (Vector Stores), getirme ile zenginleştirilmiş oluşturmanın (RAG) temel bir bileşenidir; bu nedenle LlamaIndex kullanarak yaptığınız hemen hemen her uygulamada, doğrudan veya dolaylı olarak bunları kullanacaksınız.

Vektör depoları, bir [`Node` nesneleri](/python/framework/module_guides/loading/documents_and_nodes) listesini kabul eder ve bunlardan bir indeks oluşturur.

## Verileri İndekse Yükleme

### Temel Kullanım

Bir Vektör Deposunu kullanmanın en basit yolu, bir dizi döküman yüklemek ve `from_documents` yöntemini kullanarak bunlardan bir indeks oluşturmaktır:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Dökümanları yükle ve indeks oluştur
documents = SimpleDirectoryReader(
    "../../examples/data/paul_graham"
).load_data()
index = VectorStoreIndex.from_documents(documents)
```

> **İpucu:** Komut satırında `from_documents` kullanıyorsanız, indeks inşası sırasında bir ilerleme çubuğu görüntülemek için `show_progress=True` parametresini geçmek kullanışlı olabilir.

`from_documents` kullandığınızda, Dökümanlarınız parçalara ayrılır ve meta verileri ile ilişkileri takip eden metin dizeleri üzerindeki hafif soyutlamalar olan [`Node` nesnelerine](/python/framework/module_guides/loading/documents_and_nodes) dönüştürülür.

Dökümanların nasıl yükleneceği hakkında daha fazla bilgi için [Yüklemeyi Anlamak](/python/framework/module_guides/loading) bölümüne bakın.

Varsayılan olarak, VectorStoreIndex her şeyi bellekte saklar. Kalıcı vektör depolarının nasıl kullanılacağı hakkında daha fazla bilgi için aşağıdaki [Vektör Depolarını Kullanma](#using-vector-stores) bölümüne bakın.

> **İpucu:** Varsayılan olarak, `VectorStoreIndex`, vektörleri 2048 node'luk gruplar (batches) halinde oluşturacak ve ekleyecektir. Bellek kısıtlamanız varsa (veya fazla belleğiniz varsa), bunu `insert_batch_size=2048` parametresi ile istediğiniz grup boyutunu belirterek değiştirebilirsiniz.

Bu durum özellikle uzaktan barındırılan bir vektör veritabanına ekleme yaparken çok yardımcı olur.

### Node Oluşturmak İçin Veri Alma Boru Hattını (Ingestion Pipeline) Kullanma

Dökümanlarınızın nasıl indekslendiği üzerinde daha fazla kontrol sahibi olmak istiyorsanız, veri alma boru hattını (ingestion pipeline) kullanmanızı öneririz. Bu, node'ların parçalanmasını, meta verilerini ve gömülmesini (embedding) özelleştirmenize olanak tanır.

```python
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline, IngestionCache

# dönüşümlerle (transformations) boru hattını oluştur
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TitleExtractor(),
        OpenAIEmbedding(),
    ]
)

# boru hattını çalıştır
nodes = pipeline.run(documents=[Document.example()])
```

> **İpucu:** [Veri alma boru hattının nasıl kullanılacağı](/python/framework/module_guides/loading/ingestion_pipeline) hakkında daha fazla bilgi edinebilirsiniz.

### Node'ları Doğrudan Oluşturma ve Yönetme

İndeksiniz üzerinde tam kontrole sahip olmak istiyorsanız, [node'ları manuel olarak oluşturup tanımlayabilir](/python/framework/module_guides/loading/documents_and_nodes/usage_nodes) ve bunları doğrudan indeks yapılandırıcısına (constructor) geçirebilirsiniz:

```python
from llama_index.core.schema import TextNode

node1 = TextNode(text="<metin_parçası>", id_="<node_id>")
node2 = TextNode(text="<metin_parçası>", id_="<node_id>")
nodes = [node1, node2]
index = VectorStoreIndex(nodes)
```

#### Döküman Güncellemelerini Yönetme

İndeksinizi doğrudan yönetirken, zamanla değişen veri kaynaklarıyla başa çıkmak istersiniz. `Index` sınıfları **ekleme (insertion)**, **silme (deletion)**, **güncelleme (update)** ve **yenileme (refresh)** işlemlerine sahiptir ve bunlar hakkında daha fazla bilgiyi aşağıda bulabilirsiniz:

-   [Meta Veri Çıkarımı](/python/framework/module_guides/indexing/metadata_extraction)
-   [Döküman Yönetimi](/python/framework/module_guides/indexing/document_management)

## Vektör İndeksini Saklama

LlamaIndex, [onlarca vektör deposunu](/python/framework/module_guides/storing/vector_stores) destekler. Hangisinin kullanılacağını bir `StorageContext` nesnesi geçirerek ve bu nesnede de `vector_store` parametresini belirterek belirtebilirsiniz; işte Pinecone kullanan bir örnek:

```python
import pinecone
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.pinecone import PineconeVectorStore

# pinecone başlat
pinecone.init(api_key="<api_anahtarı>", environment="<ortam>")
pinecone.create_index(
    "baslangic", dimension=1536, metric="euclidean", pod_type="p1"
)

# vektör deposunu oluştur ve depolama bağlamını özelleştir
storage_context = StorageContext.from_defaults(
    vector_store=PineconeVectorStore(pinecone.Index("baslangic"))
)

# Dökümanları yükle ve indeks oluştur
documents = SimpleDirectoryReader(
    "../../examples/data/paul_graham"
).load_data()
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

VectorStoreIndex'in nasıl kullanılacağına dair daha fazla örnek için [vektör deposu indeksi kullanım örnekleri notebook'umuza](/python/framework/module_guides/indexing/vector_store_guide) bakın.

Belirli vektör depolarıyla VectorStoreIndex'in nasıl kullanılacağına dair örnekler için, "Depolama" (Storing) bölümü altındaki [vektör depolarına](/python/framework/module_guides/storing/vector_stores) bakın.

## Birleştirilebilir Getirme (Composable Retrieval)

`VectorStoreIndex` (ve diğer herhangi bir indeks/getirici), aşağıdakiler dahil olmak üzere genel nesneleri getirme yeteneğine sahiptir:

-   Node referansları
-   Sorgu motorları
-   Getiriciler (Retrievers)
-   Sorgu boru hatları (Query pipelines)

Eğer bu nesneler getirilirse, sağlanan sorgu kullanılarak otomatik olarak çalıştırılacaklardır.

Örneğin:

```python
from llama_index.core.schema import IndexNode

query_engine = other_index.as_query_engine()
obj = IndexNode(
    text="X, Y ve Z'yi tanımlayan bir sorgu motoru.",
    obj=query_engine,
    index_id="benim_sorgu_motorum",
)

index = VectorStoreIndex(nodes=nodes, objects=[obj])
retriever = index.as_retriever(verbose=True)
```

Sorgu motorunu içeren indeks node'u getirilirse, sorgu motoru çalıştırılacak ve ortaya çıkan yanıt bir node olarak döndürülecektir.

Daha fazla ayrıntı için [kılavuza](/python/examples/retrievers/composable_retrievers) göz atın.