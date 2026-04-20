---
title: Nile Vektör Deposu (Çok Kiracılı PostgreSQL)
 | LlamaIndex OSS Belgeleri
---

# Nile Vektör Deposu (Çok Kiracılı PostgreSQL)

Bu not defteri, çok kiracılı (multi-tenant) RAG uygulamaları için vektör gömmelerini saklamak ve sorgulamak üzere PostgreSQL tabanlı vektör deposu olan `NileVectorStore`un nasıl kullanılacağını gösterir.

## Nile Nedir?

Nile; otomatik ölçeklendirme, dallanma (branching) ve yedeklemeler dahil olmak üzere kiracı başına tüm veritabanı işlemlerini tam müşteri izolasyonu ile sağlayan bir Postgres veritabanıdır.

Çok kiracılı RAG uygulamaları, büyük dil modellerini kullanırken güvenlik ve gizlilik sağladıkları için giderek daha popüler hale gelmektedir.

Ancak, alttaki Postgres veritabanını yönetmek basit değildir. Kiracı başına DB (DB-per-tenant) yönetimi pahalı ve karmaşıktır; paylaşımlı DB (shared-DB) ise güvenlik ve gizlilik endişelerine sahiptir ve ayrıca RAG uygulamasının ölçeklenebilirliğini ve performansını sınırlar. Nile, Postgres'i her iki dünyanın en iyisini sunacak şekilde yeniden tasarladı: paylaşımlı bir DB'nin maliyetinde, verimliliğinde ve geliştirici deneyiminde, kiracı başına DB'nin izolasyonunu sağlar.

Paylaşımlı bir DB'de milyonlarca vektörü saklamak yavaş olabilir ve indeksleme/sorgulama için önemli kaynaklar gerektirebilir. Ancak Nile'ın sanal kiracı veritabanlarında, her biri 1000 vektöre sahip 1000 kiracı saklarsanız, bu oldukça yönetilebilir olabilir. Özellikle büyük kiracıları kendi işlem güçlerine (compute) yerleştirebilirken, küçük kiracıların işlem kaynaklarını verimli bir şekilde paylaşmasını ve gerektiğinde otomatik olarak ölçeklenmesini sağlayabilirsiniz.

## Nile ile Başlarken

[Nile](https://console.thenile.dev/?utm_campaign=partnerlaunch&utm_source=llamaindex&utm_medium=docs)'a kaydolarak başlayın. Nile'a kaydolduktan sonra, ilk veritabanınızı oluşturmanız istenecektir. Devam edin ve oluşturun. Yeni veritabanınızın "Query Editor" (Sorgu Düzenleyici) sayfasına yönlendirileceksiniz.

Oradan "Home"a (sol menüdeki üst simge) tıklayın, "generate credentials" (kimlik bilgileri oluştur) butonuna basın ve sonuçta oluşan bağlantı dizesini kopyalayın. Bir saniye içinde buna ihtiyacınız olacak.

## Ek Kaynaklar

- [Nile'ın LlamaIndex dokümantasyonu](https://www.thenile.dev/docs/partners/llama)
- [Nile'ın üretken yapay zeka ve vektör gömme dokümanları](https://www.thenile.dev/docs/ai-embeddings)
- [Nile'ın pgvector el kitabı](https://www.thenile.dev/docs/ai-embeddings/pg_vector)
- [pgvector hakkında bilmediğiniz birkaç şey](https://www.thenile.dev/blog/pgvector_myth_debunking)

## Başlamadan Önce

### Bağımlılıkları Kurun

Bağımlılıkları kuralım ve içe aktaralım.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-nile
```

```bash
!pip install llama-index
```

```python
import logging


from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from llama_index.vector_stores.nile import NileVectorStore, IndexType
```

### Nile Veritabanına Bağlantı Kurun

Nile ile Başlarken bölümündeki talimatları uyguladıysanız, artık Nile veritabanınıza bir bağlantı dizginiz olmalıdır.

Bunu `NILEDB_SERVICE_URL` adlı bir ortam değişkeninde veya doğrudan Python'da ayarlayabilirsiniz.

```bash
%env NILEDB_SERVICE_URL=postgresql://kullaniciadi:sifre@us-west-2.db.thenile.dev:5432/niledb
```

Ve şimdi bir `NileVectorStore` oluşturacağız. URL ve boyutlar gibi olağan parametrelere ek olarak `tenant_aware=True` ayarını da yaptığımıza dikkat edin.

🔥 `NileVectorStore`, hem her kiracı (tenant) için belgeleri izole eden kiracı duyarlı (tenant-aware) vektör depolarını hem de genellikle tüm kiracıların erişebileceği paylaşılan veriler için kullanılan normal bir depoyu destekler. Aşağıda, kiracı duyarlı vektör deposunu göstereceğiz.

```python
# NILEDB_SERVICE_URL değişkenine sahip yerel .env dosyasını okuyarak servis url'sini alın
import os


NILEDB_SERVICE_URL = os.environ["NILEDB_SERVICE_URL"]


# VEYA açıkça ayarlayın
# NILEDB_SERVICE_URL = "postgresql://nile:sifre@db.thenile.dev:5432/nile"


vector_store = NileVectorStore(
    service_url=NILEDB_SERVICE_URL,
    table_name="documents",
    tenant_aware=True,
    num_dimensions=1536,
)
```

### OpenAI Kurulumu

Bunu bir .env dosyasında veya doğrudan Python'da ayarlayabilirsiniz.

```bash
%env OPENAI_API_KEY=sk-...
```

## Çok Kiracılı Benzerlik Araması

LlamaIndex ve Nile ile çok kiracılı benzerlik aramasını göstermek için, her biri farklı bir şirketin satış görüşmesine ait dökümleri içeren iki belge indireceğiz. Nexiv BT hizmetleri sunarken, ModaMart perakende sektöründedir. Her belgeye kiracı tanımlayıcıları ekleyeceğiz ve onları kiracı duyarlı bir vektör deposuna yükleyeceğiz. Ardından, depoyu her kiracı için sorgulayacağız. Aynı sorunun nasıl iki farklı yanıt oluşturduğunu göreceksiniz; çünkü her kiracı için farklı belgeleri getirecektir.

### Veriyi İndir

```bash
!mkdir -p data
!wget "https://raw.githubusercontent.com/niledatabase/niledatabase/main/examples/ai/sales_insight/data/transcripts/nexiv-solutions__0_transcript.txt" -O "data/nexiv-solutions__0_transcript.txt"
!wget "https://raw.githubusercontent.com/niledatabase/niledatabase/main/examples/ai/sales_insight/data/transcripts/modamart__0_transcript.txt" -O "data/modamart__0_transcript.txt"
```

### Belgeleri Yükle

Belgeleri yüklemek için LlamaIndex'in `SimpleDirectoryReader`ını kullanacağız. Belgeleri yükledikten sonra kiracı meta verileriyle güncellemek istediğimiz için her kiracı için ayrı bir okuyucu (reader) kullanacağız.

```python
reader = SimpleDirectoryReader(
    input_files=["data/nexiv-solutions__0_transcript.txt"]
)
documents_nexiv = reader.load_data()


reader = SimpleDirectoryReader(input_files=["data/modamart__0_transcript.txt"])
documents_modamart = reader.load_data()
```

### Belgeleri Kiracı Meta Verileriyle Zenginleştirin

İki Nile kiracısı (tenant) oluşturacağız ve her birinin kiracı kimliğini (tenant ID) belge meta verilerine ekleyeceğiz. Ayrıca özel bir belge kimliği ve kategori gibi bazı ek meta veriler de ekliyoruz. Bu meta veriler, erişim sürecinde belgeleri filtrelemek için kullanılabilir. Elbette kendi uygulamanızda mevcut kiracılar için de belgeler yükleyebilir ve yararlı bulduğunuz herhangi bir meta veri bilgisini ekleyebilirsiniz.

```python
tenant_id_nexiv = str(vector_store.create_tenant("nexiv-solutions"))
tenant_id_modamart = str(vector_store.create_tenant("modamart"))


# Kiracı kimliğini meta veriye ekle
for i, doc in enumerate(documents_nexiv, start=1):
    doc.metadata["tenant_id"] = tenant_id_nexiv
    doc.metadata[
        "category"
    ] = "BT"  # Bunu daha sonraki bir örnekte ek filtreler uygulamak için kullanacağız
    doc.id_ = f"nexiv_doc_id_{i}"  # Özel bir id de belirliyoruz, bu isteğe bağlıdır ancak kullanışlı olabilir


for i, doc in enumerate(documents_modamart, start=1):
    doc.metadata["tenant_id"] = tenant_id_modamart
    doc.metadata["category"] = "Perakende"
    doc.id_ = f"modamart_doc_id_{i}"
```

### NileVectorStore ile VectorStore İndeksi Oluşturma

Tüm belgeleri aynı `VectorStoreIndex`e yüklüyoruz. Ayarlarımızı yaparken kiracı duyarlı bir `NileVectorStore` oluşturduğumuz için Nile, belgeleri izole etmek üzere meta verideki `tenant_id` alanını doğru bir şekilde kullanacaktır.

`tenant_id` olmadan belgeleri kiracı duyarlı bir depoya yüklemek `ValueException` hatasına neden olur.

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents_nexiv + documents_modamart,
    storage_context=storage_context,
    show_progress=True,
)
```

### İndeksi Her Kiracı İçin Sorgulama

Aşağıda her sorgu için kiracıyı nasıl belirttiğimizi ve dolayısıyla sadece o kiracı için geçerli bir yanıt aldığımızı görebilirsiniz.

```python
nexiv_query_engine = index.as_query_engine(
    similarity_top_k=3,
    vector_store_kwargs={
        "tenant_id": str(tenant_id_nexiv),
    },
)


print(nexiv_query_engine.query("Müşterinin yaşadığı sıkıntılar (pain points) nelerdi?"))
```

**"Müşterinin sıkıntıları, müşteri verilerini birden fazla platform kullanarak yönetmekle ilgiliydi; bu durum veri tutarsızlıklarına, zaman alan uzlaştırma çabalarına ve üretkenliğin azalmasına neden oluyordu."**

```python
modamart_query_engine = index.as_query_engine(
    similarity_top_k=3,
    vector_store_kwargs={
        "tenant_id": str(tenant_id_modamart),
    },
)


print(modamart_query_engine.query("Müşterinin yaşadığı sıkıntılar (pain points) nelerdi?"))
```

**"Müşterinin sıkıntıları; kışlık ceketlerin kalitesi ve değeri hakkındaki endişeler, yorumlara yönelik şüphecilik, çevrimiçi kıyafet siparişi verirken beden ve uyum konusundaki endişeler ve sıcak tutan ama hafif bir ceket isteğiydi."**

### Mevcut Gömmeleri Sorgulama

Yukarıdaki örnekte, yeni belgeleri yükleyip gömerek indeksi oluşturduk. Peki ya gömmeleri zaten oluşturup Nile'da sakladıysak? Bu durumda `NileVectorStore`u yine yukarıdaki gibi başlatırsınız, ancak `VectorStoreIndex.from_documents(...)` yerine şunu kullanırsınız:

```python
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(
    vector_store_kwargs={
        "tenant_id": str(tenant_id_modamart),
    },
)
response = query_engine.query("Takip etmemiz gereken aksiyon maddeleri nelerdir?")


print(response)
```

**"Takip edilmesi gereken aksiyon maddeleri şunları içerir: müşteriye ceketlerin hafiflik ve sıcak tutma özellikleri hakkında detaylı tanıklılar göndermek, müşteriye bir beden kılavuzu sağlamak ve müşteriye ilk alışverişinde %10 indirim kuponu e-postası göndermek."**

## Yaklaşık En Yakın Komşu Araması için ANN İndekslerini Kullanma

Nile, pgvector tarafından desteklenen tüm indeksleri destekler - IVFFlat ve HNSW. IVFFlat daha hızlıdır, daha az kaynak kullanır ve ayarlanması basittir. HNSW oluşturmak ve kullanmak için daha fazla kaynak kullanır ve ayarlanması daha zordur ancak harika doğruluk/hız dengelerine sahiptir. Gelelim indeksleri nasıl kullanacağımıza (her ne kadar 2 belgeli bir örnek aslında bunları gerektirmese de).

### IVFFlat İndeksi

IVFFlat indeksleri, vektör uzayını "listeler" adı verilen bölgelere ayırarak, önce en yakın listeleri bulup ardından bu listeler içindeki en yakın komşuları arayarak çalışır. İndeks oluşturma sırasında liste sayısını (`nlists`) belirtirsiniz ve sorgu yaparken aramada kaç en yakın listenin kullanılacağını (`ivfflat_probes`) belirtebilirsiniz.

```python
try:
    vector_store.create_index(index_type=IndexType.PGVECTOR_IVFFLAT, nlists=10)
except Exception as e:
    # İndeks zaten mevcutsa bu bir hata fırlatacaktır, bu beklenen bir durum olabilir
    print(e)


nexiv_query_engine = index.as_query_engine(
    similarity_top_k=3,
    vector_store_kwargs={
        "tenant_id": str(tenant_id_nexiv),
        "ivfflat_probes": 10,
    },
)


print(
    nexiv_query_engine.query("Takip etmemiz gereken aksiyon maddeleri nelerdir?")
)


vector_store.drop_index()
```

### HNSW İndeksi

HNSW indeksleri, vektör uzayını her katmanın değişen ayrıntı düzeylerinde noktalar arasındaki bağlantıları içerdiği çok katmanlı bir grafiğe ayırarak çalışır. Arama sırasında kaba katmanlardan daha ince katmanlara doğru ilerleyerek verideki en yakın komşuları belirler. İndeks oluşturma sırasında, bir katmandaki maksimum bağlantı sayısını (`m`) ve grafı oluştururken dikkate alınan aday vektör sayısını (`ef_construction`) belirtirsiniz. Sorgulama yaparken, aranacak aday listesinin boyutunu (`hnsw_ef`) belirtebilirsiniz.

```python
try:
    vector_store.create_index(
        index_type=IndexType.PGVECTOR_HNSW, m=16, ef_construction=64
    )
except Exception as e:
    # İndeks zaten mevcutsa bu bir hata fırlatacaktır
    print(e)


nexiv_query_engine = index.as_query_engine(
    similarity_top_k=3,
    vector_store_kwargs={
        "tenant_id": str(tenant_id_nexiv),
        "hnsw_ef": 10,
    },
)


print(nexiv_query_engine.query("Fiyatlandırmadan bahsettik mi?"))


vector_store.drop_index()
```

## Ek VectorStore İşlemleri

### Meta Veri Filtreleri

`NileVectorStore` ayrıca meta verilere dayanarak vektörlerin filtrelenmesini destekler. Örneğin, belgeleri yüklediğimizde her belge için `category` meta verisini dahil etmiştik. Artık getirilen belgeleri filtrelemek için bu bilgiyi kullanabiliriz. Bu filtrelemenin kiracı filtresine **ek olarak** yapıldığını unutmayın. Kiracı duyarlı bir vektör deposunda, yanlışlıkla veri sızıntılarını önlemek için kiracı filtresi zorunludur.

```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="category", operator=FilterOperator.EQ, value="Perakende"
        ),
    ]
)


nexiv_query_engine_filtered = index.as_query_engine(
    similarity_top_k=3,
    filters=filters,
    vector_store_kwargs={"tenant_id": str(tenant_id_nexiv)},
)
print(
    "Kategori = Perakende filtresiyle nexiv üzerinde test sorgusu (boş dönmeli): ",
    nexiv_query_engine_filtered.query("Müşterinin sıkıntıları nelerdi?"),
)
```

### Belgeleri Silme

Belgeleri silmek oldukça önemli olabilir, özellikle bazı kiracılarınız GDPR'nin gerekli olduğu bir bölgedeyse.

```python
ref_doc_id = "nexiv_doc_id_1"
vector_store.delete(ref_doc_id, tenant_id=tenant_id_nexiv)


# Veriyi tekrar sorgula
print(
    "Silme işleminden sonra nexiv üzerinde test sorgusu (boş dönmeli): ",
    nexiv_query_engine.query("Müşterinin sıkıntıları nelerdi?"),
)
```
