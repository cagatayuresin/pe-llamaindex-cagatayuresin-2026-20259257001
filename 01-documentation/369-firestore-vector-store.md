---
title: Firestore Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Google Firestore (Yerel Mod - Native Mode)

> [Firestore](https://cloud.google.com/firestore), her türlü talebi karşılayacak şekilde ölçeklenen, sunucusuz (serverless), doküman yönelimli bir veritabanıdır. Firestore'un LlamaIndex entegrasyonlarından yararlanarak yapay zeka destekli deneyimler oluşturmak için veritabanı uygulamanızı geliştirin.

Bu not defteri, vektörleri saklamak ve `FirestoreVectorStore` sınıfını kullanarak bunları sorgulamak için [Firestore](https://cloud.google.com/firestore) veritabanının nasıl kullanılacağını ele almaktadır.

## Başlamadan Önce

Bu not defterini çalıştırmak için aşağıdakileri yapmanız gerekecektir:

- [Bir Google Cloud Projesi Oluşturun](https://developers.google.com/workspace/guides/create-project)
- [Firestore API'yi Etkinleştirin](https://console.cloud.google.com/flows/enableapi?apiid=firestore.googleapis.com)
- [Bir Firestore veritabanı oluşturun](https://cloud.google.com/firestore/docs/manage-databases)

Bu not defterinin çalışma ortamında veritabanına erişimi onayladıktan sonra, örnek betikleri çalıştırmadan önce aşağıdaki değerleri doldurun ve hücreyi çalıştırın.

## Kütüphane Kurulumu

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir. Bu not defteri için, Google Generative AI gömmelerini (embeddings) kullanmak amacıyla `llama-index-vector-stores-firestore` ve `llama-index-embeddings-huggingface` paketlerini de kuracağız.

```bash
%pip install --quiet llama-index
%pip install --quiet llama-index-vector-stores-firestore llama-index-embeddings-huggingface
```

### ☁ Google Cloud Projenizi Ayarlayın

Bu not defterindeki Google Cloud kaynaklarından yararlanabilmek için Google Cloud projenizi ayarlayın.

Proje kimliğinizi (project ID) bilmiyorsanız, şunları deneyebilirsiniz:

- `gcloud config list` komutunu çalıştırın.
- `gcloud projects list` komutunu çalıştırın.
- Destek sayfasını inceleyin: [Proje kimliğini bulma](https://support.google.com/googleapi/answer/7014113).

```python
# @markdown Lütfen aşağıdaki değeri Google Cloud proje kimliğinizle doldurun ve ardından hücreyi çalıştırın.


PROJECT_ID = "PROJE_KIMLIGINIZ"  # @param {type:"string"}


# Proje kimliğini ayarla
!gcloud config set project {PROJECT_ID}
```

### 🔐 Kimlik Doğrulama

Google Cloud Projenize erişmek için bu not defterinde oturum açmış IAM kullanıcısı olarak Google Cloud'da kimlik doğrulaması yapın.

- Bu not defterini çalıştırmak için Colab kullanıyorsanız, aşağıdaki hücreyi kullanın ve devam edin.
- Vertex AI Workbench kullanıyorsanız, kurulum talimatlarını [buradan](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env) inceleyin.

```python
from google.colab import auth


auth.authenticate_user()
```

# Temel Kullanım

### FirestoreVectorStore'u Başlatma

`FirestoreVectorStore`, verileri Firestore'a yüklemenize ve sorgulamanıza olanak tanır.

```python
# @markdown Lütfen demo amacıyla bir kaynak belirtin.
COLLECTION_NAME = "test_koleksiyonu"
```

```python
from llama_index.core import SimpleDirectoryReader


# Belgeleri yükle ve indeksi oluştur
documents = SimpleDirectoryReader(
    "../../examples/data/paul_graham"
).load_data()
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


# Gömme modelini ayarlayın, bu yerel bir modeldir
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

```python
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, ServiceContext


from llama_index.vector_stores.firestore import FirestoreVectorStore


# Bir Firestore vektör deposu oluşturun
store = FirestoreVectorStore(collection_name=COLLECTION_NAME)


storage_context = StorageContext.from_defaults(vector_store=store)
service_context = ServiceContext.from_defaults(
    llm=None, embed_model=embed_model
)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)
```

```text
/var/folders/mh/cqn7wzgs3j79rbg243_gfcx80000gn/T/ipykernel_29666/1668628626.py:10: DeprecationWarning: Call to deprecated class method from_defaults. (ServiceContext kullanım dışıdır, lütfen bunun yerine `llama_index.settings.Settings` kullanın.) -- 0.10.0 sürümünden beri kullanım dışıdır.
  service_context = ServiceContext.from_defaults(llm=None, embed_model=embed_model)


LLM açıkça devre dışı bırakıldı. MockLLM kullanılıyor.
```

### Arama gerçekleştirme

Sakladığınız vektörler üzerinde benzerlik aramaları yapmak için `FirestoreVectorStore` kullanabilirsiniz. Bu, benzer belgeleri veya metinleri bulmak için kullanışlıdır.

```python
query_engine = index.as_query_engine()
res = query_engine.query("Yazar büyürken neler yaptı?")
print(str(res.source_nodes[0].text))
```

```text
None
Neler Üzerine Çalıştım


Şubat 2021


Üniversiteden önce, okul dışında çalıştığım iki ana konu yazarlık ve programlamaydı. Makale yazmazdım. O zamanlar başlangıç seviyesindeki yazarların ne yazması gerekiyorsa onları yazardım (hâlâ da muhtemelen öyledir): kısa hikayeler. Hikayelerim berbattı. Neredeyse hiç olay örgüsü yoktu, sadece güçlü hisleri olan karakterler vardı ve bunun onları derin kıldığını hayal ederdim.


Yazmayı denediğim ilk programlar, okul bölgemizin o zamanlar "veri işleme" (data processing) dedikleri şey için kullandığı IBM 1401 üzerindeydi. Bu 9. sınıftaydı, yani 13 veya 14 yaşındaydım. Okul bölgesinin 1401'i tesadüfen ortaokulumuzun bodrumundaydı ve arkadaşım Rich Draves ile birlikte onu kullanmak için izin almıştık. Aşağısı küçük bir Bond kötüsünün sığınağı gibiydi; CPU, disk sürücüleri, yazıcı, kart okuyucu gibi tüm bu uzaylı görünümlü makineler, parlak floresan ışıklar altında yükseltilmiş bir zeminde duruyordu.


Kullandığımız dil, Fortran'ın erken bir sürümüydü. Programları delikli kartlara yazmanız, sonra onları kart okuyucuya istiflemeniz ve programı belleğe yükleyip çalıştırmak için bir düğmeye basmanız gerekiyordu. Sonuç normalde fevkalade gürültülü yazıcıda bir şeyler yazdırmak olurdu.


1401 kafamı karıştırmıştı. Onunla ne yapacağımı tam çözememiştim. Ve geriye dönüp baktığımda, onunla yapabileceğim pek bir şey de yoktu. Programlara tek girdi biçimi delikli kartlarda saklanan verilerdi ve bende delikli kartlarda saklanan hiç veri yoktu. Diğer tek seçenek, pi sayısının yaklaşımlarını hesaplamak gibi herhangi bir girdiye dayanmayan şeyler yapmaktı, ancak bu türden ilginç bir şey yapacak kadar matematik bilmiyordum. Bu yüzden yazdığım hiçbir programı hatırlamamam şaşırtıcı değil, çünkü pek bir şey yapmış olamazlar. En net hatırladığım an, programların sonlanmamasının mümkün olduğunu öğrendiğim andı; benimkilerden biri bitmek bilmemişti. Paylaşımlı zaman (time-sharing) olmayan bir makinede bu, veri merkezi yöneticisinin yüz ifadesinden de anlaşıldığı üzere, teknik olduğu kadar sosyal bir hataydı da.


Mikrobilgisayarlarla her şey değişti. Artık tam karşınızda, masanızın üstünde, bir deste delikli kartı işleyip durmak yerine, çalışırken tuş vuruşlarınıza yanıt verebilen bir bilgisayarınız olabilirdi. [1]


Mikrobilgisayar alan ilk arkadaşım onu kendi yapmıştı. Heathkit tarafından bir kit olarak satılıyordu. Bilgisayarın önünde oturup programları doğrudan bilgisayara yazdığını izlerken ne kadar etkilendiğimi ve kıskandığımı canlı bir şekilde hatırlıyorum.


O günlerde bilgisayarlar pahalıydı ve babamı bir tane (yaklaşık 1980'de bir TRS-80) almaya ikna etmem yıllarca dil dökmemi gerektirmişti. O zamanki altın standart Apple II idi, ancak bir TRS-80 yeterince iyiydi. Gerçekten programlamaya başladığım zaman buydu. Basit oyunlar, model roketlerimin ne kadar yükseğe uçacağını tahmin eden bir program ve babamın en az bir kitap yazmak için kullandığı bir kelime işlemci yazdım. Bellekte sadece yaklaşık 2 sayfalık metin için yer vardı, bu yüzden her seferinde 2 sayfa yazar ve sonra yazdırırdı ama bu bir daktilodan çok daha iyiydi.


Programlamayı sevsem de üniversitede okumayı planlamıyordum. Üniversitede, kulağa çok daha güçlü gelen felsefe okuyacaktım. Saf lise benliğim için felsefe, diğer alanlarda çalışılan şeylerin sadece alan bilgisi kalacağı mutlak gerçeklerin incelenmesi gibi görünüyordu. Üniversiteye gittiğimde keşfettiğim şey ise, diğer alanların fikir dünyasında o kadar çok yer kapladığıydı ki, bu sözde mutlak gerçekler için pek bir şey kalmamıştı. Felsefeye kalan tek şey, diğer alanlardaki insanların güvenle görmezden gelinebileceğini düşündüğü uç vakalardı.


18 yaşındayken bunu kelimelere dökemezdim. O sırada tek bildiğim, felsefe dersleri almaya devam ettiğim ve bunların sıkıcı olmaya devam ettiğiydi. Ben de yapay zekaya (AI) geçmeye karar verdim.


1980'lerin ortalarında yapay zeka revaçtaydı ama üzerinde çalışmak istememe neden olan özellikle iki şey vardı: Heinlein'ın Mike adında zeki bir bilgisayarı konu alan "The Moon is a Harsh Mistress" (Ay Zalim Bir Sevgilidir) adlı romanı ve Terry Winograd'ın SHRDLU kullandığını gösteren bir PBS belgeseli. "The Moon is a Harsh Mistress"ı yeniden okumayı denemedim, bu yüzden ne kadar iyi eskidiğini bilmiyorum ama okuduğumda beni tamamen dünyasının içine çekmişti.
```

Arama sonuçlarına `filters` argümanı belirterek ön filtreleme uygulayabilirsiniz.

```python
from llama_index.core.vector_stores.types import (
    MetadataFilters,
    ExactMatchFilter,
    MetadataFilter,
)


filters = MetadataFilters(
    filters=[MetadataFilter(key="author", value="Paul Graham")]
)
query_engine = index.as_query_engine(filters=filters)
res = query_engine.query("Yazar büyürken neler yaptı?")
print(str(res.source_nodes[0].text))
```
