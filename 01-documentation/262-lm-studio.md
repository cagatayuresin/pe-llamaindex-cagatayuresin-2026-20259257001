# LM Studio

---
title: LM Studio
 | LlamaIndex OSS Belgeleri
---

## Kurulum

1. LM Studio'yu indirin ve kurun.
2. [README](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/llms/llama-index-llms-lmstudio/README.md) dosyasında belirtilen adımları izleyin.

Colab'da henüz yüklü değilse, *llama-index* ve *lmstudio* entegrasyonunu kurun.

```bash
%pip install llama-index-core llama-index llama-index-llms-lmstudio
```

“RuntimeError: This event loop is already running” hatası için çözüm:

```python
import nest_asyncio


nest_asyncio.apply()
```

```python
from llama_index.llms.lmstudio import LMStudio
from llama_index.core.base.llms.types import ChatMessage, MessageRole
```

```python
llm = LMStudio(
    model_name="Hermes-2-Pro-Llama-3-8B",
    base_url="http://localhost:1234/v1",
    temperature=0.7,
)
```

```python
response = llm.complete("Selam, 2+2 kaç eder?")
print(str(response))
```

```
2 + 2'nin sonucu 4'tür.
```

```python
# llm.stream_complete kullanım örneği
response = llm.stream_complete("7+3 kaç eder?")
for r in response:
    print(r.delta, end="")
```

```
7 + 3'ün sonucu 10'dur.
```

```python
messages = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="Sen uzman bir yapay zeka asistanısın. Kullanıcıya sorularında yardımcı ol.",
    ),
    ChatMessage(
        role=MessageRole.USER,
        content="42 sayısının önemi nedir?",
    ),
]
```

```python
response = llm.chat(messages=messages)
print(str(response))
```

```
assistant: 42 sayısı, tarih boyunca ve farklı kültürlerde çeşitli bağlamlarda önemli olmuş, genellikle sembolik veya felsefi anlamlar taşımıştır.


1. Matematikte: 42, 1 ve kendisinden başka böleni olmayan (Not: Aslında bol bölenli bir sayıdır) ama yine de ilginç olan, nispeten basit bir tam sayıdır.


2. Popüler kültürde: Douglas Adams'ın bilim kurgu serisi "Otostopçunun Galaksi Rehberi"nde hayatın anlamı için nihai cevap 42 olarak sunulur; bu, 1979'da yayınlanan ilk kitaptan bu yana iyi bilinen bir şaka ve internet akımı (meme) haline gelmiştir.


3. Din ve mitolojide: 42 sayısı, çeşitli dini metinlerde veya mitlerde farklı anlamlarla yer alır; örneğin İncil'deki Sayılar Kitabı'nda Musa'nın Tanrı'dan çağrıyı almadan önce kayınpederinin sürüsüne bakarak 42 yıl geçirmesi veya İskandinav mitolojisinde Odin'in bilgi edinmek için Yggdrasil'de (Dünya Ağacı) asılı kalarak 42 gece geçirmesi gibi.


4. Sporda: Beyzbolda, vuruş (hit), hata (error) veya koşucunun kaleye ulaşmasına izin verilmeyen bir oyun "kusursuz oyun" (perfect game) olarak kabul edilir; Major League Baseball tarihinde bunu sadece 15 oyuncu başarabilmiştir ve isimlerinin toplam sayısı 42'ye eşittir (6 + 2 = 8, 3 + 4 = 7 - Not: Bu AI halüsinasyonu olabilir).


5. Müzikte: İngiliz rock grubu Coldplay'in popüler şarkısı "42", grubun başarıya ulaşması için geçen süre boyunca solist Chris Martin'in yaşı üzerine düşünmesini konu alır.


42 sayısının önemi bağlam ve kültürel arka plana göre değişir. Sık sık sembolik veya mecazi olarak kullanılmış, bu da onu insan yaşamının çeşitli yönlerinde çok yönlü ve ilgi çekici bir sayı haline getirmiştir.
```

```python
response = llm.stream_chat(messages=messages)
for r in response:
    print(r.delta, end="")
```

```
42 sayısının farklı bağlamlarda çeşitli önemleri vardır:


1. Popüler kültürde: Douglas Adams'ın bilim kurgu serisi "Otostopçunun Galaksi Rehberi"ndeki ünlü "Hayata, Evrene ve Her Şeye Dair Nihai Sorunun Cevabı" 42'dir. Bu durum, sayının anlamlı veya derin bir şey olarak yaygın şekilde tanınmasına yol açmıştır.


2. Matematik: 42 sayısı, birçok böleni (1, 2, 3, 6, 7, 14, 21 ve 42) olan yüksek kompozit bir sayıdır. Matematikte çarpanlar ve bölenler üzerine yapılan çalışmalar, asal çarpanlara ayırma ve en büyük ortak bölen gibi çeşitli kavramlarda temel bir rol oynar.


3. Hristiyanlık: Kells Kitabı'ndan (tezhip edilmiş bir el yazması) bir hikayeye göre, Aziz Patrick'in İrlanda'yı Hristiyanlığa döndürme misyonuna ne zaman başlayacağını hesaplamak için 42 sayısını kullandığı söylenir.


4. Astrolojide: Bazı geleneklerde, kış gündönümünden sonraki 42. gün, yeni astrolojik yılın başlangıcını ve 13 aylık bir döngünün başlangıcını işaret eder.


5. Edebiyat: 42 sayısı, William Shakespeare'in "Hamlet" ve "IV. Henry" gibi oyunları boyunca birkaç kez geçmektedir. Bu eserlerde bir tesadüf olarak veya muhtemelen sembolik bir niyetle yer alır.


6. Bilgisayar bilimi alanında, popüler programlama dili 'Python', yorumlayıcının başlangıç kodunu temsil etmek için "sihirli sayı" (magic number) olarak 42'yi kullanır.


Her bağlam 42 sayısına farklı bir önem atfeder, bu da onu çeşitli şekillerde çok yönlü ve kültürel olarak ilgili kılar.
```
