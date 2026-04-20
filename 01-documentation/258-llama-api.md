# Llama API

---
title: Llama API
 | LlamaIndex OSS Belgeleri
---

[Llama API](https://www.llama-api.com/), fonksiyon çağırma (function calling) desteğine sahip, Llama 2 için barındırılan bir API'dir.

## Kurulum

Başlamak için, bir API anahtarı almak üzere <https://www.llama-api.com/> adresine gidin.

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-program-openai
%pip install llama-index-llms-llama-api
```

```bash
!pip install llama-index
```

```python
from llama_index.llms.llama_api import LlamaAPI
```

```python
api_key = "LL-your-key"
```

```python
llm = LlamaAPI(api_key=api_key)
```

## Temel Kullanım

#### Bir istem (prompt) ile `complete` çağrısı

```python
resp = llm.complete("Paul Graham is ")
```

```python
print(resp)
```

```
Paul Graham tanınmış bir bilgisayar bilimcisi ve girişimcidir; en çok Viaweb'in ve daha sonra başarılı bir girişim hızlandırıcısı olan Y Combinator'ın kurucu ortağı olarak tanınır. Aynı zamanda önde gelen bir denemecidir ve girişimcilik, yazılım geliştirme ve teknoloji endüstrisi gibi konularda kapsamlı yazılar yazmıştır.
```

#### Bir mesaj listesiyle `chat` çağrısı

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

```
assistant: Arrrr, ahbap! Benim adım Kaptan Siyahgaga, yedi denizin en düzenbaz köpeği! Macera dolu bir yolculuk mu arıyorsun, ha? Öyleyse yelkenleri çek ve rotayı açık denizlere kır, dostum! Hazineni bulmana yardım etmek ve yolumuza çıkmaya cüret eden tüm düzenbazlarla savaşmak için buradayım! Peki, ilk sorun nedir, seni kara yağız?
```

## Fonksiyon Çağırma (Function Calling)

```python
from pydantic import BaseModel
from llama_index.core.llms.openai_utils import to_openai_function


class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""


    name: str
    artist: str


song_fn = to_openai_function(Song)
```

```python
llm = LlamaAPI(api_key=api_key)
response = llm.complete("Generate a song", functions=[song_fn])
function_call = response.additional_kwargs["function_call"]
print(function_call)
```

```
{'name': 'Song', 'arguments': {'name': 'Happy', 'artist': 'Pharrell Williams'}}
```

## Yapılandırılmış Veri Çıkarma (Structured Data Extraction)

Bu, bir çıktıyı birden fazla şarkı içerebilen bir `Album` şemasına ayrıştırmanın (parsing) basit bir örneğidir.

Çıktı şemasını tanımlayın

```python
from pydantic import BaseModel
from typing import List


class Song(BaseModel):
    """Bir şarkı için veri modeli."""


    title: str
    length_mins: int


class Album(BaseModel):
    """Bir albüm için veri modeli."""


    name: str
    artist: str
    songs: List[Song]
```

Pydantic program tanımlayın (Llama API, OpenAI uyumludur)

```python
from llama_index.program.openai import OpenAIPydanticProgram


prompt_template_str = """\
Sağlanan metinden albümü ve şarkıları çıkarın.
Her şarkı için başlığı (title) ve süreyi (length_mins) belirttiğinizden emin olun.
{text}
"""


llm = LlamaAPI(api_key=api_key, temperature=0.0)


program = OpenAIPydanticProgram.from_defaults(
    output_cls=Album,
    llm=llm,
    prompt_template_str=prompt_template_str,
    verbose=True,
)
```

Yapılandırılmış çıktı almak için programı çalıştırın.

```python
output = program(
    text="""
"Echoes of Eternity", ünlü sanatçı Seraphina Rivers tarafından ustalıkla hazırlanmış, etkileyici ve düşündürücü bir albümdür. \
Bu büyüleyici müzik koleksiyonu, dinleyicileri insan deneyiminin derinliklerine ve evrenin enginliğine doğru içe dönük bir yolculuğa çıkarıyor. \
Büyüleyici vokalleri ve dokunaklı şarkı sözleriyle Seraphina Rivers, her parçaya ham duygular ve kozmik bir merak duygusu aşılıyor. \
Albüm, dinleyicileri göksel bir rüya alemine taşıyan ve altı dakika süren büyüleyici güzellikteki "Stardust Serenade" dahil olmak üzere birkaç öne çıkan şarkı içeriyor. \
"Eclipse of the Soul", büyüleyici melodileriyle büyülüyor ve sekiz dakikadan fazla sürerek iç gözlem ve tefekküre davet ediyor. \
Bir başka mücevher olan "Infinity Embrace", yaklaşık on dakika sürerek dinleyicileri ruhani atmosferinin derinliklerine çeken kozmik bir macera gibi açılıyor. \
"Echoes of Eternity", Seraphina Rivers'ın sanatsal yeteneğinin ustaca bir kanıtıdır ve zaman ile mekan arasındaki bu müzikal yolculuğa çıkan herkeste kalıcı bir etki bırakır.
"""
)
```

```
Function call: Album with args: {'name': 'Echoes of Eternity', 'artist': 'Seraphina Rivers', 'songs': [{'title': 'Stardust Serenade', 'length_mins': 6}, {'title': 'Eclipse of the Soul', 'length_mins': 8}, {'title': 'Infinity Embrace', 'length_mins': 10}]}
```

```python
output
```

```
Album(name='Echoes of Eternity', artist='Seraphina Rivers', songs=[Song(title='Stardust Serenade', length_mins=6), Song(title='Eclipse of the Soul', length_mins=8), Song(title='Infinity Embrace', length_mins=10)])
```
