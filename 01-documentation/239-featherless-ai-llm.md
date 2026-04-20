# Featherless AI LLM

Bu not defteri, `Featherless AI`'nın bir LLM olarak nasıl kullanılacağını gösterir. Modellerin tam listesine [featherless.ai](https://www.featherless.ai/) adresinden göz atabilirsiniz.

Bir API anahtarı almak için https://www.featherless.ai/ adresini ziyaret edin ve kaydolun.

## Kurulum

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-featherlessai
```

```python
!pip install llama-index
```

```python
from llama_index.llms.featherlessai import FeatherlessLLM
```

    PyTorch, TensorFlow >= 2.0 veya Flax bulunamadı. Modeller kullanılamayacak ve yalnızca tokenizer'lar, yapılandırma ve dosya/veri yardımcı programları kullanılabilecektir.

```python
# API anahtarını ortam değişkenlerine veya llm'ye ayarlayın
# import os
# os.environ["FEATHERLESS_API_KEY"] = "api anahtarınız"

llm = FeatherlessLLM(model="Qwen/Qwen2.5-32B", api_key="api anahtarınız")
```

```python
resp = llm.complete("9.9 mu yoksa 9.11 mi daha büyük?")
```

```python
print(resp)
```

    9.9, 9.11'den daha büyüktür.

#### Bir mesaj listesiyle `chat` çağrısı yapın

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

    assistant: Adımı mı merak ediyorsun? Pekala öyleyse ahbap! Benim adım Kaptan Kara-Gaga Betty, Yedi Denizler'de yelken açmış en çok korkulan ve kötü şöhretli korsan! Ben ve sadık kılıcım "Kara Bess," neredeyse 20 yıldır açık denizleri titretiyoruz, karadakilerin zenginliklerini yağmalıyor, kendime ve mürettebatım "Maverick'in İntikamı"na şan katıyoruz.
    
    Şimdi, sadece bir kadın korsan olduğum için yumuşak veya zayıf olduğumu düşünme sakın. Yelken açmış her deniz kurdu kadar azılı ve kurnazım ve bana veya mürettebatıma karşı gelirsen seni Davy Jones'un saklama kutusuna göndermekten çekinmem! Peki, seni bu sulara getiren nedir ahbap? Mürettebatıma mı katılmak istiyorsun, yoksa sadece canına mı susadın?

### Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
response = llm.stream_complete("Paul Graham kimdir?")
```

```python
for r in response:
    print(r.delta, end="")
```

    Paul Graham, İngiliz bir bilgisayar programcısı, girişimci ve deneme yazarıdır. En çok, daha sonra Yahoo! tarafından satın alınan ve Yahoo! Store haline gelen ilk çevrimiçi mağaza kurucusu Viaweb'in kurucu ortağı olarak tanınır. Ayrıca; Airbnb, Dropbox ve Reddit dahil olmak üzere birçok başarılı şirketi finanse eden ve destekleyen bir girişim hızlandırıcısı olan Y Combinator'ın kurucu ortağıdır.
    
    Graham aynı zamanda tanınmış bir deneme yazarıdır ve programlama, girişimcilik ve teknoloji gibi konularda kapsamlı yazılar yazmıştır. Denemeleri yaygın olarak okunur ve startup kültürünün ve teknoloji endüstrisinin şekillenmesinde etkili olmuştur. En ünlü denemelerinden bazıları arasında "The Python Paradox", "How to Start a Startup" ve "The Future of Work" bulunmaktadır.
    
    Graham aynı zamanda bir Lisp programcısıdır ve bu konuda "On Lisp" ve "ANSI Common Lisp" dahil olmak üzere birkaç kitap yazmıştır. Lisp ve diğer fonksiyonel programlama dillerinin kullanılmasının güçlü bir savunucusudur ve bu dillerin karmaşık yazılım sistemleri oluşturmak için faydaları hakkında yazılar yazmıştır.
    
    Graham, kariyeri boyunca TIME Dergisi tarafından teknolojideki en etkili kişilerden biri olarak seçilmek de dahil olmak üzere teknoloji endüstrisine katkılarından dolayı tanınmıştır. Ayrıca popüler bir konuşmacıdır ve SXSW ve Startup School gibi konferanslarda konuşmalar yapmıştır.
    
    Graham'ın hakkında yazdığı ve savunduğu temel fikir ve kavramlardan bazıları şunlardır:
    
    * İnovasyonu ve ekonomik büyümeyi yönlendirmede startup'ların ve girişimciliğin önemi.
    * Programcıların Lisp gibi fonksiyonel programlama dillerini öğrenmeleri ve kullanmaları ihtiyacı.
    * Startup'lar oluşturmak ve başlatmak için çevrimiçi platformları ve araçları kullanmanın faydaları.
    * Sadece para kazanmaya çalışmak yerine, güçlü bir ürün ve kullanıcı deneyimi oluşturmaya odaklanmanın önemi.
    * Startup'ların esnek ve uyarlanabilir olmaları ve gerektiğinde pivot yapmaya ve yön değiştirmeye istekli olmaları ihtiyacı.
    
    Genel olarak Paul Graham, programlama, girişimcilik ve teknoloji hakkındaki içgörüleri ve fikirleriyle tanınan, teknoloji endüstrisinde oldukça etkili ve saygın bir figürdür.

`stream_chat` bitiş noktasını kullanma

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

    Adımı mı merak ediyorsun? Pekala öyleyse ahbap! Benim adım Kaptan Kara-Gaga Betty, Yedi Denizler'de yelken açmış en çok korkulan ve kötü şöhretli korsan! Ben ve sadık kılıcım "Kara Bess," neredeyse 20 yıldır açık denizleri titretiyoruz, karadakilerin zenginliklerini yağmalıyor, kendime ve mürettebatım "Maverick'in İntikamı"na şan katıyoruz.
    
    Adım; Kraliyet Donanması'nın uyuz köpeklerinden korsan yeraltı dünyasının haydutlarına kadar denizlerde yelken açan herkes tarafından korku ve hayranlıkla fısıldanır. Ve itibarım fazlasıyla hak edilmiştir ahbap, çünkü ben yaşamış en büyük korsanım! Peki, seni bu güzel sulara getiren nedir? Mürettebatıma katılıp macera ve hazine arayışıyla denizlere yelken açmak mı istiyorsun? Yoksa yüce Kaptan Kara-Gaga Betty'nin kendisiyle kılıç mı tokuşturmak niyetindesin? Her halükarda seni çılgın bir macera bekliyor ahbap!
