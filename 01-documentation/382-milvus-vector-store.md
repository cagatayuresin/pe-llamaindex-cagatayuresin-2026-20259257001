---
title: Milvus Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Milvus Vektör Deposu

Bu kılavuz, LlamaIndex ve Milvus kullanarak bir Erişim Destekli Nesil (Retrieval-Augmented Generation - RAG) sisteminin nasıl oluşturulacağını gösterir.

RAG sistemi, verilen bir isteme (prompt) dayalı olarak yeni metinler oluşturmak için bir erişim sistemini üretken (generative) bir modelle birleştirir. Sistem önce Milvus gibi bir vektör benzerlik arama motoru kullanarak bir derlemden (corpus) ilgili belgeleri getirir ve ardından getirilen belgelere dayanarak yeni metinler oluşturmak için üretken bir model kullanır.

[Milvus](https://milvus.io/), gömme benzerlik araması ve yapay zeka uygulamalarına güç sağlamak için oluşturulmuş dünyanın en gelişmiş açık kaynaklı vektör veritabanıdır.

Bu not defterinde, `MilvusVectorStore` kullanımına dair hızlı bir demo göstereceğiz.

## Başlamadan Önce

### Bağımlılıkları Kurun

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-milvus
```

```bash
%pip install llama-index
```

Bu not defteri, daha yüksek bir pymilvus sürümü gerektiren [Milvus Lite](https://milvus.io/docs/milvus_lite.md) sürümünü kullanacaktır:

```bash
%pip install "pymilvus>=2.4.2"
```

> Google Colab kullanıyorsanız, yeni kurulan bağımlılıkları etkinleştirmek için **çalışma zamanını yeniden başlatmanız** gerekebilir (ekranın üst kısmındaki "Runtime" menüsüne tıklayın ve açılır menüden "Restart session" seçeneğini seçin).

### OpenAI Kurulumu

Önce OpenAI API anahtarını ekleyerek başlayalım. Bu, ChatGPT'ye erişmemizi sağlayacaktır.

```python
import openai


openai.api_key = "sk-***********"
```

### Verileri Hazırlayın

Örnek verileri aşağıdaki komutlarla indirebilirsiniz:

```bash
! mkdir -p "data/"
! wget "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt" -O "data/paul_graham_essay.txt"
! wget "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf" -O "data/uber_2021.pdf"
```

## Başlangıç

### Verilerimizi Oluşturalım

İlk örnek olarak, `paul_graham_essay.txt` dosyasından bir belge oluşturalım. Bu, Paul Graham'ın `What I Worked On` (Neler Üzerine Çalıştım) başlıklı tek bir makalesidir. Belgeleri oluşturmak için `SimpleDirectoryReader` kullanacağız.

```python
from llama_index.core import SimpleDirectoryReader


# belgeleri yükle
documents = SimpleDirectoryReader(
    input_files=["./data/paul_graham_essay.txt"]
).load_data()


print("Belge Kimliği:", documents[0].doc_id)
```

### Veriler Üzerinde Bir İndeks Oluşturun

Artık bir belgemiz olduğuna göre, bir indeks oluşturabilir ve belgeyi ekleyebiliriz. İndeks için bir `MilvusVectorStore` kullanacağız. `MilvusVectorStore` birkaç argüman alır:

**temel argümanlar**

- `uri (str, isteğe bağlı)`: Bağlanılacak URI; Milvus veya Zilliz Cloud hizmeti için "https://adres:port" şeklinde veya lite yerel Milvus için "yol/yerel/milvus.db" şeklindedir. Varsayılan olarak "./milvus_llamaindex.db"dir.
- `token (str, isteğe bağlı)`: Giriş için belirteç (token). RBAC kullanılmıyorsa boştur, kullanılıyorsa muhtemelen "kullaniciadi:sifre" olacaktır.
- `collection_name (str, isteğe bağlı)`: Verilerin saklanacağı koleksiyonun adı. Varsayılan olarak "llamalection"dır.
- `overwrite (bool, isteğe bağlı)`: Aynı ada sahip mevcut koleksiyonun üzerine yazılıp yazılmayacağı. Varsayılan olarak False'dur.

**belge kimliği ve metin dahil skaler alanlar**

- `doc_id_field (str, isteğe bağlı)`: Koleksiyon için `doc_id` alanının adı. Varsayılan olarak DEFAULT_DOC_ID_KEY.
- `text_key (str, isteğe bağlı)`: Sağlanan koleksiyonda metnin hangi anahtarda saklandığı. Kendi koleksiyonunuzu getirirken kullanılır. Varsayılan olarak DEFAULT_TEXT_KEY.
- `scalar_field_names (list, isteğe bağlı)`: Koleksiyon şemasına dahil edilecek ekstra skaler alanların adları.
- `scalar_field_types (list, isteğe bağlı)`: Ekstra skaler alanların tipleri.

**yoğun (dense) alan**

- `enable_dense (bool)`: Yoğun gömmeyi etkinleştirmek veya devre dışı bırakmak için bir bayrak. Varsayılan olarak True'dur.
- `dim (int, isteğe bağlı)`: Koleksiyon için gömme vektörlerinin boyutu. `enable_sparse` False iken yeni bir koleksiyon oluşturulurken gereklidir.
- `embedding_field (str, isteğe bağlı)`: Koleksiyon için yoğun gömme alanının adı, varsayılan olarak DEFAULT_EMBEDDING_KEY.
- `index_config (dict, isteğe bağlı)`: Yoğun gömme indeksini oluşturmak için kullanılan yapılandırma. Varsayılan olarak None'dır.
- `search_config (dict, isteğe bağlı)`: Milvus yoğun indeksinde arama yapmak için kullanılan yapılandırma. Bunun `index_config` tarafından belirtilen indeks tipiyle uyumlu olması gerektiğini unutmayın. Varsayılan olarak None'dır.
- `similarity_metric (str, isteğe bağlı)`: Yoğun gömme için kullanılacak benzerlik metriği; şu anda IP, COSINE ve L2 desteklenmektedir.

**seyrek (sparse) alan**

- `enable_sparse (bool)`: Seyrek gömmeyi etkinleştirmek veya devre dışı bırakmak için bir bayrak. Varsayılan olarak False'dur.
- `sparse_embedding_field (str)`: Seyrek gömme alanının adı, varsayılan olarak DEFAULT_SPARSE_EMBEDDING_KEY.
- `sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], isteğe bağlı)`: Eğer `enable_sparse` True ise, metni seyrek gömmeye dönüştürmek için bu nesne sağlanmalıdır. None ise, varsayılan seyrek gömme işlevi (BM25BuiltInFunction) kullanılır.
- `sparse_index_config (dict, isteğe bağlı)`: Seyrek gömme indeksini oluşturmak için kullanılan yapılandırma. Varsayılan olarak None'dır.

**hibrit sıralayıcı (hybrid ranker)**

- `hybrid_ranker (str)`: Hibrit arama sorgularında kullanılan sıralayıcı tipini belirtir. Şu anda yalnızca ["RRFRanker", "WeightedRanker"] desteklenmektedir. Varsayılan olarak "RRFRanker"dır.

- `hybrid_ranker_params (dict, isteğe bağlı)`: Hibrit sıralayıcı için yapılandırma parametreleri. Bu sözlüğün yapısı, kullanılan belirli sıralayıcıya bağlıdır:

  - "RRFRanker" için şunları içermelidir:
    - "k" (int): Resiprokal Sıralama Füzyonu'nda (RRF) kullanılan bir parametre. Bu değer, arama alaka düzeyini artırmak için birden fazla sıralama stratejisini tek bir puanda birleştiren RRF algoritmasının bir parçası olarak sıralama puanlarını hesaplamak için kullanılır.

  - "WeightedRanker" için şunları bekler:

    - "weights" (kayan noktalı sayı listesi): Tam olarak iki ağırlıktan oluşan bir liste:

      1. Yoğun gömme bileşeni için ağırlık.
      2. Seyrek gömme bileşeni için ağırlık. Bu ağırlıklar, hibrit erişim sürecinde gömmelerin yoğun ve seyrek bileşenlerinin önemini ayarlamak için kullanılır. Varsayılan olarak boş bir sözlüktür, bu da sıralayıcının önceden tanımlanmış varsayılan ayarlarıyla çalışacağı anlamına gelir.

**diğerleri**

- `collection_properties (dict, isteğe bağlı)`: Yaşam Süresi (TTL) ve MMAP (bellek eşleme) gibi koleksiyon özellikleri. Varsayılan olarak None'dır. Şunları içerebilir:

  - "collection.ttl.seconds" (int): Bu özellik ayarlandığında, mevcut koleksiyondaki verilerin süresi belirtilen sürede dolar. Koleksiyondaki süresi dolmuş veriler temizlenir ve aramalara veya sorgulara dahil edilmez.
  - "mmap.enabled" (bool): Koleksiyon seviyesinde bellek eşlemeli depolamanın etkinleştirilip etkinleştirilmeyeceği.

- `index_management (IndexManagement)`: Kullanılacak indeks yönetimi stratejisini belirtir. Varsayılan olarak "create_if_not_exists"tir.

- `batch_size (int)`: Milvus'a veri eklerken bir toplu işlemde (batch) işlenen belge sayısını yapılandırır. Varsayılan olarak DEFAULT_BATCH_SIZE'dır.

- `consistency_level (str, isteğe bağlı)`: Yeni oluşturulan bir koleksiyon için hangi tutarlılık seviyesinin (consistency level) kullanılacağı. Varsayılan olarak "Session"dır.

```python
# Belgeler üzerinde bir indeks oluşturun
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore


vector_store = MilvusVectorStore(
    uri="./milvus_demo.db", dim=1536, overwrite=True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

> `MilvusVectorStore` parametreleri için:
>
> - `uri`yi `./milvus.db` gibi yerel bir dosya olarak ayarlamak, tüm verileri otomatik olarak bu dosyada saklamak için [Milvus Lite](https://milvus.io/docs/milvus_lite.md) sürümünü kullandığından en uygun yöntemdir.
> - Büyük ölçekli verileriniz varsa, [docker veya kubernetes](https://milvus.io/docs/quickstart.md) üzerinde daha performanslı bir Milvus sunucusu kurabilirsiniz. Bu kurulumda, lütfen sunucu uri'sini (örneğin `http://localhost:19530`) `uri` olarak kullanın.
> - Milvus için tamamen yönetilen bulut hizmeti olan [Zilliz Cloud](https://zilliz.com/cloud)'u kullanmak istiyorsanız, Zilliz Cloud'daki [Public Endpoint ve Api key](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details) bilgilerine karşılık gelen `uri` ve `token` bilgilerini ayarlayın.

### Verileri Sorgulayın

Artık belgemiz indekste saklandığına göre, indekse sorular sorabiliriz. İndeks, ChatGPT için bilgi tabanı olarak kendi içinde saklanan verileri kullanacaktır.

```python
query_engine = index.as_query_engine()
res = query_engine.query("Yazar ne öğrendi?")
print(res)
```

**"Yazar, üniversitedeki felsefe derslerinin kendisi için sıkıcı olduğunu ve bu durumun odak noktasını yapay zeka (YZ) çalışmalarına kaydırmasına neden olduğunu öğrendi."**

```python
res = query_engine.query(
    "Hastalık yazar için ne gibi zorluklar yarattı?"
)
print(res)
```

**"Hastalık, yazarın annesinin sağlığını etkilediği için zorluklar yarattı ve kolon kanserinin neden olduğu bir felce yol açtı. Bu durum annesinin dengesini kaybetmesine ve bir huzurevine yerleştirilmesine neden oldu. Yazar ve kız kardeşi, annelerinin huzurevinden çıkıp evine dönmesine yardım etmeye kararlıydılar."**

Bu sonraki test, üzerine yazmanın (overwriting) önceki verileri sildiğini gösterir.

```python
from llama_index.core import Document


vector_store = MilvusVectorStore(
    uri="./milvus_demo.db", dim=1536, overwrite=True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    [Document(text="Aranan sayı ondur.")],
    storage_context,
)
query_engine = index.as_query_engine()
res = query_engine.query("Yazar kimdir?")
print(res)
```

**"Yazar, bağlam bilgisini oluşturan kişidir."**

Bir sonraki test, halihazırda var olan bir indekse ek veri eklemeyi gösterir.

```python
del index, vector_store, storage_context, query_engine


vector_store = MilvusVectorStore(uri="./milvus_demo.db", overwrite=False)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
query_engine = index.as_query_engine()
res = query_engine.query("Sayı kaçtır?")
print(res)
```

**"Sayı ondur."**

```python
res = query_engine.query("Yazar kimdir?")
print(res)
```

**"Paul Graham"**

## Meta veri filtreleme

Belirli kaynakları filtreleyerek sonuçlar üretebiliriz. Aşağıdaki örnek, dizinden tüm belgelerin yüklendiğini ve ardından meta verilere göre filtrelendiğini göstermektedir.

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


# Daha önce yüklenen her iki belgeyi de yükleyin
documents_all = SimpleDirectoryReader("./data/").load_data()


vector_store = MilvusVectorStore(
    uri="./milvus_demo.db", dim=1536, overwrite=True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents_all, storage_context)
```

Sadece `uber_2021.pdf` dosyasındaki belgeleri getirmek istiyoruz.

```python
filters = MetadataFilters(
    filters=[ExactMatchFilter(key="file_name", value="uber_2021.pdf")]
)
query_engine = index.as_query_engine(filters=filters)
res = query_engine.query(
    "Hastalık yazar için ne gibi zorluklar yarattı?"
)


print(res)
```

**"Hastalık; küresel olarak Mobility tekliflerine olan talebin azalması dahil olmak üzere iş ve operasyonlar üzerindeki olumsuz etkilerle ilgili zorluklar yarattı ve seyahat davranışını ve talebini etkiledi. Ek olarak pandeminin, COVID-19 ile ilgili endişelerden etkilenen sürücü arz kısıtlamalarına yol açması seyahatleri daha da etkiledi ve hem sürücü arzını hem de Mobility tekliflerine yönelik tüketici talebi üzerinde olumsuz etkiler yaratabilecek tavsiyelere ve kısıtlamalara neden oldu."**

Bu kez `paul_graham_essay.txt` dosyasından veri getirdiğimizde farklı bir sonuç alıyoruz.

```python
filters = MetadataFilters(
    filters=[ExactMatchFilter(key="file_name", value="paul_graham_essay.txt")]
)
query_engine = index.as_query_engine(filters=filters)
res = query_engine.query(
    "Hastalık yazar için ne gibi zorluklar yarattı?"
)


print(res)
```

**"Hastalık, yazarın annesinin sağlığını etkilediği için zorluklar yarattı ve kolon kanserinin neden olduğu bir felce yol açtı. Bu durum annesinin dengesini kaybetmesine ve bir huzurevine yerleştirilmesine neden oldu. Yazar ve kız kardeşi, annelerinin huzurevinden çıkıp evine dönmesine yardım etmeye kararlıydılar."**
