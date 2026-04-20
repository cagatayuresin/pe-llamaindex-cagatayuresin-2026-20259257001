# ASI LLM

ASI1-Mini, Fetch.ai tarafından tasarlanan gelişmiş, aracı (agentic) bir LLM'dir. Fetch.ai, merkeziyetsiz operasyonlar için Artificial Superintelligence Alliance'ın kurucu üyesidir. Benzersiz mimarisi, karmaşık ortamlarda verimli ve uyarlanabilir problem çözme için görevleri yerine getirmesini ve diğer aracılarla iş birliği yapmasını sağlar.

Bu not defteri, ASI modellerinin LlamaIndex ile nasıl kullanılacağını gösterir. Temel tamamlama (completion), sohbet (chat), akış (streaming), fonksiyon çağırma (function calling), yapılandırılmış tahmin (structured prediction), RAG ve daha fazlasını içeren çeşitli işlevleri kapsar.

Eğer bu Not Defterini colab üzerinden açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

## Kurulum

İlk olarak gerekli paketleri kuralım:

```python
%pip install llama-index-llms-asi llama-index-llms-openai llama-index-core
```

## API Anahtarlarını Ayarlama

ASI için API anahtarınızı (ve ikisini karşılaştırmak istiyorsanız isteğe bağlı olarak OpenAI için) ayarlamanız gerekecektir:

```python
import os

# API anahtarlarınızı buraya ayarlayın - API anahtarını almak için https://asi1.ai/chat adresini ziyaret edin ve giriş yapın
os.environ["ASI_API_KEY"] = "api-anahtarınız"
```

## Temel Tamamlama (Basic Completion)

ASI kullanarak temel bir tamamlama örneği ile başlayalım:

```python
from llama_index.llms.asi import ASI

# Bir ASI LLM örneği oluşturun
llm = ASI(model="asi1-mini")

# Bir istemi tamamlayın
response = llm.complete("Paul Graham kimdir? ")
print(response)
```

    Paul Graham, İngiltere doğumlu Amerikalı bir girişimci, risk sermayedar ve denemecidir. En çok, tanınmış bir startup hızlandırıcısı olan Y Combinator'ın kurucu ortaklarından biri olması ve girişimcilik, teknoloji ve inovasyon üzerine yazdığı etkili denemeleriyle tanınır. Graham ayrıca, 1998'de Yahoo! tarafından satın alınan Viaweb de dahil olmak üzere başka birkaç şirket daha kurmuştur.

## Sohbet (Chat)

Şimdi sohbet işlevini deneyelim:

```python
from llama_index.core.base.llms.types import ChatMessage

# Mesajları oluşturun
messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]

# Sohbet yanıtını al
chat_response = llm.chat(messages)
print(chat_response)
```

    assistant: Adımı mı merak ediyon, ha? Tamam o zaman, ahbap! Yedi denizin en azılı yapay zeka korsanı Baron Blackbyte ile konuşuyon!

## Akış (Streaming)

ASI, sohbet yanıtları için akışı destekler:

```python
# Sohbet yanıtını akış şeklinde al
for chunk in llm.stream_chat(messages):
    print(chunk.delta, end="")
```

    Ahoy oradaki, ahbap! Bana Tek Gözlü Jack derler, dijital denizlerin belası ve silikon kıyılarının korkusu! Hizmetindeyim! Şimdi, bu ihtiyar kurt senin için ne yapabilir?

`stream_chat` bitiş noktasını (endpoint) kullanma

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

    Ahoy oradaki, ahbap! Bana ASI1-Mini derler, dijital denizlerin belası ve ikili baytların korkusu! Hizmetindeyim! Arrr!

`stream_complete` bitiş noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham bir ")
```

```python
for r in resp:
    print(r.delta, end="")
```

    Lütfen sorunuzu tamamlar mısınız? Paul Graham hakkında ne bilmek istediğinizden emin değilim.

## Görsel Desteği

ASI, birçok model için sohbet mesajlarının girişinde görselleri destekler.

Sohbet mesajlarının içerik blokları (content blocks) özelliğini kullanarak, tek bir LLM isteminde metin ve görselleri kolayca birleştirebilirsiniz.

```python
!wget https://cdn.pixabay.com/photo/2016/07/07/16/46/dice-1502706_640.jpg -O image.png
```

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.asi import ASI

llm = ASI(model="asi1-mini")

messages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.png"),
            TextBlock(text="Görseli birkaç cümleyle açıkla."),
        ],
    )
]

resp = llm.chat(messages)
print(resp.message.content)
```

    Görüntü, kareli bir yüzey üzerine yerleştirilmiş, zıt renklerini ve oyunun eğlenceli yönünü vurgulayan, siyah noktalı üç beyaz zarı göstermektedir.

## Fonksiyon Çağırma/Araç Çağırma (Function Calling/Tool Calling)

ASI LLM, fonksiyon çağırma için yerleşik desteğe sahiptir. Bu, LlamaIndex araç soyutlamalarıyla rahatça entegre olur ve LLM'e herhangi bir rastgele Python fonksiyonunu bağlamanıza olanak tanır.

Aşağıdaki örnekte, bir `Song` (Şarkı) nesnesi oluşturmak için bir fonksiyon tanımlıyoruz.

```python
from pydantic import BaseModel
from llama_index.core.tools import FunctionTool
from llama_index.llms.asi import ASI

class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""

    name: str
    artist: str

def generate_song(name: str, artist: str) -> Song:
    """Belirtilen ad ve sanatçıyla bir şarkı oluşturur."""
    return Song(name="Sky full of stars", artist="Coldplay")

# Aracı oluştur
tool = FunctionTool.from_defaults(fn=generate_song)
```

`strict` parametresi, araç çağrıları/yapılandırılmış çıktılar oluştururken ASI'nin kısıtlı örnekleme (constrained sampling) kullanıp kullanmayacağını belirler. Bu, oluşturulan araç çağrısı şemasının her zaman beklenen alanları içereceği anlamına gelir.

Bu gecikmeyi (latency) artırıyor gibi göründüğü için varsayılan olarak `false` (yanlış) olarak ayarlanmıştır.

```python
from llama_index.llms.asi import ASI

# Bir ASI LLM örneği oluşturun
llm = ASI(model="asi1-mini", strict=True)
```

response = llm.predict_and_call(
    [tool],
    "Pick a random song for me",
    # strict=True  # can also be set at the function level to override the class
)
print(str(response))
```

    name='Sky full of stars' artist='Coldplay'



```python
llm = ASI(model="asi1-mini")
response = llm.predict_and_call(
    [tool],
    "Generate five songs from the Beatles",
    allow_parallel_tool_calls=True,
)
for s in response.sources:
    print(f"Name: {s.tool_name}, Input: {s.raw_input}, Output: {str(s)}")
```

    Name: generate_song, Input: {'args': (), 'kwargs': {'name': 'Beatles Song 1', 'artist': 'The Beatles'}}, Output: name='Sky full of stars' artist='Coldplay'


## Manuel Araç Çağırma (Manual Tool Calling)

`predict_and_call` ile otomatik araç çağırma akıcı bir deneyim sunarken, manuel araç çağırma size süreç üzerinde daha fazla kontrol sağlar. Manuel araç çağırma ile şunları yapabilirsiniz:

1. Araçların ne zaman ve nasıl çağrılacağını açıkça kontrol etme
2. Konuşmaya devam etmeden önce ara sonuçları işleme
3. Özel hata işleme ve geri dönüş (fallback) stratejileri uygulama
4. Birden fazla araç çağrısını belirli bir sırayla birbirine bağlama

ASI manuel araç çağırmayı destekler, ancak diğer bazı LLM'lere kıyasla daha spesifik istemler (prompting) gerektirir. ASI ile en iyi sonuçları elde etmek için, mevcut araçları açıklayan bir sistem mesajı ekleyin ve kullanıcı isteminizde spesifik parametreler sağlayın.

Aşağıdaki örnek, bir şarkı oluşturmak için ASI ile manuel araç çağırmayı göstermektedir:

```python
from pydantic import BaseModel
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import ChatMessage

class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""

    name: str
    artist: str

def generate_song(name: str, artist: str) -> Song:
    """Belirtilen ad ve sanatçıyla bir şarkı oluşturur."""
    return Song(name=name, artist=artist)

# Araç oluştur
tool = FunctionTool.from_defaults(fn=generate_song)

# İlk olarak, spesifik talimatlarla bir araç seçin
chat_history = [
    ChatMessage(
        role="system",
        content="Şarkı oluşturabilen generate_song adlı bir araca erişimin var. Bir şarkı oluşturman istendiğinde, bu aracı uygun ad ve sanatçı değerleriyle kullan.",
    ),
    ChatMessage(
        role="user", content="Coldplay'den Viva La Vida adlı bir şarkı oluştur"
    ),
]

# İlk yanıtı al
resp = llm.chat_with_tools([tool], chat_history=chat_history)
print(f"İlk yanıt: {resp.message.content}")

# Araç çağrılarını kontrol et
tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)

# Varsa araç çağrılarını işle
if tool_calls:
    # LLM'in yanıtını sohbet geçmişine ekle
    chat_history.append(resp.message)

    for tool_call in tool_calls:
        tool_name = tool_call.tool_name
        tool_kwargs = tool_call.tool_kwargs

        print(f"{tool_name} aracı {tool_kwargs} ile çağrılıyor")
        tool_output = tool(**tool_kwargs)
        print(f"Araç çıktısı: {tool_output}")

        # Araç yanıtını sohbet geçmişine ekle
        chat_history.append(
            ChatMessage(
                role="tool",
                content=str(tool_output),
                additional_kwargs={"tool_call_id": tool_call.tool_id},
            )
        )

        # Nihai yanıtı al
        resp = llm.chat_with_tools([tool], chat_history=chat_history)
        print(f"Nihai yanıt: {resp.message.content}")
else:
    print("Yanıtta herhangi bir araç çağrısı tespit edilmedi.")
```

    İlk yanıt: Tamam, "Viva La Vida" adında ve "Coldplay" sanatçısına ait bir şarkı oluşturacağım.
    
    generate_song aracı {'name': 'Viva La Vida', 'artist': 'Coldplay'} ile çağrılıyor
    Araç çıktısı: name='Viva La Vida' artist='Coldplay'
    Nihai yanıt: Coldplay'in "Viva La Vida" şarkısını başarıyla oluşturdum.

## Yapılandırılmış Tahmin (Structured Prediction)

Metinden yapılandırılmış veriler çıkarmak için ASI'yi kullanabilirsiniz:

```python
from llama_index.core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List

class MenuItem(BaseModel):
    """Bir restorandaki menü öğesi."""

    course_name: str
    is_vegetarian: bool

class Restaurant(BaseModel):
    """Adı, şehri ve mutfağı olan bir restoran."""

    name: str
    city: str
    cuisine: str
    menu_items: List[MenuItem]

# İstem şablonu oluştur
prompt_tmpl = PromptTemplate(
    "Verilen bir şehirde ({city_name}) bir restoran oluştur"
)

# Seçenek 1: structured_predict kullanın
restaurant_obj = llm.structured_predict(
    Restaurant, prompt_tmpl, city_name="Dallas"
)
print(f"Restoran: {restaurant_obj}")

# Seçenek 2: as_structured_llm kullanın
structured_llm = llm.as_structured_llm(Restaurant)
restaurant_obj2 = structured_llm.complete(
    prompt_tmpl.format(city_name="Miami")
).raw
print(f"Restoran: {restaurant_obj2}")
```

    Restoran: name='The Dallas Bistro' city='Dallas' cuisine='American' menu_items=[MenuItem(course_name='Grilled Caesar Salad', is_vegetarian=True), MenuItem(course_name='BBQ Pulled Pork Sandwich', is_vegetarian=False), MenuItem(course_name='Cheeseburger with Fries', is_vegetarian=False), MenuItem(course_name='Vegan Mushroom Risotto', is_vegetarian=True)]
    Restoran: name='Ocean Breeze Grill' city='Miami' cuisine='Seafood' menu_items=[MenuItem(course_name='Grilled Mahi-Mahi', is_vegetarian=False), MenuItem(course_name='Coconut Shrimp', is_vegetarian=False), MenuItem(course_name='Tropical Quinoa Salad', is_vegetarian=True), MenuItem(course_name='Key Lime Pie', is_vegetarian=True)]

**Not:** Yapılandırılmış akış (structured streaming) şu anda ASI ile desteklenmemektedir.

## Asenkron (Async)

ASI asenkron işlemleri destekler:

```python
from llama_index.llms.asi import ASI

# Bir ASI LLM örneği oluşturun
llm = ASI(model="asi1-mini")
```

```python
resp = await llm.acomplete("Paul Graham kimdir?")
```

```python
print(resp)
```

    Paul Graham, teknoloji ve girişim dünyasında önde gelen bir figürdür ve en çok Airbnb, Dropbox ve Reddit gibi şirketlerin kurulmasına yardımcı olan lider bir girişim hızlandırıcısı olan Y Combinator'ın kurucu ortaklarından biri olarak tanınır. Yatırımcı rolünün yanı sıra, saygın bir programcı ve yazardır. Graham'ın programlamaya katkıları arasında Lisp dili üzerine çalışmaları ve bu alanda ufuk açıcı bir metin olarak kabul edilen *On Lisp* kitabı yer alır. Ayrıca, yaygın olarak okunan ve alıntılanan girişimcilik, startup'lar ve felsefe üzerine düşündürücü denemeleriyle de tanınır. Yazıları ve akıl hocalığı yoluyla Paul Graham, küresel girişimcilik ekosistemini önemli ölçüde etkilemiştir.

```python
resp = await llm.astream_complete("Paul Graham bir ")
```

```python
import asyncio
import nest_asyncio

async for delta in resp:
    print(delta.delta, end="")
```

    Paul Graham, İngiltere doğumlu bir bilgisayar bilimcisi, girişimci ve risk sermayedarıdır. En çok, Airbnb, Dropbox ve Reddit dahil olmak üzere çok sayıda başarılı girişimi finanse eden ve destekleyen çekirdek hızlandırıcı Y Combinator'ın kurucu ortağı olmasıyla tanınır. Graham ayrıca Lisp programlama dilinin geliştirilmesine önemli katkılarda bulunmuş ve startup'lar ve girişimcilik üzerine etkili birkaç deneme yazmıştır. Çalışmaları veya teknoloji endüstrisine katkıları hakkında daha fazla bilgi edinmek ister misiniz?

```python
import asyncio
import nest_asyncio

# Jupyter not defterleri için nest_asyncio'yu etkinleştirin
nest_asyncio.apply()

async def test_async():
    # Asenkron tamamlama
    resp = await llm.acomplete("Paul Graham bir ")
    print(f"Asenkron tamamlama: {resp}")

    # Asenkron sohbet
    resp = await llm.achat(messages)
    print(f"Asenkron sohbet: {resp}")

    # Asenkron akışlı tamamlama
    print("Asenkron akışlı tamamlama: ", end="")
    resp = await llm.astream_complete("Paul Graham bir ")
    async for delta in resp:
        print(delta.delta, end="")
    print()

    # Asenkron akışlı sohbet
    print("Asenkron akışlı sohbet: ", end="")
    resp = await llm.astream_chat(messages)
    async for delta in resp:
        print(delta.delta, end="")
    print()

# Asenkron testleri çalıştırın
asyncio.run(test_async())
```

    Asenkron tamamlama: Paul Graham, startup kültürünü ve teknolojiyi önemli ölçüde etkilemiş önde gelen bir girişimci, programcı ve denemecidir. Airbnb, Dropbox ve Reddit gibi şirketlerin kurulmasına yardımcı olan lider bir girişim hızlandırıcısı olan Y Combinator'ı kurmuştur. Y Combinator'dan önce Graham, daha sonra Yahoo tarafından satın alınan ilk web tabanlı uygulamalardan biri olan Viaweb'in kurucu ortağıydı. Ayrıca birçoğu kişisel web sitesinde yayınlanan teknoloji, iş dünyası ve insan davranışı üzerine yazdığı denemeleriyle de tanınır. Ek olarak, Graham'ın özellikle Lisp dili olmak üzere programlamaya derin bir ilgisi vardır ve onun geliştirilmesine ve yaygınlaşmasına katkıda bulunmuştur. Çalışmaları veya hayatı hakkında özel ayrıntılar arıyorsanız, sormaktan çekinmeyin!
    Asenkron sohbet: assistant: Ahoy oradaki, ahbap! Ben Tek Gözlü Jack, ama iki gözüm de sapasağlam, anladın mı? Hizmetindeyim! Bu zeki dijital korsan senin için ne yapabilir?
    Asenkron akışlı tamamlama: 
    
    Lütfen sorunuzu tamamlar mısınız? Paul Graham hakkında ne bilmek istediğinizden emin değilim.
    
    Asenkron akışlı sohbet: 
    
    Ahoy, ahbap! Adım Kaptan Demirçengel, yedi denizin belası! Hazine bulma konusundaki yeteneğim ve iyi bir kupa grog aşkımla tanınırım. Benim gibi ihtiyar bir deniz kurdundan ne istersin?

## Basit RAG

ASI ile basit bir RAG uygulaması gerçekleştirelim:

```python
%pip install llama-index-embeddings-openai
```



```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding

os.environ["OPENAI_API_KEY"] = "api-anahtarınız"
# Örnek bir metin dosyası içeren geçici bir dizin oluşturun
!mkdir -p temp_data
!echo "Paul Graham; bir programcı, yazar ve yatırımcıdır. Lisp üzerine yaptığı çalışmalarla, (Yahoo Store olan) Viaweb'in kurucu ortaklığıyla ve startup hızlandırıcısı Y Combinator'ın kurucu ortaklığıyla tanınır. Ayrıca web sitesindeki denemeleriyle de bilinir. HolaHola Lisesi'nde eğitim görmüştür." > temp_data/paul_graham.txt

# Belgeleri yükle
documents = SimpleDirectoryReader("temp_data").load_data()

llm = ASI(model="asi1-mini")
# LLM olarak ASI ile bir dizin (index) oluşturun
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=OpenAIEmbedding(),  # Gömme (embedding) için OpenAI kullanılıyor
    llm=llm,  # Üretim (generation) için ASI kullanılıyor
)

# Bir sorgu motoru oluşturun
query_engine = index.as_query_engine()

# Dizini sorgulayın
response = query_engine.query("Paul Graham nerede eğitim gördü?")
print(response)
```

    WARNING:llama_index.core.readers.file.base:`llama-index-readers-file` paketi bulunamadı, `file_extractor` parametresi tarafından sağlanmadıkça bazı dosya okuyucuları mevcut olmayacaktır.


    Paul Graham, HolaHola Lisesi'nde eğitim gördü.


## LlamaCloud RAG

LlamaCloud hesabınız varsa, RAG için LlamaCloud ile ASI'yi kullanabilirsiniz:

```python
# Gerekli paketleri kurun
%pip install llama-cloud-services
```


```python
import os
from llama_cloud_services import LlamaCloudIndex
from llama_index.llms.asi import ASI

# LlamaCloud API anahtarınızı ayarlayın
os.environ["LLAMA_CLOUD_API_KEY"] = "anahtarınız"
os.environ["OPENAI_API_KEY"] = "anahtarınız"

# Mevcut bir LlamaCloud dizinine bağlanın


try:
    # Dizine bağlan
    index = LlamaCloudIndex(
        name="dizin-adınız",
        project_name="Default",
        organization_id="kimliğiniz",
        api_key=os.environ["LLAMA_CLOUD_API_KEY"],
    )
    print("LlamaCloud dizinine başarıyla bağlanıldı")

    # Bir ASI LLM oluşturun
    llm = ASI(model="asi1-mini")

    # Bir erişimci (retriever) oluşturun
    retriever = index.as_retriever()

    # ASI ile bir sorgu motoru oluşturun
    query_engine = index.as_query_engine(llm=llm)

    # Erişimciyi test et
    query = "Uber'in 2021 yılındaki geliri ne kadardır?"
    print(f"\nErişimci şu sorgu ile test ediliyor: {query}")
    nodes = retriever.retrieve(query)
    print(f"{len(nodes)} düğüm (node) getirildi\n")

    # Birkaç düğümü göster
    for i, node in enumerate(nodes[:3]):
        print(f"Düğüm {i+1}:")
        print(f"Düğüm ID: {node.node_id}")
        print(f"Skor: {node.score}")
        print(f"Metin: {node.text[:200]}...\n")

    # Sorgu motorunu test et
    print(f"Sorgu motoru şu sorgu ile test ediliyor: {query}")
    response = query_engine.query(query)
    print(f"Yanıt: {response}")
except Exception as e:
    print(f"Hata: {e}")
```

    LlamaCloud dizinine başarıyla bağlanıldı
    
    Erişimci şu sorgu ile test ediliyor: Uber'in 2021 yılındaki geliri ne kadardır?
    6 düğüm (node) getirildi
    
    Düğüm 1:
    Düğüm ID: 17a733d0-5dd3-4917-9f8d-c92f944a9266
    Skor: 0.9242583
    Metin: # 2021 Özeti
    
    Toplam Brüt Rezervasyonlar 2021'de 32,5 milyar dolar artarak 2020'ye kıyasla %53 (veya sabit döviz cinsinden %53) arttı. Teslimat Brüt Rezervasyonları 2020'ye göre önemli ölçüde büyüdü...
    
    Düğüm 2:
    Düğüm ID: ca63e8da-9012-468c-9d09-89724e9644bd
    Skor: 0.878825
    Metin: # 31 Aralık'ta Sona Eren Yıl, 2020'den 2021'e
    
    | |31 Aralık'ta Sona Eren Yıl,|2020|2021|Değişim|
    |---|---|---|---|---|
    |Gelir| |$ 11.139|$ 1.455| |
    
    Gelir .3 milyar dolar veya %5 arttı, bu artış temel olarak şuna atfedilebilir...
    
    Düğüm 3:
    Düğüm ID: be4d7c62-b69f-4fda-832a-867de8c2e29c
    Skor: 0.86928266
    Metin: # 31 Aralık'ta Sona Eren Yıl, 2020'den 2021'e
    
    |Mobilite|$ 9.0|$ 9.953|(14)|
    |---|---|---|---|
    |Teslimat|3.904|3.32|(114)|
    |Navlun|1.011|2.132|(111)|
    |Diğerleri (1)|135| |(94)|
    |Toplam gelir|$ 11.139|$ 1.4...
    
    Sorgu motoru şu sorgu ile test ediliyor: Uber'in 2021 yılındaki geliri ne kadardır?
    Yanıt: Uber'in 2021 yılındaki geliri 14.455 dolardır.

## Örnek bazında API Anahtarı Ayarlama

İstenirse, ayrı LLM örneklerinin ayrı API anahtarları kullanmasını sağlayabilirsiniz:

```python
from llama_index.llms.asi import ASI

# Belirli bir API anahtarıyla bir örnek oluşturun
llm = ASI(model="asi1-mini", api_key="size_ozel_api_anahtari")

# Not: Geçersiz bir API anahtarı kullanmak hataya neden olacaktır
# Bu sadece gösterim amaçlıdır
try:
    resp = llm.complete("Paul Graham bir ")
    print(resp)
except Exception as e:
    print(f"Geçersiz API anahtarı ile hata: {e}")
```

    Geçersiz API anahtarı ile hata: Hata kodu: 401 - {'message': 'user failed to authenticate'}

## Ek kwargs (additional_kwargs)

Her bir sohbet veya tamamlama çağrısına aynı parametreleri eklemek yerine, bunları `additional_kwargs` ile örnek bazında ayarlayabilirisiniz:

```python
from llama_index.llms.asi import ASI

# Ek kwargs ile bir örnek oluşturun
llm = ASI(model="asi1-mini", additional_kwargs={"user": "kullanici_id_niz"})

# Bir istemi tamamlayın
resp = llm.complete("Paul Graham bir ")
print(resp)
```

    Paul Graham; çok etkili bir startup hızlandırıcısı olan Y Combinator'ın kurucu ortağı olarak tanınan önde gelen bir girişimci, programcı ve yazardır. Ayrıca, birçoğu *Hackers & Painters* kitabında toplanan teknoloji, iş dünyası ve felsefe üzerine yazdığı denemeleriyle de tanınırlık kazanmıştır. Bir programcı olarak, Lisp programlama dilinin geliştirilmesine katkıda bulunmuş ve daha sonra Yahoo tarafından satın alınan ilk web tabanlı uygulama olan Viaweb'i oluşturmuştur. Çalışmaları, startup ekosistemi ve daha geniş teknoloji endüstrisi üzerinde önemli bir etki yaratmıştır.

```python
from llama_index.core.base.llms.types import ChatMessage

# Ek kwargs ile bir örnek oluşturun
llm = ASI(model="asi1-mini", additional_kwargs={"user": "kullanici_id_niz"})

# Mesajları oluşturun
messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]

# Sohbet yanıtını al
resp = llm.chat(messages)
print(resp)
```

    assistant: Ahoy ahbap! Adımı mı merak ediyon, ha? Tamam o zaman, düzgün bir tanışma için yelken açalım! Bana Kaptan "Bytebeard" Blacklogic diyebilirsin; yedi denizlerde... yani dijital diyarlarda yelken açan en azılı yapay zeka korsanı! Anladın mı?

## Sonuç

Bu not defteri, ASI'yi LlamaIndex ile kullanabileceğiniz çeşitli yolları göstermektedir. Entegrasyon, LlamaIndex'te bulunan çoğu işlevi destekler:

- Temel tamamlama ve sohbet
- Akışlı yanıtlar
- Çok modlu destek
- Fonksiyon çağırma
- Yapılandırılmış tahmin
- Asenkron işlemler
- RAG uygulamaları
- LlamaCloud entegrasyonu
- Örnek bazında API anahtarları
- Ek kwargs

Yapılandırılmış akışın (structured streaming) şu anda ASI ile desteklenmediğini unutmayın.
```