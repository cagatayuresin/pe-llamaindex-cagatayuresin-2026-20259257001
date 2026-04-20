# Sohbet Robotu (Chatbot) Nasıl Oluşturulur

LlamaIndex, verileriniz ile Büyük Dil Modelleri (LLM'ler) arasında bir köprü görevi görerek soru-cevap ve özetleme gibi çeşitli görevler için verileriniz etrafında bir sorgu arayüzü kurmanıza olanak tanıyan bir araç seti sunar.

Bu eğitimde, bir [Veri Ajanı (Data Agent)](https://gpt-index.readthedocs.io/en/stable/core_modules/agent_modules/agents/root.html) kullanarak bağlamla zenginleştirilmiş (context-augmented) bir sohbet robotu oluşturma sürecinde size rehberlik edeceğiz. LLM'ler tarafından desteklenen bu ajan, verileriniz üzerinde akıllıca görevler yürütme yeteneğine sahiptir. Sonuç, verileriniz hakkındaki sorguları yanıtlamak için LlamaIndex tarafından sağlanan sağlam bir veri arayüzü araçları setiyle donatılmış bir sohbet robotu ajanı olacaktır.

**Not**: Bu eğitim, SEC 10-K dosyaları üzerinde bir sorgu arayüzü oluşturmaya yönelik ilk çalışmalara dayanmaktadır - [buradan inceleyebilirsiniz](https://medium.com/@jerryjliu98/how-unstructured-and-llamaindex-can-help-bring-the-power-of-llms-to-your-own-data-3657d063e30d).

### Bağlam

Bu kılavuzda, Dropbox'tan alınan ham UBER 10-K HTML dosyalarını kullanan bir "10-K Sohbet Robotu" inşa edeceğiz. Kullanıcılar, 10-K dosyalarıyla ilgili sorular sormak için sohbet robotuyla etkileşime girebilirler.

### Hazırlık

```python
import os
import openai

os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = os.environ["OPENAI_API_KEY"]

import nest_asyncio

nest_asyncio.apply()
```

### Verileri İçeri Alma (Ingest Data)

Öncelikle 2019-2022 yıllarına ait ham 10-K dosyalarını indirelim.

```bash
# NOT: Kod örnekleri bir Jupyter notebook içinde çalıştığınızı varsayar.
# dosyaları indir
!mkdir data
!wget "https://www.dropbox.com/s/948jr9cfs7fgj99/UBER.zip?dl=1" -O data/UBER.zip
!unzip data/UBER.zip -d data
```

HTML dosyalarını formatlanmış metne dönüştürmek için [Unstructured](https://github.com/Unstructured-IO/unstructured) kütüphanesini kullanıyoruz. [LlamaHub](https://llamahub.ai/) sayesinde Unstructured ile doğrudan entegre olabiliriz; bu da herhangi bir metnin LlamaIndex'in kabul edebileceği bir `Document` (Döküman) formatına dönüştürülmesine olanak tanır.

Önce gerekli paketleri yüklüyoruz:

```bash
!pip install llama-hub unstructured
```

Ardından HTML dosyalarını bir `Document` nesneleri listesine dönüştürmek için `UnstructuredReader`'ı kullanabiliriz.

```python
from llama_index.readers.file import UnstructuredReader
from pathlib import Path

years = [2022, 2021, 2020, 2019]

loader = UnstructuredReader()
doc_set = {}
all_docs = []
for year in years:
    year_docs = loader.load_data(
        file=Path(f"./data/UBER/UBER_{year}.html"), split_documents=False
    )
    # her yıla ait dökümana yıl meta verisini ekle
    for d in year_docs:
        d.metadata = {"year": year}
    doc_set[year] = year_docs
    all_docs.extend(year_docs)
```

### Her Yıl İçin Vektör İndekslerinin Kurulması

İlk olarak her yıl için bir vektör indeksi kuruyoruz. Her vektör indeksi, belirli bir yıla ait 10-K dosyası hakkında sorular sormamıza olanak tanır.

Her indeksi oluşturuyoruz ve diske kaydediyoruz.

```python
# basit vektör indekslerini başlat
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings

Settings.chunk_size = 512
index_set = {}
for year in years:
    storage_context = StorageContext.from_defaults()
    cur_index = VectorStoreIndex.from_documents(
        doc_set[year],
        storage_context=storage_context,
    )
    index_set[year] = cur_index
    storage_context.persist(persist_dir=f"./storage/{year}")
```

Bir indeksi diskten yüklemek için aşağıdakileri yapın:

```python
# İndeksleri diskten yükle
from llama_index.core import load_index_from_storage

index_set = {}
for year in years:
    storage_context = StorageContext.from_defaults(
        persist_dir=f"./storage/{year}"
    )
    cur_index = load_index_from_storage(
        storage_context,
    )
    index_set[year] = cur_index
```

### 10-K Dosyaları Arasında Cevapları Sentezlemek İçin Bir Alt Soru Sorgu Motoru (Sub Question Query Engine) Kurma

4 yıla ait dökümanlara erişimimiz olduğu için sadece belirli bir yılın 10-K dökümanıyla ilgili sorular sormak değil, aynı zamanda tüm 10-K dosyaları üzerinden analiz gerektiren sorular da sormak isteyebiliriz.

Bunu çözmek için bir [Alt Soru Sorgu Motoru (Sub Question Query Engine)](https://gpt-index.readthedocs.io/en/stable/examples/query_engine/sub_question_query_engine.html) kullanabiliriz. Bir sorguyu, her biri ayrı bir vektör indeksi tarafından yanıtlanan alt sorgulara ayırır ve genel sorguyu yanıtlamak için sonuçları sentezler.

LlamaIndex, indekslerin (ve sorgu motorlarının) sorgu motorları ve ajanlar tarafından kullanılabilmesi için bazı sarmalayıcılar sağlar. Öncelikle her vektör indeksi için bir `QueryEngineTool` tanımlıyoruz. Her aracın bir adı ve açıklaması vardır; bunlar, LLM ajanının hangi aracı seçeceğine karar vermek için gördüğü bilgilerdir.

```python
from llama_index.core.tools import QueryEngineTool, ToolMetadata

individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=index_set[year].as_query_engine(),
        metadata=ToolMetadata(
            name=f"vector_index_{year}",
            description=f"Uber için {year} yılı SEC 10-K dosyası hakkındaki sorguları yanıtlamak istediğinizde yararlıdır",
        ),
    )
    for year in years
]
```

Şimdi 10-K dosyaları arasında cevapları sentezlememize olanak tanıyan Alt Soru Sorgu Motorunu oluşturabiliriz. Yukarıda tanımladığımız `individual_query_engine_tools` listesini ve alt sorguları çalıştırmak için kullanılacak bir `llm` geçiyoruz.

```python
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import SubQuestionQueryEngine

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=individual_query_engine_tools,
    llm=OpenAI(model="gpt-3.5-turbo"),
)
```

### Sohbet Robotu Ajanını Kurma

Dış sohbet robotu ajanını kurmak için bir dizi Araç'a (Tools) erişimi olan bir LlamaIndex Veri Ajanı kullanıyoruz. Özellikle, OpenAI API fonksiyon çağırma özelliğinden yararlanan bir `FunctionAgent` kullanacağız. Her bir indeks için (belirli bir yıla karşılık gelen) önceden tanımladığımız ayrı Araçları ve yukarıda tanımladığımız alt soru sorgu motoru için bir aracı kullanmak istiyoruz.

Öncelikle alt soru sorgu motoru için bir `QueryEngineTool` tanımlıyoruz:

```python
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="sub_question_query_engine",
        description="Uber için birden fazla SEC 10-K dökümanının analiz edilmesini gerektiren sorguları yanıtlamak istediğinizde yararlıdır",
    ),
)
```

Ardından, yukarıda tanımladığımız Araçları ajan için tek bir araç listesinde birleştiriyoruz:

```python
tools = individual_query_engine_tools + [query_engine_tool]
```

Son olarak, yukarıda tanımladığımız araç listesini geçerek ajanı oluşturmak için `FunctionAgent()` fonksiyonunu çağırıyoruz.

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

agent = FunctionAgent(tools=tools, llm=OpenAI(model="gpt-4.1"))
```

### Ajanı Test Etme

Artık ajanı çeşitli sorgularla test edebiliriz.

Basit bir "merhaba" sorgusu ile test edersek, ajan hiçbir Araç kullanmaz.

```python
response = await agent.run("merhaba, ben bob")
print(str(response))
```

```text
Merhaba Bob! Bugün size nasıl yardımcı olabilirim?
```

Belirli bir yılın 10-K dosyasıyla ilgili bir sorgu ile test edersek, ajan ilgili vektör indeksi Aracını kullanacaktır.

```python
response = await agent.run(
    "2020 yılında Uber için en büyük risk faktörlerinden bazıları nelerdi?"
)
print(str(response))
```

```text
2020 yılında Uber için en büyük risk faktörlerinden bazıları şunlardı:

1. COVID-19 pandemisinin olumsuz etkisi ve bunu hafifletmek için iş dünyasında alınan önlemler.
2. Sürücülerin bağımsız yükleniciler yerine çalışanlar, işçiler veya yarı çalışanlar olarak potansiyel yeniden sınıflandırılması.
3. Mobilite, teslimat ve lojistik sektörlerinde düşük maliyetli alternatifler ve iyi finanse edilmiş rakiplerle yoğun rekabet.
4. Rekabetçi kalabilmek için ücretleri veya hizmet bedellerini düşürme, sürücü teşvikleri ve tüketici indirimleri sunma ihtiyacı.
5. Oluşan önemli zararlar ve karlılığa ulaşma konusundaki belirsizlik.
6. Platform kullanıcılarının kritik kütlesini çekememe veya koruyamama riski.
7. İş yeri kültürü ve ileri görüşlü yaklaşımla ilgili operasyonel, uyumluluk ve kültürel zorluklar.
8. Uluslararası yatırımların potansiyel olumsuz etkisi ve yabancı ülkelerde iş yapmanın zorlukları.
9. Operasyonel ve uyumluluk zorlukları, yerelleştirme, yasalar ve düzenlemeler, rekabet, sosyal kabul, teknolojik uyumluluk, uygunsuz iş uygulamaları, sorumluluk belirsizliği, uluslararası operasyonları yönetme, para birimi dalgalanmaları, nakit işlemler, vergi sonuçları ve ödeme dolandırıcılığı ile ilgili riskler.

Bu risk faktörleri Uber'in 2020 yılında karşılaştığı zorlukları ve belirsizlikleri vurgulamaktadır.
```

Son olarak, yıllar arasındaki risk faktörlerini karşılaştırmak/karşıtlaştırmak için bir sorgu ile test edersek, ajan Alt Soru Sorgu Motoru Aracını kullanacaktır.

```python
cross_query_str = "Uber 10-K raporlarında açıklanan risk faktörlerini yıllar itibarıyla karşılaştırın/karşıtlaştırın. Cevabı madde işaretleri halinde verin."

response = await agent.run(cross_query_str)
print(str(response))
```

```text
İşte yıllar itibarıyla Uber 10-K raporlarında açıklanan risk faktörlerinin bir karşılaştırması:

2022 Risk Faktörleri:
- Sürücülerin bağımsız yükleniciler yerine çalışan olarak sınıflandırılmasının potansiyel olumsuz etkisi.
- Mobilite, teslimat ve lojistik sektörlerinin son derece rekabetçi doğası.
- Rekabetçi kalabilmek için ücretleri veya hizmet bedellerini düşürme ihtiyacı.
- Önemli zarar geçmişi ve artan işletme giderleri beklentisi.
- Gelecekteki pandemilerin veya hastalık salgınlarının iş ve finansal sonuçlar üzerindeki etkisi.
- Ekonomik koşulların ve bunların isteğe bağlı tüketici harcamaları üzerindeki etkisinin iş dünyasına verebileceği potansiyel zarar.

2021 Risk Faktörleri:
- COVID-19 pandemisinin olumsuz etkisi ve bunu hafifletmek için iş dünyasında alınan önlemler.
- Sürücülerin bağımsız yükleniciler yerine çalışan olarak potansiyel yeniden sınıflandırılması.
- Mobilite, teslimat ve lojistik sektörlerinin son derece rekabetçi doğası.
- Rekabetçi kalabilmek için ücretleri veya hizmet bedellerini düşürme ve teşvikler sunma ihtiyacı.
- Önemli zarar geçmişi ve karlılığa ulaşma konusundaki belirsizlik.
- Platform kullanıcılarının kritik kütlesini çekmenin ve korumanın önemi.

2020 Risk Faktörleri:
- COVID-19 pandemisinin iş üzerindeki olumsuz etkisi.
- Sürücülerin çalışan olarak potansiyel yeniden sınıflandırılması.
- Mobilite, teslimat ve lojistik sektörlerinin son derece rekabetçi doğası.
- Rekabetçi kalabilmek için ücretleri veya hizmet bedellerini düşürme ihtiyacı.
- Önemli zarar geçmişi ve potansiyel gelecek harcamaları.
- Platform kullanıcılarının kritik kütlesini çekmenin ve korumanın önemi.
- Şirketin karşılaştığı operasyonel ve kültürel zorluklar.

2019 Risk Faktörleri:
- Yerel şirketlerle rekabet.
- Farklı sosyal kabul düzeyleri.
- Teknolojik uyumluluk sorunları.
- Uygunsuz iş uygulamalarına maruz kalma.
- Yasal belirsizlik.
- Uluslararası operasyonları yönetmedeki zorluklar.
- Döviz kurlarındaki dalgalanmalar.
- Yerel para birimlerini düzenleyen yasalar.
- Vergi sonuçları.
- Finansal muhasebe yükleri.
- Finansal sistemleri uygulamadaki zorluklar.
- İthalat ve ihracat kısıtlamaları.
- Siyasi ve ekonomik istikrarsızlık.
- Halk sağlığı endişeleri.
- Fikri mülkiyet hakları için azaltılmış koruma.
- Azınlık hissesine sahip olunan iştirakler üzerindeki sınırlı etki.
- Düzenleyici karmaşıklıklar.

Bu karşılaştırmalar, Uber'in farklı yıllarda karşılaştığı hem ortak hem de benzersiz risk faktörlerini vurgulamaktadır.
```

### Sohbet Robotu Döngüsünü Kurma

Artık sohbet robotu kurulumuna sahip olduğumuza göre, SEC dökümanlarıyla zenginleştirilmiş sohbet robotumuzla sohbet etmek için temel bir etkileşimli döngü kurmak sadece birkaç adım daha gerektirir!

```python
agent = FunctionAgent(tools=tools, llm=OpenAI(model="gpt-4.1"))

while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    response = await agent.run(text_input)
    print(f"Agent: {response}")
```

İşte döngünün çalışırken bir örneği:

```text
User:  2022'de Uber'e karşı açılan bazı yasal işlemler nelerdi?
Agent: 2022'de Uber birkaç yasal işlemle karşı karşıya kaldı. Önemli olanlardan bazıları şunlardır:

1. Proposition 22'ye karşı dilekçe: Kaliforniya'da, uygulama tabanlı sürücüleri bağımsız yükleniciler olarak sınıflandıran Proposition 22'nin anayasaya aykırı olduğunu iddia eden bir dilekçe verildi.

2. Massachusetts Başsavcısı tarafından açılan dava: Massachusetts Başsavcısı, sürücülerin çalışan olarak sınıflandırılması ve ücret ile iş kanunları kapsamındaki korumalardan yararlanması gerektiğini iddia ederek Uber'e dava açtı.

3. New York Başsavcısı'nın iddiaları: New York Başsavcısı, sürücülerin yanlış sınıflandırılması ve ilgili istihdam ihlalleri konusunda Uber'e karşı iddialarda bulundu.

4. İsviçre sosyal güvenlik kararları: İsviçre sosyal güvenlik kararları Uber sürücülerini çalışan olarak sınıflandırdı ve bu durum Uber'in İsviçre'deki operasyonları için sonuçlar doğurabilir.

5. Avustralya'daki toplu davalar: Uber, şirketin taksi, kiralık araç ve limuzin sektörlerindeki katılımcılara zarar vermek için iş birliği yaptığı iddialarıyla Avustralya'da toplu davalarla karşı karşıya kaldı.

Bu yasal işlemlerin sonuçlarının belirsiz olduğunu ve değişebileceğini not etmek önemlidir.

User:
```

### Notebook

[İlgili notebook'umuza](/python/examples/agent/chatbot_sec) göz atın.