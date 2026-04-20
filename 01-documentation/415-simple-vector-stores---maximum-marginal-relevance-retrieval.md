---
title: Basit Vektör Depoları - Maksimum Marjinal Alaka Düzeyi Alımı (Maximum Marginal Relevance Retrieval)
 | LlamaIndex OSS Belgeleri
---

# Basit Vektör Depoları - Maksimum Marjinal Alaka Düzeyi (Maximum Marginal Relevance) Çıkarımı / Getirimi

Bu not defteri (notebook), ağırlıklı olarak MMR (sıralama algoritması) verilerinin sistemden çıkarılması / geri çağrılması (retrieval) kullanımını inceler \[[1](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf)]. Maksimum marjinal (marginal) alaka düzeyi (relevance) kullanılarak, önceki sonuçlara benzemeyen belgeler yinelemeli (iteratively) olarak bulunabilir. Bunun LLM geri çağırmaları / getirimleri için performansı artırdığı gösterilmiştir \[[2](https://arxiv.org/pdf/2211.13892.pdf)].

Maksimum marjinal alaka düzeyi algoritması şu şekildedir: $$ \text{{MMR}} = \arg\max\_{d\_i \in D \setminus R} \[ \lambda \cdot Sim\_1(d\_i, q) - (1 - \lambda) \cdot \max\_{d\_j \in R} Sim\_2(d\_i, d\_j) ] $$

Burada D mevcut tüm aday belgelerin kümesini (setini), R halihazırda (zaten) seçilmiş olan belgelerin kümesini, q ise atılan sorguyu, $Sim\_1$ bir belge ile atılan sorgunun arasındaki benzerlik işlevini (fonksiyonunu) ve nihayetinde $Sim\_2$ ise iki belgenin kendi aralarındaki benzerlik işlevini (similarity function) temsil eder. Yukarıdaki denklemde yazılı $d\_i$ ve $d\_j$ de sırasıyla (ve uyumlu bir paralellikle) D ile R kümelerindeki belgelere karşılık gelmektedir.

λ parametresi (mmr\_threshold - mmr eşiği), bu ikilinin alaka düzeyi (ilk terim/first term) ile çeşitliliği (ikinci terim/second term) arasındaki dengeyi (bölünmeyi - trade-off) kontrol eder. Eğer mmr\_threshold (mmr eşiği) bir oran olan 1'e yaklaşırsa (yakınsa), alaka düzeyi üzerine daha çok vurgu ve önem düşer; öte yandan, şayet mmr\_threshold değeri sıfıra (0) yanaşırsa / yakınsa bu doğrultuda çeşitlilik (diversity) daha fazla vurgu ve ehemmiyet kazanır.

Veriyi İndirin

```bash
%pip install llama-index-embeddings-openai
%pip install llama-index-llms-openai
```

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

```python
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
```

llama\_index/docs/examples/data/paul\_graham

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
index = VectorStoreIndex.from_documents(documents)


# mmr arayüzünü / verisini kullanmak maksadıyla, onu bir vector_store_query_mode olarak atamak/ayarlamak icap eder
query_engine = index.as_query_engine(vector_store_query_mode="mmr")
response = query_engine.query("Yazar büyürken neler yaptı?")
print(response)
```

```bash
Yazar yazmaya kısa birer hikaye ile adım atarak / kaleme alarak, kendisini programlama üzerinde kurguladı (ve bu sahada emek verdi; spesifik örnek vermek gerekirse 9. sınıfta yer alan bir IBM 1401 cihazında).
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
index = VectorStoreIndex.from_documents(documents)


# eşiği (threshold) ayarlamak için, onu vector_store_kwargs içinde ayarlamalısınız
query_engine_with_threshold = index.as_query_engine(
    vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.2}
)


response = query_engine_with_threshold.query(
    "Yazar büyürken neler yaptı?"
)
print(response)
```

```bash
Yazar yazmaya kısa birer hikaye ile adım atarak / kaleme alarak, kendisini programlama üzerinde kurguladı (ve bu sahada emek verdi; spesifik örnek vermek gerekirse 9. sınıfta yer alan bir IBM 1401 cihazında). Sonrasında eline bir TRS-80 olan mikrobilgisayar yapısı geçtiğinde, birtakım kelime işlemcilerine ve en basitinden yazılımsal oyun tasarımlarına ufaktan varana kadar çok daha ileri/geniş çapta (daha etken şekilde - extensively) program ve kod yazmaya start verdi.
```

Düğüm (node) puanınının/değerinin (score) bir eşikle (the threshold) ölçekleneceğini ve bir de ek bedel / işlem olarak kendisinden evvel gelen düğümlerle olan benzerliğinden sebeple o düğümlere nispetle cezalandırılacağını (penalized) göz önünde bulundurun (not edin). Eşik meblağı oran bağlamında 1'e ulaştıkça; puanlar / dökümler salt haliyle eşit seviyede bir şekle (equal) dönüşür ve kendisinden önceki düğümlere mevcut benzerliği tamamen rafa kaldırılıp, MMR verisinin tüm tesir mekanizması kapatılarak yok sayılır (ignored). Nihayetinde eşik değerinin seviyesi dibi zorlarsa ya da (the threshold) taban skalasına / oransallığına doğru düşürüldükçe, söz konusu kodlama mantığının yapı taşı olarak işlem görecek algoritma, o noktada birbirinden ayrı olan ve olabildiğince çeşitliliği yakalayan evrakları (more diverse documents) döküme almak adına daha öncelikli ve gözde değerlendirir (will prefer).

```python
index1 = VectorStoreIndex.from_documents(documents)
query_engine_no_mrr = index1.as_query_engine()
response_no_mmr = query_engine_no_mrr.query(
    "Yazar büyürken neler yaptı?"
)


index2 = VectorStoreIndex.from_documents(documents)
query_engine_with_high_threshold = index2.as_query_engine(
    vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.8}
)
response_low_threshold = query_engine_with_high_threshold.query(
    "Yazar büyürken neler yaptı?"
)


index3 = VectorStoreIndex.from_documents(documents)
query_engine_with_low_threshold = index3.as_query_engine(
    vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.2}
)
response_high_threshold = query_engine_with_low_threshold.query(
    "Yazar büyürken neler yaptı?"
)


print(
    "MMR'siz Puanlar (Scores without MMR) ",
    [node.score for node in response_no_mmr.source_nodes],
)
print(
    "MMR'li ve 0,8 (0.8) eşik seviyesinde olan (threshold of 0.8) Puanlar",
    [node.score for node in response_high_threshold.source_nodes],
)
print(
    "MMR'li ve 0,2 (0.2) eşik seviyesinde olan (threshold of 0.2) Puanlar",
    [node.score for node in response_low_threshold.source_nodes],
)
```

```bash
MMR'siz Puanlar (Scores without MMR)  [0.38770109812709, 0.38159007522004046]
MMR'li ve 0,8 eşikli Puanlar  [0.07754021962541802, -0.31606868760500917]
MMR'li ve 0,2 eşikli Puanlar  [0.31016236260600616, 0.1845257045929435]
```

## Sadece Geri Çağırma/Getirme Gösterisi (Retrieval-Only Demonstration)

Yalnız küçük çaplı dilimleri/parçaları işlenebilir ebattayken dikkate alıp parça boyutu (chunk size) olarak işaretleyip atama yaparak (ve "mmr\_threshold" parametre argümanını özüne dönük kendi seviyesinden ayarlayarak (adjusting), getirilen neticedeki geri dönüş verilerinin / sonuç dökümlerinin kendi iç yapısında; ziyadesiyle birbirinden farksız (düşük çeşitlilik / less diverse) ve asit olandan (çok ilgili olan veriden) taa uzak seviyeli / birbirinden hayli kopuk (daha çeşitli/ çok ayrışık / very diverse) duruma nasıl dönüştüğüne / meyledip kaydığına rahatlıkla şahitlik yapabiliriz / inceleyebiliriz.

Şimdi şu değerlerle birlikte deneme yapabiliriz: 0.1, 0.5, 0.8, 1.0

llama\_index/docs/examples/data/paul\_graham

```python
documents = SimpleDirectoryReader("../data/paul_graham/").load_data()
index = VectorStoreIndex.from_documents(
    documents,
)
```

```python
retriever = index.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=3,
    vector_store_kwargs={"mmr_threshold": 0.1},
)
nodes = retriever.retrieve(
    "Yazar Y Combinator'da geçirdiği dönemde (during his time) neler yaptı?"
)
```

```python
from llama_index.core.response.notebook_utils import display_source_node


for n in nodes:
    display_source_node(n, source_length=1000)
```

**Düğüm Kimliği (Node ID):** 72313b35-f0dc-4abb-919c-a440aebf0398\
**Benzerlik (Similarity):** 0.05985031885642464\
**Metin (Text):** Akşam yemeğinden döndükten sonra / ayrıldıktan sonra Jessica'yla beraber bir taraftan yürürken (11 Mart gününde); Walker sokakları ile Garden yapılarının da bitiştiği köşe dahi derken bu üç bağ bir köşede kilitlendi. Daha akıllarında bir nihayete varamayan (fikirlerini bulup o akla yatıramayan) VC'lerin de (Sermayedarlar) ben ne diyeyim... Biz sadece ikimiz kendi fona sahip melek yatırım (fön / para akışı) bünyemizi ihdas edecek ve her şeyi tam da bizim önceden tartışarak o harmanladığımız fikirleri hayata taşıyarak tatbik edip faaliyete koyacağız. Finansman kısmını bizzat kendim tedarik ederken, eşim / sevgilim / eşim diyebileceğim (Jessica) kendi ana mesaisi olduğu / dahilinde o işten tüm bağı koparırken sırf varışımız dahilindeki bu hedef adına mesai (work for it) yapabilecekti; keza Trevor  ve üstüne dahi o da yetmez deyip Robert i dahi projede ortak hanesine (as partners) kaydedecektik. \[13]

Nasıl daha öncelerin aksini savunmuyorsam, bu sefer binde bir lakin cidden (defalarca olduğu kez üzere bir defa daha) cahillik tam tabiriyle yine hep bizlerin ve benim / de lehimize işledi. Basbayağı bir kuruş dahi olsa Melek Fon Yatırımcısının tam bağlamında ne olduğuna dair bile zerrece bir malumat bağlamında ön görümüz var olmadığı bir durumda / süreç dahilindeyken; bir de üstüne 2005 gibi bir tarihte (Boston'da) feyz alıp danışarak / ders öğrenecek tek model Ron Conway benzeri karakterlerin eksikliği de bir muammaydı... Bizler de tek eylem olarak aslında mantığın (the obvious choices) bizi aklın ve selimin emrettiği o tek akış yönünde sürüklenmesiyle karar verdik ve icrada kıldığımız şeylerin çoğu bilindik olmasına rağmense (turned out to be novel) bir o kadar yepyeni / ilk oldu.

Y Combinator'da (oluşumunda / bağlam yapısı dahi demeliyiz) yapboz tablosunu sarmalayan binlerce dahi farklı birden ziyade fazla parça bulunduğundan da tüm unsurları aslında dahi (birden bir günde de tamamıyla) çözmüş bir noktada hiç durmadık. Bizim en asgari tabanda kavradığımız evreyi anlatan en doğru (çözdüğümüz kısım); "melek yatırımcılık (angel firm)" statüsü tablosuydu. Elbet de geçmiş o tarihte ("melek fonlama" söz öbeğini kastetmesi suretiyle), o tarz kelimeler kolaylarına uyuşmaz ve bir çatı altında geçmezlerdi. İçlerinde yatırımlara karar verip adım atmak icap edince ona yönelen memurlarını ("people whose job it was" - görevi olanları), yani kurumsal şirketin uzantıları (milyon dolarlık iş) yapan dahi VC oluşumları vardı...

**Düğüm Kimliği (Node ID):** d18deb5b-7d2a-4d3d-a30f-a180a1cb7015\
**Benzerlik (Similarity):** -0.38235343418846846\
**Metin (Text):** Yüksek lisanstan dahi okul serüveni itibariyle atılmayı hiç beklememiş ve istemez olsam da, dışarı çıkmayı da kafaya da eylesem ben kendi içimde başka türlü de bu yaka paçayı kendim den de kurtaramaz mıydım ("how else was I going to get out?"). 1988 tarihi internet solucanını ("internet worm of 1988") eyleme alıp yazması evresi sonrası Robert Morris adlı arkadaşım an gelir ki Cornell'den ihraç edildi... Ondan böyle yüksek lisans eğitiminden dahi resmen tecrit olunmasına bile, hem hayret içinde bir bakış atıp (envious - gıpta edip) hem debu böylesine sansasyonel ("such a spectacular way") yola bulduğu çare evresine dahi cidden / resmen acayip özenmiş / gıpta ile saygı ile hislere dahi şaşırarak da gıptalar eylemiştim.

Nitekim sonrasında, bir 1990 yılı Nisan aylarının dahi bir vaktinde gelindiği esnada tablolarda ve duvar yüzeyinde de bir yarık, çatlak vuku buldu. Bay profesör isim olarak / bizzat yüz yüze dahi Cheatham'a denk gelmem ve tam bu Haziran da bir mezuniyete erebileceğime ve kendimi de bizzat dahi bir taze kan olarak o dilden hazır sanarak olup / bitirdiğime ikna eden ("if I was far enough along to graduate that June") bu bir cüret var mı sordu. Tam bu aşamada doktora tez dökümünden dahi ne bir heceyi kalem dahi almamama ("I didn’t have a word of my dissertation written") / yahut etmeme dahi karşın; hayatım süresince aldığım net ("in what must have been the quickest bit of thinking") bir tavra sarılırcasına da sadece birkaç söz ile beşimsi o haftaya yaklaşılan sürelere kalan dilimde; şunda bir deneme dahi eylemekteyim diyerek adımları / On Lisp taraflarından kendimi referans koca koca kalıntılara da atarcasına bir hece etmeksizin saniyesine (yalanla bile dahi - with no perceptible delay; tereddütsüz diyelim) hiç yalan edasına bile bulaştırmadan dahi "Elbette öyle ki ("Yes, I think so."), inşallah bunu sana okutturup günlere atıfta da takdim eyleyeceğim" kelamını diyerek karşısına dizilircesine dahi cesaretimi ortaya sürmüştüm.

Konu mahiyetine yönelik süreklilik / aktarım tabiatlı / dökümlerde dahi dahi (applications of continuations as the topic) seçimler / kararlar kıldım. Ne bir şekilde işlenebileceği ve tam neleri eskitmesine rağmen mazi yapısıyla geriler / ve gerisinde ("In retrospect") tamı tamına yatan "makrolara ve yerleşik dil sistematiği ve yapısallığına" dokunan (embedded languages) verilerde durdum... Sene o sene olsa dahi aslında ("There’s a whole world there that’s barely been explored.") zarla zorla el atılan koskocamanca el bile edilmemiş devasa bir yığın evren / veyahut tabiat yatıyordu geride... Lakin her şey dahilinde, istediğim olan neydi vs...

**Düğüm Kimliği (Node ID):** 13c6f611-ac9f-47af-b76d-7e40ea16f7ed\
**Benzerlik (Similarity):** -0.3384054315291212\
**Metin (Text):** \[18] YC'yi (mercii, yapıyı de) terk ve nihayet bırakmaktan ötürü dahi gelmiş olan / bana da ağır tek binen kötülük ("worst thing"); Jessica ile asla ve kat'iyen artık (etrafta mesaisi dahi olmayışını) mesai geçiremeyip, yanımda dahi iş arkadaşlığından (not working with Jessica anymore) dahi o izlerin gidişi dahi idi. Zaten genel evresine ve taban tablolarına dahi ilk temas ettiğimiz dönemlerden tüm geçen tam süreçler bir bakıma YC serüveninde geçtiğinden / tüm her şey neredeyse ("We’d been working on YC almost the whole time we’d known each other") iç içe omuz omuzaya dahil de geçtiğinden dolayı ne eylem ile ve nede meslek ve ev yaşantısını (ne niyet ne teşebbüs etmemiş ("neither tried nor wanted to separate it from our personal lives" - "kişisel ya da yaşamdan ayırmaya uğraşmadığımız dahi gibi") eylem dahi niyet kalmadı; keza bu "ayrılığa gitmek de cidden resmen ("leaving was like pulling up a deeply rooted tree" - "kökü derin ve dibe dalan ulu ağacın kök sökümüne benzettiğini de" ) acısına eşdeğer kalıcı bir his tabanı bırakmasına olanak verdi.

\[19] Nitekim bir durumdan ve olguntan "kavram ve verinin (concept) 'İcat / Tasarım - Invented vs Discovered / Buluş' kıyasına evrildiği noktaya (hassasiyetteki)" dahi cidden biraz ("Way to get more precise") incelik tabiatında eğilindiğinde ve ehemmiyet de atfettirilen ilk baş yapı argümanları vs uzay formlarıyla (uzaylılarla - space aliens) bir muhabbete ve sohbete denk getirmeye benzetiş yapmak icap ettirebilir. Düzeyi her ne denli asgariden bir kademe üst safha/evrelilige tekabül eden ("Any sufficiently advanced alien civilization") medeniyet veya o uzay mensubu türler (aliens); mesela bir defasında Pythagoras (Pisagor Teoreminin dahi olan evrensel ("certainly know about the Pythagorean theorem")) buluşunu mutlak olarak tüm kurallarıyla ("certainly know") sularında dahi avuçlarına geçirmiş farz edilirler fena olmaz... Bense "Eminim, ne kadar biraz kuşku barındırsa (kesinlik taşımamasa = with less certainty) dahi ben McCarthy'in o meşhur kalıntı dökümlerine ("the Lisp in McCarthy’s 1960 paper"), taa 1960 yılına giden tezine ve yazıtındaki dahi form / dil Lisp format tabloları dil / yapı da vs hepsinin aşina dahi olduğuna inanırım." demeliyim/inancım bu minval...

Süreci bu dahi kılan ise; onlara da sadece bu form dil tablolarından ziyade, kendi yapılarında da olan kelime uzantılı ("the limit of the language that might be known to them") / nelerin malum dahi olduğunun aslında bir nebze neye atıfta evrilerek sadece bu kadarına dahi neden vakıf olacak / bilinecek denmesinin ("no reason to suppose") makule tabanda / aklı melekede (göstermeye mahal) veya ne akla uygun ki farz ve zannını dahi etmemize dahi asla olanak bırakmayacağı ve mahal kılmayacağı evreninde (bilişine sınır - limit getirmemesindeki yatanı)... Kaldı ki asıl manada ("Presumably aliens need numbers and errors and I/O too.") / Onlara sayılara ve o verisel işleyişe dair olan form yapılardaki girdilere dahi (input/output) - hatasına dahi vs tüm her şeye de gerekliliği ve ihtiyaçlılığı da bilindik bir kurgu formuydu zaten... Hâl böyle kalsa gerek ki ("So it seems likely there exists at least one path out of McCarthy’s Lisp along which discoveredness is preserved.") tamı tamına o McCarthy dökümündeki / veri yazısındaki "aslın bulgusu ve kalıcılığı (süregelenden aktarılıp günümüze de bozulmayan - the discoveredness is preserved") tabanından dahi bir iz yapılı/patikalı (at least one path) dilin veya o yol evresinin en asgaride olduğu ve de kalıtsal / korunduğu yönünde muhtemel kuvvet dökümleri bir nevi duruyordur / var olur dahi ("it seems likely")...

Yine ve yeniden teşekkürler ("Thanks to"): Trevor Blackwell efendiye, dahi John Collison beye, sonra Patrick Collison ile yine Daniel Gackle ile, keza Ralph Hazell ve de Jessica Livingston da / yanısıra en nihai (Robert Mor...) ile...

```python
retriever = index.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=3,
    vector_store_kwargs={"mmr_threshold": 0.5},
)
nodes = retriever.retrieve(
    "Yazar Y Combinator'da geçirdiği dönemde neler yaptı?"
)
```

```python
for n in nodes:
    display_source_node(n, source_length=1000)
```

**Düğüm Kimliği (Node ID):** 72313b35-f0dc-4abb-919c-a440aebf0398\
**Benzerlik (Similarity):** 0.29925159428212317\
**Metin (Text):** Akşam yemeğinden döndükten sonra / ayrıldıktan sonra Jessica'yla beraber bir taraftan yürürken (11 Mart gününde); Walker sokakları ile Garden yapılarının da bitiştiği köşe dahi derken bu üç bağ bir köşede kilitlendi. Daha akıllarında bir nihayete varamayan (fikirlerini bulup o akla yatıramayan) VC'lerin de (Sermayedarlar) ben ne diyeyim... Biz sadece ikimiz kendi fona sahip melek yatırım (fön / para akışı) bünyemizi ihdas edecek ve her şeyi tam da bizim önceden tartışarak o harmanladığımız fikirleri hayata taşıyarak tatbik edip faaliyete koyacağız. Finansman kısmını bizzat kendim tedarik ederken, eşim / sevgilim / eşim diyebileceğim (Jessica) kendi ana mesaisi olduğu / dahilinde o işten tüm bağı koparırken sırf varışımız dahilindeki bu hedef adına mesai (work for it) yapabilecekti; keza Trevor  ve üstüne dahi o da yetmez deyip Robert i dahi projede ortak hanesine (as partners) kaydedecektik. \[13]

Nasıl daha öncelerin aksini savunmuyorsam, bu sefer binde bir lakin cidden (defalarca olduğu kez üzere bir defa daha) cahillik tam tabiriyle yine hep bizlerin ve benim / de lehimize işledi. Basbayağı bir kuruş dahi olsa Melek Fon Yatırımcısının tam bağlamında ne olduğuna dair bile zerrece bir malumat bağlamında ön görümüz var olmadığı bir durumda / süreç dahilindeyken; bir de üstüne 2005 gibi bir tarihte (Boston'da) feyz alıp danışarak / ders öğrenecek tek model Ron Conway benzeri karakterlerin eksikliği de bir muammaydı... Bizler de tek eylem olarak aslında mantığın (the obvious choices) bizi aklın ve selimin emrettiği o tek akış yönünde sürüklenmesiyle karar verdik ve icrada kıldığımız şeylerin çoğu bilindik olmasına rağmense (turned out to be novel) bir o kadar yepyeni / ilk oldu.

Y Combinator'da (oluşumunda / bağlam yapısı dahi demeliyiz) yapboz tablosunu sarmalayan binlerce dahi farklı birden ziyade fazla parça bulunduğundan da tüm unsurları aslında dahi (birden bir günde de tamamıyla) çözmüş bir noktada hiç durmadık. Bizim en asgari tabanda kavradığımız evreyi anlatan en doğru (çözdüğümüz kısım); "melek yatırımcılık (angel firm)" statüsü tablosuydu. Elbet de geçmiş o tarihte ("melek fonlama" söz öbeğini kastetmesi suretiyle), o tarz kelimeler kolaylarına uyuşmaz ve bir çatı altında geçmezlerdi. İçlerinde yatırımlara karar verip adım atmak icap edince ona yönelen memurlarını ("people whose job it was" - görevi olanları), yani kurumsal şirketin uzantıları (milyon dolarlık iş) yapan dahi VC oluşumları vardı...

**Düğüm Kimliği (Node ID):** 13c6f611-ac9f-47af-b76d-7e40ea16f7ed\
**Benzerlik (Similarity):** -0.06720844682537574\
**Metin (Text):** \[18] YC'yi (mercii, yapıyı de) terk ve nihayet bırakmaktan ötürü dahi gelmiş olan / bana da ağır tek binen kötülük ("worst thing"); Jessica ile asla ve kat'iyen artık (etrafta mesaisi dahi olmayışını) mesai geçiremeyip, yanımda dahi iş arkadaşlığından (not working with Jessica anymore) dahi o izlerin gidişi dahi idi. Zaten genel evresine ve taban tablolarına dahi ilk temas ettiğimiz dönemlerden tüm geçen tam süreçler bir bakıma YC serüveninde geçtiğinden / tüm her şey neredeyse ("We’d been working on YC almost the whole time we’d known each other") iç içe omuz omuzaya dahil de geçtiğinden dolayı ne eylem ile ve nede meslek ve ev yaşantısını (ne niyet ne teşebbüs etmemiş ("neither tried nor wanted to separate it from our personal lives" - "kişisel ya da yaşamdan ayırmaya uğraşmadığımız dahi gibi") eylem dahi niyet kalmadı; keza bu "ayrılığa gitmek de cidden resmen ("leaving was like pulling up a deeply rooted tree" - "kökü derin ve dibe dalan ulu ağacın kök sökümüne benzettiğini de" ) acısına eşdeğer kalıcı bir his tabanı bırakmasına olanak verdi.

\[19] Nitekim bir durumdan ve olguntan "kavram ve verinin (concept) 'İcat / Tasarım - Invented vs Discovered / Buluş' kıyasına evrildiği noktaya (hassasiyetteki)" dahi cidden biraz ("Way to get more precise") incelik tabiatında eğilindiğinde ve ehemmiyet de atfettirilen ilk baş yapı argümanları vs uzay formlarıyla (uzaylılarla - space aliens) bir muhabbete ve sohbete denk getirmeye benzetiş yapmak icap ettirebilir. Düzeyi her ne denli asgariden bir kademe üst safha/evrelilige tekabül eden ("Any sufficiently advanced alien civilization") medeniyet veya o uzay mensubu türler (aliens); mesela bir defasında Pythagoras (Pisagor Teoreminin dahi olan evrensel ("certainly know about the Pythagorean theorem")) buluşunu mutlak olarak tüm kurallarıyla ("certainly know") sularında dahi avuçlarına geçirmiş farz edilirler fena olmaz... Bense "Eminim, ne kadar biraz kuşku barındırsa (kesinlik taşımamasa = with less certainty) dahi ben McCarthy'in o meşhur kalıntı dökümlerine ("the Lisp in McCarthy’s 1960 paper"), taa 1960 yılına giden tezine ve yazıtındaki dahi form / dil Lisp format tabloları dil / yapı da vs hepsinin aşina dahi olduğuna inanırım." demeliyim/inancım bu minval...

Süreci bu dahi kılan ise; onlara da sadece bu form dil tablolarından ziyade, kendi yapılarında da olan kelime uzantılı ("the limit of the language that might be known to them") / nelerin malum dahi olduğunun aslında bir nebze neye atıfta evrilerek sadece bu kadarına dahi neden vakıf olacak / bilinecek denmesinin ("no reason to suppose") makule tabanda / aklı melekede (göstermeye mahal) veya ne akla uygun ki farz ve zannını dahi etmemize dahi asla olanak bırakmayacağı ve mahal kılmayacağı evreninde (bilişine sınır - limit getirmemesindeki yatanı)... Kaldı ki asıl manada ("Presumably aliens need numbers and errors and I/O too.") / Onlara sayılara ve o verisel işleyişe dair olan form yapılardaki girdilere dahi (input/output) - hatasına dahi vs tüm her şeye de gerekliliği ve ihtiyaçlılığı da bilindik bir kurgu formuydu zaten... Hâl böyle kalsa gerek ki ("So it seems likely there exists at least one path out of McCarthy’s Lisp along which discoveredness is preserved.") tamı tamına o McCarthy dökümündeki / veri yazısındaki "aslın bulgusu ve kalıcılığı (süregelenden aktarılıp günümüze de bozulmayan - the discoveredness is preserved") tabanından dahi bir iz yapılı/patikalı (at least one path) dilin veya o yol evresinin en asgaride olduğu ve de kalıtsal / korunduğu yönünde muhtemel kuvvet dökümleri bir nevi duruyordur / var olur dahi ("it seems likely")...

Yine ve yeniden teşekkürler ("Thanks to"): Trevor Blackwell efendiye, dahi John Collison beye, sonra Patrick Collison ile yine Daniel Gackle ile, keza Ralph Hazell ve de Jessica Livingston da / yanısıra en nihai (Robert Mor...) ile...

**Düğüm Kimliği (Node ID):** 6a638da9-f42f-4be6-a415-9698fd9636f9\
**Benzerlik (Similarity):** 0.036928354116716855\
**Metin (Text):** Oysa ben / Tam o tüm evreler içerisinde yavaştan da dahi kulak aşinasına ve bir nevi bilinci aşinalığa doğru akılarak; isminden ötürü dahi Web Ağ Örgüsü (World Wide Web) adını taşıyan / olarak nitelenen yepyeni ve bir de fütüristik evreye yelkenini ve demirlerini dahi çekecek olaydan haberdar olup duyarak ve esintiyle tanış oluyordum. Bu bağlam / süreç ise Harvard eksenli "grafik tasarımlardaki ara yüz ve sunum şekillerini ("grad school at Harvard") ve dahi "mikrobilgisayarlara sağladığı asıl getiri ve kolay kullanımla edinimine olanak tanınmasındaki deha/bilinç evrimiyle o büyük dâhice popülarite başarısını da gözler dahi öne serildiğinde" ("I’d seen what graphical user interfaces had done for the popularity of microcomputers") ne denli büyük bir etki sunduğunu bana kendisi ve dahi arkadaşı olarak aktararak Robert Morris anlattı/benliğimle yüz yüze paylaştı ("Robert Morris showed it to me when I visited him in Cambridge")... Görünen tam manada şuydu ki ağ (ağ örgüsü - the web / World Wide Web) ("It seemed to me that the web would be a big deal.") internete cidden fevkalade resmen damgasını (oldukça büyük bir işlev ile damga basacağına / etki bırakacağına ("It seemed like the web would do the same for the internet")) vuracaktı.

Bir varlık (mal ve mülk / sermaye - zengin olmayı - "want to get rich") yapma düşüncesini dahi barındırsaydım, ah işte trenin resmen son sığınağı / durağı ve yelkenini hareket noktasından kalkan tam sırası o esneye tekabül edecekti ("here was the next train leaving the station"). Ancak dürüst olmam lazım ve evet, orada ("I was right about that part") resmen doğru istikamet tabiatında olan tek unsur oydu; geri kalan tüm akıllara dahi o düşman (sakat ve hata bazlı) tabanlı tek hata ana ve tekli safsatayı bulan da dahi asıl bendim / yanılgının bizzat da fikri bana dayanıyordu ("What I got wrong was the idea."). Aldığım bir girişim ve eylem / kurmak üzere aksiyon fikrimle "bizim galerilerin internet üzerinden ("art galleries online") satıma ve dahi platform üzerinden eserlerin vs çevrimiçi ağa sunmaya dahi evirecek formda şirket ("start a company to put") atılımı ve faliyyeti içerisine gireceğiz yönündeydi... Yüz binlerce hatta ("after reading so many Y Combinator applications") bunca fecaati aşan ve dahi ne evrelere tekabül edip ulaşan onca sayısız / Y Combinator atılımına iştirakçi kaydı dökümlerine rağmen ("worst startup idea ever, but it was up there"), en kötü, resmen ve dilde ve kelam sınırında felaket senaryosu bu diyemesem bile inanın tam hudut kısmında yani dorukta/listede orada kendisiyle bir tepe kurardı... Çünkü resmen ("Art galleries didn’t want to be online") galeriler yahut onların resim formlarındaki eserlerin sergi unsurları o dönemki bağlamı nezdinde internet aşıp da sisteme yayılmaya bile ("still don’t, not the fancy ones") o havalıları dâhil gram zerre ilgi çekmek yahut istek dahi asla barındırmıyorlar iken satmaya/satış serüvenlerine dahi de yeltenme tarzlarına dahi ne bir yatkın şekline bile nezdinde evrilmediler de ("That’s not how they sell." - Keza o stil de onlara matuf bir sergileyiş yahut ticari yordam da değildi ki satıs tablosu kursunlar)... Akabinde kendi yazılım ("wrote some software to generate web sites for galleries") tablosuna sığınarak galerileri temsil mekanizmada ve vitrinde yer tutacak sisteme bir form aracı eylemi yazdım, diğer tarafta Robert de ("resize images") döküm veyahut imge / grafiğin form-satır ve çözüntü format döküm ve ayarlarına dair ve en başta döküm ile sunucunun aktarımının da yerini işleteceği http protokol / sunum evresini de ("setup an http server to serve the pages") inşa etmesine o yazıp / koda aktardı...  (Then we tried to sign up ga...

```python
retriever = index.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=3,
    vector_store_kwargs={"mmr_threshold": 0.8},
)
nodes = retriever.retrieve(
    "Yazar Y Combinator'da geçirdiği dönemde neler yaptı?"
)
```

```python
for n in nodes:
    display_source_node(n, source_length=1000)
```

**Düğüm Kimliği (Node ID):** 72313b35-f0dc-4abb-919c-a440aebf0398\
**Benzerlik (Similarity):** 0.4788025508513971\
**Metin (Text):** Akşam yemeğinden döndükten sonra / ayrıldıktan sonra Jessica'yla beraber bir taraftan yürürken (11 Mart gününde); Walker sokakları ile Garden yapılarının da bitiştiği köşe dahi derken bu üç bağ bir köşede kilitlendi. Daha akıllarında bir nihayete varamayan (fikirlerini bulup o akla yatıramayan) VC'lerin de (Sermayedarlar) ben ne diyeyim... Biz sadece ikimiz kendi fona sahip melek yatırım (fön / para akışı) bünyemizi ihdas edecek ve her şeyi tam da bizim önceden tartışarak o harmanladığımız fikirleri hayata taşıyarak tatbik edip faaliyete koyacağız. Finansman kısmını bizzat kendim tedarik ederken, eşim / sevgilim / eşim diyebileceğim (Jessica) kendi ana mesaisi olduğu / dahilinde o işten tüm bağı koparırken sırf varışımız dahilindeki bu hedef adına mesai (work for it) yapabilecekti; keza Trevor  ve üstüne dahi o da yetmez deyip Robert i dahi projede ortak hanesine (as partners) kaydedecektik. \[13]

Nasıl daha öncelerin aksini savunmuyorsam, bu sefer binde bir lakin cidden (defalarca olduğu kez üzere bir defa daha) cahillik tam tabiriyle yine hep bizlerin ve benim / de lehimize işledi. Basbayağı bir kuruş dahi olsa Melek Fon Yatırımcısının tam bağlamında ne olduğuna dair bile zerrece bir malumat bağlamında ön görümüz var olmadığı bir durumda / süreç dahilindeyken; bir de üstüne 2005 gibi bir tarihte (Boston'da) feyz alıp danışarak / ders öğrenecek tek model Ron Conway benzeri karakterlerin eksikliği de bir muammaydı... Bizler de tek eylem olarak aslında mantığın (the obvious choices) bizi aklın ve selimin emrettiği o tek akış yönünde sürüklenmesiyle karar verdik ve icrada kıldığımız şeylerin çoğu bilindik olmasına rağmense (turned out to be novel) bir o kadar yepyeni / ilk oldu.

Y Combinator'da (oluşumunda / bağlam yapısı dahi demeliyiz) yapboz tablosunu sarmalayan binlerce dahi farklı birden ziyade fazla parça bulunduğundan da tüm unsurları aslında dahi (birden bir günde de tamamıyla) çözmüş bir noktada hiç durmadık. Bizim en asgari tabanda kavradığımız evreyi anlatan en doğru (çözdüğümüz kısım); "melek yatırımcılık (angel firm)" statüsü tablosuydu. Elbet de geçmiş o tarihte ("melek fonlama" söz öbeğini kastetmesi suretiyle), o tarz kelimeler kolaylarına uyuşmaz ve bir çatı altında geçmezlerdi. İçlerinde yatırımlara karar verip adım atmak icap edince ona yönelen memurlarını ("people whose job it was" - görevi olanları), yani kurumsal şirketin uzantıları (milyon dolarlık iş) yapan dahi VC oluşumları vardı...

**Düğüm Kimliği (Node ID):** 555f8603-79f5-424c-bfef-b7a8d9523d4c\
**Benzerlik (Similarity):** 0.30086405397508975\
**Metin (Text):** \[15] İlk olarak adım attığımız (kurduğumuz) "Yaz Dönemi Kurucuları/Projeleri Fonu - Summer Founders Program" ("Summer Founders Program") atılımına tüm hatlarla tamı tamına 225 ("225 applications") bir asıl müracaat başvurusuyla gelerek katılım talebi aldık, ki şaşılacak hadise ve en tuhaf ("surprised to find that") durum, bunlarında da cidden o an okul/üniversite safhalarında diploma alarak çoktan dahi ("already graduated") çoktan mezun olma sırasına dahi adledilmiş epey oranda kimsenin bu yolla iştirakinin bile/dahi oluşuydu (veya o baharda - that spring - mezun olma arifesinde olanların)... En asgarisinden o güne kadar / bu ("Already") safhaya değin dahi biz SFP eylemini pek ciddiye veya aşırı bir raddeye tekabül edeceği kıstaslara alarak ("feel more serious than we’d intended.") başlatmamış veya böylesine niyet etmememize nazaran ciddi evresine tekabül evveliyata akmıştı/ulaşmıştı...

Ve akabindeki durakta, biz mülakata dahil olmak arzusuna binaen içlerindeki grupta yalnız veya asgarisinde sadece 20 veya 20 adediyle / grup bazındaki katılım nezdindeki sayıları, o da yalnız yüz yüze görüşmeye ("to interview in person") ve aradan elediklerimizin sayısındaki o binde oranında / ve ardından en niteliklilerini de yalnız ve sadece o yığın aralarındaki ("picked 8 to fund") sekizi sayılan döküme maddi bir fön (fona aktarmaya/fonlamaya dahi layık da gördük) takdim ederek layıkla (başlattık) ayırdık. Hepsi birbirinden göz alan / şahane yeteneklerle kuşanıp ("impressive group") etkileyiciydiler. Bizzat şu en evveliyat olan ve ta baştaki olan o listeye ilk sıralarda adlarını perçinleyip de akabinde / reddit isminde olan, Justin Kan de ve Twitch dahi kuruluşlarına imzasını yaldızla da çakan ("founded Twitch") / ve ilerleyen yıllarda spesifik evrede RSS yazılım bazlı şartnamesindeki evrelerine yardım suretli kalemi atan veyahut ("helped write the RSS spec") şimdilerde o adını veriye ve erişimde kısıt ve prangaların tecridine dair de kısıtlarla karşı gelen bir aziz/şehit kurbanı formunda dahi anılışı bakiye kalan merhum ("martyr for open access") Aaron Swartz ve de ileride/şimdilerdeki atılımı da YC atılımının başkanlığında ve akabinde de onun 2. dahi statüsündeki yer alan ("the second president of YC") Sam Altman da bilfiil o kadroda/aralarında bir nevi yer teşkil buldu ve katıldılar. Yalnız ilk gelen / olanların bu raddelerde şahikalarla / etkileyici bir de üst düzey evresinde dahi seyretmesi ("entirely luck that the first batch was so good") şüphesiz ve kanıtlarıyla asla / salt kaba (boş) kör tesadüflerle değil bilhassa tüm olanla / olgu ile / salt başarıya evirilecekti. Nasıl olmasın! Bilindik mecra/sektörler, ki bunlar Microsoft (yahut bankacı/finans dahi devlerine ("legit place like Microsoft or Goldman Sachs") bir yaz staj atılımı bulma/kovalayan o basit tabiatlı yolla geçirmeme aksinin kararın kılındığı) ve / cidden de Summer Founders / Yaz Atılım fonlama evresi/projeleri vs. evresindeki yelpazedeki gibi ekseniyle eksantrik/deli/çılgın dahi (weird thing) sayılacak bir müracaattan dahi dahi sıyrılıp ta eyleme cesaret kalmak resmen bile epey bir tabanlı yüreklilik/atılganlığı (pretty bold) cidden resmen asgari formlarla taleple/külliyen de zorunlu eyliyordu.

Bahsi edilen, sözleşmesi kılınan (deal for startups), anlaşılan girişim format anlaşmaları ilk elde (esasen; the deal we did with Julian) Julian atılımı üzerinden bizzat bir 10 bin meblağı ($10k for 10% / yüzde on) dahi atılıma referans alması / ile ...

**Düğüm Kimliği (Node ID):** d1a19a77-93e2-4f5b-8eb2-b7f265f15ec2\
**Benzerlik (Similarity):** 0.29257547208236784\
**Metin (Text):** Sorun aslında asla statü bazındaki pırıltısından (veya değerlilikteki parıltıyla parlayış - unprestigious types of work are good per se / saygın değil diye iyi olmaktan - salt değerinden azaldığından kaynaklı yahut kendi itibarı - özü nedeniyle iyi olan / yahut pür değer addedilmesinde evrilen) bir durum/neden teşkil dahi de demez. Amma ("But when you find yourself") asıl odak bir statü yahut paha arz dahi eden / veya edinimine rağmen tam eksiden de olsa kendi pırıltısında/ilgide o azlığa / zayıf parlamadaki eksiye ve o prestiji eksik görünen eksikliğine dahi bile bile ("despite its current lack of prestige") salt tutku dahi ve kalbi arzulu yöneliş buluyorsanız dahi bir sahanın dahi etrafında dönmeniz ya da o şeye/eyleme yönelişe ve (çekilmeye / "drawn to some kind of work") tabiri dahi en basiti evresi ile/nezdinde bile dahi şayet kendinizi orada eyleyen bir kurguya / yahut olgu nezdinde bulursanız da; işte tam tekmil de (It's a sign); bu durum doğrudan dahi de orada bulunacak ("there’s something real to be discovered there"), somut asgarisinde arzedilirliği elbet hakiki tabiata bürünen / ve o manada bürünen / o dilde var (olduğu olan somut gerçeğinin nişanı iken (sahici tabiatlarda)); aynı koldan ("and that you have the right kind of motives" / saik - niyetleri/motivasyonlardaki o hak olan duruma evrilmeniz demektir) da kendi itibar evrenin de dahi gayret ve güdü mahiyetindeki de tabanlarındaki ekseninizin dahi hakiki doğruluk safında / güdü niyetinin pak tabiatının ve elyafının / formunda dahi barındığına bir resmen tam bir kılavuz nişanesidir de. Hedeflenenlerin/Tebanın hırs atılımından ve dahi şatafat arayışı safsatadaki sığların/batağın kirlerine ("Impure motives") batışı ise hırslarla ("for the ambitious") demlenmenin / o tam bir kurban / bir tehlike (the big danger) formuna taban atmasına teşkil durur. Ki insan dahi ("If anything is going to lead you astray") tamı tamına bir batağa / ve yoldan dahi dahi sapmaya eğildiklerinde/evrildiklerinde de, "bunun tek müsebbibleri; bizzat şaşaa dahi yalanı ile dahi de o en insan zihniyetindekilere etki arzındaki caka satma dahi yalanına matuf o binişi - desire to impress people" duruşu ve kibri / o birikimin asıl arzularında var (tabanlarında da evriliyordur / yatar da denilebilir dahi). Tam da bu (so while working on) statüleri, evreleri / pırıltı/fiyakadan epey sığ da olsa prestiji gerilerde dahi olan / pırpırı noksan eylemlerde mesaisi dahi atarak/vakit dahi geçirmek ve yahut dahi zaman yarmak da (on things that aren’t prestigious) tüm mutlakiyeti ile yürüdüğünüzün dahi doğrusuyla ve bir minval en tam olan doğruluğu ile yolda ("doesn’t guarantee you’re on the right track") ve patikada ("guarantees you’re not on the most common type of wrong one" / "sizi bir nevi koruyup kollaması bazındaki en evvel en yanlış safhatlar patikasında / en yoldan çeldirilenler de aranızda bir barikat kurarak / teyid eder de" formunda / en sapa çarkından muhafaza ile olmanıza en kâfiyle (sanki bizzat da barikat) ve engel / garanti sayılabilir bir temin safhası veya duvarıdır diye) evrildiği/sayıldığı ve o dahi teyid eylemidir...

Neredeyse dahi ardından geçen epey bir senelikteki takiplerindeki / sonlu (senelerde/yıllarda da - Over the next several years), asgaride sayısız birden epey konuyla/mevzusunda o alanda / envai çeşidiyle makale dahi ve yığınca ve bol bol "I wrote lots of essays" evresine girdim / yazıp çizerek dahi kendim kaleme dahi çektim/aktardım. O'Reilly adıyla olanların içerisindeki yazıtlarımdan seçtiğini kitap bazında eyleyerek derlemesini (O’Reilly reprinted a collection of them as a book) "Hacker'ler ve Ressam formunda (Hackers & Painters)" diyerek kitabına unvan ve tam mahiyetinde bir nişan / dahi atfederek (after one of the essays in it / makalemin içinden ismine istinaden atıfla) eseri tabana da sürdü. Aynı şekilde / bunlarla ("also worked on spam filters") ben bizzat istenmeyen (spam vb.) kirlilik süzgecinde dahi bir aralığa varıp mesailere harcadım / zaman yaktım (çalışarak - worked), yahut / biraz azami safhalarda da ekstra da tablolarda ("did some more painting" / resim çalışmaları) da bir şeyler daha boyamaya dair de işledim. Geleneğim, alışkanlığım olarak bir kabile dahi denebilir "perşembe gün/gecesi bazında ("used to have dinners")" misafirane bir yemekli tablolarda arkadaş evrenleriyle - "dost" grubu ile akşamlarını ("for a group of friends every thursday night") eviriyor ve (ki bunun bana yemek pişirme ("taught me how to cook for groups") adabımı ve yahut kalabalık öğün evrelerinde şefliği yegâne vesile olduğu / öğrettiği) aşamalarına şahit / taban attım... Nitekim (ben ise sonradan ("And I bought another building in Cambridge") Cambridge bünyesinde yeni bir evreyi tesis ettiğim başka mülk / yapı alırken) bu yapı ki o ("a former candy factory") bir vakit şeker / tatlının ana menzilinin adresi olan fabrika tabanlı (...

```python
retriever = index.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=3,
    vector_store_kwargs={"mmr_threshold": 1.0},
)
nodes = retriever.retrieve(
    "Yazar Y Combinator'da geçirdiği dönemde neler yaptı?"
)
```

```python
for n in nodes:
    display_source_node(n, source_length=1000)
```

**Düğüm Kimliği (Node ID):** 72313b35-f0dc-4abb-919c-a440aebf0398\
**Benzerlik (Similarity):** 0.5985031885642463\
**Metin (Text):** Akşam yemeğinden döndükten sonra / ayrıldıktan sonra Jessica'yla beraber bir taraftan yürürken (11 Mart gününde); Walker sokakları ile Garden yapılarının da bitiştiği köşe dahi derken bu üç bağ bir köşede kilitlendi. Daha akıllarında bir nihayete varamayan (fikirlerini bulup o akla yatıramayan) VC'lerin de (Sermayedarlar) ben ne diyeyim... Biz sadece ikimiz kendi fona sahip melek yatırım (fön / para akışı) bünyemizi ihdas edecek ve her şeyi tam da bizim önceden tartışarak o harmanladığımız fikirleri hayata taşıyarak tatbik edip faaliyete koyacağız. Finansman kısmını bizzat kendim tedarik ederken, eşim / sevgilim / eşim diyebileceğim (Jessica) kendi ana mesaisi olduğu / dahilinde o işten tüm bağı koparırken sırf varışımız dahilindeki bu hedef adına mesai (work for it) yapabilecekti; keza Trevor  ve üstüne dahi o da yetmez deyip Robert i dahi projede ortak hanesine (as partners) kaydedecektik. \[13]

Nasıl daha öncelerin aksini savunmuyorsam, bu sefer binde bir lakin cidden (defalarca olduğu kez üzere bir defa daha) cahillik tam tabiriyle yine hep bizlerin ve benim / de lehimize işledi. Basbayağı bir kuruş dahi olsa Melek Fon Yatırımcısının tam bağlamında ne olduğuna dair bile zerrece bir malumat bağlamında ön görümüz var olmadığı bir durumda / süreç dahilindeyken; bir de üstüne 2005 gibi bir tarihte (Boston'da) feyz alıp danışarak / ders öğrenecek tek model Ron Conway benzeri karakterlerin eksikliği de bir muammaydı... Bizler de tek eylem olarak aslında mantığın (the obvious choices) bizi aklın ve selimin emrettiği o tek akış yönünde sürüklenmesiyle karar verdik ve icrada kıldığımız şeylerin çoğu bilindik olmasına rağmense (turned out to be novel) bir o kadar yepyeni / ilk oldu.

Y Combinator'da (oluşumunda / bağlam yapısı dahi demeliyiz) yapboz tablosunu sarmalayan binlerce dahi farklı birden ziyade fazla parça bulunduğundan da tüm unsurları aslında dahi (birden bir günde de tamamıyla) çözmüş bir noktada hiç durmadık. Bizim en asgari tabanda kavradığımız evreyi anlatan en doğru (çözdüğümüz kısım); "melek yatırımcılık (angel firm)" statüsü tablosuydu. Elbet de geçmiş o tarihte ("melek fonlama" söz öbeğini kastetmesi suretiyle), o tarz kelimeler kolaylarına uyuşmaz ve bir çatı altında geçmezlerdi. İçlerinde yatırımlara karar verip adım atmak icap edince ona yönelen memurlarını ("people whose job it was" - görevi olanları), yani kurumsal şirketin uzantıları (milyon dolarlık iş) yapan dahi VC oluşumları vardı...

**Düğüm Kimliği (Node ID):** 555f8603-79f5-424c-bfef-b7a8d9523d4c\
**Benzerlik (Similarity):** 0.5814802966348447\
**Metin (Text):** \[15] İlk olarak adım attığımız (kurduğumuz) "Yaz Dönemi Kurucuları/Projeleri Fonu - Summer Founders Program" ("Summer Founders Program") atılımına tüm hatlarla tamı tamına 225 ("225 applications") bir asıl müracaat başvurusuyla gelerek katılım talebi aldık, ki şaşılacak hadise ve en tuhaf ("surprised to find that") durum, bunlarında da cidden o an okul/üniversite safhalarında diploma alarak çoktan dahi ("already graduated") çoktan mezun olma sırasına dahi adledilmiş epey oranda kimsenin bu yolla iştirakinin bile/dahi oluşuydu (veya o baharda - that spring - mezun olma arifesinde olanların)... En asgarisinden o güne kadar / bu ("Already") safhaya değin dahi biz SFP eylemini pek ciddiye veya aşırı bir raddeye tekabül edeceği kıstaslara alarak ("feel more serious than we’d intended.") başlatmamış veya böylesine niyet etmememize nazaran ciddi evresine tekabül evveliyata akmıştı/ulaşmıştı...

Ve akabindeki durakta, biz mülakata dahil olmak arzusuna binaen içlerindeki grupta yalnız veya asgarisinde sadece 20 veya 20 adediyle / grup bazındaki katılım nezdindeki sayıları, o da yalnız yüz yüze görüşmeye ("to interview in person") ve aradan elediklerimizin sayısındaki o binde oranında / ve ardından en niteliklilerini de yalnız ve sadece o yığın aralarındaki ("picked 8 to fund") sekizi sayılan döküme maddi bir fön (fona aktarmaya/fonlamaya dahi layık da gördük) takdim ederek layıkla (başlattık) ayırdık. Hepsi birbirinden göz alan / şahane yeteneklerle kuşanıp ("impressive group") etkileyiciydiler. Bizzat şu en evveliyat olan ve ta baştaki olan o listeye ilk sıralarda adlarını perçinleyip de akabinde / reddit isminde olan, Justin Kan de ve Twitch dahi kuruluşlarına imzasını yaldızla da çakan ("founded Twitch") / ve ilerleyen yıllarda spesifik evrede RSS yazılım bazlı şartnamesindeki evrelerine yardım suretli kalemi atan veyahut ("helped write the RSS spec") şimdilerde o adını veriye ve erişimde kısıt ve prangaların tecridine dair de kısıtlarla karşı gelen bir aziz/şehit kurbanı formunda dahi anılışı bakiye kalan merhum ("martyr for open access") Aaron Swartz ve de ileride/şimdilerdeki atılımı da YC atılımının başkanlığında ve akabinde de onun 2. dahi statüsündeki yer alan ("the second president of YC") Sam Altman da bilfiil o kadroda/aralarında bir nevi yer teşkil buldu ve katıldılar. Yalnız ilk gelen / olanların bu raddelerde şahikalarla / etkileyici bir de üst düzey evresinde dahi seyretmesi ("entirely luck that the first batch was so good") şüphesiz ve kanıtlarıyla asla / salt kaba (boş) kör tesadüflerle değil bilhassa tüm olanla / olgu ile / salt başarıya evirilecekti. Nasıl olmasın! Bilindik mecra/sektörler, ki bunlar Microsoft (yahut bankacı/finans dahi devlerine ("legit place like Microsoft or Goldman Sachs") bir yaz staj atılımı bulma/kovalayan o basit tabiatlı yolla geçirmeme aksinin kararın kılındığı) ve / cidden de Summer Founders / Yaz Atılım fonlama evresi/projeleri vs. evresindeki yelpazedeki gibi ekseniyle eksantrik/deli/çılgın dahi (weird thing) sayılacak bir müracaattan dahi dahi sıyrılıp ta eyleme cesaret kalmak resmen bile epey bir tabanlı yüreklilik/atılganlığı (pretty bold) cidden resmen asgari formlarla taleple/külliyen de zorunlu eyliyordu.

Bahsi edilen, sözleşmesi kılınan (deal for startups), anlaşılan girişim format anlaşmaları ilk elde (esasen; the deal we did with Julian) Julian atılımı üzerinden bizzat bir 10 bin meblağı ($10k for 10% / yüzde on) dahi atılıma referans alması / ile ...

**Düğüm Kimliği (Node ID):** 23010353-0f2b-4c4f-9ff0-7c1f1201edac\
**Benzerlik (Similarity):** 0.562748668285032\
**Metin (Text):** Elbet de ben bilhassa mesaimde (YC nezdinde - dealing with some urgent problem during YC) o an tam bir kriz patladığında / bir vaka anına denk gediğim her evrede / meşgul olduğum anın getirisinde; tahmini ("there was about a 60% chance it had to do with HN") %60'a vuran orantısı / olasılığı ya HN arayüz program tabanı/yapısıyla da yahut ("and a 40% chance it had do with everything else combined") 40 oranındaki asgeri kalanı (40 chance it) ile resmen tüm / bilumum geri kalanın (bağlantı / her şey dahi) yığılarak - kombineleşerek toplaşmış pürüzlerle de tüm ilgisi iltisakıydı... \[17]

Ve HN de dahi ("As well as HN"), diğer taraftaysa / Arc ile tüm YC'nin resmen (kod / altyapısında dahi ("all of YC’s internal software in Arc") işlenilen program/dahili tüm dâhili yazılım mimarisini bizzat da kodunu işleyip yazdım / döküm ettim (I wrote)). Esasen bir nevze iyi niyet veya güzelce denilebilen bir epey safhada da ("I continued to work a good deal in Arc") işime ve gayretime dahi çabalıyor ("I gradually stopped") veya o evrelere kafa da dahi patlatıp işime uğraş dahi verseydim dahi zaman aktarışlarımda yavaş yavaş "Arc'taki yazılım faaliyetinde bulunmaya çalışmaktan / o evrelerden" de geri durularak elimi ayağımı/gayretimi de kesmeye başladım ("Stopped working on Arc"). Nedenim birazı da şuydu ("partly because"): hem zaman açısından resmen cidden / ve yahut gram vaktimin bana kâr/yahut noksansız / yetersizliğinden (don't have time to) daralması, bense kalan o parça / kısmı minvaliyle de / neden dahi ise evrelerin de ("and partly because it was a lot less attractive to mess around with the language") şahikasına dek; tüm şu yığına ("now that we had all this infrastructure depending on it") tek merkez ve bir yapıyla kökleriyle gömülmüş (depends / tutunmuş / veya bu eksene kilitli - bağımlı) bir sistemde / ağların temelinin ana unsurunda ("the infrastructure") taban teşkil ederken artık da eskisi ("now that") o eski cazibe perdesi ile / veya şatafatının ne denli dahi olsa dil ekseni ("the language") etrafı evresinde bulanmanın veya etrafta bir şekilde takılıp kurcalayacak / oynanarak de ("mess around with The language") / zaman aşırttıracak ilgisinden (çekici - attraktive olan sularından uzak / cidden bir epey çekiciliğinin solmuş / "less attractive" dahi gelmesiyle veya olmasından ve eksilmesindeki noksanına tekabül) azalmasından dayanıyordu / mütevellitti ("and partly because it was a lot less attractive to mess around with the language"). Böylelikle asıl nihayette elimde (sularıma çekilmiş/indirgenmiş olarak ("Three projects were reduced to two") var olup bana süzülen 2 şey geride yer ederek: Dökümlerimi / yazılarımı dahi eylemek ("writing essays") ve öte evresinde ise bilhassa bu platform - YC ("working on YC") nezdinde faaliyet / gayret içinde olmak kalmıştı geriye...

Hiper evresi dahilinde geçmiş ile bilhassa ("YC was different") diğer iş / taban evrelerinin akışları ve olanlarından bütünüyle dahi başkaca - bambaşkaydı ("from other kinds of work I've done"). Üzerinde tabiatına yöneltmem (kararlar - deciding for myself) odak bağlamım olan dahi mevzularda / problemlerde o an ("instead of deciding for myself what to work on") da o asıl dertlere / yahut çözümlenmesi o işlere eğilip ne üzerinde kafa yoracağıma bizzat dahi kararlar kılmak da yerine; doğrudan (bizzat - the problems came to me) asıl noksanlık / arıza ve her dert türünden olay bir şekilde gelip o sorunla benim yollarıma baş başaya kavuşuyordu / önüme kendisinden dikiliyordu... En asgaride de 6 aylık evresinde/periyodunun ardından dahi yığına taze girişim safahatlarını kucaklayan / start-up seli yahut o grubu devresine adımlardı / gelirdi ("Every 6 months there was a new batch of startups") ve nihayet resmen her demleri yahut dert de olan mevzuları (ve o engelleri (their problems) veya ne yığına / sıkıntıya sahip de olurlar dahi o her arızaları ("whatever they were")) sanki bizim o dertlere (kendi eksenimize / our problems) bizzat iç dert olmaya (became) dönüşüp bize bulaşırdı... Olası tüm denkleme rağmen resmen ("it was very engaging work" / acayip - fevkalade sarıyor veya o işin meşgulüne atılıyor / çekilerek dalıyordunuz da - ilginizi tam bir sürükleme ile kapılıp ilgi uyandırıyordu) inanılmaz derecelere bir bağlamda da / cazibe uyanarak dahi kendinizi sarıyor yahut çekiyordu da içine (it was very engaging work); nitekim dert / arıza profilleri oldukça (resmen "very varied/quite varied") fevkalade ve alabildiğine envai renkli ve neviler/teşkil türlerin dökümünden (çeşit çeşitti "quite varied") geliyor, kaldı da hakikat tabanını (the good founders) elinden alan dirayetli veya iyi olarak donanımlı kurucuların ekserisiyse de cidden ama / resmen cidden "very effective" fevkaladen oldukça etkin / veya işi kıvıran o ehillerle - maharet odaklarıyla evriliyordu (çok etkindi)... Ne olur / veya eğer / sen ("If you were trying to learn the most you could about startups in the short" - dersen ki tamı tamına ve yahut) bilakis şayet tüm o sularında; bu işlerin/o startuplar evrenine yönelik dahi dahi olabilecek (en kapsamından en bir epeyesine - the most you could do / öğrenebileceğin tüm yığının - "learn the most you could") veya o kısıtlı periyota bir en sular / ne varsa diye kısa ("in the short...") zamanda (time)... 
