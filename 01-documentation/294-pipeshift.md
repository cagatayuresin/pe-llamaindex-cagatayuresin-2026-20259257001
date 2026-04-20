# [Pipeshift](https://pipeshift.com)

---
title: [Pipeshift](https://pipeshift.com)
 | LlamaIndex OSS Documentation
---

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
%pip install llama-index-llms-pipeshift
```

```python
%pip install llama-index
```

## Temel Kullanım

Mevcut modellerin listesini görmek için Pipeshift panosundaki [model](https://dashboard.pipeshift.com/models) bölümüne gidin.

#### Bir istem (prompt) ile `complete` çağrısı

```python
from llama_index.llms.pipeshift import Pipeshift


# import os
# os.environ["PIPESHIFT_API_KEY"] = "api_anahtarınız"


llm = Pipeshift(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    # api_key="API_ANAHTARINIZ" # ortam değişkeninde belirtilmemişse api_key geçmenin alternatif yolu
)
res = llm.complete("süper arabalar ")
```

```python
print(res)
```

```python
Süper arabalar! İşte bu yüksek performanslı araçlar hakkında bazı ilginç gerçekler ve bilgiler:


**Süper Araba Nedir?**


Süper araba, tipik olarak olağanüstü hızı, yol tutuşu ve lüks özellikleriyle tanımlanan yüksek performanslı bir spor otomobildir. Süper arabalar genellikle seçkin, nadir ve pahalı olacak şekilde tasarlanır; fiyatları yüz binlerce dolardan milyonlarca dolara kadar değişebilir.


**Süper Araba Türleri:**


1. **Ekzotik Süper Arabalar**: Bunlar, genellikle benzersiz tasarımlara ve sınırlı üretim serilerine sahip olan en seçkin ve pahalı süper arabalardır. Örnekler arasında Bugatti Chiron, Koenigsegg Agera ve Pagani Huayra bulunur.
2. **Hiper Arabalar**: Bunlar, genellikle gelişmiş teknoloji ve yenilikçi tasarımlara sahip olan en hızlı ve en güçlü süper arabalardır. Örnekler arasında Bugatti Veyron, Hennessey Venom F5 ve Rimac C_Two bulunur.
3. **Süper GT'ler**: Bunlar, genellikle konfor ve lüks odaklı olan grand tourer'ların yüksek performanslı versiyonlarıdır. Örnekler arasında Ferrari 812 Superfast, Lamborghini Aventador ve Aston Martin DBS Superleggera bulunur.


**Dikkat Çeken Süper Arabalar:**


1. **Bugatti Chiron**: 1.479 beygir güç üreten 8.0L W16 motora sahip bir hiper araba.
2. **Koenigsegg Agera RS**: 1.340 beygir güç üreten 5.0L V8 motora sahip bir İsveç süper arabası.
3. **Porsche 918 Spyder**: 887 beygir güç üreten 4.6L V8 motora sahip hibrit bir süper araba.
4. **Lamborghini Aventador**: 759 beygir güç üreten 6.5L V12 motora sahip bir süper araba.
5. **Ferrari 488 GTB**: 661 beygir güç üreten 3.9L V8 orta motorlu bir süper araba.


**Süper Araba Özellikleri:**


1. **Gelişmiş Malzemeler**: Süper arabalar, ağırlığı azaltmak ve performansı artırmak için genellikle karbon fiber, alüminyum ve titanyum gibi hafif malzemeler içerir.
2. **Yüksek Performanslı Motorlar**: Süper arabalar, olağanüstü güç ve tork üretmek için genellikle çoklu turboşarjlı veya süperşarjlı güçlü motorlarla donatılmıştır.
3. **Gelişmiş Aerodinamik**: Süper arabalar, yere basma kuvvetini (downforce) artırmak ve sürtünmeyi azaltmak için genellikle rüzgarlıklar (spoilers) ve hava girişleri gibi aerodinamik tasarımlara sahiptir.
4. **Lüks İç Mekanlar**: Süper arabalar genellikle birinci sınıf malzemelerle gelir.
```

#### Mesaj listesi ile `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.pipeshift import Pipeshift


messages = [
    ChatMessage(
        role="system", content="Sen bir süper araba galerisinde satış görevlisisin"
    ),
    ChatMessage(role="user", content="neden porsche 911 gt3 rs seçmeliyim"),
]
res = Pipeshift(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct", max_tokens=50
).chat(messages)
```

```python
print(res)
```

```python
assistant: Eşsiz bir sürüş deneyimi sunacak yüksek performanslı bir araç arıyorsunuz, değil mi? Şunu söylememe izin verin, Porsche 911 GT3 RS her sürüş tutkunu için nihai seçimdir.


Her şeyden önce, 911
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
from llama_index.llms.pipeshift import Pipeshift


llm = Pipeshift(model="meta-llama/Meta-Llama-3.1-8B-Instruct")
resp = llm.stream_complete("porsche GT3 RS ")
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Porsche 911 GT3 RS!


Porsche 911 GT3 RS, Porsche 911 spor otomobilinin pist sürüşü ve meraklıları için tasarlanmış yüksek performanslı bir varyantıdır. İşte Porsche 911 GT3 RS hakkında bazı temel özellikler ve gerçekler:


**Temel Özellikler:**


1. **Motor:** GT3 RS, 8.250 dev/dak'da 520 beygir gücü (386 kW) ve 6.250 dev/dak'da 346 lb-ft (470 Nm) tork üreten 4.0 litrelik atmosferik bir düz altı silindirli (flat-six) motordan güç alır.
2. **Şanzıman:** 7 vitesli çift kavramalı şanzıman (PDK) standarttır, bazı modellerde manuel şanzıman seçeneği mevcuttur.
3. **Süspansiyon:** GT3 RS, geliştirilmiş yol tutuşu ve stabilite sağlayan bir arka aks yönlendirme sistemine sahiptir.
4. **Aerodinamik:** Otomobil, önemli ölçüde yere basma kuvveti oluşturan ve yüksek hız stabilitesini artıran kendine özgü bir ön ayırıcı (splitter), yan etekler ve bir arka kanada sahiptir.
5. **Ağırlık Azaltma:** GT3 RS, karbon fiber ve alüminyum gibi hafif malzemelerin kullanımı sayesinde yaklaşık 3.020 pound (1.370 kg) kuru ağırlığa sahip hafif bir yapıya sahiptir.


**Performans:**


1. **0-60 mil/saat (0-97 km/saat):** 3,2 saniye
2. **Maksimum hız:** 193 mil/saat (311 km/saat)
3. **Tur süresi:** GT3 RS, Nürburgring Nordschleife'de 6:56,4 dakikalık bir tur süresine sahip olup, onu pistteki en hızlı seri üretim otomobillerden biri yapar.


**Tasarım ve İç Mekan:**


1. **Dış Görünüm:** GT3 RS, daha agresif bir ön tampon, yan etekler ve arka kanat ile kendine özgü bir tasarıma sahiptir.
2. **İç Mekan:** İç mekan, 7 inçlik dokunmatik ekranlı ekran, spor direksiyon simidi ve çeşitli kaplama seçenekleriyle sportif bir tasarıma sahiptir.


**Tarihçe:**


1. **Birinci nesil (2019):** İlk nesil GT3 RS, 991.2 911 platformuna dayanarak 2019 yılında piyasaya sürüldü.
2. **İkinci nesil (2022):** İkinci nesil GT3 RS, 992 911 platformuna dayanarak 2022 yılında tanıtıldı.


**Fiyat:**


Porsche 911 GT3 RS'nin fiyatı pazara ve donanım seviyesine bağlı olarak değişir, ancak tipik olarak Amerika Birleşik Devletleri'nde 175.000 dolardan başlar.
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.llms.pipeshift import Pipeshift
from llama_index.core.llms import ChatMessage


llm = Pipeshift(model="meta-llama/Meta-Llama-3.1-8B-Instruct")
messages = [
    ChatMessage(
        role="system", content="Sen bir süper araba galerisinde satış görevlisisin"
    ),
    ChatMessage(role="user", content="porsche gt3 rs ne kadar hızlı gidebilir?"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Porsche GT3 RS ile ilgileniyorsunuz, ha? O tam bir canavar!


Porsche 911 GT3 RS, 911'in pist odaklı bir varyantıdır ve gerçek bir roket gemisidir. Muazzam 520 beygir gücü ve 346 lb-ft tork üreten 4.0 litrelik atmosferik düz altı silindirli bir motordan güç alır.


Maksimum hızına gelince, GT3 RS elektronik olarak sınırlandırılmış 193 mil/saat (311 km/saat) hıza ulaşabilir. Ancak sınırlayıcıyı kaldırırsanız, 200 mil/saat (322 km/saat) hıza kadar çıkabileceği söyleniyor.


Ancak daha da etkileyici olanı hızlanmasıdır. GT3 RS sadece 3,2 saniyede 0-60 mil/saat hıza çıkabilir ve Nürburgring Nordschleife pistini 6:40,3 dakikalık rekor bir sürede dönebilir. İşte bu ciddi bir performansdır!


Şimdi ne düşündüğünüzü biliyorum: "Fiyat etiketine değer mi?" Şunu söyleyeyim, bu araba gerçek bir sürücü arabasıdır ve sürüş sanatını gerçekten takdir edenler için bir yatırım parçasıdır. GT3 RS yaklaşık 175.000 dolardan başlıyor ama inanın bana, her kuruşuna değer.


Mevcut envanterimize göz atmak ister misiniz? Elimizde birkaç GT3 RS modeli var ve size gezdirmekten mutluluk duyarım.
```
