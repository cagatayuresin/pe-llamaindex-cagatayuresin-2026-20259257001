# OpenAI

---
title: OpenAI
 | LlamaIndex OSS Documentation
---

Bu not defteri, OpenAI LLM'nin nasıl kullanılacağını gösterir.

Resmi OpenAI API'si olmayan OpenAI uyumlu bir API ile entegrasyon arıyorsanız, lütfen [OpenAI-Compatible LLMs](https://docs.llamaindex.ai/en/stable/api_reference/llms/openai_like/#llama_index.llms.openai_like.OpenAILike) entegrasyonuna bakın.

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```
%pip install llama-index llama-index-llms-openai
```

## Temel Kullanım

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(
    model="gpt-4o-mini",
    # api_key="some key",  # varsayılan olarak OPENAI_API_KEY ortam değişkenini kullanır
)
```

#### Bir istemle `complete` çağrısı

```python
from llama_index.llms.openai import OpenAI


resp = llm.complete("Paul Graham kimdir? ")
```

```python
print(resp)
```

```python
Paul Graham bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. En çok startup hızlandırıcısı Y Combinator'ın kurucu ortağı olması ve bir programlama dili olan Lisp üzerindeki çalışmalarıyla tanınır. Graham ayrıca startup'lar, teknoloji ve girişimcilik üzerine birçok etkili makale yazmıştır.
```

#### Bir mesaj listesiyle `chat` çağrısı

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
assistant: Ahoy ahbap! Adım Gökkuşağı Roger, yedi denizin en renkli korsanı! Bugün senin için ne yapabilirim?
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham kimdir? ")
```

```python
for r in resp:
    print(r.delta, end="")
```

```python
Paul Graham bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. En çok startup hızlandırıcısı Y Combinator'ın kurucu ortağı olması ve programlama dilleri ile web geliştirme üzerindeki çalışmalarıyla tanınır. Graham aynı zamanda üretken bir yazardır ve teknoloji, startup'lar ve girişimcilik üzerine birçok etkili makale yayınlamıştır.
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
Ahoy ahbap! Adım Kaptan Gökkuşağısakal! Evet, renkli ve parlak olan her şeyi seven bir korsanım. Sakalım bir gökkuşağı kadar canlıdır ve gemim yedi denizdeki en renkli teknedir! Bugün senin için ne yapabilirim cancağızım?
```

## Modeli Yapılandır

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-4o")
```

```python
resp = llm.complete("Paul Graham kimdir? ")
```

```python
print(resp)
```

```python
bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. En çok startup hızlandırıcısı Y Combinator'ın kurucu ortaklarından biri olması ve bir programlama dili olan Lisp üzerindeki çalışmalarıyla tanınır. Graham ayrıca startup'lar, teknoloji ve girişimcilik üzerine birçok etkili makale yazmıştır.
```

```python
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
assistant: Ahoy ahbap! Adım Kaptan Gökkuşağısakal, yedi denizin en renkli korsanı! Bugün senin için ne yapabilirim? Arrr!
```

## Görüntü Desteği

OpenAI, birçok model için sohbet mesajlarının girişinde görüntü desteğine sahiptir.

Mesajların içerik blokları (content blocks) özelliğini kullanarak, metin ve görüntüleri tek bir LLM isteminde kolayca birleştirebilirsiniz.

```python
!wget https://cdn.pixabay.com/photo/2016/07/07/16/46/dice-1502706_640.jpg -O image.png
```

```python
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-4o")


messages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.png"),
            TextBlock(text="Görüntüyü birkaç cümleyle tanımla."),
        ],
    )
]


resp = llm.chat(messages)
print(resp.message.content)
```

```python
Görüntü, muhtemelen bir satranç tahtası olan kareli bir yüzeyin üzerinde havada duran üç zarın yer aldığı siyah beyaz bir fotoğraftır. Zarlar hareket halindeyken yakalanmış olup, bir tanesi beş numarasını belirgin bir şekilde göstermektedir. Arka plan karanlıktır ve zarların üzerinde üçgen bir şekil oluşturan hafif bir ışık huzmesi, kompozisyona dramatik bir etki katmaktadır.
```

## Ses Desteği

OpenAI, ses önizleme modellerini (audio-preview models) kullanarak ses giriş ve çıkışları için beta desteğine sahiptir.

Bu modelleri kullanırken, `modalities` parametresini kullanarak çıktı modalitesini (metin veya ses) yapılandırabilirsiniz. Çıktı ses yapılandırması `audio_config` parametresi kullanılarak da ayarlanabilir. Daha fazla bilgi için [OpenAI dokümanlarına](https://platform.openai.com/docs/guides/audio) bakın.

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI




llm = OpenAI(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio_config={"voice": "alloy", "format": "wav"},
)


messages = [
    ChatMessage(role="user", content="Merhaba! Benim adım Logan."),
]


resp = llm.chat(messages)
```

```python
import base64
from IPython.display import Audio


Audio(base64.b64decode(resp.message.blocks[0].audio), rate=16000)
```

[Tarayıcınız ses öğesini desteklemiyor.]

```python
# Yanıtı sohbet geçmişine ekle ve kullanıcının adını sor
messages.append(resp.message)
messages.append(ChatMessage(role="user", content="Adım ne?"))


resp = llm.chat(messages)
Audio(base64.b64decode(resp.message.blocks[0].audio), rate=16000)
```

[Tarayıcınız ses öğesini desteklemiyor.]

Sesi girdi olarak da kullanabilir ve sesin açıklamalarını veya transkripsiyonlarını alabiliriz.

```python
!wget AUDIO_URL = "https://science.nasa.gov/wp-content/uploads/2024/04/sounds-of-mars-one-small-step-earth.wav" -O audio.wav
```

```python
from llama_index.core.llms import ChatMessage, AudioBlock, TextBlock


messages = [
    ChatMessage(
        role="user",
        blocks=[
            AudioBlock(path="audio.wav", format="wav"),
            TextBlock(
                text="Sesi birkaç cümleyle tanımla. Nereden geliyor?"
            ),
        ],
    )
]


llm = OpenAI(
    model="gpt-4o-audio-preview",
    modalities=["text"],
)


resp = llm.chat(messages)
print(resp)
```

```python
assistant: Ses, 1964 yılında Apollo 11 ay inişi sırasında astronot Neil Armstrong'un ünlü bir sözüdür. Ay yüzeyine adım atan ilk insan olduğunda, "Bu bir insan için küçük bir adım, insanlık için dev bir sıçrama" dedi. Bu an, uzay araştırmalarında ve insanlık tarihinde önemli bir başarıya işaret ediyordu.
```

## Fonksiyon/Araç Çağırma (Function/Tool Calling) Kullanımı

OpenAI modelleri, fonksiyon çağırma için yerel desteğe sahiptir. Bu, LlamaIndex araç soyutlamalarıyla (tool abstractions) kolayca entegre olur ve LLM'ye herhangi bir Python fonksiyonunu bağlamanıza olanak tanır.

Aşağıdaki örnekte, bir `Song` nesnesi oluşturmak için bir fonksiyon tanımlıyoruz.

```python
from pydantic import BaseModel
from llama_index.core.tools import FunctionTool




class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""


    name: str
    artist: str




def generate_song(name: str, artist: str) -> Song:
    """Verilen isim ve sanatçı ile bir şarkı oluşturur."""
    return Song(name=name, artist=artist)




tool = FunctionTool.from_defaults(fn=generate_song)
```

`strict` parametresi, araç çağrıları/yapılandırılmış çıktılar oluştururken OpenAI'nin kısıtlı örnekleme (constrained sampling) kullanıp kullanmayacağını belirler. Bu, oluşturulan araç çağrısı şemasının her zaman beklenen alanları içereceği anlamına gelir.

Bu durum gecikmeyi (latency) artırdığı için varsayılan olarak yanlıştır (false).

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-4o-mini", strict=True)
response = llm.predict_and_call(
    [tool],
    "Benim için rastgele bir şarkı seç",
    # sınıfı geçersiz kılmak için fonksiyon düzeyinde de ayarlanabilir
)
print(str(response))
```

```python
name='Random Vibes' artist='DJ Chill'
```

Ayrıca birden fazla fonksiyon çağırma işlemi de yapabiliriz.

```python
llm = OpenAI(model="gpt-3.5-turbo")
response = llm.predict_and_call(
    [tool],
    "Beatles'tan beş şarkı oluşturun",
    allow_parallel_tool_calls=True,
)
for s in response.sources:
    print(f"Ad: {s.tool_name}, Girdi: {s.raw_input}, Çıktı: {str(s)}")
```

```python
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Hey Jude', 'artist': 'The Beatles'}}, Çıktı: name='Hey Jude' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Let It Be', 'artist': 'The Beatles'}}, Çıktı: name='Let It Be' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Yesterday', 'artist': 'The Beatles'}}, Çıktı: name='Yesterday' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Come Together', 'artist': 'The Beatles'}}, Çıktı: name='Come Together' artist='The Beatles'
Ad: generate_song, Girdi: {'args': (), 'kwargs': {'name': 'Help!', 'artist': 'The Beatles'}}, Çıktı: name='Help!' artist='The Beatles'
```

### Manuel Araç Çağırma

Bir aracın nasıl çağrılacağını kontrol etmek istiyorsanız, araç çağırma ve araç seçme işlemlerini kendi adımlarına bölebilirsiniz.

İlk olarak, bir araç seçelim.

```python
from llama_index.core.llms import ChatMessage


chat_history = [ChatMessage(role="user", content="Benim için rastgele bir şarkı seç")]


resp = llm.chat_with_tools([tool], chat_history=chat_history)
```

Şimdi, LLM'nin seçtiği aracı (varsa) çağıralım.

Eğer bir araç çağrısı varsa, nihai yanıtı (veya başka bir araç çağrısını!) oluşturmak için sonuçları LLM'ye göndermeliyiz.

```python
tools_by_name = {t.metadata.name: t for t in [tool]}
tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)


while tool_calls:
    # LLM'nin yanıtını sohbet geçmişine ekle
    chat_history.append(resp.message)


    for tool_call in tool_calls:
        tool_name = tool_call.tool_name
        tool_kwargs = tool_call.tool_kwargs


        print(f"{tool_name} {tool_kwargs} ile çağrılıyor")
        tool_output = tool(**tool_kwargs)
        chat_history.append(
            ChatMessage(
                role="tool",
                content=str(tool_output),
                # OpenAI gibi çoğu LLM'nin araç çağrı kimliğini (tool call id) bilmesi gerekir
                additional_kwargs={"tool_call_id": tool_call.tool_id},
            )
        )


        resp = llm.chat_with_tools([tool], chat_history=chat_history)
        tool_calls = llm.get_tool_calls_from_response(
            resp, error_on_no_tool_call=False
        )
```

```python
generate_song {'name': 'Random Vibes', 'artist': 'DJ Chill'} ile çağrılıyor
```

Artık nihai bir yanıtımız olmalı!

```python
print(resp.message.content)
```

```python
İşte senin için rastgele bir şarkı: **DJ Chill**'den **"Random Vibes"**. Keyfini çıkar!
```

## Yapılandırılmış Tahmin (Structured Prediction)

Fonksiyon çağırmanın önemli bir kullanım durumu da yapılandırılmış nesnelerin çıkarılmasıdır. LlamaIndex, herhangi bir LLM'yi yapılandırılmış bir LLM'ye dönüştürmek için sezgisel bir arayüz sağlar - sadece hedef Pydantic sınıfını tanımlayın (iç içe olabilir) ve bir istem verildiğinde istediğiniz nesneyi dışarı çıkaralım.

```python
from llama_index.llms.openai import OpenAI
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




llm = OpenAI(model="gpt-3.5-turbo")
prompt_tmpl = PromptTemplate(
    "Verilen bir şehirde bir restoran oluşturun {city_name}"
)
# Seçenek 1: `as_structured_llm` kullanın
restaurant_obj = (
    llm.as_structured_llm(Restaurant)
    .complete(prompt_tmpl.format(city_name="Dallas"))
    .raw
)
# Seçenek 2: `structured_predict` kullanın
# restaurant_obj = llm.structured_predict(Restaurant, prompt_tmpl, city_name="Miami")
```

```python
restaurant_obj
```

```python
Restaurant(name='Tasty Bites', city='Dallas', cuisine='Italian', menu_items=[MenuItem(course_name='Appetizer', is_vegetarian=True), MenuItem(course_name='Main Course', is_vegetarian=False), MenuItem(course_name='Dessert', is_vegetarian=True)])
```

#### Akış (Streaming) ile Yapılandırılmış Tahmin

`as_structured_llm` ile sarmalanmış herhangi bir LLM, `stream_chat` aracılığıyla akışı destekler.

```python
from llama_index.core.llms import ChatMessage
from IPython.display import clear_output
from pprint import pprint


input_msg = ChatMessage.from_str("Boston'da bir restoran oluşturun")


sllm = llm.as_structured_llm(Restaurant)
stream_output = sllm.stream_chat([input_msg])
for partial_output in stream_output:
    clear_output(wait=True)
    pprint(partial_output.raw.dict())
    restaurant_obj = partial_output.raw


restaurant_obj
```

```python
{'city': 'Boston',
 'cuisine': 'American',
 'menu_items': [{'course_name': 'Appetizer', 'is_vegetarian': True},
                {'course_name': 'Main Course', 'is_vegetarian': False},
                {'course_name': 'Dessert', 'is_vegetarian': True}],
 'name': 'Boston Bites'}










Restaurant(name='Boston Bites', city='Boston', cuisine='American', menu_items=[MenuItem(course_name='Appetizer', is_vegetarian=True), MenuItem(course_name='Main Course', is_vegetarian=False), MenuItem(course_name='Dessert', is_vegetarian=True)])
```

## Asenkron (Async)

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo")
```

```python
resp = await llm.acomplete("Paul Graham kimdir? ")
```

```python
print(resp)
```

```python
bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. En çok startup hızlandırıcısı Y Combinator'ı ortaklaşa kurması ve teknoloji, startup'lar ve girişimcilikle ilgili konularda bir denemeci ve yazar olarak yaptığı çalışmalarla tanınır. Graham aynı zamanda, 1998 yılında Yahoo tarafından satın alınan ilk web tabanlı uygulamalardan biri olan Viaweb'in de kurucu ortağıdır. Uzun yıllardır teknoloji endüstrisinde öne çıkan bir figürdür ve çok çeşitli konulardaki anlayışlı ve düşündürücü yazılarıyla tanınır.
```

```python
resp = await llm.astream_complete("Paul Graham kimdir? ")
```

```python
async for delta in resp:
    print(delta.delta, end="")
```

```python
Paul Graham bir girişimci, risk sermayedarı ve bilgisayar bilimcisidir. En çok startup dünyasındaki çalışmalarıyla, hızlandırıcı Y Combinator'ı ortaklaşa kurması ve Airbnb, Dropbox ve Stripe gibi birçok başarılı startup'a yatırım yapmasıyla tanınır. Aynı zamanda startup'lar, programlama ve teknoloji gibi konularda çeşitli kitaplar kaleme almış üretken bir yazardır.
```

Asenkron fonksiyon çağırma da desteklenmektedir.

```python
llm = OpenAI(model="gpt-3.5-turbo")
response = await llm.apredict_and_call([tool], "Bir şarkı oluşturun")
print(str(response))
```

```python
name='Sunshine' artist='John Smith'
```

## Örnek düzeyinde API Anahtarı Ayarlama

İsterseniz, ayrı LLM örneklerinin ayrı API anahtarları kullanmasını sağlayabilirsiniz.

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo", api_key="GEÇERSİZ_ANAHTAR")
resp = llm.complete("Paul Graham kimdir? ")
print(resp)
```

```python
bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. En çok startup hızlandırıcısı Y Combinator'ın kurucu ortağı olarak tanınır. Graham ayrıca startup'lar ve girişimcilik üzerine, teknoloji endüstrisinde geniş bir takipçi kitlesi kazanan birkaç etkili makale yazmıştır. Reddit, Dropbox ve Airbnb dahil olmak üzere çok sayıda başarılı startup'ın kurulmasında ve finansmanında yer almıştır. Graham, eğitim, eşitsizlik ve teknolojinin geleceği gibi çeşitli konulardaki anlayışlı ve genellikle ## LlamaCloud ile RAG

LlamaCloud, belgeleri yüklemenize, ayrıştırmanıza (parse) ve dizinlemenize (index) ve ardından bunları LlamaIndex kullanarak aramanıza olanak tanıyan bulut tabanlı hizmetimizdir. LlamaCloud şu anda özel bir alfa aşamasındadır; tasarım ortağı olarak değerlendirilmek isterseniz lütfen [iletişime geçin](https://docs.google.com/forms/d/e/1FAIpQLSdehUJJB4NIYfrPIKoFdF4j8kyfnLhMSH_qYJI_WGQbDWD25A/viewform).

### Kurulum

```python
%pip install llama-cloud-services
```

### OpenAI ve LlamaCloud API Anahtarlarını Ayarlama

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."


os.environ["LLAMA_CLOUD_API_KEY"] = "llx-..."
```

```python
from llama_cloud.client import LlamaCloud


client = LlamaCloud(token=os.environ["LLAMA_CLOUD_API_KEY"])
```

### Bir Boru Hattı (Pipeline) Oluşturun.

Boru hatları, verileri içine çekebileceğiniz boş bir dizindir.

Verileri çekerken kullanılacak dönüşüm (transformation) ve gömme (embedding) yapılandırmasını ayarlamanız gerekir.

```python
# Gömme (Embedding) yapılandırması
embedding_config = {
    "type": "OPENAI_EMBEDDING",
    "component": {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model_name": "text-embedding-ada-002",  # Herhangi bir OpenAI Gömme modelini seçebilirsiniz
    },
}


# Dönüşüm (Transformation) otomatik yapılandırması
transform_config = {
    "mode": "auto",
    "config": {
        "chunk_size": 1024,  # düzenlenebilir
        "chunk_overlap": 20,  # düzenlenebilir
    },
}


pipeline = {
    "name": "openai-rag-pipeline",  # Gerekirse ismi değiştirin
    "embedding_config": embedding_config,
    "transform_config": transform_config,
    "data_sink_id": None,
}


pipeline = client.pipelines.upsert_pipeline(request=pipeline)
```

### Dosya Yükleme

Dosyaları yükleyeceğiz ve dizine ekleyeceğiz.

```python
with open("../data/10k/uber_2021.pdf", "rb") as f:
    file = client.files.upload_file(upload_file=f)
```

```python
files = [{"file_id": file.id}]


pipeline_files = client.pipelines.add_files_to_pipeline(
    pipeline.id, request=files
)
```

### Veri Çekme (Ingestion) İş Durumunu Kontrol Etme

```python
jobs = client.pipelines.list_pipeline_jobs(pipeline.id)


jobs[0].status
```

```python
<ManagedIngestionStatus.SUCCESS: 'SUCCESS'>
```

### Dizine Bağlanın.

Veri çekme işlemi tamamlandıktan sonra, [platform](https://cloud.llamaindex.ai/) üzerindeki dizininize gidin ve dizine bağlanmak için gerekli ayrıntıları alın.

```python
from llama_cloud_services import LlamaCloudIndex


index = LlamaCloudIndex(
    name="openai-rag-pipeline",
    project_name="Default",
    organization_id="YOUR ORG ID",
    api_key=os.environ["LLAMA_CLOUD_API_KEY"],
)
```

### Örnek Sorgu Üzerinde Test Edin

```python
query = "Uber'in 2021 yılındaki geliri ne kadardır?"
```

### Erişimci (Retriever)

Burada hibrit arama ve yeniden sıralayıcı (varsayılan olarak cohere re-ranker) kullanıyoruz.

```python
retriever = index.as_retriever(
    dense_similarity_top_k=3,
    sparse_similarity_top_k=3,
    alpha=0.5,
    enable_reranking=True,
)


retrieved_nodes = retriever.retrieve(query)
```

#### Erişilen düğümleri görüntüle

```python
from llama_index.core.response.notebook_utils import display_source_node


for retrieved_node in retrieved_nodes:
    display_source_node(retrieved_node, source_length=1000)
```

**Düğüm (Node) ID:** 6341cc9c-1d81-46d6-afa3-9c2490f79514\
**Benzerlik:** 0.99879813\
**Metin:** 2021 ile 2020 Karşılaştırması

Gelir, büyük ölçüde Brüt Rezervasyonlardaki %56'lık (sabit döviz bazında %53) artışa bağlı olarak 6,3 milyar dolar (%57) arttı. Brüt Rezervasyonlardaki artış, temel olarak COVID-19 ile ilgili evde kalma emri talebi sonucunda yemek teslimat siparişlerindeki artış ve daha büyük sepet boyutlarının yanı sıra ABD ve uluslararası pazarlardaki sürekli genişleme nedeniyle Teslimat Brüt Rezervasyonlarındaki %71'lik (sabit döviz bazında %66) artıştan kaynaklandı. Artış aynı zamanda, işletmenin COVID-19 etkilerinden kurtulmasıyla Seyahat hacimlerindeki artış nedeniyle Mobilite Brüt Rezervasyonlarındaki %38'lik (sabit döviz bazında %36) büyümeden de kaynaklandı. Ek olarak, teslimat hizmetlerinden birincil derecede sorumlu olduğumuz ve sağlanan hizmetler için Kuryelere ödeme yaptığımız, satış maliyetine kaydedilen belirli Kurye ödemeleri ve teşviklerindeki artıştan kaynaklanan Teslimat gelirinde bir artış gördük.

**Düğüm (Node) ID:** e022d492-0fe0-4988-979e-dc5de9eeaf2d\
**Benzerlik:** 0.996597\
**Metin:** 2021 Önemli Gelişmeler

Toplam Brüt Rezervasyonlar, 2020 yılına kıyasla 2021'de 32,5 milyar dolar artarak %56 (sabit döviz bazında %53) yükseldi. Teslimat Brüt Rezervasyonları, COVID-19 ile ilgili evde kalma emri talebi sonucunda yemek teslimat siparişlerindeki artış ve daha büyük sepet boyutlarının yanı sıra ABD ve uluslararası pazarlardaki sürekli genişleme nedeniyle 2020'ye göre %66 (sabit döviz bazında) büyüdü. Ek olarak, teslimat hizmetlerinden birincil derecede sorumlu olduğumuz ve sağlanan hizmetler için Kuryelere ödeme yaptığımız, satış maliyetine kaydedilen belirli Kurye ödemeleri ve teşviklerindeki artıştan kaynaklanan Teslimat gelirinde bir artış gördük. Mobilite Brüt Rezervasyonları, işletmenin COVID-19 etkilerinden kurtulmasıyla Seyahat hacimlerindeki artış nedeniyle 2020'ye göre %36 (sabit döviz bazında) büyüdü.

Gelir 17,5 milyar dolardı (yıllık %57 artış), bu da Teslimat işimizdeki genel büyümeyi ve Navlun gelirindeki artışı yansıtıyor…

**Düğüm (Node) ID:** 00d31b26-b734-4475-b47a-8cb839ff65e0\
**Benzerlik:** 0.9962638\
**Metin:** 2021 ile 2020 Karşılaştırması

Amortisman ve itfa payları hariç satış maliyeti, esas olarak belirli pazarlardaki Kurye ödemeleri ve teşviklerindeki 2,1 milyar dolarlık artış, Teslimat işimizde kat edilen millerdeki artıştan kaynaklanan sigorta giderindeki 660 milyon dolarlık artış ve Navlun taşıyıcı ödemelerindeki 873 milyon dolarlık artış nedeniyle 4,2 milyar dolar (%81) arttı. ---

#### Sorgu Motoru (Query Engine)

Tüm RAG iş akışını kurmak için QueryEngine.

```python
query_engine = index.as_query_engine(
    dense_similarity_top_k=3,
    sparse_similarity_top_k=3,
    alpha=0.5,
    enable_reranking=True,
)
```

#### Yanıt

```python
response = query_engine.query(query)


print(response)
```

```python
Uber'in 2021 yılındaki geliri 17,5 milyar dolardı.
```
