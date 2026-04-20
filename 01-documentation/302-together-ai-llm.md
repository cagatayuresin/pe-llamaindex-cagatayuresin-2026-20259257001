# Together AI LLM

---
title: Together AI LLM
 | LlamaIndex OSS Documentation
---

Bu not defteri, `Together AI`'ın bir LLM olarak nasıl kullanılacağını gösterir. Together AI, birçok son teknoloji LLM modeline erişim sağlar. Modellerin tam listesine [buradan](https://docs.together.ai/docs/inference-models) göz atabilirsiniz.

API anahtarı almak için <https://together.ai> adresini ziyaret edin ve kaydolun.

## Kurulum

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-together
```

```python
!pip install llama-index
```

```python
from llama_index.llms.together import TogetherLLM
```

```python
# API anahtarını ortam değişkenlerinde (env) veya llm içinde ayarlayın
# import os
# os.environ["TOGETHER_API_KEY"] = "api_anahtarınız"


llm = TogetherLLM(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key="api_anahtarınız"
)
```

```python
resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

```text
Paul Graham, İngiltere doğumlu bir bilgisayar bilimcisi, risk sermayedar ve deneme yazarıdır. En çok, Dropbox, Airbnb ve Reddit dahil olmak üzere sayısız başarılı teknoloji girişimine fon ve destek sağlayan startup hızlandırıcısı ve yatırım firması Y Combinator'ın kurucu ortaklarından biri olarak tanınır.


Y Combinator'ı kurmadan önce Graham, 1995 yılında kurduğu ve daha sonra 1998'de Yahoo tarafından satın alınan Viaweb şirketinin kurucu ortaklarından biri olarak kendisi de başarılı bir girişimciydi. Graham ayrıca girişimler, teknoloji ve programlama üzerine yazdığı, teknoloji endüstrisinde geniş çapta okunan ve etkili olan denemeleriyle de tanınır.


Teknoloji endüstrisindeki çalışmalarına ek olarak Graham, Harvard Üniversitesi'nden bilgisayar bilimleri alanında doktora derecesine sahip olup yapay zeka ve bilgisayar bilimi geçmişine sahiptir. Aynı zamanda üretken bir deneme yazarıdır ve "Hackers & Painters" ile "The Hundred-Year Lie: How to Prevent Corporate Abuse and Save the World from Its Own Worst Appetites" dahil olmak üzere birkaç kitap yazmıştır.
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
```

```python
print(resp)
```

```text
asistan: Ahoy ahbap, ben Kaptan Kızıl Sakal, yedi denizde yelken açmış en azılı korsan! Gemim Kızıl Dalga, yolumuza çıkmaya cüret eden herkesin kalbine korku salar. Sadık mürettebatımla birlikte, her zaman hazine ve macera peşinde yağmalar ve talanlar yaparız. Ama yanlış anlama, bana saygı ve sadakat gösterdiğin sürece adil ve onurlu bir korsanımdır. Şimdi söyle bakalım kara faresi, senin adın ne?
```

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = llm.stream_complete("Paul Graham kimdir?")
```

```python
for r in response:
    print(r.delta, end="")
```

```text
 Paul Graham, İngiltere doğumlu bir bilgisayar bilimcisi, girişimci, risk sermayedar ve deneme yazarıdır. En çok, Dropbox, Airbnb ve Reddit dahil olmak üzere sayısız başarılı girişime fon ve destek sağlayan startup hızlandırıcısı ve yatırım firması Y Combinator'ın kurucu ortağı olarak tanınır.


Y Combinator'ı kurmadan önce Graham, 1995 yılında kurduğu ve daha sonra 1998'de Yahoo tarafından satın alınan Viaweb şirketinin kurucu ortaklarından biri olarak kendisi de başarılı bir girişimciydi. Graham ayrıca girişimler, teknoloji ve programlama üzerine yazdığı, teknoloji endüstrisinde geniş çapta okunan ve etkili olan denemeleriyle de tanınır.


Teknoloji endüstrisindeki çalışmalarına ek olarak Graham, Harvard Üniversitesi'nden bu alanda doktora derecesine sahip olup bilgisayar bilimi ve yapay zeka geçmişine sahiptir. Ayrıca Harvard ve Stanford dahil olmak üzere birkaç üniversitede programlama ve girişimcilik dersleri vermiştir.
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
 Ahoy ahbap, ben Kaptan Kızıl Sakal
engini denizlerde kurnazlığı ve cesaretiyle tanınan korkunç korsan
tabii ki bu sadece insanlara söylediğim şey. Gerçekte, gününüze biraz eğlence ve heyecan katmaya çalışan basit bir yapay zekayım!
```
