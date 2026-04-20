# Üst Düzey Kavramlar

Bu, LLM uygulamaları oluştururken sıkça karşılaşacağınız üst düzey kavramlar için hızlı bir rehberdir.

## Büyük Dil Modelleri (Large Language Models - LLMs)

LLM'ler, LlamaIndex'in doğuşunu sağlayan temel inovasyondur. Bunlar; doğal dili anlayabilen, üretebilen ve işleyebilen; eğitim verilerine veya sorgu sırasında kendilerine sağlanan verilere dayanarak soruları yanıtlayabilen yapay zeka (AI) bilgisayar sistemleridir. [LLM'leri kullanma hakkında daha fazla bilgi edinebilirsiniz](/python/framework/understanding/using_llms).

## Ajansal Uygulamalar (Agentic Applications)

Bir LLM, bir uygulama içinde kullanıldığında; genellikle karar vermek, eyleme geçmek ve/veya dünyayla etkileşime girmek için kullanılır. Bu, bir **ajansal uygulamanın** temel tanımıdır.

Ajansal uygulama tanımı geniş olsa da, bu tür uygulamaları tanımlayan birkaç anahtar özellik vardır:

- **LLM Artırma (LLM Augmentation)**: LLM; araçlar (yani kod içindeki çağrılabilir fonksiyonlar), bellek ve/veya dinamik istemler (prompts) ile desteklenir.
- **İstem Zincirleme (Prompt Chaining)**: Birbirini takip eden birden fazla LLM çağrısı kullanılır; bir LLM çağrısının çıktısı bir sonrakinin girdisi olur.
- **Yönlendirme (Routing)**: LLM, uygulamayı bir sonraki uygun adıma veya duruma yönlendirmek için kullanılır.
- **Paralellik (Parallelism)**: Uygulama, birden fazla adımı veya eylemi paralel olarak gerçekleştirebilir.
- **Düzenleme (Orchestration)**: Alt düzey eylemleri ve LLM'leri koordine etmek için hiyerarşik bir LLM yapısı kullanılır.
- **Yansıtma (Reflection)**: LLM, önceki adımların veya LLM çağrılarının çıktılarını yansıtmak ve doğrulamak için kullanılır; bu, uygulamayı bir sonraki uygun adıma veya duruma yönlendirmek için rehberlik edebilir.

LlamaIndex'te, bir dizi adımı ve LLM'yi koordine etmek için `Workflow` sınıfını kullanarak ajansal uygulamalar oluşturabilirsiniz. [İş akışları hakkında daha fazla bilgi edinebilirsiniz](/python/llamaagents/workflows).

## Ajanlar (Agents)

Bir ajanı, bir "ajansal uygulamanın" belirli bir örneği olarak tanımlıyoruz. Ajan; LLM'leri diğer araçlar ve bellek ile birleştiren, hangi aracın bir sonraki adımda kullanılacağına (eğer varsa) karar veren bir akıl yürütme döngüsünde koordine edilen ve yarı otonom olarak görevleri yerine getiren bir yazılım parçasıdır.

Pratikte bu şuna benzer:

- Bir ajan kullanıcıdan mesaj alır.
- Ajan; önceki sohbet geçmişini, araçları ve en son kullanıcı mesajını kullanarak bir sonraki uygun eylemi belirlemek için bir LLM kullanır.
- Ajan, kullanıcının isteğine yardımcı olmak için bir veya daha fazla araç çağırabilir.
- Araçlar kullanılırsa, ajan araç çıktılarını yorumlar ve bunları bir sonraki eylemi belirlemek için kullanır.
- Ajan eylemde bulunmayı bıraktığında, nihai çıktıyı kullanıcıya döndürür.

[Ajanlar hakkında daha fazla bilgi edinebilirsiniz](/python/framework/understanding/agent).

## Geri Getirme Destekli Nesil (Retrieval Augmented Generation - RAG)

Geri Getirme Destekli Nesil (RAG), LlamaIndex ile veri destekli LLM uygulamaları oluşturmak için kullanılan temel bir tekniktir. LLM'ye sorgu anında verilerinizi sağlayarak, LLM'nin özel verileriniz hakkındaki soruları yanıtlamasına olanak tanır (LLM'yi verilerinizle eğitmeye gerek kalmaz). Her seferinde **tüm** verilerinizi LLM'ye göndermekten kaçınmak için RAG, verilerinizi indeksler ve sorgunuzla birlikte yalnızca ilgili kısımları seçerek gönderir. [RAG hakkında daha fazla bilgi edinebilirsiniz](/python/framework/understanding/rag).

## Kullanım Örnekleri

Veri destekli LLM uygulamaları için sayısız kullanım durumu vardır ancak bunlar kabaca beş kategoriye ayrılabilir:

[**Ajanlar (Agents)**](/python/framework/module_guides/deploying/agents):
Bir ajan, bir dizi [araç](/python/framework/module_guides/deploying/agents/tools) aracılığıyla dünyayla etkileşime giren, LLM destekli otomatik bir karar vericidir. Ajanlar, verilen bir görevi tamamlamak için rastgele sayıda adım atabilir ve önceden belirlenmiş adımları izlemek yerine en iyi eylem planına dinamik olarak karar verebilirler. Bu, ona daha karmaşık görevlerin üstesinden gelmek için ek esneklik sağlar.

[**İş Akışları (Workflows)**](/python/framework/llamaagents/workflows):
LlamaIndex'teki bir İş Akışı, bir dizi adımı ve LLM çağrısını düzenlemenize olanak tanıyan özel bir olay güdümlü soyutlamadır. İş akışları her türlü ajansal uygulamayı uygulamak için kullanılabilir ve LlamaIndex'in temel bir bileşenidir.

[**Yapılandırılmış Veri Çıkarma (Structured Data Extraction)**](/python/framework/use_cases/extraction):
Pydantic çıkarıcılar, verilerinizden çıkarılacak kesin bir veri yapısı belirlemenize ve eksik parçaları tip güvenli (type-safe) bir şekilde doldurmak için LLM'leri kullanmanıza olanak tanır. Bu, PDF'ler, web siteleri ve daha fazlası gibi yapılandırılmamış kaynaklardan yapılandırılmış veriler çıkarmak için yararlıdır ve iş akışlarını otomatikleştirmek için anahtardır.

[**Sorgu Motorları (Query Engines)**](/python/framework/module_guides/deploying/query_engine):
Bir sorgu motoru, verileriniz üzerinde soru sormanıza olanak tanıyan uçtan uca bir akıştır. Doğal dilde bir sorgu alır ve bir yanıtla birlikte, LLM'ye iletilen ve getirilen referans bağlamı döndürür.

[**Sohbet Motorları (Chat Engines)**](/python/framework/module_guides/deploying/chat_engines):
Bir sohbet motoru, verilerinizle bir sohbet gerçekleştirmek için uçtan uca bir akıştır (tek bir soru-cevap yerine karşılıklı etkileşim).

> **İpucu:**
> * [Nasıl özelleştirebileceğinizi](/python/framework/getting_started/faq) öğrenin.
> * [LlamaIndex'i Anlama](/python/framework/understanding) rehberimizle öğrenmeye devam edin.
> * Daha derinlere inmeye hazır mısınız? [Bileşen rehberlerine](/python/framework/module_guides) göz atın.