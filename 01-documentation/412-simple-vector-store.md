---
title: Basit Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Basit Vektör Deposu (Simple Vector Store)

Eğer bu Not Defterini (Notebook) Colab ortamında açıyorsanız, muhtemelen LlamaIndex'i 🦙 sisteminize kurmanız gerekecektir.

```bash
!pip install llama-index
```

```python
import os
import openai


os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = os.environ["OPENAI_API_KEY"]
```

#### Belgeleri yükleyin, VectorStoreIndex'i (Vektör Deposu İndeksi) oluşturun

```python
import nltk


nltk.download("stopwords")
```

```bash
[nltk_data] Downloading package stopwords to
[nltk_data]     /Users/jerryliu/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!










True
```

```python
import llama_index.core
```

```bash
[nltk_data] Downloading package stopwords to /Users/jerryliu/Programmi
[nltk_data]     ng/gpt_index/.venv/lib/python3.10/site-
[nltk_data]     packages/llama_index/core/_static/nltk_cache...
[nltk_data]   Unzipping corpora/stopwords.zip.
[nltk_data] Downloading package punkt to /Users/jerryliu/Programming/g
[nltk_data]     pt_index/.venv/lib/python3.10/site-
[nltk_data]     packages/llama_index/core/_static/nltk_cache...
[nltk_data]   Unzipping tokenizers/punkt.zip.
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
)
from IPython.display import Markdown, display
```

Veriyi İndirin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```bash
--2024-02-12 13:21:13--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
raw.githubusercontent.com (raw.githubusercontent.com) çözümleniyor... 185.199.110.133, 185.199.111.133, 185.199.108.133, ...
raw.githubusercontent.com (raw.githubusercontent.com)|185.199.110.133|:443 adresine bağlanılıyor... bağlanıldı.
HTTP isteği gönderildi, yanıt bekleniyor... 200 OK
Uzunluk: 75042 (73K) [text/plain]
Kaydediliyor: ‘data/paul_graham/paul_graham_essay.txt’


data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    0.02s içinde


2024-02-12 13:21:13 (4.76 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ kaydedildi [75042/75042]
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
index = VectorStoreIndex.from_documents(documents)
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
```

```python
# indeksi diske kaydet
index.set_index_id("vector_index")
index.storage_context.persist("./storage")
```

```python
# depolama bağlamını yeniden kur/inşa et
storage_context = StorageContext.from_defaults(persist_dir="storage")
# indeksi yükle
index = load_index_from_storage(storage_context, index_id="vector_index")
```

```bash
INFO:llama_index.core.indices.loading:Şu kimliklere (ids) sahip indeksler yükleniyor: ['vector_index']
Şu kimliklere (ids) sahip indeksler yükleniyor: ['vector_index']
```

#### İndeks Sorgulayın (Query Index)

```python
# Daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine(response_mode="tree_summarize")
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar bu mecrada kısa hikayeler kaleme alarak, bunlara ilaveten programlama üzerine (özellikle 9. sınıfta yer aldığı dönem boyunca bir IBM 1401 bilgisayar eşliğinde) çeşitli çalışmalar yürüttü. Kendisi daha sonra kitleler için yapılmış standart bir mikrobilgisayarla değil de, kit halinde alınmış modüler bir mikrobilgisayarla işlem yapmaya yönelerek nihayetinde bir TRS-80 tabanına uzanış gerçekleştirdi. Buna binaen basit oyunlar, roketlerin yükseleceği mesafeleri (yükseklik) tespit etmeye olanak tanıyan bir tür deneme ve dahi bilinen kelime işlemcilerine uzanan programlar yazdı. Yazar en başta üniversite yıllarında doğrudan felsefe okumayı tasarlasa da sonraları bir netice olarak (veya yönelerek) Yapay Zeka (AI) alanında çalışmaya karar verdi.**

**SVM / Doğrusal Regresyon (Linear Regression) ile İndeks Sorgulama**

Karpathy’nin [SVM tabanlı](https://twitter.com/karpathy/status/1647025230546886658?s=20) (SVM-based) yaklaşımını kullanın. Sorguyu pozitif örnek olarak, diğer tüm veri noktalarını ise negatif örnekler olarak ayarlayın ve ardından da bir hiperdüzlem (hyperplane) uydurun (fit).

```python
query_modes = [
    "svm",
    "linear_regression",
    "logistic_regression",
]
for query_mode in query_modes:
    # Daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
    query_engine = index.as_query_engine(vector_store_query_mode=query_mode)
    response = query_engine.query("Yazar büyürken neler yaptı?")
    print(f"Sorgu modu (Query mode): {query_mode}")
    display(Markdown(f"<b>{response}</b>"))
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




/Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages/sklearn/svm/_classes.py:31: FutureWarning: `dual` öğesinin varsayılan (default) değeri 1.5 sürümünde `True` iken değişerek `'auto'` olacaktır. Uyarıyı (warning) bastırmak (kaldırmak için) için `dual` değerini açıkça ayarlayın.
  warnings.warn(




INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Sorgu modu: svm
```

**Yazar bu mecrada kısa hikayeler kaleme alarak, bunlara ilaveten programlama üzerine (özellikle 9. sınıfta yer aldığı dönem boyunca bir IBM 1401 bilgisayar eşliğinde) çeşitli çalışmalar yürüttü. Kendisi daha sonra kitleler için yapılmış standart bir mikrobilgisayarla değil de, kit halinde alınmış modüler bir mikrobilgisayarla işlem yapmaya yönelerek nihayetinde bir TRS-80 tabanına uzanış gerçekleştirdi. Buna binaen basit oyunlar ve kelime işlemcisine uzanan programlar yazdı. Yazar en başta üniversitedeyken felsefe okumayı tasarlasa da sonraları bir netice olarak Yapay Zeka (AI) alanında çalışmaya karar verdi.**

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




/Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages/sklearn/svm/_classes.py:31: FutureWarning: `dual` öğesinin varsayılan (default) değeri 1.5 sürümünde `True` iken değişerek `'auto'` olacaktır. Uyarıyı (warning) bastırmak (kaldırmak için) için `dual` değerini açıkça ayarlayın.
  warnings.warn(




INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Sorgu modu: linear_regression
```

**Yazar kısa hikayeler kaleme alarak ve ayrıca programlama üzerine (özellikle 9. sınıfta olduğu bir dönemde bir IBM 1401 bilgisayarı eşliğinde) çeşitli çalışmalarda bulundu. Sonrasında standart (mikrobilgisayar) bir düzen yerine; kit halinde alınmış bir mikrobilgisayar bazında işlem yapmaya yönelerek basit oyunlar ve ardından (dahi) bilinen kelime işlemcilerine varıncaya dek programlar yazdı. Yazar en başta felsefe okumayı tasarlasa da sonraları yönünü Yapay Zeka (AI) alanına değiştirdi.**

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




/Users/jerryliu/Programming/gpt_index/.venv/lib/python3.10/site-packages/sklearn/svm/_classes.py:31: FutureWarning: `dual` öğesinin varsayılan (default) değeri 1.5 sürümünde `True` iken değişerek `'auto'` olacaktır. Uyarıyı (warning) bastırmak (kaldırmak için) için `dual` değerini açıkça ayarlayın.
  warnings.warn(




INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Sorgu modu: logistic_regression
```

**Yazar bu dönemde kısa öyküler kaleme aldı ve ilaveten programlama üzerinde (bilhassa 9. sınıfa tekabül eden bir IBM 1401 platformu çerçevesinde) çalıştı. Bilahare kendisine has bir mikrobilgisayara adım atarak bu formatla bazı yapılar meydana getirdi; sözgelimi kelime işlemcisine uzanıp, basit oyunlar kodladı. Yazar esasında felsefe eğitimine başlasa da bir nihayet olarak Yapay Zeka (AI) tabanına geçti.**

```python
display(Markdown(f"<b>{response}</b>"))
```

**Yazar bu dönemde kısa öyküler kaleme aldı ve ilaveten programlama üzerinde (bilhassa 9. sınıfa tekabül eden bir IBM 1401 platformu çerçevesinde) çalıştı. Bilahare kendisine has bir mikrobilgisayara adım atarak bu formatla bazı yapılar meydana getirdi; sözgelimi kelime işlemcisine uzanıp, basit oyunlar kodladı. Yazar esasında felsefe eğitimine başlasa da bir nihayet olarak Yapay Zeka (AI) tabanına geçti.**

```python
print(response.source_nodes[0].text)
```

```bash
Ne Üzerinde Çalıştım


Şubat 2021


Üniversiteden önce okul dışında üzerinde çalıştığım iki ana şey yazma ve programlamaydı. Makaleler yazmadım. O zamanlar yeni başlayan yazarların yazması gerekenleri yazdım ki muhtemelen hâlâ böyledir: kısa hikayeler. Hikayelerim korkunçtu (awful). Neredeyse hiçbir olay örgüleri yoktu, sadece derin olduklarını hayal ettiğim, güçlü hislere sahip karakterler vardı.


Yazmayı denediğim ilk programlar, okul bölgemizin o zamanlar "veri işleme" (data processing) olarak adlandırılan şey için kullandığı IBM 1401 üzerindeydi. Bu 9. sınıftaydı, yani 13 veya 14 yaşındaydım. Okul bölgesinin 1401'i tesadüfen (happened to) ortaokulumuzun bodrum katındaydı ve arkadaşım Rich Draves ile birlikte kullanma iznimiz vardı. CPU, disk sürücüleri, yazıcı, kart okuyucu (card reader) gibi tüm bu uzaylı görünümlü (alien-looking) makinelerin parlak floresan ışıklar altındaki yükseltilmiş bir zeminde durduğu, mini bir Bond kötü adamının sığınağı (lair) gibi hissediliyordu.


Kullandığımız dil Fortran'ın eski bir sürümüydü. Programları delikli kartlara (punch cards) yazmanız, ardından bunları kart okuyucuya istiflemeniz ve programı belleğe (memory) yüklemek ve çalıştırmak için bir düğmeyi basmanız gerekiyordu. Sonuç genellikle olağanüstü gürültülü (spectacularly loud) yazıcıda bir şeyler yazdırmaktan ibaret olurdu.


1401 kafamı karıştırmıştı (puzzled). Onunla ne yapacağımı tam olarak bir türlü çözemiyordum. Ve geriye dönüp baktığımda da, hakikatte de zaten elimden gelen çok bir şey de yoktu denebilir. Programlara (veri olarak yapılabilecek) tek veri girişi "delinmiş kağıt kartları" (punch cards) halindeydi lakin delinmiş kağıtlar bünyesinde elimde olan bir verim yoktu. Diğer yegâne opsiyonum hiçbir veriye bağımlı olmayan pi (pi sayıları) hesaplamaları yapmaktan öteye gitmemekteydi. Lakin bu kapsamdaki çekici/cezbeden türden görevleri üstlenmek için yeterli seviyede matematik bilgim bulunmuyordu. Bu sebeple yazdığım kod satırlarını dahi (programları) hiç hatırlayamıyor olmam beni kesinlikle hiç şaşırtmıyor, çünkü eyleme geçirebilecekleri kayda ve tabana değer özellikleri bulunmuyordu. Olan en berrak ve sarih hatıram ise; yazdığım kodların bittiğine dair programın işleyişi hakkında emin olduğum anda, programlarımdan birinin duraklama ve (terminate) işlemini bitirme serüveni tamamlanmadığında elde ettiğim sonlanmaması gerçeğidir. Bir zaman paylaşımlı (time-sharing) sunucusu olmayan ve eş zamanlı işlem yürütemeyen tek kanallı makinede/bilgisayarda (machine without time-sharing) hatayla sonlandırılmış bir döküm çıktısında olan; veri merkezi görevlisinin (data center manager) anında yüzünden anladığım hal; bunun, teknik değil sadece kurumsal bir çöküntü oluşuydu.


Mikrobilgisayarlarla ise tüm yapılar ve bakış açısı bütünüyle boyut değiştirdi. Yalnızca kurguyu besleyerek ve duraksamasını beklemeden de bir yığın (stack of punch cards) zımba kartı destesine girmeden evvel bizzat masanızda oturan; verinize ve tüm girdilerinize bir anda aksiyonel cevap üretebilen komputere (bilgisayara) sahip olma imkânına sahip oldunuz. [1]


Arkadaşlarımdan mikrobilgisayar sahibi olan ilk kişi, cihazı bizzat kendi donanımıyla (kendi marifetiyle) (built it himself) dizayn etmişti. Bu bilgisayar yapısı doğrudan Heathkit aracılığıyla, donanımsal yapısı kurgulanabilir (sold as a kit by) bir platform dahilindeydi. Sisteme yerleştirilen metin yapısı aracılığıyla ve bizzat kendi kodunu girmesi aşamasında onu ve olan biteni takip etmem esnasında ne kadar heyecan duyduğumu ve kendisini kıskandığımı hâlâ tüm şeffaflığıyla (vividly) anımsıyorum (I remember vividly).


O yıllarda bilgisayar formatları (sistemleri) fazlasıyla paha ve maddi bir külfet (expensive) değerindeydi. Ancak yaklaşık 1980 tarihinde; uzun aylar/seneler süren telkinlerin/baskıların sonrasında babamı bir 'TRS-80' almaya ikna dahi etsem de kendimi geliştirmeye başladım. Gerçi dönem standartları için, (the gold standard then) tam bir Altın Standard formu da 'Apple II' idi ama yine de bu format ('TRS-80') sistem de benim için kâfi ve çalışabileceğim nitelikteydi. Kendi asıl odak serüvenimin dahi aslında bir çerçevede tam da burada şahlandığını (başladığını) söylemeliyim. (Basit yapı kodlamaları) Örneğin ilk süreçte kimi basit oyunlar yazdım (I wrote simple games), akabinde roket tasarım test modelleri baz alarak, kendi minyatür modellerimin/roketlerimin çıkabileceği maksimum irtifayı ve test aşamalarını öngörebilecek spesifik kodlamalardan (a program to predict how high my model rockets would fly), ki o süreçte bunları çok mühim detay ve olaylar bütünü kabul ediyorum; babamın bile kullanıp en son kitap evresi noktasında işine koşan/kullandığı en az bir kitabı barındıran; spesifik bir de kelime döküm dosyası yazdım (word processor). Bir veri ve donanım belleği üzerinden işlenerek yalnız 2 civarı kitap yaprağı metin döküm hafızasını bünyesine alan komputerde her biri takribi iki sayfayı işleyerek ilerlettiği baskıları basarak işlemi sonlandırabilsin ama, bir klasik el ve tuş makinesine da kıyasla evvelden her şeye bedel ve paha biçilemez bir imkana sahiptir (but it was a lot better than a typewriter).


Bilhassa her şeye karşın programlamayı ziyadesiyle de sevsem, bir vakit ne yalan söyleyeyim ki ilk ve öncelikli öğrenim kararlarım dahi programlama ekseninde ilerlemiyordu (Though I liked programming, I didn't plan to study it in college.). Tüm ciddiyet, gerçeklik (felsefe - philosophy) arayışımın saf bir getirisi olarak üniversite tahsilimde her süreçte bir tık ve gömlek de üstünlüğünün etkisinde, dâir olana (to be the study of the ultimate truths); yani diğer donanımları çok daha ehemmiyetli bir seviyenin basamağında geride hissettiren asıl bilgi/hakikat evrenine tutkuluyum sanıyordum. Neticesinde liseden kalan tüm hamasi hayallere değmiş olacak mıydı diye sormanıza kalmadan da üniversite hayatımın (got to college) akışında öğrendim; tüm kavramsal alana yayılan her felsefe dalının (her o ilmi disiplinin alt metni de diyebilirsiniz) zaten o gerçeği savunan (ultimate truths) yapısının (space of ideas) dar ve sığ olduğuydu. Haliyle artık kendisini hissettiren saf gerçekleri savunarak tüm bu alanı boş (left for philosophy were edge cases) ve anlamsız bıraktığını keşfetmiştim...


Esasen sadece on sekiz (18) yaşım dahilindeyken kendi düşünce bulutlarımda bunu tanımlayıp size aktarabilme imkânına sahip olmadığımdan (I couldn't have put this into words when I was 18) dahi bunu ilk defa o an; ama ancak yine derste (felsefede) canımın ciddi oranda (boring) da sıkılmasının bir eyleme de taşmasıyla kararlarımı tazeleyerek fark etmiş oldum. Bu andan kelli en sonunda zihnimi AI - (Yapay zeka) üzerine çevrildim ve kendime farklı bir macera, taban buldum.


Zaten; 1980 senesinin o dönemki ortaları; havanın, atmosferin bizzat o en AI'a ve rüzgâra eğilim evreleri de denilebilirdi. Lakin spesifik ölçekte AI mecrasını ve kendisini bir meslek / gelecek odaklı kılan esas olay ise bilhassa Mike isminde fütüristik bilgisayar odaklı (intelligent computer) akıl / zekâ ile yazılan The Moon is a Harsh Mistress adeta; Heinlein serisi kurgusal/roman eseri idi ve bir nevi Winograd ile bir simülasyon olarak SHRDLU formunun yayınlandığı PBS belgeselini (PBS documentary) beraber gördüğüm ana rastlar. Gerçi aradan ne kadar zaman aksın; lakin hala eseri dönüp okuma veya şahit olduklarımdan ders çıkartma arayışımlarımı düşününce "eserin/kitabın aradan bunca vakit aksa dahi eskidiğini vs. hissettim mi?" (aged) net demem zor elbet de. Ne var ne yok tam olarak kitabı tecrübe edinerek o anki dünyasına adeta gömüldüğüm de en saf ve bir o kadar en yalın gerçeğim/safhalarımdır (I was drawn entirely into its world.). En nihayetinde o form yapıya eninde sonunda zaten illa bir gün varacağımız belli ve aniden benim nazarımda Winograd sunumlarına ve bilhassa SHRDLU modülü esasına şahitliğim ise tam bu öngörülerin son kertelerine ulaşıp birkaç yıla buraların tamamen evrileceğine/geleceğine dayandığıydı (Winograd using SHRDLU, it seemed like that time would be a few years at most.). 
```

**Özel gömme / ekleme (custom embedding) dizesiyle beraber (string) İndeks Sorgulama (Query Index)**

```python
from llama_index.core import QueryBundle
```

```python
query_bundle = QueryBundle(
    query_str="Yazar büyürken neler yaptı?",
    custom_embedding_strs=["Yazar resim yaparak büyüdü."],
)
query_engine = index.as_query_engine()
response = query_engine.query(query_bundle)
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Mevcut (sunulan) bağlam (context), yazarın büyürken ne yaptığına dair herhangi bir bilgi (information) vermiyor (sağlamaz).**

**Maksimum marjinal (marginal) alaka düzeyini (relevance) (MMR) kullanma**

Vektörleri salt/sadece benzerliğe göre sıralamak (ranking) yerine, halihazırda bulunanlarla benzer belgelere ceza/yaptırım (penalizing documents) uygulayarak, [MMR](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf) temel alınmak (based on) suretiyle belgelere çeşitlilik (diversity) kazandırır. Daha düşük bir mmr\_eşiği (mmr\_threshold) uygulanırsa, bu ayar çeşitliliği büyük bir düzeyde artırır.

```python
query_engine = index.as_query_engine(
    vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.2}
)
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

#### Kaynakları/İçerikleri Elde Edin (Get Sources)

```python
print(response.get_formatted_sources())
```

```bash
> Source (Doc id: c4118521-8f55-4a4d-819a-2db546b6491e): Ne Üzerinde Çalıştım (What I Worked On)


Şubat 2021


Üniversiteden önce okul dışında üzerinde çalıştığım iki ana şey...


> Source (Doc id: 74f77233-e4fe-4389-9820-76dd9f765af6): Bu da; yapıları kullanımları itibariyle kolay formata çekmekle birlikte onları ucuza (inexpensive) tekabül ettirir anlamı/manasına da çıkıyordu. Esasen bir miktar (fukara) zengin değildik denebilir ama, bir bağlamda da...
```

#### Filtreler (Filters) Aracılığıyla İndeks Sorgulama (Query Index)

Sorgularımızı doğrudan meta verilerimizi (metadata) de hesaba alarak yapılandırabilir, aynı zamanda (we can also filter) da filtreleyebiliriz (elekten geçirebiliriz).

```python
from llama_index.core import Document


doc = Document(text="target", metadata={"tag": "target"})


index.insert(doc)
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
```

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="tag", value="target")]
)


retriever = index.as_retriever(
    similarity_top_k=20,
    filters=filters,
)


source_nodes = retriever.retrieve("Yazar büyürken neler yaptı?")
```

```bash
INFO:httpx:HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
HTTP İsteği (Request): POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
```

```python
# Her ne kadar tepe limit bandını (top k değerini) 20 belirlemiş olsak da; kodumuz spesifik olarak yine salt ana eylemi içeren bizim hedeflenen düğümü/veriyi (target node) geri getirir.
print(len(source_nodes))
```

```bash
1
```

```python
print(source_nodes[0].text)
print(source_nodes[0].metadata)
```

```bash
hedef (target)
{'tag': 'hedef (target)'}
```
