# LLM'leri Kullanma

> **İpucu:** Desteklenen LLM'lerimizin listesi ve işlevlerinin karşılaştırması için [LLM modül kılavuzumuza](/python/framework/module_guides/models/llms) göz atın.

LLM tabanlı bir uygulama oluştururken ilk adımlardan biri hangi LLM'in kullanılacağıdır; modellerin farklı güçlü yönleri ve fiyat noktaları vardır ve birden fazlasını kullanmak isteyebilirsiniz.

LlamaIndex, çok sayıda farklı LLM için tek bir arayüz sağlar. Bir LLM'i kullanmak, uygun entegrasyonu kurmak kadar basit olabilir:

```bash
pip install llama-index-llms-openai
```

Ve ardından tek bir satırla çağırmak:

```python
from llama_index.llms.openai import OpenAI

response = OpenAI().complete("William Shakespeare şudur: ")
print(response)
```

Bunun ortamınızda `OPENAI_API_KEY` adında bir API anahtarı gerektirdiğini unutmayın; daha fazla ayrıntı için [başlangıç eğitimine](/python/framework/getting_started/starter_example) bakın.

`complete` metodu ayrıca asenkron olarak `acomplete` adıyla da mevcuttur.

Ayrıca, üretildikçe token'ları döndüren bir üreteç (generator) olan `stream_complete` metodunu çağırarak bir akış (streaming) yanıtı da alabilirsiniz:

```python
handle = OpenAI().stream_complete("William Shakespeare şudur: ")

for token in handle:
    print(token.delta, end="", flush=True)
```

`stream_complete` metodu da asenkron olarak `astream_complete` adıyla mevcuttur.

## Sohbet (Chat) Arayüzü

LLM sınıfı ayrıca, daha karmaşık etkileşimler yapmanıza olanak tanıyan bir `chat` metodu da içerir:

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansınız."),
    ChatMessage(role="user", content="Bana bir fıkra anlat."),
]
chat_response = llm.chat(messages)
```

Akışlı yanıtlar için (token'lar oluşturuldukça döndürülür), `stream_chat` ve `astream_chat` metodları mevcuttus.

**Senkron (`stream_chat`):**

Engelleyici (blocking) işlemlerin kabul edilebilir olduğu standart Python betiklerinde veya notebook'larda bunu kullanın. Doğrudan bir üreteç döndürür.

```python
stream_response = llm.stream_chat(messages)

for token in stream_response:
    print(token.delta, end="", flush=True)
```

**Asenkron (`astream_chat`):**

Asenkron framework'ler (FastAPI gibi) kullanırken, metod çağrısını `await` etmeyi ve döndürülen asenkron akış üzerinde döngü kurmayı unutmayın.

```python
stream_response = await llm.astream_chat(messages)

async for token in stream_response:
    print(token.delta, end="", flush=True)
```

## Modelleri Belirleme

Birçok LLM entegrasyonu birden fazla model sunar. LLM oluşturucusuna (constructor) `model` parametresini geçerek bir model belirtebilirsiniz:

```python
llm = OpenAI(model="gpt-4o-mini")
response = llm.complete("Laurie Voss kimdir?")
print(response)
```

## Çok Modlu (Multi-Modal) LLM'ler

Bazı LLM'ler çok modlu sohbet mesajlarını destekler. Bu, metin ve diğer modların (resimler, ses, video vb.) bir karışımını geçebileceğiniz ve LLM'in bunu işleyebileceği anlamına gelir.

Şu anda LlamaIndex, içerik bloklarını (content blocks) kullanarak ChatMessage'lar içinde metin, resim ve sesi desteklemektedir.

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o")

messages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.png"),
            TextBlock(text="Resmi birkaç cümleyle açıkla."),
        ],
    )
]

resp = llm.chat(messages)
print(resp.message.content)
```

## Araç Çağırma (Tool Calling)

Bazı LLM'ler (OpenAI, Anthropic, Gemini, Ollama vb.) doğrudan API çağrıları üzerinden araç çağırmayı destekler; bu, araçların ve fonksiyonların özel komutlar ve ayrıştırma mekanizmaları olmadan çağrılabileceği anlamına gelir.

```python
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI


def generate_song(name: str, artist: str) -> dict:
    """Verilen isim ve sanatçıyla bir şarkı oluşturur."""
    return {"name": name, "artist": artist}


tool = FunctionTool.from_defaults(fn=generate_song)

llm = OpenAI(model="gpt-4o")
response = llm.predict_and_call(
    [tool],
    "Benim için rastgele bir şarkı seç",
)
print(str(response))
```

Daha gelişmiş araç çağırma hakkında ayrıntılar için, [OpenAI](/python/examples/llm/openai) kullanan derinlemesine kılavuza göz atın. Aynı yaklaşımlar araçları/fonksiyonları destekleyen tüm LLM'ler (örn. Anthropic, Gemini, Ollama vb.) için geçerlidir.

Araçlar ve ajanlar hakkında daha fazla bilgiyi [araçlar kılavuzunda](/python/framework/understanding/agent/tools) bulabilirsiniz.

## Mevcut LLM'ler

OpenAI, Anthropic, Mistral, DeepSeek, Hugging Face ve daha düzinelerce entegrasyonu destekliyoruz. Yerel bir modelin nasıl çalıştırılacağı da dahil olmak üzere tam liste için [LLM modül kılavuzumuza](/python/framework/module_guides/models/llms) göz atın.

> **İpucu:** Gizlilik ve LLM kullanımıyla ilgili genel bir nota [gizlilik sayfasından](/python/framework/understanding/privacy) ulaşabilirsiniz.

### Yerel bir LLM kullanma

LlamaIndex yalnızca barındırılan LLM API'lerini desteklemez; Meta'nın Llama 3'ü gibi yerel bir modeli de kendi makinenizde çalıştırabilirsiniz. Örneğin, makinenizde [Ollama](https://github.com/ollama/ollama) kurulu ve çalışır durumdaysa:

```python
from llama_index.llms.ollama import Ollama

llm = Ollama(
    model="llama3.3",
    request_timeout=60.0,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)
```

LLM modellerini kullanma ve yapılandırma hakkında daha fazla ayrıntı için [Özel LLM'ler Nasıl Kullanılır](/python/framework/module_guides/models/llms/usage_custom) sayfasına bakın.