# Google GenAI

Bu notebook'ta, Google GenAI modelleriyle etkileşim kurmak için LlamaIndex ile birlikte `google-genai` Python SDK'sının nasıl kullanılacağını gösteriyoruz.

Eğer bu Notebook'u Colab üzerinde açıyorsanız, LlamaIndex 🦙 ve `google-genai` Python SDK'sını kurmanız gerekecektir.

```python
%pip install llama-index-llms-google-genai llama-index
```

## Temel Kullanım

[Google AI Studio](https://makersuite.google.com/app/apikey) adresinden bir API anahtarı almanız gerekecektir. Bir anahtarınız olduğunda, bunu doğrudan modele geçebilir veya `GOOGLE_API_KEY` ortam değişkenini kullanabilirsiniz.

```python
import os

os.environ["GOOGLE_API_KEY"] = "..."
```

## Temel Kullanım

Bir istem (prompt) ile `complete` fonksiyonunu çağırabilirsiniz:

```python
from llama_index.llms.google_genai import GoogleGenAI

llm = GoogleGenAI(
    model="gemini-2.5-flash",
    # api_key="bir anahtar",  # varsayılan olarak GOOGLE_API_KEY ortam değişkenini kullanır
)

resp = llm.complete("Paul Graham kimdir?")
print(resp)
```

    Paul Graham, teknoloji dünyasında tanınmış bir isimdir; programcı, deneme yazarı ve risk sermayedarısı olarak çalışmalarıyla bilinir. İşte temel katkılarının bir dökümü:
    
    *   **Programcı ve Hacker:** Özellikle Lisp konusunda yetenekli bir programcıdır. Çevrimiçi mağazalar oluşturmak için araçlar sunan ilk yazılım-servis (SaaS) şirketlerinden biri olan Viaweb'in kurucu ortaklarındandır. Yahoo, Viaweb'i 1998'de satın aldı ve şirket Yahoo! Store haline geldi.
    
    *   **Deneme Yazarı:** Graham, üretken ve etkili bir deneme yazarıdır. Denemeleri, girişimler, programlama, tasarım ve toplumsal trendler gibi geniş bir yelpazeyi kapsar. Yazım stili net, özlü ve düşündürücü olmasıyla tanınır. Denemelerinin çoğu, girişimciler ve teknolojiyle ilgilenenler için temel okuma materyali olarak kabul edilir.
    
    *   **Risk Sermayedarı ve Y Combinator Kurucusu:** Belki de en önemli katkısı, 2005 yılında Y Combinator'ı (YC) kurmasıdır. YC, erken aşamadaki girişimlere tohum yatırımı, mentorluk ve ağ oluşturma fırsatları sunan son derece başarılı bir girişim hızlandırıcısıdır. YC, Airbnb, Dropbox, Reddit, Stripe ve daha pek çok tanınmış şirkete fon sağlamıştır. Graham, 2014 yılında YC'deki günlük görevlerinden ayrılmıştır ancak hala sürece dahildir.
    
    Özetle Paul Graham; programcı, deneme yazarı ve risk sermayedarı olarak teknoloji endüstrisine önemli katkılarda bulunmuş çok yönlü bir bireydir. Özellikle dünyanın önde gelen girişim hızlandırıcılarından biri olan Y Combinator'ı kurması ve şekillendirmesiyle tanınır.

Sohbet mesajları listesiyle `chat` fonksiyonunu da çağırabilirsiniz:

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.google_genai import GoogleGenAI

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın."
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]
llm = GoogleGenAI(model="gemini-2.5-flash")
resp = llm.chat(messages)

print(resp)
```

    assistant: Ahoy orada, ahbap! Toplanın etrafıma, deniz tutmuşlar sizi, ve kemiklerinizi sızlatacak, ayak parmaklarınızı kıvıracak bir hikaye dinleyin! Bu, Tek Gözlü Jack'in Kayıp Papağanı ve Büyük Mango Karışıklığı'nın hikayesi!
    
    Şimdi, Tek Gözlü Jack, o midye kabuğuyla kaplı kalbi sağ olsun, korkunç bir korsandı, tamam mı. Bir kasırgadan daha yüksek sesle kükreyebilir, bir derviş gibi pala sallayabilir ve bir balık gibi rom içebilirdi. Ama yumuşak bir karnı vardı, anlıyor musun? Papağanı Polly için yumuşak bir karın. Polly sadece herhangi bir papağan değildi, aklınızda bulunsun. Kaptanın her küfrünü taklit edebilir, tüylerini kabartış şekliyle hava durumunu tahmin edebilir ve parlak ıvır zıvırlara karşı özel bir ilgisi vardı.
    
    Bir gün, Mango Adası kıyılarında demirlemiştik; şimdiye kadar gördüğünüz en sulu, en tatlı mangolarla dolup taşan yemyeşil bir cennet. Jack, o açgözlü ruhu sağ olsun, onlarla dolu bir kargo ambarına ihtiyacımız olduğuna karar verdi. "İskorbüt önlemi için!" diye ilan etti, sağlam gözüyle kırparak. Bana sorarsanız, daha çok kendi kişisel mango yeme yarışması içindi.
    
    Kıyıya hücum ettik, palalar parlıyordu, mango bahçelerini yağmalamaya hazırdık. Ama Polly, o küçük tüylü şeytan, gemiden bıktığına karar verdi. "Parlak! Parlak!" diye cıyakladı ve adanın kalbine doğru yeşil bir çizgi gibi fırladı.
    
    Jack çılgına döndü! "Polly! Polly, seni tüylü canavar! Buraya gel!" Arkasından kovalamaya başladı, aşk acısı çeken bir mors gibi böğürerek. Geri kalanımız ise mango toplamak ve kendimize gülmemek için çabalamakla kaldık.
    
    Şimdi, Mango Adası sadece mangolarla dolu değildi. Aynı zamanda yaramaz maymunlardan oluşan bir kabileye, Mango Yağmacıları'na da ev sahipliği yapıyordu. Şakalarıyla ve çivilenmemiş her şeyi çalma konusundaki esrarengiz yetenekleriyle ünlüydüler.
    
    Meğer Polly tam onların bölgesinin ortasına inmiş. Ve o maymunlar, onun parlak tüylerine bir bakış atmışlar ve onun çalınmış hazine koleksiyonlarına mükemmel bir katkı olacağına karar vermişler. Onu kaptılar, dır dır ederek ve çığlık atarak ve zamanla oyulmuş dev bir mango ağacı olan gizli inlerine götürdüler.
    
    Jack, o inatçı kalbi sağ olsun, Polly'nin çığlıklarını takip etti. Sarmaşıkları yardı, düşen mangolardan kaçtı ve hatta tüylü arkadaşının peşinde özellikle huysuz bir iguanayla güreşti.
    
    Sonunda mango ağacına ulaştı. İçeriye baktı ve Polly'yi, hepsi onun parlak tüylerine hayran kalmış bir maymun sürüsüyle çevrili gördü. Ya Polly? Maymunların dır dırlarını taklit ederek ve mangolarını çalarak hayatının en güzel vaktini geçiriyordu!
    
    Jack, sinirlenmek yerine gülmeye başladı. Ağacın temellerini sarsan gür, gürleyen bir kahkaha. Maymunlar, irkilerek mangolarını düşürdüler ve ona baktılar.
    
    Sonra Polly, kaptanını görünce cıyakladı: "Rom! Herkese rom!"
    
    Ve işte böyle, dostlarım, Tek Gözlü Jack mango seven bir maymun kabilesiyle bir fıçı rom paylaşırken buldu kendini. Günün geri kalanını mango yiyerek, rom içerek ve Polly'nin maymunların maskaralıklarını taklit etmesini dinleyerek geçirdik. Hatta kargo ambarını mangolarla doldurmayı bile başardık, gerçi büyük bir kısmının maymunlar tarafından çoktan yarı yarıya yenmiş olduğundan şüpheleniyorum.
    
    Yani hikayenin ana fikri ne, çocuklarım? En sert korsanın bile yumuşak bir karnı vardır ve bazen en iyi hazineler en az beklediklerinizdir. Ve her zaman, AMA HER ZAMAN, papağanınıza göz kulak olun! Şimdi, bir tur daha grog isteyen var mı?

## Akış (Streaming) Desteği

Her yöntem, `stream_` ön eki aracılığıyla akış desteği sunar.

```python
from llama_index.llms.google_genai import GoogleGenAI

llm = GoogleGenAI(model="gemini-2.5-flash")

resp = llm.stream_complete("Paul Graham kimdir?")
for r in resp:
    print(r.delta, end="")
```

    Paul Graham, teknoloji dünyasında tanınmış bir isimdir; bilgisayar programcısı, deneme yazarı, risk sermayedarı ve girişim hızlandırıcısı Y Combinator'ın kurucu ortağı olarak bilinir. İşte temel başarıları ve katkılarının bir dökümü:
    
    *   **Bilgisayar Programcısı ve Yazar:** Graham, Harvard Üniversitesi'nden bilgisayar bilimleri alanında doktora derecesine sahiptir. Bir programlama dili olan Lisp üzerindeki çalışmalarıyla ve daha sonra Yahoo! tarafından satın alınarak Yahoo! Store haline gelen ilk yazılım-servis (SaaS) şirketlerinden biri olan Viaweb'i geliştirmesiyle tanınır. Ayrıca "On Lisp", "ANSI Common Lisp", "Hackers & Painters" ve "A Plan for Spam" dahil olmak üzere programlama ve girişimcilik üzerine etkili birkaç kitabın yazarıdır.
    
    *   **Deneme Yazarı:** Graham; teknoloji, girişimler, sanat, felsefe ve toplum dahil çok çeşitli konularda yazan üretken bir deneme yazarıdır. Denemeleri; derin gözlemleri, net yazım stili ve genellikle aykırı bakış açılarıyla bilinir. Teknoloji topluluğunda yaygın olarak okunur ve tartışılırlar. Denemelerini web sitesi paulgraham.com'da bulabilirsiniz.
    
    *   **Risk Sermayedarı ve Y Combinator:** Graham, 2005 yılında Jessica Livingston, Robert Morris ve Trevor Blackwell ile birlikte Y Combinator'ı (YC) kurmuştur. YC, erken aşamadaki girişimlere tohum yatırımı, mentorluk ve ağ oluşturma fırsatları sunan son derece başarılı bir girişim hızlandırıcısıdır. YC, Airbnb, Dropbox, Reddit, Stripe ve daha pek çok tanınmış şirketi fonlamıştır. 2014 yılında YC'deki günlük operasyonlardan ayrılmış olsa da, organizasyon ve girişim ekosistemi üzerindeki etkisi önemli olmaya devam etmektedir.
    
    Özetle Paul Graham; bilgisayar bilimi, girişimcilik ve daha geniş teknoloji kültürüne önemli katkılarda bulunmuş çok yönlü bir bireydir. Teknik uzmanlığı, derinlikli yazıları ve modern girişim manzarasını şekillendirmedeki rolüyle büyük saygı görmektedir.

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="user", content="Paul Graham kimdir?"),
]

resp = llm.stream_chat(messages)
for r in resp:
    print(r.delta, end="")
```

    Paul Graham, teknoloji dünyasında tanınmış bir isimdir; programcı, deneme yazarı ve risk sermayedarı olarak çalışmalarıyla bilinir. İşte temel katkılarının bir dökümü:
    
    *   **Programcı ve Hacker:** Özellikle Lisp konusunda yetenekli bir programcıdır. Daha sonra Yahoo! tarafından satın alınan ve Yahoo! Store haline gelen ilk yazılım-servis (SaaS) şirketlerinden biri olan Viaweb'in kurucu ortaklarındandır.
    
    *   **Deneme Yazarı:** Graham, programlama ve girişimlerden sanat, felsefe ve sosyal yorumlara kadar uzanan konularda yazan üretken ve etkili bir deneme yazarıdır. Denemeleri netliği, derinliği ve genellikle aykırı bakış açılarıyla bilinir. Teknoloji topluluğunda yaygın olarak okunur ve tartışılırlar.
    
    *   **Risk Sermayedarı:** 2005 yılında son derece başarılı bir girişim hızlandırıcısı olan Y Combinator'ı (YC) kurmuştur. YC, Airbnb, Dropbox, Reddit, Stripe ve diğer pek çok tanınmış şirketi fonlamış ve onlara mentorluk yapmıştır. Graham'ın erken aşama yatırımcılığına ve girişim mentorluğuna yaklaşımı, girişim ekosistemi üzerinde önemli bir etki yaratmıştır.
    
    Özetle Paul Graham; programcı, deneme yazarı ve risk sermayedarı olarak teknoloji endüstrisine önemli katkılarda bulunmuş çok yönlü bir bireydir. Özellikle Y Combinator ile yaptığı çalışmalarla girişim dünyasında oldukça etkilidir.

## Asenkron Kullanım

Her senkron yöntemin asenkron bir karşılığı vardır.

```python
from llama_index.llms.google_genai import GoogleGenAI

llm = GoogleGenAI(model="gemini-2.5-flash")

resp = await llm.astream_complete("Paul Graham kimdir?")
async for r in resp:
    print(r.delta, end="")
```

    Paul Graham, teknoloji dünyasında tanınmış bir isimdir; programcı, deneme yazarı ve risk sermayedarı olarak çalışmalarıyla bilinir. İşte temel başarıları ve rollerinin bir dökümü:
    
    *   **Programcı ve Hacker:** Harvard'dan bilgisayar bilimleri doktorasına sahiptir ve bir programlama dili olan Lisp üzerindeki çalışmalarıyla tanınır. Daha sonra Yahoo! tarafından satın alınan ve Yahoo! Store haline gelen ilk yazılım-servis (SaaS) şirketlerinden biri olan Viaweb'in kurucu ortaklarındandır.
    
    *   **Deneme Yazarı:** Graham, programlama ve girişimlerden sanat, felsefe ve sosyal yorumlara kadar uzanan konularda yazan üretken ve etkili bir deneme yazarıdır. Denemeleri teknoloji topluluğunda yaygın olarak okunur ve tartışılır.
    
    *   **Risk Sermayedarı:** 2005 yılında Airbnb, Dropbox, Reddit, Stripe ve diğer pek çok şirketi fonlayan son derece başarılı bir girişim hızlandırıcısı olan Y Combinator'ı (YC) kurmuştur. YC, erken aşamadaki girişimlere tohum yatırımı, mentorluk ve ağ oluşturma fırsatları sunar. 2014 yılında YC'deki günlük operasyonlardan geri çekilmiş olsa da, risk sermayesi dünyasında önemli bir isim olmaya devam etmektedir.
    
    Özetle Paul Graham; bilgisayar bilimi, girişimcilik ve risk sermayesi alanlarına önemli katkılarda bulunmuş çok yönlü bir bireydir. Derinlikli yazıları ve modern girişim ekosistemini şekillendirmedeki rolüyle büyük saygı görmektedir.

```python
messages = [
    ChatMessage(role="user", content="Paul Graham kimdir?"),
]

resp = await llm.achat(messages)
print(resp)
```

    assistant: Paul Graham, teknoloji dünyasında tanınmış bir isimdir; programcı, deneme yazarı ve risk sermayedarı olarak çalışmalarıyla bilinir. İşte temel başarıları ve katkılarının bir dökümü:
    
    *   **Programcı ve Hacker:** Özellikle Lisp konusunda yetenekli bir programcıdır. Daha sonra Yahoo! tarafından satın alınan ve Yahoo! Store haline gelen ilk yazılım-servis (SaaS) şirketlerinden biri olan Viaweb'in kurucu ortaklarındandır.
    
    *   **Deneme Yazarı:** Graham, programlama ve girişimlerden sanat, tasarım ve toplumsal trendlere kadar uzanan konularda yazan üretken ve etkili bir deneme yazarıdır. Denemeleri derinlemesine gözlemleri, aykırı bakış açıları ve net yazım stiliyle tanınır. Denemelerinin çoğu web sitesi paulgraham.com'da mevcuttur.
    
    *   **Risk Sermayedarı ve Y Combinator:** 2005 yılında Airbnb, Dropbox, Reddit, Stripe ve diğer pek çok tanınmış şirketi fonlayan son derece başarılı bir girişim hızlandırıcısı olan Y Combinator'ı (YC) kurmuştur. YC, erken aşamadaki girişimlere tohum yatırımı, mentorluk ve ağ oluşturma fırsatları sunar. Graham, YC'nin felsefesini ve yatırım yaklaşımını şekillendirmede kilit bir rol oynamıştır.
    
    *   **Yazar:** "On Lisp" ve "Hackers & Painters: Big Ideas from the Age of Enlightenment" dahil olmak üzere birkaç kitap yazmıştır.
    
    Özetle Paul Graham; programcı, deneme yazarı ve risk sermayedarı olarak teknoloji endüstrisine önemli katkılarda bulunmuş çok yönlü bir bireydir. Özellikle Y Combinator ile yaptığı çalışmalarla girişim dünyasında oldukça etkilidir.

## Vertex AI Desteği

`region` ve `project_id` parametrelerini (ortam değişkenleri aracılığıyla veya doğrudan) sağlayarak, Vertex AI üzerinden kullanımı etkinleştirebilirsiniz.

```python
# Ortam değişkenlerini ayarlayın
!export GOOGLE_GENAI_USE_VERTEXAI=true
!export GOOGLE_CLOUD_PROJECT='proje-id-niz'
!export GOOGLE_CLOUD_LOCATION='us-central1'
```

```python
from llama_index.llms.google_genai import GoogleGenAI

# veya parametreleri doğrudan ayarlayın
llm = GoogleGenAI(
    model="gemini-2.5-flash",
    vertexai_config={"project": "proje-id-niz", "location": "us-central1"},
    # bağlam penceresini (context window) model için maksimum girdi token'ına ayarlamalısınız
    context_window=200000,
    max_tokens=512,
)
```

    Paul Graham, teknoloji ve girişim dünyasında önde gelen bir figürdür ve en çok şu rolleriyle tanınır:
    
    *   **Y Combinator (YC) Kurucu Ortağı:** Bu, tartışmasız onun en etkili rolüdür. YC, Airbnb, Dropbox, Stripe, Reddit ve daha pek çok şirketi fonlamış son derece başarılı bir girişim hızlandırıcısıdır. Graham'ın girişimleri fonlama ve onlara mentorluk yapma yaklaşımı, girişim ekosistemini önemli ölçüde şekillendirmiştir.
    
    *   **Deneme Yazarı ve Programcı:** YC'den önce Graham bir programcı ve deneme yazarıydı. Programlama, girişimler, tasarım ve toplumsal trendler gibi geniş bir yelpazede yazdığı derinlikli ve genellikle aykırı denemeleriyle tanınır. Denemeleri teknoloji topluluğunda yaygın olarak okunur ve tartışılır.
    
    *   **Viaweb'in Kurucusu (daha sonra Yahoo! Store):** Graham, kullanıcıların çevrimiçi mağazalar kurmasına ve yönetmesine olanak tanıyan ilk uygulama servis sağlayıcılarından biri olan Viaweb'i kurdu. Şirket, 1998'de Yahoo! tarafından satın alındı ve Yahoo! Store adını aldı.
    
    Özetle Paul Graham, Y Combinator'ı kurmadaki rolü, derinlikli denemeleri ve programcı ile girişimci olarak elde ettiği erken başarılarıyla tanınan, girişim dünyasında son derece etkili bir figürdür.

## Önbelleğe Alınmış İçerik Desteği

Google GenAI, büyük bağlamları birden fazla istekte yeniden kullanırken performansı artırmak ve maliyet verimliliği sağlamak için önbelleğe alınmış içeriği destekler. Bu, özellikle RAG uygulamaları, belge analizi ve tutarlı bağlam gerektiren çok turlu konuşmalar için yararlıdır.

#### Avantajlar

- **Daha hızlı yanıtlar**
- Girdi token kullanımının azalmasıyla **maliyet tasarrufu**
- Birden fazla sorguda **tutarlı bağlam**
- Büyük dosyalarla yapılan **belge analizi için mükemmel**

#### Önbelleğe Alınmış İçerik Oluşturma

İlk olarak, Google GenAI SDK'sını kullanarak önbelleğe alınmış içerik oluşturun:

```python
from google import genai
from google.genai.types import CreateCachedContentConfig, Content, Part
import time

client = genai.Client(api_key="api-anahtarınız")

# VertexAI için
# client = genai.Client(
#     http_options=HttpOptions(api_version="v1"),
#     project="proje-id-niz",
#     location="us-central1",
#     vertexai="True"
# )
```

Seçenek 1: Yerel Dosyaları Yükleme

```python
# Yerel PDF dosyalarını yükleyin ve işleyin
pdf_file = client.files.upload(file="./belgeniz.pdf")
while pdf_file.state.name == "PROCESSING":
    print("PDF'nin işlenmesi bekleniyor.")
    time.sleep(2)
    pdf_file = client.files.get(name=pdf_file.name)

# Yüklenen dosya ile önbellek oluşturun
cache = client.caches.create(
    model="gemini-2.5-flash",
    config=CreateCachedContentConfig(
        display_name="Belge Analizi Önbelleği",
        system_instruction=(
            "Sen uzman bir belge analizcisisin. Soruları "
            "sağlanan belgelere dayanarak doğruluk ve detayla yanıtla."
        ),
        contents=[pdf_file],  # Doğrudan dosya referansı
        ttl="3600s",  # 1 saat boyunca önbelleğe al
    ),
)
```

Seçenek 2: İçerik Yapısına Sahip Birden Fazla Dosya

```python
# VertexAI ile birden fazla dosya veya Cloud Storage dosyaları için
contents = [
    Content(
        role="user",
        parts=[
            Part.from_uri(
                # file_uri=pdf_file.uri,    # yüklenen dosyanın URI'sini de kullanabilirsiniz
                file_uri="gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf",
                mime_type="application/pdf",
            ),
            Part.from_uri(
                file_uri="gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
                mime_type="application/pdf",
            ),
        ],
    )
]

cache = client.caches.create(
    model="gemini-2.5-flash",
    config=CreateCachedContentConfig(
        display_name="Çoklu Belge Önbelleği",
        system_instruction=(
            "Sen uzman bir araştırmacısın. Sağlanan belgeler "
            "arasındaki bilgileri analiz et ve karşılaştır."
        ),
        contents=contents,
        ttl="3600s",
    ),
)

print(f"Önbellek oluşturuldu: {cache.name}")
print(f"Önbelleğe alınan token'lar: {cache.usage_metadata.total_token_count}")
```

    Önbellek oluşturuldu: projects/391.../locations/us-central1/cachedContents/267...
    Önbelleğe alınan token'lar: 43102

LlamaIndex ile Önbelleğe Alınmış İçeriği Kullanma

Önbelleği oluşturduktan sonra LlamaIndex ile kullanın:

```python
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage

llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key="api-anahtarınız",
    cached_content=cache.name,
)

# VertexAI için
# llm = GoogleGenAI(
#     model="gemini-2.5-flash",
#     vertexai_config={"project": "proje-id-niz", "location": "us-central1"},
#     cached_content=cache.name
# )

# Önbelleğe alınmış içeriği kullanın
message = ChatMessage(
    role="user", content="Bölüm 4'teki temel bulguları özetle."
)
response = llm.chat([message])
print(response)
```

    assistant: Bölüm 4, "Soyutlama: Süreç" (The Abstraction: The Process), işletim sistemi (OS) tarafından sağlanan temel bir soyutlama olan ve çalışan bir program olarak tanımlanan süreç kavramını tanıtır. İşte temel bulgular:
    
    1.  **Süreç Tanımı:** Bir süreç temel olarak çalışan bir programdır; bellek (adres alanı), kayıtçılar (program sayacı ve yığın işaretçisi dahil) ve I/O bilgileri dahil olmak üzere makine durumuyla karakterize edilir.
    
    2.  **Süreç API'si:** İşletim sistemi; süreç oluşturma (Create), süreç sonlandırma (Destroy), süreçlerin tamamlanmasını bekleme (Wait), süreçlerin kontrolü (Miscellaneous Control) ve durum bilgisi alma (Status) fonksiyonlarını içeren bir süreç API'si sağlar.
    
    3.  **Süreç Oluşturma:** Bir süreç oluşturmak; kod ve statik verilerin belleğe yüklenmesini, yığın (stack) ve yığın bellek (heap) için bellek ayrılmasını, yığının başlatılmasını ve ardından programın giriş noktasında (main()) başlatılmasını içerir.
    
    4.  **Süreç Durumları:** Bir süreç üç durumdan birinde olabilir: Çalışıyor (Running - bir işlemci üzerinde yürütülüyor), Hazır (Ready - çalışmaya hazır ama şu anda çalışmıyor) veya Engellenmiş (Blocked - I/O tamamlanması gibi bir olayı bekliyor).
    
    5.  **Veri Yapıları:** İşletim sistemi, her sürecin durumunu takip etmek için süreç listesi gibi veri yapıları tutar. Bu yapılar, kayıtçı bağlamı (kaydedilmiş kayıtçı değerleri) ve süreç durumu gibi bilgileri içerir.
    
    Özünde Bölüm 4, süreç kavramını ve onunla ilişkili nitelikleri ve durumları tanıtarak, işletim sisteminin CPU'yu nasıl yönettiğini ve sanallaştırdığını anlamak için temel oluşturur.

Üretim Yapılandırmasında (Generation Config) Önbelleğe Alınmış İçeriği Kullanma

İstek düzeyinde önbellek kontrolü için:

```python
import google.genai.types as types

# İstek başına önbelleğe alınmış içeriği belirtin
config = types.GenerateContentConfig(
    cached_content=cache.name, temperature=0.1, max_output_tokens=1024
)

llm = GoogleGenAI(model="gemini-2.5-flash", generation_config=config)

response = llm.complete("Belgenin ilk beş bölümünü listele")
print(response)
```

    İşte İçindekiler kısmında listelendiği gibi belgenin ilk beş bölümü:
    
    1.  Kitap Üzerine Bir Diyalog
    2.  İşletim Sistemlerine Giriş
    3.  Sanallaştırma Üzerine Bir Diyalog
    4.  Soyutlama: Süreç
    5.  Ara Bölüm: Süreç API'si

Önbellek Yönetimi

```python
# Tüm önbellekleri listele
caches = client.caches.list()
for cache_item in caches:
    print(f"Önbellek: {cache_item.display_name} ({cache_item.name})")
    print(f"Token'lar: {cache_item.usage_metadata.total_token_count}")

# Önbellek detaylarını al
cache_info = client.caches.get(name=cache.name)
print(f"Oluşturulma: {cache_info.create_time}")
print(f"Sona Erme: {cache_info.expire_time}")

# İşiniz bittiğinde önbelleği silin
client.caches.delete(name=cache.name)
print("Önbellek silindi")
```

    Önbellek: Belge Analizi Önbelleği (cachedContents/8v3va2x...)
    Token'lar: 77421
    Oluşturulma: 2025-07-08 16:06:11.821190+00:00
    Sona Erme: 2025-07-08 17:06:10.813310+00:00
    Önbellek silindi

## Çok Modlu (Multi-Modal) Destek

`ChatMessage` nesnelerini kullanarak, LLM'e görüntü ve metin gönderebilirsiniz.

```python
!wget https://cdn.pixabay.com/photo/2021/12/12/20/00/play-6865967_640.jpg -O image.jpg
```

    --2025-03-14 10:59:00--  https://cdn.pixabay.com/photo/2021/12/12/20/00/play-6865967_640.jpg
    cdn.pixabay.com (cdn.pixabay.com) çözülüyor... 104.18.40.96, 172.64.147.160
    cdn.pixabay.com (cdn.pixabay.com)|104.18.40.96|:443 bağlanılıyor... bağlandı.
    HTTP isteği gönderildi, yanıt bekleniyor... 200 OK
    Uzunluk: 71557 (70K) [binary/octet-stream]
    Kayıt yeri: ‘image.jpg’
    
    image.jpg           100%[===================>]  69.88K  --.-KB/s    içinde 0.003s  
    
    2025-03-14 10:59:00 (24.8 MB/s) - ‘image.jpg’ kaydedildi [71557/71557]

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.google_genai import GoogleGenAI

llm = GoogleGenAI(model="gemini-2.5-flash")

messages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.jpg", image_mimetype="image/jpeg"),
            TextBlock(text="Bu görüntüde ne var?"),
        ],
    )
]

resp = llm.chat(messages)
print(resp)
```

    assistant: Görüntüde, koyu gri bir yüzey üzerinde siyah noktaları olan dört adet ahşap zar bulunuyor. Her zar farklı sayıda nokta göstererek farklı değerleri işaret ediyor.

Belgeleri de gönderebilirsiniz.

```python
from llama_index.core.llms import DocumentBlock

messages = [
    ChatMessage(
        role="user",
        blocks=[
            DocumentBlock(
                path="/path/to/your/test.pdf",
                document_mimetype="application/pdf",
            ),
            TextBlock(text="Belgeyi tek bir cümleyle tanımla."),
        ],
    )
]

resp = llm.chat(messages)
print(resp)
```

    assistant: Bu araştırma makalesi, Crescendo saldırısını kullanarak son büyük dil modellerindeki (LLM) çok turlu "jailbreak" zafiyetlerini değerlendiriyor ve azaltmaya çalışıyor; çeşitli görev kategorilerinde istem (prompt) güçlendirme ve bir koruma duvarı olarak LLM (LLM-as-guardrail) stratejilerini analiz ediyor.

Son olarak, videoları da gönderebilirsiniz.

```python
from llama_index.core.llms import VideoBlock

messages = [
    ChatMessage(
        role="user",
        blocks=[
            VideoBlock(
                path="/path/to/your/video.mp4", video_mimetype="video/mp4"
            ),
            TextBlock(text="Bu videoyu tek bir cümleyle tanımla."),
        ],
    )
)

resp = llm.chat(messages)
print(resp)
```

    assistant: Beyaz bir SpaceX Crew Dragon kapsülünün, arka planda Dünya'nın kavisli yüzeyi görünürken, Uluslararası Uzay İstasyonu'nun bir modülüne yaklaştığı ve kenetlendiği görülüyor.

## Yapılandırılmış Tahmin (Structured Prediction)

LlamaIndex, `structured_predict` aracılığıyla herhangi bir LLM'i yapılandırılmış bir LLM'e dönüştürmek için sezgisel bir arayüz sunar - sadece hedef Pydantic sınıfını tanımlayın (iç içe geçmiş olabilir) ve verilen bir istemden istenen nesneyi çıkaralım.

```python
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.prompts import PromptTemplate
from llama_index.core.bridge.pydantic import BaseModel
from typing import List


class MenuItem(BaseModel):
    """Bir restorandaki menü öğesi."""

    course_name: str
    is_vegetarian: bool


class Restaurant(BaseModel):
    """Adı, şehri ve mutfağı olan bir restoran."""

    name: str
    city: str
    cuisine: str
    menu_items: List[MenuItem]


llm = GoogleGenAI(model="gemini-2.5-flash")
prompt_tmpl = PromptTemplate(
    "Verilen bir şehirde bir restoran oluştur: {city_name}"
)

# Seçenek 1: `as_structured_llm` kullanın
restaurant_obj = (
    llm.as_structured_llm(Restaurant)
    .complete(prompt_tmpl.format(city_name="Miami"))
    .raw
)
# Seçenek 2: `structured_predict` kullanın
# restaurant_obj = llm.structured_predict(Restaurant, prompt_tmpl, city_name="Miami")
```

```python
print(restaurant_obj)
```

    name='Pasta Mia' city='Miami' cuisine='Italian' menu_items=[MenuItem(course_name='pasta', is_vegetarian=False)]

#### Akış (Streaming) ile Yapılandırılmış Tahmin

`as_structured_llm` ile sarılmış her LLM, `stream_chat` üzerinden akış desteği sunar.

```python
from llama_index.core.llms import ChatMessage
from IPython.display import clear_output
from pprint import pprint

input_msg = ChatMessage.from_str("San Francisco'da bir restoran oluştur")

sllm = llm.as_structured_llm(Restaurant)
stream_output = sllm.stream_chat([input_msg])
for partial_output in stream_output:
    clear_output(wait=True)
    pprint(partial_output.raw.dict())
    restaurant_obj = partial_output.raw

restaurant_obj
```

    {'city': 'San Francisco',
     'cuisine': 'Italian',
     'menu_items': [{'course_name': 'pasta', 'is_vegetarian': False}],
     'name': 'Italian Delight'}


    /var/folders/lw/xwsz_3yj4ln1gvkxhyddbvvw0000gn/T/ipykernel_76091/1885953561.py:11: PydanticDeprecatedSince20: `dict` yöntemi kullanımdan kaldırılmıştır; bunun yerine `model_dump` kullanın. Pydantic V2.0'da kullanımdan kaldırılmış olup V3.0'da kaldırılacaktır. Bkz. https://errors.pydantic.dev/2.10/migration/ adresindeki Pydantic V2 Geçiş Kılavuzu.
      pprint(partial_output.raw.dict())





    Restaurant(name='Italian Delight', city='San Francisco', cuisine='Italian', menu_items=[MenuItem(course_name='pasta', is_vegetarian=False)])

## Araç/Fonksiyon Çağırma (Tool/Function Calling)

Google GenAI, API üzerinden doğrudan araç/fonksiyon çağırmayı destekler. LlamaIndex'i kullanarak bazı temel ajan tabanlı araç çağırma modellerini uygulayabiliriz.

```python
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import ChatMessage
from llama_index.llms.google_genai import GoogleGenAI
from datetime import datetime

llm = GoogleGenAI(model="gemini-2.5-flash")


def get_current_time(timezone: str) -> dict:
    """Geçerli saati getirir"""
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": timezone,
    }


# Aracı tanımlamak için fonksiyon adını, tip notasyonlarını ve docstring'i kullanır
tool = FunctionTool.from_defaults(fn=get_current_time)
```

Aracı çağırmak ve sonucu almak için tek bir geçiş (pass) yapabiliriz:

```python
resp = llm.predict_and_call([tool], "New York'ta şu an saat kaç?")
print(resp)
```

    {'time': '2025-03-14 10:59:05', 'timezone': 'America/New_York'}

Ayrıca, bir ajan tabanlı araç çağırma döngüsü uygulamak için daha düşük seviyeli API'leri de kullanabiliriz!

```python
chat_history = [
    ChatMessage(role="user", content="New York'ta şu an saat kaç?")
]
tools_by_name = {t.metadata.name: t for t in [tool]}

resp = llm.chat_with_tools([tool], chat_history=chat_history)
tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)

if not tool_calls:
    print(resp)
else:
    while tool_calls:
        # LLM'in yanıtını sohbet geçmişine ekle
        chat_history.append(resp.message)

        for tool_call in tool_calls:
            tool_name = tool_call.tool_name
            tool_kwargs = tool_call.tool_kwargs

            print(f"{tool_name} aracı {tool_kwargs} ile çağrılıyor")
            tool_output = tool.call(**tool_kwargs)
            print("Araç çıktısı: ", tool_output)
            chat_history.append(
                ChatMessage(
                    role="tool",
                    content=str(tool_output),
                    # Gemini, Anthropic, OpenAI gibi çoğu LLM'in araç çağrı kimliğini (tool call id) bilmesi gerekir
                    additional_kwargs={"tool_call_id": tool_call.tool_id},
                )
            )

            resp = llm.chat_with_tools([tool], chat_history=chat_history)
            tool_calls = llm.get_tool_calls_from_response(
                resp, error_on_no_tool_call=False
            )
    print("Son yanıt: ", resp.message.content)
```

    get_current_time aracı {'timezone': 'America/New_York'} ile çağrılıyor
    Araç çıktısı:  {'time': '2025-03-14 10:59:06', 'timezone': 'America/New_York'}
    Son yanıt:  New York'ta şu an saat 2025-03-14 10:59:06.

Ayrıca tek bir istekte birden fazla aracı aynı anda çağırabiliriz; bu da farklı bilgi türleri gerektiren karmaşık sorgular için verimlilik sağlar.

```python
# Sıcaklık için başka bir araç tanımlayın
def get_temperature(city: str) -> dict:
    """Bir şehir için mevcut sıcaklığı getirir"""
    return {
        "city": city,
        "temperature": "25°C",
    }


# Fonksiyonlardan araçlar oluşturun
tool1 = FunctionTool.from_defaults(fn=get_current_time)
tool2 = FunctionTool.from_defaults(fn=get_temperature)

# Her iki aracı da gerektiren bir soru sorun
chat_history = [
    ChatMessage(
        role="user",
        content="New York'ta şu an saat ve sıcaklık nedir?",
    )
]

# Model hangi araçları çağıracağına akıllıca karar verecektir
resp = llm.chat_with_tools([tool1, tool2], chat_history=chat_history)
tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)

print(f"Model {len(tool_calls)} araç çağrısı yaptı:")
for i, tool_call in enumerate(tool_calls, 1):
    print(f"{i}. {tool_call.tool_name} parametreler: {tool_call.tool_kwargs}")
```

    Model 2 araç çağrısı yaptı:
    1. get_current_time parametreler: {'timezone': 'America/New_York'}
    2. get_temperature parametreler: {'city': 'New York'}

## Google Arama Temellendirme (Google Search Grounding)

Google Gemini 2.0 ve 2.5 modelleri, modelin gerçek zamanlı bilgi aramasına ve yanıtlarını web arama sonuçlarıyla temellendirmesine olanak tanıyan Google Arama temellendirmesini destekler. Bu, özellikle güncel bilgileri almak için yararlıdır.

`built_in_tool` parametresi, modelin yanıtlarını Google Arama sonuçlarından gelen gerçek dünya verileriyle temellendirmesini sağlayan Google Arama araçlarını kabul eder.

```python
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage
from google.genai import types

# Google Arama temellendirme aracı oluşturun
grounding_tool = types.Tool(google_search=types.GoogleSearch())

llm = GoogleGenAI(
    model="gemini-2.5-flash",
    built_in_tool=grounding_tool,
)

resp = llm.complete("ABD'deki bir sonraki tam güneş tutulması ne zaman?")
print(resp)
```

    Amerika Birleşik Devletleri'nde görülecek bir sonraki tam güneş tutulması 23 Ağustos 2044 tarihinde gerçekleşecek. Ancak bütünlük (totality) sadece Montana, Kuzey Dakota ve Güney Dakota'da görülebilecek. Bir başka tam güneş tutulması ise 12 Ağustos 2045'te Kaliforniya'dan Florida'ya uzanan bir hat üzerinde gerçekleşecek.

Google Arama temellendirme aracı birkaç avantaj sağlar:

- **Gerçek zamanlı bilgi**: Güncel olaylara ve en son verilere erişim
- **Olgusal doğruluk**: Gerçek arama sonuçlarına dayanan yanıtlar
- **Kaynak atfı**: Temellendirme meta verileri arama kaynaklarını içerir
- **Otomatik arama kararları**: Model, sorguya göre ne zaman arama yapacağına karar verir

Temellendirme aracını sohbet mesajlarıyla da kullanabilirsiniz:

```python
# Sohbet mesajlarıyla Google Arama'yı kullanma
messages = [ChatMessage(role="user", content="Euro 2024'ü kim kazandı?")]

resp = llm.chat(messages)
print(resp)

# Ham yanıttan temellendirme meta verilerine erişebilirsiniz
if hasattr(resp, "raw") and "grounding_metadata" in resp.raw:
    print(resp.raw["grounding_metadata"])
else:
    print("\nBu yanıtta temellendirme meta verisi bulunamadı")
```

    assistant: İspanya, finalde İngiltere'yi 2-1 mağlup ederek Euro 2024'ü kazandı. Maç Berlin'deki Olimpiyat Stadı'nda (Olympiastadion) oynandı. Bu zafer, İspanya'nın dördüncü Avrupa Şampiyonası şampiyonluğu oldu ve turnuvadaki en çok galibiyet sayısında Almanya'yı geride bıraktı.
    
    {'grounding_chunks': [{'retrieved_context': None, 'web': {'domain': None, 'title': 'olympics.com', 'uri': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEkqnG_iRjkf89rilwO5fSBjbAADgm-Ad83fhYOhtAgW2qoG5Y8Gkselc-GshmvpqgMzke0vSUmkc6B8WwmXuxGBl9IPk3YWsytW2nOvGo1n8MlxqcrCpP62vvqjYFoo3wDQsb-tZ3RfZYTjKSTdKfVEBhvSfi4wSKMIgbnQkRx50DLqr2w3sjYI3hyZGWdsFyJFfviXdPSnVCZqQ=='}}, {'retrieved_context': None, 'web': {'domain': None, 'title': 'aljazeera.com', 'uri': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFHwRYxryu8EgG5hG-Gwgdn9sRn88H8iehIOG7KPis7rpJcRo35EAc0onyC_5hqcjUozIddtikyjHmUdK2oIBX8_3ENpLTqpu8TyYb97EibGX6_-ZtRtlPnOsd4TukiRVwfiWMk5sk9FZCsNUEFTWb9OJzPhSjOiAPW78aoAQkM9LSKLBY5vBNyQtUsNvb7k6WEd23pHAKtofxi5i7W_qYrtZPiSkqOBTqtyJ2N69oYDw=='}}, {'retrieved_context': None, 'web': {'domain': None, 'title': 'wikipedia.org', 'uri': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF2WEgQILX6A9y0uLZzBXY9UsduYELn9ahnW-FBNNHBvTQPWkuc_9cwyKmUEbfx0iton_BcIGh_85ibG5hkoE3kPvyBFfh6dEdy3UG2Vvn9gIprxruYLiUKtx8o6I06ZyFiERJqUzboU8s8Dvbd'}}, {'retrieved_context': None, 'web': {'domain': None, 'title': 'thehindu.com', 'uri': 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHqXK-zKOuGkYtQFyc48K49_TYwib-bRIvPqnn5UmjUcVI69vTxIiXnpXXkJtSMHa5-cBZ6Ht_4cAuWs5GuKZSzHeAQ-sHJQ2BEk52qIzjTvSteXGf7v0oBOQ_AUTqdTOpH8vXEVhqnp3o6WFVchKfexDT2sk1IDBqlqLxqQrKD9PrMsMOvU8_kfuGqH3IR_V2GHHnrPgwgR93LpiYvFdtVDlo3Wi12kj1FAgqDHHjkqyZpSc-pJ-522x0VgcdKGX6mXZ0Ssd7-aLK0YYO028ex6-o8ZeKEqeSpC9H7GP3bnw=='}}], 'grounding_supports': [{'confidence_scores': [0.97524184, 0.950235, 0.64699775], 'grounding_chunk_indices': [0, 1, 2], 'segment': {'end_index': 55, 'part_index': None, 'start_index': None, 'text': "İspanya, finalde İngiltere'yi 2-1 mağlup ederek Euro 2024'ü kazandı"}}, {'confidence_scores': [0.9290034, 0.9209086], 'grounding_chunk_indices': [2, 3], 'segment': {'end_index': 109, 'part_index': None, 'start_index': 57, 'text': "Maç Berlin'deki Olimpiyat Stadı'nda oynandı"}}, {'confidence_scores': [0.842964, 0.0068578157], 'grounding_chunk_indices': [2, 1], 'segment': {'end_index': 229, 'part_index': None, 'start_index': 111, 'text': "Bu zafer, İspanya'nın dördüncü Avrupa Şampiyonası şampiyonluğu oldu ve turnuvadaki en çok galibiyet sayısında Almanya'yı geride bıraktı"}}], 'retrieval_metadata': {'google_search_dynamic_retrieval_score': None}, 'retrieval_queries': None, 'search_entry_point': {'rendered_content': '...', 'sdk_blob': None}, 'web_search_queries': ['euro 2024\'ü kim kazandı']}

## Kod Yürütme (Code Execution)

`built_in_tool` parametresi ayrıca, modelin sorunları çözmek, hesaplamalar yapmak ve verileri analiz etmek için Python kodu yazmasına ve yürütmesine olanak tanıyan kod yürütme araçlarını da kabul eder. Bu, özellikle matematiksel hesaplamalar, veri analizi ve görselleştirmeler oluşturmak için yararlıdır.

```python
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage
from google.genai import types

# Kod yürütme aracı oluşturun
code_execution_tool = types.Tool(code_execution=types.ToolCodeExecution())

llm = GoogleGenAI(
    model="gemini-2.5-flash",
    built_in_tool=code_execution_tool,
)

resp = llm.complete("20. fibonacci sayısını hesapla.")
print(resp)
```

    Tamam, 20. Fibonacci sayısını hesaplayabilirim. Bunun için bir python betiği kullanacağım.
    
    
    20. Fibonacci sayısı 6765'tir.

### Kod Yürütme Detaylarına Erişim

Model kod yürütmeyi kullandığında, yürütülen koda, sonuçlara ve diğer meta verilere ham yanıt üzerinden erişebilirsiniz. Bu şunları içerir:

- **executable_code**: Gerçekten yürütülen Python kodu
- **code_execution_result**: Kodun çalıştırılmasından elde edilen çıktı
- **text**: Modelin açıklaması ve yorumu

Bunu iş başında görelim:

```python
# Kod yürütmeyi kullanması muhtemel bir hesaplama isteyin
messages = [
    ChatMessage(
        role="user", content="İlk 50 asal sayının toplamı nedir?"
    )
]

resp = llm.chat(messages)

# Kod yürütme detaylarını görmek için ham yanıta erişin
if hasattr(resp, "raw") and "content" in resp.raw:
    parts = resp.raw["content"].get("parts", [])

    for i, part in enumerate(parts):
        print(f"Parça {i+1}:")

        if "text" in part and part["text"]:
            print(f"  Metin: {part['text'][:100]}", end="")
            print(" ..." if len(part["text"]) > 100 else "")

        if "executable_code" in part and part["executable_code"]:
            print(f"  Yürütülebilir Kod: {part['executable_code']}")

        if "code_execution_result" in part and part["code_execution_result"]:
            print(f"  Kod Sonucu: {part['code_execution_result']}")
else:
    print("Ham yanıtta detaylı parçalar bulunamadı")
```

    Parça 1:
      Metin: Tamam, ilk 50 asal sayının toplamını hesaplamam gerekiyor. Bunun için bir python betiği kullanabilir ...
    Parça 2:
      Yürütülebilir Kod: {'code': "def is_prime(n):\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True\n\nprimes = []\nnum = 2\nwhile len(primes) < 50:\n    if is_prime(num):\n        primes.append(num)\n    num += 1\n\nprint(f'{sum(primes)=}')\n", 'language': <Language.PYTHON: 'PYTHON'>}
    Parça 3:
      Kod Sonucu: {'outcome': <Outcome.OUTCOME_OK: 'OUTCOME_OK'>, 'output': 'sum(primes)=5117\n'}
    Parça 4:
      Metin: İlk 50 asal sayının toplamı 5117'dir.

## Görüntü Oluşturma (Image Generation)

Seçili modeller, görüntü girdilerinin yanı sıra görüntü çıktılarını da destekler. `response_modalities` yapılandırmasını kullanarak bir Gemini modeliyle görüntüler oluşturabilir ve düzenleyebiliriz!

```python
from llama_index.llms.google_genai import GoogleGenAI
import google.genai.types as types

config = types.GenerateContentConfig(
    temperature=0.1, response_modalities=["Text", "Image"]
)

llm = GoogleGenAI(
    model="gemini-2.5-flash-image-preview", generation_config=config
)
```

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock

messages = [
    ChatMessage(role="user", content="Lütfen sevimli bir köpek görüntüsü oluştur")
]

resp = llm.chat(messages)
```

```python
from PIL import Image
from IPython.display import display

for block in resp.message.blocks:
    if isinstance(block, ImageBlock):
        image = Image.open(block.resolve_image())
        display(image)
    elif isinstance(block, TextBlock):
        print(block.text)
```

    İşte senin için sevimli bir köpek! 

![png](output_62_1.png)

Görüntüyü de düzenleyebiliriz!

```python
messages.append(resp.message)
messages.append(
    ChatMessage(
        role="user",
        content="Lütfen görüntüyü köpeği mini schnauzer yapacak şekilde düzenle, ancak genel pozu, çerçevelemeyi, arka planı ve sanat stilini aynı tut.",
    )
)

resp = llm.chat(messages)

for block in resp.message.blocks:
    if isinstance(block, ImageBlock):
        image = Image.open(block.resolve_image())
        display(image)
    elif isinstance(block, TextBlock):
        print(block.text)
```

    İşte mini schnauzer'ın! 

![png](output_64_1.png)