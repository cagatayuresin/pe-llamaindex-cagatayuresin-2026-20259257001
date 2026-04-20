# Yi LLM Modelleri

---
title: Yi LLMs
 | LlamaIndex OSS Documentation
---

Bu not defteri, Yi serisi LLM'lerin nasıl kullanılacağını göstermektedir.

Bu Not Defterini colab üzerinde açıyorsanız, LlamaIndex 🦙 ve Yi Python SDK'sını yüklemeniz gerekecektir.

```python
%pip install llama-index-llms-yi
```

```python
!pip install llama-index
```

## Temel Kullanım

[platform.01.ai](https://platform.01.ai/apikeys) adresinden bir API anahtarı almanız gerekecektir. Bir anahtarınız olduğunda, bunu modele doğrudan iletebilir veya `YI_API_KEY` ortam değişkenini kullanabilirsiniz.

Detaylar aşağıdaki gibidir:

```python
import os


os.environ["YI_API_KEY"] = "api anahtarınız"
```

#### Bir istem (prompt) ile `complete` fonksiyonunu çağırın

```python
from llama_index.llms.yi import Yi


llm = Yi(model="yi-large")
response = llm.complete("Fransa'nın başkenti neresidir?")
print(response)
```

```text
Fransa'nın başkenti Paris'tir.
```

#### Bir mesaj listesi ile `chat` fonksiyonunu çağırın

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.chat(messages)
print(resp)
```

```text
asistan: Hey hey, dostum! Benim adım Kaptan Kara Sakal, ama sen bana kısaca Kara Sakal diyebilirsin. Şimdi, seni gemime getiren nedir? Hazine ve macera arayışıyla yedi denize yelken açmaya hazır mısın?
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
from llama_index.llms.yi import Yi


llm = Yi(model="yi-large")
response = llm.stream_complete("Paul Graham kimdir?")
```

```python
for r in response:
    print(r.delta, end="")
```

```text
Paul Graham, İngiliz-Amerikalı bir bilgisayar bilimcisi, girişimci ve deneme yazarıdır. En çok Lisp programlama dili üzerine yaptığı çalışmalarla ve Dropbox, Airbnb, Stripe ve Coinbase gibi başarılı şirketlerin kurulmasına yardımcı olan bir startup hızlandırıcısı olan Y Combinator'ın kurucu ortağı olarak tanınır.

Graham'ın kariyeri onlarca yıla yayılmaktadır ve Viaweb'i kurmayı (daha sonra Yahoo!'ya satıldı ve Yahoo! Store olarak yeniden markalandı), startup'lar, teknoloji ve girişimcilik üzerine etkili denemeler yazmayı ve yazılım geliştirmede Lisp kullanımını savunmayı içermektedir. Çok geniş bir yelpazedeki konuları kapsayan denemeleri yaygın olarak okunmuş ve teknoloji topluluğu üzerinde önemli bir etki yaratmıştır.

Y Combinator aracılığıyla Graham, girişimcilere sadece finansal destek değil, aynı zamanda mentorluk ve tavsiye de sağlayarak startup ekosisteminde kilit bir rol oynamıştır. Startup fonlamasına yaklaşımı ve kurucuların ve fikirlerin önemine yaptığı vurgu, teknoloji endüstrisinde etkili olmuştur.
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```text
Bir yapay zeka olarak kişisel bir ismim yok, ama bana istediğin şekilde hitap edebilirsin! Kaptan Yapay Zeka Sakal'a ne dersin?
```
