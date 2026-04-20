# Perplexity

---
title: Perplexity
 | LlamaIndex OSS Documentation
---

Perplexity’nin Sonar API'si, gerçek zamanlı, doğrulanmış web araması ile gelişmiş akıl yürütme ve derin araştırma yeteneklerini birleştiren bir çözüm sunar.

Ne zaman kullanılmalı:

- Uygulamanız, dinamik içerik güncellemeleri veya güncel olay takibi gibi web'den doğrudan zamanında ve ilgili veriler gerektirdiğinde.
- Dijital asistanlar veya gelişmiş arama motorları gibi entegre akıl yürütme ve derin araştırma ile karmaşık kullanıcı sorgularını desteklemesi gereken ürünler için.

Başlamadan önce `llama_index`'i kurduğunuzdan emin olun.

```python
%pip install llama-index-llms-perplexity
```

```python
!pip install llama-index
```

## Başlangıç Kurulumu

12 Nisan 2025 itibarıyla - LlamaIndex'teki Perplexity LLM sınıfı ile aşağıdaki modeller desteklenmektedir:

| Model                 | Bağlam Uzunluğu | Model Tipi      |
| --------------------- | -------------- | --------------- |
| `sonar-deep-research` | 128k           | Chat Completion |
| `sonar-reasoning-pro` | 128k           | Chat Completion |
| `sonar-reasoning`     | 128k           | Chat Completion |
| `sonar-pro`           | 200k           | Chat Completion |
| `sonar`               | 128k           | Chat Completion |
| `r1-1776`             | 128k           | Chat Completion |

- `sonar-pro` modelinin maksimum çıktı jeton (token) sınırı 8k'dır.
- Akıl yürütme modelleri Düşünce Zinciri (Chain of Thought) yanıtları üretir.
- `r1-1776`, Perplexity arama alt sistemini kullanmayan çevrimdışı bir sohbet modelidir.

En son desteklenen modelleri [burada](https://docs.perplexity.ai/docs/model-cards) bulabilirsiniz.
İstek limitleri [burada](https://docs.perplexity.ai/docs/rate-limits) bulunur.
Fiyatlandırma [burada](https://docs.perplexity.ai/guides/pricing) bulunabilir.

```python
import getpass
import os


if "PPLX_API_KEY" not in os.environ:
    os.environ["PPLX_API_KEY"] = getpass.getpass(
        "Perplexity API anahtarınızı girin: "
    )
```

```python
from llama_index.llms.perplexity import Perplexity


PPLX_API_KEY = __import__("os").environ.get("PPLX_API_KEY")


llm = Perplexity(api_key=PPLX_API_KEY, model="sonar-pro", temperature=0.2)
```

```python
# llama_index kütüphanesinden ChatMessage sınıfını içe aktarın.
from llama_index.core.llms import ChatMessage


# Her bir sözlüğün bir sohbet mesajını temsil ettiği bir sözlük listesi oluşturun.
# Her sözlük bir 'role' anahtarı (örneğin, sistem veya kullanıcı) ve karşılık gelen mesajla birlikte bir 'content' anahtarı içerir.
messages_dict = [
    {"role": "system", "content": "Kesin ve özlü ol."},
    {
        "role": "user",
        "content": "Bana ABD Borsa piyasası hakkındaki son haberleri anlat.",
    },
]


# Liste içerisindeki her bir sözlüğü, bir liste kapsamı (list comprehension) içinde paket açma (**msg) kullanarak bir ChatMessage nesnesine dönüştürün.
messages = [ChatMessage(**msg) for msg in messages_dict]


# Dönüşümü doğrulamak için ChatMessage nesnelerinin listesini yazdırın.
print(messages)
```

```python
[ChatMessage(role=<MessageRole.SYSTEM: 'system'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text='Kesin ve özlü ol.')]), ChatMessage(role=<MessageRole.USER: 'user'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text='Bana ABD Borsa piyasası hakkındaki son haberleri anlat.')])]
```

## Sohbet (Chat)

```python
response = llm.chat(messages)
print(response)
```

```python
assistant: ABD borsa piyasasındaki son güncellemeler, son zamanlarda güçlü bir performans olduğunu gösteriyor. Çarşamba günü gerçekleşen %10'luk önemli ralli, piyasa kazançlarına büyük katkı sağladı. Ayrıca piyasa Cuma günü %2'lik bir artışla güçlü bir kapanış yaparak gün içi en yüksek seviyesine yakın bir seviyede tamamladı. Bu durum, özellikle mega ve büyük ölçekli büyüme hisselerinde güçlü bir ivmeyi yansıtıyor[1].
```

## Asenkron Sohbet (Async Chat)

Asenkron konuşma işleme için, mesaj göndermek ve yanıtı beklemek için `achat` yöntemini kullanın:

```python
# 'achat' yöntemini kullanarak sohbet mesajları listesini LLM'ye asenkron olarak gönderin.
# Bu yöntem, modelin cevabını içeren bir ChatResponse nesnesi döndürür.
response = await llm.achat(messages)


print(response)
```

```python
assistant: ABD borsa piyasası son zamanlarda önemli kazanımlar elde etti. Çarşamba günü gerçekleşen büyük bir ralli %10'luk bir artışla sonuçlanarak piyasanın genel yükselişine önemli ölçüde katkıda bulundu. Ayrıca piyasa Cuma günü %2'lik bir artışla güçlü bir şekilde kapandı ve gün içi en yüksek seviyesine yakın bir noktada tamamladı. Bu performans, özellikle mega ve büyük ölçekli büyüme hisselerindeki güçlü ivmeyi vurguluyor[1].
```

## Akışlı Sohbet (Stream Chat)

Bir yanıtı gerçek zamanlı olarak jeton jeton (token by token) almak istediğiniz durumlar için `stream_chat` yöntemini kullanın:

```python
# LLM örneğinde, sohbet yanıtını her seferinde bir delta (jeton veya yığın) olarak akışla iletmek için bir üreteç veya yinelenebilir döndüren stream_chat yöntemini çağırın.
response = llm.stream_chat(messages)


# Her bir akış yanıt yığını üzerinde yineleme yapın.
for r in response:
    # Yeni bir satır eklemeden deltayı (oluşturulan metnin yeni yığını) yazdırın.
    print(r.delta, end="")
```

```python
ABD borsa piyasası hakkındaki son haberler, son zamanlarda güçlü bir performans olduğunu gösteriyor. New York Borsası (NYSE), Çarşamba günü %10'luk önemli bir ralli ve ardından Cuma günü %2'lik bir kazançla karşılaştı. Bu yukarı yönlü ivme, mega ve büyük ölçekli büyüme hisselerinin etkisiyle piyasayı gün içi en yüksek seviyelerine yaklaştırdı[1].
```

## Asenkron Akışlı Sohbet (Async Stream Chat)

Benzer şekilde, asenkron akış için `astream_chat` yöntemi, yanıt deltalarını asenkron olarak işleme yolu sunar:

```python
# LLM örneğinde, yanıt yığınlarını döndüren bir asenkron üreteç olan astream_chat yöntemini asenkron olarak çağırın.
resp = await llm.astream_chat(messages)


# Üreteçten gelen her bir yanıt yığını üzerinde asenkron olarak yineleme yapın.
# Her bir yığın (delta) için yığının metin içeriğini yazdırın.
async for delta in resp:
    print(delta.delta, end="")
```

```python
ABD borsa piyasasındaki son güncellemeler önemli bir pozitif ivme gösteriyor. New York Borsası (NYSE), Çarşamba günü %10'luk dikkat çekici bir yükselişle güçlü bir ralli yaşadı. Bunu Cuma günü gün içi en yüksek seviyeye yakın bir kapanışla gelen %2'lik bir kazanç takip etti. Piyasanın bu performansı, genel yükselişe katkıda bulunan mega ve büyük ölçekli büyüme hisseleri tarafından yönlendirildi[1].
```

### Araç çağırma (Tool calling)

Perplexity modelleri, veri işleme veya konuşma iş akışlarınızın bir parçası olarak çağrılabilmesi için kolayca bir LlamaIndex aracına sarmalanabilir. Bu araç, Perplexity tarafından desteklenen gerçek zamanlı üretken aramayı kullanır ve güncellenmiş varsayılan model (“sonar-pro”) ve etkinleştirilmiş enable_search_classifier parametresi ile yapılandırılmıştır.

Aşağıda aracın nasıl tanımlanacağına ve kaydedileceğine dair bir örnek bulunmaktadır:

```python
from llama_index.core.tools import FunctionTool
from llama_index.llms.perplexity import Perplexity
from llama_index.core.llms import ChatMessage




def query_perplexity(query: str) -> str:
    """
    LlamaIndex entegrasyonu aracılığıyla Perplexity API'sini sorgular.


    Bu fonksiyon, güncellenmiş varsayılan ayarlarla (model "sonar-pro" kullanarak
    ve bir aramanın gerekli olup olmadığına API'nin akıllıca karar verebilmesi için
    arama sınıflandırıcısını etkinleştirerek) bir Perplexity LLM örneği oluşturur,
    sorguyu bir ChatMessage haline getirir ve oluşturulan yanıt içeriğini döndürür.
    """
    pplx_api_key = (
        "perplexity-api-anahtarınız"  # Gerçek API anahtarınızla değiştirin
    )


    llm = Perplexity(
        api_key=pplx_api_key,
        model="sonar-pro",
        temperature=0.7,
        enable_search_classifier=True,  # Bu, bu özel bağlamda arama bileşeninin gerekli olup olmadığını belirleyecektir.
    )


    messages = [ChatMessage(role="user", content=query)]
    response = llm.chat(messages)
    return response.message.content




# query_perplexity fonksiyonundan araç oluşturun
query_perplexity_tool = FunctionTool.from_defaults(fn=query_perplexity)
```
