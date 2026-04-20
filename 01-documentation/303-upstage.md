# Upstage

---
title: Upstage
 | LlamaIndex OSS Documentation
---

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-upstage llama-index
```

## Temel Kullanım

#### Bir istem (prompt) ile `complete` fonksiyonunu çağırın

```python
import os


os.environ["UPSTAGE_API_KEY"] = "API_ANAHTARINIZ"
```

```python
from llama_index.llms.upstage import Upstage


llm = Upstage(
    model="solar-mini",
    # api_key="API_ANAHTARINIZ"  # varsayılan olarak UPSTAGE_API_KEY ortam değişkenini kullanır
)


resp = llm.complete("Paul Graham ")
```

```python
print(resp)
```

```text
Paul Graham bir bilgisayar bilimcisi, girişimci ve deneme yazarıdır. En çok, birçok başarılı girişime fon sağlayan ve kuluçka merkezi olan risk sermayesi şirketi Y Combinator'ın kurucu ortağı olarak tanınır. Ayrıca girişimcilik, startup kültürü ve teknoloji üzerine yazdığı birkaç etkili denemenin de yazarıdır.
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
asistan: Ben Kaptan Kızıl Sakal, korkusuz korsan!
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham ")
```

```python
for r in resp:
    print(r.delta, end="")
```

```text
Paul Graham bir bilgisayar bilimcisi, girişimci ve deneme yazarıdır. En çok, Airbnb, Dropbox ve Stripe gibi dünyanın en başarılı teknoloji şirketlerinden bazılarının kurulmasına yardımcı olan startup hızlandırıcısı Y Combinator'ın kurucu ortağı olarak tanınır. Ayrıca, "How to Start a Startup" ve "Hackers & Painters" dahil olmak üzere startup kültürü ve girişimcilik üzerine yazdığı birkaç etkili denemenin yazarıdır.
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
Ben Kaptan Kızıl Sakal, korkusuz korsan!
```

## Fonksiyon Çağırma (Function Calling)

Upstage modelleri, fonksiyon çağırma için yerel desteğe sahiptir. Bu, LlamaIndex araç soyutlamalarıyla kolayca entegre olur ve herhangi bir Python fonksiyonunu LLM'ye bağlamanıza olanak tanır.

```python
from pydantic import BaseModel
from llama_index.core.tools import FunctionTool




class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""


    name: str
    artist: str




def generate_song(name: str, artist: str) -> Song:
    """Sağlanan ad ve sanatçı ile bir şarkı oluşturur."""
    return Song(name=name, artist=artist)




tool = FunctionTool.from_defaults(fn=generate_song)
```

```python
from llama_index.llms.upstage import Upstage


llm = Upstage()
response = llm.predict_and_call([tool], "Bir şarkı oluştur")
print(str(response))
```

```text
name='Şarkım' artist='Can Doe'
```

Ayrıca birden fazla fonksiyon çağırma işlemi de yapabiliriz.

```python
llm = Upstage()
response = llm.predict_and_call(
    [tool],
    "Beatles'tan beş şarkı oluştur",
    allow_parallel_tool_calls=True,
)
for s in response.sources:
    print(f"Ad: {s.tool_name}, Girdi: {s.raw_input}, Çıktı: {str(s)}")
```

```text
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Beatles', 'artist': 'Beatles'}}, Çıktı: name='Beatles' artist='Beatles'
```

## Asenkron (Async)

```python
from llama_index.llms.upstage import Upstage


llm = Upstage()
```

```python
resp = await llm.acomplete("Paul Graham ")
```

```python
print(resp)
```

```text
Paul Graham bir bilgisayar bilimcisi, girişimci ve deneme yazarıdır. En çok, birçok başarılı teknoloji şirketinin kurulmasına ve fonlanmasına yardımcı olan startup hızlandırıcısı Y Combinator'ın kurucu ortağı olarak tanınır. Ayrıca, "How to Start a Startup" ve "Hackers & Painters" dahil olmak üzere startup'lar, girişimcilik ve teknoloji üzerine yazdığı birkaç etkili denemenin yazarıdır.
```

```python
resp = await llm.astream_complete("Paul Graham ")
```

```python
async for delta in resp:
    print(delta.delta, end="")
```

```text
Paul Graham bir bilgisayar bilimcisi, girişimci ve deneme yazarıdır. En çok, Airbnb, Dropbox ve Stripe gibi dünyanın en başarılı teknoloji şirketlerinden bazılarının kurulmasına yardımcı olan startup hızlandırıcısı Y Combinator'ın kurucu ortağı olarak tanınır. Graham aynı zamanda üretken bir yazardır ve startup tavsiyeleri, yapay zeka ve işin geleceği gibi konulardaki denemeleri teknoloji endüstrisinde geniş çapta okunmuş ve etkili olmuştur.
```

Asenkron fonksiyon çağırma da desteklenmektedir.

```python
llm = Upstage()
response = await llm.apredict_and_call([tool], "Bir şarkı oluştur")
print(str(response))
```

```text
name='Şarkım' artist='Ben'
```
