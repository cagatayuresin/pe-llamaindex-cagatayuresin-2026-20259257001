# Baseten Yemek Kitabı (Cookbook)

```python
%pip install llama-index llama-index-llms-baseten
```

```python
from llama_index.llms.baseten import Baseten
```

## Model API'leri ve Özel Dağıtımlar

Baseten, çıkarım (inference) için iki ana yol sunar.
1. Model API'leri; (GPT-OSS, Kimi K2, DeepSeek vb.) popüler açık kaynaklı modeller için, `deepseek-ai/DeepSeek-V3-0324` gibi kısa adlar (slug) aracılığıyla doğrudan bir öncü modeli kullanabileceğiniz ve belirteç başına (per-token) ücretlendirileceğiniz genel uç noktalardır. Desteklenen modellerin listesini burada bulabilirsiniz: https://docs.baseten.co/development/model-apis/overview#supported-models.

2. Özel dağıtımlar (Dedicated deployments); üretim iş yüklerini otomatik ölçeklendirmek istediğiniz ve ince ayarlı yapılandırmaya sahip olduğunuz özel modelleri sunmak için kullanışlıdır. Baseten panelinizde bir model dağıtmanız ve `abcd1234` gibi 8 karakterli model kimliğini sağlamanız gerekir.

Varsayılan olarak, `model_apis` parametresini `True` olarak ayarlıyoruz. Eğer özel bir dağıtım kullanmak istiyorsanız, Baseten nesnesini oluştururken `model_apis` parametresini `False` olarak ayarlamalısınız.

#### Örnekleme (Instantiation)

```python
# Model API'leri, model_slug bilgisini burada bulabilirsiniz: https://docs.baseten.co/development/model-apis/overview#supported-models
llm = Baseten(
    model_id="MODEL_KISA_ADI",
    api_key="API_ANAHTARINIZ",
    model_apis=True,  # Varsayılan değerdir, bu yüzden belirtilmesi zorunlu değildir
)

# Özel Dağıtımlar, model_id bilgisini Baseten panelinde burada bulabilirsiniz: https://app.baseten.co/overview
llm = Baseten(
    model_id="MODEL_KİMLİĞİ",
    api_key="API_ANAHTARINIZ",
    model_apis=False,
)
```

#### Bir istemle `complete` çağrısı yapın

```python
llm_response = llm.complete("Paul Graham kimdir?")
print(llm_response.text)
```

    Paul Graham; teknoloji, startup'lar ve felsefe üzerine yazdığı etkili denemeleriyle ve startup hızlandırıcısı **Y Combinator (YC)**'ın kurucu ortaklarından biri olmasıyla tanınan İngiliz-Amerikalı bir girişimci, denemeci ve programcıdır. İşte onunla ilgili bazı önemli noktalar:
    
    ### **Geçmiş ve Kariyer**
    - 1964 yılında İngiltere'de doğan Graham, **Cornell Üniversitesi**'nde eğitim gördü ve **Harvard**'dan **Bilgisayar Bilimleri** alanında doktora derecesi aldı.
    - İlk web tabanlı uygulama olan **Viaweb**'i (1995) oluşturdu; bu uygulama daha sonra 1998'de Yahoo! tarafından satın alındı ve **Yahoo! Store** oldu.
    - 2005 yılında Jessica Livingston, Robert Morris ve Trevor Blackwell ile birlikte **Y Combinator (YC)**'ı kurdu. YC; **Airbnb, Dropbox, Stripe, Reddit ve DoorDash** gibi şirketleri finanse etmiştir.
    
    ### **Yazarlık ve Etki**
    - Startup'lar, teknoloji ve yaşam felsefesi üzerine yazdığı ve web sitesinde ([paulgraham.com](http://www.paulgraham.com)) barındırdığı **denemeleri** ile tanınır.
    - Popüler denemeleri şunlardır:
      - *"Bir Girişime Nasıl Başlanır (How to Start a Startup)"*  
      - *"Ölçeklenmeyen Şeyler Yapın (Do Things That Don't Scale)"*  
      - *"Girişimler İçin En Zor Dersler"* 


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

    assistant: Arrr, ahbap! Ben Kaptan Al-Sakal (Crimsonbeard) olarak bilinirim — gerçi sakalım kızıldan çok yanan bir kırmızıdır, doğruya doğru! Efsanelerin korsanı, yedi mem'in (memes) belası ve şüpheli yaşam tercihlerinin uzmanı. Ama istersen bana Kaptan diyebilirsin ya da "Ananaslar Hakkında Konuşmayı Bırakmayan Şu Tuhaf Korsan". Şimdi, seni bugün gemime hangi fesatlık getirdi? 🏴‍☠️🍍

## Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
resp = llm.stream_complete("Paul Graham bir ")
```

```python
for r in resp:
    print(r.delta, end="")
```

    Paul Graham; Airbnb, Dropbox, Stripe ve Reddit gibi şirketlerin kurulmasına yardımcı olan son derece etkili bir startup hızlandırıcısı olan **Y Combinator**'ın kurucu ortaklarından biri olarak tanınan İngiliz-Amerikalı bir girişimci, denemeci ve risk sermayedarıdır.  
    
    ### Paul Graham Hakkında Önemli Bilgiler:  
    1. **Erken Kariyer**: Başlangıçta bir programcı olarak, 1998'de Yahoo! tarafından satın alınan ve Yahoo! Store olan ilk web tabanlı uygulamalardan biri olan **Viaweb**'i geliştirdi.  
    2. **Y Combinator**: 2005 yılında Jessica Livingston, Robert Morris ve Trevor Blackwell ile birlikte Y Combinator'ı kurdu. Erken aşamadaki girişimlere finansman ve mentorluk sağlayan "tohum hızlandırıcı" modeline öncülük etti.  
    3. **Denemeler**: Graham; startup'lar, teknoloji ve yaşam felsefesi üzerine yazdığı, web sitesinde ([paulgraham.com](http://www.paulgraham.com)) bulunan anlayışlı denemeleriyle tanınır. *"Startup Fikirleri Nasıl Bulunur"* ve *"Ölçeklenmeyen Şeyler Yapın"* gibi denemeleri popülerdir.  
    4. **Yatırımlar**: YC aracılığıyla binlerce girişimi destekleyerek Silikon Vadisi'nin teknoloji ortamını şekillendirdi.  
    5. **Lisp Savunucusu**: Lisp programlama dilinin güçlü bir savunucusudur.

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

    Arrr, benim adım Kaptan Al-Sakal! Batan güneş kadar kırmızı bir sakalı ve mücevher dolu bir hazine sandığından daha parlak bir gardırobu olan, korkusuz ve gösterişli bir korsanım! Macera, altın ve en iyi romu aramak için yedi denize yelken açıyorum — her zaman dramatik bir yetenek ve gözümde bir parıltıyla. 
    
    Ya senin adın ne, ahbap? Yoksa şimdilik sana sadece "Şanslı Mürettebat Üyesi" mi diyeyim? *göz kırpar ve tüylü şapkasını düzeltir*

# Asenkron (Async)
Asenkron işlemler; istek zaman aşımlarına takılabilecek uzun süreli çıkarım görevleri, toplu çıkarım işleri ve belirli isteklere öncelik vermek için kullanılır.

(1) Entegrasyonda, `acomplete` asenkron fonksiyonu, Python'da asenkron bir HTTP istemcisi olan aiohttp kütüphanesi kullanılarak uygulanmıştır. Fonksiyon, uygun Baseten model uç noktasında async_predict'i çağırır, ardından başarılı olursa kullanıcıya bir request_id (istek kimliği) içeren bir yanıt verilir. Kullanıcı daha sonra döndürülen request_id'yi kullanarak async_predict isteğinin durumunu kontrol edebilir veya isteği iptal edebilir.

(2) Model isteği yürütmeyi bitirdiğinde, asenkron sonuç kullanıcı tarafından sağlanan bir webhook uç noktasına gönderilecektir. Webhook imzasını güvenlik için doğrulamak, ardından çıktıyı işlemek ve depolamak kullanıcının uç noktasının sorumluluğundadır.

Baseten: request_id'yi al → sonuç webhook'a gönderilir.

##### Not: Asenkron kullanım yalnızca özel dağıtımlar için mevcuttur ve model API'leri için geçerli değildir. Sohbet (chat) asenkron işlemler için mantıklı olmadığından `achat` desteklenmemektedir.

```python
async_llm = Baseten(
    model_id="MODEL_KİMLİĞİNİZ",
    api_key="API_ANAHTARINIZ",
    webhook_endpoint="WEBHOOK_UC_NOKTANIZ",
)
response = await async_llm.acomplete("Paul Graham bir ")
print(response)  # Bu, istek kimliğidir (request id)
```

    35643965636d4c3da6f54b5c3b354aa0

```python
"""
Bu kod, bir async_predict isteğinin request_id'sini ve bu isteğin yapıldığı model_id'yi kullanarak isteğin durum bilgilerini döndürecektir.
"""

import requests
import os

model_id = "MODEL_KİMLİĞİNİZ"
request_id = "İSTEK_KİMLİĞİNİZ"
# Sırları ortam değişkenlerinden okuyun
baseten_api_key = "API_ANAHTARINIZ"

resp = requests.get(
    f"https://model-{model_id}.api.baseten.co/async_request/{request_id}",
    headers={"Authorization": f"Api-Key {baseten_api_key}"},
)

print(resp.json())
```

    {'request_id': '35643965636d4c3da6f54b5c3b354aa0', 'model_id': 'yqvr2lxw', 'deployment_id': '31kmg1w', 'status': 'SUCCEEDED', 'webhook_status': 'SUCCEEDED', 'created_at': '2025-03-27T00:17:51.578558Z', 'status_at': '2025-03-27T00:18:38.768572Z', 'errors': []}
