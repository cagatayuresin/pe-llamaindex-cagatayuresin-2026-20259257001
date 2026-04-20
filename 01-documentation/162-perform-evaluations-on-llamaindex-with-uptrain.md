# UpTrain ile LlamaIndex Üzerinde Değerlendirmeler Gerçekleştirme

**Genel Bakış**: Bu örnekte, UpTrain'in LlamaIndex ile nasıl kullanılacağını göreceğiz. UpTrain ([github](https://github.com/uptrain-ai/uptrain) || [web sitesi](https://github.com/uptrain-ai/uptrain/) || [dökümanlar](https://docs.uptrain.ai/)), GenAI uygulamalarını değerlendirmek ve iyileştirmek için açık kaynaklı bir platformdur. 20'den fazla önceden yapılandırılmış kontrol (dil, kod, embedding kullanım durumlarını kapsayan) için derecelendirmeler sağlar, hata durumlarında kök neden analizi yapar ve bunları nasıl çözeceğinize dair içgörüler sunar. UpTrain'in değerlendirmeleri hakkında daha fazla ayrıntı [burada](https://github.com/uptrain-ai/uptrain?tab=readme-ov-file#pre-built-evaluations-we-offer-) bulunabilir.

**Problem**: Giderek daha fazla şirket LLM prototiplerini üretime hazır uygulamalara dönüştürdükçe, RAG boru hatları (pipelines) da karmaşıklaşıyor. Geliştiriciler; RAG sistemlerinin doğruluğunu artırmak için `QueryRewrite`, `Context ReRank` gibi modüllerden yararlanıyor.

Artan karmaşıklıkla birlikte daha fazla hata noktası ortaya çıkıyor:

1. Bu yeni modüllerin kalitesini değerlendirmek ve sistemin doğruluğunu gerçekten artırıp artırmadıklarını belirlemek için **Gelişmiş Değerlendirmelere (Advanced Evals)** ihtiyaç vardır.
2. Farklı modülleri sistematik olarak test etmek ve veri odaklı kararlar almak için **sağlam bir deney çerçevesine (experimentation framework)** ihtiyaç vardır.

**Çözüm**: UpTrain her ikisi için de çözüm sunar:

1. UpTrain; üretilen yanıtın, erişilen bağlamın ve tüm ara adımların kalitesini değerlendirmek için bir dizi kontrol sağlar. İlgili kontroller şunlardır: `ContextRelevance` (Bağlam Uygunluğu), `SubQueryCompleteness` (Alt Sorgu Tamlığı), `ContextReranking` (Bağlam Yeniden Sıralama), `ContextConciseness` (Bağlam Özlüğü), `FactualAccuracy` (Olgusal Doğruluk), `ContextUtilization` (Bağlam Kullanımı), `ResponseCompleteness` (Yanıt Tamlığı), `ResponseConciseness` (Yanıt Özlüğü) vb.
2. UpTrain ayrıca farklı embedding modelleriyle deneyler yapmanıza olanak tanır ve farklı RAG yapılandırmalarını karşılaştırmak için bir `evaluate_experiments` yöntemine sahiptir.

# Nasıl Yapılır?

UpTrain'i LlamaIndex ile kullanmanın iki yolu vardır:

1. **UpTrain Geri Çağırma Yöneticisini (Callback Handler) Kullanmak**: Bu yöntem, UpTrain'i LlamaIndex ile sorunsuz bir şekilde entegre etmenize olanak tanır. Mevcut LlamaIndex boru hattınıza `UpTrainCallbackHandler` eklemeniz yeterlidir; RAG boru hattınızın tüm bileşenlerini değerlendirecektir. En kolay kullanım şekli olduğu ve minimum çabayla size paneller ve içgörüler sağladığı için önerilen yöntem budur.

2. **UpTrain'in EvalLlamaIndex Nesnesini Kullanmak**: Bu yöntem, üretilen yanıtlar üzerinde değerlendirmeler yapmak için UpTrain'i kullanmanıza olanak tanır. Sorgular için yanıtlar oluşturmak üzere `EvalLlamaIndex` nesnesini kullanabilir ve ardından yanıtlar üzerinde değerlendirmeler yapabilirsiniz. Bunun nasıl yapılacağına dair ayrıntılı bir eğitimi aşağıda bulabilirsiniz. Bu yöntem değerledirmeler üzerinde daha fazla esneklik ve kontrol sunar, ancak kurulumu ve kullanımı daha fazla çaba gerektirir.

# 1. UpTrain Geri Çağırma Yöneticisini (Callback Handler) Kullanmak <a href="https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/callbacks/UpTrainCallback.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab'da Aç"/></a>

Aşağıdaki üç gösterim, RAG boru hatlarınızın farklı bileşenlerini değerlendirmek için UpTrain Geri Çağırma Yöneticisini nasıl kullanabileceğinizi açıklamaktadır.

## 1. **RAG Sorgu Motoru Değerlendirmeleri**:

RAG sorgu motoru, bağlamın erişilmesinde ve yanıtların üretilmesinde kritik bir rol oynar. Performansını ve yanıt kalitesini sağlamak için aşağıdaki değerlendirmeleri yapıyoruz:

- **[Bağlam Uygunluğu (Context Relevance)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-relevance)**: Erişilen bağlamın kullanıcı sorgusunu cevaplamak için yeterli bilgiye sahip olup olmadığını belirler.
- **[Olgusal Doğruluk (Factual Accuracy)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/factual-accuracy)**: LLM'nin yanıtının erişilen bağlam aracılığıyla doğrulanıp doğrulanamayacağını değerlendirir.
- **[Yanıt Tamlığı (Response Completeness)](https://docs.uptrain.ai/predefined-evaluations/response-quality/response-completeness)**: Yanıtın, kullanıcı sorgusunu kapsamlı bir şekilde cevaplamak için gereken tüm bilgileri içerip içermediğini kontrol eder.

## 2. **Alt Soru Sorgu Üretimi Değerlendirmesi**:

`SubQuestionQueryGeneration` operatörü, bir soruyu alt sorulara böler ve her biri için bir RAG sorgu motoru kullanarak yanıtlar oluşturur. Doğruluğunu ölçmek için şunları kullanırız:

- **[Alt Sorgu Tamlığı (Sub Query Completeness)](https://docs.uptrain.ai/predefined-evaluations/query-quality/sub-query-completeness)**: Alt soruların orijinal sorguyu doğru ve kapsamlı bir şekilde kapsamasını sağlar.

## 3. **Yeniden Sıralama (Re-Ranking) Değerlendirmeleri**:

Yeniden sıralama, node'ların sorguyla olan uygunluklarına göre yeniden düzenlenmesini ve en üstteki node'ların seçilmesini içerir. Yeniden sıralamadan sonra döndürülen node sayısına göre farklı değerlendirmeler yapılır.

a. Aynı Sayıda Node

- **[Bağlam Yeniden Sıralama (Context Reranking)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-reranking)**: Yeniden sıralanan node'ların sırasının, orijinal sıraya göre sorguyla daha alakalı olup olmadığını kontrol eder.

b. Farklı Sayıda Node:

- **[Bağlam Özlüğü (Context Conciseness)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-conciseness)**: Azaltılmış node sayısının hala gerekli tüm bilgileri sağlayıp sağlamadığını inceler.

Bu değerlendirmeler toplu olarak RAG sorgu motorunun, `SubQuestionQueryGeneration` operatörünün ve LlamaIndex boru hattındaki yeniden sıralama işleminin sağlamlığını ve etkinliğini sağlar.

#### **Not:**

- Temel bir RAG sorgu motoru kullanarak değerlendirmeler yaptık; aynı değerlendirmeler gelişmiş RAG sorgu motoru kullanılarak da yapılabilir.
- Aynı durum Yeniden Sıralama değerlendirmeleri için de geçerlidir; `SentenceTransformerRerank` kullanarak değerlendirmeler yaptık, aynı değerlendirmeler diğer yeniden sıralayıcılar (re-rankers) kullanılarak da yapılabilir.

## Bağımlılıkları Kurun ve Kütüphaneleri İçe Aktarın

Not defteri bağımlılıklarını kurun.

```bash
%pip install llama-index-readers-web
%pip install llama-index-callbacks-uptrain
%pip install -q html2text llama-index pandas tqdm uptrain torch sentence-transformers
```

Kütüphaneleri içe aktarın.

```python
from getpass import getpass

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.callbacks import CallbackManager
from llama_index.callbacks.uptrain.base import UpTrainCallbackHandler
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.llms.openai import OpenAI

import os
```

## Kurulum (Setup)

UpTrain size şunları sağlar:

1. Gelişmiş detaylandırma (drill-down) ve filtreleme seçeneklerine sahip paneller
2. Başarısız durumlardaki içgörüler ve ortak konular
3. Üretim verilerinin gözlemlenebilirliği ve gerçek zamanlı izlenmesi
4. CI/CD boru hatlarınızla sorunsuz entegrasyon yoluyla regresyon testi

UpTrain kullanarak değerlendirme yapmak için aşağıdaki seçenekler arasından seçim yapabilirsiniz:

### 1. **UpTrain'in Açık Kaynak Yazılımı (OSS)**:

Modelinizi değerlendirmek için açık kaynaklı değerlendirme hizmetini kullanabilirsiniz. Bu durumda bir OpenAI API anahtarı sağlamanız gerekecektir. Anahtarınızı [buradan](https://platform.openai.com/account/api-keys) alabilirsiniz.

Değerlendirmelerinizi UpTrain panelinde görüntülemek için terminalinizde aşağıdaki komutları çalıştırarak kurulum yapmanız gerekecektir:

```bash
git clone https://github.com/uptrain-ai/uptrain
cd uptrain
bash run_uptrain.sh
```

Bu, UpTrain panelini yerel makinenizde başlatacaktır. Ona `http://localhost:3000/dashboard` adresinden erişebilirsiniz.

Parametreler:

-   key_type="openai"
-   api_key="OPENAI_API_ANAHTARI"
-   project_name="PROJE_ADI"

### 2. **UpTrain Yönetilen Hizmeti ve Panelleri**:

Alternatif olarak, modelinizi değerlendirmek için UpTrain'in yönetilen hizmetini kullanabilirsiniz. [Buradan](https://uptrain.ai/) ücretsiz bir UpTrain hesabı oluşturabilir ve ücretsiz deneme kredileri alabilirsiniz. Daha fazla deneme kredisi istiyorsanız, [UpTrain yöneticileriyle buradan bir görüşme ayarlayın](https://calendly.com/uptrain-sourabh/30min).

Yönetilen hizmeti kullanmanın avantajları:

1. Yerel makinenizde UpTrain panelini kurmanıza gerek yoktur.
2. API anahtarlarına ihtiyaç duymadan birçok LLM'ye erişim sağlar.

Değerlendirmeleri gerçekleştirdikten sonra bunları `https://dashboard.uptrain.ai/dashboard` adresindeki UpTrain panelinde görüntüleyebilirsiniz.

Parametreler:

-   key_type="uptrain"
-   api_key="UPTRAIN_API_ANAHTARI"
-   project_name="PROJE_ADI"

**Not:** `project_name`, yapılan değerlendirmelerin UpTrain panelinde görüneceği proje adı olacaktır.

## UpTrain Geri Çağırma Yöneticisini Oluşturun

```python
os.environ["OPENAI_API_KEY"] = getpass()

callback_handler = UpTrainCallbackHandler(
    key_type="openai",
    api_key=os.environ["OPENAI_API_KEY"],
    project_name="uptrain_llamaindex",
)

Settings.callback_manager = CallbackManager([callback_handler])
```

## Dökümanları Yükleyin ve Ayrıştırın

Paul Graham'ın "What I Worked On" (Neler Üzerinde Çalıştım) adlı makalesinden dökümanları yükleyin.

```python
documents = SimpleWebPageReader().load_data(
    [
        "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt"
    ]
)
```

Dökümanı node'lara ayrıştırın.

```python
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)
```

# 1. RAG Sorgu Motoru Değerlendirmesi

UpTrain geri çağırma yöneticisi, oluşturulduktan sonra sorguyu, bağlamı ve yanıtı otomatik olarak yakalayacak ve yanıt üzerinde aşağıdaki üç değerlendirmeyi _(0 ile 1 arası derecelendirilir)_ çalıştıracaktır:

- **[Bağlam Uygunluğu (Context Relevance)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-relevance)**: Erişilen bağlamın kullanıcı sorgusunu cevaplamak için yeterli bilgiye sahip olup olmadığını belirler.
- **[Olgusal Doğruluk (Factual Accuracy)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/factual-accuracy)**: LLM'nin yanıtının erişilen bağlam aracılığıyla doğrulanıp doğrulanamayacağını değerlendirir.
- **[Yanıt Tamlığı (Response Completeness)](https://docs.uptrain.ai/predefined-evaluations/response-quality/response-completeness)**: Yanıtın, kullanıcı sorgusunu kapsamlı bir şekilde cevaplamak için gereken tüm bilgileri içerip içermediğini kontrol eder.

```python
index = VectorStoreIndex.from_documents(
    documents,
)
query_engine = index.as_query_engine()

queries = [
    "Paul Graham büyürken ne yaptı?",
    "Paul Graham'ın annesi ne zaman ve nasıl öldü?",
    "Paul Graham'a göre YC hakkındaki en ayırt edici şey nedir?",
    "Paul Graham, Jessica Livingston ile ne zaman ve nasıl tanıştı?",
    "Bel nedir, ne zaman ve nerede yazılmıştır?",
]
for query in queries:
    response = query_engine.query(query)
```

    Soru: Paul Graham büyürken ne yaptı?
    Yanıt: Paul Graham kısa hikayeler yazdı ve 9. sınıfta Fortran'ın erken bir sürümünü kullanarak IBM 1401 üzerinde programlamaya başladı. Daha sonra babasını bir TRS-80 almaya ikna etti; burada basit oyunlar, roket yüksekliklerini tahmin eden bir program ve bir kelime işlemci yazdı.

    Bağlam Uygunluğu Puanı: 0.0
    Olgusal Doğruluk Puanı: 1.0
    Yanıt Tamlığı Puanı: 1.0


    Soru: Paul Graham'ın annesi ne zaman ve nasıl öldü?
    Yanıt: Paul Graham'ın annesi o 18 yaşındayken beyin tümöründen öldü.

    Bağlam Uygunluğu Puanı: 0.0
    Olgusal Doğruluk Puanı: 0.0
    Yanıt Tamlığı Puanı: 1.0


    Soru: Paul Graham'a göre YC hakkındaki en ayırt edici şey nedir?
    Yanıt: Paul Graham'a göre Y Combinator hakkındaki en ayırt edici şey, üzerinde ne çalışılacağına kendisinin karar vermesi yerine, problemlerin ona gelmesidir. Her 6 ayda bir, yeni bir girişim grubu kendi problemlerini getirir ve bunlar YC'nin çalışmasının odak noktası olur.

    Bağlam Uygunluğu Puanı: 0.0
    Olgusal Doğruluk Puanı: 0.5
    Yanıt Tamlığı Puanı: 1.0


    Soru: Paul Graham, Jessica Livingston ile ne zaman ve nasıl tanıştı?
    Yanıt: Paul Graham, Jessica Livingston ile Ekim 2003'te kendi evinde verdiği büyük bir partide tanıştı.

    Bağlam Uygunluğu Puanı: 1.0
    Olgusal Doğruluk Puanı: 0.5
    Yanıt Tamlığı Puanı: 1.0


    Soru: Bel nedir, ne zaman ve nerede yazılmıştır?
    Yanıt: Bel, Arc ile yazılmış yeni bir Lisp'tir. 26 Mart 2015'ten 12 Ekim 2019'a kadar olan 4 yıllık bir süre zarfında geliştirilmiştir. Bel üzerindeki çalışmaların çoğu, yazarın 2016 yazında taşındığı İngiltere'de yapılmıştır.

    Bağlam Uygunluğu Puanı: 1.0
    Olgusal Doğruluk Puanı: 1.0
    Yanıt Tamlığı Puanı: 1.0

İşte başarısız durumları nasıl filtreleyebileceğinizi, derinlemesine inceleyebileceğinizi ve başarısız durumlar hakkında nasıl içgörü edinebileceğinizi gösteren panel örneği:
![image-2.png](https://uptrain-assets.s3.ap-south-1.amazonaws.com/images/llamaindex/image-2.png)

# 2. Alt Soru Sorgu Motoru Değerlendirmesi

**Alt soru sorgu motoru (sub-question query engine)**, birden fazla veri kaynağı kullanarak karmaşık bir sorguyu yanıtlama sorununu çözmek için kullanılır. Önce karmaşık sorguyu her bir ilgili veri kaynağı için alt sorulara böler, ardından tüm ara yanıtları toplar ve nihai bir yanıt sentezler.

UpTrain geri çağırma yöneticisi, alt soruları ve oluşturulduktan sonra her birinin yanıtlarını otomatik olarak yakalayacak ve yanıt üzerinde şu üç değerlendirmeyi _(0 ile 1 arası derecelendirilir)_ çalıştıracaktır:

- **[Bağlam Uygunluğu (Context Relevance)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-relevance)**: Erişilen bağlamın kullanıcı sorgusunu cevaplamak için yeterli bilgiye sahip olup olmadığını belirler.
- **[Olgusal Doğruluk (Factual Accuracy)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/factual-accuracy)**: LLM'nin yanıtının erişilen bağlam aracılığıyla doğrulanıp doğrulanamayacağını değerlendirir.
- **[Yanıt Tamlığı (Response Completeness)](https://docs.uptrain.ai/predefined-evaluations/response-quality/response-completeness)**: Yanıtın, kullanıcı sorgusunu kapsamlı bir şekilde cevaplamak için gereken tüm bilgileri içerip içermediğini kontrol eder.

Yukarıdaki değerlendirmelere ek olarak, geri çağırma yöneticisi şu değerlendirmeyi de çalıştıracaktır:

- **[Alt Sorgu Tamlığı (Sub Query Completeness)](https://docs.uptrain.ai/predefined-evaluations/query-quality/sub-query-completeness)**: Alt soruların orijinal sorguyu doğru ve kapsamlı bir şekilde kapsamasını sağlar.

```python
# indeksi ve sorgu motorunu oluştur
vector_query_engine = VectorStoreIndex.from_documents(
    documents=documents,
    use_async=True,
).as_query_engine()

query_engine_tools = [
    QueryEngineTool(
        query_engine=vector_query_engine,
        metadata=ToolMetadata(
            name="documents",
            description="Paul Graham essay on What I Worked On",
        ),
    ),
]

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    use_async=True,
)

response = query_engine.query(
    "Paul Graham'ın hayatı YC öncesinde, sırasında ve sonrasında nasıl farklıydı?"
)
```

    3 alt soru oluşturuldu.
    [documents] Q: Paul Graham Y Combinator'dan önce ne üzerinde çalıştı?
    [documents] Q: Paul Graham Y Combinator sırasında ne üzerinde çalıştı?
    [documents] Q: Paul Graham Y Combinator'dan sonra ne üzerinde çalıştı?
    [documents] A: Paul Graham, Y Combinator'dan sonra Robert ve Trevor ile birlikte bir proje üzerinde çalıştı.
    [documents] A: Paul Graham, Y Combinator'dan önce meslektaşları Robert ve Trevor ile birlikte projeler üzerinde çalıştı.
    [documents] A: Paul Graham, Y Combinator'daki zamanı boyunca makaleler yazmak ve Y Combinator üzerinde çalışmakla meşgul oldu.


    Soru: Paul Graham Y Combinator'dan sonra ne üzerinde çalıştı?
    Yanıt: Paul Graham, Y Combinator'dan sonra Robert ve Trevor ile birlikte bir proje üzerinde çalıştı.

    Bağlam Uygunluğu Puanı: 0.0
    Olgusal Doğruluk Puanı: 1.0
    Yanıt Tamlığı Puanı: 0.5


    Soru: Paul Graham Y Combinator'dan önce ne üzerinde çalıştı?
    Yanıt: Paul Graham, Y Combinator'dan önce meslektaşları Robert ve Trevor ile birlikte projeler üzerinde çalıştı.

    Bağlam Uygunluğu Puanı: 0.0
    Olgusal Doğruluk Puanı: 1.0
    Yanıt Tamlığı Puanı: 0.5


    Soru: Paul Graham Y Combinator sırasında ne üzerinde çalıştı?
    Yanıt: Paul Graham, Y Combinator'daki zamanı boyunca makaleler yazmak ve Y Combinator üzerinde çalışmakla meşgul oldu.

    Bağlam Uygunluğu Puanı: 0.0
    Olgusal Doğruluk Puanı: 0.5
    Yanıt Tamlığı Puanı: 0.5


    Soru: Paul Graham'ın hayatı YC öncesinde, sırasında ve sonrasında nasıl farklıydı?
    Alt Sorgu Tamlığı Puanı: 1.0

İşte alt soruların puanlarını çubuk grafik formunda görselleştiren panel örneği:

![image.png](https://uptrain-assets.s3.ap-south-1.amazonaws.com/images/llamaindex/image.png)

# 3. Yeniden Sıralama (Re-ranking)

Yeniden sıralama, node'ların sorguyla olan uygunluklarına göre yeniden düzenlenmesi işlemidir. LlamaIndex tarafından sunulan birden fazla yeniden sıralama algoritması sınıfı vardır. Bu örnek için `SentenceTransformerRerank` kullandık.

Yeniden sıralayıcı, yeniden sıralamadan sonra döndürülecek olan en üstteki n node sayısını girmenize olanak tanır. Bu değer orijinal node sayısıyla aynı kalırsa, yeniden sıralayıcı sadece node'ları yeniden sıralar ve node sayısını değiştirmez. Aksi takdirde, node'ları yeniden sıralar ve en üstteki n node'u döndürür.

Yeniden sıralamadan sonra döndürülen node sayısına göre farklı değerlendirmeler gerçekleştireceğiz.

## 3a. Yeniden Sıralama (Aynı sayıda node ile)

Yeniden sıralamadan sonra döndürülen node sayısı orijinal node sayısıyla aynıysa, aşağıdaki değerlendirme gerçekleştirilecektir:

- **[Bağlam Yeniden Sıralama (Context Reranking)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-reranking)**: Yeniden sıralanan node'ların sırasının, orijinal sıraya göre sorguyla daha alakalı olup olmadığını kontrol eder.

```python
callback_handler = UpTrainCallbackHandler(
    key_type="openai",
    api_key=os.environ["OPENAI_API_KEY"],
    project_name_prefix="llama",
)
Settings.callback_manager = CallbackManager([callback_handler])

rerank_postprocessor = SentenceTransformerRerank(
    top_n=3,  # yeniden sıralamadan sonraki node sayısı
    keep_retrieval_score=True,
)

index = VectorStoreIndex.from_documents(
    documents=documents,
)

query_engine = index.as_query_engine(
    similarity_top_k=3,  # yeniden sıralamadan önceki node sayısı
    node_postprocessors=[rerank_postprocessor],
)

response = query_engine.query(
    "Sam Altman bu makalede ne yaptı?",
)
```

    Soru: Sam Altman bu makalede ne yaptı?
    Bağlam Yeniden Sıralama Puanı: 0.0


    Soru: Sam Altman bu makalede ne yaptı?
    Yanıt: Sam Altman, orijinal kurucular geri çekilmeye ve şirketi uzun vadeli sürdürülebilirlik için yeniden organize etmeye karar verdikten sonra Y Combinator'ın başkanı olması istendi.

    Bağlam Uygunluğu Puanı: 1.0
    Olgusal Doğruluk Puanı: 1.0
    Yanıt Tamlığı Puanı: 0.5

# 3b. Yeniden Sıralama (Farklı sayıda node ile)

Yeniden sıralamadan sonra döndürülen node sayısı orijinal node sayısından azsa, aşağıdaki değerlendirme gerçekleştirilecektir:

- **[Bağlam Özlüğü (Context Conciseness)](https://docs.uptrain.ai/predefined-evaluations/context-awareness/context-conciseness)**: Azaltılmış node sayısının hala gerekli tüm bilgileri sağlayıp sağlamadığını inceler.

```python
callback_handler = UpTrainCallbackHandler(
    key_type="openai",
    api_key=os.environ["OPENAI_API_KEY"],
    project_name_prefix="llama",
)
Settings.callback_manager = CallbackManager([callback_handler])

rerank_postprocessor = SentenceTransformerRerank(
    top_n=2,  # Yeniden sıralamadan sonraki node sayısı
    keep_retrieval_score=True,
)

index = VectorStoreIndex.from_documents(
    documents=documents,
)
query_engine = index.as_query_engine(
    similarity_top_k=5,  # Yeniden sıralamadan önceki node sayısı
    node_postprocessors=[rerank_postprocessor],
)

# Gelişmiş RAG'ınızı kullanın
response = query_engine.query(
    "Sam Altman bu makalede ne yaptı?",
)
```

    Soru: Sam Altman bu makalede ne yaptı?
    Bağlam Özlüğü Puanı: 0.0


    Soru: Sam Altman bu makalede ne yaptı?
    Yanıt: Sam Altman, mülakatlar için Kaliforniya'ya yaptığı bir ziyaret sırasında yazara istenmeyen (unsolicited) tavsiyelerde bulundu.


    Bağlam Uygunluğu Puanı: 1.0
    Olgusal Doğruluk Puanı: 1.0
    Yanıt Tamlığı Puanı: 0.5

# UpTrain Yönetilen Hizmet Paneli ve İçgörüler

UpTrain geri çağırma yöneticisi aracılığıyla UpTrain'in yönetilen hizmetini kullanmak için gereken tek değişiklik `key_type` ve `api_key` parametrelerini ayarlamaktır. Kodun geri kalanı aynı kalır.

```python
callback_handler = UpTrainCallbackHandler(
    key_type="uptrain",
    api_key="up-******************************",
    project_name_prefix="llama",
)
```

İşte UpTrain yönetilen hizmetinden alabileceğiniz paneli ve içgörüleri gösteren kısa bir GIF:

![output.gif](https://uptrain-assets.s3.ap-south-1.amazonaws.com/images/llamaindex/output.gif)

# 2. UpTrain'in EvalLlamaIndex Nesnesini Kullanmak <a href="https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/evaluation/UpTrain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab'da Aç"/></a>

## UpTrain ve LlamaIndex'i Kurun

```bash
pip install uptrain llama_index
```

## Gerekli Kütüphaneleri İçe Aktarın

```python
import httpx
import os
import openai
import pandas as pd

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from uptrain import Evals, EvalLlamaIndex, Settings as UpTrainSettings
```

## Sorgu Motoru İçin Veri Kümesi Klasörünü Oluşturun

Bunu yapmak için sahip olduğunuz herhangi bir dökümanı kullanabilirsiniz. Bu eğitim için Wikipedia'dan alınan New York Şehri (NYC) hakkındaki verileri kullanacağız. Klasöre sadece bir döküman ekleyeceğiz ancak siz istediğiniz kadar ekleyebilirsiniz.

```python
url = "https://uptrain-assets.s3.ap-south-1.amazonaws.com/data/nyc_text.txt"
if not os.path.exists("nyc_wikipedia"):
    os.makedirs("nyc_wikipedia")
dataset_path = os.path.join("./nyc_wikipedia", "nyc_text.txt")

if not os.path.exists(dataset_path):
    r = httpx.get(url)
    with open(dataset_path, "wb") as f:
        f.write(r.content)
```

## Sorgu Listesini Yapın

Yanıtlar oluşturmadan önce bir sorgu listesi oluşturmamız gerekiyor. Sorgu motoru New York Şehri üzerine eğitildiği için, New York Şehri ile ilgili sorgulardan oluşan bir liste oluşturacağız.

```python
data = [
    {"question": "New York Şehri'nin nüfusu nedir?"},
    {"question": "New York Şehri'nin yüzölçümü nedir?"},
    {"question": "New York Şehri'ndeki en büyük ilçe (borough) hangisidir?"},
    {"question": "New York Şehri'nde ortalama sıcaklık nedir?"},
    {"question": "New York Şehri'ndeki ana havaalanı hangisidir?"},
    {"question": "New York Şehri'ndeki ünlü simge yapı nedir?"},
    {"question": "New York Şehri'nin resmi dili nedir?"},
    {"question": "New York Şehri'nde kullanılan para birimi nedir?"},
    {"question": "New York Şehri'nin saat dilimi nedir?"},
    {"question": "New York Şehri'ndeki ünlü spor takımı hangisidir?"},
]
```

**Bu not defteri, istemler için metin oluşturmak ve Vektör Depo İndeksi oluşturmak için OpenAI API'sini kullanır. Bu nedenle `openai.api_key` değerini OpenAI API anahtarınıza ayarlayın.**

```python
openai.api_key = "sk-************************"  # OpenAI API anahtarınız
```

## LlamaIndex Kullanarak Bir Sorgu Motoru Oluşturun

LlamaIndex kullanarak bir vektör depo indeksi oluşturalım ve ardından bunu dökümantasyondan ilgili bölümleri getirmek için bir sorgu motoru olarak kullanalım.

```python
Settings.chunk_size = 512

documents = SimpleDirectoryReader("./nyc_wikipedia/").load_data()

vector_index = VectorStoreIndex.from_documents(
    documents,
)

query_engine = vector_index.as_query_engine()
```

## Kurulum (Setup)

UpTrain size şunları sağlar:

1. Gelişmiş detaylandırma ve filtreleme seçeneklerine sahip paneller
2. Başarısız durumlardaki içgörüler ve ortak konular
3. Üretim verilerinin gözlemlenebilirliği ve gerçek zamanlı izlenmesi
4. CI/CD boru hatlarınızla sorunsuz entegrasyon yoluyla regresyon testi

UpTrain kullanarak değerlendirme yapmak için aşağıdaki iki alternatiften birini seçebilirsiniz:

# Alternatif 1: UpTrain'in Açık Kaynak Yazılımını (OSS) Kullanarak Değerlendirin

Modelinizi değerlendirmek için açık kaynaklı değerlendirme hizmetini kullanabilirsiniz. Bu durumda bir OpenAI API anahtarı sağlamanız gerekecektir. Anahtarınızı [buradan](https://platform.openai.com/account/api-keys) alabilirsiniz.

Değerlendirmelerinizi UpTrain panelinde görüntülemek için terminalinizde aşağıdaki komutları çalıştırarak kurulum yapmanız gerekecektir:

```bash
git clone https://github.com/uptrain-ai/uptrain
cd uptrain
bash run_uptrain.sh
```

Bu, UpTrain panelini yerel makinenizde başlatacaktır. Ona `http://localhost:3000/dashboard` adresinden erişebilirsiniz.

**Not:** `project_name`, yapılan değerlendirmelerin UpTrain panelinde görüneceği proje adı olacaktır.

```python
settings = UpTrainSettings(
    openai_api_key=openai.api_key,
)
```

## EvalLlamaIndex Nesnesini Oluşturun

Sorgu motorunu oluşturduğumuza göre, onu bir `EvalLlamaIndex` nesnesi oluşturmak için kullanabiliriz. Bu nesne sorgular için yanıtlar üretmek amacıyla kullanılacaktır.

```python
llamaindex_object = EvalLlamaIndex(
    settings=settings, query_engine=query_engine
)
```

## Değerlendirmeyi Çalıştırın

Artık sorgu listesine sahip olduğumuza göre, sorgular için yanıtlar oluşturmak ve ardından yanıtlar üzerinde değerlendirmeler yapmak için `EvalLlamaIndex` nesnesini kullanabiliriz. UpTrain tarafından sunulan değerlendirmelerin kapsamlı bir listesini [burada](https://docs.uptrain.ai/key-components/evals) bulabilirsiniz. Bu eğitim için en alakalı bulduğumuz ikisini seçtik:

1. **Bağlam Uygunluğu (Context Relevance)**: Bu değerlendirme, erişilen bağlamın sorguyla alakalı olup olmadığını kontrol eder. Bu önemlidir çünkü erişilen bağlam yanıtı oluşturmak için kullanılır. Erişilen bağlam sorguyla alakalı değilse, yanıt da sorguyla alakalı olmayacaktır.

2. **Yanıt Özlüğü (Response Conciseness)**: Bu değerlendirme, yanıtın öz olup olmadığını kontrol eder. Bu önemlidir çünkü yanıt öz olmalı ve gereksiz bilgi içermemelidir.

```python
results = llamaindex_object.evaluate(
    project_name="uptrain-llama-index",
    evaluation_name="nyc_wikipedia",  # proje ve değerlendirme isimlerini eklemek, sonuçları UpTrain panelinde takip etmenize olanak tanır
    data=data,
    checks=[Evals.CONTEXT_RELEVANCE, Evals.RESPONSE_CONCISENESS],
)
```

```python
pd.DataFrame(results)
```

# Alternatif 2: UpTrain'in Yönetilen Hizmetini ve Panellerini Kullanarak Değerlendirin

Alternatif olarak, modelinizi değerlendirmek için UpTrain'in yönetilen hizmetini kullanabilirsiniz. [Buradan](https://uptrain.ai/) ücretsiz bir UpTrain hesabı oluşturabilir ve ücretsiz deneme kredileri alabilirsiniz. Daha fazla deneme kredisi istiyorsanız, [UpTrain yöneticileriyle buradan bir görüşme ayarlayın](https://calendly.com/uptrain-sourabh/30min).

Yönetilen hizmeti kullanmanın avantajları:

1. Yerel makinenizde UpTrain panelini kurmanıza gerek yoktur.
2. API anahtarlarına ihtiyaç duymadan birçok LLM'ye erişim sağlar.

Değerlendirmeleri gerçekleştirdikten sonra bunları `https://dashboard.uptrain.ai/dashboard` adresindeki UpTrain panelinde görüntüleyebilirsiniz.

**Not:** `project_name`, yapılan değerlendirmelerin UpTrain panelinde görüneceği proje adı olacaktır.

```python
UPTRAIN_API_KEY = "up-**********************"  # UpTrain API anahtarınız

# Bu durumda ayarlarda 'openai_api_key' yerine `uptrain_access_token` parametresini kullanıyoruz
settings = UpTrainSettings(
    uptrain_access_token=UPTRAIN_API_KEY,
)
```

## EvalLlamaIndex Nesnesini Oluşturun

Sorgu motorunu oluşturduğumuza göre, onu bir `EvalLlamaIndex` nesnesi oluşturmak için kullanabiliriz. Bu nesne sorgular için yanıtlar üretmek amacıyla kullanılacaktır.

```python
llamaindex_object = EvalLlamaIndex(
    settings=settings, query_engine=query_engine
)
```

## Değerlendirmeyi Çalıştırın

Artık sorgu listesine sahip olduğumuza göre, sorgular için yanıtlar oluşturmak ve ardından yanıtlar üzerinde değerlendirmeler yapmak için `EvalLlamaIndex` nesnesini kullanabiliriz. UpTrain tarafından sunulan değerlendirmelerin kapsamlı bir listesini [burada](https://docs.uptrain.ai/key-components/evals) bulabilirsiniz. Bu eğitim için en alakalı bulduğumuz ikisini seçtik:

1. **Bağlam Uygunluğu (Context Relevance)**: Bu değerlendirme, erişilen bağlamın sorguyla alakalı olup olmadığını kontrol eder. Bu önemlidir çünkü erişilen bağlam yanıtı oluşturmak için kullanılır. Erişilen bağlam sorguyla alakalı değilse, yanıt da sorguyla alakalı olmayacaktır.

2. **Yanıt Özlüğü (Response Conciseness)**: Bu değerlendirme, yanıtın öz olup olmadığını kontrol eder. Bu önemlidir çünkü yanıt öz olmalı ve gereksiz bilgi içermemelidir.

```python
results = llamaindex_object.evaluate(
    project_name="uptrain-llama-index",
    evaluation_name="nyc_wikipedia",  # proje ve değerlendirme isimlerini eklemek, sonuçları UpTrain panelinde takip etmenize olanak tanır
    data=data,
    checks=[Evals.CONTEXT_RELEVANCE, Evals.RESPONSE_CONCISENESS],
)
```

```python
pd.DataFrame(results)
```

### Paneller:

Puan ve o puana sahip vaka sayısının histogramı:

![nyc_dashboard.png](https://uptrain-assets.s3.ap-south-1.amazonaws.com/images/llamaindex/nyc_dashboard.png)

Başarısız vakaları filtreleyebilir ve aralarında ortak konular oluşturabilirsiniz. Bu, temel sorunu belirlemeye ve çözmeye yardımcı olabilir:

![nyc_insights.png](https://uptrain-assets.s3.ap-south-1.amazonaws.com/images/llamaindex/nyc_insights.png)

## Daha Fazla Bilgi Edinin

1. [UpTrainCallbackHandler Üzerine Colab Not Defteri](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/callbacks/UpTrainCallback.ipynb)
2. [LlamaIndex ile UpTrain Entegrasyonu Üzerine Colab Not Defteri](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/evaluation/UpTrain.ipynb)
3. [UpTrain Github Deposu](https://github.com/uptrain-ai/uptrain)
4. [UpTrain Dökümantasyonu](https://docs.uptrain.ai/)