# LlamaIndex'e Hoş Geldiniz 🦙 !

LlamaIndex; verileriniz üzerinde [LLM'ler (Büyük Dil Modelleri)](https://en.wikipedia.org/wiki/Large_language_model) ve [iş akışları](/python/llamaagents/workflows) kullanarak LLM destekli ajanlar oluşturmak için önde gelen çerçevedir (framework).

### [Giriş](#introduction)

Bağlam artırma (context augmentation) nedir? Ajanlar ve iş akışları nelerdir? LlamaIndex bunları oluşturmaya nasıl yardımcı olur?

### [Kullanım Örnekleri](#use-cases)

LlamaIndex ile ne tür uygulamalar geliştirebilirsiniz? Kimler kullanmalı?

### [Başlangıç](#getting-started)

Python veya TypeScript'te sadece 5 satır kodla başlayın!

### [LlamaCloud](https://docs.cloud.llamaindex.ai/)

Dünyanın en iyi belge ayrıştırıcısı olan [LlamaParse](https://developers.llamaindex.ai/python/cloud/llamaparse/) dahil olmak üzere LlamaIndex için yönetilen servisler.

### [Topluluk](#community)

Discord, Twitter, LinkedIn üzerinden yardım alın ve iş birlikçilerle tanışın; projeye nasıl katkıda bulunabileceğinizi öğrenin.

### [İlgili Projeler](#related-projects)

[LlamaHub](https://llamahub.ai) adresindeki bağlayıcı, okuyucu ve diğer entegrasyon kütüphanemizin yanı sıra [create-llama](https://www.npmjs.com/package/create-llama) gibi demoları ve başlangıç uygulamalarını inceleyin.

## Giriş

### Ajanlar (Agents) nedir?

[Ajanlar](/python/framework/understanding/agent), araştırma, veri çıkarma ve daha fazlası gibi görevleri yerine getirmek için araçlar kullanan LLM destekli bilgi asistanlarıdır. Ajanlar, basit soru-cevap işlemlerinden, görevleri tamamlamak için algılama, karar verme ve eyleme geçme yeteneğine sahip sistemlere kadar çeşitlilik gösterir.

LlamaIndex, bir görevi tamamlamak için RAG hatlarını (pipelines) birçok araçtan biri olarak kullanma yeteneği de dahil olmak üzere, ajanlar oluşturmak için bir çerçeve sağlar.

### İş akışları (Workflows) nedir?

[İş akışları](/python/llamaagents/workflows), bir görevi tamamlamak için bir veya daha fazla ajanı, veri bağlayıcıyı ve diğer araçları birleştiren çok adımlı süreçlerdir. Bunlar; olay güdümlü (event-driven) yazılımlardır ve RAG veri kaynaklarını birden fazla ajanla birleştirerek; yansıtma (reflection), hata düzeltme ve gelişmiş LLM uygulamalarının diğer belirgin özellikleriyle çok çeşitli görevleri yerine getirebilen karmaşık uygulamalar oluşturmanıza olanak tanır. Daha sonra bu [ajansal iş akışlarını](/python/workflows/deployment/) üretim mikro servisleri olarak dağıtabilirsiniz.

### Bağlam artırma (Context augmentation) nedir?

LLM'ler, insanlar ve veriler arasında doğal bir dil arayüzü sunar. LLM'ler çok büyük miktardaki halka açık verilerle önceden eğitilmiş olarak gelirler, ancak **sizin** verilerinizle eğitilmemişlerdir. Verileriniz özel olabilir veya çözmeye çalıştığınız soruna özgü olabilir. Bu veriler API'lerin arkasında, SQL veritabanlarında veya PDF ve sunumlarda hapsolmuş olabilir.

Bağlam artırma, verilerinizi mevcut sorunu çözmek için LLM'nin kullanımına sunar. LlamaIndex, prototipten üretime kadar her türlü bağlam artırma kullanım durumunu oluşturmak için gerekli araçları sağlar. Araçlarımız; verilerinizi almanıza (ingest), ayrıştırmanıza, dizinlemenize (index) ve işlemenize; ayrıca veri erişimini LLM istemiyle (prompting) birleştiren karmaşık sorgu iş akışlarını hızlıca uygulamanıza olanak tanır.

Bağlam artırmanın en popüler örneği, çıkarım (inference) sırasında bağlamı LLM'lerle birleştiren [Geri Getirme Destekli Nesil (Retrieval-Augmented Generation) veya RAG](/python/framework/getting_started/concepts) yöntemidir.

### LlamaIndex, Bağlam Destekli LLM Uygulamaları için bir çerçevedir

LlamaIndex, LLM'leri nasıl kullanacağınız konusunda hiçbir kısıtlama getirmez. LLM'leri otomatik tamamlama, sohbet robotları, ajanlar ve daha fazlası olarak kullanabilirsiniz. Sadece bunları kullanmayı kolaylaştırır. Aşağıdaki gibi araçlar sunuyoruz:

- **Veri bağlayıcıları (Data connectors)**, mevcut verilerinizi yerel kaynaklarından ve formatlarından alır. Bunlar API'ler, PDF'ler, SQL ve (çok) daha fazlası olabilir.
- **Veri indeksleri (Data indexes)**, verilerinizi LLM'lerin tüketmesi için kolay ve performanslı ara temsillere göre yapılandırır.
- **Motorlar (Engines)**, verilerinize doğal dil erişimi sağlar. Örneğin:
  - Sorgu motorları (Query engines), soru-cevaplama (örneğin bir RAG akışı) için güçlü arayüzlerdir.
  - Sohbet motorları (Chat engines), verilerinizle çok mesajlı, "karşılıklı" etkileşimler için konuşma arayüzleridir.
- **Ajanlar (Agents)**, basit yardımcı fonksiyonlardan API entegrasyonlarına kadar araçlarla desteklenen, LLM destekli bilgi çalışanlarıdır.
- **Gözlemlenebilirlik/Değerlendirme (Observability/Evaluation)** entegrasyonları, uygulamanızı titizlikle denemenize, değerlendirmenize ve izlemenize olanak tanır.
- **İş akışları (Workflows)**, yukarıdakilerin tümünü diğer grafik tabanlı yaklaşımlardan çok daha esnek, olay güdümlü bir sistemde birleştirmenizi sağlar.

## Kullanım Örnekleri

LlamaIndex ve genel olarak bağlam artırma için bazı popüler kullanım durumları şunlardır:

- [Soru-Cevap](/python/framework/use_cases/q_and_a) (Geri Getirme Destekli Nesil - RAG)
- [Sohbet Robotları](/python/framework/use_cases/chatbots)
- [Belge Anlama ve Veri Çıkarma](/python/framework/use_cases/extraction)
- Araştırma yapabilen ve eyleme geçebilen [Otonom Ajanlar](/python/framework/use_cases/agents)
- Metin, resim ve diğer veri türlerini birleştiren [Çok modlu (Multi-modal) uygulamalar](/python/framework/use_cases/multimodal)
- Performansı artırmak için modelleri veriler üzerinde [İnce ayar (Fine-tuning)](/python/framework/use_cases/fine_tuning) yapma

Daha fazla örnek ve öğretici bağlantıları için [kullanım örnekleri](/python/framework/use_cases) belgelerimize göz atın.

### 👨‍👩‍👧‍👦 LlamaIndex Kimler İçindir?

LlamaIndex yeni başlayanlar, ileri düzey kullanıcılar ve aradaki herkes için araçlar sunar.

Üst düzey (high-level) API'miz, yeni başlayan kullanıcıların 5 satır kodla verilerini almasına ve sorgulamasına olanak tanır.

Daha karmaşık uygulamalar için alt düzey (lower-level) API'lerimiz; ileri düzey kullanıcıların veri bağlayıcıları, indeksler, geri getiriciler (retrievers), sorgu motorları ve yeniden sıralama (reranking) modülleri gibi her türlü modülü ihtiyaçlarına göre özelleştirmesine ve genişletmesine olanak tanır.

## Başlangıç

LlamaIndex, Python (bu belgeler) ve [Typescript](https://ts.llamaindex.ai/) dillerinde mevcuttur. Nereden başlayacağınızdan emin değilseniz, deneyim seviyenize göre sizi doğru yere yönlendirecek olan [bu belgeler nasıl okunur](/python/framework/getting_started/reading) bölümünü okumanızı öneririz.

### 30 saniyelik hızlı başlangıç

Bir [OpenAI API anahtarı](https://platform.openai.com/api-keys) ile `OPENAI_API_KEY` adlı bir ortam değişkeni ayarlayın. Python kütüphanesini yükleyin:

```bash
pip install llama-index
```

Bazı belgeleri `data` adlı bir klasöre koyun, ardından ünlü 5 satırlık başlangıç kodumuzla onlara sorular sorun:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Veriler hakkında bir soru buraya gelmelidir")
print(response)
```

Eğer herhangi bir kısım sizi zorlarsa endişelenmeyin! [OpenAI gibi uzak API'leri](/python/framework/getting_started/starter_example) veya [dizüstü bilgisayarınızda çalışan herhangi bir modeli](/python/framework/getting_started/starter_example_local) kullanan daha kapsamlı başlangıç öğreticilerimize göz atın.

## LlamaCloud

Kurumsal bir geliştiriciyseniz [**LlamaCloud**](https://llamaindex.ai/enterprise)'ı inceleyin. Belge ayrıştırma, çıkarma, indeksleme ve geri getirme için uçtan uca yönetilen bir servistir; AI ajanınız için üretim kalitesinde veriler elde etmenizi sağlar. [Kaydolabilir](https://cloud.llamaindex.ai/) ve ayda 10.000 ücretsiz kredi alabilir, [planlarımızdan](https://www.llamaindex.ai/pricing) birine abone olabilir veya kurumsal bir çözümle ilgileniyorsanız [bizimle iletişime geçebilirsiniz](https://www.llamaindex.ai/contact). Hem SaaS hem de kendi sunucunuzda barındırabileceğiniz planlar sunuyoruz.

Daha fazla ayrıntı için [LlamaCloud belgelerine](https://docs.cloud.llamaindex.ai/) de göz atabilirsiniz.

- **Belge Ayrıştırma (LlamaParse)**: LlamaParse, sınıfının en iyisi belge ayrıştırma çözümüdür. VLM'ler (Görsel Dil Modelleri) ile desteklenir ve en karmaşık belgeler (iç içe geçmiş tablolar, gömülü grafikler/resimler ve daha fazlası) için bile mükemmeldir. [Daha fazla bilgi edinin](https://www.llamaindex.ai/llamaparse) veya [belgeleri](https://docs.cloud.llamaindex.ai/llamaparse) inceleyin.
- **Belge Çıkarma (LlamaExtract)**: İnsan tarafından tanımlanmış veya çıkarımlanmış bir şemaya dayanarak, herhangi bir belgeden yapıılmış veriler çıkarın. [Daha fazla bilgi edinin](https://www.llamaindex.ai/llamaextract) veya [belgeleri](https://docs.cloud.llamaindex.ai/llamaextract/getting_started) inceleyin.
- **İndeksleme/Geri Getirme**: Geri getirme için bir belge koleksiyonunu indekslemek üzere uçtan uca bir bor hattı kurun. Veri kaynağınızı (örneğin Sharepoint, Google Drive, S3) ve vektör veritabanı hedefinizi bağlayın; belge işleme ve senkronizasyon işlemlerini biz otomatik olarak hallederiz. [Daha fazla bilgi edinin](https://www.llamaindex.ai/enterprise) veya [belgeleri](https://docs.cloud.llamaindex.ai/llamacloud/getting_started) inceleyin.

## Topluluk

Yardıma mı ihtiyacınız var? Bir özellik öneriniz mi var? LlamaIndex topluluğuna katılın:

- [Twitter](https://twitter.com/llama_index)
- [Discord](https://discord.gg/dGcwcsnxhU)
- [LinkedIn](https://www.linkedin.com/company/llamaindex/)

### Kütüphaneyi Edinme

- LlamaIndex Python
  - [LlamaIndex Python Github](https://github.com/run-llama/llama_index)
  - [Python Belgeleri](https://docs.llamaindex.ai/) (şu an okuduğunuz yer)
  - [PyPi üzerinde LlamaIndex](https://pypi.org/project/llama-index/)
- LlamaIndex.TS (Typescript/Javascript paketi):
  - [LlamaIndex.TS Github](https://github.com/run-llama/LlamaIndexTS)
  - [TypeScript Belgeleri](https://ts.llamaindex.ai/)
  - [npm üzerinde LlamaIndex.TS](https://www.npmjs.com/package/llamaindex)

### Katkıda Bulunma

Açık kaynaklıyız ve projeye katkıları her zaman memnuniyetle karşılıyoruz! Çekirdek kütüphaneyi nasıl genişleteceğiniz veya LLM, vektör deposu, ajan aracı gibi üçüncü taraf entegrasyonlarını nasıl ekleyeceğinizle ilgili tüm ayrıntılar için [katkıda bulunma kılavuzumuza](https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md) göz atın.

## LlamaIndex Ekosistemi

LlamaIndex evreninde daha fazlası var! Diğer projelerimizden bazılarına göz atın:

- [llama_deploy](https://github.com/run-llama/llama_deploy) | Ajansal iş akışlarınızı üretim mikro servisleri olarak dağıtın
- [LlamaHub](https://llamahub.ai) | Özel veri bağlayıcılarından oluşan geniş (ve giderek büyüyen!) bir koleksiyon
- [SEC Insights](https://secinsights.ai) | Finansal araştırmalar için LlamaIndex destekli bir uygulama
- [create-llama](https://www.npmjs.com/package/create-llama) | LlamaIndex projelerini hızlıca oluşturmak için bir CLI aracı