# Maritalk

---
title: Maritalk
 | LlamaIndex OSS Belgeleri
---

## Giriş

MariTalk, Brezilyalı şirket [Maritaca AI](https://www.maritaca.ai) tarafından geliştirilen bir asistandır. MariTalk, Portekizceyi iyi anlamak üzere özel olarak eğitilmiş dil modellerine dayanmaktadır.

Bu not defteri, MariTalk'un Llama Index ile nasıl kullanılacağını iki örnekle göstermektedir:

1. Sohbet (chat) yöntemiyle evcil hayvan ismi önerileri alma;
2. Tamamlama (complete) yöntemiyle few-shot örnekleri kullanarak film incelemelerini negatif veya pozitif olarak sınıflandırma.

## Kurulum

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i kurmanız gerekecektir.

```bash
!pip install llama-index
!pip install llama-index-llms-maritalk
!pip install asyncio
```

## API Anahtarı

chat.maritaca.ai adresinden ("Chaves da API" bölümü) alabileceğiniz bir API anahtarına ihtiyacınız olacak.

### Örnek 1 - Sohbet (Chat) ile Evcil Hayvan İsim Önerileri

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.maritalk import Maritalk


import asyncio


# API anahtarınızı özelleştirmek için bunu yapın
# aksi takdirde ortam değişkeninizden MARITALK_API_KEY'i arayacaktır
llm = Maritalk(api_key="<your_maritalk_api_key>", model="sabia-2-medium")


# Mesaj listesiyle sohbeti çağırın
messages = [
    ChatMessage(
        role="system",
        content="Evcil hayvan isimleri önerme konusunda uzmanlaşmış bir asistansın. Verilen hayvana göre 4 isim önermelisin.",
    ),
    ChatMessage(role="user", content="Bir köpeğim var."),
]


# Senkron sohbet (Sync chat)
response = llm.chat(messages)
print(response)




# Asenkron sohbet (Async chat)
async def get_dog_name(llm, messages):
    response = await llm.achat(messages)
    print(response)




asyncio.run(get_dog_name(llm, messages))
```

#### Akış (Stream) Oluşturma

Kapsamlı bir makale oluşturma veya büyük bir belgeyi çevirme gibi uzun metin oluşturma içeren görevlerde, yanıtı metin oluşturuldukça parça parça almak, metnin tamamını beklemek yerine avantajlı olabilir. Bu, özellikle oluşturulan metin kapsamlı olduğunda uygulamayı daha duyarlı ve verimli hale getirir. Bu ihtiyacı karşılamak için iki yaklaşım sunuyoruz: biri senkron, diğeri asenkron.

```python
# Senkron akışlı sohbet (Sync streaming chat)
response = llm.stream_chat(messages)
for chunk in response:
    print(chunk.delta, end="", flush=True)




# Asenkron akışlı sohbet (Async streaming chat)
async def get_dog_name_streaming(llm, messages):
    async for chunk in await llm.astream_chat(messages):
        print(chunk.delta, end="", flush=True)




asyncio.run(get_dog_name_streaming(llm, messages))
```

### Örnek 2 - Tamamlama (Complete) ile Few-shot Örnekleri

Modeli few-shot örnekleriyle kullanırken `llm.complete()` yöntemini kullanmanızı öneririz.

```python
prompt = """Film incelemesini "pozitif" veya "negatif" olarak sınıflandırın.


İnceleme: Filmi çok beğendim, yılın en iyisi!
Sınıf: pozitif


İnceleme: Film beklentilerin çok altında kalıyor.
Sınıf: negatif


İnceleme: Uzun olmasına rağmen bilet parasına değdi..
Sınıf:"""


# Senkron tamamlama (Sync complete)
response = llm.complete(prompt)
print(response)




# Asenkron tamamlama (Async complete)
async def classify_review(llm, prompt):
    response = await llm.acomplete(prompt)
    print(response)




asyncio.run(classify_review(llm, prompt))
```

```python
# Senkron akışlı tamamlama (Sync streaming complete)
response = llm.stream_complete(prompt)
for chunk in response:
    print(chunk.delta, end="", flush=True)




# Asenkron akışlı tamamlama (Async streaming complete)
async def classify_review_streaming(llm, prompt):
    async for chunk in await llm.astream_complete(prompt):
        print(chunk.delta, end="", flush=True)




asyncio.run(classify_review_streaming(llm, prompt))
```
