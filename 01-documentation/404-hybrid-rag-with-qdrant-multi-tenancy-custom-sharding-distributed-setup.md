---
title: Qdrant ile Hibrit RAG - çoklu kiralacı (multi-tenancy), özel parçalama (custom sharding), dağıtık kurulum
 | LlamaIndex OSS Belgeleri
---

# Qdrant ile Hibrit RAG: çoklu kiralacı (multi-tenancy), özel parçalama (custom sharding), dağıtık kurulum

## Neler oluşturacaksınız

Bu not defteri, çoklu kiralacı (multitenancy) ve özel parçalama (custom sharding) yoluyla dışa doğru ölçeklendirme için tasarlanmış LlamaIndex kullanarak Qdrant üzerinde üretim (production) tarzı bir Hibrit RAG uygular.

- Hibrit arama: daha yüksek geri çağırma (recall) ve kesinlik (precision) için yoğun (dense) gömmeler + seyrek (sparse) BM25.
- Çoklu kiralacı yapısı: yük algılama filtreleri (payload filters) ve parça yönlendirme (shard routing) kullanılarak kiracıları (tenants) izole eder.
- Özel parçalama: performans ve maliyet verimliliği için her bir kiracıyı yerel düzeyde tutar.
- Dağıtık Qdrant: yüksek bulunabilirlik (high availability) ve işlem hacmi (throughput) için replikasyona (replication) sahip çok düğümlü (multi-node) kurulum.

Bu not defteri, dağıtık bir hibrit arama arka ucu olarak Qdrant'ı ve orkestrasyon katmanı olarak LlamaIndex'i kullanan uçtan uca (end-to-end) bir Retrieval Augmented Generation (Erişim Artırılmış Üretim) iş akışını adım adım gösterir. Yoğun (dense) vektörleri seyrek sinyallerle (sparse signals) birleştiren, kiracıya duyarlı bir RAG oluşturacaksınız, filtrelerle kiracı başına verileri izole edeceksiniz ve ölçeklendirme için özel bir parça anahtarı (shard key) ile verileri ve sorguları yönlendireceksiniz.

## Bağımlılıkları kurun

### Bağımlılıklar hakkında

- llama-index: Veri alımı (ingestion), indeksleme ve geri getirme (retrieval) işlemleri için orkestrasyon katmanı.
- llama-index-vector-stores-qdrant: Hibrit destekli Qdrant entegrasyonu.
- fastembed: CPU dostu hafif gömme(embedding)/seyrek(sparse) modelleri

```bash
%pip install -U llama-index llama-index-vector-stores-qdrant fastembed
```

Sisteminizde çalışır durumda olan dağıtık bir Qdrant kümeniz olduğundan emin olun. İşte bir örnek `compose.yaml` dosyası:

```yaml
services:
  qdrant_primary:
    image: "qdrant/qdrant:latest"
    ports:
      - "6333:6333"
    environment:
      QDRANT__CLUSTER__ENABLED: "true"
    command: ["./qdrant", "--uri", "http://qdrant_primary:6335"]
    restart: always
  qdrant_secondary:
    image: "qdrant/qdrant:latest"
    environment:
      QDRANT__CLUSTER__ENABLED: "true"
    command: ["./qdrant", "--bootstrap", "http://qdrant_primary:6335"]
    restart: always
```

## İçe Aktarmalar (Imports) ve Genel Ayarlar

### Ayarlar ve bağlantı

- Gömmeler (Embeddings): `FastEmbedEmbedding('BAAI/bge-base-en-v1.5')` kompakt, yüksek kaliteli bir temel modeldir (baseline).
- Bağlantı: `QDRANT_URL` varsayılan olarak bir HTTP uç noktasına ayarlıdır; güvenli/bulut (secured/cloud) yapılandırmalar için `QDRANT_API_KEY` değişkenini ayarlayın.

```python
import os


from qdrant_client import AsyncQdrantClient, QdrantClient
from qdrant_client import models


from llama_index.core import (
    Settings,
    VectorStoreIndex,
    Document,
    StorageContext,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding


# Gömme Modelleri, küçük ve hızlı
Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")


# Qdrant bağlantısı, varsayılan olarak yereldir (local), bulut için QDRANT_URL ve QDRANT_API_KEY'i ayarlayın.
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


client: QdrantClient = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
aclient: AsyncQdrantClient = AsyncQdrantClient(
    url=QDRANT_URL, api_key=QDRANT_API_KEY
)
COLLECTION = "hybrid_rag_multitenant_sharding_demo"
```

## Dağıtıma hazır bir koleksiyon oluşturun

### Çift vektörlü şemayı (yoğun + seyrek) yapılandırın

- Vektör alanı (vector field) adlarını tanımlayın: Gömmeler için `dense` ve BM25 tarzı sinyaller için `sparse` kullanın.

- Yoğun yapılandırma (Dense config):

  - Gömme işleminin boyutunu sabit kodlama (hardcoding) yapmaktan kaçınarak, çalışma zamanında `Settings.embed_model` yöntemini yoklayarak (probing) belirleyin.
  - Anlamsal benzerlik (semantic similarity) işlemleri için kosinüs mesafesini (cosine distance) kullanın.

- Seyrek yapılandırma (Sparse config):
  - Hibrit puanlama yeteneklerini desteklemek için bellek içi bir seyrek indeks (in-memory sparse index) etkinleştirin (`on_disk=False`).

- Bu ayarlar, QdrantVectorStore tarafından hibrit vektör çağrımı/getirimi için daha sonra kullanılacak olan koleksiyonun çift indeksli yapısını oluşturur.

```python
dense_vector_name = "dense"
dense_config = models.VectorParams(
    size=len(Settings.embed_model.get_text_embedding("probe")),
    distance=models.Distance.COSINE,
)
sparse_vector_name = "sparse"
sparse_config = models.SparseVectorParams(
    index=models.SparseIndexParams(on_disk=False)
)
```

### Parça anahtarları (Shard keys) ve seçici sözleşmesi (selector contract)

- `shard_keys`: \[‘tenant\_a’, ‘tenant\_b’] — Her bir kiracıyı yerel seviyelerde muhafaza etmek için özel parçalama (custom sharding) işleminde kullanılan önceden tanımlanmış bölümler.
- `payload_indexes`: Filtre tabanlı sorgu süreçlerini hızlandırmak için `tenant_id` bazlı anahtar kelime indeksi (keyword index).
- `shard_key_selector_fn(tenant_id) -> tenant_id`: Hem yazma hem de okuma işlemleri için kullanılan parça anahtarını (shard key) döndürür.

```python
shard_keys = ["tenant_a", "tenant_b"]
payload_indexes = [
    {
        "field_name": "tenant_id",
        "field_schema": models.PayloadSchemaType.KEYWORD,
    }
]




def shard_key_selector_fn(tenant_id: str) -> models.ShardKeySelector:
    return tenant_id
```

### Özel parçalama (custom sharding) içeren hibrit Qdrant deposunu (store) başlatın

Bu adım, `COLLECTION` değişkeni içindeki koleksiyonu yaratır veya ona bağlanır. İki vektörlü hibrit depoyu ise şöyle yapılandırır:

- Hibrit arama: `dense_vector_name='dense'` ve `sparse_vector_name='sparse'` yapıları eşliğinde `enable_hybrid=True`.

- Yoğun konfigürasyon: `dense_config` değişkeni kosinüs uzaklığını kullanır ve verilerin boyutunu `Settings.embed_model` ile belirler.

- Seyrek konfigürasyon: `sparse_config` bellek üzerinde bir indeks açar; `fastembed_sparse_model='Qdrant/bm25'` ise BM25 tarzı sinyalleri işleme alır.

- Dağıtık (Distributed) topoloji:

  - `shard_keys=['tenant_a','tenant_b']` kullanılarak `sharding_method=Custom`.
  - `shard_key_selector_fn(tenant_id) -> tenant_id` mekanizması işlemleri ve sorguları doğru yönlendirir.
  - Ölçeklendirme ve 'Yüksek Bulunabilirlik' (HA) için `shard_number=6`, `replication_factor=2`.

- Yük indeksi: `payload_indexes` değişkeni, filtrelemeyi `tenant_id` temelinde hızlandırmakla görevlidir.

Eşkuvvetlilik (Idempotent) karakteristiği: Vektör deposu mevcut değilse yeni bir tane yaratacak, bir sonraki işlemlerde aynısını kullanacaktır.

```python
vector_store = QdrantVectorStore(
    collection_name=COLLECTION,
    client=client,
    aclient=aclient,
    dense_vector_name=dense_vector_name,
    sparse_vector_name=sparse_vector_name,
    enable_hybrid=True,
    dense_config=dense_config,
    sparse_config=sparse_config,
    fastembed_sparse_model="Qdrant/bm25",
    shard_number=6,
    sharding_method=models.ShardingMethod.CUSTOM,
    shard_key_selector_fn=shard_key_selector_fn,
    shard_keys=shard_keys,
    replication_factor=2,
    payload_indexes=payload_indexes,
)
```

## Çok kiracılı veri kümesini hazırlayın

Birbiri içerisine giren küçük gruplar halindeki belge setleri ile iki ayrı kiracı grubu meydana getiriyoruz. Her `Document` sınıfı bir tenant\_id, etiket (tags) listesi, ve bir tanımlayıcı belge (doc\_id) içerir.

### Veri kümesi tasarımı (Dataset design) ve genişletilebilirlik (extensibility)

Her bir metin bloğu için, birbirinden izole ve kısa birer parçadan oluşan ve iki ayrı bölüm (kiracı grubu) barındıran bir modeli simüle ediyoruz. Bu kapsamda `Document` şunları taşır:

- Bölme yönlendirmesi (shard routing) ve izolasyon için `tenant_id`,
- Çözümleme/Sorun giderme ile kolay filtreleme yapabilmek için `tags`,
- Yoğun/Seyrek indeksleme süreçlerinde yer bulan içerikler için de `text` formatı kullanılır.

```python
TENANT_DOCS: dict[str, list[Document]] = {
    "tenant_a": [
        Document(
            text="Güneş panelleri, karbon ayakizini azaltır ve elektrik kullanım faturalarındaki masrafları düşürür",
            metadata={"tenant_id": "tenant_a", "tags": ["energy", "solar"]},
        ),
        Document(
            text="İnvertörler doğru akımı ev aletleri için alternatif bir sisteme dönüştürür",
            metadata={"tenant_id": "tenant_a", "tags": ["energy", "hardware"]},
        ),
        Document(
            text="Elektrik dağıtıcıların belirlediği fatura (Net metering policies) oranları bölgelere göre değişiklik arz eder",
            metadata={
                "tenant_id": "tenant_a",
                "tags": ["policy", "regulation"],
            },
        ),
    ],
    "tenant_b": [
        Document(
            text="Kubernetes clusterlar üzerinde iş konteynerlerini organize ve koordine eder",
            metadata={"tenant_id": "tenant_b", "tags": ["cloud", "k8s"]},
        ),
        Document(
            text="Servis kafesleri ile işlerin gözlemlenebilmesi ve çalışma trafiğinin kontrolü sağlanır",
            metadata={
                "tenant_id": "tenant_b",
                "tags": ["cloud", "networking"],
            },
        ),
        Document(
            text="Helm şemaları kurgularınızdaki Kubernetes verilerini toplar ve deploy eder",
            metadata={"tenant_id": "tenant_b", "tags": ["cloud", "devops"]},
        ),
    ],
}
```

## Hedef bölge odaklı yollarla verilerinizi entegre edin (Ingest with shard key for locality)

Etkin Settings.embed\_model metodolojisiyle (methodology) metin içeriğimizi uyumlu hale getiriyor ve bunu ilgili paylar ile (payload & shard key) Upsert işlemini yapıp, verileri kümeye işliyoruz. Sistem bu yöntemi izleyerek verilerin küme içindeki bir (tenant) shard (parça) bölümü ile lokal baz üzerinde eş değer olmasını temin eder.

### Gömme stratejisi (Embedding strategy)

- FastEmbed, bu test için işlemci (CPU) dostu yapıyı sağlar. Daha kurumsal kullanımlar göz önüne alındığında, bir hizmet planlayıcısını (ör. text-embedding-3-large modelini kullanmak) veya kendi üretiminizi gerçekleştirdiğiniz yapıyı hayata geçirip; daha sonra gömme çıktılarınızı ön bellekte tasnif etmeniz önerilir (cache).
- Sisteminize entegre edip kullandığınız modeli (gömmeleri) değiştirirseniz, sistem modeline denklik getirmesini sağlamak amacıyla `dense_config.size` komutundaki girdileri güncellemeli ve re-index yapılarını tekrar incelemelisiniz.
- Notebook üzerindeki işlemler boyunca gömme tasniflerinizi sürekli biçimde çalıştırmaktan genel itibarıyla kaçının ve bunu daha çok birleştirilmiş verileri (persist) bellek üzerinden (cache) okuyarak hızını artırmak adına dizayn edin.

```python
def create_dense_embeddings(docs: list[Document]) -> list[Document]:
    for doc in docs:
        doc.embedding = Settings.embed_model.get_text_embedding(doc.text)
    return docs
```

### Veri alım süreci (Ingestion flow) ve bölgesel garantiler

- Sisteme eklediğimiz (configured) her bir gömme blokajını (embedding block) metotlar üzerinden (dense ile belirterek) düzenler ve Vector Store komutları (sparse representation) sistem kütüphaneleriyle ile işlemesini kurarız.
- Yazılımsal süreç, ilgili belgelerin `shard_identifier=tenant_id` kod yapısıyla bir hedef veya bölümü dikkate (shard groups) alarak işleme alır.

Not (Tip): Yoğun bilgi alımları esnasında async ingestion mantığını oluşturmayı göz önüne alın (ters akışlı (backpressure control) durumunu aşabilmek için bilgi süzgeci tasnif blokajları ile verilerinizi işleyin).

```python
for tenant_id, docs in TENANT_DOCS.items():
    docs = create_dense_embeddings(docs)
    await vector_store.async_add(docs, shard_identifier=tenant_id)
```

### Index sarmalama işlemleri ve yeniden kullanımı (reusability)

`StorageContext.from_defaults(vector_store=vector_store)` komutu, sistemde veri tabanını (re-ingesting methodu ile) tekrar işlemden geçirmeden evvel Qdrant veri indeksindeki LlamaIndex’s `VectorStoreIndex` bağını yürürlüğe alır (kurar).

Faydaları:

- Tekil parçacık sistemleri çerçevesindeki verileri aynı birleşik küme ile sorgu yapılarında yeniden organize edin.
- Retriever modülünün kurgusunda arama işlemlerini (dense-only, sparse-only, hybrid yapılarını dikkate alan argümanlarla) veri tabanını değiştirmeksizin yapılandırın (retriever config ile kullanırsınız).
- Sistem üzerine yazılmış komutlardan uygulama içindeki algoritmik yapının ayrışmasını (sharding-kopyalama) organize edin (Bunun için dış mimari ile sistem algısını birbirinden kopartmanız lazımdır).

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)
```

## Çoklu Kiralacı Veri Araması (Multi-tenant retrieval)

Yerel verilerde bir etki alanı (tenant-scoped) seçerek, işleyiş süreçlerinizi spesifik yapıdaki kiralacıların (hybrid retriever formatıyla kısıtlanmış ortamlara) hedef rotasında işlem (shard-local ile) sağlayın. Sadece ilgili kullanıcılara ayrıştırılmış birim içerisinden verilerin sınırlarını korumak hedefli metadata (özel uzantılı veritabanlarındaki yapı) filtreleriyle işlem gerçekleştirebilirsiniz.

### Hibrit Arama (hybrid mode) için faydalı bilgiler

- Modeldeki yapıyı `vector_store_query_mode=HYBRID` diyerek yoğun ve seyrek modellerle kombine (bir araya getirmesini/birleştirmesini) olmasını dizayn ediniz. Akabinde, `similarity_top_k`, `sparse_top_k` ile `hybrid_top_k` modifikasyonlarını sağlayın (Tune ile test yapın).
- Argüman yapısını kullanan modüller esnasında komutlarınızın ilgili kiracı/kullanıcının parçalama alanına (tenant's shard) iletildiğinden tam olarak emin olmalısınız. `vector_store_kwargs={"shard_identifier": tenant_id}`
- Arama modülünün kurgularındaki hedefleri (gerekir ise `tenant_id` veya `tags` gibi parametrelerle), meta alanlarından veri getirimi ve filtrelemelerini güçlendirerek ek işlemler tanımlayın.

```python
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores.types import VectorStoreQueryMode




def create_retriever_for_tenant(tenant_id: str) -> VectorIndexRetriever:
    if tenant_id not in shard_keys:
        raise ValueError(
            f"Bilinmeyen (Unknown) tenant_id: {tenant_id}. Şu değerlerden biri bekleniyordu: {shard_keys}"
        )
    return VectorIndexRetriever(
        index=index,
        vector_store_query_mode=VectorStoreQueryMode.HYBRID,
        similarity_top_k=5,
        sparse_top_k=5,
        hybrid_top_k=5,
        vector_store_kwargs={"shard_identifier": tenant_id},
    )




tenant_id = "tenant_b"
retriever = create_retriever_for_tenant(tenant_id)


query = "manage microservices traffic and observability"
results = retriever.retrieve(query)


print(f"Kiracı (Tenant): {tenant_id} | Sorgu (Query): {query}")
for i, r in enumerate(results, 1):
    meta = r.node.metadata
    print(
        f"{i}. score={r.score:.4f} | tags={meta.get('tags')} | text={r.node.get_content()}"
    )
```

```bash
Kiracı (Tenant): tenant_b | Sorgu (Query): manage microservices traffic and observability
1. score=4.6271 | tags=['cloud', 'networking'] | text=Servis kafesleri ile işlerin gözlemlenebilmesi ve çalışma trafiğinin kontrolü sağlanır
2. score=0.1213 | tags=['cloud', 'k8s'] | text=Kubernetes clusterlar üzerinde iş konteynerlerini organize ve koordine eder
3. score=0.0000 | tags=['cloud', 'devops'] | text=Helm şemaları kurgularınızdaki Kubernetes verilerini toplar ve deploy eder
```

### Sonuçları yorumlama

- Yukarıdaki çıktı, hibrit puanını, etiketleri (meta veriler) ve eşleşen metnin önizlemesini/parçasını göstermektedir.
- `tenant_id`'yi değiştirerek kiracı veya veritabanı yalıtımını doğrulayın (testi çalıştırın), zira sonuçların tek taraflı o veriye ulaşmasını kanıtlamak gereklidir.
