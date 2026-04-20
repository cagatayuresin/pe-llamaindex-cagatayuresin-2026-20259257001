# Nebius LLM'leri

---
title: Nebius LLM'leri
 | LlamaIndex OSS Belgeleri
---

Bu not defteri, LlamaIndex ile [Nebius AI Studio](https://studio.nebius.ai/)'dan LLM'lerin nasıl kullanılacağını gösterir. Nebius AI Studio, ticari kullanım için mevcut olan tüm son teknoloji LLM'leri uygular.

Öncelikle LlamaIndex'i ve Nebius AI Studio bağımlılıklarını kuralım.

```bash
%pip install llama-index-llms-nebius llama-index
```

Aşağıdaki sistem değişkenlerinden Nebius AI Studio anahtarınızı yükleyin veya doğrudan ekleyin. [Nebius AI Studio](https://auth.eu.nebius.com/ui/login) adresinden ücretsiz kaydolarak ve [API Anahtarları bölümünden](https://studio.nebius.ai/settings/api-keys) anahtarı oluşturarak alabilirsiniz.

```python
import os


NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")  # veya NEBIUS_API_KEY = "anahtarınız"
```

```python
from llama_index.llms.nebius import NebiusLLM


llm = NebiusLLM(
    api_key=NEBIUS_API_KEY, model="meta-llama/Llama-3.3-70B-Instruct-fast"
)
```

#### Bir istem (prompt) ile `complete` çağrısı

```python
response = llm.complete("Amsterdam buranın başkentidir: ")
print(response)
```

```
Hollanda! Amsterdam gerçekten de Hollanda'nın başkenti ve en büyük şehridir.
```

#### Bir mesaj listesiyle `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(role="system", content="Yardımsever bir yapay zeka asistanısın."),
    ChatMessage(
        role="user",
        content="Kısaca cevapla: Wall-e kimdir?",
    ),
]
response = llm.chat(messages)
print(response)
```

```
assistant: WALL-E, aynı adı taşıyan 2008 yapımı Pixar animasyon filminin baş karakteri olan küçük bir atık toplama robotudur.
```

### Akış (Streaming)

#### `stream_complete` uç noktasını kullanma

```python
response = llm.stream_complete("Amsterdam buranın başkentidir: ")
for r in response:
    print(r.delta, end="")
```

```
Hollanda! Amsterdam gerçekten de Hollanda'nın başkenti ve en büyük şehridir.
```

#### Mesaj listesiyle `stream_chat` kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(role="system", content="Yardımsever bir yapay zeka asistanısın."),
    ChatMessage(
        role="user",
        content="Kısaca cevapla: Wall-e kimdir?",
    ),
]
response = llm.stream_chat(messages)
for r in response:
    print(r.delta, end="")
```

```
WALL-E, aynı adı taşıyan 2008 yapımı Pixar animasyon filminin baş karakteri olan küçük bir atık toplama robotudur.
```
