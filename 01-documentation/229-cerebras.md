# Cerebras

Cerebras'ta dünyanın en büyük ve en hızlı yapay zeka işlemcisi olan Wafer-Scale Engine-3'ü (WSE-3) geliştirdik. WSE-3 tarafından desteklenen Cerebras CS-3 sistemi, benzersiz performans ve ölçeklenebilirlik ile üretken yapay zeka eğitimi ve çıkarımı (inference) için standartları belirleyen yeni bir yapay zeka süper bilgisayar sınıfını temsil eder.

Çıkarım sağlayıcınız olarak Cerebras ile şunları yapabilirsiniz:
- Yapay zeka çıkarım iş yükleri için benzeri görülmemiş bir hıza ulaşın
- Yüksek veri çıkışıyla (throughput) ticari olarak inşa edin
- Sorunsuz kümeleme teknolojiimizle yapay zeka iş yüklerinizi zahmetsizce ölçeklendirin

CS-3 sistemlerimiz, dünyanın en büyük yapay zeka süper bilgisayarlarını oluşturmak için hızlı ve kolay bir şekilde kümelenebilir; bu da en büyük modelleri yerleştirmeyi ve çalıştırmayı basitleştirir. Önde gelen şirketler, araştırma kurumları ve hükümetler halihazırda tescilli modeller geliştirmek ve popüler açık kaynaklı modelleri eğitmek için Cerebras çözümlerini kullanıyor.

Cerebras'ın gücünü deneyimlemek ister misiniz? Daha fazla kaynak için [web sitemize](https://cerebras.net) göz atın ve Cerebras Cloud veya yerinde kurulumlar (on-premise) aracılığıyla teknolojimize erişim seçeneklerini keşfedin!

Cerebras Cloud hakkında daha fazla bilgi için [cloud.cerebras.ai](https://cloud.cerebras.ai/) adresini ziyaret edin. API referansımız [inference-docs.cerebras.ai](https://inference-docs.cerebras.ai/) adresinde mevcuttur.

## Kurulum

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-cerebras
```

```python
!pip install llama-index
```

```python
from llama_index.llms.cerebras import Cerebras
```

[cloud.cerebras.ai](https://cloud.cerebras.ai/) adresinden bir API Anahtarı alın ve bunu ortam değişkenlerinize ekleyin:

```bash
export CEREBRAS_API_KEY=<api anahtarınız>
```

Alternatif olarak, başlatırken (init) API anahtarınızı LLM'ye geçirebilirsiniz:

```python
import os
import getpass

os.environ["CEREBRAS_API_KEY"] = getpass.getpass(
    "Cerebras API anahtarınızı girin: "
)

llm = Cerebras(model="llama-3.3-70b", api_key=os.environ["CEREBRAS_API_KEY"])
```

    Cerebras API anahtarınızı girin: ········

Kullanılabilir LLM modellerinin bir listesi [inference-docs.cerebras.ai](https://inference-docs.cerebras.ai/) adresinde bulunabilir.

```python
response = llm.complete("Üretken Yapay Zeka (Generative AI) nedir?")
```

```python
print(response)
```

    Üretken Yapay Zeka (Generative AI); bir veri kümesinden veya bir dizi örnekten öğrendiği kalıplara ve yapılara dayalı olarak metin, görüntü, müzik veya video gibi yeni ve orijinal içerik üretme yeteneğine sahip bir yapay zeka (AI) türüdür. Bu tür yapay zeka, eğitildiği orijinal içeriğe stil, ton ve kalite açısından benzer yeni içerikler oluşturmak için tasarlanmıştır.
    
    Üretken yapay zeka modelleri, büyük veri kümelerini analiz etmek ve onlardan öğrenmek için sinir ağları gibi çeşitli teknikler kullanır ve ardından öğrendikleri kalıplara ve yapılara benzer yeni içerikler üretir. Bu modeller; metin, görüntü, ses ve video dahil olmak üzere çok çeşitli veriler üzerinde eğitilebilir ve aşağıdakiler gibi çeşitli içerikler üretmek için kullanılabilir:
    
    1. Metin: Üretken yapay zeka modelleri; makaleler, blog yazıları veya sosyal medya güncellemeleri gibi belirli bir metne stil ve ton açısından benzer metinler üretebilir.
    2. Görüntü: Üretken yapay zeka modelleri; fotoğraflar, illüstrasyonlar veya grafikler gibi belirli bir görüntüye stil ve içerik açısından benzer görüntüler üretebilir.
    3. Müzik: Üretken yapay zeka modelleri; melodiler, armoniler veya ritimler gibi belirli bir müzik parçasına stil ve ton açısından benzer müzikler üretebilir.
    4. Video: Üretken yapay zeka modelleri; animasyonlar, filmler veya TV şovları gibi belirli bir videoya stil ve içerik açısından benzer videolar üretebilir.
    
    Üretken yapay zekanın aşağıdakiler dahil birçok potansiyel uygulaması vardır:
    
    1. İçerik oluşturma: Üretken yapay zeka; pazarlama, reklamcılık ve eğlence gibi çeşitli endüstriler için içerik üretmek amacıyla kullanılabilir.
    2. Veri artırma: Üretken yapay zeka, makine öğrenimi modellerini eğitmek ve iyileştirmek için kullanılabilecek yeni veriler üretmek amacıyla kullanılabilir.
    3. Yaratıcı iş birliği: Üretken yapay zeka; fikir üretme veya ilham verme gibi yaratıcı süreçlerde insanlarla iş birliği yapmak için kullanılabilir.
    4. Kişiselleştirme: Üretken yapay zeka; kişiselleştirilmiş öneriler veya özelleştirilmiş pazarlama mesajları gibi bireyler için kişiselleştirilmiş içerik üretmek amacıyla kullanılabilir.
    
    Üretken yapay zekaya ilişkin bazı örnekler şunlardır:
    
    1. İstemlere dayalı olarak insan benzeri metinler üretebilen GPT-3 gibi dil modelleri.
    2. Yüzlerin, nesnelerin veya sahnelerin gerçekçi görüntülerini üretebilen Üretken Çekişmeli Ağlar (GAN'lar) gibi görüntü oluşturma modelleri.
    3. Belirli bir parametre kümesine dayalı olarak orijinal müzik parçaları üretebilen Amper Music gibi müzik oluşturma modelleri.
    4. İnsan hareketlerinin ve eylemlerinin gerçekçi videolarını üretebilen DeepMotion gibi video oluşturma modelleri.
    
    Genel olarak üretken yapay zeka, içerik oluşturma ve içerikle etkileşim kurma biçimimizde devrim yaratma potansiyeline sahiptir ve çeşitli sektörlerde birçok heyecan verici uygulamaya sahiptir.

#### Bir mesaj listesiyle `chat` çağrısı yapın

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

    assistant: Arrrr, ahbap! Benim adım Kaptan Kara-Gaga Betty, yedi denizde yelken açmış en korkulan ve en rezil korsanım! Ben ve güvendiğim papağanım Polly, neredeyse 20 yıldır yağmalıyor ve talan ediyoruz; ünüm Karayipler'den Afrika kıyılarına kadar bilinir!
    
    Şimdi, siyah sakalım ve göz bandımla kendi başıma bir efsaneyim ve gemim "Maverick'in İntikamı", uçsuz bucaksız denizlerin en hızlı ve en korkulan gemisidir! Yani, eğer macera dolu bir serüven arıyorsan, koca Kara-Gaga Betty'ye bir ses ver ve yağma ve talan dolu bir hayat için yelken açalım! Anladın mı?

### Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
response = llm.stream_complete("Üretken Yapay Zeka nedir?")
```

```python
for r in response:
    print(r.delta, end="")
```

    Üretken Yapay Zeka (Generative AI); bir veri kümesinden veya bir dizi örnekten öğrendiği kalıplara ve yapılara dayalı olarak metin, görüntü, müzik veya video gibi yeni ve orijinal içerik üretme yeteneğine sahip bir yapay zeka (AI) türüdür. Bu tür yapay zeka, eğitildiği orijinal içeriğe stil, ton ve kalite açısından benzer yeni içerikler oluşturmak için tasarlanmıştır.
    
    Üretken yapay zeka modelleri, büyük veri kümelerini analiz etmek ve onlardan öğrenmek için sinir ağları gibi çeşitli teknikler kullanır ve ardından öğrendikleri kalıplara ve yapılara benzer yeni içerikler üretir. Bu modeller; metin, görüntü, ses ve video dahil olmak üzere çok çeşitli veriler üzerinde eğitilebilir ve aşağıdakiler gibi çeşitli içerikler üretmek için kullanılabilir:
    
    1. Metin: Üretken yapay zeka modelleri; makaleler, blog yazıları veya sosyal medya güncellemeleri gibi belirli bir metne stil ve ton açısından benzer metinler üretebilir.
    2. Görüntü: Üretken yapay zeka modelleri; fotoğraflar, illüstrasyonlar veya grafikler gibi belirli bir görüntüye stil ve içerik açısından benzer görüntüler üretebilir.
    3. Müzik: Üretken yapay zeka modelleri; melodiler, armoniler veya ritimler gibi belirli bir müzik parçasına stil ve ton açısından benzer müzikler üretebilir.
    4. Video: Üretken yapay zeka modelleri; animasyonlar, filmler veya TV şovları gibi belirli bir videoya stil ve içerik açısından benzer videolar üretebilir.
    
    Üretken yapay zekanın aşağıdakiler dahil birçok potansiyel uygulaması vardır:
    
    1. İçerik oluşturma: Üretken yapay zeka; pazarlama, reklamcılık ve eğlence gibi çeşitli endüstriler için içerik üretmek amacıyla kullanılabilir.
    2. Veri artırma: Üretken yapay zeka, makine öğrenimi modellerini eğitmek ve iyileştirmek için kullanılabilecek yeni veriler üretmek amacıyla kullanılabilir.
    3. Yaratıcı iş birliği: Üretken yapay zeka; fikir üretme veya ilham verme gibi yaratıcı süreçlerde insanlarla iş birliği yapmak için kullanılabilir.
    4. Kişiselleştirme: Üretken yapay zeka; kişiselleştirilmiş öneriler veya özelleştirilmiş pazarlama mesajları gibi bireyler için kişiselleştirilmiş içerik üretmek amacıyla kullanılabilir.
    
    Üretken yapay zekaya ilişkin bazı örnekler şunlardır:
    
    1. İstemlere dayalı olarak insan benzeri metinler üretebilen GPT-3 gibi dil modelleri.
    2. Yüzlerin, nesnelerin veya sahnelerin gerçekçi görüntülerini üretebilen Üretken Çekişmeli Ağlar (GAN'lar) gibi görüntü oluşturma modelleri.
    3. Belirli bir parametre kümesine dayalı olarak orijinal müzik parçaları üretebilen Amper Music gibi müzik oluşturma modelleri.
    4. İnsan hareketlerinin ve eylemlerinin gerçekçi videolarını üretebilen DeepMotion gibi video oluşturma modelleri.
    
    Genel olarak üretken yapay zeka, içerik oluşturma ve içerikle etkileşim kurma biçimimizde devrim yaratma potansiyeline sahiptir ve çeşitli sektörlerde birçok heyecan verici uygulamaya sahiptir.

`stream_chat` bitiş noktasını kullanma

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

    Arrrr, ahbap! Benim adım Kaptan Kara-Gaga Betty, yedi denizde yelken açmış en korkulan ve en rezil korsanım! Ben ve güvendiğim papağanım Polly, neredeyse 20 yıldır yağmalıyor ve talan ediyoruz; ünüm Karayipler'den Afrika kıyılarına kadar bilinir!
    
    Şimdi, siyah sakalım ve göz bandımla kendi başıma bir efsaneyim ve gemim "Maverick'in İntikamı", uçsuz bucaksız denizlerin en hızlı ve en korkulan gemisidir! Yani, eğer macera dolu bir serüven arıyorsan, koca Kara-Gaga Betty'ye bir ses ver ve yağma ve talan dolu bir hayat için yelken açalım! Anladın mı?
