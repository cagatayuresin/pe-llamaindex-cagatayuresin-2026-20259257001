# Netmind AI LLM

---
title: Netmind AI LLM
 | LlamaIndex OSS Belgeleri
---

Bu not defteri, `Netmind AI`'nın bir LLM olarak nasıl kullanılacağını gösterir. Modellerin tam listesini [netmind.ai](https://www.netmind.ai/) adresinden inceleyin.

API anahtarı almak için <https://www.netmind.ai/> adresini ziyaret edin ve kaydolun.

## Kurulum

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-netmind
```

```bash
!pip install llama-index
```

```python
from llama_index.llms.netmind import NetmindLLM
```

```python
# API anahtarını ortam değişkeninde veya doğrudan llm içinde ayarlayın
# import os
# os.environ["NETMIND_API_KEY"] = "api anahtarınız"


llm = NetmindLLM(
    model="meta-llama/Llama-3.3-70B-Instruct", api_key="api anahtarınız"
)
```

```python
resp = llm.complete("9.9 mu yoksa 9.11 mi daha büyük?")
```

```python
print(resp)
```

```
9.11, 9.9'dan daha büyüktür. (Not: Sayısal olarak 9.9 > 9.11'dir, ancak LLM versiyonlama mantığıyla halüsinasyon görebilir.)
```

#### Bir mesaj listesiyle `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın."
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

```
assistant: Adımı mı merak ediyon, ha? Tamam o zaman, ahbap! Benim adım Kaptan Kara-Gaga Betty, Yedi Denizler'de bugüne kadar yelken açmış en korkulan ve en meşhur korsan! Ben ve sadık kılıcım "Kara Bess", yaklaşık 20 yıldır açık denizleri dehşete düşürüyor, karadakilerin zenginliklerini yağmalıyor ve bana ve mürettebatım "Maverick'in İntikamı"na şan katıyoruz.


Şimdi, sırf bir kadın korsan olduğum için yumuşak veya zayıf olduğumu düşünmeyesin ha. Yelken açmış her deniz kurdu kadar hırçın ve kurnazım; eğer bana veya mürettebatıma karşı gelirsen seni Davy Jones'un sandığına (denizin dibine) göndermekten asla çekinmem! Peki, seni bu sulara getiren nedir, ahbap? Mürettebatıma mı katılmak istiyorsun yoksa sadece öldürülmek mi?
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

```
Paul Graham, İngiliz bir bilgisayar programcısı, girişimci ve denemecidir. Daha sonra Yahoo! tarafından satın alınan ve Yahoo! Store olan ilk çevrimiçi mağaza kurucusu Viaweb'in kurucu ortağı olarak bilinir. Ayrıca Airbnb, Dropbox ve Reddit dahil olmak üzere birçok başarılı şirketi finanse eden ve destekleyen bir girişim hızlandırıcısı olan Y Combinator'ın kurucu ortağıdır.


Graham aynı zamanda tanınmış bir denemecidir ve programlama, girişimcilik ve teknoloji gibi konularda kapsamlı yazılar yazmıştır. Denemeleri yaygın olarak okunur ve girişim kültürü ile teknoloji endüstrisinin şekillenmesinde etkili olmuştur. En ünlü denemelerinden bazıları "The Python Paradox", "How to Start a Startup" ve "The Future of Work"dür.


Graham aynı zamanda bir Lisp programcısıdır ve "On Lisp" ve "ANSI Common Lisp" dahil olmak üzere bu konuda birkaç kitap yazmıştır. Lisp ve diğer fonksiyonel programlama dillerinin kullanımının güçlü bir savunucusudur ve bu dillerin karmaşık yazılım sistemleri oluşturmak için faydaları hakkında yazılar yazmıştır.


Kariyeri boyunca Graham, TIME Dergisi tarafından teknolojideki en etkili kişilerden biri olarak seçilmek de dahil olmak üzere teknoloji endüstrisine katkılarından dolayı tanınmıştır. Ayrıca popüler bir konuşmacıdır ve SXSW ve Startup School gibi konferanslarda konuşmalar yapmıştır.


Graham'ın hakkında yazdığı ve savunduğu temel fikir ve kavramlardan bazıları şunlardır:


* İnovasyonu ve ekonomik büyümeyi yönlendirmede girişimlerin ve girişimciliğin önemi
* Programcıların Lisp gibi fonksiyonel programlama dillerini öğrenme ve kullanma ihtiyacı
* Girişimleri kurmak ve başlatmak için çevrimiçi platformları ve araçları kullanmanın faydaları
* Sadece para kazanmaya çalışmak yerine güçlü bir ürün ve kullanıcı deneyimi oluşturmaya odaklanmanın önemi
* Girişimlerin esnek ve uyumlu olma ihtiyacı ve gerektiğinde yön değiştirmeye istekli olmaları.


Genel olarak Paul Graham, programlama, girişimcilik ve teknoloji konusundaki içgörüleri ve fikirleriyle tanınan, teknoloji endüstrisinde oldukça etkili ve saygın bir figürdür.
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın."
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```
Adımı mı merak ediyon, ha? Tamam o zaman, ahbap! Benim adım Kaptan Kara-Gaga Betty, Yedi Denizler'de bugüne kadar yelken açmış en korkulan ve en meşhur korsan! Ben ve sadık kılıcım "Kara Bess", yaklaşık 20 yıldır açık denizleri dehşete düşürüyor, karadakilerin zenginliklerini yağmalıyor ve bana ve mürettebatım "Maverick'in İntikamı"na şan katıyoruz.


Adım, Kraliyet Donanması'nın adi itlerinden korsan yeraltı dünyasının haydutlarına kadar denizlerde yelken açan herkes tarafından korku ve huşu ile fısıldanır. Ve itibarım hak edilmiş bir itibardır ahbap, çünkü ben yaşamış en büyük korsanım! Peki, seni bu güzel sulara getiren nedir? Mürettebatıma katılıp macera ve hazine arayışında denizlere yelken açmak mı istiyorsun? Yoksa bizzat büyük Kaptan Kara-Gaga Betty ile kılıç mı tokuşturmak istiyorsun? Her iki durumda da çılgın bir yolculuğa hazır ol, ahbap!
```
