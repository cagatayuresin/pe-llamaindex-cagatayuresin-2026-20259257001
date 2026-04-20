# OctoAI

---
title: OctoAI 
 | LlamaIndex OSS Belgeleri
---

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-octoai
%pip install llama-index
%pip install octoai-sdk
```

OctoAI API anahtarınızı aşağıya ekleyin. Anahtarınızı [OctoAI](https://octo.ai) adresinden alabilirsiniz.

Daha fazla rehberliğe ihtiyaç duyarsanız, [burada](https://octo.ai/docs/getting-started/how-to-create-an-octoai-access-token) bazı talimatlar bulunmaktadır.

```python
OCTOAI_API_KEY = ""
```

#### Entegrasyonu varsayılan modelle başlatma

```python
from llama_index.llms.octoai import OctoAI


octoai = OctoAI(token=OCTOAI_API_KEY)
```

#### Bir istem (prompt) ile `complete` çağrısı

```python
response = octoai.complete("Paul Graham bir ")
print(response)
```

#### Bir mesaj listesiyle `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system",
        content="Aşağıda bir görevi tanımlayan bir talimat bulunmaktadır. İsteği uygun şekilde tamamlayan bir yanıt yazın.",
    ),
    ChatMessage(role="user", content="Seattle hakkında bir blog yazısı yaz"),
]
response = octoai.chat(messages)
print(response)
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = octoai.stream_complete("Paul Graham bir ")
for r in response:
    print(r.delta, end="")
```

Bir mesaj listesiyle `stream_chat` kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system",
        content="Aşağıda bir görevi tanımlayan bir talimat bulunmaktadır. İsteği uygun şekilde tamamlayan bir yanıt yazın.",
    ),
    ChatMessage(role="user", content="Seattle hakkında bir blog yazısı yaz"),
]
response = octoai.stream_chat(messages)
for r in response:
    print(r.delta, end="")
```

## Modeli Yapılandırma

```python
# API anahtarınızı özelleştirmek için bunu yapın
# aksi takdirde ortam değişkeninizden OCTOAI_TOKEN bilgisini arayacaktır
octoai = OctoAI(
    model="mistral-7b-instruct", max_tokens=128, token=OCTOAI_API_KEY
)


response = octoai.complete("Paul Graham bir ")
print(response)
```
