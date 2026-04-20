# AlibabaCloud-PaiEas

---
title: AlibabaCloud-PaiEas
 | LlamaIndex OSS Documentation
---

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
%pip install llama-index-llms-paieas
```

```python
Requirement already satisfied: llama-index-llms-paieas in /mnt/llm/xiaowen/miniconda3/envs/llama_env/lib/python3.9/site-packages (0.1.16)es (from llama-index-core<0.11.0,>=0.10.57->llama-index-llms-paieas) (1.0.8)
...
Not: Güncellenmiş paketleri kullanmak için çekirdeği (kernel) yeniden başlatmanız gerekebilir.
```

```python
!pip install llama-index
```

```python
Collecting llama-index
  Downloading llama_index-0.10.58-py3-none-any.whl.metadata (11 kB)
  ...
llama-index-readers-llama-parse-0.1.6 llama-parse-0.4.9 pypdf-4.3.1 striprtf-0.0.26
```

## Temel Kullanım

[AlibabaCloud PAI Eas](https://help.aliyun.com/zh/pai/use-cases/deploy-llm-in-eas?spm=5176.pai-console-inland.help.dexternal.107e642dLd2e9J) adresinden bir API anahtarı ve URL almanız gerekecektir. Aldıktan sonra, bunları modele doğrudan geçirebilir veya `PAIEAS_API_KEY` ve `PAIEAS_API_BASE` ortam değişkenlerini kullanabilirsiniz.

```bash
!export PAIEAS_API_KEY=servis_tokeniniz
!export PAIEAS_API_BASE=erisim_adresiniz
```

#### Bir istem (prompt) ile `complete` çağrısı

```python
from llama_index.llms.paieas import PaiEas


llm = PaiEas()
resp = llm.complete("Sihirli bir sırt çantası hakkında bir şiir yaz")
```

```python
print(resp)
```

```python
Harikalar ve neşe dolu bir diyarda, Düşlerin ve sihrin gün yüzüne çıktığı yerde, Genç bir gezgin yaşarmış, yüreği sevinçle dolu, Ve sırt çantasında saklarmış bir sırrı, Görülmeye değer sihirli bir hazine yolu.

Nasıl da parıldarmış bu çanta, nasıl da ışık saçarmış, İçinden bir efsun akar, her yana yayılırmış, Gözlerden gizli ince bir güç, sessizce akarmış, Ama sahibi için, o yücelere çıkan bir bakışmış.

Ağırlığı hafifmiş ama taşırmış kendi yükünü, Henüz bilinmeyen hikayelerin gizli düğümünü, Boşken küçülür, iyilikle dolunca büyürmüş, Gerçek bir dost, sadık bir araç gibi görünürmüş.

Basit bir hışırtıyla, fısıltıyla konuşurmuş, Genç gezgine çetin yolculuğunda rehber olurmuş, Dağları taşıyacak kadar genişler veya bir meltem taşırmış, Sihri sınır tanımaz, her arzuyu karşılamaya şaşarmış.

İçinde ölçülemez hazineler barındırırmış, Evrenin sırları içinde saklı dururmuş, Kayıp yönler için bir pusula, karanlıkta bir fener, İhtiyaç anında bir dost, sihirli çantadan izler.

Gezgine yardım etmiş ormanlarda, geniş nehirlerde, Çatışma ve gurur anlarında el vermiş her yerde, Ona dersler öğretmiş, göstermiş doğru yolu, Ve onun kucağında, huzurla bulmuş sağı solu.

İşte sihirli sırt çantasına, o harika şeye selam, Genç yolcu için kanatların senfonisidir bu kelam, Sadece zihnimizde değil, var olan bir sihir bu, Kaşiflerin bulduğu dünyada, en güzel gerçek bu.
```

#### Mesaj listesi ile `chat` çağrısı

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne"),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

```python
assistant: Bir korsan olarak beni Jack "Sparrow" Silverhand veya sadece Korsan Jack olarak bilirler. Eğer maceracı hissediyorsan bana öyle seslenebilirsin!
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham kimdir?")
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Paul Graham bir bilgisayar bilimcisi, girişimci ve yatırımcıdır. 24 Haziran 1955'te New York City'de doğdu. Graham, çevrimiçi kodlama platformu HackerRank'in, startup girişim firması Y Combinator'ın ve daha sonra Yahoo! GeoMaps haline gelen Viaweb'in kurucu ortaklarındandır. Ayrıca, "Hackers & Painters" (Hackerlar ve Ressamlar) kitabı ve teknoloji, startup'lar ve girişimcilik üzerine görüşlerini paylaştığı bloguyla da tanınır. Graham, teknoloji endüstrisinde önde gelen bir figür olarak kabul edilir ve genellikle Silikon Vadisi ekosisteminin büyümesine yaptığı erken katkılarla anılır.
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Bir korsan olarak, bir kara fare (landlubber) gibi süslü bir ismim yok. Düşmanlarımın kalbine korku salmak ve kılıç sallayan yollarımı haklı çıkarmak için "Karasakal" veya "Kaptan Jack" gibi korkunç lakaplar kullanırım. Ama unutma, ben burada sadece sohbet etmek için bulunan dost canlısı bir yapay zekayım, gerçek bir zarar vermek için değil!
```

## Asenkron (Async)

```python
resp = await llm.acomplete("Paul Graham kimdir?")
```

```python
print(resp)
```

```python
Paul Graham ünlü bir girişimci, bilgisayar bilimcisi ve risk sermayedaridir. 24 Nisan 1973'te Massachusetts, ABD'de doğan Graham, en çok Airbnb, Dropbox ve GitHub gibi birçok başarılı şirkete güç veren bir startup hızlandırıcısı olan Y Combinator'ın kurucu ortaklarından biri olarak tanınır. Graham aynı zamanda, girişimcilik ve teknoloji hakkındaki görüşlerini paylaştığı "Hackerlar ve Ressamlar" ve "Startup Okulu" gibi etkili kitapların yazarıdır. Teknoloji endüstrisinde önemli bir figür olmuştur ve genellikle bu alanda bir düşünce lideri olarak görülür.
```

```python
resp = await llm.astream_complete("Paul Graham kimdir?")
```

```python
async for delta in resp:
    print(delta.delta, end="")
```

```python
Paul Graham Amerikalı bir girişimci, bilgisayar bilimcisi ve yazardır. Tanınmış bir startup hızlandırıcısı ve yatırım firması olan yazılım şirketi Y Combinator'ın kurucu ortaklarındandır. Graham ayrıca, girişimcilik, teknoloji ve eğitim dahil olmak üzere çeşitli konulardaki düşüncelerini paylaştığı "Hackers & Painters" adlı bloguyla da tanınır. "Hackers: Heroes of the Computer Age" (Hackerlar: Bilgisayar Çağının Kahramanları) ve "Neden Oturma Odası Kanepenizde Bir Startup Kuramazsınız" dahil olmak üzere etkili kitaplar yazmıştır. Teknoloji endüstrisinde etkili olmuş bir isimdir ve startup ekosisteminde önde gelen bir figür olarak kabul edilir.
```
