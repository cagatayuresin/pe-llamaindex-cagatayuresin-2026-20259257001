# Vertex AI

---
title: Vertex AI
 | LlamaIndex OSS Documentation
---

**NOT:** Vertex, büyük ölçüde `google-genai` paketini kullanarak Vertex ile aynı işlevselliği destekleyen Google GenAI ile değiştirilmiştir. En son örnekler ve dokümantasyon için [Google GenAI sayfasını](https://docs.llamaindex.ai/en/stable/examples/llm/google_genai/) ziyaret edin.

## Vertex AI'ı Yükleme

Vertex AI'ı yüklemek için aşağıdaki adımları izlemeniz gerekir:

- Vertex Cloud SDK'sını yükleyin (<https://googleapis.dev/python/aiplatform/latest/index.html>)
- Varsayılan Projenizi, kimlik bilgilerinizi ve bölgenizi ayarlayın

# Servis hesabı için temel kimlik doğrulama örneği

```python
%pip install llama-index-llms-vertex
```

```python
from llama_index.llms.vertex import Vertex
from google.oauth2 import service_account


filename = "vertex-407108-37495ce6c303.json"
credentials: service_account.Credentials = (
    service_account.Credentials.from_service_account_file(filename)
)
Vertex(
    model="text-bison", project=credentials.project_id, credentials=credentials
)
```

## Temel Kullanım

text-bison modeline temel çağrı

```python
from llama_index.llms.vertex import Vertex
from llama_index.core.llms import ChatMessage, MessageRole


llm = Vertex(model="text-bison", temperature=0, additional_kwargs={})
llm.complete("Merhaba, bu örnek bir metindir").text
```

```text
' ```\nMerhaba, bu örnek bir metindir\n```'
```

## Asenkron Kullanım

### Asenkron (Async)

```python
(await llm.acomplete("merhaba")).text
```

```text
' Merhaba! Size nasıl yardımcı olabilirim?'
```

# Akışlı (Streaming) Kullanım

### Akışlı (Streaming)

```python
list(llm.stream_complete("merhaba"))[-1].text
```

```text
' Merhaba! Size nasıl yardımcı olabilirim?'
```

# Sohbet (Chat) Kullanımı

### sohbet oluşturma

```python
chat = Vertex(model="chat-bison")
messages = [
    ChatMessage(role=MessageRole.SYSTEM, content="Her şeye Fransızca cevap ver"),
    ChatMessage(role="user", content="Merhaba"),
]
```

```python
chat.chat(messages=messages).message.content
```

```text
' Bonjour! Comment vas-tu?'
```

# Asenkron Sohbet

### Asenkron sohbet yanıtı

```python
(await chat.achat(messages=messages)).message.content
```

```text
' Bonjour! Comment vas-tu?'
```

# Akışlı Sohbet

### akışlı sohbet yanıtı

```python
list(chat.stream_chat(messages=messages))[-1].message.content
```

```text
' Bonjour! Comment vas-tu?'
```

# Gemini Modelleri

Vertex AI kullanarak Google Gemini Modellerini çağırmak tam olarak desteklenmektedir.

### Gemini Pro

```python
llm = Vertex(
    model="gemini-pro",
    project=credentials.project_id,
    credentials=credentials,
    context_window=100000,
)
llm.complete("Merhaba Gemini").text
```

### Gemini Vision Modelleri

Gemini vision özellikli modeller, artık yapılandırılmış çok modlu girdiler için `TextBlock` ve `ImageBlock` yapılarını destekleyerek eski sözlük tabanlı `content` formatının yerini almıştır. Dosya yolları veya URL'ler aracılığıyla metin ve görselleri dahil etmek için `blocks` kullanın.

**Görüntü Yolu ile Örnek:**

```python
from llama_index.llms.vertex import Vertex
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock


history = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="sample.jpg"),
            TextBlock(text="Bu görüntüde ne var?"),
        ],
    ),
]
llm = Vertex(
    model="gemini-1.5-flash",
    project=credentials.project_id,
    credentials=credentials,
    context_window=100000,
)
print(llm.chat(history).message.content)
```

```text
Görüntüde, polis memurları tarafından eşlik edilen kelepçeli bir adam görülüyor. Adam siyah bir ceket ve siyah kapüşonlu bir sweatshirt giyiyor. Kendisine siyah kar maskesi ve kurşun geçirmez yelek giymiş iki polis memuru eşlik ediyor. Memurlar Romanya Jandarması'ndan. Görüntü muhtemelen bir suçla ilgili bir haber raporundan veya belgeselden alınmış.
```

**Görüntü URL'si ile Örnek:**

```python
from llama_index.llms.vertex import Vertex
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock


history = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(
                url="https://upload.wikimedia.org/wikipedia/commons/7/71/Sibirischer_tiger_de_edit02.jpg"
            ),
            TextBlock(text="Bu görüntüde ne var?"),
        ],
    ),
]
llm = Vertex(
    model="gemini-1.5-flash",
    project=credentials.project_id,
    credentials=credentials,
    context_window=100000,
)
print(llm.chat(history).message.content)
```

```text
Bir kaplanın yüzünün yakın plan çekimi. Kaplan, ciddi bir ifadeyle doğrudan kameraya bakıyor. Kürk, turuncu, siyah ve beyazın bir karışımıdır. Arka plan bulanıklaştırılarak kaplan görüntünün ana odak noktası haline getirilmiş.
```
