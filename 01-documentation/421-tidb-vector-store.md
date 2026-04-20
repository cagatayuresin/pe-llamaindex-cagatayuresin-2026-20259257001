---
title: TiDB Vektör Deposu (TiDB Vector Store)
 | LlamaIndex OSS Belgeleri
---

# TiDB Vektör Deposu (TiDB Vector Store)

> [TiDB Cloud - TiDB Bulut (Hizmeti) / TiDB Serverless], tahsis edilmiş bizzat kendine ait / adanmış türlerle (dedicated options) ile/yahut sunucusuz / servissiz eylemsel seçeneklerini de bir arada tesis eden / temin dahi (provides) kılan bütünüyle sarmalayan çaplı ("comprehensive") Hizmet evreli Veritabanı / (Database-as-a-Service = DBaaS) çözüm atılımıdır. TiDB Sunucusuz hizmet evresi sistemi / varyasyon modeli (TiDB Serverless); hâl-i hazırda doğrudan MySQL sahasına / evreninin ortam tabanına içsel ("built-in") yerleşik kurgusuyla vektörel arama (vector search) dökümünü doğrudan adapte ve/ dahi de entegre eder/sunar. Sizler dahi de elinizdeki yetilerin bu son eklentisi / bu denli bu bir üstünleştirilen bu kapasite gelişimi (enhancement) vesilesi/vasfıyla yeni olan yepyeni başkaca veri tabanlarını falan gerektirmeksizin yahut eklentili, onca karmaşık ("additional technical stacks") teknolojik yığınlara gerek dahi bırakmadan TiDB Sunucusuz ("Serverless") vasıtasıyla pürüzsüz ("seamlessly"), zahmetsiz pür bir AI işlevi veyahutta evresini geliştiredebilir/yapılandırabilirsiniz ("develop AI applications"). Serbest / Bir tane ücretsiz/ serbest ("free TiDB Serverless cluster") TiDB Sunucusuz küme / kümelenimi de oluşturun, ardından da vektör aramalı o özelliğini asıl kullanımına start verebilmek ve işlemek / eyleme akmak dahi (<https://pingcap.com/ai> adresiyle/üstünden de erişerek) dahi başlayın (start using).

Bu not defteri (notebook), LlamaIndex içinde dahil olan "tidb" ibareli vektör arayış/sorgu motorunu kullanma ("utilizing the tidb vector search") mekaniğine ışık tutarak / dönük dair ince ve detaya tabanlı tam / ("detailed guide") eksen bir yönergeyi, yahutta sağlam bir izleği temin (ve o da yol kılavuzluğunu/rehberliği) sunar/tahsis ("provides") eder.

## Ortamları / Ortam evrelerini Yapılandırma ve Kurma (Setting up environments)

```bash
%pip install llama-index-vector-stores-tidbvector
%pip install llama-index
```

```python
import textwrap


from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

OpenAI API Anahtarınızın / Şifreli Verinizin (Key) Ayarlanması ve Yapılandırılması (Configuring)

```python
import getpass
import os


os.environ["OPENAI_API_KEY"] = getpass.getpass("Lütfen OpenAI API anahtarınızı (key) sisteme takdim ile girin / işleyin (Input your OpenAI API key):")
```

Size ("that you will need" - lazımda kalacak / size zaruri gereken/yahutta ihtiyaç ve elinizde de de duyacağınız) TiDB evrelerinin (kurulacak - connection setting) o bağlanım tabiatlı / bağlantısal değer / ayarlar tabanına o deklarede dahi (Configure) de form evresi kurun. Kendi (To connect to your - bünyenizdeki sistem - tabanda yatan TiDB ortamınıza) TiDB bulutunuza / Bulut Tabanındaki Kümelenme verinize bağlanmak / ve o entegreyi tamamlamak/için bu şu safhalı/evreli (follow these steps / bu denklemli süreci vb) aşamaları resmen izlemeli/kat de dahi ederek takipte kalın/tatbike sokun:

- Kendi asıl/asli form da dahi eldeki ("Go to your.../Sizin o") sistem / o formki / TiDB Bulut (Cloud) tabanınızın dahi küme yapısının barınan (cluster / veri salkımları) Konsol döküm / Arayüz sahası paneli evrenine uzanıp sekmeyle de ("Connect/Bağlan" evresindeki bağlantı sayfasına (the `Connect` page)) dahi gezintileyin / adım tabiat atın.
- SQLAlchemy'yi dahi de ('SQLAlchemy' formuyal beraber) "PyMySQL" entegre formunda/yahut tabiat ile bizzat de "birlikte kullanma suretinde vararak / kullanılarak da o entegreyi sağlamaya ("Select the option to connect using") yönelik/ve o husutaki (ve ibareki o seçimi/durumu-seçeneği dahi vb) tıklama yoluyla/yahut bizzat seçin ("Select the option")...", o seçime de binaende ve bilakis takdim de kılışan / ekranda beliren bağlantı yol/evreli (URL adresinin) URL adres -/ve bağlantısını dahi ("and copy the provided connection URL") tüm safhasıyla (lakim unutmayın (without password) katiyetle sisteme yahut döküme falan da o dökülen şifresiz ("şifresinin" eksik) biçimde olan form/uzantıyla dahi vs) kopyalamasına ("copy") varın.
- Şimdiki sonlara yakın evre/formdaki bağlamınız ve kod yapınız de (into your code), kopyalamaya da dahil o/döküm (connection URL - URL bağlantısını vb dahi o link adres metnini), sadece tabandaki/veride aslen geçen `tidb_connection_string_template` sistem değisikeni / ibaresi konumuna devretmek suretiyle ("replacing" onun yerine ikame yap/üzerine vb atarak de / de ikame kılmaz yahut değiştirme niyetiyle) dahi de bir nevi o değerdeki alana sığdırıp - yapıştırın ("Paste the...").
- Şifrenizi (parolanızı) falan (Type your password) aslen/bizzatı dahi klavye tabanlı vs "girin / yahut kendi el yazımınızla sisteme yazın - tuşlayın- deklareyee vs".

```python
# Kendi TiDB Bulut ('tidb cloud') tabanlı sunulan arayüz / o konsol sayfasından vb o alandan kopyaladığınız, kendi - ("replace with your/sizin_olan") asıl 'tidb' entegre bağlantı veri dökümü/yapı dizgini ile (connect string/bağlantı dizesi yahutta değer formatıyla dahi vs.) buradakini yer değiştirin.
tidb_connection_string_template = "mysql+pymysql://<KULLANICI_ADI/USER>:<SIFRE/PASSWORD>@<SUNUCU/HOST>:4000/<VERITABANI_ADI/DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
# TiDB parolanızı/şifrenizi ("tidb password") buraya yazınız (girin vb - type)
tidb_password = getpass.getpass("TiDB Parolanızı (password) lütfen/sisteme asgari de dökün/giriniz:")
tidb_connection_url = tidb_connection_string_template.replace(
    "<SIFRE/PASSWORD>", tidb_password
)
```

Görünüşte bir demo/örnek vaka formu gibi ve de tabiatına (that used to show case / durum-vakıa vb örneği olarak de kullanılmak ve/sunum yapmak / gösterim-göstermek) kullanılmaya dair döküm olacak veri ve döküm dosyalarını (data) vb tertipleyin / de hazırla-yayarak çekin (Prepare).

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
for index, document in enumerate(documents):
    document.metadata = {"book": "paul_graham"}
```

```bash
Document ID: 86e12675-2e9a-4097-847c-8b981dd41806
```

## TiDB Vektör Deposunun (Vectore Store) Yaratılıp Kurulması (Create)

Aşağı yönünde yazılı gelen kod taslağı yahut (The code snippet below), TiDB içinde sistemsel/bizzat dahi direkt bizzat "büyük ve aslen optimize olan/yani epey/cidden o" vektörel döküm/sorgulara ya da bağlam - ("optimized for vector searching") arama evresine en asgari yapısıyla o tam eyleme/amaca odaklı, mükemmelleştiririlip optime (yahutta evrede optimize) bir eylemle edilmiş (isimli) `VECTOR_TABLE_NAME` varlık ad(label) ismiyle/olarak da anılan bir tablo/çizelge yahutta alan dizin var edip inşa/tesis ("creates a table named") eylemektedir. İşte kuran bu o/ ("of this code") taban varlık/veyahut form da başarılı (tam randımanlı -"successful") tahhakkuku/icrası ya da çalışmasından / yürütülmesinden bitip de tamamlanır akabindeki an ("Upon successful execution... , you will be able to") evrelerinde de, tüm bir o dizelge / alandaki " `VECTOR_TABLE_NAME` " veri tablasını tam direkt/dosdoğru form evreyle bizzat (directly within) salt/direkt o kendi olan kendi ('your') "TiDB" dökümlü sisteminizde/ o veritabanı (TiDB database environment) ekolojik - ekosistemi bünyesindeki evrede dökümp de falan ("view and access") - / aslen hem tüm görüntülemesine de ve de keza resmen erişilmesine dahi imkân tanınıp/muktedir var edilmiş formlu bir tabanda yeriniz olabilecektir (you will be able to varıp erişebilirsiniz...).

```python
VECTOR_TABLE_NAME = "paul_graham_test_tablo_adi"
tidbvec = TiDBVectorStore(
    connection_string=tidb_connection_url,
    table_name=VECTOR_TABLE_NAME,
    distance_strategy="cosine",
    vector_dimension=1536,
    drop_existing_table=False,
)
```

Üste bahsi gelip o kurulan tiDB vektör yapısına - /yahutta 'tidb' dökümüyle tesis olan bu veri bazlı o temel (based on tidb vectore store) Vektör deposu mimarisinin üzerinde tamı tamına yatan ("Create a query engine based on") kurgusunda/merkezsinde bir de yeni (arama sorgusu/ yahut işlev motoru) sorgu motoru formu / "query engine" tabir/evreni ve dizgesi (Create a query) oluşturun (inşa).

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
```

Ehemmiyetli Not (Note): Şayet (If you), "MySQL protolokolünün / kendi sisteminin sahip ve kendisindeki de barındığı iletişim form evresi / yahut protokol o veri boyu paketi limit kısıtı ( MySQL protocol’s packet size limitation / engel formu ile ) " vesile - hasebiyle ve ya - kaynaklı / (due to ile dahi (bundan dolayısı)) tam bu aşamadaki operasyon evrimde aslen falan eyleme ("during this process") resmen veyahut bir denli (encounter errors) o hata sekans/yahut "arızalara meylekip / veya resmen takılmalar falan" (e.g. , 2000 satıra (rows) ya da yığına/kapsama yakın falan (en çok / o kadar meblağca dahi "large number of vectors") olan çok epey sayıda da o asgari büyük hacim ("like inserting a large.../when trying to / falan gibicesine sokmaya-araya sokma ya da içeri aktarımlarda falan / ya yeltenmelere dek gibi") vektör evren - kayıt eklemesine deneme/ve meyil / de yahut çabasındayken olan gibi) rastlarsınız; yığını veya tam içeri basıp-ve eylem verisindeki döküm sokuşturma vb gibi işlemi (insertion / veri sokmalrını vs), tam oldukça da dahi daha minimal, ufak/küçük o hacimli asgari çaplı dökümcüklere ('into smaller batches') parça hisseleri formunda de ufak porsiyon / partiler halinde vs da (bölerek/yahutta - / kesip vb bölerek dahi (splitting) kırmak/evirmek / dahi yöntemi ile vb) tam/resmen / (bu pürüz yahut musibet sorunu ve de "mitigate this issue") bu vaziyeti daha esnek yahut o esnek kıvamında varan yapısıyla yatıştırarak aşabilirsiniz/yahutta epey / rahatı sulara-en azda/en aza kısıpta dahi o asgari o "o hafifletmede" (baskı-yı kırmak vs) bulabilirsiniz. Söz gelimi / Farz - mesele formundaki bir tasavvur vs. örnein dahi ('For example'); veri paketi evre döküm/beden limit kısıtını (the packet size limit) falan taşma/ihlal sınırlarını / değerleri ("exceeding the packet size limit") de (asgari yahutta o taşmadan vesveselerde) geçmesinden olabildecek kadar o imtinayi o koruma çemberine-yahut - / dahi ("avoid exceeding... - aşından formuna da evrilmeden - ondan korumak-çekinerek vb) sakınıp/ondan "kaçınmak - "kaçınmaya matuf dahi vs)", tam verilerinizin tüm döküm yapı/olarak (your data) resmiden/yegane TiDB ("into the TiDB vector store) vektör verisine/deposuna kusursuz ya pürürsüz/dahi (ensuring smooth insertion - sağlaması/ yahutta pürürssü akış-sorunsuzca vb aktarımı "teminat") girmesini / veri kaydının atılması işlemi dökümünü de - emniyete dahi temin vesile ettirmesine dahi cidden ("ensuring smooth insertion") de bizzat ve resmen o garantilemeli eylemi - ('ensuring smooth.... / sağlamak adıyla formuna / için, o dahi vb vs) - garantilemek adına da `insert_batch_size (giris_parti_parcalama_ebati)` ibresini/ yahutta (asıl parametresi-form - / parametresini (the parameter)) olan de döküm değişkenini vb; resmen / değerde dahi daha cidden aşağı - minval (e.g. 1000 - / misal asgarisinde misali ("e.g. 1000") = örnek olsun vs. 1000 ("bin") de /yahutta gibi dahi vs... ) o değer ("smaller value" değerindeki / ya nicelikteki de / ufak "diğerine" asgari/kısık/düşük olan bir meblağa vs formlu bir değere de vs... ("to a smaller value") ) orana çekerek vs ayarlamasında " (can set - deklare vs)" / atamalısına meylederek ("you can set/atamasını eyleyebilirsiniz dahi") kurguya girebilirsiniz (ayarlayabilirsiniz falan):

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, insert_batch_size=1000, show_progress=True
)
```

## Anlamsal - semantik/ve mana türünde (bağlama dönük dahi formunda vs) benzerlik araması (Semantic similarity search)

Söz konusu mevzu yahut tüm o (This section - Bu mühim (ve de evre) olan bölüm / veya alan); tekmil ve aslen temel ve en zemin baz dökümlerinden ('basics' olan tabanı dahi/ yahut vs temel esas/olanlara - focus on... vb) gelen o esas (vektörel asıl/arama vs) - vektör aramalı evresinin döküm zemin/ve temel unsurlarına, keza / (dahi-bununla -/ve) ve dahi formundaki bir filtre/ayıklayıcı vb ('metadata filters') vasıtadaki işlevi - ve o filtre mekanizmaları (meta/üst verili süzeç olanlar -) ve süzme aracı dahi ile bizzat kullanması/tahsis yolu ile de; aradan kalanlardan en "süzülen falan (refining results - sonuç bağlamlarıyla rafine)" - dökülen netice bakiye evrenlerinden (neticelerin ayıklanarak incelmesi falan - iyileştirilmesine / rafine evresine vs de dahi vb) epey / odak noktalarına eğilir, - bizzat odaklanılır (This section focus on).  Sisteme ya da lütfederek / lütfen dahi ('Please note that/... dikkate alın yahut o detayın-zihine de (Please note)- kaydedilmesine dikkat vs...'); "tidb ve form tabiatlı oktör" yahutta genel de ki " "tidb vektör ("tidb vector") " bizzat ve/sadece asıl fıtratından gelme (varsayılan) niteliğine uyacak (Deafult / "Default VectorStoreQueryMode") VectorStoreQueryMode / yahut dökümlerde de - (Varsayılan VektorDeposuSorguModunu) yapısını destekler.
(Not: Sadece Default (Varsayılan) VectorStoreQueryMode formu desteklenmektedir.)

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar nele meşgul olmuştur/yahut aslen ne yapmıştır? (What did the author do?)")
print(textwrap.fill(str(response), 100))
```

```bash
Yazar bir adet kitap/eser evresini derleyerek - esere / kaleme- de dahi veya- döküme yazı ("wrote a book") - yazmıştır.
```

### Metaveri ile (meta veriler asıl evresini) süzgeç formlarında Fitreleme (Filter with metadata)

Uygulanan o kurgulu tabiate konmuş - bizzat işlenen (uygulanan - applied filters) yahutta o dökülen (applied / o uygulanan vb) "applied filters (kullanılan formdaki filtre süzeçleriyle vs)" formundaki dökümlerle dahi - (ile örtüşüp dahi veya onun form ve evresine uyan / uyum içerisinde dahi o olandan -"that align with" (ki o uyumlu eşleyen hizalanan form vs))- en asıl ve ziyade asgari dahi belli, spesifik ebat ya bir nispette / yahut tutarda ('specific number') en en yakın olan "komşu/içte olan ("nearest-neighbor - en yakınından komşu de formunda") netice evreleri-sonuç silsielerini/dökümlerini dahi sistemi de falan -" alabilmesi - elde evirmesi/ve dahi veya "çağırıp vb ("retrieve") / alabilmekten yola / geri çekip de temin (ve getirmesi / geri alması falan vs)" vb/ için meta veri (üst düzeyli filtre aracı - 'metadata filters' )'yi süzme /filitreleyip formlarında yahut taban vasıta-ları ile  ( "using - vasıtası yahut kullanımı vs ile" dahi vs ) eyleme alarak / ('perform searches' (aramalar/ya taramaları aslen icra/ya (yapıp yerine getirmek/evirmek - işle vb)") atfederek / tatbiken o aramaları icrasına alın/ (yaparak / işletin falan vs - yürütün).

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
)


query_engine = index.as_query_engine(
    filters=MetadataFilters(
        filters=[
            MetadataFilter(key="book - / kitap (alan/anahtari)", value="paul_graham", operator="!="),
        ]
    ),
    similarity_top_k=2,
)
response = query_engine.query("Yazar ne/neleri falan ("öğrendi") -(edindi) - / yahuttan ne çıkardı/öğrendi? (What did the author learn?)")
print(textwrap.fill(str(response), 100))
```

```bash
Boş / Karşılıksız (Yahut/ - Hiçlik Dökümlü) Yanıt (Netice - Empty Response)
```

Yeniden ("again/tekrar") - Sorgulayın (Sual/Sorgu verisi atın).

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
)


query_engine = index.as_query_engine(
    filters=MetadataFilters(
        filters=[
            MetadataFilter(key="book", value="paul_graham", operator="=="),
        ]
    ),
    similarity_top_k=2,
)
response = query_engine.query("Yazar ne çıkardı/ yahut - ne öğrendi? (What did the author learn?)")
print(textwrap.fill(str(response), 100))
```

```bash
Yazar / Kalem-Sahibi; (Author) kendi - ve bizzat o hayat ve yahut şahsi tecrübe ve deneyim bulgusu ve / yaşantılarından da dahi - paha evresinde (ve hayli değerli o paha döküm ve "valuable lessons (değeri hayli epey kıymetli falan cidden" ) biçilmez dahi dersleri bürüyen evre çıkarımı/çıkarımları dahi (dersleri / lessons vs / cidden falan tecrübeyle cidden ) de - edindi/ders çıkartıp - / öğrendi ("learned").
```

## Döküleri (veyahut Belgeleri / Doküman formları) silin (Delete documents)

```python
tidbvec.delete(documents[0].doc_id)
```

Belgelerin/veyahut form/dokümana malik olan dökümlerin ("whether the documents") tamı tamına yahutta - silinip / silinmediğine döküm ve yahuttaki ("had been deleted") formlarda bizzat cidden yok dahi yok de (silinip - silinmediğini vs dahi / denetliyip)  bir eylemsel - / - tetkik yapıp falan ('Check - / Kontrol edin') inceleyin.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neleri öğrenmişti/ (ve neyi) - ne öğrendi? (What did the author learn?)")
print(textwrap.fill(str(response), 100))
```

```bash
Boş (veyahutta Hiç / Noksan evreli ) Karşılık-Yanıt (Empty Response)
```
