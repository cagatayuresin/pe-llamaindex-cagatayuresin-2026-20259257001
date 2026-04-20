# Apertis

Apertis; OpenAI, Anthropic, Google ve daha fazlası dahil olmak üzere birden fazla LLM sağlayıcısına OpenAI uyumlu bir arayüz aracılığıyla erişmek için birleşik bir API ağ geçidi sağlar. Daha fazlasını [dokümantasyonlarından](https://docs.stima.tech) öğrenebilirsiniz.

**Desteklenen Bitiş Noktaları (Endpoints):**
- `/v1/chat/completions` - OpenAI Sohbet Tamamlama formatı (varsayılan)
- `/v1/responses` - OpenAI Yanıtları formatı ile uyumlu
- `/v1/messages` - Anthropic formatı ile uyumlu

Eğer bu Not Defterini colab üzerinden açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-apertis
```

```python
!pip install llama-index
```

```python
from llama_index.llms.apertis import Apertis
from llama_index.core.llms import ChatMessage
```

## ChatMessage Listesi ile `chat` Çağrısı
`APERTIS_API_KEY` ortam değişkenini ayarlamanız veya sınıf yapıcıda (constructor) api_key değerini belirtmeniz gerekir.

```python
# import os
# os.environ['APERTIS_API_KEY'] = '<api-anahtarınız>'

llm = Apertis(
    api_key="<api-anahtarınız>",
    max_tokens=256,
    context_window=4096,
    model="gpt-5.2",
)
```

```python
message = ChatMessage(role="user", content="Bana bir fıkra anlat")
resp = llm.chat([message])
print(resp)
```

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Bana 250 kelimelik bir hikaye anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

## İstem (Prompt) ile `complete` Çağrısı

```python
resp = llm.complete("Bana bir fıkra anlat")
print(resp)
```

```python
resp = llm.stream_complete("Bana 250 kelimelik bir hikaye anlat")
for r in resp:
    print(r.delta, end="")
```

## Model Yapılandırması

Apertis birden fazla sağlayıcıdan gelen modelleri destekler:

| Sağlayıcı | Örnek Modeller |
|-----------|----------------|
| OpenAI | `gpt-5.2`, `gpt-5-mini-2025-08-07` |
| Anthropic | `claude-sonnet-4.5` |
| Google | `gemini-3-flash-preview` |

```python
# Claude Kullanımı
llm = Apertis(model="claude-sonnet-4.5")
```

```python
resp = llm.complete("Rust dilinde kod yazabilen bir ejderha hakkında bir hikaye yaz")
print(resp)
```

```python
# Gemini Kullanımı
llm = Apertis(model="gemini-3-flash-preview")
```

```python
resp = llm.complete("Kuantum bilgisayarları basit terimlerle açıkla")
print(resp)
```
