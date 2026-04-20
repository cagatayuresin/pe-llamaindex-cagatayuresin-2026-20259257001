# Portkey

---
title: Portkey
 | LlamaIndex OSS Documentation
---

**Portkey**, Gen AI uygulamanızı güvenilir ve emniyetli bir şekilde üretim ortamına taşıyan tam kapsamlı bir LLMOps platformudur.

#### Portkey'in LlamaIndex ile Entegrasyonunun Temel Özellikleri:

![header](https://3798672042-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FeWEp2XRBGxs7C1jgAdk7%2Fuploads%2FjDGBQvw5aFOCqctr0xwp%2FColab%20Version%202.png?alt=media\&token=16057c99-b86c-416c-932e-c2b71549c506)

1. **[🚪 AI Gateway (Yapay Zeka Ağ Geçidi)](#%F0%9F%94%81-implementing-fallbacks-and-retries-with-portkey)**:

   - **[Otomatik Yedekleme (Fallback) ve Yeniden Denemeler](#%F0%9F%94%81-implementing-fallbacks-and-retries-with-portkey)**: Birincil servis başarısız olsa bile uygulamanızın işlevsel kalmasını sağlayın.
   - **[Yük Dengeleme (Load Balancing)](#%E2%9A%96%EF%B8%8F-implementing-load-balancing-with-portkey)**: Gelen istekleri birden fazla model arasında verimli bir şekilde dağıtın.
   - **[Anlamsal Önbelleğe Alma (Semantic Caching)](#%F0%9F%A7%A0-implementing-semantic-caching-with-portkey)**: Sonuçları akıllıca önbelleğe alarak maliyetleri ve gecikmeyi azaltın.

2. **[🔬 Gözlemlenebilirlik (Observability)](#%F0%9F%94%AC-observability-with-portkey)**:

   - **Günlükleme (Logging)**: İzleme ve hata ayıklama için tüm istekleri takip edin.
   - **İstek İzleme (Requests Tracing)**: Optimizasyon için her isteğin yolculuğunu anlayın.
   - **Özel Etiketler (Custom Tags)**: Daha iyi içgörüler için istekleri segmentlere ayırın ve kategorize edin.

3. **[📝 Kullanıcı Geri Bildirimi ile Sürekli İyileştirme](#%F0%9F%93%9D-feedback-with-portkey)**:

   - **Geri Bildirim Toplama**: İster bir üretim ister konuşma düzeyinde olsun, sunulan herhangi bir istek hakkında sorunsuz bir şekilde geri bildirim toplayın.
   - **Ağırlıklı Geri Bildirim**: Kullanıcı geri bildirim değerlerine ağırlıklar ekleyerek incelikli bilgiler edinin.
   - **Geri Bildirim Meta Verileri**: Bağlam sağlamak için geri bildirimle birlikte özel meta verileri dahil edin, böylece daha zengin içgörüler ve analizler elde edin.

4. **[🔑 Güvenli Anahtar Yönetimi](#feedback-with-portkey)**:

   - **Sanal Anahtarlar (Virtual Keys)**: Portkey, orijinal sağlayıcı anahtarlarını sanal anahtarlara dönüştürerek birincil kimlik bilgilerinizin dokunulmadan kalmasını sağlar.
   - **Çoklu Tanımlayıcılar**: Güvenlikten ödün vermeden kolay tanımlama için aynı sağlayıcı için birden fazla anahtar veya farklı isimler altında aynı anahtarı ekleme yeteneği.

Bu özellikleri kullanmak için kuruluma başlayalım:

[![\\"Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/llm/portkey.ipynb)

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
%pip install llama-index-llms-portkey
```

```python
!pip install llama-index
```

```python
# LlamaIndex ve Portkey SDK Kurulumu
!pip install -U llama_index
!pip install -U portkey-ai


# Gerekli kütüphanelerin ve modüllerin içe aktarılması
from llama_index.llms.portkey import Portkey
from llama_index.core.llms import ChatMessage
import portkey as pk
```

LlamaIndex uygulamanıza **başka** herhangi bir SDK yüklemenize veya bunları içe aktarmanıza gerek yoktur.

#### **Adım 1️⃣: OpenAI, Anthropic ve daha fazlası için Portkey API Anahtarınızı ve Sanal Anahtarlarınızı alın**

**[Portkey API Anahtarı](https://app.portkey.ai/)**: [Buradan Portkey'e](https://app.portkey.ai/) giriş yapın, ardından sol üstteki profil simgesine tıklayın ve "API Key'i Kopyala" (Copy API Key) deyin.

```python
import os


os.environ["PORTKEY_API_KEY"] = "PORTKEY_API_KEY"
```

**[Sanal Anahtarlar (Virtual Keys)](https://docs.portkey.ai/key-features/ai-provider-keys)**

1. [Portkey panosundaki](https://app.portkey.ai/) "Sanal Anahtarlar" (Virtual Keys) sayfasına gidin ve sağ üst köşedeki "Anahtar Ekle" (Add Key) düğmesine basın.
2. Yapay zeka sağlayıcınızı seçin (OpenAI, Anthropic, Cohere, HuggingFace vb.), anahtarınıza benzersiz bir isim atayın ve gerekirse ilgili kullanım notlarını not edin. Sanal anahtarınız hazır!

![header](https://3798672042-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FeWEp2XRBGxs7C1jgAdk7%2Fuploads%2F66S1ik16Gle8jS1u6smr%2Fvirtual_keys.png?alt=media\&token=2fec1c39-df4e-4c93-9549-7445a833321c) 3. Şimdi aşağıdaki anahtarları kopyalayıp yapıştırın - bunları Portkey ekosisteminin herhangi bir yerinde kullanabilir ve orijinal anahtarınızı güvenli ve dokunulmamış halde tutabilirsiniz.

```python
openai_virtual_key_a = ""
openai_virtual_key_b = ""


anthropic_virtual_key_a = ""
anthropic_virtual_key_b = ""


cohere_virtual_key_a = ""
cohere_virtual_key_b = ""
```

Portkey'in Sanal anahtarlarını kullanmak istemiyorsanız, yapay zeka sağlayıcı anahtarlarınızı doğrudan da kullanabilirsiniz.

```python
os.environ["OPENAI_API_KEY"] = ""
os.environ["ANTHROPIC_API_KEY"] = ""
```

#### **Adım 2️⃣: Portkey Özelliklerini Yapılandırın**

To harness the full potential of Portkey’s integration with Llamaindex, you can configure various features as illustrated above. Here’s a guide to all Portkey features and the expected values:

| Özellik             | Yapılandırma Anahtarı | Değer(Tür)                                                                     | Gerekli                           |
| ------------------- | --------------------- | ------------------------------------------------------------------------------- | ---------------------------------- |
| API Key             | `api_key`             | `string`                                                                        | ✅ Gerekli (harici olarak ayarlanabilir) |
| Mod                 | `mode`                | `fallback`, `loadbalance`, `single`                                             | ✅ Gerekli                         |
| Önbellek Türü       | `cache_status`        | `simple`, `semantic`                                                            | ❔ İsteğe Bağlı                         |
| Önbelleği Zorla Yenile | `cache_force_refresh` | `True`, `False`                                                                 | ❔ İsteğe Bağlı                         |
| Önbellek Ömrü       | `cache_age`           | `integer` (saniye cinsinden)                                                          | ❔ İsteğe Bağlı                         |
| İzleme Kimliği      | `trace_id`            | `string`                                                                        | ❔ İsteğe Bağlı                         |
| Yeniden Denemeler    | `retry`               | `integer` \[0,5]                                                                | ❔ İsteğe Bağlı                         |
| Meta Veri           | `metadata`            | `json object` [Daha fazla bilgi](https://docs.portkey.ai/key-features/custom-metadata) | ❔ İsteğe Bağlı                         |
| Temel URL           | `base_url`            | `url`                                                                           | ❔ İsteğe Bağlı                         |

- `api_key` ve `mode` gerekli değerlerdir.

- Portkey API anahtarınızı Portkey kurucusunu kullanarak ayarlayabilir veya ortam değişkeni olarak da ayarlayabilirsiniz.

- **3** mod vardır - Single (Tek), Fallback (Yedekleme), Loadbalance (Yük Dengeleme).

  - **Single** - Bu standart moddur. Fallback VEYA Loadbalance özelliklerini istemiyorsanız bunu kullanın.
  - **Fallback** - Fallback özelliğini etkinleştirmek istiyorsanız bu modu ayarlayın. [Kılavuza buradan göz atın](#implementing-fallbacks-and-retries-with-portkey).
  - **Loadbalance** - Loadbalance özelliğini etkinleştirmek istiyorsanız bu modu ayarlayın. [Kılavuza buradan göz atın](#implementing-load-balancing-with-portkey).

İşte bu özelliklerinden bazılarının nasıl kurulacağına dair bir örnek:

```python
portkey_client = Portkey(
    mode="single",
)


# Portkey API Anahtarını os.environ ile tanımladığımız için, burada api_key'i tekrar ayarlamamıza gerek yok
```

#### **Adım 3️⃣: LLM'yi Oluşturma**

Portkey entegrasyonu ile bir LLM oluşturmak basitleştirilmiştir. OpenAI veya Anthropic kurucularınızda alışık olduğunuz anahtarların aynısıyla tüm sağlayıcılar için `LLMOptions` fonksiyonunu kullanın. Tek yeni anahtar, yük dengeleme özelliği için gerekli olan `weight` (ağırlık) anahtarıdır.

```python
openai_llm = pk.LLMOptions(
    provider="openai",
    model="gpt-4",
    virtual_key=openai_virtual_key_a,
)
```

Yukarıdaki kod, OpenAI sağlayıcısı ve GPT-4 modeli ile bir LLM kurmak için `LLMOptions` fonksiyonunun nasıl kullanılacağını göstermektedir. Aynı fonksiyon diğer sağlayıcılar için de kullanılabilir, bu da entegrasyon sürecini çeşitli sağlayıcılar arasında basitleştirilmiş ve tutarlı hale getirir.

#### **Adım 4️⃣: Portkey İstemcisini Aktif Edin**

`LLMOptions` fonksiyonunu kullanarak LLM'yi oluşturduktan sonraki adım, onu Portkey ile aktif hale getirmektir. Bu adım, tüm Portkey özelliklerinin LLM'niz için kullanılabilir olmasını sağlamak için gereklidir.

```python
portkey_client.add_llms(openai_llm)
```

Ve işte bu kadar! Sadece 4 adımda, LlamaIndex uygulamanıza gelişmiş üretim yetenekleri aşıladınız.

#### **🔧 Entegrasyonu Test Etme**

Her şeyin doğru kurulduğundan emin olalım. Aşağıda, basit bir sohbet senaryosu oluşturuyoruz ve yanıtı görmek için bunu Portkey istemcimiz üzerinden geçiriyoruz.

```python
messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Neler yapabilirsin?"),
]
print("Portkey LlamaIndex entegrasyonu test ediliyor:")
response = portkey_client.chat(messages)
print(response)
```

Günlüklerinizin (logs) [Portkey panonuzda](https://app.portkey.ai/) nasıl görüneceği aşağıda açıklanmıştır:

![Günlükler](https://portkey.ai/blog/content/images/2023/09/Log-1.png)

#### **⏩ Yanıtları Akışla İletme (Streaming)**

Portkey ile yanıtları akışla iletmek hiç bu kadar kolay olmamıştı. Portkey'in 4 yanıt fonksiyonu vardır:

1. `.complete(prompt)`
2. `.stream_complete(prompt)`
3. `.chat(messages)`
4. `.stream_chat(messages)`

`complete` fonksiyonu bir dize girdisi (`str`) beklerken, `chat` fonksiyonu bir `ChatMessage` nesneleri dizisiyle çalışır.

**Örnek kullanım:**

```python
# Bir istem hazırlayalım ve ardından akışlı bir yanıt almak için stream_complete fonksiyonunu kullanalım.


prompt = "Gökyüzü neden mavidir?"


print("\nStream Complete Test Ediliyor:\n")
response = portkey_client.stream_complete(prompt)
for i in response:
    print(i.delta, end="", flush=True)


# Bir dizi sohbet mesajı hazırlayalım ve ardından akışlı bir sohbet yanıtı elde etmek için stream_chat fonksiyonunu kullanalım.


messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Neler yapabilirsin?"),
]


print("\nStream Chat Test Ediliyor:\n")
response = portkey_client.stream_chat(messages)
for i in response:
    print(i.delta, end="", flush=True)
```

#### **🔍 Özet ve Referanslar**

Tebrikler! 🎉 Portkey entegrasyonunu LlamaIndex ile başarıyla kurdunuz ve test ettiniz. Adımları özetlemek gerekirse:

1. pip install portkey-ai
2. from llama_index.llms import Portkey
3. Portkey API Anahtarınızı alın ve sanal sağlayıcı anahtarlarınızı [buradan](https://app.portkey.ai/) oluşturun.
4. Portkey istemcinizi oluşturun ve modu ayarlayın: `portkey_client=Portkey(mode="fallback")`
5. Sağlayıcı LLM'nizi LLMOptions ile oluşturun: `openai_llm = pk.LLMOptions(provider="openai", model="gpt-4", virtual_key=openai_key_a)`
6. `portkey_client.add_llms(openai_llm)` ile LLM'yi Portkey'e ekleyin
7. Portkey yöntemlerini, `portkey_client.chat(messages)` ile herhangi bir LLM'de yaptığınız gibi düzenli olarak çağırın.

İşte tüm fonksiyonlara ve parametrelerine dair kılavuz:

- [Portkey LLM Constructor](#step-2-add-all-the-portkey-features-you-want-as-illustrated-below-by-calling-the-portkey-class)
- [LLMOptions Constructor](https://github.com/Portkey-AI/rubeus-python-sdk/blob/4cf3e17b847225123e92f8e8467b41d082186d60/rubeus/api_resources/utils.py#L179)
- [Portkey + LlamaIndex Özelliklerinin Listesi](#portkeys-integration-with-llamaindex-adds-the-following-production-capabilities-to-your-apps-out-of-the-box)

[![\\"Open](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/llm/portkey.ipynb)

#### **🔁 Portkey ile Yedekleme (Fallback) ve Yeniden Denemelerin Uygulanması**

Yedeklemeler (fallbacks) ve yeniden denemeler (retries), dayanıklı yapay zeka uygulamaları oluşturmak için gereklidir. Portkey ile bu özellikleri uygulamak basittir:

- **Yedeklemeler (Fallbacks)**: Birincil servis veya model başarısız olursa, Portkey otomatik olarak bir yedek modele geçecektir.
- **Yeniden Denemeler (Retries)**: Bir istek başarısız olursa, Portkey isteği birden fazla kez yeniden deneyecek şekilde yapılandırılabilir.

Aşağıda, Portkey kullanarak yedeklemelerin ve yeniden denemelerin nasıl kurulacağını gösteriyoruz:

```python
portkey_client = Portkey(mode="fallback")
messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Neler yapabilirsin?"),
]


llm1 = pk.LLMOptions(
    provider="openai",
    model="gpt-4",
    retry_settings={"on_status_codes": [429, 500], "attempts": 2},
    virtual_key=openai_virtual_key_a,
)


llm2 = pk.LLMOptions(
    provider="openai",
    model="gpt-3.5-turbo",
    virtual_key=openai_virtual_key_b,
)


portkey_client.add_llms(llm_params=[llm1, llm2])


print("Yedekleme (Fallback) & Yeniden Deneme (Retry) işlevselliği test ediliyor:")
response = portkey_client.chat(messages)
print(response)
```

#### **⚖️ Portkey ile Yük Dengelemenin (Load Balancing) Uygulanması**

Yük dengeleme, gelen isteklerin birden fazla model arasında verimli bir şekilde dağıtılmasını sağlar. Bu sadece performansı artırmakla kalmaz, aynı zamanda bir modelin başarısız olması durumunda yedeklilik (redundancy) sağlar.

Portkey ile yük dengelemeyi uygulamak basittir. Şunları yapmanız gerekir:

- Her bir LLM için `weight` (ağırlık) parametresini tanımlayın. Bu ağırlık, isteklerin LLM'ler arasında nasıl dağıtılacağını belirler.
- Tüm LLM'lerin ağırlıklarının toplamının 1 olduğundan emin olun.

İşte Portkey ile yük dengeleme kurmaya dair bir örnek:

```python
portkey_client = Portkey(mode="ab_test")


messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Neler yapabilirsin?"),
]


llm1 = pk.LLMOptions(
    provider="openai",
    model="gpt-4",
    virtual_key=openai_virtual_key_a,
    weight=0.2,
)


llm2 = pk.LLMOptions(
    provider="openai",
    model="gpt-3.5-turbo",
    virtual_key=openai_virtual_key_a,
    weight=0.8,
)


portkey_client.add_llms(llm_params=[llm1, llm2])


print("Yük dengeleme (Loadbalance) işlevselliği test ediliyor:")
response = portkey_client.chat(messages)
print(response)
```

#### **🧠 Portkey ile Anlamsal Önbelleğe Almanın (Semantic Caching) Uygulanması**

Anlamsal önbelleğe alma, bir isteğin bağlamını anlayan akıllı bir önbellekleme mekanizmasıdır. Yalnızca tam girdi eşleşmelerine dayalı önbelleğe almak yerine, anlamsal önbelleğe alma benzer istekleri tanımlar ve önbelleğe alınmış sonuçları sunarak gereksiz istekleri azaltır, yanıt sürelerini iyileştirir ve para tasarrufu sağlar.

Portkey ile anlamsal önbelleğe almanın nasıl uygulanacağını görelim:

```python
import time


portkey_client = Portkey(mode="single")


openai_llm = pk.LLMOptions(
    provider="openai",
    model="gpt-3.5-turbo",
    virtual_key=openai_virtual_key_a,
    cache_status="semantic",
)


portkey_client.add_llms(openai_llm)


current_messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Bir pizzanın malzemeleri nelerdir?"),
]


print("Portkey Anlamsal Önbelleği Test Ediliyor:")


start = time.time()
response = portkey_client.chat(current_messages)
end = time.time() - start


print(response)
print(f"{'-'*50}\n{end} saniyede sunuldu.\n{'-'*50}")


new_messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Pizzanın malzemeleri"),
]


print("Portkey Anlamsal Önbelleği Test Ediliyor:")


start = time.time()
response = portkey_client.chat(new_messages)
end = time.time() - start


print(response)
print(f"{'-'*50}\n{end} saniyede sunuldu.\n{'-'*50}")
```

Portkey'in önbelleği, önbellek açısından kritik iki fonksiyonu daha destekler - Zorla Yenileme (Force Refresh) ve Ömür (Age).


`cache_force_refresh`: Cevabı önbellekten sunmak yerine sağlayıcınıza zorla bir istek gönderir. `cache_age`: Bu belirli dize için önbellek deposunun otomatik olarak hangi aralıkla yenileneceğine karar verir. Önbellek ömrü saniye cinsinden ayarlanır.


İşte nasıl kullanabileceğiniz:


```python
# Önbellek durumunu `semantic` (anlamsal) ve cache_age'i (önbellek ömrü) 60 saniye olarak ayarlama.
openai_llm = pk.LLMOptions(
    provider="openai",
    model="gpt-3.5-turbo",
    virtual_key=openai_virtual_key_a,
    cache_force_refresh=True,
    cache_age=60,
)
```


#### **🔬 Portkey ile Gözlemlenebilirlik (Observability)**


Uygulamanızın davranışına dair içgörüye sahip olmak çok önemlidir. Portkey'in gözlemlenebilirlik özellikleri, yapay zeka uygulamalarınızı kolaylıkla izlemenize, hata ayıklamanıza ve optimize etmenize olanak tanır. Her bir isteği takip edebilir, yolculuğunu anlayabilir ve özel etiketlere göre segmentlere ayırabilirsiniz. Bu detay düzeyi, darboğazları belirlemede, maliyetleri optimize etmede ve genel kullanıcı deneyimini iyileştirmede yardımcı olabilir.


İşte Portkey ile gözlemlenebilirliğin nasıl kurulacağı:


```python
metadata = {
    "_environment": "production",
    "_prompt": "test",
    "_user": "user",
    "_organisation": "acme",
}


trace_id = "llamaindex_portkey"


portkey_client = Portkey(mode="single")


openai_llm = pk.LLMOptions(
    provider="openai",
    model="gpt-3.5-turbo",
    virtual_key=openai_virtual_key_a,
    metadata=metadata,
    trace_id=trace_id,
)


portkey_client.add_llms(openai_llm)


print("Gözlemlenebilirlik (Observability) işlevselliği test ediliyor:")
response = portkey_client.chat(messages)
print(response)
```


#### **🌉 Açık Kaynak Yapay Zeka Ağ Geçidi (AI Gateway)**


Portkey'in AI Gateway'i dahili olarak [açık kaynaklı Rubeus projesini](https://github.com/portkey-ai/rubeus) kullanır. Rubeus; LLM'lerin birlikte çalışabilirliği, yük dengeleme, yedeklemeler gibi özellikleri destekler ve isteklerinizin en iyi şekilde işlenmesini sağlayarak bir aracı görevi görür.


Portkey kullanmanın avantajlarından biri esnekliğidir. Davranışını kolayca özelleştirebilir, istekleri farklı sağlayıcılara yönlendirebilir ve hatta Portkey'e günlük kaydını tamamen atlayabilirsiniz.


İşte Portkey ile davranışı özelleştirmeye dair bir örnek:


```python
portkey_client.base_url=None
```


#### **📝 Portkey ile Geri Bildirim (Feedback)**


Sürekli iyileştirme, yapay zekanın temel taşıdır. Modellerinizin ve uygulamalarınızın gelişmesini ve kullanıcılara daha iyi hizmet vermesini sağlamak için geri bildirim hayati önem taşır. Portkey'in Geri Bildirim API'si, kullanıcılardan ağırlıklı geri bildirim toplamanın basit bir yolunu sunarak zaman içinde iyileştirmenize ve geliştirmenize olanak tanır.


İşte Portkey ile Geri Bildirim API'sinin nasıl kullanılacağı:


[Geri bildirim (Feedback) hakkında buradan](https://docs.portkey.ai/key-features/feedback-api) daha fazla bilgi okuyun.


```python
import requests
import json


# Uç Nokta URL'si
url = "https://api.portkey.ai/v1/feedback"


# Başlıklar
headers = {
    "x-portkey-api-key": os.environ.get("PORTKEY_API_KEY"),
    "Content-Type": "application/json",
}


# Veri
data = {"trace_id": "llamaindex_portkey", "value": 1}


# İstek yapma
response = requests.post(url, headers=headers, data=json.dumps(data))


# Yanıtı yazdırma
print(response.text)
```


Her bir izleme kimliği (trace id) için `weight` (ağırlık) ve `value` (değer) içeren tüm geri bildirimler Portkey panosunda mevcuttur:


![Geri Bildirim](https://portkey.ai/blog/content/images/2023/09/feedback.png)


#### **✅ Sonuç**


Portkey'i LlamaIndex ile entegre etmek, sağlam ve dayanıklı yapay zeka uygulamaları oluşturma sürecini basitleştirir. Anlamsal önbelleğe alma, gözlemlenebilirlik, yük dengeleme, geri bildirim ve yedeklemeler gibi özelliklerle optimum performans ve sürekli iyileştirme sağlayabilirsiniz.


Bu kılavuzu takip ederek, Portkey entegrasyonunu LlamaIndex ile kurdunuz ve test ettiniz. Yapay zeka uygulamaları oluşturmaya ve dağıtmaya devam ederken, bu entegrasyonun tüm potansiyelinden yararlanmayı unutmayın!


Daha fazla yardım veya sorularınız için geliştiricilere ulaşın ➡️\
[![Twitter](https://img.shields.io/twitter/follow/portkeyai?style=social\&logo=twitter)](https://twitter.com/intent/follow?screen_name=portkeyai)


Yapay zeka modellerini üretim ortamına taşıyan uygulayıcılar topluluğumuza katılın ➡️\
[![Discord](https://img.shields.io/discord/1143393887742861333?logo=discord)](https://discord.gg/sDk9JaNfK8)
