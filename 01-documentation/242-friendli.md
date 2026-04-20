# Friendli

## Temel Kullanım

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-friendli
```

```python
!pip install llama-index
```

```python
%env FRIENDLI_TOKEN=...
```

    env: FRIENDLI_TOKEN=...

```python
from llama_index.llms.friendli import Friendli

# Friendli belirtecinizi (token) özelleştirmek için bunu yapın
# aksi takdirde ortam değişkeninizden FRIENDLI_TOKEN'ı arayacaktır
# llm = Friendli(friendli_token="Kişisel erişim belirteciniz")

llm = Friendli()
```

### Bir mesaj listesiyle `chat` çağrısı yapın

```python
from llama_index.core.llms import ChatMessage, MessageRole

message = ChatMessage(role=MessageRole.USER, content="Bana bir şaka anlat.")
resp = llm.chat([message])

print(resp)
```

    assistant: Tabii ki, seninle bir şaka paylaşmaktan mutluluk duyarım! İşte burada:
    
    Bilim insanları neden atomlara güvenmezler?
    
    Çünkü her şeyi onlar uyduruyorlar!
    
    Umarım bu yüzünde bir gülümseme oluşturmuştur. Başka bir şaka duymak ister misin, yoksa konuşmak istediğin başka bir şey var mı?

#### Akış (Streaming)

```python
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

    Tabii ki, seninle bir şaka paylaşmaktan mutluluk duyarım! İşte burada:
    
    Bilim insanları neden atomlara güvenmezler?
    
    Çünkü her şeyi onlar uyduruyorlar!
    
    Umarım bu yüzünde bir gülümseme oluşturmuştur. Başka bir şaka duymak ister misin, yoksa konuşmak istediğin başka bir şey var mı?

#### Asenkron (Async)

```python
resp = await llm.achat([message])

print(resp)
```

    assistant: Elbette, işte bir tane:
    
    Bilim insanları neden atomlara güvenmezler?
    
    Çünkü her şeyi onlar uyduruyorlar!

#### Asenkron Akış (Async Streaming)

```python
resp = await llm.astream_chat([message])
async for r in resp:
    print(r.delta, end="")
```

    Elbette, işte bir tane:
    
    Bilim insanları neden atomlara güvenmezler?
    
    Çünkü her şeyi onlar uyduruyorlar!

### Bir istemle (prompt) `complete` çağrısı yapın

```python
prompt = "Yazılım mühendisliği rolü için bir ön yazı taslağı hazırla."
resp = llm.complete(prompt)

print(resp)
```

    
    Sayın İşe Alım Yöneticisi,
    
    XYZ Şirketi'ndeki Yazılım Mühendisi pozisyonuna olan ilgimi ifade etmek için yazıyorum. Alanında beş yılı aşkın deneyime sahip, son derece yetenekli ve motivasyonu yüksek bir yazılım mühendisi olarak, ekibinize değerli bir katkıda bulunmak için gerekli beceri ve uzmanlığa sahip olduğumdan eminim.
    
    Kariyerim boyunca karmaşık yazılım sistemlerinin tasarlanması, geliştirilmesi ve bakımı konusunda kapsamlı deneyim kazandım. Java, Python ve C++ gibi programlama dillerinde güçlü bir geçmişe sahibim ve çeşitli yazılım geliştirme araçlarını ve çerçevelerini kullanma konusunda yetkinim. Ayrıca çevik (agile) metodolojilerle çalışma konusunda deneyimliyim ve yüksek kaliteli yazılımı zamanında ve bütçe dahilinde teslim etme konusunda kanıtlanmış bir geçmişe sahibim.
    
    ABC Şirketi'ndeki mevcut görevimde, 10.000'den fazla kullanıcı tarafından kullanılan kritik bir uygulamanın geliştirilmesinde bir yazılım mühendisleri ekibine liderlik etmekten sorumlu oldum. Gereksinim toplamadan dağıtıma kadar tüm yazılım geliştirme yaşam döngüsünü başarıyla yönettim ve uygulamanın yoğun kullanım zamanlarında bile sorunsuz çalışmasını sağlamak için çeşitli performans optimizasyon teknikleri uyguladım.
    
    Yazılım mühendisliği endüstrisinde bir lider olarak sahip olduğu itibar nedeniyle özellikle XYZ Şirketi'ne ilgi duyuyorum.

#### Akış (Streaming)

```python
resp = llm.stream_complete(prompt)
for r in resp:
    print(r.delta, end="")
```

    
    Sayın İşe Alım Yöneticisi,
    
    XYZ Şirketi'ndeki Yazılım Mühendisi pozisyonuna olan ilgimi ifade etmek için yazıyorum. Bilgisayar Bilimleri alanındaki lisans derecem ve yazılım geliştirme konusundaki beş yılı aşkın deneyimimle, ekibinize değerli bir katkıda bulunma yeteneğime güveniyorum.
    
    Kariyerim boyunca Java, Python ve C++ gibi çeşitli programlama dillerinde deneyim kazandım. Ayrıca hem ön uç (front-end) hem de arka uç (back-end) geliştirmeden sorumlu olduğum tam kapsamlı (full-stack) geliştirme projelerinde çalıştım. Deneyimim; yazılım çözümleri tasarlamayı ve uygulamayı, çapraz fonksiyonel ekiplerle iş birliği yapmayı ve kod incelemeleri gerçekleştirmeyi içeriyor.
    
    Özellikle XYZ Şirketi'nin inovasyon ve en son teknolojiye odaklanmasıyla ilgileniyorum. Yaratıcılığa ve sürekli öğrenmeye değer veren bir ekiple çalışma fırsatı beni heyecanlandırıyor. Becerilerimin ve deneyimimin beni bu rol için güçlü bir aday yaptığına eminim.
    
    Başvurumu değerlendirdiğiniz için teşekkür ederim. Niteliklerimi daha detaylı tartışmak için sabırsızlanıyorum.
    
    Saygılarımla,
    
    [Adınız]

#### Asenkron (Async)

```python
resp = await llm.acomplete(prompt)

print(resp)
```

    
    Sayın İşe Alım Yöneticisi,
    
    XYZ Şirketi'ndeki Yazılım Mühendisi pozisyonuna olan ilgimi ifade etmek için yazıyorum. Bilgisayar Bilimleri alanındaki lisans derecem ve yazılım geliştirme konusundaki beş yılı aşkın deneyimimle, ekibinize değerli bir katkıda bulunma yeteneğime güveniyorum.
    
    Kariyerim boyunca Java, Python ve C++ gibi çeşitli programlama dillerinde deneyim kazandım. Ayrıca hem ön uç hem de arka uç geliştirmeden sorumlu olduğum tam kapsamlı geliştirme projelerinde çalıştım. Deneyimim; bulut tabanlı uygulamalar üzerinde çalışmayı, API'ler geliştirmeyi ve üçüncü taraf hizmetlerini entegre etmeyi içeriyor.
    
    Temiz, verimli ve sürdürülebilir kod yazma konusunda tutkuluyum. Ayrıca Çevik (Agile) metodolojilere güçlü bir şekilde inanıyorum ve Çevik ekiplerde çalışma deneyimim var. Bir ekip oyuncusuyum ve karmaşık sorunlara çözüm bulmak için başkalarıyla iş birliği yapmaktan keyif alıyorum.
    
    ABC Şirketi'ndeki mevcut görevimde, bulut tabanlı bir uygulamanın geliştirilmesinde bir yazılım mühendisleri ekibine liderlik etmekten sorumlu oldum. Ayrıca, ekibin üretkenliğini ve verimliliğini artırmaya yardımcı olan şirketin DevOps uygulamalarının tasarımı ve uygulanmasında yer aldım.

#### Asenkron Akış (Async Streaming)

```python
resp = await llm.astream_complete(prompt)
async for r in resp:
    print(r.delta, end="")
```

    
    Sayın İşe Alım Yöneticisi,
    
    XYZ Şirketi'ndeki Yazılım Mühendisi pozisyonuna olan ilgimi ifade etmek için yazıyorum. Bilgisayar Bilimleri alanındaki lisans derecem ve yazılım geliştirme konusundaki beş yılı aşkın deneyimimle, ekibinize değerli bir katkıda bulunma yeteneğime güveniyorum.
    
    Kariyerim boyunca Java, Python ve C++ gibi çeşitli programlama dillerinde kapsamlı deneyim kazandım. Ayrıca React ve Angular gibi çerçeveleri (frameworks) kullanarak web uygulamaları geliştirme üzerinde çalıştım. Deneyimim; hem ön uç hem de arka uç geliştirme üzerinde çalışmanın yanı sıra, yüksek kaliteli yazılım ürünleri sunmak için ekiplere liderlik etmeyi içeriyor.
    
    Mevcut görevimde, çeşitli endüstrilerdeki müşteriler için yazılım çözümleri tasarlamak ve uygulamaktan sorumlu oldum. Final ürünün müşterinin gereksinimlerini karşıladığından emin olmak için ürün yöneticileri, tasarımcılar ve kalite güvence mühendisleri dahil olmak üzere çapraz fonksiyonel ekiplerle yakın bir şekilde çalıştım. Ayrıca, gereksinim toplamadan dağıtıma kadar tüm yazılım geliştirme yaşam döngüsünde yer aldım.
    
    XYZ Şirketi'nin inovasyon ve mükemmellik konusundaki itibarı nedeniyle bu şirketteki Yazılım Mühendisi rolüyle özellikle ilgileniyorum. Yetenekli bir ekiple çalışma fırsatı beni heyecanlandırıyor.

## Modeli Yapılandırın

```python
from llama_index.llms.friendli import Friendli

llm = Friendli(model="llama-2-70b-chat")
```

```python
resp = llm.chat([message])

print(resp)
```

    assistant: Elbette, işte senin için bir şaka:
    
    Bisiklet neden kendi başına ayakta duramıyormuş?
    
    Çünkü iki tekerleği (too-tired/yorgun) varmış! (Because it was two-tired!)
    
    Umarım bu yüzünde bir gülümseme oluşturmuştur! Başka soruların veya tartışmak istediğin konular varsa, yardım etmek için buradayım.
