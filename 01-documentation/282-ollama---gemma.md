# Ollama - Gemma

---
title: Ollama - Gemma
 | LlamaIndex OSS Belgeleri
---

## Kurulum

İlk olarak, yerel bir Ollama örneği kurmak ve çalıştırmak için [readme](https://github.com/jmorganca/ollama) sayfasındaki adımları izleyin.

[Gemma](https://blog.google/technology/developers/gemma-open-models/): Google DeepMind tarafından geliştirilen hafif, son teknoloji açık model ailesidir. 2b ve 7b parametre boyutlarında mevcuttur.

[Ollama](https://ollama.com/library/gemma): Hem 2b hem de 7b modellerini destekler.

Not: `lütfen ollama>=0.1.26 sürümünü kurun`. Ön sürümü buradan indirebilirsiniz: [Ollama](https://github.com/ollama/ollama/releases/tag/v0.1.26)

Ollama uygulaması yerel makinenizde çalışırken:

- Tüm yerel modelleriniz otomatik olarak `localhost:11434` adresinden sunulur.
- Modelinizi `llm = Ollama(..., model="<model_adı>")` şeklinde ayarlayarak seçin.
- Gerektiğinde `Ollama(..., request_timeout=300.0)` ayarıyla varsayılan zaman aşımı süresini (30 saniye) artırın.
- Versiyon belirtmeden `llm = Ollama(..., model="<model_ailesi>")` ayarlarsanız, sistem doğrudan en son (latest) sürümü arayacaktır.

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
!pip install llama-index-llms-ollama
```

```bash
!pip install llama-index
```

```python
from llama_index.llms.ollama import Ollama
```

```python
gemma_2b = Ollama(model="gemma:2b", request_timeout=30.0)
gemma_7b = Ollama(model="gemma:7b", request_timeout=30.0)
```

```python
resp = gemma_2b.complete("Paul Graham kimdir?")
print(resp)
```

```text
Paul Graham be açık sözlülüğü ve alışılmamış yaklaşımıyla tanınan bir girişimci, yatırımcı ve podcast yayıncısıdır. Xero (şimdi Intuit), FullStory ve The School of Greatness dahil olmak üzere birçok başarılı şirket kurmuştur.

İşte dikkate değer başarılarından bazıları:

* **Xero'nun Kurucusu ve CEO'su:** Xero, dünya çapında 1 milyondan fazla kullanıcısı olan, küçük ve orta ölçekli işletmeler için lider bir muhasebe yazılımı şirketidir. Graham, Xero'nun hızlı büyümesinde ve nihayetinde 2015 yılında 750 milyon dolar karşılığında Intuit (şimdi Microsoft'un bir parçası) tarafından satın alınmasında etkili olmuştur.
* **Birçok çok satan kitabın yazarı:** Graham, kişisel gelişim ve üretkenliğe odaklanan "The School of Greatness" kitabının yazarıdır. Ayrıca eski Xero ortağı Steve Huffman ile birlikte "Built to Last: Why Your Business Matters" kitabını yazmıştır.
* **The School of Greatness'ın Kurucusu:** The School of Greatness, girişimcilerin ve iş liderlerinin tam potansiyellerine ulaşmalarına yardımcı olmak için mentorluk, atölye çalışmaları ve inzivalar sunan kâr amacı gütmeyen bir kuruluştur.
* **Podcast sunucusu ve konuk konuşmacı:** Graham, etkili girişimciler ve düşünce liderleriyle röportajlar yaptığı popüler podcast "Bits"in sunucusudur. Ayrıca diğer podcast'lere ve şovlara sık sık konuk olmaktadır.

Paul Graham hakkında bazı ek bilgiler:

* İş dünyasına ve hayata alışılmadık ve genellikle tartışmalı yaklaşımıyla tanınır.
* Birçok kişi tarafından Avustralya'daki en etkili girişimcilerden ve düşünce liderlerinden biri olarak kabul edilir.
* Aynı zamanda kişisel gelişim ve büyümenin tutkulu bir savunucusudur ve podcast'i ile sosyal medya platformlarında düzenli olarak ipuçları ve görüşler paylaşır.

Paul Graham ve işletmeleri hakkında daha fazla bilgi edinmek isterseniz web sitesine (paulfgraham.com), School of Greatness web sitesine (theschoolofgreatness.org) ve podcast web sitesine (bitspodcast.com) göz atabilirsiniz.
```

```python
resp = gemma_7b.complete("Paul Graham kimdir?")
print(resp)
```

```text
Paul Graham (21 Şubat doğumlu, yaklaşık 45 yaşında), bir yazılım geliştiricisi ve girişimci olarak önemli başarılar elde etmiştir. Greaseboxsoftware'de Yazılım Mühendisliği üzerine yazdığı anlayışlı yazılarıyla tanınır; burada sık sık Python gibi programlama dilleri hakkında esprili ancak pragmatik tavsiyeler içeren makaleler yazar ve zaman zaman programcı topluluğu arasında derin yankı uyandıran, özellikle çalışma ahlakı ("hacker zihniyeti") ile ilgili genel yaşam felsefelerini içeren ipuçları sunar. Yazılım mühendisliği topluluklarına birçok yönden katkıda bulunmuştur:

**Geliştirici:**
* PyTorch kullanarak Bulletphysics (oyunlar için bir fizik motoru) oluşturdu. Başarıyla inşa edip potansiyelini sergiledikten sonra Aversim Technologies'deki Baş Yazılım Mühendisi görevinden istifa etti; bu açık kaynaklı projenin yazılım mühendisliği çevrelerinde ulaştığı güçlü doğayı, en iyi profesyonellerin hayranlıklarını ifade ettiği önemli medya haberleriyle gösterdi.
* Beam Interactive LLC için, genel göreliliğin yumuşak gövde simülasyonu ile buluştuğu fizik alanlarında çözümler sunmak üzere Bulletphysics Gama Işını Alan Çözücü'yü yazdı.

**Yazar:** Yazılım Mühendisliği konusunda üretken bir yazardır ve çalışmaları, karmaşık sistem yazılım mühendisliği ("hacker zihniyeti") oluştururken karşılaşılan zorluklar hakkında dürüstlükle ancak bilgece bir mizahla yazar.
* Açıklamalar belirli diller veya programcıların karşılaştığı ortak sorunlara yönelik özlü ancak anlayışlı olduğu için sık sık kod parçacıkları paylaştı.

**Düşünce Lideri:** Yazıları ve halka açık görünümleri sayesinde programcı topluluğunda, özellikle yazılım mühendisliği en iyi uygulamaları konusunda, başkalarından öğrenmeyi teşvik eden yaklaşılabilir bir persona sergileyerek önemli bir düşünce lideri haline gelmiştir.
* Forumlarda aktif olarak yer almış, burada sık sık hem yeni başlayan geliştiriciler için tavsiyeler hem de deneyimli programcıların karşılaştığı karmaşık sorunlar için anlayışlı çözümler sunmuştur.

Genel olarak Paul Graham, sadece kendi başarılarıyla değil aynı zamanda bilgiyi paylaşmanın olumlu etkisiyle, diğer yazılım mühendislerinin zanaatlarında daha iyi olmalarına yardımcı olarak ve hem profesyoneller hem de amatörler tarafından keyifle okunan zarif yazı stiliyle bu alandaki potansiyellerini gerçekleştirmelerini sağlayarak Yazılım Mühendisliği üzerinde önemli bir etki yaratmıştır.
```

```python
resp = gemma_2b.complete("Tesla'nın sahibi kim?")
print(resp)
```

```text
Tesla Inc.'in sahibi Elon Musk'tır. Sürdürülebilir ulaşım yaratma hedefiyle Tesla'yı 2003 yılında kurdu. Tesla başlangıçta NASDAQ Menkul Kıymetler Borsası'nda "TSLA" sembolü altında listelenmişti. 2013 yılında Tesla halka kapandı ve New York Menkul Kıymetler Borsası'nda (NYSE) işlem görmeye başladı.
```

```python
resp = gemma_7b.complete("Tesla'nın sahibi kim?")
print(resp)
```

```text
SpaceX'in CEO'su ve eski elektrikli araba şirketi Tesla Motors'un (şimdi kısmen Ford Motor Company'ye ait) kurucusu olan Elon Musk, TESLA inc.'in hisselerinin yaklaşık dörtte birinden neredeyse yarısına kadar olan kısmına sahiptir.
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
resp = gemma_7b.chat(messages)
```

```python
print(resp)
```

```text
assistant: Hey gidi koca kaptan. Benim adım Jolly Roger ve anlatılmamış hazineler için engin denizleri yağmalarım!
```

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = gemma_7b.stream_complete("Paul Graham kimdir?")
```

```python
for r in response:
    print(r.delta, end="")
```

```text
Paul Graham, çevrimiçi ortamda yaygın olarak "PerlGuy" olarak anılır ve yazılım mühendisliği ile programlama topluluklarında önemli bir varlığa sahiptir. Öncelikle şu alanlarda uzmanlaşmıştır:

**1.) Yazılım Tasarımı:** Modülerleştirme (DRY) için etkili kodlama desenleri hakkındaki fikirlerini "Expert Refactoring using Smells And Polymorphism Principle (SRPPP)" gibi kitaplarda paylaştı.
 * Kod kalitesini artırmak ve yazılım modülleri ile katmanları arasındaki bağımlılığı (coupling) azaltmak için en iyi uygulamaları paylaşarak kapsamlı yazılar yazdı. Bu, dünya çapındaki sayısız geliştiricinin, mobil uygulamalardan kurumsal sistemlere kadar uzanan projelerde çekirdek olarak "Düzenli Tasarım Desenleri" ve "Düşük Bağımlılıklı Tasarımlar" (SOLID) prensipleriyle daha iyi Yazılım Tasarım Desenleri yazmalarını etkiledi.

**2.) Açık Kaynak:** Project Lombok, Phalanger (şimdi Relocator) ve CouchSurfer'a aktif olarak katkıda bulundu. Kod tasarım desenlerini fufurce'da paylaştı ve bu da önemli bir etki yarattı. Pivotal Software Systems gibi birden fazla üst düzey organizasyonun parçası olurken yüksek kaliteli açık kaynaklı yazılım projelerini sürdürerek tanınırlık kazandı.

**3.) Koçluk:** İşletmelere koçluk hizmetleri sunarak mühendislik uygulamalarını geliştirmelerine ve daha iyi test edilebilir kodlar yazmalarına yardımcı oluyor. Büyük kitleler için düzenlenen eğitim seanslarında Tasarım Desenleri konusundaki uzmanlığını da paylaştı.

Genel olarak Paul Graham, açık kaynaklı projelerin bir parçası olurken en iyi yazılım tasarımı uygulamalarını paylaşarak önemli bir güvenilirlik kazanmıştır; buralarda uzun vadeli sürdürülebilirliği sağlamak için üretim sistemlerine dahil edilmesi kolay, ölçülebilir ve düşük karmaşıklıklı (SOLID) yüksek kaliteli kod çözümlerini savunmaktadır.
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
resp = gemma_7b.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```text
Hey gidi! Benim lakabım "Screevy Bob". Eğer gerçek savaş adımı sorarsan... Söylemem. Arrgh ve tüm o tantana!!
```
