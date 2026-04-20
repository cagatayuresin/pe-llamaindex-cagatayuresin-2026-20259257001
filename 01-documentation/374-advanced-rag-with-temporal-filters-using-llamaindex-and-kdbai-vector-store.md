---
title: LlamaIndex ve KDB.AI Vektör Deposu Kullanarak Zamansal Filtrelerle Gelişmiş RAG
 | LlamaIndex OSS Belgeleri
---

# LlamaIndex ve KDB.AI Vektör Deposu Kullanarak Zamansal Filtrelerle Gelişmiş RAG

##### Not: Bu örnek bir KDB.AI uç noktası ve API anahtarı gerektirir. Ücretsiz bir [KDB.AI hesabı](https://kdb.ai/get-started) için kaydolun.

> [KDB.AI](https://kdb.ai/), gelişmiş arama, tavsiye ve kişiselleştirme sağlayarak gerçek zamanlı verileri kullanarak ölçeklenebilir, güvenilir yapay zeka uygulamaları oluşturmanıza olanak tanıyan güçlü, bilgi tabanlı bir vektör veritabanı ve arama motorudur.

Bu örnek, KDB.AI'nın finansal düzenlemelerin belirli bir zaman dilimi etrafında semantik aramasını, özetlenmesini ve analizini yapmak için nasıl kullanılacağını göstermektedir.

Uç noktanıza (endpoint) ve API anahtarlarınıza erişmek için [buradan](https://kdb.ai/get-started) KDB.AI'ya kaydolun.

Geliştirme ortamınızı kurmak için KDB.AI'nın ön koşullar sayfasındaki talimatları izleyin.

Aşağıdaki örnekler, LlamaIndex aracılığıyla KDB.AI ile etkileşim kurmanın bazı yollarını göstermektedir.

## Pip ile bağımlılıkları kurun

Bu örneği başarıyla çalıştırmak için, bu not defterini nerede çalıştırdığınıza bağlı olarak aşağıdaki adımları dikkate alın:

- **Yerel Olarak / Özel Ortamda Çalıştırma:** Deponun `README.md` dosyasındaki [Kurulum (Setup)](https://github.com/KxSystems/kdbai-samples/blob/main/README.md#setup) adımları, ön koşullar ve bunun Jupyter ile nasıl çalıştırılacağı konusunda size yol gösterecektir.

- **Colab / Barındırılan Ortamda Çalıştırma:** Bu not defterini Colab'de açın ve hücreleri sırayla çalıştırın.

```bash
!pip install llama-index llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file llama-index-vector-stores-kdbai
!pip install kdbai_client pandas
```

## Bağımlılıkları içe aktarın

```python
from getpass import getpass
import re
import os
import shutil
import time
import urllib
import datetime


import pandas as pd


from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.kdbai import KDBAIVectorStore


import kdbai_client as kdbai


OUTDIR = "pdf"
RESET = True
```

#### OpenAI API anahtarını ayarlayın ve kullanılacak LLM ve Gömme (Embedding) modelini seçin:

```python
# os.environ["OPENAI_API_KEY"] = getpass("OpenAI API anahtarı: ")
os.environ["OPENAI_API_KEY"] = (
    os.environ["OPENAI_API_KEY"]
    if "OPENAI_API_KEY" in os.environ
    else getpass("OpenAI API Anahtarı: ")
)
```

```python
import os
from getpass import getpass


# OpenAI API'yi Ayarla
if "OPENAI_API_KEY" in os.environ:
    KDBAI_API_KEY = os.environ["OPENAI_API_KEY"]
else:
    # Kullanıcıdan API anahtarını girmesini iste
    OPENAI_API_KEY = getpass("OPENAI API ANAHTARI: ")
    # API anahtarını geçerli oturum için bir ortam değişkeni olarak kaydet
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

```python
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"


llm = OpenAI(model=GENERATION_MODEL)
embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL)


Settings.llm = llm
Settings.embed_model = embed_model
```

## KDB.AI oturumu ve tablosu oluşturun

```python
# vektör DB içe aktarmaları
import os
from getpass import getpass
import kdbai_client as kdbai
import time
```

##### Seçenek 1. KDB.AI Cloud

KDB.AI Cloud'u kullanmak için iki oturum detayına ihtiyacınız olacaktır: bir URL uç noktası ve bir API anahtarı. Bunları almak için [buradan](https://trykdb.kx.com/kdbai/signup) ücretsiz kayıt olabilirsiniz.

`kdbai.Session` kullanarak ve KDB.AI Cloud portalınızdaki oturum URL uç noktası ve API anahtarı bilgilerini ileterek bir KDB.AI Cloud oturumuna bağlanabilirsiniz.

Sisteminizde KDB.AI Cloud portal bilgilerinizi içeren `KDBAI_ENDPOINTS` ve `KDBAI_API_KEY` ortam değişkenleri varsa, bu değişkenler otomatik olarak bağlanmak için kullanılacaktır. Mevcut değillerse, KDB.AI Cloud portal oturum URL uç noktanızı ve API anahtarı bilgilerinizi girmeniz istenecektir.

```python
# KDB.AI uç noktasını ve API anahtarını ayarla
KDBAI_ENDPOINT = (
    os.environ["KDBAI_ENDPOINT"]
    if "KDBAI_ENDPOINT" in os.environ
    else input("KDB.AI uç noktası (endpoint): ")
)
KDBAI_API_KEY = (
    os.environ["KDBAI_API_KEY"]
    if "KDBAI_API_KEY" in os.environ
    else getpass("KDB.AI API anahtarı: ")
)


session = kdbai.Session(endpoint=KDBAI_ENDPOINT, api_key=KDBAI_API_KEY)
```

##### Seçenek 2. KDB.AI Server

KDB.AI Server'ı kullanmak için kendi konteynerinizi indirip çalıştırmanız gerekecektir. Bunu yapmak için önce [buradan](https://trykdb.kx.com/kdbaiserver/signup/) ücretsiz kaydolmanız gerekir.

Örneğinizi (instance) indirmek için gereken lisans dosyasını ve taşıyıcı belirteci (bearer token) içeren bir e-posta alacaksınız. Oturumunuzu çalışır hale getirmek için kayıt e-postasındaki talimatları izleyin.

[Kurulum adımları](https://code.kx.com/kdbai/gettingStarted/kdb-ai-server-setup.html) tamamlandıktan sonra, `kdbai.Session` kullanarak ve yerel uç noktanızı ileterek KDB.AI Server oturumunuza bağlanabilirsiniz.

```python
# session = kdbai.Session()
```

### KDB.AI tablonuz için şema oluşturun

***!!! Not:*** Gömme sütunundaki 'dims' parametresi, seçtiğiniz gömme modelinin çıktı boyutlarını yansıtmalıdır.

- OpenAI 'text-embedding-3-small' 1536 boyut çıktı verir.

```python
schema = [
    {"name": "document_id", "type": "bytes"},
    {"name": "text", "type": "bytes"},
    {"name": "embeddings", "type": "float32s"},
    {"name": "title", "type": "str"},
    {"name": "publication_date", "type": "datetime64[ns]"},
]




indexFlat = {
    "name": "flat_index",
    "type": "flat",
    "column": "embeddings",
    "params": {"dims": 1536, "metric": "L2"},
}
```

```python
KDBAI_TABLE_NAME = "reports"
database = session.database("default")


# Önce tablonun zaten var olmadığından emin ol
for table in database.tables:
    if table.name == KDBAI_TABLE_NAME:
        table.drop()
        break


# Tabloyu oluştur
table = database.create_table(
    KDBAI_TABLE_NAME, schema=schema, indexes=[indexFlat]
)
```

## Finansal rapor URL'leri ve meta veriler

```python
INPUT_URLS = [
    "https://www.govinfo.gov/content/pkg/PLAW-106publ102/pdf/PLAW-106publ102.pdf",
    "https://www.govinfo.gov/content/pkg/PLAW-111publ203/pdf/PLAW-111publ203.pdf",
]


METADATA = {
    "pdf/PLAW-106publ102.pdf": {
        "title": "GRAMM–LEACH–BLILEY YASASI, 1999",
        "publication_date": pd.to_datetime("1999-11-12"),
    },
    "pdf/PLAW-111publ203.pdf": {
        "title": "DODD-FRANK WALL STREET REFORMU VE TÜKETİCİ KORUMA YASASI, 2010",
        "publication_date": pd.to_datetime("2010-07-21"),
    },
}
```

## PDF dosyalarını yerel olarak indir

```python
%%time


CHUNK_SIZE = 512 * 1024




def download_file(url):
    print("İndiriliyor: %s..." % url)
    out = os.path.join(OUTDIR, os.path.basename(url))
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        logging.exception("%s indirilemedi!" % url)
    else:
        with open(out, "wb") as f:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if chunk:
                    f.write(chunk)
                else:
                    break
    return out




if RESET:
    if os.path.exists(OUTDIR):
        shutil.rmtree(OUTDIR)
    os.mkdir(OUTDIR)


    local_files = [download_file(x) for x in INPUT_URLS]
    local_files[:10]
```

```text
İndiriliyor: https://www.govinfo.gov/content/pkg/PLAW-106publ102/pdf/PLAW-106publ102.pdf...




İndiriliyor: https://www.govinfo.gov/content/pkg/PLAW-111publ203/pdf/PLAW-111publ203.pdf...
CPU times: user 52.6 ms, sys: 1.2 ms, total: 53.8 ms
Wall time: 7.86 s
```

## Yerel PDF dosyalarını LlamaIndex ile yükle

```python
%%time




def get_metadata(filepath):
    return METADATA[filepath]




documents = SimpleDirectoryReader(
    input_files=local_files,
    file_metadata=get_metadata,
)


docs = documents.load_data()
len(docs)
```

```text
CPU times: user 8.22 s, sys: 9.04 ms, total: 8.23 s
Wall time: 8.23 s


994
```

## KDB.AI vektör deposunu kullanarak LlamaIndex RAG hattını kurun

```python
%%time


# llm = OpenAI(temperature=0, model=LLM)
vector_store = KDBAIVectorStore(table)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    docs,
    storage_context=storage_context,
    transformations=[SentenceSplitter(chunk_size=2048, chunk_overlap=0)],
)
```

```text
CPU times: user 3.67 s, sys: 31.9 ms, total: 3.7 s
Wall time: 22.3 s
```

```python
table.query()
```

|     | document_id                            | text                                              | embeddings                                         | title                                             | publication_date |
| --- | --------------------------------------- | ------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------- | ----------------- |
| 0   | b'272d7d24-c232-41b6-823e-27aa6203c100' | b'PUBLIC LAW 106\xc2\xb1102\xc3\x90NOV. 12, 19... | \[0.034452137, 0.03166917, -0.011892043, 0.0184... | GRAMM–LEACH–BLILEY ACT, 1999                      | 1999-11-12        |
| ... | ...                                     | ...                                               | ...                                                | ...                                               | ...               |

## LlamaIndex Sorgu Motorunu (Query Engine) Kurun

```python
%%time


# gpt-4o-mini kullanıldığında, 128k token bağlam boyutu 100 sayfa alabilir.
K = 15


query_engine = index.as_query_engine(
    similarity_top_k=K,
    vector_store_kwargs={
        "index": "flat_index",
        "filter": [["<", "publication_date", datetime.date(2008, 9, 15)]],
        "sort_columns": "publication_date",
    },
)
```

## 2008 krizi öncesi

```python
%%time


result = query_engine.query(
    """
    2008 finansal krizinden önce ABD'deki ana finansal düzenleme neydi?
    """
)
print(result.response)
```

**2008 finansal krizinden önce ABD'deki ana finansal düzenleme, 1999 yılında yürürlüğe giren Gramm-Leach-Bliley Yasası idi. Bu yasa, bankalar, menkul kıymetler firmaları ve sigorta şirketleri arasındaki birleşmeleri kolaylaştırarak; daha önce bu finansal hizmetleri birbirinden ayıran Glass-Steagall Yasası'nın bazı bölümlerini fiilen iptal etti. Gramm-Leach-Bliley Yasası, çeşitli finansal kuruluşların entegrasyonu için bir çerçeve sağlayarak finansal hizmetler sektöründeki rekabeti artırmayı amaçlıyordu.**

```python
%%time


result = query_engine.query(
    """
    1999 tarihli Gramm-Leach-Bliley Yasası, 2008 krizini önlemek için yeterli miydi? Belgeyi araştırın ve ABD borsasını düzenlemedeki güçlü ve zayıf yönlerini açıklayın.
    """
)
print(result.response)
```

**1999 tarihli Gramm-Leach-Bliley Yasası, bankalar, menkul kıymetler firmaları ve sigorta şirketleri arasında ortaklıklara izin vererek finansal hizmetler sektöründeki rekabeti artırmayı amaçlıyordu. Güçlü yönleri arasında, daha önce ticari bankacılığı yatırım bankacılığından ayıran Glass-Steagall Yasası'nın iptal edilmesi yer alır; bu, finansal kurumların hizmetlerini çeşitlendirmesine ve potansiyel olarak rekabeti artırmasına olanak tanımıştır. Bu çeşitlendirme, daha yenilikçi finansal ürün ve hizmetlerin ortaya çıkmasına yol açabilirdi.**

**Ancak, Yasa'nın kayda değer zayıf yönleri de vardır. Daha büyük ortaklıklara izin vererek ve düzenleyici engelleri azaltarak, finansal sistem için sistemik riskler oluşturan "batamayacak kadar büyük" (too big to fail) kurumların oluşmasına katkıda bulunmuş olabilir. Sıkı denetim eksikliği ve finansal holding şirketlerinin yeterli düzenleme olmaksızın geniş bir yelpazede faaliyet gösterme yeteneği, aşırı risk alımına yol açmış olabilir. Ayrıca Yasa, 2008 finansal krizinde önemli rol oynayan türev araçlar gibi modern finansal ürünlerin karmaşıklığını yeterince ele almamıştır.**

**Özetle, Gramm-Leach-Bliley Yasası finans sektöründe rekabeti ve yenilikçiliği teşvik etmeyi amaçlasa da; düzenleme çerçevesi istemeden de olsa finansal krize yol açan koşulları kolaylaştırmış olabilir ve bu da finansal sistem içindeki bağlantıları ve riskleri denetlemek için daha sağlam bir düzenleme yaklaşımına duyulan ihtiyacı vurgulamaktadır.**

## 2008 krizi sonrası

```python
%%time


# gpt-4o-mini kullanıldığında, 128k token bağlam boyutu 100 sayfa alabilir.
K = 15


query_engine = index.as_query_engine(
    similarity_top_k=K,
    vector_store_kwargs={
        "index": "flat_index",
        "filter": [[">=", "publication_date", datetime.date(2008, 9, 15)]],
        "sort_columns": "publication_date",
    },
)
```

```python
%%time


result = query_engine.query(
    """
    15 Eylül 2008'de ne oldu?
    """
)
print(result.response)
```

**15 Eylül 2008'de, küresel bir finansal hizmetler devi olan Lehman Brothers iflas başvurusunda bulundu. Bu olay, ABD tarihindeki en büyük iflaslardan biriydi ve 2007-2008 finansal krizinin dönüm noktalarından biri oldu; finans piyasalarında yaygın paniğe yol açtı ve küresel ekonomik krize damgasını vurdu.**

```python
%%time


result = query_engine.query(
    """
    Piyasa düzenlemesini artırmak ve tüketici güvenini iyileştirmek için 2008 krizinden sonra yürürlüğe giren yeni ABD finansal düzenlemesi neydi?
    """
)
print(result.response)
```

**Piyasa düzenlemesini artırmak ve tüketici güvenini iyileştirmek için 2008 krizinden sonra yürürlüğe giren yeni ABD finansal düzenlemesi, 21 Temmuz 2010 tarihinde yasalaşan Dodd-Frank Wall Street Reformu ve Tüketici Koruma Yasası'dır. Bu mevzuat, finansal istikrarı teşvik etmeyi, finansal sistemde hesap verebilirliği ve şeffaflığı artırmayı ve tüketicileri suistimalci finansal uygulamalardan korumayı amaçlamıştır.**

## Derinlemesine analiz

```python
%%time


# gpt-4o-mini kullanıldığında, 128k token bağlam boyutu 100 sayfa alabilir.
K = 20


query_engine = index.as_query_engine(
    similarity_top_k=K,
    vector_store_kwargs={
        "index": "flat_index",
        "sort_columns": "publication_date",
    },
)
```

```python
%%time


result = query_engine.query(
    """
    2008 krizi öncesi ve sonrası ABD finansal düzenlemelerini analiz edin ve nelerin yaşandığını açıklamak ve bunun tekrar yaşanmamasını sağlamak için tüm ilgili argümanları içeren bir rapor oluşturun.
    Hem sağlanan bağlamı hem de kendi bilgilerinizi kullanın, ancak hangisini kullandığınızı açıkça belirtin.
    """
)
print(result.response)
```

**2008 finansal krizi öncesi ve sonrası ABD finansal düzenlemelerinin analizi, böyle bir krizin tekrarlanmasını önlemeyi amaçlayan önemli değişiklikleri ortaya koymaktadır.**

**Krizden önce, düzenleyici çerçeve, özellikle banka dışı finansal kuruluşlar için kapsamlı denetim eksikliği ile karakterize ediliyordu. Düzenleyici ortam; aşırı risk alımına, yetersiz sermaye gereksinimlerine ve finansal işlemlerde yetersiz şeffaflığa izin veriyordu. Bu ortam, konut balonuna ve ardından büyük finansal kurumların çöküşüne katkıda bulunarak yaygın ekonomik kargaşaya yol açtı.**

**Krize yanıt olarak, 2010 yılında Dodd-Frank Wall Street Reformu ve Tüketici Koruma Yasası yürürlüğe girdi. Bu mevzuat birkaç temel reform getirdi:**

1.  **Finansal İstikrar Gözetim Konseyi'nin (FSOC) Kurulması:** Bu kurum, sistemik riskleri izlemek ve farklı finans sektörleri arasındaki düzenleme çabalarını koordine etmek amacıyla kurulmuştur. Finansal istikrar için risk oluşturabilecek finansal faaliyetler için yükseltilmiş standartlar ve korumalar önerme yetkisine sahiptir.
2.  **Gelişmiş Düzenleyici Denetim:** Dodd-Frank, özellikle önemli varlıklara sahip olan banka holding şirketleri ve banka dışı finansal şirketler üzerinde daha sıkı düzenlemeler getirdi. Buna stres testleri, sermaye planlaması ve başarısızlık durumunda düzenli tasfiye (wind-down) süreçlerini sağlamak için çözüm planlarının sunulması şartları dahildir.
3.  **Tüketici Koruma Önlemleri:** Tüketici Finansal Koruma Bürosu'nun (CFPB) kurulması, tüketicileri suistimalci borç verme uygulamalarından korumayı ve finansal ürünlerde şeffaflığı sağlamayı amaçlamıştır.
4.  **Volcker Kuralı:** Bu hüküm, bankaların kendi nam ve hesabına (proprietary) ticaret yapmalarını kısıtlar; serbest yatırım fonlarına (hedge funds) ve özel sermaye fonlarına (private equity funds) yaptıkları yatırımları sınırlayarak çıkar çatışmalarını ve aşırı risk alımını azaltır.
5.  **Artan Şeffaflık ve Raporlama Gereksinimleri:** Finansal kurumların artık risk maruziyetleri ve finansal sağlıkları hakkında daha fazla bilgi açıklamaları gerekmektedir, bu da piyasa disiplinini ve yatırımcı güvenini artırır.

**Bu reformların temelindeki argümanlar, ekonomik şoklara dayanabilecek daha dirençli bir finansal sisteme duyulan ihtiyaç etrafında toplanmaktadır. Reformlar, kriz öncesinde yaygın olan sistemik riskleri ele almayı, finansal kurumların yeterli sermaye tamponlarını korumalarını ve ihtiyatlı risk yönetimi uygulamalarında bulunmalarını sağlamayı amaçlamaktadır.**

**Sonuç olarak, 2008 krizinden bu yana düzenleme ortamı; aşırı risk alımını önlemeye, şeffaflığı artırmaya ve tüketicileri korumaya odaklanarak önemli ölçüde değişmiştir. Bu önlemler, daha istikrarlı bir finansal ortam yaratmak ve gelecekteki krizlerin olasılığını azaltmak için tasarlanmıştır.**

## KDB.AI Tablosunu Silme

Tablo ile işiniz bittiğinde, tabloyu silmek en iyi uygulamadır.

```python
table.drop()
```

#### Ankete Katılın

Bu örneği faydalı bulduğunuzu umuyoruz! Geri bildiriminiz bizim için önemlidir ve kısa anketimizi doldurmak için bir dakikanızı ayırırsanız memnun oluruz. Girdiğiniz bilgiler içeriğimizi geliştirmemize yardımcı olur.

[Ankete Katılın](https://delighted.com/t/kWYXv316)
