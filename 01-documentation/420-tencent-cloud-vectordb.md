---
title: Tencent Bulut Vektör Veritabanı (Tencent Cloud VectorDB)
 | LlamaIndex OSS Belgeleri
---

# Tencent Bulut Vektör Veritabanı (Tencent Cloud VectorDB)

> [Tencent Cloud VectorDB (Tencent Bulut Vektör Veritabanı);](https://cloud.tencent.com/document/product/1709) tamamen ve tam denetimli yönetilen (fully managed), şirketin kendi öz geliştirmesiyle bünyesinde (self-developed) ürettiği çok boyutlu vektör (multi-dimensional vector) verilerinin alınıp saklanması/depolanması, getirilip çekilmesi (retrieving) ve verilerin tetkik ile analizleri için geliştirilmiş kurumsal düzeyde (enterprise-level), büsbütün dağıtık (distributed) bir veritabanı servisidir / platformudur. Bu veri/depo tabanı servisi; birden oldukça fazla indeks ve dizin formuna ve onun yanında envai türlü benzerlik hesaplama / bulma yöntemine de (similarity calculation methods) rahatça destek sağlar. Sadece (ve tek bir - a single index) dizin (indeks) bazında hesaba göre tahmini 1 milyara yakın ("up to 1 billion") bir vektör hacimli ölçeğe kadar tamı tamına bir destek aktarıp milyonu dahi aşan / olan ("millions of QPS") QPS ile resmen milisaniye periyotlarındaki (milisaniye seviyesi - millisecond-level) değerlere varan sorgu gecikmesini asgaride de eyleyerek/destekleyerek barındırabilir. Tencent Cloud Vektör Veritabanı / ortamı; Yalnızca ("not only") cüsseli formlara sahip geniş çaplı (büyük) dillere/modellere harici kaynak ve bir dış bilgi tabanı da (external knowledge base) sevk edip (provide), o devasa formlu modellerden akan dönüşlerin ve de cevaplarındaki isabet / o doğruluk derecesinin pürüzsüz yapısına (improve the accuracy) etken olup fayda sağlayanla beraber ("but can also be widely used"), ayrıca Yapay Zekanın (AI'ın) bilimum tavsiye sistem dizilimleriyle, NLP altyapı işlevleriyle, yapay (computer) görü yapılarıyla, dahi dahi (ve zeki diye de isimlendirilen) yetkin / akıllı bir müşteri - destek de hizmet (intelligent customer service) ağlarına dahi geniş ölçeklerden (yaygın platformlarla) de uygulanıp/kullanılabilir.

**Bu not defteri (notebook), TencentVectorDB'nin LlamaIndex'te / dökümünde bir Vektör Deposu (Vector Store) misali temelde kullanımını açıklar/gösterir.**

Burada eyleme alabilmek - çalıştırmak doğrultusunda tahsis edilmiş bir [Veritabanı örneğinizin / referansınızın](https://cloud.tencent.com/document/product/1709/95101) da (Database instance) elbette var olması icap edecektir.

## Kurulum (Setup)

Eğer bu Not Defterini (Notebook) Colab ortamında açıyorsanız, muhtemelen LlamaIndex'i 🦙 sisteminize kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-tencentvectordb
```

```bash
!pip install llama-index
```

```bash
!pip install tcvectordb
```

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.tencentvectordb import TencentVectorDB
from llama_index.core.vector_stores.tencentvectordb import (
    CollectionParams,
    FilterField,
)
import tcvectordb


tcvectordb.debug.DebugEnable = False
```

### Lütfen OpenAI erişim anahtarını (access key) deklare edip temin ederek sağlayın (provide)

OpenAI'in de yerleşimiyle olan gömmeler/katmanları (embeddings) layıkıyla tatbik edebilmek/uygulayabilmek yolunda da (In order use) sisteme kesinlikle bir OpenAI API lisans kod / anahtarı deklare etmeniz, yâni sağlamanız şarttır/elzemdir:

```python
import openai


OPENAI_API_KEY = getpass.getpass("OpenAI API Anahtari (Key):")
openai.api_key = OPENAI_API_KEY
```

```bash
OpenAI API Key: ········
```

## Veriyi İndirin (Download Data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Vektör Deposunun Yaratılması (Oluşturulması) ve İçinin Doldurulması (Populating)

Siz de dahi derhal/şimdi (now); belli ebatla/satırda birtakım dökümleri; doğrudan yerel / kendi eliniz (local file) konumunuzdaki adresten (Paul Graham imzasını taşıyan/yazılarından makale derlemlerini), sistem dahilinde / döküp (to load) Tencent Bulut - Cloud tabanlı/veritabanına ve formlu olan VectorDB içine sığdırıp (store them) bütünüyle buralarda da depolayacaksınız.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print(f"Toplam belge / evrak adedi (Total documents): {len(documents)}")
print(f"İlk belge, kimliği (id): {documents[0].doc_id}")
print(f"İlk belge, özeti - değer (hash): {documents[0].hash}")
print(
    f"İlk belge, metin kısmı ({len(documents[0].text)} karakterden (characters) müteşekkildir):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

```bash
Total documents: 1
İlk belge, id: 5b7489b6-0cca-4088-8f30-6de32d540fdf
İlk belge, hash: 4c702b4df575421e1d1af4b1fd50511b226e0c9863dbfffeccb8b689b8448f35
İlk belge, metin (75019 characters):
====================




What I Worked On


February 2021


Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined  ...
```

### Tencent Cloud VectorDB servisini ilklendirin / başlatın (Initialize)

Uygulamalı o vektör tabanlı veri platformu/deposu tahsis eyleminin başlatılıp (Creation entails); zemininde / altında / ardında yatıp barınacak (underlying) temel veritabanı klasman/koleksiyon derlemlerini de (collection) şayet/eğer ki evvelden ortamda halihazırda inşa edilip de bulunmuyorlar ise (does not exist yet) bunların bizzat sisteme entegrasyonuyla oluşmasını/kurulmasını elzemce / tam bir şart koşuluyla icap ettirir / beraberine/üstüne çeker.

```python
vector_store = TencentVectorDB(
    url="http://10.0.X.X",
    key="eC4bLRy2va******************************",
    collection_params=CollectionParams(dimension=1536, drop_exists=True),
)
```

Şimdiki varışta (Now); az önce / de var ettiğiniz / sahip olunan tam bu tabanı / depoyu da gelecekte yapacağımız çekme / yahut olan/gidecek sorgulara ("for later querying") hasrederek / hitap kılması ve muhafaza kılması için LlamaIndex evresinin formlarındaki o (kapsüllenip korunakla/sarılışıyla - abstraction) `index` bloğu / formu etrafı gibi de sarmalayın/kaplayın.

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Bu dökümlerde ki `from_documents` tetiklenmesinin (kod çağrımının) bir sefere kalmadan dahi dahi (at once) aslında da epey/birden ziyadedeki pek bir işi/eylemi ifa ettiğini aklederek de not alınız/yahut kaydediniz (Note that): Bu da sisteme zemin ile akan / dökülen tüm sunulu ve akışları dahil girdilerle evrak ve dosyaları / belgeleri; asgari yahut ideal çapta da üstünden kalkılacak/anlamına bürünen ve idare edilebilecek meblağdaki de kısımlarına / parçalı ebata parçalamakta/hisselere kesmektedir (chunks of manageable size), ve de keza ("nodes"  - düğümlere vb) de döküp; tüm parça başı yahut her "düğüm (node)" dahi bağlamından her birine tam yerleşkeli bir gömme (embedding) değerli vektörü işleyerek/hesap edip oluşturup (computes embedding vectors), ardından bu oluşturulanların (them all in the) tamamını/döküm tutarlarını Tencent Bulut platformu dahilindeki (Tencent Cloud VectorDB) yapısallığına depolamaktadır/kayda geçirir.

## Depoyu/veri alanını Sorgulama (Querying the store)

### Temel sorgulama (Basic querying)

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden yapay zeka alanında çalışmayı seçti? (Why did the author choose to work on AI?)")
print(response)
```

```bash
Yazar yapay zeka (AI) üzerinde ve tüm bu sahada çalışma ekseninde dökülen kararında; Mike adlı / tabirine evirilmiş bir zeki bilgisayar yahut tasarımla o sistem kurgusundan feyz alınan / The Moon is a Harsh Mistress adeta/adı geçmek suretiyle olan bir kurgulu bilim dökümü bir eserde (ve romanından da) ziyadesi ve epeyi büyüsüne / çekimine oldukça maruz kalmasından; ve bir de üzerine yapım platformlarından bir PBS sularındaki kanal belgesel yapısına çıkan ("SHRDLU") terimi kullanarak Terry Winograd'ın evrelerini dahi bir televizyon belgeselinden görmesinden/ve bununla perçinlenmesinden ilham etmiştir. Hem dahi yazar aslen kendisi diğer / ötekilerden yahut bir branş-saha yığınlarının asla yapamadığı-bulamadıklarına inandığı (other fields could not), o evrene özgü/olabilecek dev nihai/en temel hakikat/kuralları yahut safsata sanılışı aşmak - ("explore the ultimate truths") keşfine doğru (fırsat olarak dahi görerek) onu evrilen / kullanan AI formunun bir büyü dökümündeki esans/düşünsel tarafının (idea) de yapısını asıllarıyla / epey derinden benimseyerek bağlanmış/kapılarak dahi evrilmiştir (He was also drawn).
```

### MMR tabanlı sorgulamalar (MMR-based queries)

Maksimal marjinal (marginal) alaka / sınır düzeyini sağlayan form metodu (The MMR method); kendi büründüğü nezdinde o sorgu (the query)/sual atımına dahi evrildiği/işleme koymaya dek atılan safhada onlara elbette konu başlıklarıyla ne derecede ilgiyi uyandıran (relevant) formda metin ve kelamlar dizilimlerini depolardan bir şekilde arayıp/çekenken ("fetch text chunks"), bunların yanında o alınan evvel veyahutta diğer o yapı taşlarının / bölümlerinin/nitelik dökümlerinin kendi sahalarıyla ("as different as possible from each other") dahi de olabileceğinden olabildiğince / de yahut azami derecelere kadar oldukça uyumsuz ve de resmen birbirilerinden dahi tabiatlara varacak zıt / oldukça dahi farklı ve yabancı / çeşitli yapıda yer edinmesine dönük evresiyle harmanlanmasını (kurgulanmıştır/işte tasarım ve dahi mimarisi sırf da bu maksat - designed to - üzerinedir), bu vesilesi itibariyle yansıyan netice bağlamındaki son nihayet ve varılan mutlak olan ("the building of the final answer") o tekmil cevaba da dahi olan daha kapsam / da yahutta epey de daha yalpaze yapılı daha bol form / harman da "yine daha o bağlama da evrildiği resmen bollaştıran veyahutta geniş" tabanda bir yapı sunma (providing a broader context) ile o amacı hedeftir/hedefi izler.

```python
query_engine = index.as_query_engine(vector_store_query_mode="mmr")
response = query_engine.query("Yazar neden yapay zeka alanında çalışmayı seçti? (Why did the author choose to work on AI?)")
print(response)
```

```bash
Yazar yapay zeka (AI) dahi çalışmasında form dökümünü olanda / alandakileri kararını vermesindeki taban eylemi (çünkü); bizzat asıl mesai arkadaşlarının tabiatlarından (his friend) kendi eli ("who had built a computer kit") / kendileri inşa varıp ürettikleri cihaz evre formunda bir şeyine (veyahut) sistem / kit makinasındaki o yapısında ona ("type programs into it") içine yahut tüm programa atılarak yığın yapıp kod dizmesi evresine imrenmesi/hayran gıpta yapısıyla / saygısının ("he was impressed and envious of his friend") kıskançlıkla özenmesinden doğup / tetiklenir ("because"). Diğer yoldan ("He was also inspired/etkilenmiş"); o bahsi dahi gelen / kurgulu sistemde de Mike tasarı / ismindeki var sayıp nitelenen ("intelligent computer called Mike") epey de formca bilgisayarı evrene alan / veya bir kurgusal Heinlein yazıtı / evre eseri dahi the Moon is a Harsh Mistress adıyla sayılan yazar/yazıt eseri / formundan ve diğer (şurada - PBS) dökülen - belgesel (documentary) kanal safhasından Terry Winograd izlerini buluşmadan beslenmişti... O dahi okul yıllarındaki tahsillerden (college) gördüğü okullara / dahi bir felsefe bazındaki safha / süreç derlemiş dökümlü dersleri yapısına epey bir sönük yahut sıkıcı ("boring") dahi bularak hayal ve ümitlerinin çöküş ve noksan (disappointed) yapısını da kırıklık / kırılması evresine denk düştüğünden ötürü eylemdeki arayışı daima hep de de ondan bir üste daha azamet ("seemed more powerful") duracak ve barındıran yahut asgari saflarda bir suların evreye varma niyeti (he wanted to work on) ekseninden çıkıyordu/arıyordu...
```

## Var olan (halihazırdaki mevcut) bir depoya bağlantı kurma (Connecting to an existing store)

Bu kullanılan dökümün (bu deponun - Since this store), aslen bizzat da "Tencent Cloud VectorDB" uzantısı dahi silsileyle desteğine entegre edildiğiyle bağlantıda olmasından aslı sebeple kalıcı (persist/ısrarcı) ve kalıtsallık teşkil (is persistent by definition - tanımı / esası gereğinden) ile vardır. Tabiatının / Öyle ki varlığına ("So, if you want to"), o sebeple / dolayısıyla biz de ön evre dökümlerde de yahut da evvel de ("populated previously") döküm sağlayan / veya da ihdas oluşturulup dökümü o taban (ve platformlarıyla/bağlantı sağlayan var (oradan - existing store)) tabiatlara atfedilerek çekip yahutta bağlanmak dilenirseniz (connect to a store / orayı referansa alırsınız dahi demek gerek de evre), bizzat yol yordamı / şekli ve de şemali buradadır (here is how):

```python
new_vector_store = TencentVectorDB(
    url="http://10.0.X.X",
    key="eC4bLRy2va******************************",
    collection_params=CollectionParams(dimension=1536, drop_exists=False),
)


# İndeksi/dizini formlayın / oluşturup var edin (önceden - daha evvelinde sisteme barınan indeksin de vektör kayıt evresindeki / hafızadaki kalıntısına/yahut taştan "from preexisting stored vectors")
new_index_instance = VectorStoreIndex.from_vector_store(
    vector_store=new_vector_store
)


# işte cidden yapınız / tüm her bir işlem dahi de tabanımız (now you can do querying, etc:) sorgu - sual (işine girişiniz filan ve türevi vb. evlatlarını döküverip/yapınız da edebilirsiniz arık):
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query(
    "Yazar yapay zeka alanında çalışmaya başlamadan (AI) önce neler okudu/çalıştı? (What did the author study prior to working on AI?)"
)
```

```python
print(response)
```

```bash
Yazar AI dökümüne iş yapmaya ve / veya girmesine de dahi uzanmasına dahi o eyleme evresi basmadan evveliyatında epeyce resimleme sanatı ("painting") ve / diğer (ve de "felsefe" gibi konular) nezdinde de eğitim almış/özenmiş ("studied philosophy"), keza aslen bilinen spam süzeçlemeleri / formlarına taban (worked on spam filters / spam temizleme-filtre dökümüyle vs) işleyişi ile vaktinde harcayıp yanına kalıptan eylemler/yazılarına (ve makalelerle karayalar - wrote essays) de yönelmiştir yazardır.
```

## Belgeleri İndeksten / Dizinden Silmek ve Kaldırmak (Removing documents from the index)

Öncelikle ve en başta evreli/doğrudan sistemden olan bir evrak ile ("list of pieces of a document") parça parça bağlamlarını, ya da nesnel (nodes) evreleriyle bir dizinin kendisinden/o evrenden oluşturulan (spawned from) ve asıllarından kopuk ya doğan döküm de (from a `Retriever`) "O Geri Çağrım/Çekme (Retriever) motor mekanizması eylem yapısından da" bariz net ve açık/isabet bir format dökümüyle tüm olan dizisini liste/yığılı elde kılıp alarak verin/çağırın (get an explicit list of):

```python
retriever = new_index_instance.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=3,
    vector_store_kwargs={"mmr_prefetch_factor": 4},
)
nodes_with_scores = retriever.retrieve(
    "Yazar yapay zeka alanında çalışmaya başlamadan önce ne üzerine çalıştı / çalışıyordu?"
)
```

```python
print(f"Bünyede halihazırda bulunan (bulunan/eşleşen-Found) {len(nodes_with_scores)} adet node dökümünden / düğümden.")
for idx, node_with_score in enumerate(nodes_with_scores):
    print(f"    [{idx}] puan/değer (score) = {node_with_score.score}")
    print(f"        kimlik (id)    = {node_with_score.node.node_id}")
    print(f"        metin (text)  = {node_with_score.node.text[:90]} ...")
```

```bash
Found 3 nodes (Tahmini 3 tane node (düğüm) elde-çıktı.).
    [0] score = 0.42589144520149874
        id    = 05f53f06-9905-461a-bc6d-fa4817e5a776
        text  = Ne üzerinde/hangisi adına vs Uğraştığım (Mesai Döktüm/What I Worked On)


Şubat 2021


Koleje /yahut lise ya asıl o lisans eğitim kampüslerine ve tahsil evresine uzanmazdan bizzat önceki lise öncesinde vs... benim uğraşı verdiğim/gayret döküp de uğraştığım evre ile ...
    [1] score = -0.0012061281453193962
        id    = 2f9f843e-6495-4646-a03d-4b844ff7c1ab
        text  = epey de işlendiği - keşfedilene kadar ("been explored"). Gelgelelim ne yapsam ki aslında / cidden dahi de cidden o andaki en elzem dilek ve "tüm arzum/yahut " (Ancak benim bir tek aradığım da = "But all I wanted was") - cidden "to get out of grad school / o lisansta doktora ve lisansüstü döküm/teşkilinin ve evrim okulundan uzaklaşıp da evreyle sıvışmaktandı/kaçarak kopabilmemdi..." - , bir diğer yönden akabinde bana çırpı-yazı veya hararet ve çok daralan ("and my rapidly written diss.../tez vs")...
    [2] score = 0.025454533089838027
        id    = 28ad32da-25f9-4aaa-8487-88390ec13348
        text  = Terry Winograd form / belgeselin yapısında (Gösterimi ile) SHRDLU (yapı - dil/model yapısı) yazılımlarıyla beraber (using SHRDLU...). "Asla şunları demeliyim denemeyi cidden ne niyet / asıl teşebbüs dahi ("I haven't tried rereading") tekrar alıp o dökümü / yahut o The Moon is a Harsh Mistress yazıtlı evreyi ("The Moon is a Harsh Mistress / Ay Zahmetli-Gaddar bir Metrestir") tekrar devrederek tekrar el atıp da ...
```

Ama bilhassa da bekleyin! (But wait!). Vektörel veri depolamanıza asıl form / bazından dahi o kullanımda referans sağladığında, tabiat formuna o makul / uygun/silinmeye elzem gelen de de o silinme ölçütü/"birim (unit)" teşkilinde olanın (o anki tek bir düğüm dökümlerini atfedilip/odak almadan) hiçbir birleşik (birlikte yer alan nevi düğüme/yapıya bağlı olmamasından - "belonging to it", ve bireysel odak = individual node); aslında topyekun formuyla kendisi "bir koca/ana metin **belge (document)** formunu dahi ("consider the document as") hesaba çekmeniz de tavsiye formlarından en uygun / öte elzem tablolardandır. Peki formda da böyleyken (Well, in this case), siz halihazırda bizzat bir adet dümdüz (sade/tek bir text/metin bazlı file döküm dosyası / veri içeriğinden ibaret de "single text file" eklentisini / içeri aktarımı var etmiş olduğunuzdan mütevellit - you just inserted), buradaki tüm o aradaki yapın taban düğümlerinin hep evrede aynısına/fark formlarıyla ("all nodes will have the same") ve şu referansla tekeş (aynı/çiftsiz kalarak - `ref_doc_id`: belgenin ana adres kimlik niteleyicisi gibi) uzanır dökümden de bir yansıyışı bulunacağı kesindir / alabilecektir de:

```python
print("Düğümlere dönük `ref_doc_id` referans ID evrak değeri (Nodes' ref_doc_id):")
print("\n".join([nws.node.ref_doc_id for nws in nodes_with_scores]))
```

```bash
Nodes' ref_doc_id:
5b7489b6-0cca-4088-8f30-6de32d540fdf
5b7489b6-0cca-4088-8f30-6de32d540fdf
5b7489b6-0cca-4088-8f30-6de32d540fdf
```

De ki misalen (Now let’s say); o sisteme sunduğunuz (kaldırıp/çıkarmanızın vacip duruma girdiği "you need to remove the text file you uploaded") eklenti dosyasını da kaldırmak zaruretinden doğup evreli geldi eyleme:

```python
new_vector_store.delete(nodes_with_scores[0].node.ref_doc_id)
```

Nihayet bizzat (tam tıpa tıp resmen dahi) aynı sorguyu (the very same query) alın tekerrür halinde yine bir tur yineleyin ve bu denli şuan tam/net çıktılara / ve o veriye de dahi sonuca bir göz gezdirerek de yığınları asıl şimdi inceleyin. Karşılığında / taban bulgusunda resmen ("You should see *no results* being found:") *hiçbir verisel neticenin* ve yahut kalıntı dahi döküm bulgusu bulunmayarak dahi boş gelmiş bulunduğunu / yahut görebildiğinizi anlayabiliyor dahi olmanız dahi zaruridir (düşünülür ve görülmeli dahi eylem gelir):

```python
nodes_with_scores = retriever.retrieve(
    "Yazar yapay zeka alanında çalışmaya başlamadan önce ne okudu / çalıştı?"
)


print(f"Toplamda yahut döküme sığan ("Found {len(nodes_with_scores)} nodes") adet nesne/node (düğüm) dökümdedir/çıktıdır/düşmüştür.")
```

```bash
0 (Sıfır) adet / hiçbiri olmak kaydı ile 0 nesne/düğüm eşleşmiştir. (Found 0 nodes.)
```

## Meta veri formlarla Süzeçleme / Filtreleme (Metadata filtering)

Tencent Cloud Formunda var olan VectorDB deposu dahi; öz yapısında atılan / yahut eşleşmeye dair bir döküm araması/yapı sorgusu icra eylem sularında / bir eşleşme de ("at query time") resmen tam/nokta vuruşlukla uyum teşkil edesice "eşit/kesin uyan eşleşmeli - exact-match" olan tabandaki `key=value (anahtar-değer)` yapılarını deklareli olarak süzeçten dahi işleyip ayıklatarak (metadata filtering) meta veri süzmesine dönük olanlarına izin tabanlı tüm bir destek teşkil ederek de destek kordili barındırır. Sonrasından giden takip tabiatlı - bir kurguya sıfırdan/tertemiz yeni ("brand new collection") doğmuş o form klasmanıyla çalışabilir, ve keza bu işlevi bu vasfı (kabiliyetin tüm hatlarını) size barizlikle sergileyerek gösterir (demonstrate this feature) aşağıdaki metin yapılarına tekabül hücre/koduyla olan dizeler.

Söz konusu demo dökümünde de / bu gösterimden, vakitten feragat yahut evreli sadeliğin barınması namından sadece "bütünlük kalsın kurgusuyla o zaman/ihtiyaç yahut (sake of brevity - olabiledikçe kısaliğı için);" doğrudan/bizzat yegane teşkil - birey tabanda sadece tek kalıplı bir/el evraklı form dahi olan belge ana (kaynak evrak) formata (is loaded) referans sunulmasına da (yani the `../data/paul_graham/paul_graham_essay.txt` evraku dökümünde text-metnine vs) yüklettirilir de alınır. Bunun da elbet yanından kalmaksızın formda (Nevertheless) ve yapıda "bir takım meta veriye has ve kendi elyafça o formdan yansıtmalı bazı özel-uyarlamış meta değerleri ("attach some custom metadata to the document") evraka has (bu de tekmilde / o şarta dair de evlere has kilit yahutta o evraka dayalı / dahi iliştirilen verilerine olan o limit koşulları da o sorgu/dökümlerine ne yönle var edip kısıt (restrict) getirmesini yapabildiğinizi / evreli - yapabileceğinizi canlandırarak canla o tabirle bir size izaha kurgulamalı olarak göstereceğiz...

```python
filter_fields = [
    FilterField(name="source_type - kaynak_tipi (veyahut cinsi vb)"),
]


md_storage_context = StorageContext.from_defaults(
    vector_store=TencentVectorDB(
        url="http://10.0.X.X",
        key="eC4bLRy2va******************************",
        collection_params=CollectionParams(
            dimension=1536, drop_exists=True, filter_fields=filter_fields
        ),
    )
)




def my_file_metadata(file_name: str):
    """Giren/tahmini gelen form dosyanın ve döküm verisi adından eyleme / o içeriğe matuf bağıl uyumla / ya da oradaki şekli suretiyle ismine vesil (Depending on the input file name), başka/ayrı dökümden/özünden evre meta veri formül ve kimliğini eşleştirin (associate a different metadata)."""
    if "essay - (deneme-makale gibi sözcüğün evre ismi geçerse şayet vb)" in file_name:
        source_type = "essay - makale/deneme"
    elif "dinosaur - dinozor vb (yahut büründüğü ne tip/isimde tabir vb dökümü)" in file_name:
        # her ne ki (this - bu) elbette elzem tezatları ve keza talihinde aksi ile/ maalesef o hüsran (veya maalesef - unfortunately) yahutta tüm buradaki demo - ön sunum deneme işleyişinin bu turundan gerçekleşmeyerek de oluşmaz (de karşısına vs. (will not happen in this demo vb))
        source_type = "dinos - (dinazor gibi döküp ona değer vb ekli hali gibi vb)"
    else:
        source_type = "other - farkli/diger_farkli verili cidden baska (yahut bir digeri form vb)"
    return {"source_type (kaynagin tipi - degeri ve bizzat formu vs)": source_type}




# Belgeleri doğrudan çek at içeri ve döküm sistemi formuna yükle (Load documents) ve index dizinini vb de inşa (build) edip şekil kur ("and build index")
md_documents = SimpleDirectoryReader(
    "../data/paul_graham", file_metadata=my_file_metadata
).load_data()
md_index = VectorStoreIndex.from_documents(
    md_documents, storage_context=md_storage_context
)
```

Tümü bitip asıl evre bu tamlık / evredir ("That’s it"): Şu dakika andan ("you can now") / itibaren ve formunuzu bütüne yaymaya ("add filtering to your query engine"), kendi bu o/o evre makinasına ait/evresine ve de o sorgu sistem-tabiatınıza yahutta da olan o "sorgu motorunuza dahi filtre süzmek evresini de ("add filtering") rahat evresiyle dahi ilave eylemine ("you can now add") rahatça / edip (de katıp) yapabilirsiniz (dahi alabiliyorsunuz):

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
```

```python
md_query_engine = md_index.as_query_engine(
    filters=MetadataFilters(
        filters=[ExactMatchFilter(key="source_type", value="essay (makale veya deneme evreli vs)")]
    )
)
md_response = md_query_engine.query(
    "Yazarın tez evrakını / yahut bizzat o tezinin ("his thesis") de bir fiil tam bitiş sureti ("How long it took") veya yazımı tez döküm formunu da tamamlaması (yazmasına varımı / to write his thesis) kendi nezdinde dahi evreli ve yahut toplamında dahi olarak ne sürece / tabiana vs olarak cidden ona (it took the author) cidden de ne kadarlık bir periyodik - zaman dahi zarfına/ne kadarlık fiyata veya zaman meblağı olarak (ne kadar sürdü = how long it took) mal olup ne kadar evreyle sürdü/aldı etti? (How long it took the author to write his thesis?)"
)
print(md_response.response)
```

```bash
Yazar'ın bizzat kendisine / kendi hanesi (kendi tezi olarak büründüğü) ve var ettiği tezini o şekli tabiatından / tezini de tamamlaması dahi (yazması = write his thesis) toplam yahut yığındaki formda ("It took the author") yazara tamı tamına beş ('five') asgari yahut o hafta/hafalık bir periyotla beş ("It took the author five weeks") ayrı 5 haftalık (hafta dahi) gibi bir süresine dahi mâl olup alım/veya süresini buldu yahut o kadar bürünüp kadar epey aldı/sürdü ("took").
```

O süzgecin/veya fitrenin yahut mekanizmada taban evrenden de bir işlevde dahi bizzat devreden / dönen rol almasından dahi cengaver formuna sinesini dayayan çalışılışı veyahutta ("filtering is at play - filitre-süzgecin de bizzat oyunda yer veya bizzat o devrede, işlevdeki - çalışır formda / oyunda/ devrede olduğunu vs" ) sınamak - yahut o döküm de formunu ("To test") denemek yeltenmesi namına ("try to change it to use only"); filtre / o kullanım tabanlı olarak onu "sadece ve bizzat yegâne olarak `"dinos" / (o dinozor vari kelamdakilerden vs dökümde form) `" var edilmiş uzantı/kıstaslı belgeleri vb (documents) arayadurmasına / de "değiştirmeye de/ayarlamaya - dahi bu uğraşa eliniz ile denemeden de bir teşebbüs edin..."... (there will be no answer this time :)). Meraklanmayın elbet, hiç aslen dökümlerinde veya bu ("this time") tur defa veyhut döküm serisinde kati suretiyle zerre hiç cevap form evreyle (olmayacaktır / veya hiçbir yahutta tek kelimeyle evren - dahi döküm hiçbir surette cevap yok - no answer - formuna / yahutta hiç netice olmayacaktır vb: tabirince olacaktır elbet :)).
