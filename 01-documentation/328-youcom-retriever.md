# You.com Erişicisi (You.com Retriever)

---
title: You.com Erişicisi (You.com Retriever)
 | LlamaIndex OSS Belgeleri
---

Bu not defteri, You.com'un Arama API'sini LlamaIndex'te bir erişici (retriever) olarak nasıl kullanacağınızı gösterir. API, sorgunuza dayalı olarak ilgili web ve/veya haber sonuçlarını otomatik olarak döndürür. Arama ve diğer API'lerimiz hakkında daha fazla bilgi edinmek için belgelerimizi ziyaret edin: <https://docs.you.com/>

Erişici, You.com'un arama sonuçlarını LlamaIndex'in standart formatına (`NodeWithScore`) dönüştürerek şunları yapmanıza olanak tanır:

- Arama sonuçlarını LLM sorguları için bağlam (context) olarak kullanma
- Diğer erişicilerle (vektör depoları, veritabanları) birleştirme
- Sorgu motorları ve ajanlarla sorunsuz entegrasyon

'.venv (Python 3.13.9)' ile hücreleri çalıştırmak `ipykernel` paketini gerektirir. Bunu Python ortamınıza kurmanız gerekebilir.

Başlamak için `llama-index-retrievers-you` paketini kurun.

```bash
%pip install llama-index-retrievers-you
```

## Kurulum (Setup)

API anahtarınızı [You.com platformundan](https://you.com/platform) alın.

```python
import os
from getpass import getpass


# API anahtarınızı ayarlayın
you_api_key = os.environ.get("YDC_API_KEY") or getpass(
    "You.com API anahtarınızı girin: "
)
```

## Temel Kullanım (Basic usage)

Öncelikle erişiciyi kuralım ve hangi verileri döndürdüğünü görelim:

```python
from llama_index.retrievers.you import YouRetriever


retriever = YouRetriever(api_key=you_api_key)
retrieved_results = retriever.retrieve("ABD'deki ulusal parklar")


print(f"{len(retrieved_results)} sonuç getirildi")


for i, result in enumerate(retrieved_results):
    print(f"\nSonuç {i+1}:")
    print(f"  Metin: {result.node.text[:200]}...")
    print("Metaveri (Metadata):")
    for key, value in result.node.metadata.items():
        print(f"  {key}: {value}")
```

```text
10 sonuç getirildi

Sonuç 1:
  Metin: Ulusal anıtlar ise sıklıkla tarihi veya arkeolojik önemleri nedeniyle korunur. Sekiz ulusal park (Alaska'daki altı tane dahil), birlikte yönetilen ancak ayrı birimler olarak kabul edilen ve alanları aşağıdaki rakamlara dahil edilmeyen, farklı koruma düzeylerine sahip alanlar olan bir ulusal koruma alanı ile eşleştirilmiştir.
İlk ulusal park olan Yellowstone'u oluşturan bir yasa tasarısı 1872'de Başkan Ulysses S. Grant tarafından imzalanmış, bunu 1875'te Mackinac Ulusal Parkı (1895'te hizmet dışı bırakıldı) ve ardından 1890'da Rock Creek Park (daha sonra National Capital Parks ile birleştirildi), Sequoia ve Yosemite izlemiştir.
On dört ulusal park UNESCO Dünya Mirası Alanı (WHS) olarak belirlenmiştir ve 21 ulusal park UNESCO Biyosfer Rezervi (BR) olarak adlandırılmıştır; sekiz ulusal park her iki programda da yer almaktadır. Otuz eyaletin yanı sıra Amerikan Samoası ve ABD topraklarında da ulusal parklar bulunmaktadır.
En çok ulusal parka sahip eyalet dokuz parkla California'dır; onu sekiz parkla Alaska, beş parkla Utah ve dört parkla Colorado izlemektedir. En büyük ulusal park Alaska'daki Wrangell–St. Elias'tır: 8 milyon dönümden (32.375 km2) fazla alanı ile dokuz en küçük eyaletin her birinden daha büyüktür.
Kuzey Karolina ve Tennessee'deki Great Smoky Mountains Ulusal Parkı, 1944'ten bu yana en çok ziyaret edilen park olmuştur ve 2024'te 12 milyondan fazla ziyaretçiye ulaşmıştır. Buna karşılık, 2024 yılında Alaska'daki uzak Gates of the Arctic Ulusal Parkı ve Koruma Alanı'nı yaklaşık 11.900 kişi ziyaret etmiştir. ... Aşağıdaki tablo ulusal parkı olan 30 eyalet ve iki bölgeyi içermektedir....
Metaveri (Metadata):
  url: https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States
  title: List of national parks of the United States - Wikipedia
  description: National monuments, on the other hand, are also frequently protected for their historical or archaeological significance...
  page_age: 2025-12-10T05:10:46
  thumbnail_url: https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/RNS_Yellowstone_13399u.jpg/960px-RNS_Yellowstone_13399u.jpg
  favicon_url: https://you.com/favicon?domain=en.wikipedia.org&size=128
  source_type: web
...
```

## Asenkron Kullanım (Async usage)

Erişici asenkron işlemleri de destekler.

```python
from llama_index.retrievers.you import YouRetriever


retriever = YouRetriever(api_key=you_api_key)


# Asenkron işlemler için aretrieve kullanın
retrieved_results = await retriever.aretrieve("ABD'deki ulusal parklar")


print(f"Asenkron olarak {len(retrieved_results)} sonuç getirildi")


for i, result in enumerate(retrieved_results):
    print(f"\nSonuç {i+1}:")
    print(f"  Metin: {result.node.text[:200]}...")
    print("Metaveri (Metadata):")
    for key, value in result.node.metadata.items():
        print(f"  {key}: {value}")
```

## En Son Haberleri Alma (Getting the latest news)

You.com API'si sorgunuza bağlı olarak haber sonuçlarını da otomatik olarak getirebilir.

```python
# Haberlerle ilgili sorgular, yanıtta haber sonuçlarını da içerecektir
from typing import Any


# Her türden (haber ve web) en fazla 5 sonuç görmelisiniz
# source_type: "news" veya "web" olduğuna dikkat edin
retriever = YouRetriever(api_key=you_api_key, count=5, country="IN")


retrieved_results = retriever.retrieve(
    "Hindistan'daki en son jeopolitik güncellemeler nelerdir?"
)


print(f"{len(retrieved_results)} sonuç getirildi")
for i, result in enumerate(retrieved_results):
    print(f"\nSonuç {i+1}:")
    print(f"  Metin: {result.node.text[:200]}...")
    print("Metaveri (Metadata):")
    for key, value in result.node.metadata.items():
        print(f"  {key}: {value}")
```

## Arama Parametrelerini Özelleştirme (Customizing Search Parameters)

Aramayı isteğe bağlı parametrelerle özelleştirebilirsiniz:

```python
retriever = YouRetriever(
    api_key=you_api_key,
    count=20,  # Her bölüm (web/haber) için 20'ye kadar sonuç döndür
    country="US",  # ABD sonuçlarına odaklan
    language="en",  # İngilizce sonuçlar
    freshness="week",  # Geçen haftadan sonuçlar
    safesearch="moderate",  # Orta düzeyde güvenli arama filtreleme
)


retrieved_results = retriever.retrieve("yenilenebilir enerji atılımları")


print(f"ABD'den {len(retrieved_results)} güncel sonuç getirildi")
for i, result in enumerate(retrieved_results):
    print(f"\nSonuç {i+1}:")
    print(f"  Metin: {result.node.text[:200]}...")
    print("Metaveri (Metadata):")
    for key, value in result.node.metadata.items():
        print(f"  {key}: {value}")
```

## Sorgu Motoruyla Kullanım (Using with Query Engine)

Almak istediğimiz web verilerini nasıl özelleştireceğimizi gördüğümüze göre, şimdi arama sonuçlarından doğal dilde yanıtlar sentezlemek için bir LLM kullanalım. Bu örnekte Anthropic'ten bir model kullanacağız.

```bash
%pip install llama-index-llms-anthropic
```

```python
import os
from getpass import getpass


# Anthropic API anahtarınızı ayarlayın
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY") or getpass(
    "Anthropic API anahtarınızı girin: "
)
```

```python
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings
from llama_index.retrievers.you import YouRetriever


# Anthropic'i LLM'iniz olarak yapılandırın
llm = Anthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_api_key)


# Bağlam olarak You.com arama sonuçlarını kullanan bir sorgu motoru oluşturun
retriever = YouRetriever(api_key=you_api_key)
query_engine = RetrieverQueryEngine.from_args(retriever, llm)
```

```python
# Sorgu motoru:
# 1. You.com'dan ilgili arama sonuçlarını getirmek için erişiciyi kullanır
# 2. Bu sonuçları LLM'e bağlam olarak iletir
# 3. Sentezlenmiş bir yanıt döndürür


response = query_engine.query(
    "ABD'de en çok ziyaret edilen ulusal parklar hangileridir ve neden? Kısa tutun."
)


print(str(response))
```

```text
# ABD'de En Çok Ziyaret Edilen Ulusal Parklar

**En Çok Ziyaret Edilen İlk 3:**

1. **Great Smoky Mountains Ulusal Parkı** (Kuzey Karolina/Tennessee) - 13,3 milyon ziyaretçi
   - Neden: Muhteşem antik dağlar, çeşitli bitki ve hayvan yaşamı, tarihi Güney Appalachian kültürü ve Amerikan kara ayıları ile diğer vahşi yaşamın evi.

2. **Zion Ulusal Parkı** (Utah) - 4,9 milyon ziyaretçi
   - Neden: Kızıl kaya oluşumları, kumtaşı kanyonları ve keskin uçurumlar içeren çarpıcı dikey topografya.

3. **Büyük Kanyon (Grand Canyon) Ulusal Parkı** (Arizona) - 4,7 milyon ziyaretçi
   - Neden: İkonik bir mil derinliğindeki kanyon; muhteşem erozyon örnekleri ve her iki kenardan eşsiz manzaralar.

**Diğer Popüler Parklar:**
- **Yosemite Ulusal Parkı** (California) - Devasa granit kayalıkları, şelaleleri ve dev sekoya ağaçlarıyla ünlü.
- **Glacier Ulusal Parkı** (Montana) - Buzul kuvvetleri tarafından şekillendirilmiş dağ manzaraları.

Bu parklar, dramatik doğal manzaraları, çeşitli ekosistemleri, bol vahşi yaşamı ve doğa yürüyüşü, tekne gezintisi ve vahşi yaşam gözlemciliği gibi kapsamlı açık hava rekreasyon olanakları nedeniyle her yıl milyonlarca ziyaretçiyi kendine çekmektedir.
```

## Neden bu format? (Why this format?)

Erişici, You.com'un JSON yanıtını LlamaIndex'in standart `NodeWithScore` formatına dönüştürür. Bu şunları sağlar:

**Faydalar:**

- **Kaynaktan bağımsız (Source-agnostic)**: İster You.com'dan, ister vektör veritabanlarından veya diğer kaynaklardan veri getirilsin, aynı arayüz kullanılır.
- **Birleştirilebilirlik (Composability)**: Birden fazla erişiciyi kolayca birleştirin veya birbirleriyle değiştirin.
- **Entegrasyon**: LlamaIndex sorgu motorları, ajanları ve diğer bileşenleri ile sorunsuz çalışır.

**Neler korunur:**

- **Metin içeriği (Text content)**: Web sonuçlarından parçacıklar veya haber makalelerinden açıklamalar.
- **Metaveri (Metadata)**: `metadata` sözlüğünde saklanan URL, başlık ve sayfa yaşı (`page_age`).
- **Puan (Score)**: Alaka düzeyi puanı (You.com puan sağlamadığı için varsayılan olarak 1.0).

Bu soyutlama, API'ye özgü yanıt formatlarını işlemek yerine uygulama oluşturmaya odaklanmanızı sağlar.
