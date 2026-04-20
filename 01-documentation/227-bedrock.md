# Bedrock

**Kullanımdan Kaldırılmıştır**: Bunun yerine [llama-index-llms-bedrock-converse](https://docs.llamaindex.ai/en/stable/examples/llm/bedrock_converse/) kullanın; converse API, Bedrock'u kullanmak için önerilen yoldur.

## Temel Kullanım

#### Bir istemle `complete` çağrısı yapın

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-bedrock
```

```python
!pip install llama-index
```

```python
from llama_index.llms.bedrock import Bedrock

profile_name = "AWS profil adınız"
resp = Bedrock(
    model="amazon.titan-text-express-v1", profile_name=profile_name
).complete("Paul Graham bir ")
```

```python
print(resp)
```

    Paul Graham; Silikon Vadisi merkezli girişim hızlandırıcısı Y Combinator'ın kurucu ortaklarından biri olarak tanınan bir bilgisayar bilimcisi ve girişimcidir. Ayrıca teknoloji ve iş konularında önde gelen bir yazar ve konuşmacıdır; denemeleri "Hackers & Painters" adlı bir kitapta toplanmıştır.

#### Bir mesaj listesiyle `chat` çağrısı yapın

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock import Bedrock

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]

resp = Bedrock(
    model="amazon.titan-text-express-v1", profile_name=profile_name
).chat(messages)
```

```python
print(resp)
```

    assistant: Tamamdır, ahbap! İşte sana bir hikaye:
    
    Bir zamanlar, yelken açtığı denizlerde bir sonraki macerasını arayan Kaptan Jack Sparrow adında bir korsan vardı. Tahmin edilemez ve biraz da haylaz biri olarak nam salmış, azılı bir düzenbazdı.
    
    Bir gün Kaptan Jack, aynı hazinenin peşinde olan bir grup hazine avcısı rakiple karşılaştı. Rakipler hazineyi Kaptan Jack'ten çalmaya çalıştılar ama Jack onları zekasıyla alt etti ve hazineyi kendine saklamayı başardı.
    
    Ancak Kaptan Jack kısa süre sonra çaldığı hazinenin lanetli olduğunu keşfetti. Onu ne zaman kullanmaya çalışsa, başına bir tür bela veya zahmet açıyordu. Örneğin, ne zaman harcamaya çalışsa, bir kum yığınına veya bir sürü deniz kaplumbağasına dönüşüyordu.
    
    Lanete rağmen Kaptan Jack onu kırmanın bir yolunu bulmaya kararlıydı. Laneti kaldırmasına yardım edebilecek bilge ve ihtiyar bir kahini bulmak için yola koyuldu. Yol boyunca, konuşan bir papağan ve bir deniz cadısı da dahil olmak üzere her türlü tuhaf ve büyülü yaratıkla karşılaştı.
    
    Sonunda Kaptan Jack kahini buldu ve durumunu anlattı. Kahin ona laneti kırmanın tek yolunun hazineyi gerçek sahibine geri vermek olduğunu söyledi.
    
    Kaptan Jack ilk başta tereddüt etti ama yapılması gereken doğru şeyin bu olduğunu biliyordu. Hazinenin gerçek sahibini bulmak için yeni bir maceraya atıldı ve yol boyunca bazen en büyük hazinelerin altın veya gümüşle ölçülebilenler değil, bir amaç ve anlam duygusuyla birlikte gelenler olduğunu keşfetti.
    
    Ve böylece Kaptan Jack hazineyi gerçek sahibine geri verdi ve lanet kalktı. Hayatın gerçek hazinesinin maddi mülklerde bulunmadığını, başkalarıyla kurduğumuz deneyimlerde ve bağlantılarda bulunduğunu öğrenmiş bir kahraman olarak gün batımına doğru yelken açtı.
    
    Yarr! Umarım bu hikayeyi beğenmişsindir, ahbap!

## Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
from llama_index.llms.bedrock import Bedrock

llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name)
resp = llm.stream_complete("Paul Graham bir ")
```

```python
for r in resp:
    print(r.delta, end="")
```

    Paul Graham; internet firması Y Combinator'ın kurucu ortaklarından biri olarak tanınan bilgisayar programcısı, girişimci, yatırımcı ve yazardır. Ayrıca "Girişimcinin İkilemi (The Innovator's Dilemma)" ve "İnternet Üzerine (On the Internet)" dahil olmak üzere birçok kitabın yazarıdır.
    
    Graham, startup topluluğunun ve teknoloji sektöründeki "yıkım" (disruption) kavramının güçlü bir destekçisi olmuştur. Erken aşamadaki şirketlerin karşılaştığı zorluklar ve yeni ve yenilikçi ürünler yaratmanın önemi hakkında kapsamlı yazılar yazmıştır.
    
    Graham ayrıca eğitim, hükümet ve internetin geleceği gibi çeşitli konulardaki aykırı görüşleriyle de tanınır. Amerika Birleşik Devletleri'nde yükseköğretimin yönetilme biçimini açıkça eleştirmiş ve öğrenmeye karşı daha deneysel ve girişimci bir yaklaşımı savunmuştur.
    
    Genel olarak Paul Graham, düşünceli ve düşündürücü yazıları ve yenilikçi startup'lara ve girişimcilere verdiği destekle tanınan, teknoloji endüstrisinde oldukça etkili bir figürdür.

`stream_chat` bitiş noktasını kullanma

```python
from llama_index.llms.bedrock import Bedrock

llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name)
messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

    Bir zamanlar, yedi denizde macera peşinde koşan renkli bir kişiliğe sahip bir korsan vardı. Cesareti, zekası ve gösterişli ve süslü olan her şeye duyduğu aşkla tanınırdı. Ancak bu kabadayı dış görünüşünün altında altın gibi bir kalp ve dünyada iyilik yapma arzusu yatıyordu.
    
    Bir gün, her zamanki yolculuklarından birindeyken, korsan zor durumda olan küçük bir adaya rastladı. Köylüler korkunç bir kuraklıktan muzdaripti ve mahsulleri ölüyordu. Korsan onlara yardım etmesi gerektiğini biliyordu ve bu yüzden adaya su getirmenin bir yolunu bulmak için yola çıktı.
    
    Uzun araştırmalar sonucunda korsan, adanın kalbinin derinliklerinde gizli bir kaynak keşfetti. Kaynak suyunu köylere taşıyacak bir boru ve su yolu sistemi inşa etmek için yorulmadan çalıştı ve nihayet aylar süren sıkı çalışmanın ardından kuraklık sona erdi ve insanlar kurtuldu.
    
    Korsan bir kahraman olarak ilan edildi ve köylüler onun onuruna büyük bir kutlama düzenlediler. Ama o işinin henüz bitmediğini biliyordu. İhtiyacı olan başkalarına yardım etmenin ve gittiği her yere neşe ve mutluluk yaymanın başka yollarını arayarak denizlerde yelken açmaya devam etti.
    
    Ve böylece, renkli kişiliğe sahip korsan, cesareti, nezaketi ve bitmek bilmeyen macera duygusuyla başkalarına ilham vererek ömrünü bir zafer parıltısı içinde yaşadı.

## Modeli Yapılandırma

```python
from llama_index.llms.bedrock import Bedrock

llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name)
```

```python
resp = llm.complete("Paul Graham bir ")
```

```python
print(resp)
```

    Paul Graham; bir bilgisayar bilimcisi, girişimci, yatırımcı ve yazardır. İlk ticari web tarayıcısı olan Viaweb'in kurucu ortaklarından biridir ve bir startup hızlandırıcısı olan Y Combinator'ın kurucusudur. "Bilgisayar Programlama Sanatı (The Art of Computer Programming)" ve "On Lisp" dahil olmak üzere birçok kitabın yazarıdır. Teknoloji ve iş dünyası üzerine yazdığı denemeleri ve teknoloji endüstrisine bakış açısıyla tanınır.

# Erişim Anahtarları (Access Keys) ile Bedrock'a Bağlanma

```python
from llama_index.llms.bedrock import Bedrock

llm = Bedrock(
    model="amazon.titan-text-express-v1",
    aws_access_key_id="Kullanılacak AWS Erişim Anahtar Kimliği (Access Key ID)",
    aws_secret_access_key="Kullanılacak AWS Gizli Erişim Anahtarı (Secret Access Key)",
    aws_session_token="Kullanılacak AWS Oturum Belirteci (Session Token)",
    region_name="Kullanılacak AWS Bölgesi, örn. us-east-1",
)

resp = llm.complete("Paul Graham bir ")
```

```python
print(resp)
```

    Paul Graham; ilk ticari web tarayıcısı olan Viaweb'in kurucu ortaklığıyla tanınan Amerikalı bir bilgisayar bilimcisi, girişimci, yatırımcı ve yazardır. Netscape Communications'ın kurucu ortağı ve Mozilla Vakfı'nın yaratıcısıdır. Aynı zamanda bir Y Combinator ortağıdır ve Airbnb, Dropbox, Facebook ve Twitter gibi şirketlerin önde gelen erken aşama yatırımcılarından biridir.
