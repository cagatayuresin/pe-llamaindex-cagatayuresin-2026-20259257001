# SambaNova Systems

---
title: SambaNova Systems
 | LlamaIndex OSS Documentation
---

Bu not defterinde [SambaNova Cloud](https://cloud.sambanova.ai/) ve [SambaStudio](https://docs.sambanova.ai/sambastudio/latest/sambastudio-intro.html) platformlarını nasıl kuracağınızı, yapılandıracağınızı ve kullanacağınızı öğreneceksiniz. Bir göz atın ve kendiniz deneyin!

# SambaNova Cloud

[SambaNova Cloud](https://cloud.sambanova.ai/), hızlı ve kesin sonuçlar sunan yüksek performanslı bir çıkarım (inference) servisidir. Müşteriler, FastAPI çıkarım API'lerini uygulamalarıyla entegre ederek kullanıcı deneyimlerini geliştirmek için SambaNova teknolojisinden sorunsuz bir şekilde yararlanabilirler. Bu servis, çıkarım sonuçlarını akışla (streaming) iletmek için kullanımı kolay bir REST arayüzü sağlar. Kullanıcılar çıkarım parametrelerini özelleştirebilir ve ML modelini servise aktarabilirler.

## Kurulum

SambaNova Cloud modeline erişmek için bir [SambaNovaCloud](https://cloud.sambanova.ai/apis) hesabı oluşturmanız, bir API anahtarı almanız, `llama-index-llms-sambanova` entegrasyon paketini kurmanız ve `SSEClient` paketini yüklemeniz gerekir.

```python
%pip install llama-index-llms-sambanovasystems
%pip install sseclient-py
```

### Kimlik Bilgileri (Credentials)

[cloud.sambanova.ai](https://cloud.sambanova.ai/apis) adresinden bir API Anahtarı alın ve bunu ortam değişkenlerinize ekleyin:

Terminal penceresi

```bash
export SAMBANOVA_API_KEY="api-anahtarınız-buraya"
```

Eğer ortam değişkenlerinizde yoksa, açılır giriş metni kutusuna da ekleyebilirsiniz.

```python
import getpass
import os


if not os.getenv("SAMBANOVA_API_KEY"):
    os.environ["SAMBANOVA_API_KEY"] = getpass.getpass(
        "SambaNova Cloud API anahtarınızı girin: "
    )
```

## Örneklendirme (Instantiation)

Artık model nesnemizi örneklendirebilir ve sohbet tamamlamaları oluşturabiliriz:

```python
from llama_index.llms.sambanovasystems import SambaNovaCloud


llm = SambaNovaCloud(
    model="Meta-Llama-3.1-70B-Instruct",
    context_window=100000,
    max_tokens=1024,
    temperature=0.7,
    top_k=1,
    top_p=0.01,
)
```

## Çağırma (Invocation)

Aşağıdaki sistem ve kullanıcı mesajlarını göz önüne alarak, bir SambaNova Cloud modelini çağırmanın farklı yollarını inceleyelim.

```python
from llama_index.core.base.llms.types import (
    ChatMessage,
    MessageRole,
)


system_msg = ChatMessage(
    role=MessageRole.SYSTEM,
    content="İngilizceyi Fransızcaya çeviren yardımsever bir asistansın. Kullanıcının cümlesini çevir.",
)
user_msg = ChatMessage(role=MessageRole.USER, content="Programlamayı seviyorum.")


messages = [
    system_msg,
    user_msg,
]
```

### Sohbet (Chat)

```python
ai_msg = llm.chat(messages)
ai_msg.message
```

```python
print(ai_msg.message.content)
```

### Tamamlama (Complete)

```python
ai_msg = llm.complete(user_msg.content)
ai_msg
```

```python
print(ai_msg.text)
```

## Akış (Streaming)

### Sohbet (Chat)

```python
ai_stream_msgs = []
for stream in llm.stream_chat(messages):
    ai_stream_msgs.append(stream)
ai_stream_msgs
```

```python
print(ai_stream_msgs[-1])
```

### Tamamlama (Complete)

```python
ai_stream_msgs = []
for stream in llm.stream_complete(user_msg.content):
    ai_stream_msgs.append(stream)
ai_stream_msgs
```

```python
print(ai_stream_msgs[-1])
```

## Asenkron (Async)

### Sohbet (Chat)

```python
ai_msg = await llm.achat(messages)
ai_msg
```

```python
print(ai_msg.message.content)
```

### Tamamlama (Complete)

```python
ai_msg = await llm.acomplete(user_msg.content)
ai_msg
```

```python
print(ai_msg.text)
```

## Asenkron Akış (Async Streaming)

Henüz desteklenmiyor. Yakında gelecek!

# SambaStudio

[SambaStudio](https://docs.sambanova.ai/sambastudio/latest/sambastudio-intro.html), modelleri eğitme, dağıtma ve yönetme işlevselliği sağlayan zengin, GUI tabanlı bir platformdur.

## Kurulum

SambaStudio modellerine erişmek için **SambaNova müşterisi** olmanız, GUI veya CLI kullanarak bir uç nokta (endpoint) dağıtmanız ve [SambaStudio uç nokta dokümantasyonunda](https://docs.sambanova.ai/sambastudio/latest/endpoints.html#_endpoint_api_keys) açıklandığı gibi uç noktaya bağlanmak için URL'yi ve API Anahtarını kullanmanız gerekir. Ardından, `llama-index-llms-sambanova` entegrasyon paketini kurun ve `SSEClient` paketini yükleyin.

```python
%pip install llama-index-llms-sambanova
%pip install sseclient-py
```

### Kimlik Bilgileri (Credentials)

URL ve API Anahtarını almak için SambaStudio'da bir uç nokta dağıtılmalıdır. Bunlar kullanılabilir olduğunda, ortam değişkenlerinize ekleyin:

Terminal penceresi

```bash
export SAMBASTUDIO_URL="url-adresiniz-buraya"
export SAMBASTUDIO_API_KEY="api-anahtarınız-buraya"
```

```python
import getpass
import os


if not os.getenv("SAMBASTUDIO_URL"):
    os.environ["SAMBASTUDIO_URL"] = getpass.getpass(
        "SambaStudio uç nokta (endpoint) URL'nizi girin: "
    )


if not os.getenv("SAMBASTUDIO_API_KEY"):
    os.environ["SAMBASTUDIO_API_KEY"] = getpass.getpass(
        "SambaStudio uç nokta (endpoint) API anahtarınızı girin: "
    )
```

## Örneklendirme (Instantiation)

Artık model nesnemizi örneklendirebilir ve sohbet tamamlamaları oluşturabiliriz:

```python
from llama_index.llms.sambanovasystems import SambaStudio


llm = SambaStudio(
    model="Meta-Llama-3-70B-Instruct-4096",
    context_window=100000,
    max_tokens=1024,
    temperature=0.7,
    top_k=1,
    top_p=0.01,
)
```

## Çağırma (Invocation)

Aşağıdaki sistem ve kullanıcı mesajlarını göz önüne alarak, bir SambaStudio modelini çağırmanın farklı yollarını inceleyelim.

```python
from llama_index.core.base.llms.types import (
    ChatMessage,
    MessageRole,
)


system_msg = ChatMessage(
    role=MessageRole.SYSTEM,
    content="İngilizceyi Fransızcaya çeviren yardımsever bir asistansın. Kullanıcının cümlesini çevir.",
)
user_msg = ChatMessage(role=MessageRole.USER, content="Programlamayı seviyorum.")


messages = [
    system_msg,
    user_msg,
]
```

### Sohbet (Chat)

```python
ai_msg = llm.chat(messages)
ai_msg.message
```

```python
print(ai_msg.message.content)
```

### Tamamlama (Complete)

```python
ai_msg = llm.complete(user_msg.content)
ai_msg
```

```python
print(ai_msg.text)
```

## Akış (Streaming)

### Sohbet (Chat)

```python
ai_stream_msgs = []
for stream in llm.stream_chat(messages):
    ai_stream_msgs.append(stream)
ai_stream_msgs
```

```python
print(ai_stream_msgs[-1])
```

### Tamamlama (Complete)

```python
ai_stream_msgs = []
for stream in llm.stream_complete(user_msg.content):
    ai_stream_msgs.append(stream)
ai_stream_msgs
```

```python
print(ai_stream_msgs[-1])
```

## Asenkron (Async)

### Sohbet (Chat)

```python
ai_msg = await llm.achat(messages)
ai_msg
```

```python
print(ai_msg.message.content)
```

### Tamamlama (Complete)

```python
ai_msg = await llm.acomplete(user_msg.content)
ai_msg
```

```python
print(ai_msg.text)
```

## Asenkron Akış (Async Streaming)

Henüz desteklenmiyor. Yakında gelecek!
