# Neutrino AI

---
title: Neutrino AI
 | LlamaIndex OSS Belgeleri
---

Neutrino, sorguları istem (prompt) için en uygun LLM'ye akıllıca yönlendirmenizi sağlayarak bir yandan maliyetleri ve gecikmeyi optimize ederken diğer yandan performansı en üst düzeye çıkarır.

Bizi buradan inceleyin: [neutrinoapp.com](https://www.neutrinoapp.com/) Belgeler: [docs.neutrinoapp.com](https://docs.neutrinoapp.com/) API anahtarı oluşturun: [platform.neutrinoapp.com](https://platform.neutrinoapp.com/)

```bash
%pip install llama-index-llms-neutrino
```

```bash
!pip install llama-index
```

#### Neutrino API Anahtarı Ortam Değişkenini Ayarla

[platform.neutrinoapp.com](https://platform.neutrinoapp.com/) adresinden bir API anahtarı oluşturabilirsiniz.

```python
import os


os.environ["NEUTRINO_API_KEY"] = "<neutrino-api-anahtarınız>"
```

#### Yönlendiricinizi (Router) Kullanma

Yönlendirici, sorguları yönlendirebileceğiniz bir LLM koleksiyonudur. Neutrino [kontrol panelinde](https://platform.neutrinoapp.com/) bir yönlendirici oluşturabilir veya desteklenen tüm modelleri içeren varsayılan yönlendiriciyi kullanabilirsiniz. Bir yönlendiriciye bir LLM gibi davranabilirsiniz.

```python
from llama_index.llms.neutrino import Neutrino
from llama_index.core.llms import ChatMessage


llm = Neutrino(
    # api_key="<neutrino-api-anahtarınız>",
    # router="<yönlendirici-id-niz>"  # (veya 'default')
)


response = llm.complete("In short, a Neutrino is")
print(f"Optimal model: {response.raw['model']}")
print(response)
```

```
Optimal model: gpt-3.5-turbo
assistant: elektriksel olarak nötr olan ve çok küçük bir kütleye sahip olan bir atom altı parçacıktır. Evreni oluşturan temel parçacıklardan biridir. Nötrinoların tespiti son derece zordur çünkü maddeyle çok zayıf etkileşime girerler, bu da onların çoğu malzemenin içinden herhangi bir etkileşim olmadan geçebilmelerini sağlar. Güneş ve diğer yıldızlardaki nükleer reaksiyonlar gibi çeşitli doğal süreçlerin yanı sıra Dünya'daki parçacık etkileşimlerinde üretilirler. Nötrinolar, parçacık fiziği ve evren hakkındaki anlayışımızı geliştirmede önemli bir rol oynamıştır.
```

```python
message = ChatMessage(
    role="user",
    content="Statik olarak yazılmış (statically typed) ve dinamik olarak yazılmış (dynamically typed) diller arasındaki farkı açıklayın.",
)
resp = llm.chat([message])
print(f"Optimal model: {resp.raw['model']}")
print(resp)
```

```
Optimal model: mistralai/Mixtral-8x7B-Instruct-v0.1
assistant: Statik olarak yazılmış diller ve dinamik olarak yazılmış diller, değişken türlerini nasıl işlediklerine bağlı programlama dili kategorileridir.


Statik olarak yazılmış dillerde, bir değişkenin türü derleme zamanında (compile-time) belirlenir, bu da türün program çalıştırılmadan önce kontrol edildiği anlamına gelir. Bu, değişkenlerin her zaman tür açısından güvenli bir şekilde kullanılmasını sağlayarak birçok hata türünün çalışma zamanında oluşmasını engeller. Statik olarak yazılmış dillere örnek olarak Java, C, C++ ve C# verilebilir.


Dinamik olarak yazılmış dillerde, bir değişkenin türü çalışma zamanında (runtime) belirlenir, bu da türün program çalışırken kontrol edildiği anlamına gelir. Bu daha fazla esneklik sağlar, çünkü değişkenlere farklı zamanlarda farklı türden değerler atanabilir, ancak aynı zamanda tür hatalarının program çalışana kadar yakalanamayabileceği anlamına gelir ve bu da hata ayıklamayı zorlaştırabilir. Dinamik olarak yazılmış dillere örnek olarak Python, Ruby, JavaScript ve PHP verilebilir.


Statik ve dinamik diller arasındaki temel farklardan biri, statik dillerin değişkenler için açık tür bildirimleri gerektirerek daha ayrıntılı olma eğiliminde olmasıdır; dinamik diller ise daha özlüdür ve dolaylı tür bildirimlerine izin verir. Ancak bu aynı zamanda statik dillerin tür hatalarını daha erken yakalayabileceği anlamına gelir.
```

#### Akışlı Yanıtlar (Streaming Responses)

```python
message = ChatMessage(
    role="user", content="Meksika'nın yaklaşık nüfusu nedir?"
)
resp = llm.stream_chat([message])
for i, r in enumerate(resp):
    if i == 0:
        print(f"Optimal model: {r.raw['model']}")
    print(r.delta, end="")
```

```
Optimal model: anthropic.claude-instant-v1
assistant: En son BM tahminlerine göre, 2020 itibarıyla Meksika'nın nüfusu yaklaşık 128 milyondur. Meksika, dünyadaki en büyük 10. nüfusa sahiptir.
```
