# Replicate - Vicuna 13B

---
title: Replicate - Vicuna 13B
 | LlamaIndex OSS Documentation
---

## Kurulum

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-replicate
```

```python
!pip install llama-index
```

`REPLICATE_API_TOKEN` ortam değişkeninin ayarlandığından emin olun.\
Eğer henüz bir hesabınız yoksa, bir anahtar almak için <https://replicate.com/> adresine gidin.

```python
import os
```

```python
os.environ["REPLICATE_API_TOKEN"] = "<API anahtarınız>"
```

## Temel Kullanım

Doğrudan şu adresten deneyebileceğiniz "vicuna-13b" modelini gösteriyoruz: <https://replicate.com/replicate/vicuna-13b>

```python
from llama_index.llms.replicate import Replicate


llm = Replicate(
    model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b"
)
```

#### Bir istem (prompt) ile `complete` fonksiyonunu çağırın

```python
resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

```text
Paul Graham İngiliz bir fizikçi, matematikçi ve bilgisayar bilimcisidir. En çok kuantum mekaniğinin temelleri üzerine yaptığı çalışmalar ve kuantum bilişim alanının gelişimine yaptığı katkılarla tanınır.


Graham 15 Ağustos 1957'de Cambridge, İngiltere'de doğdu. Lisans derecesini 1979'da Cambridge Üniversitesi'nden matematik alanında aldı ve daha sonra 1984'te Kaliforniya Üniversitesi, Berkeley'den teorik fizik alanında doktora derecesini kazandı.


Kariyeri boyunca Graham, kuantum mekaniği alanına önemli katkılarda bulunmuştur. Konuyla ilgili "Yarı fiyatına kuantum mekaniği", "Kuantum mekaniğinin holonomisi" ve "Sınırlı öz-eş operatörlerin varlığında kuantum mekaniği" gibi bir dizi etkili makale yayınlamıştır.


Graham ayrıca kuantum bilişimin geliştirilmesinde kilit bir figür olmuştur. Kuantum bilişim şirketi QxBranch'in kurucu ortağıdır ve pratik kuantum algoritmaları geliştirme ve büyük ölçekli kuantum bilgisayarlar inşa etme çabalarında lider bir rol oynamıştır.


Buna ek olarak...
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
asistan: ​
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
Paul Graham İngiliz bir filozof, bilişsel bilimci ve girişimcidir. En çok zihin felsefesi ve bilinç üzerine yaptığı çalışmaların yanı sıra Yapay Zeka (AI) alanının gelişimine yaptığı katkılarla tanınır.


Graham 1938'de Londra'da doğdu ve felsefe ve doğa bilimleri okuduğu Cambridge Üniversitesi'nde eğitim gördü. Eğitimini tamamladıktan sonra Oxford Üniversitesi ve Kaliforniya Üniversitesi, Berkeley dahil olmak üzere birçok prestijli üniversitede akademik görevlerde bulundu.


Kariyeri boyunca Graham; zihin felsefesi, bilinç, AI ve bilim ile din arasındaki ilişki gibi geniş bir yelpazedeki konularda çok sayıda makale ve kitap yayınlayan üretken bir yazar ve düşünür olmuştur. Ayrıca Viaweb (daha sonra Yahoo! tarafından satın alındı) ve Palantir Technologies dahil olmak üzere birkaç başarılı teknoloji girişiminin geliştirilmesinde yer almıştır.


Pek çok başarısına rağmen Graham, belki de en çok zihin felsefesi ve bilinç konusundaki katkılarıyla tanınır. Özellikle... kavramı üzerindeki çalışmaları...
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
​
```

## Modeli Yapılandırma

```python
from llama_index.llms.replicate import Replicate


llm = Replicate(
    model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
    temperature=0.9,
    max_tokens=32,
)
```

```python
resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

```text
Paul Graham, etkili bir bilgisayar bilimcisi, risk sermayedar ve deneme yazarıdır. En çok ... olarak tanınır.
```
