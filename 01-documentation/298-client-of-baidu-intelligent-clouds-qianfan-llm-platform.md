# Baidu Akıllı Bulut Qianfan LLM Platformu İstemcisi

---
title: Baidu Akıllı Bulut Qianfan LLM Platformu İstemcisi
 | LlamaIndex OSS Documentation
---

Baidu Akıllı Bulut'un Qianfan LLM Platformu; ERNIE-3.5-8K ve ERNIE-4.0-8K gibi tüm Baidu LLM'leri için API servisleri sunar. Ayrıca Llama-2-70b-chat gibi az sayıda açık kaynaklı LLM de sağlar.

Sohbet istemcisini kullanmadan önce, Qianfan LLM Platformu konsolunun [çevrimiçi servis](https://console.bce.baidu.com/qianfan/ais/console/onlineService) sayfasındaki LLM servisini aktif etmeniz gerekir. Ardından, konsolun [Güvenlik Kimlik Doğrulaması](https://console.bce.baidu.com/iam/#/iam/accesslist) sayfasında bir Erişim Anahtarı (Access Key) ve Gizli Anahtar (Secret Key) oluşturun.

## Kurulum

Gerekli paketi kurun:

```python
%pip install llama-index-llms-qianfan
```

## Başlatma (Initialization)

```python
from llama_index.llms.qianfan import Qianfan
import asyncio


access_key = "XXX"
secret_key = "XXX"
model_name = "ERNIE-Speed-8K"
endpoint_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed"
context_window = 8192
llm = Qianfan(access_key, secret_key, model_name, endpoint_url, context_window)
```

## Senkron Sohbet (Synchronous Chat)

`chat` yöntemini kullanarak senkronize olarak bir sohbet yanıtı oluşturun:

```python
from llama_index.core.base.llms.types import ChatMessage


messages = [
    ChatMessage(role="user", content="Bana bir fıkra anlat."),
]
chat_response = llm.chat(messages)
print(chat_response.message.content)
```

## Senkron Akışlı Sohbet (Synchronous Stream Chat)

`stream_chat` yöntemini kullanarak senkronize olarak akışlı bir sohbet yanıtı oluşturun:

```python
messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın."),
    ChatMessage(role="user", content="Bana bir hikaye anlat."),
]
content = ""
for chat_response in llm.stream_chat(messages):
    content += chat_response.delta
    print(chat_response.delta, end="")
```

## Asenkron Sohbet (Asynchronous Chat)

`achat` yöntemini kullanarak asenkron olarak bir sohbet yanıtı oluşturun:

```python
async def async_chat():
    messages = [
        ChatMessage(role="user", content="Bana asenkron bir fıkra anlat."),
    ]
    chat_response = await llm.achat(messages)
    print(chat_response.message.content)




asyncio.run(async_chat())
```

## Asenkron Akışlı Sohbet (Asynchronous Stream Chat)

`astream_chat` yöntemini kullanarak asenkron olarak akışlı bir sohbet yanıtı oluşturun:

```python
async def async_stream_chat():
    messages = [
        ChatMessage(role="system", content="Yardımsever bir asistansın."),
        ChatMessage(role="user", content="Bana asenkron bir hikaye anlat."),
    ]
    content = ""
    response = await llm.astream_chat(messages)
    async for chat_response in response:
        content += chat_response.delta
        print(chat_response.delta, end="")




asyncio.run(async_stream_chat())
```
