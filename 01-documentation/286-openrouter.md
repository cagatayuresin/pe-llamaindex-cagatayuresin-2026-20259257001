# OpenRouter

---
title: OpenRouter
 | LlamaIndex OSS Documentation
---

OpenRouter, birçok LLM'ye sunulan en iyi fiyattan erişmek için standartlaştırılmış bir API sağlar. [Ana sayfalarından](https://openrouter.ai) daha fazla bilgi edinebilirsiniz.

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
%pip install llama-index-llms-openrouter
```

```python
!pip install llama-index
```

```python
from llama_index.llms.openrouter import OpenRouter
from llama_index.core.llms import ChatMessage
```

## Bir ChatMessage Listesi ile `chat` Çağrısı

Ya `OPENROUTER_API_KEY` ortam değişkenini ayarlamanız ya da sınıf yapılandırıcısında (constructor) `api_key` parametresini belirtmeniz gerekir.

```python
# import os
# os.environ['OPENROUTER_API_KEY'] = '<api-anahtarınız>'


llm = OpenRouter(
    api_key="<api-anahtarınız>",
    max_tokens=256,
    context_window=4096,
    model="gryphe/mythomax-l2-13b",
)
```

```python
message = ChatMessage(role="user", content="Bana bir şaka yap")
resp = llm.chat([message])
print(resp)
```

```python
assistant: Domates neden kızardı? Çünkü salata sosunu gördü!
```

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Bana 250 kelimelik bir hikaye anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

```python
Bir zamanlar, gür yeşil ormanlarla çevrili küçük bir köyde yaşayan Maria adında genç bir kız vardı. Maria, köydeki herkes tarafından sevilen nazik ve kibar bir ruhtu. Günlerinin çoğunu ormanları keşfederek, yeni bitki ve hayvan türleri keşfederek ve köylülere günlük işlerinde yardım ederek geçirirdi.

Bir gün, Maria yürüyüşe çıkmışken daha önce hiç görmediği gizli bir yola rastladı. Yolun üzeri yabani otlar ve sarmaşıklarla kaplıydı ama içinden bir şey onu çağırıyordu. Onu takip etmeye karar verdi ve yol onu ormanın derinliklerine, daha da derinlerine götürdü.

Yürüdükçe ağaçlar uzadı ve hava soğudu. Maria bir huzursuzluk hissetmeye başladı ama yolun nereye çıktığını görmeye kararlıydı. Sonunda bir açıklığa geldi ve açıklığın tam ortasında, gövdesi bir ev kadar geniş olan devasa bir ağaç duruyordu.

Maria ağaca yaklaştı ve ağacın tuhaf sembollerle kaplı olduğunu gördü. Sembollerden birine dokunmak için elini uzattı ve aniden ağaç parlamaya başladı. Parıltı gitgide güçlendi, ta ki Maria...
```

## Bir İstem (Prompt) ile `complete` Çağrısı

```python
resp = llm.complete("Bana bir şaka yap")
print(resp)
```

```python
Tabii, işte senin için bir şaka:

Bisiklet neden kendi başına ayakta duramaz?

Çünkü iki tekerleği (too-tired / yorgun) vardır!

Umarım bu yüzünüze bir gülümseme getirmiştir!
```

```python
resp = llm.stream_complete("Bana 250 kelimelik bir hikaye anlat")
for r in resp:
    print(r.delta, end="")
```

```python
Bir zamanlar Maria adında genç bir kız vardı. Gür yeşil ormanlar ve pırıl pırıl nehirlerle çevrili küçük bir köyde yaşıyordu. Maria, köydeki herkes tarafından sevilen nazik ve kibar bir ruhtu. Günlerini ailesine çiftlik işlerinde yardım ederek ve çevredeki doğayı keşfederek geçirirdi.

Bir gün ormanda dolaşırken Maria daha önce hiç görmediği gizli bir yola rastladı. Onu takip etmeye karar verdi ve yol onu yaban çiçekleriyle dolu güzel bir çayıra götürdü. Çayırın ortasında küçük bir gölet buldu ve suda kendi yansımasını gördü.

Gölete bakarken Maria kendisine doğru yaklaşan bir figür gördü. Bu, kendisini çayırın koruyucusu olarak tanıtan bilge yaşlı bir kadındı. Yaşlı kadın Maria'ya, kendisine büyük bir neşe ve mutluluk getirecek özel bir hediye almak üzere seçildiğini söyledi.

Yaşlı kadın daha sonra Maria'ya küçük, narin bir çiçek sundu. Bu çiçeğin hem fiziksel hem de duygusal her türlü yarayı iyileştirme gücüne sahip olduğunu söyledi. Maria hayretler içinde kaldı ve minnettar oldu ve çiçeği akıllıca kullanacağına söz verdi.
```

## Model Yapılandırması

```python
# https://openrouter.ai/models adresindeki seçenekleri görüntüleyin
# Bu örnek Mistral'ın MoE'si olan Mixtral'ı kullanır:
llm = OpenRouter(model="mistralai/mixtral-8x7b-instruct")
```

```python
resp = llm.complete("Rust dilinde kod yazabilen bir ejderha hakkında bir hikaye yaz")
print(resp)
```
