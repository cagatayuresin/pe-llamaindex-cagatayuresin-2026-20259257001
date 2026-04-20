# DeepInfra

## Kurulum

Öncelikle gerekli paketi kurun:

```bash
%pip install llama-index-llms-deepinfra
```

```python
%pip install llama-index-llms-deepinfra
```

## Başlatma (Initialization)

API anahtarınız ve istediğiniz parametrelerle `DeepInfraLLM` sınıfını kurun:

```python
from llama_index.llms.deepinfra import DeepInfraLLM
import asyncio

llm = DeepInfraLLM(
    model="mistralai/Mixtral-8x22B-Instruct-v0.1",  # Varsayılan model adı
    api_key="deepinfra-api-anahtarınız",  # DeepInfra API anahtarınızla değiştirin
    temperature=0.5,
    max_tokens=50,
    additional_kwargs={"top_p": 0.9},
)
```

## Senkron Tamamlama (Synchronous Complete)

`complete` yöntemini kullanarak senkronize bir metin tamamlaması oluşturun:

```python
response = llm.complete("Merhaba Dünya!")
print(response.text)
```

## Senkron Akışlı Tamamlama (Synchronous Stream Complete)

`stream_complete` yöntemini kullanarak senkronize bir akışlı metin tamamlaması oluşturun:

```python
content = ""
for completion in llm.stream_complete("Bir varmış bir yokmuş"):
    content += completion.delta
    print(completion.delta, end="")
```

## Senkron Sohbet (Synchronous Chat)

`chat` yöntemini kullanarak senkronize bir sohbet yanıtı oluşturun:

```python
from llama_index.core.base.llms.types import ChatMessage

messages = [
    ChatMessage(role="user", content="Bana bir şaka anlat."),
]
chat_response = llm.chat(messages)
print(chat_response.message.content)
```

## Senkron Akışlı Sohbet (Synchronous Stream Chat)

`stream_chat` yöntemini kullanarak senkronize bir akışlı sohbet yanıtı oluşturun:

```python
messages = [
    ChatMessage(role="system", content="Sen yardımcı bir asistansın."),
    ChatMessage(role="user", content="Bana bir hikaye anlat."),
]
content = ""
for chat_response in llm.stream_chat(messages):
    content += chat_response.message.delta
    print(chat_response.message.delta, end="")
```

## Asenkron Tamamlama (Asynchronous Complete)

`acomplete` yöntemini kullanarak asenkron bir metin tamamlaması oluşturun:

```python
async def async_complete():
    response = await llm.acomplete("Merhaba Asenkron Dünya!")
    print(response.text)


asyncio.run(async_complete())
```

## Asenkron Akışlı Tamamlama (Asynchronous Stream Complete)

`astream_complete` yöntemini kullanarak asenkron bir akışlı metin tamamlaması oluşturun:

```python
async def async_stream_complete():
    content = ""
    response = await llm.astream_complete("Asenkron bir zamanda bir varmış bir yokmuş")
    async for completion in response:
        content += completion.delta
        print(completion.delta, end="")


asyncio.run(async_stream_complete())
```

## Asenkron Sohbet (Asynchronous Chat)

`achat` yöntemini kullanarak asenkron bir sohbet yanıtı oluşturun:

```python
async def async_chat():
    messages = [
        ChatMessage(role="user", content="Bana asenkron bir şaka anlat."),
    ]
    chat_response = await llm.achat(messages)
    print(chat_response.message.content)


asyncio.run(async_chat())
```

## Asenkron Akışlı Sohbet (Asynchronous Stream Chat)

`astream_chat` yöntemini kullanarak asenkron bir akışlı sohbet yanıtı oluşturun:

```python
async def async_stream_chat():
    messages = [
        ChatMessage(role="system", content="Sen yardımcı bir asistansın."),
        ChatMessage(role="user", content="Bana asenkron bir hikaye anlat."),
    ]
    content = ""
    response = await llm.astream_chat(messages)
    async for chat_response in response:
        content += chat_response.message.delta
        print(chat_response.message.delta, end="")


asyncio.run(async_stream_chat())
```

---

Herhangi bir sorunuz veya geri bildiriminiz için lütfen [feedback@deepinfra.com](mailto:feedback@deepinfra.com) adresinden bizimle iletişime geçin.
