# Ollama LLM

---
title: Ollama LLM
 | LlamaIndex OSS Belgeleri
---

## Kurulum

İlk olarak, yerel bir Ollama örneği kurmak ve çalıştırmak için [readme](https://github.com/jmorganca/ollama) sayfasındaki adımları izleyin.

Ollama uygulaması yerel makinenizde çalışırken:

- Tüm yerel modelleriniz otomatik olarak `localhost:11434` adresinden sunulur.
- Modelinizi `llm = Ollama(..., model="<model_adı>")` şeklinde ayarlayarak seçin.
- Gerektiğinde `Ollama(..., request_timeout=300.0)` ayarıyla varsayılan zaman aşımı süresini (30 saniye) artırın.
- Versiyon belirtmeden `llm = Ollama(..., model="<model_ailesi>")` ayarlarsanız, sistem doğrudan en son (latest) sürümü arayacaktır.
- Varsayılan olarak, modeliniz için maksimum bağlam penceresi (context window) kullanılır. Bellek kullanımını sınırlamak için `context_window` değerini manuel olarak ayarlayabilirsiniz.

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-ollama
```

```python
from llama_index.llms.ollama import Ollama
```

```python
llm = Ollama(
    model="llama3.1:latest",
    request_timeout=120.0,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)
```

```python
resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

```text
Paul Graham, İngiliz-Amerikan kökenli bir girişimci, programcı ve yazardır. Teknoloji endüstrisinde önde gelen bir figürdür ve özellikle girişimcilik, programlama ve kültür üzerine yaptığı analizlerle tanınır.

Paul Graham hakkındaki bazı temel bilgiler şunlardır:

1. **Y Combinator'ın Kurucusu**: 2005 yılında Graham, erken aşamadaki şirketlere tohum sermayesi sağlayan bir startup hızlandırıcı programı olan Y Combinator'ı (YC) kurdu. YC o zamandan beri dünyanın en başarılı ve etkili startup hızlandırıcılarından biri haline geldi.
2. **Başarılı Girişimci**: YC'yi kurmadan önce Graham, eBay satıcıları için bir çevrimiçi mağaza geliştiren Viaweb (2000 yılında Yahoo! tarafından satın alındı) ve PCGenie (Apple'a satıldı) dahil olmak üzere birçok başarılı startup kurmuştu.
3. **Yazar ve Denemeci**: Graham, girişimcilik, programlama ve teknoloji kültürü gibi konularda paulgraham.com adresinde yayınlanan çok sayıda deneme yazmıştır. Yazıları genellikle iş dünyası, teknoloji ve insan davranışının kesişim noktalarını inceler.
4. **Startup Topluluğunda Düşünce Lideri**: Y Combinator ve yazıları aracılığıyla Graham, girişimciler, yatırımcılar ve programcılar arasında saygın bir düşünce lideri haline gelmiştir. Başarılı bir şirket kurma konusundaki doğrudan tavsiyeleri ve teknoloji endüstrisinin çeşitli yönlerine yönelik eleştirileriyle tanınır.
5. **Eğitim ve Geçmiş**: Paul Graham, lisans derecesini Cambridge Üniversitesi'nde felsefe alanında almış ve daha sonra bilgisayar bilimleri üzerine çalıştığı Harvard Üniversitesi'ne devam etmiştir.

Graham, startup dünyasının en etkili isimlerinden biri olarak kabul edilir; birçok girişimci ve yatırımcı, başarılı şirketlerin nasıl kurulacağı konusunda ondan rehberlik beklemektedir.
```

#### Bir mesaj listesiyle `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

```text
assistant: Adımı mı merak ediyon, ha? Bak hele dostum, ben Kaptan Calico Jack "Kara Gaga" McCoy'um, Yedi Denizler'de bugüne kadar yelken açmış en azılı korsan! *göz bandını düzeltir*

Gemim "Maverick'in İntikamı", üç direkli ve kömür kadar siyah gövdeli, sağlam bir kalyondur. O benim evim, en iyi dostum ve engin denizlerdeki zenginliğe ve maceraya giden biletimdir!

Ve sadık papağan ortağım Polly'yi de sakın unutma! Gemimize fazla yaklaşan her kara yağızına deniz türküleri söyler ve hakaretler yağdırır. *göz kırpar*

Eee, seni bu sulara hangi rüzgar attı? Gömülü bir hazine mi arıyon, yoksa sadece benim denizlerdeki maceralarımı mı dinlemek istersin?
```

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = llm.stream_complete("Paul Graham kimdir?")
```

```python
for r in response:
    print(r.delta, end="")
```

```text
Paul Graham, İngiliz-Amerikan bir programcı, yazar ve girişimcidir. En çok, 2005 yılında dünyanın en başarılı ve etkili startup hızlandırıcılarından biri haline gelen çevrimiçi startup hızlandırıcısı Y Combinator'ı (YC) kurmasıyla tanınır.

Graham, 1964 yılında Cambridge, İngiltere'de doğdu. Durham Üniversitesi'nde felsefe okudu ve daha sonra programcı olarak çalışmak üzere Amerika Birleşik Devletleri'ne taşındı. 1990'ların başında, 2002 yılında 1,5 milyar dolara eBay tarafından satın alınan Viaweb (daha sonra adı PayPal olarak değiştirildi) dahil olmak üzere birkaç startup kurdu.

2005 yılında Graham, girişimci arkadaşları Ron Conway ve Robert Targ ile birlikte Y Combinator'ı kurdu. Hızlandırıcının amacı, erken aşamadaki startuplara fon, mentorluk ve ağ oluşturma fırsatları sunarak başarılı olmalarına yardımcı olmaktır. Yıllar içinde YC, Dropbox, Airbnb, Reddit ve Stripe gibi önemli başarılar dahil olmak üzere 2.000'den fazla şirkete yatırım yaptı.

Graham aynı zamanda teknoloji, girişimcilik ve iş dünyası ile ilgili konularda üretken bir yazar ve blog yazarıdır. Denemeleri çevrimiçi ortamda yaygın olarak okunmuş ve paylaşılmıştır; teknoloji endüstrisi hakkındaki anlayışlı yorumlarıyla tanınır. En popüler denemelerinden bazıları "Startup Tavsiyelerinin 4 Türü" ve "Yapmış Olmayı Dileyeceğiniz Şeyler"dir.

Y Combinator ile yaptığı çalışmaların yanı sıra Graham; programlama, iş dünyası ve felsefe üzerine birkaç kitap da yazmıştır. Konferanslarda ve etkinliklerde aranan bir konuşmacıdır ve teknoloji endüstrisine katkılarından dolayı takdir edilmiştir.

Genel olarak Paul Graham, girişimci ruhu, anlayışlı yazıları ve erken aşamadaki şirketlerin başarılı olmasına yardımcı olma konusundaki kararlılığıyla tanınan, startup dünyasında saygın bir figürdür.
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```text
Vay canına! Benim adım Kaptan Pala "Kara Yürek" McCoy, Yedi Denizler'de yelken açmış, hem korkulan hem de saygı duyulan en büyük korsan! *bandanasını düzeltir*

Gemim "Maverick'in İntikamı" benim canım evimdir ve mürettebatım "Kargaşa Takımı" ganimet ve yağma peşindeki sadık dostlarımdır! Hazine, macera ve güzel bir kadeh içki bulmak için denizlerde fırtına gibi eseriz!

Eee, seni bu sulara hangi rüzgar attı? Korsan gibi şatafatlı bir vakit mi geçirmek istiyon, yoksa kayıp papağanın Polly'yi nasıl bulacağını mı merak ediyon?
```

## JSON Modu

Ollama ayrıca, tüm yanıtların geçerli JSON olmasını sağlamaya çalışan bir JSON modunu da destekler.

Bu, özellikle yapılandırılmış çıktıları ayrıştırması gereken araçları çalıştırmaya çalışırken çok kullanışlıdır.

```python
llm = Ollama(
    model="llama3.1:latest",
    request_timeout=120.0,
    json_mode=True,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)
```

```python
response = llm.complete(
    "Paul Graham kimdir? Yapılandırılmış bir JSON nesnesi olarak çıktı ver."
)
print(str(response))
```

```json
{ 
  "name": "Paul Graham",
  "occupation": ["Bilgisayar Programcısı", "Girişimci", "Risk Sermayedar"],
  "bestKnownFor": ["Y Combinator (YC) Kurucu Ortağı", "Hacker News'in Yaratıcısı"],
  "books": ["Hackers & Painters: Big Ideas from the Computer Age", "The Lean Startup"],
  "education": ["University College London (UCL)", "Harvard University"],
  "awards": ["PC Magazine Yılın Programcısı ödülü"],
  "netWorth": ["yaklaşık 500 milyon dolar olduğu tahmin ediliyor"],
  "personalWebsite": ["https://paulgraham.com/"] 
}
```

## Yapılandırılmış Çıktılar

Yapılandırılmış çıktıları garanti altına almak için LLM'ye bir Pydantic sınıfı da ekleyebiliriz. Bu, verilen bir Pydantic sınıfı için Ollama'nın yerleşik yapılandırılmış çıktı yeteneklerini kullanacaktır.

```python
from llama_index.core.bridge.pydantic import BaseModel


class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı."""

    name: str
    artist: str
```

```python
llm = Ollama(
    model="llama3.1:latest",
    request_timeout=120.0,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)


sllm = llm.as_structured_llm(Song)
```

```python
from llama_index.core.llms import ChatMessage


response = sllm.chat([ChatMessage(role="user", content="Rasgele bir şarkı adı söyle!")])
print(response.message.content)
```

```json
{"name":"Hey Ya!","artist":"OutKast"}
```

Veya asenkron (async) ile:

```python
response = await sllm.achat(
    [ChatMessage(role="user", content="Rasgele bir şarkı adı söyle!")]
)
print(response.message.content)
```

```json
{"name":"Mr. Blue Sky","artist":"Electric Light Orchestra (ELO)"}
```

Yapılandırılmış çıktıları akış yöntemiyle de alabilirsiniz! Yapılandırılmış bir çıktının akışı, normal bir dizenin akışından biraz farklıdır. En güncel yapılandırılmış nesneyi üreten bir üreteç (generator) sunacaktır.

```python
response_gen = sllm.stream_chat(
    [ChatMessage(role="user", content="Rasgele bir şarkı adı söyle!")]
)
for r in response_gen:
    print(r.message.content)
```

```json
{"name":null,"artist":null}
{"name":null,"artist":null}
{"name":null,"artist":null}
{"name":null,"artist":null}
{"name":null,"artist":null}
{"name":"","artist":null}
{"name":"Mr","artist":null}
{"name":"Mr.","artist":null}
{"name":"Mr. Blue","artist":null}
{"name":"Mr. Blue Sky","artist":null}
{"name":"Mr. Blue Sky","artist":null}
{"name":"Mr. Blue Sky","artist":null}
{"name":"Mr. Blue Sky","artist":null}
{"name":"Mr. Blue Sky","artist":null}
{"name":"Mr. Blue Sky","artist":null}
{"name":"Mr. Blue Sky","artist":""}
{"name":"Mr. Blue Sky","artist":"Electric"}
{"name":"Mr. Blue Sky","artist":"Electric Light"}
{"name":"Mr. Blue Sky","artist":"Electric Light Orchestra"}
{"name":"Mr. Blue Sky","artist":"Electric Light Orchestra"}
{"name":"Mr. Blue Sky","artist":"Electric Light Orchestra"}
```

## Çok Modlu (Multi-Modal) Desteği

Ollama, çok modlu modelleri destekler ve Ollama LLM sınıfı, görüntüleri doğrudan destekler.

Bu özellik, chat mesajlarının içerik blokları (content blocks) özelliğinden yararlanır.

Burada, bir görüntü hakkındaki soruyu yanıtlamak için `llama3.2-vision` modelini kullanıyoruz. Eğer bu modele henüz sahip değilseniz, `ollama pull llama3.2-vision` komutunu çalıştırmanız gerekecektir.

```bash
!wget "https://pbs.twimg.com/media/GVhGD1PXkAANfPV?format=jpg&name=4096x4096" -O ollama_image.jpg
```

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.ollama import Ollama


llm = Ollama(
    model="llama3.2-vision",
    request_timeout=120.0,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)


messages = [
    ChatMessage(
        role="user",
        blocks=[
            TextBlock(text="Bu ne tür bir hayvandır?"),
            ImageBlock(path="ollama_image.jpg"),
        ],
    ),
]


resp = llm.chat(messages)
print(resp)
```

```text
assistant: Görüntüde, VR gözlüğü ve kulaklık takmış, önünde Google logosu belirgin bir şekilde duran çizgi film karakteri bir alpaka tasvir ediliyor. Alpaka, kendine özgü uzun boynu, yumuşak yünü ve başına tünenmiş VR gözlüğüyle karakterize edilmiştir. Ayrıca gözlüklere bağlı bir kulaklık seti ile donatılmıştır. Alpakanın vücudu, Google markasının yaygın bir görsel temsili olan bir bulut şeklinde temsil edilmiştir. Görüntünün genel tasarımı oyuncu ve esprilidir; alpakanın VR gözlükleri ve kulaklıkları ona fütüristik ve teknoloji meraklısı bir görünüm kazandırmaktadır.
```

Yeterince yakın ;)

## Düşünme (Thinking)

Ollama'daki modeller "düşünme" özelliğini destekler; yani nihai bir yanıt döndürmeden önce bir yanıt üzerinde akıl yürütme ve yansıtma süreci.

Aşağıda, `thinking` parametresini ve `qwen3:8b` modelini kullanarak hem akış hem de akış olmayan modlarda Ollama modellerinde düşünmenin nasıl etkinleştirileceği gösterilmektedir.

```python
from llama_index.llms.ollama import Ollama


llm = Ollama(
    model="qwen3:8b",
    request_timeout=360,
    thinking=True,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)
```

```python
resp = llm.complete("434 / 22 kaç eder?")
```

```python
print(resp.additional_kwargs["thinking"])
```

```text
Pekala, 434 bölü 22'nin kaç olduğunu bulmam gerekiyor. Bölme işleminin nasıl çalıştığını hatırlayarak başlayayım. Büyük bir sayıyı daha küçük bir sayıya bölmek bazen zor olabilir, özellikle de sayılar birbirinin katı olmadığında. Bakalım... Belki burada uzun bölme kullanabilirim.

Öncelikle 22'nin 434'e tam olarak bölünüp bölünmediğini veya kalan olup olmadığını kontrol etmeliyim. Adım adım yazayım.

434'ün ilk basamağı olan 4 ile başlayalım. Ancak 22, 4'ten büyüktür, bu yüzden 22'yi 4'e bölemem. Sonra ilk iki basamağı yani 43'ü alırım. Şimdi 22, 43'ün içinde kaç kez var? Bir düşüneyim. 22 kere 1, 22 eder ve 22 kere 2, 44 eder. Aa, 44 çok büyük çünkü 44, 43'ten fazla. Yani 22, 43'ün içinde bir kez var.

Böylece bölümün ilk basamağına 1 yazıyorum. Sonra 1'i 22 ile çarpıyorum, bu da 22 eder. Bunu 43'ten çıkarıyorum ve 43 - 22 = 21 elde ediyorum.

Şimdi 434'ten bir sonraki basamağı yani 4'ü aşağı indiriyorum. Yani şimdi yeni sayı 214 oldu. Dur bir saniye, 4'ü aşağı indirdikten sonra 214 mü oluyor? Bir kontrol edeyim. Orijinal sayı 434. İlk iki basamağı 43 olarak aldıktan sonra 22'yi çıkarırsak 21 kalır, sonra 4'ü aşağı indirmek onu 214 yapar. Evet, doğru.

Şimdi 22, 214'ün içinde kaç kez var? Hesaplayayım. 22 kere 9, 198 eder ve 22 kere 10, 220 eder. 220, 214'ten büyüktür, yani 9 kez var.

Böylece bölümdeki 1'in yanına 9 yazıyorum ve 19 oluyor. 9'u 22 ile çarpıyorum: 9*20 = 180 ve 9*2 = 18, yani toplam 198. Bunu 214'ten çıkarıyorum: 214 - 198 = 16.

Artık aşağı inecek basamak kalmadı, bu yüzden bölmeye devam etmek için bir ondalık virgül ve bir sıfır ekliyoruz. Yani 16,0 elde ettik.

Şimdi 22, 160'ın içinde kaç kez var? Bakalım. 22*7 = 154 ve 22*8 = 176. 176 çok büyük, yani 7 kez var.

7'yi 22 ile çarpalım: 7*20=140, 7*2=14, toplam 154. Bunu 160'tan çıkaralım: 160 - 154 = 6.

Yine bir sıfır indirelim, 60 olsun. Şimdi 22, 60'ın içinde iki kez var (22*2=44). 60'tan 44 çıkaralım: 60 - 44 = 16.

Bir dakika, bu kalanı daha önce görmüştüm. İlk adımdan sonra 16 kalmıştı ve şimdi yine 16 kaldı. Bu, ondalık kısmın tekrarlamaya başlayacağı anlamına gelir.

Yani hepsini bir araya getirirsek, bölüm 19.72... ve bu desen tekrar edecek. Yani ondalık genişleme 19.727272... şeklindedir ve "72" kısmı devretmektedir.

Doğru olup olmadığını doğrulayayım. 22'yi 19.727272... ile çarparsam 434 eder mi? Bir bakayım.

Önce 22 * 19 = 418. Sonra 22 * 0.727272... Bunu hesaplayayım.

0.727272... devirli sayısı 72/99 ile aynıdır, bu da 8/11'e basitleşir. Yani 22 * (8/11) = (22/11)*8 = 2*8 = 16.

Dolayısıyla, 22*(19 + 8/11) = 22*19 + 22*(8/11) = 418 + 16 = 434. Mükemmel, bu tam tutuyor.

Böylece 434'ün 22'ye bölünmesi, 16 kalanla birlikte 19'dur veya ondalık olarak yaklaşık 19.727272... (devirli).

Alternatif olarak, eğer kesir olarak yazmak istersem, 434 bölü 22 sadeleştirilebilir. Bakalım 434 ile 22'nin ortak bir böleni var mı?

Önce 22'yi çarpanlarına ayıralım: 2*11. 434'ün 2'ye bölünüp bölünmediğini kontrol edelim. Evet, çünkü çift bir sayıdır. 434 bölü 2, 217 eder. Sonra 217'nin 11'e bölünüp bölünmediğini kontrol edelim. 11*19 = 209 ve 11*20 = 220. Yani 217 - 209 = 8, bu yüzden bölünemez. Dolayısıyla sadeleşmiş kesir 217/11'dir.

Bekle, 434 bölü 2 = 217 ve 22 bölü 2 = 11. Yani evet, 434/22 kesri 217/11'e sadeleşir.

Tam sayılı kesir olarak yazarsak, 11'e bölünen 217, 8 kalanla birlikte 19 eder.

Bu nedenle cevap 19 tam 8/11'dir veya yaklaşık 19.7272... (devirli).

Ancak soru sadece 434 / 22'yi istiyor. Cevabın nasıl istendiğine bağlı olarak, kesir, ondalık veya tam sayılı kesir olarak sunulabilir. Kullanıcı belirtmediği için çoğu durumda, aksi söylenmedikçe, devirli gösterimle ondalık vermek uygun olabilir. Ancak bazen kesirler tercih edilir.

Alternatif olarak, tam değeri istiyorlarsa, 217/11 kesri tamdır ve ondalık sayı devirlidir.

Doğru olduğundan emin olmak için hesaplamalarımı tekrar kontrol edeyim.

Önce 22*19 = 418. 434 - 418 = 16. Yani kalan 16. Dolayısıyla 434/22 = 19 + 16/22. 16/22'yi pay ve paydayı 2'ye bölerek sadeleştirelim: 8/11. Yani 19 tam 8/11.

Evet, bu doğru. Tam değer 19 tam 8/11'dir, bu da yaklaşık 19.727272...'ye eşittir.

Alternatif olarak, ondalık sayı olarak istenirse 19.727272...'dir ve "72" devretmektedir.

Yani sanırım cevap ya 19.7272... ya da 19 tam 8/11. İstenen formata göre değişir.

Kullanıcı "434 / 22 kaçtır?" diye sorduğuna ve bir format belirtmediğine göre, sanırım her ikisini de sunmalıyım, ancak belki kesir daha hassastır. Yine de ondalık sayı devirliyse kabul edilebilir.

Özetle cevap, 72'nin üzerinde çizgi olan 19.7272...'dir.

Sonuç olarak cevap 217/11 veya yaklaşık 19.7272...'dir.

Adımları teyit etmek için bölme işlemini bir kez daha yapayım.

434'ü 22'ye bölelim:

43'te (ilk iki basamak) 22, 1 kez var, 1*22=22, 43'ten çıkarınca 21 kalır. 4'ü indirip 214 yapalım.

214'te 22, 9 kez var (çünkü 22*9=198), 214'ten 198 çıkarınca 16 kalır. Bir 0 ekleyip 160 yapalım.

160'ta 22, 7 kez var (22*7=154), 160'tan 154 çıkarınca 6 kalır. Bir 0 ekleyip 60 yapalım.

60'ta 22, 2 kez var (22*2=44), 60'tan 44 çıkarınca 16 kalır. Tekrar 160 yapmak için bir 0 ekleyelim.

Şimdi desenin kendini tekrar ettiğini görüyoruz: 160, 154, kalan 6, sonra 60, 44, kalan 16, sonra tekrar 160... Yani ondalık sayı her iki basamakta bir kendini tekrar ediyor: 72.

Dolayısıyla ondalık sayı 19.727272...'dir, yani 19.72 devirlidir.

Bu nedenle, kutulu biçimde şunlar olabilir: ondalık olarak \boxed{19.\overline{72}} veya kesir olarak \boxed{\dfrac{217}{11}}.

Her iki form da doğrudur. Kullanıcı bir ondalık bekliyor olabilir ancak matematiksel bağlamlarda kesirler tamlık açısından genellikle tercih edilir.

Karar vermek için 434/22'nin daha fazla sadeleştirilip sadeleştirilemeyeceğine bakayım. 217 ve 11'in ortak çarpanı olmadığına göre (11 asal bir sayıdır ve 217'yi bölmez), kesir en sade halindedir.

Dolayısıyla, cevap 217/11'dir ve \boxed{\dfrac{217}{11}} olarak yazılabilir.
```

```python
print(resp.text)
```

```text
434 / 22 bölme işlemini çözmek için önce kesri sadeleştirerek başlayalım.

---

### **Adım 1: Kesri Sadeleştirme**

Hem 434 hem de 22, 2'ye tam bölünür:

$$
\frac{434}{22} = \frac{434 \div 2}{22 \div 2} = \frac{217}{11}
$$

217 / 11 kesri en sade halindedir çünkü 11 asal bir sayıdır ve 217'yi tam bölmez (11 × 19 = 209 ve 217 − 209 = 8).

---

### **Adım 2: Tam Sayılı Kesre Dönüştürme (İsteğe Bağlı)**

217 / 11'i tam sayılı kesir olarak da ifade edebiliriz:

- 217'yi 11'e bölün: 217 / 11 = 19 ve kalan 8'dir.
- Dolayısıyla: $\frac{217}{11} = 19 \frac{8}{11}$

---

### **Adım 3: Ondalık Sayıya Dönüştürme (İsteğe Bağlı)**

217 / 11'i ondalık sayıya dönüştürürsek:

$$
\frac{217}{11} = 19.727272\ldots
$$

Bu, "72" kısmının sonsuza kadar tekrar ettiği devirli bir ondalık sayıdır. Bunu şu şekilde gösterebiliriz:

$$
19.\overline{72}
$$

---

### **Nihai Cevap**

Soru ucu açık olduğundan ve bir format belirtmediğinden, en kesin ve tercih edilen form **kesir** halidir:

$$
\boxed{\dfrac{217}{11}}
$$
```

Bu gerçekten çok fazla düşünme!

Şimdi, beklemeyi daha az zahmetli hale getirmek için bir akış (streaming) örneği deneyelim:

```python
resp_gen = llm.stream_complete("434 / 22 kaç eder?")


thinking_started = False
response_started = False


for resp in resp_gen:
    if resp.additional_kwargs.get("thinking_delta", None):
        if not thinking_started:
            print("\n\n-------- Düşünme: --------\n")
            thinking_started = True
            response_started = False
        print(resp.additional_kwargs["thinking_delta"], end="", flush=True)
    if resp.delta:
        if not response_started:
            print("\n\n-------- Yanıt: --------\n")
            response_started = True
            thinking_started = False
        print(resp.delta, end="", flush=True)
```

```text
-------- Düşünme: --------


Pekala, 434 bölü 22'nin kaç olduğunu bulmam gerekiyor. Bölme işleminin nasıl çalıştığını hatırlayarak başlayayım. Bir sayıyı diğerine bölmenin, bölenin bölünene kaç kez sığdığını bulmak anlamına geldiğini biliyorum. Bu durumda bölen 22 ve bölünen 434'tür.

Öncelikle bu bölme işlemini basitleştirmeyi deneyebilirim. Her iki sayının ortak bir çarpana bölünüp bölünemeyeceğini kontrol edeyim. 22 ve 434'ün herhangi bir ortak çarpanı olup olmadığına bakalım. 22'nin asal çarpanları 2 ve 11'dir. 434'ün 2'ye bölünüp bölünmediğini kontrol edeyim. Evet, çünkü 434 çift bir sayıdır. 434'ü 2'ye bölmek bana 217 verir. Yani hem payı hem de paydayı 2'ye bölersem, problem 217 bölü 11 haline gelir. Bu daha kolay halledilebilir.

Şimdi 217'yi 11'e bölmem gerekiyor. Bunu adım adım yapayım. 11, 21'in içine kaç kez girer? Pekala, 11 kere 1, 11'dir ve 11 kere 2, 22'dir; bu da çok fazla olur. Yani 1 kez. 21'den 11 çıkaralım, 10 kalır. Sayının 7 olan bir sonraki basamağını indirelim, 107 olsun. Şimdi 11, 107'nin içine kaç kez girer? Hesaplayayım: 11 kere 9, 99'dur ve 11 kere 10, 110'dur; bu da çok büktür. Yani 9 kez. 107'den 99 çıkaralım, 8 kalır.

Böylece bunu bir araya getirirsek, 217 bölü 11, 8 kalanla birlikte 19 olur. Dolayısıyla 217/11, 19 tam 8/11'e eşittir. Ama bekle, orijinal problemi pay ve paydayı 2'ye bölerek basitleştirdiğim için, orijinal bölme işleminin 434 bölü 22 olduğunu ve bunun (217/11) ile aynı olduğunu unutmamalıyım. Dolayısıyla sonuç 19 tam 8/11'dir.

Ancak hata yapmadığımdan emin olmak için bu bölme işlemini başka bir yolla daha kontrol etmeliyim. 434 bölü 22'yi doğrudan uzun bölme ile deniyeyim.

434 ÷ 22 ile başlayalım. Önce 22'nin 43'ün içine kaç kez girdiğini belirleyelim. 22 kere 1, 22; 22 kere 2, 44; bu çok büyük. Yani 1 kez. 22'yi 1 ile çarpalım, 43'ten çıkaralım, 21 kalır. 4'ü aşağı indirelim, 214 olsun. Şimdi 22, 214'ün içine kaç kez girer? Hesaplayayım: 22 kere 9, 198; 22 kere 10, 220; bu çok büyük. Yani 9 kez. 22'yi 9 ile çarpalım, 198 olur. 214'ten çıkaralım, 16 kalır.

Yani bölme işlemi bana 16 kalanla birlikte 19 sonucunu verir. Ama bekle, pay ve paydayı 2'ye bölerek sadeleştirdiğimde 19 tam 8/11 bulmuştum. Ama burada doğrudan bölme bana 16 kalanla birlikte 19 sonucunu veriyor. Burada bir tutarsızlık var. Hangisi doğru?

Kontrol edeyim. 22 kere 19'u alırsam, 22*20=440 eksi 22 eder, bu da 418'dir. Sonra 434 - 418 = 16 eder. Yani 434 bölü 22, 16 kalanla birlikte 19'dur. Ama daha önce sadeleştirdiğimde bunun 19 tam 8/11 olduğunu düşünmüştüm. Bu, sadeleştirme adımımda hata yaptığım anlamına gelir. Geri döneyim.

Orijinal problem: 434 bölü 22. Pay ve paydayı 2'ye böldüm, 217 bölü 11 oldu. 217 bölü 11'i kontrol edeyim. 11*19 = 209. 217 - 209 = 8. Dolayısıyla 217/11, 19 tam 8/11'dir. Ancak doğrudan bölmeye göre 434/22, 16 kalanla birlikte 19'dur. Bekle, eğer 217 bölü 11'i (yani 19.818...) alırsam ve 434 bölü 22, 217 bölü 11 ile aynıysa, birbirlerine eşit olmaları gerekir. Ancak doğrudan bölmeye göre 434 bölü 22, 16 kalanla birlikte 19'dur; bu da 19 + 16/22 eder ve 19 + 8/11'e sadeleşir. Ah! Bekle, 16/22 kesri 8/11'e sadeleşir. Yani her iki yöntem de aynı sonucu veriyor. Yani 19 tam 8/11, yaklaşık 19.727 olan 19.727... ile aynıdır.

Yani ondalık formda 434 bölü 22. Bunu hesaplayayım. 22*19 = 418 ve 434 - 418 = 16 olduğuna göre, 16/22 değeri 0.727...'dir, yani ondalık sayı yaklaşık 19.727'dir.

Alternatif olarak, bunu bir ondalık sayı olarak yazmak istersem, 16 bölü 22 bölme işlemini gerçekleştirebilirim. Onu yapayım. 16 bölü 22. 16, 22'den küçük olduğu için ondalık basamaklar ekleyerek onu 0.727... olarak yazarız. 16,0 bölü 22. 22, 160'ın içine yedi kez girer (22*7=154), 160'tan 154 çıkaralım, 6 kalsın. 60 yapmak için bir sıfır indirelim. 22, 60'ın içine iki kez girer (22*2=44), 60'tan 44 çıkaralım, 16 kalsın. Tekrar 160 yapmak için bir sıfır indirelim. Bu döngü devam eder, yani 0.7272... olur, bu da devirli 0.727'dir. Dolayısıyla 434 bölü 22, 19.727... veya 19 tam 8/11'dir.

Yani teyit etmek gerekirse, her iki yöntem de aynı sonucu veriyor. Dolayısıyla cevap 19 tam 8/11 veya yaklaşık 19.727'dir.

Alternatif olarak, belli bir basamağa yuvarlanmış bir ondalık sayı olarak yazmak istersem, ancak soru bunu belirtmediği için tam kesir 19 tam 8/11 veya bileşik kesir olarak 217/11'dir. Ama 217 ve 11'in herhangi bir ortak çarpanı olup olmadığını kontrol edeyim. 11 asal bir sayıdır. 11*19 = 209, 11*20 = 220. 217-209=8, yani 217 sayısı 11*19 + 8'dir, dolayısıyla 11'e bölünemez. Bu nedenle 217/11 en sade halidir.

Sonuç olarak 434 bölü 22, 19 tam 8/11'dir veya yaklaşık 19.727'dir.

Bekle, başka bir yöntemle daha doğrulama yapmalıyım. Kontrol etmek için çarpma işlemini kullanayım. 19.727... ile 22'yi çarparsam 434 eder mi? 19.727 * 22 işlemini hesaplayayım.

Önce 19 * 22 = 418. Sonra 0.727 * 22. 0.727 * 22 hesaplayalım. 0.7 * 22 = 15.4 ve 0.027 * 22 = 0.594. Bunları birbirine eklersek 15.4 + 0.594 = 15.994 eder. Yani toplam 418 + 15.994 = 433.994'tür ve yuvarlama hatalarını hesaba katarsak yaklaşık 434 eder. Dolayısıyla bu tam uyuyor.

Alternatif olarak kesirleri kullanırsam: 19 tam 8/11 * 22. Bunu hesaplayalım. 19*22 + (8/11)*22. 19*22, 418 eder ve (8/11)*22, 8*2 = 16 eder. Yani toplam 418 + 16 = 434 eder. Mükemmel, bu tam uyuyor. Dolayısıyla kesin değer 19 tam 8/11'dir.

Bu nedenle cevap 19 tam 8/11 veya ondalık olarak yaklaşık 19.727'dir. Soru formatı belirtilmediği için fakat matematik problemlerinde aksi belirtilmedikçe genellikle tamlık açısından kesirler tercih edilir. Bu yüzden tam cevap 19 tam 8/11'dir, bu da bileşik kesir olarak 217/11 şeklinde yazılabilir.

Alternatif olarak, eğer ondalık istiyorlarsa yaklaşık 19.727...'dir. İstenen biçime göre değişir. Ancak orijinal sayılar tam sayı olduğu için kesirli form muhtemelen beklenen cevaptır.

Dolayısıyla, tüm bu kontrollerden sonra 434 bölü 22'nin 19 tam 8/11 olduğunu güvenle söyleyebilirim.


-------- Yanıt: --------


$ \frac{434}{22} $ işlemini çözmek için, doğruluğu sağlamak adına sadeleştirme ve doğrulama kullanarak adım adım ilerleyelim.

---

### Adım 1: Kesri Sadeleştirme

Hem payı hem de paydayı en büyük ortak bölenlerine (EBOB) bölerek kesri sadeleştirmeye başlıyoruz. 22 ve 434 çift sayı olduğundan her ikisi de 2'ye tam bölünür.

$$
\frac{434}{22} = \frac{434 \div 2}{22 \div 2} = \frac{217}{11}
$$

Şimdi $ \frac{217}{11} $ işlemini sadeleştirelim.

---

### Adım 2: Bölme İşlemini Gerçekleştirme

217'yi 11'e bölüyoruz:

- $ 11 \times 19 = 209 $
- $ 217 - 209 = 8 $

Sonuç şöyledir:

$$
\frac{217}{11} = 19 \text{ kalan } 8 = 19 \frac{8}{11}
$$

Bu, bölme işleminin **tam kesir formu**dur.

---

### Adım 3: Ondalık Sayıya Dönüştürme (İsteğe Bağlı)

$ 19 \frac{8}{11} $ değerini ondalık sayıya dönüştürmek için $ \frac{8}{11} $ değerini hesaplarız:

- $ \frac{8}{11} \approx 0.7272\ldots $

Yani:

$$
\frac{434}{22} \approx 19.7272\ldots
$$

Bu, $ 19.\overline{72} $ olarak gösterilen **devirli bir ondalık sayı**dır.

---

### Nihai Cevap

$$
\boxed{19 \frac{8}{11}} \quad \text{veya} \quad \boxed{\frac{217}{11}} \quad \text{veya} \quad \boxed{19.7272\ldots}
$$

En **kesin ve tercih edilen** cevap:

$$
\boxed{19 \frac{8}{11}}
$$
```
