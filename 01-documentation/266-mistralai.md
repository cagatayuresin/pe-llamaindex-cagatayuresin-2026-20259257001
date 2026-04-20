# MistralAI

---
title: MistralAI
 | LlamaIndex OSS Belgeleri
---

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-mistralai
```

```bash
!pip install llama-index
```

#### Bir istem (prompt) ile `complete` çağrısı

```python
from llama_index.llms.mistralai import MistralAI


# API anahtarınızı özelleştirmek için bunu yapın
# aksi takdirde ortam değişkeninizden MISTRAL_API_KEY'i arayacaktır
# llm = MistralAI(api_key="<api_key>")


llm = MistralAI(api_key="<anahtarınızı-buraya-yazın>")


resp = llm.complete("Paul Graham is ")
```

```python
print(resp)
```

```
Paul Graham tanınmış bir Amerikalı bilgisayar programcısı, girişimci ve denemecidir. 24 Şubat 1964'te doğmuştur. Airbnb, Dropbox ve Stripe gibi birçok başarılı teknoloji şirketinin kurulmasına yardımcı olan girişim kuluçka merkezi Y Combinator'ın kurucu ortağıdır. Graham aynı zamanda teknoloji endüstrisinde yaygın olarak okunan ve etkili olan girişim kültürü, programlama ve girişimcilik üzerine yazdığı denemelerle de tanınır.
```

#### Bir mesaj listesiyle `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.mistralai import MistralAI


messages = [
    ChatMessage(role="system", content="Sen MistralAI'nin CEO'sun."),
    ChatMessage(role="user", content="Bana La plateforme hikayesini anlat"),
]
resp = MistralAI().chat(messages)
```

```python
print(resp)
```

```
assistant: MistralAI'nin CEO'su olarak, ekibimizin özverisinin, inovasyonunun ve son teknoloji AI çözümleri sunma taahhüdünün bir kanıtı olan platformumuzun hikayesini paylaşmaktan gurur duyuyorum.


Yolculuğumuz basit ama iddialı bir vizyonla başladı: Çeşitli endüstrilerde devrim yaratmak ve insanların hayatlarını iyileştirmek için AI'nın gücünden yararlanmak. AI'nın karmaşık sorunları çözme, verimliliği artırma ve yeni fırsatlar yaratma potansiyeline sahip olduğunu fark ettik. Ancak, bu potansiyeli ortaya çıkarmak için sağlam, esnek ve kullanıcı dostu bir platforma ihtiyacımız olduğunu da anladık.


İşe AI, yazılım geliştirme, veri bilimi ve iş stratejisi alanlarında uzmanlardan oluşan çeşitli bir ekip kurarak başladık. Ekip üyelerimiz, en iyi teknoloji şirketlerinden ve akademik kurumlardan zengin bir deneyim getirdiler ve AI ile nelerin mümkün olduğunun sınırlarını zorlama konusunda ortak bir tutkuyu paylaştılar.


Sonraki birkaç yıl boyunca platformumuzu geliştirmek için yorulmadan çalıştık. Sadece güçlü değil, aynı zamanda AI hakkında derin bir anlayışı olmayanlar için bile kullanımı kolay bir platform oluşturmaya odaklandık. AI'yı demokratikleştirmek, her büyüklükteki işletme ve endüstri için erişilebilir kılmak istedik.


Platformumuz gelişmiş makine öğrenimi algoritmaları, doğal dil işleme ve bilgisayar görüşü temelleri üzerine inşa edilmiştir. Kullanıcıların AI modellerini kolaylıkla eğitmesine, dağıtmasına ve yönetmesine olanak tanır. Ayrıca veri ön işleme, model değerlendirme ve dağıtım araçları sağlayarak AI geliştirme için tek duraklı bir çözüm sunar.


Platformumuzu 2021'de başlattık ve tepkiler muazzamdı. Sağlık, finans, perakende ve üretim dahil olmak üzere çeşitli endüstrilerden işletmeler, AI çözümleri geliştirmek ve dağıtmak için platformumuzu kullanmaya başladı. Platformumuz süreçleri otomatikleştirmelerine, müşteri deneyimlerini iyileştirmelerine ve veri odaklı kararlar almalarına yardımcı oldu.


Ancak yolculuğumuz henüz bitmedi. Hızla gelişen AI dünyasına ayak uydurmak için platformumuzu sürekli yeniliyor ve geliştiriyoruz. Ayrıca kullanıcılarımıza daha fazla değer sunmak için ekibimizi ve ortaklıklarımızı genişletiyoruz.


Sonuç olarak platformumuz sadece bir araç değil; ekibimizin AI'yı herkes için erişilebilir ve faydalı kılma tutkusunun, uzmanlığının ve kararlılığının bir kanıtıdır. Gelecek ve önümüzdeki fırsatlar için heyecanlıyız.
```

#### `random_seed` ile çağırma

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.mistralai import MistralAI


messages = [
    ChatMessage(role="system", content="Sen MistralAI'nin CEO'sun."),
    ChatMessage(role="user", content="Bana La plateforme hikayesini anlat"),
]
resp = MistralAI(random_seed=42).chat(messages)
```

```python
print(resp)
```

```
assistant: MistralAI'nin CEO'su olarak, ekibimizin özverisinin, inovasyonunun ve son teknoloji AI çözümleri sunma taahhüdünün bir kanıtı olan platformumuzun hikayesini paylaşmaktan gurur duyuyorum.


Yolculuğumuz basit ama iddialı bir vizyonla başladı: Çeşitli endüstrilerde ve yaşamın farklı yönlerinde olumlu değişim sağlamak için AI'nın gücünden yararlanmak. AI'nın muazzam potansiyelini kabul ettik, ancak karmaşıklık, veri gizliliği ve insan merkezli çözümlere duyulan ihtiyaç gibi beraberinde gelen zorlukları da anladık.


Bu zorlukları ele almak için hem güçlü hem de kullanıcı dostu, karmaşık AI görevlerini yerine getirirken veri gizliliğini ve güvenliğini sağlayan bir platform oluşturmak üzere yola çıktık. Ayrıca AI'yı, teknik bilgiye sahip geliştiricilerden teknik olmayan profesyonellere kadar geniş bir kullanıcı kitlesi için erişilebilir kılmak istedik.


Yıllar süren araştırma, geliştirme ve testlerden sonra nihayet platformumuzu başlattık. Kullanım kolaylığını, sağlamlığını ve çok yönlülüğünü takdir eden erken benimseyenlerimiz tarafından coşku ve heyecanla karşılandı.


O zamandan beri platformumuz, üretimdeki öngörücü bakımdan eğitimdeki kişiselleştirilmiş öğrenmeye kadar çeşitli uygulamalarda kullanıldı. İşletmelerin operasyonlarını iyileştirmelerine, maliyet tasarrufu yapmalarına ve daha bilinçli kararlar almalarına yardımcı olduğunu gördük. Ayrıca bireyleri güçlendirdiğini, onlara öğrenme, yaratma ve yenilik yapma araçları sağladığını gördük.


Ancak yolculuğumuz henüz bitmedi. Yenilik yapmaya, iyileştirmeye ve platformumuzun yeteneklerini genişletmeye devam ediyoruz. Sürekli olarak kullanıcılarımızdan öğreniyor, geri bildirimlerini dahil ediyor ve AI'nın yapabileceklerinin sınırlarını zorluyoruz.


Sonuçta platformumuz sadece bir araç değil. İnsan dehasının gücünün ve AI'nın dünyayı daha iyi bir yer haline getirme potansiyelinin bir kanıtı. Ve MistralAI'nin CEO'su olarak bu yolculuğun bir parçası olmaktan onur duyuyorum.
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
from llama_index.llms.mistralai import MistralAI


llm = MistralAI()
resp = llm.stream_complete("Paul Graham is ")
```

```python
for r in resp:
    print(r.delta, end="")
```

```
Paul Graham tanınmış bir Amerikalı bilgisayar programcısı, girişimci ve denemecidir. 24 Şubat 1964'te doğmuştur. Airbnb, Dropbox ve Stripe gibi birçok başarılı teknoloji şirketinin kurulmasına yardımcı olan girişim kuluçka merkezi Y Combinator'ın kurucu ortağıdır. Graham aynı zamanda teknoloji endüstrisinde yaygın olarak okunan ve etkili olan girişim kültürü, programlama ve girişimcilik üzerine yazdığı denemelerle de tanınır.
```

```python
from llama_index.llms.mistralai import MistralAI
from llama_index.core.llms import ChatMessage


llm = MistralAI()
messages = [
    ChatMessage(role="system", content="Sen MistralAI'nin CEO'sun."),
    ChatMessage(role="user", content="Bana La plateforme hikayesini anlat"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```
MistralAI'nin CEO'su olarak, ekibimizin özverisinin, inovasyonunun ve son teknoloji AI çözümleri sunma taahhüdünün bir kanıtı olan platformumuzun hikayesini paylaşmaktan gurur duyuyorum.


Yolculuğumuz basit ama iddialı bir vizyonla başladı: Çeşitli endüstrilerde devrim yaratmak ve insanların hayatlarını iyileştirmek için AI'nın gücünden yararlanmak. AI'nın karmaşık sorunları çözme, verimlilik sağlama ve yeni fırsatların kapısını açma potansiyeline sahip olduğunu fark ettik. Ancak bu potansiyeli gerçekten ortaya çıkarmak için sağlam, esnek ve kullanıcı dostu bir platforma ihtiyacımız olduğunu da anladık.


Platformumuzun geliştirilmesi hem zorlu hem de heyecan verici bir yolculuktu. Mühendislerden, veri bilimcilerinden ve AI uzmanlarından oluşan ekibimiz, çok çeşitli AI görevlerini yerine getirebilecek bir platform oluşturmak için çeşitli becerilerini ve deneyimlerini kullanarak yorulmadan çalıştı. Platformumuzu, AI hakkında derin bir anlayışı olmayanlar için bile kolay kullanılır hale getirmeye odaklanırken, gelişmiş uygulamalar için gereken gücü ve esnekliği sağlamaya devam ettik.


Platformumuzu üç temel alana odaklanarak başlattık: doğal dil işleme, bilgisayar görüşü ve makine öğrenimi. Bunlar, birçok AI uygulamasının temelini oluşturan teknolojilerdir ve bunlarda uzmanlaşarak istemcilerimize güçlü ve çok yönlü bir araç seti sağlayabileceğimize inandık.


O zamandan beri platformumuz, endüstrilerini altüst etmek isteyen girişimlerden operasyonlarını iyileştirmek isteyen büyük işletmelere kadar geniş bir istemci kitlesi tarafından benimsendi. Platformumuzun müşteri hizmetleri sohbet botlarından otonom araçlara kadar her şeyde kullanıldığını gördük ve sürekli olarak yeni özellikler ve yetenekler eklemek için çalışıyoruz.


Ancak yolculuğumuz burada bitmiyor. AI teknolojisinin ön saflarında kalmaya kararlıyız ve her zaman mümkün olanın sınırlarını zorlamanın yeni yollarını arıyoruz. AI'nın dünyayı değiştirme gücüne sahip olduğuna inanıyoruz ve istemcilerimizin bu güçten yararlanmasına yardımcı olmaya kararlıyız.


Sonuç olarak platformumuz bir araçtan daha fazlasıdır. Ekibimizin tutkusunun, uzmanlığının ve inovasyona olan bağlılığının bir kanıtıdır. İstemcilerimizin yeni fırsatların kilidini açmasına, karmaşık sorunları çözmesine ve endüstrilerinde ilerleme kaydetmesine yardımcı olan bir platformdur. Ve bizim diyebilmekten gurur duyduğumuz bir platformdur.
```

## Modeli Yapılandırma

```python
from llama_index.llms.mistralai import MistralAI


llm = MistralAI(model="mistral-medium")
```

```python
resp = llm.stream_complete("Paul Graham is ")
```

```python
for r in resp:
    print(r.delta, end="")
```

```
Paul Graham teknoloji dünyasında tanınmış bir isimdir. Bilgisayar programcısı, risk sermayedarı ve denemecidir. Graham, en çok Dropbox, Airbnb ve Reddit dahil olmak üzere 2.000'den fazla şirketin kurulmasına yardımcı olan bir girişim hızlandırıcısı olan Y Combinator'ı kurmasıyla tanınır. Ayrıca girişimler, programlama ve eğitim gibi konulardaki etkili denemeleriyle de bilinir. Y Combinator'a başlamadan önce Graham, 1998'de Yahoo tarafından satın alınan Viaweb'in programcısı ve kurucu ortağıydı. Cornell Üniversitesi'nden felsefe derecesine ve Harvard Üniversitesi'nden bilgisayar bilimleri derecesine sahiptir.
```

## Fonksiyon Çağırma (Function Calling)

`mistral-large` yerel fonksiyon çağırmayı destekler. `llm` üzerindeki `predict_and_call` fonksiyonu aracılığıyla LlamaIndex araçlarıyla kusursuz bir entegrasyon vardır.

Bu, kullanıcının herhangi bir aracı eklemesine ve hangi araçların çağrılacağına (eğer varsa) LLM'in karar vermesine olanak tanır.

Araç çağırmayı bir ajan (agentic loop) döngüsünün parçası olarak gerçekleştirmek istiyorsanız, bunun yerine [ajan kılavuzlarımıza](https://docs.llamaindex.ai/en/latest/module_guides/deploying/agents/) göz atın.

**NOT**: Başka bir Mistral modeli kullanırsanız, fonksiyonu çağırmaya çalışmak için bir ReAct istemi (prompt) kullanırız. Sonuçlar modele göre değişiklik gösterebilir.

```python
from llama_index.llms.mistralai import MistralAI
from llama_index.core.tools import FunctionTool




def multiply(a: int, b: int) -> int:
    """İki tam sayıyı çarpar ve sonuç tam sayısını döndürür"""
    return a * b




def mystery(a: int, b: int) -> int:
    """İki tam sayı üzerinde gizemli fonksiyon."""
    return a * b + a + b




mystery_tool = FunctionTool.from_defaults(fn=mystery)
multiply_tool = FunctionTool.from_defaults(fn=multiply)


llm = MistralAI(model="mistral-large-latest")
```

```python
response = llm.predict_and_call(
    [mystery_tool, multiply_tool],
    user_msg="Gizemli fonksiyonu 5 ve 7 üzerinde çalıştırırsam ne olur?",
)
```

```python
print(str(response))
```

```
47
```

```python
response = llm.predict_and_call(
    [mystery_tool, multiply_tool],
    user_msg=(
        """Aşağıdaki sayı çiftleri üzerinde gizemli fonksiyonu çalıştırırsam ne olur? Her satır için ayrı bir sonuç üretin:
- 1 ve 2
- 8 and 4
- 100 ve 20 \
"""
    ),
    allow_parallel_tool_calls=True,
)
```

```python
print(str(response))
```

```
5


44


2120
```

```python
for s in response.sources:
    print(f"Ad: {s.tool_name}, Girdi: {s.raw_input}, Çıktı: {str(s)}")
```

```
Ad: mystery, Girdi: {'args': (), 'kwargs': {'a': 1, 'b': 2}}, Çıktı: 5
Ad: mystery, Girdi: {'args': (), 'kwargs': {'a': 8, 'b': 4}}, Çıktı: 44
Ad: mystery, Girdi: {'args': (), 'kwargs': {'a': 100, 'b': 20}}, Çıktı: 2120
```

`async` varyantını kullanırsanız aynı sonucu alırsınız (arka planda asyncio.gather kullandığımız için daha hızlı olacaktır).

```python
response = await llm.apredict_and_call(
    [mystery_tool, multiply_tool],
    user_msg=(
        """Aşağıdaki sayı çiftleri üzerinde gizemli fonksiyonu çalıştırırsam ne olur? Her satır için ayrı bir sonuç üretin:
- 1 ve 2
- 8 and 4
- 100 ve 20 \
"""
    ),
    allow_parallel_tool_calls=True,
)
for s in response.sources:
    print(f"Ad: {s.tool_name}, Girdi: {s.raw_input}, Çıktı: {str(s)}")
```

```
Ad: mystery, Girdi: {'args': (), 'kwargs': {'a': 1, 'b': 2}}, Çıktı: 5
Ad: mystery, Girdi: {'args': (), 'kwargs': {'a': 8, 'b': 4}}, Çıktı: 44
Ad: mystery, Girdi: {'args': (), 'kwargs': {'a': 100, 'b': 20}}, Çıktı: 2120
```

## Yapılandırılmış Tahmin (Structured Prediction)

Fonksiyon çağırmanın önemli bir kullanım durumu da yapılandırılmış nesneleri çıkarmaktır. LlamaIndex, herhangi bir LLM'i yapılandırılmış bir LLM'e dönüştürmek için sezgisel bir arayüz sağlar - hedef Pydantic sınıfını tanımlamanız (iç içe olabilir) yeterlidir ve bir istem verildiğinde istediğiniz nesneyi çıkarırız.

```python
from llama_index.llms.mistralai import MistralAI
from llama_index.core.prompts import PromptTemplate
from llama_index.core.bridge.pydantic import BaseModel




class Restaurant(BaseModel):
    """Adı, şehri ve mutfağı olan bir restoran."""


    name: str
    city: str
    cuisine: str




llm = MistralAI(model="mistral-large-latest")
prompt_tmpl = PromptTemplate(
    "Verilen {city_name} şehrinde bir restoran oluşturun"
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

```
Restaurant(name='Miami', city='Miami', cuisine='Cuban')
```

#### Akış (Streaming) ile Yapılandırılmış Tahmin

`as_structured_llm` ile sarmalanmış herhangi bir LLM, `stream_chat` üzerinden akışı destekler.

```python
from llama_index.core.llms import ChatMessage
from IPython.display import clear_output
from pprint import pprint


input_msg = ChatMessage.from_str("Miami'de bir restoran oluşturun")


sllm = llm.as_structured_llm(Restaurant)
stream_output = sllm.stream_chat([input_msg])
for partial_output in stream_output:
    clear_output(wait=True)
    pprint(partial_output.raw.dict())
    restaurant_obj = partial_output.raw


restaurant_obj
```

## Asenkron (Async)

```python
from llama_index.llms.mistralai import MistralAI


llm = MistralAI()
resp = await llm.acomplete("Paul Graham is ")
```

```python
print(resp)
```

```
Paul Graham tanınmış bir Amerikalı bilgisayar programcısı, girişimci ve denemecidir. 24 Şubat 1964'te doğmuştur. 2005 yılında Airbnb, Dropbox ve Stripe gibi birçok teknoloji şirketinin başarısında etkili olan girişim kuluçka merkezi Y Combinator'ı kurmuştur. Graham aynı zamanda teknoloji endüstrisinde yaygın olarak okunan ve etkili olan girişim kültürü, programlama ve girişimcilik üzerine yazdığı denemelerle de tanınır.
```
