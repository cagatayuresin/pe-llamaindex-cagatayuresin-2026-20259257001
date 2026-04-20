---
title: Redis Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Redis Vektör Deposu (Vector Store)

Bu not defterinde RedisVectorStore'un kullanımına dair hızlı bir demo göstereceğiz.

Bu Not Defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install -U llama-index llama-index-vector-stores-redis llama-index-embeddings-cohere llama-index-embeddings-openai
```

```python
import os
import getpass
import sys
import logging
import textwrap
import warnings


warnings.filterwarnings("ignore")


# Hata ayıklama (debug) günlüklerini görmek için açıklama satırını kaldırın
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.redis import RedisVectorStore
```

### Redis'i Başlatın

Redis'i başlatmanın en kolay yolu [Redis Stack](https://hub.docker.com/r/redis/redis-stack) docker imajını kullanmak veya [ÜCRETSİZ Redis Cloud](https://redis.com/try-free) örneği (instance) için hızlıca kayıt olmaktır.

Bu eğitimin her adımını takip etmek için imajı aşağıdaki gibi başlatın:

Terminal penceresi

```bash
docker run --name redis-vecdb -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

Bu ayrıca 8001 bağlantı noktasında (port) RedisInsight kullanıcı arayüzünü (UI) başlatacaktır ve bunu <http://localhost:8001> adresinden görüntüleyebilirsiniz.

### OpenAI'yi Kurun

Öncelikle openai API anahtarını ekleyerek başlayalım. Bu, gömmeler (embeddings) için openai'ye erişmemizi ve chatgpt'yi kullanmamızı sağlayacaktır.

```python
oai_api_key = getpass.getpass("OpenAI API Anahtarı:")
os.environ["OPENAI_API_KEY"] = oai_api_key
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```bash
--2024-04-10 19:35:33--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
raw.githubusercontent.com (raw.githubusercontent.com) Çözümleniyor... 2606:50c0:8003::154, 2606:50c0:8000::154, 2606:50c0:8002::154, ...
raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8003::154|:443 adresine bağlanılıyor... bağlanıldı.
HTTP isteği gönderildi, yanıt bekleniyor... 200 OK
Uzunluk: 75042 (73K) [text/plain]
Kaydediliyor: ‘data/paul_graham/paul_graham_essay.txt’


data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    0.03sn içinde


2024-04-10 19:35:33 (2.15 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ kaydedildi [75042/75042]
```

### Bir veri seti okuyun

Burada, `RedisVectorStore` içinde depolamak üzere gömmelere (embeddings) dönüştürülecek metni sağlamak ve LLM Soru-Cevap (QnA) döngümüz (loop) için bağlam (context) bulmak üzere bir dizi Paul Graham makalesi kullanacağız.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print(
    "Belge (Document) Kimliği:",
    documents[0].id_,
    "Belge Dosya Adı (Filename):",
    documents[0].metadata["file_name"],
)
```

```bash
Belge (Document) Kimliği: 7056f7ba-3513-4ef4-9792-2bd28040aaed Belge Dosya Adı (Filename): paul_graham_essay.txt
```

### Varsayılan (default) Redis Vektör Deposunu başlatın

Artık belgelerimiz hazır olduğuna göre, Redis Vektör Deposunu **varsayılan** ayarlarla başlatabiliriz. Bu, vektörlerimizi Redis'te saklamamıza ve gerçek zamanlı arama için bir indeks oluşturmamıza olanak tanıyacaktır.

```python
from llama_index.core import StorageContext
from redis import Redis


# bir Redis istemci (client) bağlantısı oluştur
redis_client = Redis.from_url("redis://localhost:6379")


# vektör deposu sarmalayıcısını (wrapper) oluştur
vector_store = RedisVectorStore(redis_client=redis_client, overwrite=True)


# depolama bağlamını (storage context) yükle
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# belgelerden ve depolama bağlamından indeks oluştur ve yükle
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
# index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
```

```bash
19:39:17 llama_index.vector_stores.redis.base INFO   Varsayılan (default) RedisVectorStore şeması (schema) kullanılıyor.
19:39:19 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
19:39:19 llama_index.vector_stores.redis.base INFO   Llama_index indeksine 22 belge eklendi.
```

### Varsayılan vektör deposunu sorgulayın

Verilerimizi indekste depoladığımıza göre, indekse yönelik sorular sorabiliriz.

İndeks, verileri bir Yüksek Lisans Programı (LLM) için bilgi tabanı (knowledge base) olarak kullanacaktır. as\_query\_engine() varsayılan ayarı, OpenAI gömmelerini (embeddings) ve dil modeli olarak GPT'yi kullanır. Bu nedenle, özelleştirilmiş veya yerel bir dil modeli seçmediğiniz sürece bir OpenAI anahtarı gereklidir.

Aşağıda indeksimize yönelik aramaları (searches) ve ardından bir LLM ile tam RAG'yi test edeceğiz.

```python
query_engine = index.as_query_engine()
retriever = index.as_retriever()
```

```python
result_nodes = retriever.retrieve("Yazar (author) ne öğrendi?")
for node in result_nodes:
    print(node)
```

```bash
19:39:22 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
19:39:22 llama_index.vector_stores.redis.base INFO   llama_index indeksi * filtreleriyle sorgulanıyor
19:39:22 llama_index.vector_stores.redis.base INFO   Şu kimliğe (id) sahip sorgu için 2 sonuç bulundu: ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108']
Düğüm (Node) Kimliği: adb6b7ce-49bb-4961-8506-37082c02a389
Metin (Text): Ne Üzerinde Çalıştım (What I Worked On) Şubat 2021 Üniversiteden önce 
okul dışında üzerinde çalıştığım iki ana şey yazma ve programlamaydı. 
Makaleler (essays) yazmadım. O zamanlar yeni başlayan yazarların yazması gerekenleri yazdım, 
ki muhtemelen hala öyledir: kısa hikayeler (short stories). Hikayelerim
korkunçtu. Neredeyse hiç olay örgüleri yoktu, sadece benim ...
Score:  0.820


Düğüm (Node) Kimliği: e39be1fe-32d0-456e-b211-4efabd191108
Metin (Text): New York'taki doğru partilere giden, resmi olarak atanmış birkaç düşünür dışında, 
makale yayınlamasına izin verilen tek kişiler 
kendi uzmanlıkları hakkında yazan uzmanlardı. Daha önce yayınlanmaları için
hiçbir yol olmadığı için yazılmamış pek çok
makale vardı. Artık olabilirlerdi ve ben onları yazacaktım. [12]
Çalıştım...
Score:  0.819
```

```python
response = query_engine.query("Yazar (author) ne öğrendi?")
print(textwrap.fill(str(response), 100))
```

```bash
19:39:25 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
19:39:25 llama_index.vector_stores.redis.base INFO   llama_index indeksi * filtreleriyle sorgulanıyor
19:39:25 llama_index.vector_stores.redis.base INFO   Şu kimliğe (id) sahip sorgu için 2 sonuç bulundu: ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108']
19:39:27 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Yazar, prestijli olmayan şeyler üzerinde çalışmanın çoğu zaman değerli keşiflere yol açtığını
ve doğru türde motivasyonlara işaret ettiğini öğrendi. İlk prestij eksikliğine rağmen, bu tür çalışmaları
sürdürmek, sadece başkalarını etkileme arzusuyla hareket etmenin ortak
tuzaklarından uzak durarak, gerçek potansiyelin ve uygun motivasyonların bir işareti olabilir.
```

```python
result_nodes = retriever.retrieve("Yazar için zor olan an neydi?")
for node in result_nodes:
    print(node)
```

```bash
19:39:27 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
19:39:27 llama_index.vector_stores.redis.base INFO   llama_index indeksi * filtreleriyle sorgulanıyor
19:39:27 llama_index.vector_stores.redis.base INFO   Şu kimliğe (id) sahip sorgu için 2 sonuç bulundu: ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108']
Düğüm (Node) Kimliği: adb6b7ce-49bb-4961-8506-37082c02a389
Metin (Text): Ne Üzerinde Çalıştım (What I Worked On) Şubat 2021 Üniversiteden önce 
okul dışında üzerinde çalıştığım iki ana şey yazma ve programlamaydı. 
Makaleler (essays) yazmadım. O zamanlar yeni başlayan yazarların yazması gerekenleri yazdım, 
ki muhtemelen hala öyledir: kısa hikayeler (short stories). Hikayelerim
korkunçtu. Neredeyse hiç olay örgüleri yoktu, sadece benim ...
Score:  0.802


Düğüm (Node) Kimliği: e39be1fe-32d0-456e-b211-4efabd191108
Metin (Text): New York'taki doğru partilere giden, resmi olarak atanmış birkaç düşünür dışında, 
makale yayınlamasına izin verilen tek kişiler 
kendi uzmanlıkları hakkında yazan uzmanlardı. Daha önce yayınlanmaları için
hiçbir yol olmadığı için yazılmamış pek çok
makale vardı. Artık olabilirlerdi ve ben onları yazacaktım. [12]
Çalıştım...
Score:  0.799
```

```python
response = query_engine.query("Yazar için zor olan an neydi?")
print(textwrap.fill(str(response), 100))
```

```bash
19:39:29 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
19:39:29 llama_index.vector_stores.redis.base INFO   llama_index indeksi * filtreleriyle sorgulanıyor
19:39:29 llama_index.vector_stores.redis.base INFO   Şu kimliğe (id) sahip sorgu için 2 sonuç bulundu: ['llama_index/vector_adb6b7ce-49bb-4961-8506-37082c02a389', 'llama_index/vector_e39be1fe-32d0-456e-b211-4efabd191108']
19:39:31 httpx INFO   HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Yazar için zor an, IBM 1401 ana bilgisayarındaki (mainframe) programlarından birinin 
sonlanmaması (terminate etmemesi) sonucunda teknik bir hataya yol açması 
ve veri merkezi (data center) yöneticisi ile rahatsız edici bir durumun yaşanmasıydı.
```

```python
index.vector_store.delete_index()
```

```bash
19:39:34 llama_index.vector_stores.redis.base INFO   llama_index indeksi siliniyor
```

### Özel (custom) bir indeks şeması kullanma

Çoğu kullanım durumunda (use cases), temel indeks yapılandırmasını ve spesifikasyonunu özelleştirme yeteneğine ihtiyaç duyarsınız. Örneğin, etkinleştirmek (enable) istediğiniz belirli meta veri filtrelerini tanımlamak için bu kullanışlıdır.

Redis söz konusu olduğunda, bu işlem tıpkı dosya (file) veya sözlükten (dict) indeks şeması nesnesinin yaratılması ve ardından bu nesnenin vektör saklayıcı (vector store) istemcisinin iç sarmalayıcısına (client wrapper) iletilmesi kadar basittir.

Bu örnekte, şunları yapacağız:

1. gömme modelini (embedding model) [Cohere](cohereai.com)'a geçireceğiz
2. belgenin zaman damgası, `updated_at` (güncelleme\_zamanı) için ekstra bir özellik barındıran meta veri alanı ekleyeceğiz
3. halihazırda var olan `file_name` (dosya\_adı) meta veri alanını indeksleyeceğiz

```python
from llama_index.core.settings import Settings
from llama_index.embeddings.cohere import CohereEmbedding


# Cohere Anahtarını (Key) ayarla
co_api_key = getpass.getpass("Cohere API Anahtarı:")
os.environ["CO_API_KEY"] = co_api_key


# llamaindex'i Cohere gömmelerini kullanacak şekilde ayarla
Settings.embed_model = CohereEmbedding()
```

```python
from redisvl.schema import IndexSchema




custom_schema = IndexSchema.from_dict(
    {
        # temel indeks özelliklerini (specs) özelleştir
        "index": {
            "name": "paul_graham",
            "prefix": "essay",
            "key_separator": ":",
        },
        # indekslenen alanları özelleştir
        "fields": [
            # llamaindex için gerekli alanlar
            {"type": "tag", "name": "id"},
            {"type": "tag", "name": "doc_id"},
            {"type": "text", "name": "text"},
            # özel (custom) meta veri alanları
            {"type": "numeric", "name": "updated_at"},
            {"type": "tag", "name": "file_name"},
            # cohere gömmeleri (embeddings) için özel vektör alanı tanımı
            {
                "type": "vector",
                "name": "vector",
                "attrs": {
                    "dims": 1024,
                    "algorithm": "hnsw",
                    "distance_metric": "cosine",
                },
            },
        ],
    }
)
```

```python
custom_schema.index
```

```bash
IndexInfo(name='paul_graham', prefix='essay', key_separator=':', storage_type=<StorageType.HASH: 'hash'>)
```

```python
custom_schema.fields
```

```bash
{'id': TagField(name='id', type='tag', path=None, attrs=TagFieldAttributes(sortable=False, separator=',', case_sensitive=False, withsuffixtrie=False)),
 'doc_id': TagField(name='doc_id', type='tag', path=None, attrs=TagFieldAttributes(sortable=False, separator=',', case_sensitive=False, withsuffixtrie=False)),
 'text': TextField(name='text', type='text', path=None, attrs=TextFieldAttributes(sortable=False, weight=1, no_stem=False, withsuffixtrie=False, phonetic_matcher=None)),
 'updated_at': NumericField(name='updated_at', type='numeric', path=None, attrs=NumericFieldAttributes(sortable=False)),
 'file_name': TagField(name='file_name', type='tag', path=None, attrs=TagFieldAttributes(sortable=False, separator=',', case_sensitive=False, withsuffixtrie=False)),
 'vector': HNSWVectorField(name='vector', type='vector', path=None, attrs=HNSWVectorFieldAttributes(dims=1024, algorithm=<VectorIndexAlgorithm.HNSW: 'HNSW'>, datatype=<VectorDataType.FLOAT32: 'FLOAT32'>, distance_metric=<VectorDistanceMetric.COSINE: 'COSINE'>, initial_cap=None, m=16, ef_construction=200, ef_runtime=10, epsilon=0.01))}
```

Redis ile [şema ve indeks tasarımı (schema and index design)](https://redisvl.com) hakkında daha fazla bilgi edinin.

```python
from datetime import datetime




def date_to_timestamp(date_string: str) -> int:
    date_format: str = "%Y-%m-%d"
    return int(datetime.strptime(date_string, date_format).timestamp())




# belgeler arasında gezin ve yeni alan ekle
for document in documents:
    document.metadata["updated_at"] = date_to_timestamp(
        document.metadata["last_modified_date"]
    )
```

```python
vector_store = RedisVectorStore(
    schema=custom_schema,  # özelleştirilmiş şema (customized schema) sağlayın
    redis_client=redis_client,
    overwrite=True,
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)


# belgelerden ve depolama bağlamından indeks oluştur ve yükle
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```bash
19:40:05 httpx INFO   HTTP İsteği (Request): POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK"
19:40:06 httpx INFO   HTTP İsteği (Request): POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK"
19:40:06 httpx INFO   HTTP İsteği (Request): POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK"
19:40:06 llama_index.vector_stores.redis.base INFO   paul_graham indeksine 22 belge eklendi
```

### Vektör deposunu sorgulama ve meta veri üzerinde filtreleme

Artık Redis'te ek meta verilerin indekslendiğine göre, bazı filtreli sorgular deneyelim.

```python
from llama_index.core.vector_stores import (
    MetadataFilters,
    MetadataFilter,
    ExactMatchFilter,
)


retriever = index.as_retriever(
    similarity_top_k=3,
    filters=MetadataFilters(
        filters=[
            ExactMatchFilter(key="file_name", value="paul_graham_essay.txt"),
            MetadataFilter(
                key="updated_at",
                value=date_to_timestamp("2023-01-01"),
                operator=">=",
            ),
            MetadataFilter(
                key="text",
                value="learn",
                operator="text_match",
            ),
        ],
        condition="and",
    ),
)
```

```python
result_nodes = retriever.retrieve("Yazar (author) ne öğrendi?")


for node in result_nodes:
    print(node)
```

```bash
19:40:22 httpx INFO   HTTP İsteği (Request): POST https://api.cohere.ai/v1/embed "HTTP/1.1 200 OK"




19:40:22 llama_index.vector_stores.redis.base INFO   paul_graham indeksi şu filtrelerle sorgulanıyor: ((@file_name:{paul_graham_essay\.txt} @updated_at:[1672549200 +inf]) @text:(learn))
19:40:22 llama_index.vector_stores.redis.base INFO   Şu kimliğe (id) sahip sorgu için 3 sonuç bulundu: ['essay:0df3b734-ecdb-438e-8c90-f21a8c80f552', 'essay:01108c0d-140b-4dcc-b581-c38b7df9251e', 'essay:ced36463-ac36-46b0-b2d7-935c1b38b781']
Düğüm (Node) Kimliği: 0df3b734-ecdb-438e-8c90-f21a8c80f552
Metin (Text): Felsefe adına görünürde tek işe yarar alan olarak geriye kalan şey, farklı 
disiplinler üzerindeki kişilerin kendi alanlarında ihmale gelmeyebileceğini düşündükleri istisnai olan durumlardı (edge cases).  18 yaşındayken ben bunu
kelimelere dökemezdim. O zamanlar tek bildiğim, felsefe 
dersleri almaya devam ettiğim ve bunların sürekli sıkıcı olduğuydu. Bu yüzden Yapay Zeka'ya (AI) geçmeye
karar verdim.  1980'lerin ortalarında yapay zeka havada uçuşuyordu ama iki
şey...
Score:  0.410


Düğüm (Node) Kimliği: 01108c0d-140b-4dcc-b581-c38b7df9251e
Metin (Text): Aslında bu, SHRDLU'ya daha fazla kelime 
öğretmekten ibaret değildi. Kavramları temsil eden açık veri yapılarıyla 
Yapay Zeka yapmanın o bütünsel yolu işe yaramayacaktı. Onun bozukluğu (brokenness), 
çoğu zaman olduğu gibi, ona uygulanabilecek çeşitli geçici önlemler (band-aids) hakkında makaleler 
yazmak için bir sürü fırsat yarattı ama bu bizi hiçbir zaman ...
Score:  0.390


Düğüm (Node) Kimliği: ced36463-ac36-46b0-b2d7-935c1b38b781
Metin (Text): Yüksek lisans (Grad) öğrencileri herhangi bir bölümden dersler alabiliyordu ve
danışmanım Tom Cheatham çok uyumluydu. Aldığım bu garip derslerden
haberdar olsaydı bile asla bir şey söylemezdi.  Şimdi ben;
hayatıma sanatçı olarak devam edebilmenin kurgusu paralelinde bilgisayar bilimlerinde Doktora (PhD) yapıyor,
bunlara ilaveten Lisp hack ve de "On Lisp" üzerindeki işime gerçekten ve
tüm samimiyetimle arzu bağlıyordum. Diğe...
Score:  0.389
```

### Redis'teki mevcut bir indeksten geri yükleme

Bir indeksten geri yükleme işlemi; bir Redis bağlantı istemcisine (veya URL), `overwrite=False` atamasına ve daha önce kullanılan aynı şema (schema) nesnesinin aktarılmasına (passing in) ihtiyaç duyar. (Kolaylık sağlamak için bu `.to_yaml()` kullanılarak bir YAML dosyasına aktarılabilir (offloaded))

```python
custom_schema.to_yaml("paul_graham.yaml")
```

```python
vector_store = RedisVectorStore(
    schema=IndexSchema.from_yaml("paul_graham.yaml"),
    redis_client=redis_client,
)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
```

```bash
19:40:28 redisvl.index.index INFO   İndeks zaten (already) var, üzerine yazılmıyor (not overwriting).
```

**Yakın gelecekte** — sadece bir indeks adını (index name) kullanarak yüklemeye imkân tanıyacak kullanışlı bir yöntem (convenience method) uygulayacağız:

```python
RedisVectorStore.from_existing_index(index_name="paul_graham", redis_client=redis_client)
```

### Belgeleri veya indeksi tamamen silme

Bazen belgeleri veya tüm indeksi büsbütün silmek yararlı olabilir. Bu eylem ise `delete` (sil) ve `delete_index` method formülleri yardımıyla tatbik edilebilir.

```python
document_id = documents[0].doc_id
document_id
```

```python
'7056f7ba-3513-4ef4-9792-2bd28040aaed'
```

```python
print("Silmeden önceki belge sayısı (Number of documents before deleting)", redis_client.dbsize())
vector_store.delete(document_id)
print("Sildikten sonraki belge sayısı (Number of documents after deleting)", redis_client.dbsize())
```

```bash
Silmeden önceki belge sayısı (Number of documents before deleting) 22
19:40:32 llama_index.vector_stores.redis.base INFO   paul_graham indeksinden 22 belge silindi
Sildikten sonraki belge sayısı (Number of documents after deleting) 0
```

Bununla birlikte, sürekli ekleme/güncelleme (continuous upsert) için Redis indeksi (kendisiyle ilişkili hiçbir belge olmasa da) var olmaya devam eder.

```python
vector_store.index_exists()
```

```bash
True
```

```python
# şimdi indeksi tamamen silelim
# bu, tüm belgeleri ve indeksi silecektir
vector_store.delete_index()
```

```bash
19:40:37 llama_index.vector_stores.redis.base INFO   paul_graham indeksi siliniyor
```

```python
print("Sildikten sonraki belge sayısı (Number of documents after deleting)", redis_client.dbsize())
```

```bash
Sildikten sonraki belge sayısı (Number of documents after deleting) 0
```

### Sorun Giderme (Troubleshooting)

Boş bir sorgu sonucu alırsanız, kontrol edilmesi gereken birkaç sorun vardır:

#### Şema (Schema)

Diğer vektör depoları örneklerinden farklı olarak Redis, kullanıcılardan ilgili olan (kullandıkları) indeks şemasının tanımını bariz/kesin sınırlar içinde bir netlik yaratarak yapmasını arzu/talep eder. Bunun birkaç nedeni vardır:

1. Redis sadece eş zamanlı (real-time) vektörel arama için değil; ayrıca dosya/evrak (document) aramaları-depolanmaları, önbelleğe (cache) alma, anlık olan uyarı (mesajlaşma), pub/sub sistem yapıları ve de en nihayetinde oturum tabanlı sistemlerde vs. muhtelif işlemler ile yaygın bir kullanıma sahiptir. Arama amacıyla kayıtlara ait her bileşen veya özellik kodunun ayrıntısıyla taranmasına ihtiyaç yoktur. İşin tabiatı; bu tarz konularda sadece kısmen etkinliğe yaslanırken, büyük ölçüde de kullanıcı cephesindeki pürüzleri bertaraf (minimize) etmeye odaklanır.
2. Redis ile LLamaIndex platformlarında kullanıma sokulan formların ve indeks türlerinin bütünü `id`, `doc_id`, `text`, ve bunlara ek olacak biçimde de asgari vasıfta minimum ebatlı bir `vector` dosyası/nesnesi içerir.

`RedisVectorStore` eklentinizi yukarıda bahsettiğimiz özel/şahsi yapı (custom schema) ile kombine şekilde (açık biçimde tanımlanmış olmasını da dikkate alarak) veya basit bir yaklaşımla olağan ayarıyla (OpenAI gömmeleri olan (assumes) varsayılan (default) tabanlı şema/modül konfigürasyonu) sisteme işleyin.

#### Önek (Prefix) sorunları

Redis, tüm kayıtlar ile verileri ilgili sistemde çeşitli uygulama/yazılım ve müşteri formatlarına uygun şekilde kilit tabanlı kullanım "partitions" ebatlarına ("bölümlere") parçalamak (segment) üzere öneklerin/değerlerin olmasını beklemekte.

İndeks şemasının bir uzvu (ve de bir parçası) sayılan seçili modelin/yapının `prefix` bazlı uyumluluklarında her şartta ve kurguda bir tutarlılık olduğunu birimsel ölçeklerdeki indeks parametrelerine (a specific index) sâdık kalarak takip edin.

İndeksinizin hangi öneklerle yaratıldığını görmek maksadıyla; yazılım dillerinizde ve derlemelerinizde Redis İstemcisinden (Redis CLI) şu komutları test edebilir, böylelikle `FT.INFO <indeksinizin_adı (name of your index)>` yazarak `index_definition` => `prefixes` sekmesinin altında yer tutan yapıya bakabilirsiniz.

#### Veri ile İndeks Ayrımı (Data vs Index)

Redis, dizindeki kayıtları (records) ve indeks modülünü iki farklı (ilkesel olarak apayrı) hususiyet şeklinde (different entities) kabul ve telakki eder. Böylece sizin ek güncellemelerdeki veya yeni işlenen girdiler ile eklenen tabanlı tasarımların göç ettirilmesi (migrations/upserts) konularında size bariz bir serbestlik-rahatlık kazandırır (more flexibility).

Eğer mevcut ve kullanılabilir/hazır bir indeks yapınız (an existing index) varsa; hem bundan sonlanma garantisi almanız hem de yapıyı tamamlayarak imha suretiyle devreden tecrit edilmesi beklentilerinizi somutlaştırmak nâmına; dilediğiniz gibi Redis İstemcisindeki ilgili bölüme (Redis CLI) `FT.DROPINDEX <indeksinizin_adı>` ekleyerek/yazarak isteğinizi yerine getirebilirsiniz. Unutmayın ve aklınızda kalsın ki; sistemsel komutlar ve yönlendirmeler bünyesinde söz konusu olarak tasvir edilen yapılar; siz kendiniz bir eklenti argümanı olarak `DD` girmezseniz ve ibaresini geçirmezseniz aslî (actual data) ana/esas unsurlarınızı silmez.

#### Meta verileri kullanırken alınan boş sorgular (Empty queries)

Eğer meta verileri var edilmiş olan mevcut bir dizine (index) *sonradan (after)* iliştirir ve ardından ilave ettiğiniz o meta alanı için taramalarla sorgu yürütürseniz neticeleriniz cevapsız/boş dönecektir.

Redis dizin sahalarını; tıpkı evvelce tanımlanmış ibareler olarak izahı yapılmış ('özellikler-prefixes' durumundaki anlatımların paralelliğinde olduğu minvalde) yalnız ve yalnız o dizinin var ediliş evresinde indeksler (indexes fields upon index creation only).
