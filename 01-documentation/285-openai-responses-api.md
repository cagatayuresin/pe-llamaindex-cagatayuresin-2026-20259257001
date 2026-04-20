# OpenAI Responses API

---
title: OpenAI Responses API
 | LlamaIndex OSS Documentation
---

Bu not defteri, OpenAI Responses LLM'nin nasıl kullanılacağını gösterir.

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
%pip install llama-index llama-index-llms-openai
```

## Temel Kullanım

```python
import os


os.environ["OPENAI_API_KEY"] = "..."
```

```python
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(
    model="gpt-4o-mini",
    # api_key="some key",  # varsayılan olarak OPENAI_API_KEY ortam değişkenini kullanır
)
```

#### Bir istemle `complete` çağrısı

```python
from llama_index.llms.openai import OpenAI


resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

```python
Paul Graham, startup hızlandırıcısı Y Combinator'ın kurucu ortağı olmasıyla tanınan önde gelen bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. Ayrıca teknoloji camiasındaki birçok kişiyi etkileyen teknoloji, startup'lar ve programlama üzerine yazdığı makaleleriyle de tanınır. Graham, Harvard Üniversitesi'nden doktora derecesi almış olup, programlama dilleri ve yapay zeka alanında bir geçmişe sahiptir. Çalışmaları, özellikle Silikon Vadisi'ndeki startup ekosistemini önemli ölçüde şekillendirmiştir. Çalışmalarının veya fikirlerinin belirli bir yönü hakkında daha fazla bilgi edinmek ister misiniz?
```

#### Bir mesaj listesiyle `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne"),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

```python
assistant: Ahoy, ahbap! Bana Kaptan Neşelısakal diyebilirsin, yedi denizde yelken açan en renkli korsan! Bugün seni gemime ne getirdi? Arrr!
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham kimdir?")
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Paul Graham, startup hızlandırıcısı Y Combinator'ın kurucu ortağı olmasıyla tanınan önde gelen bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. Ayrıca teknoloji camiasındaki birçok kişiyi etkileyen teknoloji, startup'lar ve programlama üzerine yazdığı makaleleriyle de tanınır. Graham'ın programlama dilleri ve yapay zeka alanında bir geçmişi vardır ve "Hackers and Painters" (Hacker'lar ve Ressamlar) dahil olmak üzere birkaç etkili eser kaleme almıştır. Girişimcilik ve inovasyon konusundaki içgörüleri onu Silikon Vadisi'nde saygın bir figür haline getirmiştir.
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Ahoy oradan! Bana Kaptan Neşelısakal diyebilirsin, yedi denizde yelken açan en renkli korsan! Bugün seni gemime ne getirdi?
```

## Parametreleri Yapılandır

Responses API birçok seçeneği destekler:

- Model adını ayarlama
- Sıcaklık (temperature), top_p, max_output_tokens gibi üretim parametreleri
- Yerleşik araç çağırmayı (built-in tool calling) etkinleştirme
- O-serisi modeller için akıl yürütme (reasoning) çabasını ayarlama
- Otomatik konuşma geçmişi için önceki yanıtları izleme
- Ve daha fazlası!

### Temel Parametreler

```python
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(
    model="gpt-4o-mini",
    temperature=0.5,  # varsayılan 0.1'dir
    max_output_tokens=100,  # varsayılan None'dır
    top_p=0.95,  # varsayılan 1.0'dır
)
```

### Yerleşik Araç Çağırma (Built-in Tool Calling)

Responses API, hakkında daha fazla bilgiyi [buradan](https://platform.openai.com/docs/guides/tools?api-mode=responses) okuyabileceğiniz yerleşik araç çağırmayı destekler.

Bunu yapılandırmak, LLM'nin aracı otomatik olarak çağıracağı ve yanıtı zenginleştirmek için kullanacağı anlamına gelir.

Araçlar, her biri bir araç için ayarlar içeren bir sözlük listesi olarak tanımlanır.

Aşağıda yerleşik web arama aracını kullanmaya yönelik bir örnek bulunmaktadır.

```python
from llama_index.llms.openai import OpenAIResponses
from llama_index.core.llms import ChatMessage


llm = OpenAIResponses(
    model="gpt-4o-mini",
    built_in_tools=[{"type": "web_search_preview"}],
)


resp = llm.chat(
    [ChatMessage(role="user", content="San Francisco'da hava nasıl?")]
)
print(resp)
print("========" * 2)
print(resp.additional_kwargs)
```

```python
assistant: 28 Mart 2025 Cuma günü saat 00:18 itibarıyla San Francisco'da mevcut hava durumu parçalı güneşli ve sıcaklık 61°F (16°C).


## San Francisco, CA için Hava Durumu:
Mevcut Koşullar: Parçalı güneşli, 61°F (16°C)


Günlük Tahmin:
* 27 Mart Perşembe: En Düşük: 52°F (11°C), En Yüksek: 61°F (16°C), Açıklama: Sabahın geç saatlerinde başlayan yağmur ve çisenti dönemleri; bu öğleden sonra rüzgarlı
* 28 Mart Cuma: En Düşük: 47°F (8°C), En Yüksek: 61°F (16°C), Açıklama: Sabah bölgede sağanak yağış; aksi takdirde yer yer güneşli bulutlu
* 29 Mart Cumartesi: En Düşük: 50°F (10°C), En Yüksek: 60°F (15°C), Açıklama: Çoğunlukla güneşli
* 30 Mart Pazar: En Düşük: 51°F (11°C), En Yüksek: 59°F (15°C), Açıklama: Bulutlu; sabah saatlerinde yağmur, öğleden sonra yer yer sağanak yağış
* 31 Mart Pazartesi: En Düşük: 49°F (10°C), En Yüksek: 58°F (14°C), Açıklama: Bulutlu ve serin; öğleden sonra birkaç sağanak yağış
* 1 Nisan Salı: En Düşük: 53°F (12°C), En Yüksek: 58°F (14°C), Açıklama: Giderek bulutlanan güneşli hava, rüzgarlı ve serin; öğleden sonra yer yer yağmur
* 2 Nisan Çarşamba: En Düşük: 52°F (11°C), En Yüksek: 56°F (13°C), Açıklama: Sabah saatlerinde birkaç sağanak yağış; aksi takdirde bulutlu ve serin


Mart ayında, San Francisco genellikle gündüzleri 61°F (16°C) ve geceleri 47°F (8°C) civarında sıcaklıklar yaşar. Şehir genellikle ay boyunca yaklaşık 11 gün süresince yaklaşık 3,5 inç (89 mm) yağış alır. ([weather2visit.com](https://www.weather2visit.com/north-america/united-states/san-francisco-march.htm?utm_source=openai))
================
{'built_in_tool_calls': [ResponseFunctionWebSearch(id='ws_67e5eaecce088191ab2edce452ef25420a24041ef7e917b2', status='completed', type='web_search_call')], 'annotations': [AnnotationURLCitation(end_index=1561, start_index=1439, title='San Francisco Weather in March 2025 | United States Averages | Weather-2-Visit', type='url_citation', url='https://www.weather2visit.com/north-america/united-states/san-francisco-march.htm?utm_source=openai')], 'usage': ResponseUsage(input_tokens=327, output_tokens=462, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=789, input_tokens_details={'cached_tokens': 0})}
```

## Akıl Yürütme Çabası (Reasoning Effort)

O-serisi modeller için, modelin akıl yürütmeye ayıracağı süreyi kontrol etmek için akıl yürütme çabasını ayarlayabilirsiniz.

Daha fazla bilgi için [OpenAI API dokümanlarına](https://platform.openai.com/docs/guides/reasoning?api-mode=responses) bakın.

```python
from llama_index.llms.openai import OpenAIResponses
from llama_index.core.llms import ChatMessage


llm = OpenAIResponses(
    model="o3-mini",
    reasoning_options={"effort": "high"},
)


resp = llm.chat(
    [ChatMessage(role="user", content="Hayatın anlamı nedir?")]
)
print(resp)
print("========" * 2)
print(resp.additional_kwargs)
```

```python
assistant: "Hayatın anlamı nedir?" sorusu tarih boyunca filozoflar, ilahiyatçılar, bilim insanları ve sayısız birey tarafından sorulmuştur ve herkesi tatmin eden tek bir kesin cevap yoktur. İşte cevabın neden bu kadar ucu açık olduğunu göstermeye yardımcı olan birkaç bakış açısı:


1. Felsefi ve Varoluşçu Görüşler:
• Jean-Paul Sartre ve Albert Camus gibi bazı varoluşçu düşünürler, hayatın önceden belirlenmiş bir anlamla gelmediğini savunurlar. Bunun yerine, kendi amaçlarını seçimler, ilişkiler ve kişisel projeler yoluyla oluşturmanın her bireyin kendisine bağlı olduğunu öne sürerler.
• Klasik felsefedekiler gibi diğer felsefeler, anlamlı bir yaşamın anahtarı olarak erdem, bilgi veya mutluluk arayışını vurgulamıştır.


2. Dini ve Manevi Perspektifler:
• Birçok dini gelenek, manevi inançlarına bağlı anlamlar sunar. Bu görüşlerde hayat; Tanrı'nın emirlerine göre yaşamak, aydınlanmaya ulaşmak veya reenkarnasyon yoluyla dersler çıkarmak anlamına gelse de, ruhsal bir büyüme, ahlaki gelişim veya ilahi bir planı gerçekleştirme yolculuğu olarak görülebilir.
• Manevi gelenekler genellikle takipçilerini sevgide, şefkatte ve başkalarına hizmette anlam bulmaya teşvik eder.


3. Bilimsel ve Doğal Yaklaşımlar:
• Biyolojik bir bakış açısıyla, hayatın amacının sadece hayatta kalmak ve üremek olduğu söylenebilir; bunlar doğal seçilimi ve evrimi yönlendiren temel mekanizmalardır.
• Bazıları, biyoloji yaşamın mekaniğini tanımlarken, insan bilincinin salt hayatta kalmanın ötesine geçmemize ve varlığımıza kişisel ve kültürel bir anlam yüklememize izin verdiğini savunur.


4. Kişisel ve Kültürel Yorumlar:
• Birçokları için anlam, günlük bağlantılarda bulunur: sevgi, yaratıcılık, öğrenme ve genel olarak topluma veya cemiyete katkıda bulunma.
• Farklı kültürler ve bireyler çeşitli değerlere (başarı, şefkat veya keşif gibi) öncelik verebilir, bu da "anlam"ın birinin yetiştirilme tarzına, deneyimlerine ve kişisel yansımalarına bağlı olarak büyük ölçüde değişebileceği anlamına gelir.


5. Mizahi Bir Yaklaşım:
• Popüler kültürde, özellikle Douglas Adams'ın Otostopçunun Galaksi Rehberi'nde, hayatın nihai sorusunun cevabının "42" olduğu meşhurdur; bu, asıl önemin tek bir cevaba ulaşmaktan ziyade sorgulama yolculuğunun kendisinde yattığına dair eğlenceli bir hatırlatmadır.


Sonuç olarak, hayatın anlamı mutlak bir gerçeklikten ziyade, sizin için en önemli olanı keşfetmeye, sorgulamaya ve tanımlamaya yönelik bir davet olarak kabul edilebilir. İster ilişkiler, ister yaratıcı uğraşlar, entelektüel zorluklar veya manevi uygulamalar yoluyla olsun, birçoğu uçsuz bucaksız ve karmaşık bir evrende kendi anlamımızı yaratma gücüne sahip olduğumuza inanıyor.
================
{'built_in_tool_calls': [], 'reasoning': ResponseReasoningItem(id='rs_683e2dde0e308198a72c5e7f2e9bf52a0dd2faa5908183b8', summary=[], type='reasoning', encrypted_content=None, status=None), 'annotations': [], 'usage': ResponseUsage(input_tokens=13, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=841, output_tokens_details=OutputTokensDetails(reasoning_tokens=320), total_tokens=854)}
```

## Görüntü Desteği

OpenAI, birçok model için sohbet mesajlarının girişinde görüntü desteğine sahiptir.

Mesajların içerik blokları (content blocks) özelliğini kullanarak, metin ve görüntüleri tek bir LLM isteminde kolayca birleştirebilirsiniz.

```python
!wget https://cdn.pixabay.com/photo/2016/07/07/16/46/dice-1502706_640.jpg -O image.png
```

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(model="gpt-4o")


messages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.png"),
            TextBlock(text="Görüntüyü birkaç cümleyle tanımla."),
        ],
    )
]


resp = llm.chat(messages)
print(resp.message.content)
```

```python
Görüntü, kareli bir yüzeyin üzerinde havada yakalanmış siyah noktalı üç beyaz zarı göstermektedir. Zarlar farklı yönlerde durmakta ve farklı nokta sayılarını sergilemektedir. Arka plan karanlıktır ve zarları aydınlatan hafif bir ışık dramatik bir etki yaratmaktadır. Kareli yüzey bir satranç veya dama tahtasına benzemektedir.
```

## Fonksiyon/Araç Çağırma Kullanımı

OpenAI modelleri, fonksiyon çağırma (function calling) için yerel desteğe sahiptir. Bu, LlamaIndex araç soyutlamalarıyla uygun şekilde entegre olur ve herhangi bir rastgele Python fonksiyonunu LLM'ye bağlamanıza olanak tanır.

Aşağıdaki örnekte, bir Şarkı (Song) nesnesi oluşturmak için bir fonksiyon tanımlıyoruz.

```python
from pydantic import BaseModel
from llama_index.core.tools import FunctionTool




class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""


    name: str
    artist: str




def generate_song(name: str, artist: str) -> Song:
    """Verilen ad ve sanatçı ile bir şarkı oluşturur."""
    return Song(name=name, artist=artist)




tool = FunctionTool.from_defaults(fn=generate_song)
```

`strict` parametresi, OpenAI'ye araç çağrıları/yapılandırılmış çıktılar oluştururken kısıtlı örnekleme kullanıp kullanmayacağını bildirir. Bu, oluşturulan araç çağrısı şemasının her zaman beklenen alanları içereceği anlamına gelir.

Bunun gecikmeyi (latency) artırdığı görüldüğünden, varsayılan olarak false (yanlış) değerine ayarlanmıştır.

```python
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(model="gpt-4o-mini", strict=True)
response = llm.predict_and_call(
    [tool],
    "Benim için rastgele bir şarkı yaz",
    # strict=True  # sınıfı geçersiz kılmak için fonksiyon düzeyinde de ayarlanabilir
)
print(str(response))
```

```python
name='Chasing Stars' artist='Luna Sky'
```

Ayrıca birden fazla fonksiyon çağırma da yapabiliriz.

```python
llm = OpenAIResponses(model="gpt-4o-mini")
response = llm.predict_and_call(
    [tool],
    "Beatles'dan beş şarkı oluştur",
    allow_parallel_tool_calls=True,
)
for s in response.sources:
    print(f"Ad: {s.tool_name}, Girdi: {s.raw_input}, Çıktı: {str(s)}")
```

```python
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Hey Jude', 'artist': 'The Beatles'}}, Çıktı: name='Hey Jude' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Let It Be', 'artist': 'The Beatles'}}, Çıktı: name='Let It Be' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Come Together', 'artist': 'The Beatles'}}, Çıktı: name='Come Together' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Yesterday', 'artist': 'The Beatles'}}, Çıktı: name='Yesterday' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Twist and Shout', 'artist': 'The Beatles'}}, Çıktı: name='Twist and Shout' artist='The Beatles'
```

### Manuel Araç Çağırma

Bir aracın nasıl çağrıldığını kontrol etmek istiyorsanız, araç çağırma ve araç seçimini kendi adımlarına ayırabilirsiniz.

İlk olarak, bir araç seçelim.

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(model="gpt-4o-mini")


chat_history = [ChatMessage(role="user", content="Benim için rastgele bir şarkı yaz")]


resp = llm.chat_with_tools([tool], chat_history=chat_history)
```

Şimdi, LLM'nin seçtiği aracı çağıralım (varsa).

Bir araç çağrısı varsa, final yanıtını (veya başka bir araç çağrısını!) oluşturmak için sonuçları LLM'ye göndermeliyiz.

```python
tools_by_name = {t.metadata.name: t for t in [tool]}
tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)


while tool_calls:
    # LLM'nin yanıtını sohbet geçmişine ekleyin
    chat_history.append(resp.message)


    for tool_call in tool_calls:
        tool_name = tool_call.tool_name
        tool_kwargs = tool_call.tool_kwargs


        print(f"{tool_name} şu argümanlarla çağrılıyor: {tool_kwargs}")
        tool_output = tool(**tool_kwargs)
        chat_history.append(
            ChatMessage(
                role="tool",
                content=str(tool_output),
                # OpenAI gibi çoğu LLM'nin araç çağrısı kimliğini bilmesi gerekir
                additional_kwargs={"call_id": tool_call.tool_id},
            )
        )


        resp = llm.chat_with_tools([tool], chat_history=chat_history)
        tool_calls = llm.get_tool_calls_from_response(
            resp, error_on_no_tool_call=False
        )
```

```python
Calling generate_song with {'name': 'Chasing Stars', 'artist': 'Luna Sky'}
```

Şimdi, final bir yanıtımız olmalı!

```python
print(resp.message.content)
```

```python
İşte senin için **Luna Sky**'dan **"Chasing Stars"** adlı bir şarkı!


### Chasing Stars


**Bölüm 1**
Gece yarısı parıltısında, özgürce dolaşıyoruz,
Ateş böcekleri gibi hayallerle, denizi aydınlatıyoruz.
Gecenin fısıltıları, isimlerimizi haykırıyor,
Birlikte tutuşturacağız bu vahşi, evcilleşmemiş alevi.


**Nakarat**
Yıldızları kovalıyoruz, sonsuz gece boyunca,
Her kalp atışıyla uçuşa geçeceğiz.
El ele, karanlığı yaracağız,
Bu kozmik dansta, izimizi bırakacağız.


**Bölüm 2**
Ayın altında, yavaşça paylaşılan sırlar,
Her bakış bir söz, her dokunuş bir meydan okuma.
Evren bizim, yolculuk başlasın,
Attığımız her adımla bir sanat boyuyoruz.


**Nakarat**
Yıldızları kovalıyoruz, sonsuz gece boyunca,
Her kalp atışıyla uçuşa geçeceğiz.
El ele, karanlığı yaracağız,
Bu kozmik dansta, izimizi bırakacağız.


**Köprü**
Ve şafak vakti geldiğinde, hâlâ burada olacağız,
Kahkahalarımızın yankılarıyla, cam gibi berrak.
Nereye gidersek gidelim, ne kadar uzak olursa olsun,
Sonsuza dek kalbimizde o yıldızları kovalayacağız.


**Nakarat**
Yıldızları kovalıyoruz, sonsuz gece boyunca,
Her kalp atışıyla uçuşa geçeceğiz.
El ele, karanlığı yaracağız,
Bu kozmik dansta, izimizi bırakacağız.


**Çıkış**
Öyleyse yıldızları kovalayalım, yolu aydınlatalım,
Bu güzel yolculukta asla sapmayacağız.
Pusulamız hayallerimiz, rehberimiz sevgimiz,
Birlikte yan yana yükseleceğiz.


Herhangi bir değişiklik veya başka bir şarkı isterseniz bana bildirmekten çekinmeyin!
```

## Yapılandırılmış Tahmin (Structured Prediction)

Fonksiyon çağırmanın önemli bir kullanım durumu da yapılandırılmış nesnelerin çıkarılmasıdır. LlamaIndex, herhangi bir LLM'yi yapılandırılmış bir LLM'ye dönüştürmek için sezgisel bir arayüz sağlar - sadece hedef Pydantic sınıfını tanımlayın (içiçe olabilir) ve bir istem verildiğinde istediğiniz nesneyi çıkaralım.

```python
from llama_index.llms.openai import OpenAIResponses
from llama_index.core.prompts import PromptTemplate
from pydantic import BaseModel
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




llm = OpenAIResponses(model="gpt-4o-mini")
prompt_tmpl = PromptTemplate(
    "Verilen {city_name} şehri için bir restoran oluşturun"
)
# Seçenek 1: `as_structured_llm` kullanın
restaurant_obj = (
    llm.as_structured_llm(Restaurant)
    .complete(prompt_tmpl.format(city_name="Dallas"))
    .raw
)
# Seçenek 2: `structured_predict` kullanın
# restaurant_obj = llm.structured_predict(Restaurant, prompt_tmpl, city_name="Miami")
```

```python
restaurant_obj
```

```python
Restaurant(name='Tex-Mex Delight', city='Dallas', cuisine='Tex-Mex', menu_items=[MenuItem(course_name='Tacos', is_vegetarian=False), MenuItem(course_name='Vejetaryen Enchiladas', is_vegetarian=True), MenuItem(course_name='Fajitas', is_vegetarian=False), MenuItem(course_name='Cips ve Salsa', is_vegetarian=True), MenuItem(course_name='Peynir Sosu', is_vegetarian=True)])
```

## Asenkron (Async)

```python
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(model="gpt-4o")
```

```python
resp = await llm.acomplete("Paul Graham kimdir?")
```

```python
print(resp)
```

```python
Paul Graham, İngiliz-Amerikalı bir girişimci, risk sermayedaridir ve denemecidir. En çok, Yahoo'ya satılan ve Yahoo Store haline gelen ilk web tabanlı uygulamalardan biri olan Viaweb'in kurucu ortağı olarak tanınır. Graham aynı zamanda Dropbox, Airbnb ve Reddit dahil olmak üzere çok sayıda başarılı girişimi finanse eden ve destekleyen etkili bir startup hızlandırıcısı olan Y Combinator'ın kurucu ortağıdır. Teknoloji ve girişimcilikteki çalışmalarına ek olarak, programlama, girişimcilik ve çalışma felsefesi gibi konulardaki derinlikli denemeleriyle de tanınır.
```

```python
resp = await llm.astream_complete("Paul Graham kimdir?")
```

```python
async for delta in resp:
    print(delta.delta, end="")
```

```python
Paul Graham, İngiliz-Amerikalı bir girişimci, risk sermayedaridir ve denemecidir. En çok, Yahoo'ya satılan ve Yahoo Store haline gelen ilk web tabanlı uygulamalardan biri olan Viaweb'in kurucu ortağı olarak tanınır. Graham aynı zamanda Dropbox, Airbnb ve Reddit dahil olmak üzere çok sayıda başarılı girişimi finanse eden ve destekleyen etkili bir startup hızlandırıcısı olan Y Combinator'ın kurucu ortağıdır. Teknoloji ve girişimcilikteki çalışmalarına ek olarak, programlama, girişimcilik ve toplumla ilgili konulardaki derinlikli denemeleriyle de tanınır.
```

Asenkron fonksiyon çağırma da desteklenmektedir.

```python
llm = OpenAIResponses(model="gpt-4o-mini")
response = await llm.apredict_and_call([tool], "Rastgele bir şarkı oluştur")
print(str(response))
```

```python
name='Chasing Stars' artist='Luna Sky'
```

## Ek Argümanlar (Additional kwargs)

Yapılandırıcıda (constructor) bulunmayan ek argümanlar varsa, bunları `additional_kwargs` ile örnek düzeyinde ayarlayabilirsiniz.

Bunlar LLM'ye yapılan her çağrıya iletilecektir.

```python
from llama_index.llms.openai import OpenAIResponses


llm = OpenAIResponses(
    model="gpt-4o-mini", additional_kwargs={"user": "kullanici_id_niz"}
)
resp = llm.complete("Paul Graham kimdir?")
print(resp)
```

## Görüntü oluşturma (Image generation)

[Görüntü oluşturma](https://platform.openai.com/docs/guides/image-generation?image-generation-model=gpt-image-1#generate-images) özelliğini, yerleşik bir araç olarak `{'type': 'image_generation'}` veya akışı etkinleştirmek istiyorsanız `{'type': 'image_generation', 'partial_images': 2}` parametrelerini geçirerek kullanabilirsiniz:

```python
import base64
from llama_index.llms.openai import OpenAIResponses
from llama_index.core.llms import ChatMessage, ImageBlock, TextBlock


# Akış olmadan çalıştır
llm = OpenAIResponses(
    model="gpt-4.1-mini", built_in_tools=[{"type": "image_generation"}]
)
messages = [
    ChatMessage.from_str(
        content="Çayırda kediyle dans eden bir lama", role="user"
    )
]
response = llm.chat(
    messages
)  # asenkron bir uygulama için: response = await llm.achat(messages)
for block in response.message.blocks:
    if isinstance(block, ImageBlock):
        with open("dans_eden_lama_ve_kedi.png", "wb") as f:
            f.write(base64.b64decode(block.image))
    elif isinstance(block, TextBlock):
        print(block.text)


# Akış ile çalıştır
llm_stream = OpenAIResponses(
    model="gpt-4.1-mini",
    built_in_tools=[{"type": "image_generation", "partial_images": 2}],
)
response = llm_stream.stream_chat(
    messages
)  # asenkron bir uygulama için: response = await llm_stream.asteam_chat(messages)
for event in response:
    for block in event.message.blocks:
        if isinstance(block, ImageBlock):
            # block.detail görüntünün kimliğini (ID) içerir
            with open(f"dans_eden_lama_ve_kedi_{block.detail}.png", "wb") as f:
                f.write(base64.b64decode(block.image))
        elif isinstance(block, TextBlock):
            print(block.text)
```

## MCP Uzak Çağrıları (MCP Remote calls)

MCP ayrıntılarını LLM'ye yerleşik bir araç olarak geçirerek OpenAI Responses API aracılığıyla herhangi bir [uzak MCP](https://platform.openai.com/docs/guides/tools-remote-mcp)'yi çağırabilirsiniz.

```python
from llama_index.llms.openai import OpenAIResponses
from llama_index.core.llms import ChatMessage


llm = OpenAIResponses(
    model="gpt-4.1",
    built_in_tools=[
        {
            "type": "mcp",
            "server_label": "deepwiki",
            "server_url": "https://mcp.deepwiki.com/mcp",
            "require_approval": "never",
        }
    ],
)
messages = [
    ChatMessage.from_str(
        content="MCP spesifikasyonunun 2025-03-26 sürümünde hangi taşıma protokolleri destekleniyor?",
        role="user",
    )
]
response = llm.chat(messages)
# metin çıktısını gör
print(response.message.content)
# MCP araç çağrısını gör
print(response.raw.output[0])
```

## Kod Yorumlayıcı (Code interpreter)

[Kod Yorumlayıcıyı (Code Interpreter)](https://platform.openai.com/docs/guides/tools-code-interpreter) sadece yerleşik bir araç olarak `"type": "code_interpreter", "container": { "type": "auto" }` ayarını yaparak kullanabilirsiniz.

```python
from llama_index.llms.openai import OpenAIResponses
from llama_index.core.llms import ChatMessage


llm = OpenAIResponses(
    model="gpt-4.1",
    built_in_tools=[
        {
            "type": "code_interpreter",
            "container": {"type": "auto"},
        }
    ],
)
messages = [
    ChatMessage.from_str(
        content="3x + 11 = 14 denklemini çözmem gerekiyor. Bana yardım edebilir misin?",
        role="user",
    )
]
response = llm.chat(messages)
# metin çıktısını gör
print(response.message.content)
# MCP araç çağrısını gör (Kod yorumlayıcı çağrısı)
print(response.raw.output[0])
```
