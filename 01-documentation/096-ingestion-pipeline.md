# Veri Alma Boru Hattı (Ingestion Pipeline)

Bir `IngestionPipeline`, giriş verilerine uygulanan `Transformations` (Dönüşümler) kavramını kullanır. Bu `Transformations`, giriş verilerinize uygulanır ve ortaya çıkan node'lar ya geri döndürülür ya da (belirtilmişse) bir vektör veritabanına eklenir. Her node+dönüşüm çifti önbelleğe alınır; böylece aynı node+dönüşüm kombinasyonuyla yapılan sonraki çalıştırmalar (eğer önbellek kalıcı hale getirilmişse) önbelleğe alınmış sonucu kullanarak size zaman kazandırabilir.

`IngestionPipeline` kullanımına dair etkileşimli bir örnek görmek için [RAG CLI](/python/framework/getting_started/starter_tools/rag_cli) aracına göz atın.

## Kullanım Kalıbı (Usage Pattern)

En basit kullanım, bir `IngestionPipeline` nesnesini şu şekilde oluşturmaktır:

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

Gerçek dünya senaryosunda dökümanlarınızı `SimpleDirectoryReader` veya Llama Hub'dan başka bir okuyucu ile alacağınızı unutmayın.

## Vektör Veritabanlarına Bağlanma

Bir veri alma boru hattını çalıştırırken, ortaya çıkan node'ları otomatik olarak uzak bir vektör deposuna eklemeyi de seçebilirsiniz.

Daha sonra, bu vektör deposundan bir indeks oluşturabilirsiniz.

```python
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.qdrant import QdrantVectorStore

import qdrant_client

client = qdrant_client.QdrantClient(location=":memory:")
vector_store = QdrantVectorStore(client=client, collection_name="test_depos_u")

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TitleExtractor(),
        OpenAIEmbedding(),
    ],
    vector_store=vector_store,
)

# Doğrudan bir vektör veritabanına al (ingest)
pipeline.run(documents=[Document.example()])

# İndeksinizi oluşturun
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_vector_store(vector_store)
```

## Bir Boru Hattında Embedding Hesaplama

Yukarıdaki örnekte embedding'lerin boru hattının bir parçası olarak hesaplandığını unutmayın. Boru hattınızı bir vektör deposuna bağlıyorsanız, embedding'ler boru hattınızın bir aşaması olmalıdır; aksi takdirde daha sonra indeksi oluştururken hata alırsınız.

Bir vektör deposuna bağlanmıyorsanız, yani sadece bir node listesi üretiyorsanız, embedding'leri boru hattınızdan çıkarabilirsiniz.

## Önbelleğe Alma (Caching)

Bir `IngestionPipeline` içinde, her node + dönüşüm kombinasyonu hash'lenir ve önbelleğe alınır. Bu, aynı verileri kullanan sonraki çalıştırmalarda zaman kazandırır.

Aşağıdaki bölümler önbelleğe alma ile ilgili bazı temel kullanımları açıklamaktadır.

### Yerel Önbellek Yönetimi

Bir boru hattınız olduğunda, önbelleği saklamak ve yüklemek isteyebilirsiniz.

```python
# kaydet
pipeline.persist("./pipeline_depolama")

# durumu yükle ve geri yükle
new_pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TitleExtractor(),
    ],
)
new_pipeline.load("./pipeline_depolama")

# önbellek sayesinde anında çalışacaktır
nodes = pipeline.run(documents=[Document.example()])
```

Önbellek çok büyük hale gelirse temizleyebilirsiniz:

```python
# önbelleğin tüm içeriğini sil
cache.clear()
```

### Uzak Önbellek Yönetimi

Önbellekler için birden fazla uzak depolama arka ucunu destekliyoruz:

-   `RedisCache`
-   `MongoDBCache`
-   `FirestoreCache`

İşte `RedisCache` kullanan bir örnek:

```python
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache


ingest_cache = IngestionCache(
    cache=RedisCache.from_host_and_port(host="127.0.0.1", port=6379),
    collection="test_onbellegim",
)

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TitleExtractor(),
        OpenAIEmbedding(),
    ],
    cache=ingest_cache,
)

# Doğrudan veri al
nodes = pipeline.run(documents=[Document.example()])
```

Burada herhangi bir `persist` (kalıcı hale getirme) adımı gerekmez; çünkü her şey belirtilen uzak koleksiyonda işlem sırasında önbelleğe alınır.

## Asenkron Destek (Async Support)

`IngestionPipeline` ayrıca asenkron işlemleri de destekler:

```python
nodes = await pipeline.arun(documents=documents)
```

## Döküman Yönetimi

Veri alma boru hattına bir `docstore` (döküman deposu) eklemek döküman yönetimini etkinleştirir.

`document.doc_id` veya `node.ref_doc_id` değerlerini dayanak noktası olarak kullanarak, veri alma boru hattı aktif olarak kopya dökümanları arayacaktır.

Nasıl çalışır:

-   Bir `doc_id` -> `document_hash` eşlemesi saklar.
-   Bir vektör deposu bağlıysa:
    -   Bir kopya `doc_id` tespit edilirse ve hash değişmişse, döküman yeniden işlenir ve güncellenir (upserted).
    -   Bir kopya `doc_id` tespit edilirse ve hash değişmemişse, node atlanır.
-   Vektör deposu bağlı değilse:
    -   Her node için mevcut tüm hash'leri kontrol eder.
    -   Bir kopya bulunursa node atlanır.
    -   Aksi takdirde node işlenir.

**NOT:** Bir vektör deposu bağlamazsak, yalnızca kopya girişleri kontrol edebilir ve kaldırabiliriz.

```python
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.storage.docstore import SimpleDocumentStore

pipeline = IngestionPipeline(
    transformations=[...], docstore=SimpleDocumentStore()
)
```

Tam bir anlatımı [demo notebook](/python/examples/ingestion/document_management_pipeline) dosyamızda bulabilirsiniz.

Ayrıca [tüm veri alma yığını olarak Redis kullanan](/python/examples/ingestion/redis_ingestion_pipeline) başka bir kılavuza da göz atın.

## Paralel İşleme

`IngestionPipeline` nesnesinin `run` metodu paralel işlemlerle yürütülebilir.
Bu, node gruplarını işlemcilere dağıtan `multiprocessing.Pool` kullanarak yapılır.

Paralel işleme ile yürütmek için, `num_workers` parametresini kullanmak istediğiniz işlem sayısına ayarlayın:

```python
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[...],
)
pipeline.run(documents=[...], num_workers=4)
```

## Modüller

-   [Dönüşümler Kılavuzu](/python/framework/module_guides/loading/ingestion_pipeline/transformations)
-   [Gelişmiş Veri Alma Boru Hattı](/python/examples/ingestion/advanced_ingestion_pipeline)
-   [Asenkron Veri Alma Boru Hattı](/python/examples/ingestion/async_ingestion_pipeline)
-   [Döküman Yönetimi Boru Hattı](/python/examples/ingestion/document_management_pipeline)
-   [Redis Veri Alma Boru Hattı](/python/examples/ingestion/redis_ingestion_pipeline)
-   [Google Drive Veri Alma Boru Hattı](/python/examples/ingestion/ingestion_gdrive)
-   [Paralel Yürütme Boru Hattı](/python/examples/ingestion/parallel_execution_ingestion_pipeline)