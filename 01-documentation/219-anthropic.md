# Anthropic

Anthropic; haiku, sonnet ve opus ailelerinden pek çok son teknoloji model sunar.

Bu modelleri LlamaIndex ile nasıl kullanacağınızı öğrenmek için okumaya devam edin!

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-anthropic
```

#### Belirteç Oluşturucuyu (Tokenizer) Ayarla

Öncelikle, TikToken'dan biraz farklı olan belirteç oluşturucuyu ayarlamak istiyoruz. Bu, kitaplık genelinde belirteç sayımının doğru olmasını sağlar.

**NOT**: Anthropic yakın zamanda belirteç sayma API'sini güncelledi. claude-2.1 gibi eski modeller, Anthropic python istemcisinin en yeni sürümlerinde belirteç sayımı için artık desteklenmemektedir.

```python
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings

tokenizer = Anthropic().tokenizer
Settings.tokenizer = tokenizer
```

## Temel Kullanım

```python
import os

os.environ["ANTHROPIC_API_KEY"] = "sk-..."
```

Bir istemle (prompt) `complete` çağrısı yapabilirsiniz:

```python
from llama_index.llms.anthropic import Anthropic

# API anahtarınızı özelleştirmek için bunu yapın,
# aksi takdirde ortam değişkeninizden ANTHROPIC_API_KEY aranacaktır
# llm = Anthropic(api_key="<api_key>")
llm = Anthropic(model="claude-sonnet-4-0")

resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

    Paul Graham bir bilgisayar programcısı, girişimci, risk sermayedarı ve denemecidir. İşte tanındığı başlıca noktalar:
    
    **Y Combinator**: 2005 yılında Airbnb, Dropbox, Stripe ve Reddit gibi şirketlerin kurulmasına yardımcı olan bu oldukça etkili girişim hızlandırıcısının kurucu ortaklarındandır. Y Combinator, erken aşamadaki girişimlere tohum yatırımı ve mentörlük sağlar.
    
    **Programlama**: Programlama topluluğunda saygın bir figürdür, özellikle Lisp programlama dili üzerindeki çalışmalarıyla ve 1990'larda ilk web tabanlı uygulama olan Viaweb'i (Yahoo'ya satılarak Yahoo Store olmuştur) ortaklaşa oluşturmasıyla tanınır.
    
    **Yazarlık**: Graham, paulgraham.com adresindeki web sitesinde yayınladığı girişimler, teknoloji, programlama ve toplum üzerine düşünceli denemeleriyle tanınır. Denemeleri teknoloji çevrelerinde geniş çapta okunur ve bir girişimin nasıl kurulacağı, inovasyonun doğası ve sosyal yorumlar gibi konuları kapsar.
    
    **Kitaplar**: "Hackers & Painters" ve "On Lisp" dahil olmak üzere birkaç kitabın yazarıdır.
    
    **Etki**: Hem Y Combinator'ın etkisiyle hem de girişimcilik ve teknoloji üzerine yazılarıyla Silikon Vadisi'nin girişim ekosistemindeki en etkili kişilerden biri olarak kabul edilir.
    
    Graham, analitik düşüncesi ve iş dünyası, teknoloji ve kültür hakkındaki aykırı perspektifleriyle tanınır.

Sohbet mesajlarının bir listesiyle `chat` çağrısı da yapabilirsiniz:

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.anthropic import Anthropic

messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]
llm = Anthropic(model="claude-sonnet-4-0")
resp = llm.chat(messages)

print(resp)
```

    assistant: Ahoy orada, ahbap! *üç köşeli şapkasını düzeltir ve sakalını sıvazlar* 
    
    Sana denizcilik günlerimden, okyanusun bir krakenin öfkesi kadar vahşi ve iki kat daha öngörülemez olduğu zamanlardan bir hikaye anlatayım!
    
    **Şarkı Söyleyen Pusulanın Hikayesi**
    
    Mürettebatımla birlikte en tuhaf hazineyi keşfettiğimiz sisli bir sabahtı - altın ya da mücevher değil, dikkat et, deniz türküleri mırıldanan bir pusula! Evet, doğru duydun! Bu garip küçük alet, hangi yöne baktığına bağlı olarak farklı ezgiler mırıldanırdı.
    
    Kuzey, kayıp aşklar hakkında melankolik bir balad getirirken, Güney, en huysuz denizcimiz Tek Gözlü Pete'in bile tahta bacağına tempo tutturmasına neden olan neşeli bir melodi söylerdi. Ama işin ilginç yanı şuydu - Batı'yı gösterdiğinde, hiçbirimizin daha önce duymadığı, antik bir dilde sözleri olan gizemli bir melodi söylerdi.
    
    Maceracı tipler olduğumuz için (ve belki biraz da aptal), bu batı şarkısını üç gün üç gece takip ettik. Pusula bizi tehlikeli sulardan, seraplar gibi parıldayan adaların yanından geçirdi ve sonunda suyun sıvı zümrütler gibi parladığı gizli bir koya ulaştık.
    
    Ve orada, yürekli dostum, en büyük hazineyi bulduk - zenginlik değil, efsunlu pusulalarını birinin iade etmesini yüzyıllardır bekleyen bir deniz kızı ailesi! Nezaketimizi, herhangi bir fırtınadan güvenli bir geçişle ve üç gerçek hazine adasının gizli yerleriyle ödüllendirdiler.
    
    *göz kırpar ve hayali bir şişeden bir yudum alır*
    
    Bazen en iyi maceralar en tuhaf şarkıları takip etmekten gelir, anladın mı?

## Akış (Streaming) Desteği

Her metot, `stream_` ön eki aracılığıyla akışı destekler.

```python
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(model="claude-sonnet-4-0")

resp = llm.stream_complete("Paul Graham kimdir?")
for r in resp:
    print(r.delta, end="")
```

    Paul Graham bir bilgisayar programcısı, girişimci, risk sermayedarı ve denemecidir. İşte tanındığı başlıca noktalar:
    
    **Y Combinator Kurucu Ortağı**: 2005 yılında dünyanın en başarılı girişim hızlandırıcılarından biri olan Y Combinator'ı kurmuştur. Y Combinator; Airbnb, Dropbox, Stripe, Reddit ve yüzlerce başka şirketi finanse etmiştir.
    
    **Programlama ve Lisp**: Lisp programlama dilinin güçlü bir savunucusudur ve "On Lisp" ile "ANSI Common Lisp" dahil olmak üzere etkili kitaplar yazmıştır.
    
    **Viaweb**: 1990'larda, ilk web tabanlı yazılım şirketlerinden biri olan Viaweb'i kurmuştur; şirket 1998'de Yahoo tarafından satın alınmış ve Yahoo Store olmuştur.
    
    **Denemeler**: paulgraham.com adresindeki web sitesinde yayınladığı girişimler, programlama ve teknoloji üzerine etkili birçok deneme yazmıştır. Denemeleri teknoloji topluluğunda geniş çapta okunur ve bir girişimin nasıl kurulacağı, neyin iyi bir programcı yaptığı ve inovasyonun doğası gibi konuları kapsar.
    
    **Sanat ve Akademi**: Harvard'da Bilgisayar Bilimi alanında doktorası vardır ve ayrıca Rhode Island Tasarım Okulu ile Floransa'daki Accademia di Belle Arti'de resim eğitimi almıştır.
    
    Graham, girişim ekosistemindeki en etkili figürlerden biri olarak kabul edilir ve girişimcilik ile teknoloji girişimleri hakkındaki modern düşünceyi şekillendirmeye yardımcı olmuştur.

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="user", content="Paul Graham kimdir?"),
]

resp = llm.stream_chat(messages)
for r in resp:
    print(r.delta, end="")
```

    Paul Graham bir bilgisayar programcısı, girişimci, risk sermayedarı ve denemecidir. İşte tanındığı başlıca noktalar:
    
    **Y Combinator**: 2005 yılında Airbnb, Dropbox, Stripe ve Reddit gibi şirketlerin kurulmasına yardımcı olan bu oldukça etkili girişim hızlandırıcısının kurucu ortaklarındandır. Y Combinator, erken aşamadaki girişimlere tohum yatırımı ve mentörlük sağlar.
    
    **Programlama**: Programlama topluluğunda saygın bir figürdür, özellikle Lisp programlama dili üzerindeki çalışmalarıyla ve 1990'larda ilk web tabanlı uygulama olan Viaweb'i (Yahoo'ya satılarak Yahoo Store olmuştur) ortaklaşa oluşturmasıyla tanınır.
    
    **Yazarlık**: Graham, paulgraham.com adresindeki web sitesinde yayınladığı girişimler, teknoloji, programlama ve girişimcilik üzerine düşünceli denemeleriyle tanınır. Denemeleri teknoloji çevrelerinde geniş çapta okunur ve bir girişimin nasıl kurulacağı, inovasyonun doğası ve teknoloji trendleri gibi konuları kapsar.
    
    **Etki**: Hem Y Combinator'ın başarısıyla hem de birçok insanın girişimcilik ve teknoloji hakkındaki düşüncelerini şekillendiren yazılarıyla Silikon Vadisi'nin girişim ekosistemindeki en etkili kişilerden biri olarak kabul edilir.
    
    Teknik uzmanlığı, iş zekası ve net yazım tarzının kombinasyonu, onu yirmi yılı aşkın bir süredir teknoloji endüstrisinde önde gelen bir ses haline getirmiştir.

## Asenkron Kullanım

Her senkron metodun asenkron bir karşılığı vardır.

```python
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(model="claude-sonnet-4-0")

resp = await llm.astream_complete("Paul Graham kimdir?")
async for r in resp:
    print(r.delta, end="")
```

    Paul Graham bir bilgisayar programcısı, girişimci, risk sermayedarı ve denemecidir. İşte tanındığı başlıca noktalar:
    
    **Y Combinator**: 2005 yılında Airbnb, Dropbox, Stripe ve Reddit gibi şirketlerin kurulmasına yardımcı olan bu oldukça etkili girişim hızlandırıcısının kurucu ortaklarındandır. Y Combinator, erken aşamadaki girişimlere tohum yatırımı ve mentörlük sağlar.
    
    **Programlama**: Programlama topluluğunda saygın bir figürdür, özellikle Lisp programlama dili üzerindeki çalışmalarıyla tanınır. "On Lisp" ve "ANSI Common Lisp" gibi etkili kitaplar yazmıştır.
    
    **Denemeler**: Graham, paulgraham.com adresindeki web sitesinde yayınladığı girişimler, teknoloji, programlama ve toplum üzerine geniş çapta okunan denemeler yazar. "Do Things That Don't Scale" ve "How to Start a Startup" gibi denemeleri teknoloji dünyasında temel okuma parçaları olarak kabul edilir.
    
    **Girişimcilik**: Y Combinator'dan önce, 1998 yılında Yahoo tarafından yaklaşık 49 milyon dolara satın alınan ve Yahoo Store olan Viaweb'i (çevrimiçi mağazalar kurmak için ilk web tabanlı uygulamalardan biri) kurmuştur.
    
    **Sanat geçmişi**: İlginç bir şekilde, sanat alanında da bir geçmişi vardır ve resim eğitimi almıştır; bu deneyimi teknolojideki yaratıcılık ve estetik bakış açısını etkiler.
    
    Graham, Silikon Vadisi'nde ve daha geniş girişim ekosisteminde en etkili seslerden biri olarak kabul edilir.

```python
messages = [
    ChatMessage(role="user", content="Paul Graham kimdir?"),
]

resp = await llm.achat(messages)
print(resp)
```

    assistant: Paul Graham bir bilgisayar programcısı, girişimci, risk sermayedarı ve denemecidir. İşte tanındığı başlıca noktalar:
    
    **Y Combinator**: 2005 yılında Airbnb, Dropbox, Stripe ve Reddit gibi şirketlerin kurulmasına yardımcı olan bu oldukça etkili girişim hızlandırıcısının kurucu ortaklarındandır. Y Combinator, erken aşamadaki girişimlere tohum yatırımı ve mentörlük sağlar.
    
    **Programlama**: Programlama topluluğunda saygın bir figürdür, özellikle Lisp programlama dili üzerindeki çalışmalarıyla ve 1990'larda ilk web tabanlı uygulama olan Viaweb'i (Yahoo'ya satılarak Yahoo Store olmuştur) ortaklaşa oluşturmasıyla tanınır.
    
    **Yazarlık**: Graham, paulgraham.com adresindeki web sitesinde yayınladığı girişimler, teknoloji, programlama ve toplum üzerine düşünceli denemeleriyle tanınır. Denemeleri teknoloji çevrelerinde geniş çapta okunur ve bir girişimin nasıl kurulacağı, inovasyonun doğası ve sosyal yorumlar gibi konuları kapsar.
    
    **Kitaplar**: "Hackers & Painters" ve "On Lisp" dahil olmak üzere birkaç kitabın yazarıdır.
    
    **Etki**: Hem Y Combinator'ın etkisiyle hem de girişimcilik ve teknoloji üzerine yazılarıyla Silikon Vadisi'nin girişim ekosistemindeki en etkili kişilerden biri olarak kabul edilir.
    
    Graham, analitik düşüncesi ve iş dünyası, teknoloji ve kültür hakkındaki aykırı perspektifleriyle tanınır.



## Vertex AI Desteği

`region` ve `project_id` parametrelerini (ortam değişkenleri aracılığıyla veya doğrudan) sağlayarak, Vertex AI üzerinden bir Anthropic modelini kullanabilirsiniz.

```python
import os

os.environ["ANTHROPIC_PROJECT_ID"] = "PROJE KİMLİĞİNİZ BURAYA"
os.environ["ANTHROPIC_REGION"] = "PROJE BÖLGENİZ BURAYA"
```

Bölge ve proje kimliğini burada ayarlamanın, Anthropic'in Vertex AI istemcisini kullanmasını sağlayacağını unutmayın.

## Bedrock Desteği

LlamaIndex ayrıca AWS Bedrock üzerinden Anthropic modellerini de destekler.

```python
from llama_index.llms.anthropic import Anthropic

# Not: Bu, ortamınızda standart AWS kimlik bilgilerinin yapılandırıldığını varsayar
llm = Anthropic(
    model="anthropic.claude-3-7-sonnet-20250219-v1:0",
    aws_region="us-east-1",
)

resp = llm.complete("Paul Graham kimdir?")
```

## Çok Modlu (Multi-Modal) Destek

`ChatMessage` nesnelerini kullanarak, LLM'e görüntüler ve metinler gönderebilirsiniz.

```python
!wget https://cdn.pixabay.com/photo/2021/12/12/20/00/play-6865967_640.jpg -O image.jpg
```

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(model="claude-sonnet-4-0")

messages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.jpg"),
            TextBlock(text="Bu görselde ne var?"),
        ],
    )
]

resp = llm.chat(messages)
print(resp)
```

    assistant: Bu görselde, koyu renkli bir kumaş yüzey üzerinde dört adet ahşap zar görülmektedir. Zarlar açık renkli ahşaptan yapılmış gibi görünüyor ve her bir yüzdeki sayıları belirten geleneksel siyah noktalara (pip) sahip. Koyu mavi veya siyah bir kumaş arka plan gibi görünen bir yere rastgele dağılmış durumdalar.

## İstem Önbelleğe Alma (Prompt Caching)

Anthropic modelleri, istem önbelleğe alma fikrini destekler - bu yöntemde bir istem birden çok kez tekrarlanırsa veya bir istemin başlangıcı tekrarlanırsa, LLM yanıtı hızlandırmak ve maliyetleri düşürmek için önceden hesaplanmış dikkat (attention) sonuçlarını yeniden kullanabilir.

İstem önbelleğe almayı etkinleştirmek için, `ChatMessage` nesnelerinizde `cache_control` ayarını yapabilir veya her zaman ilk X mesajı önbelleğe almak için LLM üzerinde `cache_idx` ayarını yapabilirsiniz (-1 tüm mesajlar anlamına gelir).

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(model="claude-sonnet-4-0")

# münferit mesajları önbelleğe al
messages = [
    ChatMessage(
        role="user",
        content="<bazı çok uzun istemler>",
        additional_kwargs={"cache_control": {"type": "ephemeral"}},
    ),
]

resp = llm.chat(messages)

# ilk X mesajı önbelleğe al (-1 tüm mesajlar anlamına gelir)
llm = Anthropic(model="claude-sonnet-4-0", cache_idx=-1)

resp = llm.chat(messages)
```

## Yapılandırılmış Tahmin (Structured Prediction)

LlamaIndex, `structured_predict` aracılığıyla herhangi bir Anthropic LLM'ini yapılandırılmış bir LLM'e dönüştürmek için sezgisel bir arayüz sağlar - sadece hedef Pydantic sınıfını (iç içe olabilir) tanımlayın ve bir istem verildiğinde, istenen nesneyi dışarı çıkaralım.

```python
from llama_index.llms.anthropic import Anthropic
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


llm = Anthropic(model="claude-sonnet-4-0")
prompt_tmpl = PromptTemplate(
    "Verilen bir şehirde ({city_name}) bir restoran oluştur"
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
restaurant_obj
```

    Restaurant(name='Ocean Breeze Bistro', city='Miami', cuisine='Seafood', menu_items=[MenuItem(course_name='Grilled Mahi-Mahi with Mango Salsa', is_vegetarian=False), MenuItem(course_name='Coconut Shrimp with Pineapple Dipping Sauce', is_vegetarian=False), MenuItem(course_name='Quinoa and Black Bean Bowl', is_vegetarian=True), MenuItem(course_name='Key Lime Pie', is_vegetarian=True), MenuItem(course_name='Lobster Bisque', is_vegetarian=False), MenuItem(course_name='Grilled Vegetable Platter with Chimichurri', is_vegetarian=True)])

#### Akışlı Yapılandırılmış Tahmin (Structured Prediction with Streaming)

`as_structured_llm` ile sarmalanmış herhangi bir LLM, `stream_chat` aracılığıyla akışı destekler.

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
     'cuisine': 'California Fusion',
     'menu_items': [{'course_name': 'Dungeness Crab Cakes', 'is_vegetarian': False},
                    {'course_name': 'Roasted Beet and Arugula Salad',
                     'is_vegetarian': True},
                    {'course_name': 'Grilled Pacific Salmon',
                     'is_vegetarian': False},
                    {'course_name': 'Wild Mushroom Risotto', 'is_vegetarian': True},
                    {'course_name': 'Grass-Fed Beef Tenderloin',
                     'is_vegetarian': False},
                    {'course_name': 'Chocolate Lava Cake', 'is_vegetarian': True}],
     'name': 'Golden Gate Bistro'}

    Restaurant(name='Golden Gate Bistro', city='San Francisco', cuisine='California Fusion', menu_items=[MenuItem(course_name='Dungeness Crab Cakes', is_vegetarian=False), MenuItem(course_name='Roasted Beet and Arugula Salad', is_vegetarian=True), MenuItem(course_name='Grilled Pacific Salmon', is_vegetarian=False), MenuItem(course_name='Wild Mushroom Risotto', is_vegetarian=True), MenuItem(course_name='Grass-Fed Beef Tenderloin', is_vegetarian=False), MenuItem(course_name='Chocolate Lava Cake', is_vegetarian=True)])




## Model Düşünme (Model Thinking)

`claude-3.7 Sonnet` ile, modelin bir görev hakkında daha derin "düşünmesini" sağlayabilir ve nihai cevabı yazmadan önce bir düşünce zinciri (chain-of-thought) yanıtı üretmesini temin edebilirsiniz.

Bunu, yapıcıya (constructor) `thinking_dict` parametresini geçirerek ve düşünme süreci için ayrılacak belirteç miktarını belirterek etkinleştirebilirsiniz.

```python
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage

llm = Anthropic(
    model="claude-sonnet-4-0",
    # max_tokens, budget_tokens'tan büyük olmalıdır
    max_tokens=64000,
    # düşünmenin çalışması için temperature 1.0 olmalıdır
    temperature=1.0,
    thinking_dict={"type": "enabled", "budget_tokens": 1600},
)
```

```python
messages = [
    ChatMessage(role="user", content="(1234 * 3421) / (231 + 2341) = ?")
]

resp_gen = llm.stream_chat(messages)

for r in resp_gen:
    print(r.delta, end="")

print()
print(r.message.content)
```

    Bunu adım adım çözeceğim.
    
    Önce, payı hesaplayalım:
    1234 × 3421 = 4.221.514
    
    Sonra, paydayı hesaplayalım:
    231 + 2341 = 2.572
    
    Şimdi bölme işlemini yapabilirim:
    4.221.514 ÷ 2.572 = 1.641,42 (2 ondalık basamağa yuvarlanmış)
    
    Dolayısıyla: (1234 × 3421) ÷ (231 + 2341) = **1.641,42**
    Bunu adım adım çözeceğim.
    
    Önce, payı hesaplayalım:
    1234 × 3421 = 4.221.514
    
    Sonra, paydayı hesaplayalım:
    231 + 2341 = 2.572
    
    Şimdi bölme işlemini yapabilirim:
    4.221.514 ÷ 2.572 = 1.641,42 (2 ondalık basamağa yuvarlanmış)
    
    Dolayısıyla: (1234 × 3421) ÷ (231 + 2341) = **1.641,42**

```python
print(r.message.additional_kwargs["thinking"]["signature"])
```

    EsgICkYIAxgCKkBcW71ZZ3zt/vVxd0Aw2evRNOsyewVAaXXFcHa2zRC5O/TG/Db+RfgHqKNF7EWL0WuJKRXJZ20Y/...

Tam düşünme sürecini de ortaya çıkarabiliriz:

```python
print(r.message.additional_kwargs["thinking"]["thinking"])
```

    (1234 * 3421) / (231 + 2341) işlemini hesaplamam gerekiyor.
    
    Adım adım yapayım.
    
    Önce payı hesaplayalım: 1234 * 3421
    1234 * 3421
    = 1234 * (3000 + 400 + 20 + 1)
    = 1234 * 3000 + 1234 * 400 + 1234 * 20 + 1234 * 1
    = 3.702.000 + 493.600 + 24.680 + 1.234
    = 4.221.514
    
    Şimdi paydayı hesaplayalım: 231 + 2341
    231 + 2341 = 2.572
    
    İşlem şuna dönüşüyor:
    4.221.514 / 2.572
    
    Bölmeyi yapalım:
    4.221.514 ÷ 2.572 = 1.641,4...
    
    Daha kesin olalım:
    4.221.514 ÷ 2.572 = 1.641,42...
    
    Aslında çarpmamı tekrar kontrol edeyim:
    1234 * 3421
    
    1234
    ×3421
    -----
    1234 (1234 × 1)
    2468 (1234 × 2, bir basamak kaydırılmış)
    4936 (1234 × 4, iki basamak kaydırılmış)
    3702 (1234 × 3, üç basamak kaydırılmış)
    -----
    
    Daha dikkatli olayım:
    1234 × 1 = 1234
    1234 × 20 = 24680
    1234 × 400 = 493600
    1234 × 3000 = 3702000
    
    1234 + 24680 + 493600 + 3702000 = 4.221.514
    
    Bu doğru.
    
    Şimdi 4.221.514 ÷ 2.572 ≈ 1.641,42

## Araç/Fonksiyon Çağırma (Tool/Function Calling)

Anthropic, API üzerinden doğrudan araç/fonksiyon çağırmayı destekler. LlamaIndex kullanarak bazı temel otonom araç çağırma modellerini uygulayabiliriz.

```python
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import ChatMessage
from llama_index.llms.anthropic import Anthropic
from datetime import datetime

llm = Anthropic(model="claude-sonnet-4-0")


def get_current_time() -> dict:
    """Mevcut saati getirir"""
    return {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# aracı tanımlamak için araç adını, varsa tip ek açıklamalarını ve docstring'i kullanır
tool = FunctionTool.from_defaults(fn=get_current_time)
```

Aracı çağırmak ve sonucu almak için basitçe tek bir geçiş yapabiliriz:

```python
resp = llm.predict_and_call([tool], "Şu an saat kaç?")
print(resp)
```

    {'time': '2025-05-22 12:45:48'}

Otonom bir araç çağırma döngüsü uygulamak için daha düşük seviyeli API'leri de kullanabiliriz!

```python
chat_history = [ChatMessage(role="user", content="Şu an saat kaç?")]
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
                    # Anthropic, OpenAI vb. çoğu LLM'in araç çağrı kimliğini (id) bilmesi gerekir
                    additional_kwargs={"tool_call_id": tool_call.tool_id},
                )
            )

            resp = llm.chat_with_tools([tool], chat_history=chat_history)
            tool_calls = llm.get_tool_calls_from_response(
                resp, error_on_no_tool_call=False
            )
    print("Nihai yanıt: ", resp.message.content)
```

    get_current_time aracı {} ile çağrılıyor
    Araç çıktısı:  {'time': '2025-05-22 12:45:51'}
    Nihai yanıt:  Şu anki saat 22 Mayıs 2025, 12:45:51.

## Sunucu Tarafı Araç Çağırma (Server-Side Tool Calling)

Anthropic artık en yeni sürümlerde sunucu tarafı araç çağırmayı da destekliyor.

İşte bunun nasıl kullanılacağına dair bir örnek:

```python
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(
    model="claude-sonnet-4-0",
    max_tokens=1024,
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 3,  # Maksimum 3 arama ile sınırla
        }
    ],
)

# Atıflar (citations) ile yanıt al
response = llm.complete("En son yapay zeka araştırma trendleri nelerdir?")

# Ana yanıt içeriğine eriş
print(response.text)

# Varsa atıflara eriş
for citation in response.citations:
    print(f"Kaynak: {citation.get('url')} - {citation.get('cited_text')}")
```

    En son araştırma ve endüstri raporlarına dayanarak, 2025'i şekillendiren temel yapay zeka trendleri şunlardır:
    
    ## 1. Otonom YZ (Agentic AI) Ön Plana Çıkıyor
    
    Otonom YZ - asgari insan müdahalesiyle bağımsız olarak görevleri yerine getirebilen YZ sistemleri - 2025'in en önemli trendi olarak ortaya çıkıyor. Microsoft yöneticilerine göre, "aracıları (agent) YZ çağının uygulamaları olarak düşünün." Erken uygulamalar, parola değişiklikleri veya izin talepleri gibi küçük, yapılandırılmış dahili görevlere odaklanacak; şirketler ise gerçek para içeren müşteri odaklı etkinlikler için aracıları kullanma konusunda temkinli davranacak.
    
    ## 2. Gelişmiş Muhakeme Yetenekleri
    
    OpenAI'nin o1 modeli gibi gelişmiş muhakeme yeteneklerine sahip YZ modelleri, karmaşık problemleri insan düşüncesine benzer mantıksal adımlarla çözebilir; bu da onları özellikle bilim, kodlama, matematik, hukuk ve tıp alanlarında yararlı kılar. Teknoloji şirketleri, doğal dil işleme, görüntü oluşturma ve kodlama alanlarında sınırları zorlayan öncü modeller geliştirmek için yarışıyor.
    
    ## 3. Ölçülebilir ROI ve Kurumsal Benimsemeye Odaklanma
    
    2025'te işletmeler, üretken YZ'den ölçülebilir sonuçlar bekliyor: maliyetlerin düşürülmesi, kanıtlanabilir yatırım getirisi (ROI) ve verimlilik artışı. Kuruluşların %90'ından fazlasının üretken YZ kullanımını artırmasına rağmen, girişimlerini sadece %8'inin olgun sayması, pratik uygulamada önemli bir büyüme alanı olduğunu gösteriyor.
    
    ## 4. Bilimsel Keşif ve Malzeme Bilimi
    
    YZ, bilimsel keşiflerde giderek daha fazla uygulanıyor; malzeme bilimi, YZ'nin protein araştırmalarındaki başarısının ardından gelecek vaat eden bir alan olarak ortaya çıkıyor. Meta, bilim insanlarının yeni malzemeleri daha hızlı keşfetmelerine yardımcı olmak için devasa veri kümeleri ve modeller yayınladı.
    
    ## 5. Çok Modlu YZ ve Sohbet Robotlarının Ötesi
    
    YZ teknolojisi olgunlaştıkça, geliştiriciler ve işletmeler, sohbet robotlarını bağımsız araçlar olarak kullanmak yerine büyük dil modellerinin üzerine gelişmiş yazılım uygulamaları oluşturmaya yöneliyor.
    
    ## 6. Dramatik Maliyet Düşüşleri
    
    Çıkarım (inference) maliyetleri hızla düşüyor - bir yıldan kısa bir sürede milyon belirteç başına 20 dolardan 0,07 dolara geriledi; GPT-3.5 düzeyindeki performans maliyeti Kasım 2022 ile Ekim 2024 arasında 280 kattan fazla azaldı.
    
    ## 7. Performans Farklarının Kapanması
    
    En iyi ABD ve Çin YZ modelleri arasındaki performans farkı bir yıl içinde %9,26'dan sadece %1,70'e indi; açık ağırlıklı modeller ise kapalı modellerle aradaki farkı kapatıyor ve bazı kıyaslamalarda performans farkını %8'den %1,7'ye indiriyor.
    
    ## 8. Artan Düzenleyici Faaliyetler
    
    ABD federal kurumları 2024'te 59 YZ ile ilgili düzenleme getirdi - bu sayı 2023'tekinin iki katından fazla - küresel çapta ise YZ'den bahseden yasal düzenlemeler 75 ülkede %21,3 arttı.
    
    ## 9. Veri Yönetimi Devrimi
    
    Üretken YZ, yapılandırılmamış verileri yeniden önemli hale getiriyor; veri ve YZ liderlerinin %94'ü YZ ilgisinin veriye olan odağı artırdığını, veri göllerinin esnekliğini veri ambarlarının yapısıyla birleştiren bir "veri göl evi devrimi"ni tetiklediğini söylüyor.
    
    ## 10. Savunma ve Askeri Uygulamalar
    
    Savunma teknolojisi şirketleri, YZ modellerini eğitmek için gizli askeri verilerden yararlanıyor; OpenAI gibi ana akım YZ şirketleri askeri ortaklıklara yönelerek Pentagon ile çalışan Microsoft, Amazon ve Google arasına katılıyor.
    
    Bu trendler 2025'i gösteriyor...
    Kaynak: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - · YZ destekli aracılar, evde ve işte hayatınızı basitleştirmeye yardımcı olmak için daha fazla özerklikle daha fazlasını yapacak. 
    Kaynak: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - 2025'te yeni nesil YZ destekli aracılar daha fazlasını yapacak - hatta sizin adınıza belirli görevleri yürütecek.  
    Kaynak: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2025/ - Otonom YZ'yi -bağımsız olarak görev yapan YZ türü- önceden aradan çıkaralım: 2025'in "en trend YZ trendi" olacağı kesin. 
    Kaynak: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - Microsoft'un iş ve sektör Copilot kurumsal başkan yardımcısı Charles Lamanna, "Aracıları YZ çağının uygulamaları olarak düşünün," diyor.
    Kaynak: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2025/ - İlk aracılar, az miktarda paranın söz konusu olduğu küçük, yapılandırılmış dahili görevler için olanlar olacak - örneğin, parolanızı değiştirmenize yardımcı olmak...
    Kaynak: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - OpenAI o1 gibi gelişmiş muhakeme yeteneklerine sahip modeller, karmaşık problemleri insanların düşünme şekline benzer mantıksal adımlarla zaten çözebiliyor...
    Kaynak: https://www.morganstanley.com/insights/articles/ai-trends-reasoning-frontier-models-2025-tmt - Dünyanın en büyük teknoloji şirketleri yapay zeka kullanımı için en son teknolojileri geliştirmek üzere yarışıyorlar: büyük dil modellerinin akıl yürütme yeteneği...
    Kaynak: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - 2025'te işletmelerin üretken YZ'den ölçülebilir sonuçlar: maliyet düşüşleri, kanıtlanabilir ROI ve verimlilik kazanımları için daha fazla baskı yapmasını bekleyin. 
    Kaynak: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - 2025'te işletmelerin üretken YZ'den ölçülebilir sonuçlar: maliyet düşüşleri, kanıtlanabilir ROI ve verimlilik kazanımları için daha fazla baskı yapmasını bekleyin. 
    Kaynak: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - Eylül 2024 tarihli bir araştırma raporunda, Informa TechTarget’ın Enterprise Strategy Group ekibi, kuruluşların %90’ından fazlasının üretken YZ kullanımını artırmasına rağmen...
    Kaynak: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - Bu eğilimin gelecek yıl da devam etmesini ve özellikle bilimsel keşifleri amaçlayan daha fazla veri kümesi ve model görmeyi bekleyin. 
    Kaynak: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - Potansiyel alanlardan biri malzeme bilimi. Meta, bilim insanlarının yeni malzemeleri çok daha hızlı keşfetmek için YZ kullanmalarına yardımcı olabilecek devasa veri kümeleri ve modeller yayınladı...
    Kaynak: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - Meta, bilim insanlarının yeni malzemeleri çok daha hızlı keşfetmek için YZ kullanmalarına yardımcı olabilecek devasa veri kümeleri ve modeller yayınladı ve Aralık ayında Hugging Face...
    Kaynak: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - Ancak teknoloji olgunlaştıkça, YZ geliştiricileri, son kullanıcılar ve işletme müşterileri sohbet robotlarının ötesine bakıyor. "İnsanların daha yaratıcı düşünmesi gerekiyor..."
    Kaynak: https://spectrum.ieee.org/ai-index-2025 - Bu, çıkarım maliyetlerinin veya eğitilmiş bir modeli sorgulama maliyetinin dramatik bir şekilde düştüğü anlamına geliyor. 
    Kaynak: https://spectrum.ieee.org/ai-index-2025 - Rapor, mavi çizginin milyon belirteç başına 20 dolardan 0,07 dolara düştüğünü; pembe çizginin ise 15 dolardan düştüğünü gösteriyor...
    Kaynak: https://hai.stanford.edu/ai-index/2025-ai-index-report - Giderek daha yetenekli hale gelen küçük modellerin etkisiyle, GPT-3.5 seviyesinde performans gösteren bir sistemin çıkarım maliyeti Kasım 2022'den bu yana 280 kattan fazla düştü...
    Kaynak: https://spectrum.ieee.org/ai-index-2025 - Ocak 2024'te en iyi ABD modeli en iyi Çin modelinden %9,26 daha iyi performans gösteriyordu; Şubat 2025 itibarıyla bu fark sadece %1,70'e indi....
    Kaynak: https://hai.stanford.edu/ai-index/2025-ai-index-report - Açık ağırlıklı modeller de kapalı modellerle aradaki farkı kapatıyor ve bazı kıyaslamalarda performans farkını tek bir yılda %8'den sadece %1,7'ye indiriyor...
    Kaynak: https://hai.stanford.edu/ai-index/2025-ai-index-report - 2024 yılında ABD federal kurumları 59 yapay zeka bağlantılı düzenleme getirdi - bu rakam 2023'tekinin iki katından fazla - ve bu düzenlemeler iki kat daha fazla kurum tarafından yayınlandı. Küresel olarak...
    Kaynak: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2025/ - Üretken YZ'nin kuruluşlar üzerinde başka bir etkisi daha oldu: Yapılandırılmamış verileri yeniden önemli hale getiriyor. 2025 YZ ve Veri Liderliği Yönetici Araştırması'nda...
    Kaynak: https://www.morganstanley.com/insights/articles/ai-trends-reasoning-frontier-models-2025-tmt - Yöneticiler ayrıca veri göllerinin düşük maliyetli depolaması ve esnekliğini veri ambarlarının yapısıyla birleştiren birleşik veri platformları oluşturma eğilimi olan "veri göl evi devrimi"ni vurguladılar...
    Kaynak: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - 2025 yılında bu trendler, şu anda gizli askeri verilerden yararlanan Palantir, Anduril ve diğerleri gibi savunma teknolojisi şirketleri için bir nimet olmaya devam edecek...


## Araç Çağırma + Atıflar (Tool Calling + Citations)

`llama-index-core>=0.12.46` + `llama-index-llms-anthropic>=0.7.6` sürümlerinde, atıf yapılabilir araç sonuçlarını çıktı olarak verme desteği ekledik!

Anthropic kullanarak, artık araç sonuçlarınızın belirli bölümlerine atıf yapmak için sunucu tarafı atıflarından yararlanabilirsiniz.

Eğer LLM bir araç sonucuna atıf yaparsa, atıf çıktıda kaynak, başlık ve atıf yapılan içeriği içeren bir `CitationBlock` olarak görünecektir.

Bunu pratikte yapmanın birkaç yolunu inceleyelim.

İlk olarak, atıf yapılabilir bir blok döndüren bir taslak (dummy) araç/fonksiyon tanımlayalım.

```python
from llama_index.core import Document
from llama_index.core.llms import CitableBlock, TextBlock
from llama_index.core.tools import FunctionTool

dummy_text = Document.example().text


async def search_fn(query: str):
    """Soruları yanıtlamak için web'de arama yapmak için kullanışlıdır."""
    return CitableBlock(
        content=[TextBlock(text=dummy_text)],
        title="LLM'ler ve LlamaIndex Hakkında Gerçekler",
        source="https://docs.llamaindex.ai",
    )


search_tool = FunctionTool.from_defaults(search_fn)
```

```python
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(
    model="claude-sonnet-4-0",
    # api_key="sk-...",
)
```

### Aracılar + Atıf Yapılabilir Araçlar

Çıktıda aynı atıfları almak için bu araçları doğrudan `FunctionAgent` gibi önceden oluşturulmuş aracılarda da kullanabilirsiniz.

```python
from llama_index.core.agent.workflow import FunctionAgent

agent = FunctionAgent(
    tools=[search_tool],
    llm=llm,
    # Statik bir sonuç döndüren sahte bir aracımız olduğu için LLM belirteçlerini boşa harcamak istemiyoruz
    system_prompt="Kullanıcı mesajı başına yalnızca bir arama sorgusu yapın.",
    timeout=None,
)
```

```python
output = await agent.run("LlamaIndex ve LLM'ler birlikte nasıl çalışır?")
```

```python
from llama_index.core.llms import CitationBlock

print(output.response.content)
print("----" * 20)
for block in output.response.blocks:
    if isinstance(block, CitationBlock):
        print("Kaynak: ", block.source)
        print("Başlık: ", block.title)
        print("Atıf Yapılan İçerik:\n", block.cited_content.text)
        print("----" * 20)
```

    Arama sonuçlarına dayanarak, LlamaIndex ve LLM'lerin birlikte nasıl çalıştığını açıklayabilirim:
    
    LLM'ler, bilgi oluşturma ve muhakeme için olağanüstü bir teknoloji parçasıdır. Büyük miktarda halka açık veri üzerinde önceden eğitilmişlerdir. Ancak temel bir zorluk vardır: LLM'leri kendi özel verilerimizle en iyi nasıl güçlendirebiliriz?
    
    İşte LlamaIndex burada çözüm olarak devreye giriyor. LlamaIndex, LLM uygulamaları oluşturmanıza yardımcı olacak bir "veri çerçevesidir" (data framework). Birlikte şu şekilde çalışırlar:
    
    ## Veri Entegrasyonu ve Yapısı
    LlamaIndex, mevcut veri kaynaklarınızı ve veri formatlarınızı (API'ler, PDF'ler, belgeler, SQL vb.) almak için veri bağlayıcıları sunar ve bu verilerin LLM'lerle kolayca kullanılabilmesi için verilerinizi yapılandırma yolları (indeksler, grafikler) sağlar.
    
    ## Gelişmiş Sorgu Arayüzü
    LlamaIndex, verileriniz üzerinde gelişmiş bir erişim/sorgu arayüzü sağlar: Herhangi bir LLM giriş istemini besleyin, geri erişilen bağlamı ve bilgiyle güçlendirilmiş çıktıyı alın. Bu, bir soru sorduğunuzda LlamaIndex'in özel verilerinizden ilgili bilgileri aldığı ve bunu LLM'e bağlam olarak sunduğu, böylece daha doğru ve kişiselleştirilmiş yanıtlar sağladığı anlamına gelir.
    
    ## Esnek Entegrasyon
    LlamaIndex, dış uygulama çerçevenizle (örneğin LangChain, Flask, Docker, ChatGPT, başka herhangi bir şeyle) kolay entegrasyonlar sağlar.
    
    ## Kullanıcı Dostu Tasarım
    LlamaIndex hem başlangıç seviyesindeki kullanıcılar hem de ileri düzey kullanıcılar için araçlar sağlar. Üst düzey API, yeni başlayanların LlamaIndex'i kullanarak verilerini 5 satır kodla almalarına ve sorgulamalarına olanak tanır. Alt seviye API'ler, ileri düzey kullanıcıların herhangi bir modülü (veri bağlayıcıları, indeksler, alıcılar, sorgu motorları, yeniden sıralama modülleri) ihtiyaçlarına göre özelleştirmesine ve genişletmesine olanak tanır.
    --------------------------------------------------------------------------------
    Kaynak:  https://docs.llamaindex.ai
    Başlık:  LLM'ler ve LlamaIndex Hakkında Gerçekler
    Atıf Yapılan İçerik:
     
    Bağlam
    LLM'ler, bilgi oluşturma ve muhakeme için olağanüstü bir teknoloji parçasıdır.
    Büyük miktarda halka açık veri üzerinde önceden eğitilmişlerdir.
    LLM'leri kendi özel verilerimizle en iyi nasıl güçlendirebiliriz?
    LLM'ler için bu veri güçlendirmesini gerçekleştirmeye yardımcı olacak kapsamlı bir araç setine ihtiyacımız var.
    
    Önerilen Çözüm
    İşte LlamaIndex burada devreye giriyor. LlamaIndex, LLM uygulamaları oluşturmanıza yardımcı olacak bir "veri çerçevesidir". Şu araçları sağlar:
    
    Mevcut veri kaynaklarınızı ve veri formatlarınızı (API'ler, PDF'ler, belgeler, SQL vb.) almak için veri bağlayıcıları sunar.
    Verilerinizin LLM'lerle kolayca kullanılabilmesi için verilerinizi yapılandırma yolları (indeksler, grafikler) sağlar.
    Verileriniz üzerinde gelişmiş bir erişim/sorgu arayüzü sağlar:
    Herhangi bir LLM giriş istemini besleyin, geri erişilen bağlamı ve bilgiyle güçlendirilmiş çıktıyı alın.
    Dış uygulama çerçevenizle (örneğin LangChain, Flask, Docker, ChatGPT, başka herhangi bir şeyle) kolay entegrasyonlar sağlar.
    LlamaIndex hem başlangıç seviyesindeki kullanıcılar hem de ileri düzey kullanıcılar için araçlar sağlar.
    Üst düzey API'miz, yeni başlayanların LlamaIndex'i kullanarak verilerini 5 satır kodla almalarına ve sorgulamalarına olanak tanır. Alt seviye API'lerimiz, ileri düzey kullanıcıların herhangi bir modülü (veri bağlayıcıları, indeksler, alıcılar, sorgu motorları, yeniden sıralama modülleri) ihtiyaçlarına göre özelleştirmesine ve genişletmesine olanak tanır.
    
    --------------------------------------------------------------------------------

### Manuel Araç Çağırma + Atıflar

Atıf yapılabilir bir blok döndüren aracımızı kullanarak, bir manuel aracı döngüsünde verilen araçla LLM'i manuel olarak çağırabiliriz.

LLM araç çağırmayı durdurduğunda, nihai yanıtı döndürebilir ve yanıttaki atıfları ayrıştırabiliriz.

```python
from llama_index.core.llms import ChatMessage, CitationBlock

chat_history = [
    ChatMessage(
        role="system",
        # Statik bir sonuç döndüren sahte bir aracımız olduğu için LLM belirteçlerini boşa harcamak istemiyoruz
        content="Kullanıcı mesajı başına yalnızca bir arama sorgusu yapın.",
    ),
    ChatMessage(
        role="user", content="LlamaIndex ve LLM'ler birlikte nasıl çalışır?"
    ),
]
resp = llm.chat_with_tools([search_tool], chat_history=chat_history)
chat_history.append(resp.message)

tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)
while tool_calls:
    for tool_call in tool_calls:
        if tool_call.tool_name == "search_fn":
            tool_result = search_tool.call(tool_call.tool_kwargs)
            chat_history.append(
                ChatMessage(
                    role="tool",
                    blocks=tool_result.blocks,
                    additional_kwargs={"tool_call_id": tool_call.tool_id},
                )
            )

    resp = llm.chat_with_tools([search_tool], chat_history=chat_history)
    chat_history.append(resp.message)
    tool_calls = llm.get_tool_calls_from_response(
        resp, error_on_no_tool_call=False
    )

print(resp.message.content)
print("----" * 20)
for block in resp.message.blocks:
    if isinstance(block, CitationBlock):
        print("Kaynak: ", block.source)
        print("Başlık: ", block.title)
        print("Atıf Yapılan İçerik:\n", block.cited_content.text)
        print("----" * 20)
```

    Arama sonuçlarına dayanarak, LlamaIndex ve LLM'lerin birlikte nasıl çalıştığını açıklayabilirim:
    
    LlamaIndex, LLM uygulamaları oluşturmanıza yardımcı olacak bir "veri çerçevesidir"
    . Entegrasyon, temel bir zorluğu ele alarak çalışır: 
    LLM'ler bilgi üretimi ve muhakeme için olağanüstü bir teknoloji parçası olmalarına ve büyük miktarda halka açık veri üzerinde önceden eğitilmelerine rağmen, LLM'leri kendi özel verilerimizle güçlendirmek için kapsamlı bir araç setine ihtiyacımız vardır
    .
    
    LlamaIndex ve LLM'lerin birlikte çalışma şekli şöyledir:
    
    ## Veri Entegrasyonu
    
    LlamaIndex, mevcut veri kaynaklarınızı ve veri formatlarınızı (API'ler, PDF'ler, belgeler, SQL vb.) almak için veri bağlayıcıları sunar
    , bu da özel verilerinizi LLM'lerin çalışabileceği bir formata getirmenizi sağlar.
    
    ## Veri Yapılandırma
    
    LlamaIndex, bu verilerin LLM'lerle kolayca kullanılabilmesi için verilerinizi yapılandırma yolları (indeksler, grafikler) sağlar
    . Bu yapılandırma, verilerinizin LLM tarafından erişilebilir ve taranabilir olması için çok önemlidir.
    
    ## Gelişmiş Sorgulama
    
    LlamaIndex, verileriniz üzerinde gelişmiş bir erişim/sorgu arayüzü sağlar: Herhangi bir LLM giriş istemini besleyin, geri erişilen bağlamı ve bilgiyle güçlendirilmiş çıktıyı alın
    . Bu, LLM'e bir soru sorduğunuzda LlamaIndex'in verilerinizden ilgili bilgileri aldığı ve LLM'in yanıtını geliştirmek için bunu bağlam olarak sunduğu anlamına gelir.
    
    ## Uygulama Entegrasyonu
    
    LlamaIndex, dış uygulama çerçevenizle (örneğin LangChain, Flask, Docker, ChatGPT, başka herhangi bir şeyle) kolay entegrasyonlar sağlar
    , bu da mevcut sistemlere dahil edilmesini esnek hale getirir.
    
    Çerçeve, farklı seviyelerdeki kullanıcılara erişilebilir olacak şekilde tasarlanmıştır: 
    LlamaIndex'in üst düzey API'si, yeni başlayanların verilerini 5 satır kodla almalarına ve sorgulamalarına olanak tanırken, alt seviye API'ler uzmanların ihtiyaçlarına göre özelleştirme yapmasına izin verir
    --------------------------------------------------------------------------------
    Kaynak:  https://docs.llamaindex.ai
    Başlık:  LLM'ler ve LlamaIndex Hakkında Gerçekler
    Atıf Yapılan İçerik:
     
    Bağlam
    LLM'ler, bilgi oluşturma ve muhakeme için olağanüstü bir teknoloji parçasıdır.
    Büyük miktarda halka açık veri üzerinde önceden eğitilmişlerdir.
    LLM'leri kendi özel verilerimizle en iyi nasıl güçlendirebiliriz?
    LLM'ler için bu veri güçlendirmesini gerçekleştirmeye yardımcı olacak kapsamlı bir araç setine ihtiyacımız var.
    
    Önerilen Çözüm
    İşte LlamaIndex burada devreye giriyor. LlamaIndex, LLM uygulamaları oluşturmanıza yardımcı olacak bir "veri çerçevesidir". Şu araçları sağlar:
    
    Mevcut veri kaynaklarınızı ve veri formatlarınızı (API'ler, PDF'ler, belgeler, SQL vb.) almak için veri bağlayıcıları sunar.
    Verilerinizin LLM'lerle kolayca kullanılabilmesi için verilerinizi yapılandırma yolları (indeksler, grafikler) sağlar.
    Verileriniz üzerinde gelişmiş bir erişim/sorgu arayüzü sağlar:
    Herhangi bir LLM giriş istemini besleyin, geri erişilen bağlamı ve bilgiyle güçlendirilmiş çıktıyı alın.
    Dış uygulama çerçevenizle (örneğin LangChain, Flask, Docker, ChatGPT, başka herhangi bir şeyle) kolay entegrasyonlar sağlar.
    LlamaIndex hem başlangıç seviyesindeki kullanıcılar hem de ileri düzey kullanıcılar için araçlar sağlar.
    Üst düzey API'miz, yeni başlayanların LlamaIndex'i kullanarak verilerini 5 satır kodla almalarına ve sorgulamalarına olanak tanır. Alt seviye API'lerimiz, ileri düzey kullanıcıların herhangi bir modülü (veri bağlayıcıları, indeksler, alıcılar, sorgu motorları, yeniden sıralama modülleri) ihtiyaçlarına göre özelleştirmesine ve genişletmesine olanak tanır.
    
    --------------------------------------------------------------------------------
