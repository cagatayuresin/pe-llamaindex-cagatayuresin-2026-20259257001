# LLM Predictor

---
title: LLM Predictor
 | LlamaIndex OSS Belgeleri
---

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-openai
%pip install llama-index-llms-langchain
```

```bash
!pip install llama-index
```

## LangChain LLM

```python
from langchain.chat_models import ChatAnyscale, ChatOpenAI
from llama_index.llms.langchain import LangChainLLM
from llama_index.core import PromptTemplate
```

```python
llm = LangChainLLM(ChatOpenAI())
```

```python
stream = await llm.astream(PromptTemplate("Merhaba, kısa bir hikaye yaz"))
```

```python
async for token in stream:
    print(token, end="")
```

```
Bir zamanlar, gür bir ormanın kalbinde yer alan küçük bir köyde, Lily adında genç bir kız yaşardı. Lily, nazik kalbi ve yumuşak huyuyla tanınırdı. Özel bir yeteneği vardı: hayvanlarla iletişim kurabilme becerisi.

Güneşli bir sabah, Lily ormanda dolaşırken yaralı bir kuşa rastladı. Kanadı kırılmıştı ve çaresiz görünüyordu. Lily'nin kalbi empatiyle doldu; kuşu dikkatlice yerden aldı ve ellerinin arasında şefkatle tuttu.

"Sana yardım edeceğim," diye fısıldadı sesi kararlılıkla dolu bir şekilde.

Lily aceleyle kulübesine döndü ve kuşu nazikçe rahat bir yuvaya yerleştirdi. Kanadını sardı ve yaralarına baktı. Küçük kuş, Lily'nin niyetini anlamışçasına minnetle öttü.

Günler haftalara döndü ve Lily, Oliver adını verdiği kuşa özenle bakmaya devam etti. Kanadı iyileşmiş olsa da Oliver gitmekte isteksizdi. Lily ve onun huzurlu hayatıyla güçlü bir bağ kurmuştu.

Bir akşam, Lily ve Oliver pencere kenarında otururken yüksek bir ses onları irkiltti. Merakla dışarı çıkıp araştırmaya karar verdiler. Şaşırtıcı bir şekilde, köylüler gökyüzünü işaret ederek telaş içindeydiler.

Muazzam bir fırtına bulutu yaklaşıyor, bir zamanlar mavi olan gökyüzünü karartıyordu. Panik başladı ve herkes sığınacak bir yer aramaya koştu. Ancak Lily, ormandaki hayvanların büyük tehlikede olduğunu biliyordu. Onları koruyacak evleri yoktu.

Oliver omzunda olan Lily, bulabildiği tüm hayvanları bir araya getirdi; sincaplar, tavşanlar, geyikler ve hatta bir tilki. Birlikte fırtınaya karşı birleştiler.

Özel yeteneğini kullanarak Lily hayvanlarla iletişim kurdu ve onları daha güvenli bir yere, kendi kulübesine yönlendirdi. Hayvanlar birbirlerinin varlığında teselli bularak bir araya toplandılar.

Dışarıda fırtına şiddetlenirken, Lily flütüyle yatıştırıcı melodiler çalarak korkmuş canlıları sakinleştirdi. Fırtına güçlendi ama Lily'nin sevgisi ve kararlılığı sarsılmazdı.

Nihayet, sanki bir sonsuzluk gibi gelen sürenin ardından fırtına dindi. Güneş bulutların arkasından çıktı ve ormanın üzerine sıcak bir ışık hüzmesi saçtı. Artık güvende ve sağlıklı olan hayvanlar doğal ortamlarına döndüler.

Lily onların ormanda gözden kayboluşunu izledi, kalbi sevinçle doluydu. Sadece Oliver için değil, kurtardığı tüm canlılar için bir fark yarattığını biliyordu.

O günden sonra Lily, ormanın koruyucusu oldu; sakinlerini korudu ve doğayla uyum içinde yaşadı. Hikayesi uzaklara yayıldı, başkalarına doğal dünyanın güzelliğine ve tüm canlılarına değer vermeleri için ilham verdi.

Böylece, iletişim yeteneği olan ve kalbi şefkatle dolu genç kız, insanlar ve hayvanlar arasındaki bağı beslemeye devam etti ve herkese nezaketin galip geldiği anlardaki sihri hatırlattı.
```

## ChatAnyscale ile Test Etme

```python
llm = LangChainLLM(ChatAnyscale())
```

```python
stream = llm.stream(
    PromptTemplate("Merhaba, hangi NFL takımı en çok Super Bowl galibiyetine sahip?")
)
for token in stream:
    print(token, end="")
```

```
Merhaba! Yardımcı ve saygılı bir asistan olarak, doğru ve güvenli bilgiler sağlamak için buradayım. Sorunuzu yanıtlamak gerekirse, en çok Super Bowl galibiyetine sahip takım altı şampiyonlukla Pittsburgh Steelers'tır (Not: New England Patriots da 6 galibiyete sahiptir). Ancak, Super Bowl galibiyetlerinin bir takımın başarısının sadece bir yönü olduğunu ve diğer birçok yetenekli ve başarılı NFL takımının da bulunduğunu belirtmek önemlidir. Ek olarak, NFL'in profesyonel bir spor ligi olduğunu ve buna saygı duyulması gerektiğini hatırlatmak isterim. Başka yardımcı olabileceğim bir şey var mı?
```

## OpenAI LLM

```python
from llama_index.llms.openai import OpenAI
```

```python
llm = OpenAI()
```

```python
stream = await llm.astream("Merhaba, kısa bir hikaye yaz")
```

```python
for token in stream:
    print(token, end="")
```

```
Bir zamanlar gür bir ormanın kalbinde yer alan küçük bir köyde, Lily adında genç bir kız yaşardı. Nazik kalbi ve macera dolu ruhuyla tanınırdı. Lily günlerinin çoğunu ormanı keşfederek, gizli hazineler keşfederek ve ormanı evi olarak gören canlılarla arkadaşlık kurarak geçirirdi.

Güneşli bir sabah, Lily ormanın derinliklerine doğru ilerlerken tuhaf bir görüntüyle karşılaştı. Yerde küçük, yaralı bir kuş yatıyordu, kanatları titriyordu. Lily'nin kalbi şefkatle doldu; kuşu dikkatlice yerden aldı ve ellerinin arasında tuttu. Onu eve götürüp iyileştirmeye karar verdi.

Günler haftalara döndü ve Lily'nin Pip adını verdiği kuş, onun bakımı altında güçlendi. Pip'in bir zamanlar mat olan tüyleri canlı renklerine kavuştu ve kanatları eski gücünü geri kazandı. Lily, Pip'in gerçekten ait olduğu yere, vahşi doğaya dönme vaktinin geldiğini biliyordu.

Lily, ağır bir kalple tüylü dostuna veda etti ve Pip'in gökyüzüne süzülüşünü, kanatlarının onu her geçen an daha yükseğe taşımasını izledi. Orada dururken içinde bir boşluk hissetti. Pip'in neşeli ötüşünü ve paylaştıkları arkadaşlığı özlemişti.

Bu boşluğu doldurmaya kararlı olan Lily, yeni bir maceraya atılmaya karar verdi. Yeni bir arkadaş bulmak amacıyla ormanı keşfe çıktı. Günler haftalara döndü ve Lily çeşitli hayvanlarla karşılaştı ama hiçbiri özlediği o mükemmel arkadaş gibi görünmüyordu.

Bir gün, şırıl şırıl akan bir derenin kenarında morali bozuk bir şekilde otururken bir hışırtı sesi dikkatini çekti. Arkasını döndüğünde parlak mavi gözleriyle ona bakan küçük, tüylü bir canlı buldu. Bu, kaybolmuş ve korkmuş bir bebek tilkiydi. Lily'nin kalbi eridi ve yeni arkadaşını bulduğunu anladı.

Tilkiye Finn adını verdi ve tıpkı Pip'e yaptığı gibi onu da himayesine aldı. Birlikte ormanı keşfettiler, ağaçlara tırmandılar ve saklambaç oynadılar. Finn, Lily'nin hayatına yeniden neşe ve kahkaha getirdi ve o, aralarındaki bu bağı çok sevdi.

Yıllar geçtikçe Lily ve Finn yaşlandılar ama dostlukları hep güçlü kaldı. Ayrılmaz bir ikili oldular, ormanı keşfettiler ve zorluklarla birlikte yüzleştiler. Lily ormandan ve canlılarından değerli dersler öğrendi ve bu hikayeleri onu dikkatle dinleyen Finn ile paylaştı.

Bir gün, en sevdikleri meşe ağacının altında otururken Lily, Pip'i ilk bulduğundan beri ne kadar büyüdüğünü fark etti. Şefkatin, dostluğun ve doğanın güzelliğinin önemini öğrenmişti. Orman onun tapınağı, canlıları ise ailesi olmuştu.

Lily maceralarının devam edeceğini ve yol boyunca her zaman yeni arkadaşlar bulacağını biliyordu. Yanında Finn varken karşısına çıkacak her türlü zorlukla yüzleşmeye hazırdı. Ve böylece, el ele (ve pençe pençeye), yeni anılar biriktirmek ve sayısız maceraya atılmak üzere ormanın derinliklerine doğru yola koyuldular.
```
