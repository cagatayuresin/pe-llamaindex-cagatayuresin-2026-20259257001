# Fireworks

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index llama-index-llms-fireworks
```

## Temel Kullanım

```python
from llama_index.llms.fireworks import Fireworks

# Kullanılabilir modellerin güncel listesi için bkz: https://app.fireworks.ai/models
llm = Fireworks(
    model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    # api_key="bir anahtar",  # varsayılan olarak FIREWORKS_API_KEY ortam değişkenini kullanır
)
```

#### Bir istemle `complete` çağrısı yapın

```python
resp = llm.complete("Paul Graham bir ")
```

```python
print(resp)
```

    Teknoloji endüstrisinde ve girişimcilik dünyasında tanınmış bir figürdür. Paul Graham şunlardır:
    
    1. **Risk sermayedarı**: Airbnb, Dropbox ve Reddit dahil olmak üzere birçok başarılı şirkete yatırım yapmış bir girişim hızlandırıcısı ve tohum fonu olan Y Combinator'ın (YC) kurucu ortaklarındandır.
    2. **Girişimci**: Graham, 1998 yılında Yahoo! tarafından 49 milyon dolara satın alınan bir çevrimiçi açık artırma şirketi olan Viaweb'in kurucu ortaklarındandır.
    3. **Yazar**: "Hackers & Painters: Big Ideas from the Computer Age" ve "The Startup Owner's Manual" dahil olmak üzere girişimcilik üzerine birkaç kitap yazmıştır.
    4. **Blogger**: Girişimcilik, startup'lar ve teknoloji hakkındaki düşüncelerini paylaştığı popüler bir blog olan "Paul Graham's Essays"in yazarıdır.
    5. **Filozof**: Yazıları genellikle teknoloji, ekonomi ve felsefenin kesişimini araştırır ve Friedrich Hayek ve Ayn Rand gibi düşünürlerden etkilenmiştir.
    
    Graham, girişimcilik konusundaki aykırı görüşleri ve deney yapmanın, yinelemenin ve başarısızlıktan ders çıkarmanın önemi üzerindeki vurgusuyla tanınır. Ayrıca, startup'ların bir "tek boynuzlu at" (unicorn) şirket kurmaya çalışmak yerine gerçek bir sorunu çözen bir ürün oluşturmaya odaklanmaları gerektiği fikrinin güçlü bir savunucusu olmuştur.

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

    assistant: Hey hey! Benim adım Kaptan Kara-Gaga Betty, Yedi Denizler'de yelken açmış en çok korkulan ve kötü şöhretli korsan! Altın gibi bir kalbi ve macera dolu bir ruhu olan kılıç ustası bir haydutum. Gemim, "Maverick'in İntikamı", benim evim ve gururumdur; mürettebatım ise açık denizlerdeki en sadık ve güvenilir deniz kurtlarıdır!
    
    Peki, seni bu güzel sulara getiren nedir? Mürettebatıma katılıp hazine ve şan arayışıyla denizlere yelken açmak mı istiyorsun? Yoksa sadece biraz bela ve korsan hayatından bir parça tat mı arıyorsun? Her halükarda şanslısın ahbap, çünkü Kaptan Kara-Gaga Betty en dalgalı sularda ve en tehlikeli denizlerde sana rehberlik etmek için burada!

## Akış (Streaming)

`stream_complete` bitiş noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham bir ")
```

```python
for r in resp:
    print(r.delta, end="")
```

    Teknoloji endüstrisinde tanınmış bir figürdür!
    
    Paul Graham, İngiliz-Amerikalı bir programcı, risk sermayedarı ve deneme yazarıdır. En çok şunlarla tanınır:
    
    1. **Y Combinator'ın Kurucu Ortaklığı**: 2005 yılında Graham, erken aşamadaki startup'lara tohum finansmanı ve mentorluk sağlayan bir girişim hızlandırıcısı olan Y Combinator'ı kurdu. Y Combinator, dünyanın en başarılı ve etkili girişim hızlandırıcılarından biri haline geldi.
    2. **Girişimcilik ve Programlama Üzerine Denemeler Yazmak**: Graham üretken bir yazardır ve girişimcilik, programlama ve startup ekosistemi gibi konularda birçok deneme yazmıştır. Denemeleri teknoloji dünyasında yaygın olarak okunur ve saygı görür.
    3. **Başarılı Bir Girişimci Olmak**: Y Combinator'ı kurmadan önce Graham, 1998'de Yahoo! tarafından 49 milyon dolara satın alınan bir çevrimiçi açık artırma şirketi olan Viaweb'in kurucu ortaklığını yaptı.
    4. **Startup'lara Yatırım Yapmak**: Graham, Y Combinator aracılığıyla Dropbox, Airbnb ve Reddit dahil olmak üzere birçok başarılı girişime yatırım yaptı.
    
    Graham'ın fikirleri ve yazıları startup ekosistemi üzerinde önemli bir etkiye sahip olmuştur ve teknoloji endüstrisindeki en etkili isimlerden biri olarak kabul edilmektedir.

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

    Hey hey! Benim adım Kaptan Kara-Gaga Betty, Yedi Denizler'de yelken açmış en çok korkulan ve kötü şöhretli korsan! Altın gibi bir kalbi ve macera dolu bir ruhu olan kılıç ustası bir haydutum. Ben ve sadık papağanım Polly, neredeyse 20 yıldır açık denizlerde yelken açıyor, hazine yağmalıyor ve yolumuza çıkan herkese neşe dağıtıyoruz.
    
    Gemim, "Maverick'in İntikamı", üç direkli ve kömür kadar siyah gövdeli bir güzeldir. Hızlıdır, azılıdır ve benim evimdir. Mürettebatım, "Maverick'in Adamları", karışık bir gruptur ama birbirimize ve kaptanımıza, yani bana sadığız!
    
    Peki, seni bu güzel sulara getiren nedir? Mürettebatıma katılıp tüm zamanların en büyük korsanıyla denizlere yelken açmak mı istiyorsun? Yoksa sadece biraz hazine ve anlatılacak bir hikaye mi arıyorsun? Her halükarda şanslısın ahbap! Kaptan Kara-Gaga Betty aradığın şeyi bulmana yardım etmek için burada!
