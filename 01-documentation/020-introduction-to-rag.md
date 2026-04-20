# RAG'e Giriş

> **İpucu:** Bunu okumadan önce henüz yapmadıysanız [LlamaIndex'i kurun](/python/framework/getting_started/installation) ve [başlangıç eğitimini](/python/framework/getting_started/starter_example) tamamlayın. Bu, bu adımları deneyimlerinizle temellendirmenize yardımcı olacaktır.

LLM'ler muazzam veri kütleleri üzerinde eğitilmiştir ancak **sizin** verileriniz üzerinde eğitilmemişlerdir. Veri Getirme ile Güçlendirilmiş Üretim (Retrieval-Augmented Generation - RAG), verilerinizi LLM'lerin zaten erişebildiği verilere ekleyerek bu sorunu çözer. Bu dökümantasyonda RAG referanslarıyla sıkça karşılaşacaksınız. Sorgu motorları, sohbet motorları ve ajanlar genellikle görevlerini tamamlamak için RAG kullanırlar.

RAG'de verileriniz yüklenir ve sorgular için hazırlanır veya "indekslenir". Kullanıcı sorguları, verilerinizi en alakalı bağlama (context) indirgeyen indeks üzerinde işlem yapar. Bu bağlam ve sorgunuz daha sonra bir komut (prompt) ile birlikte LLM'e gider ve LLM bir yanıt sağlar.

Oluşturduğunuz şey bir sohbet robotu veya bir ajan olsa bile, verileri uygulamanıza dahil etmek için RAG tekniklerini bilmek isteyeceksiniz.

![](./../../_static/getting_started/basic_rag.png)

### RAG İçindeki Aşamalar

RAG içinde beş temel aşama vardır ve bunlar oluşturduğunuz çoğu büyük uygulamanın bir parçası olacaktır. Bunlar:

- **Yükleme (Loading)**: Verilerinizi yaşadığı yerden (metin dosyaları, PDF'ler, başka bir web sitesi, veritabanı veya bir API olsun) iş akışınıza almayı ifade eder. [LlamaHub](https://llamahub.ai/) seçebileceğiniz yüzlerce bağlayıcı sağlar.

- **İndeksleme (Indexing)**: Verilerin sorgulanmasına olanak tanıyan bir veri yapısı oluşturmak anlamına gelir. LLM'ler için bu hemen hemen her zaman, verilerinizin anlamının sayısal temsilleri olan `vektör gömmeleri` (vector embeddings) oluşturmak ve bağlamsal olarak alakalı verileri doğru bir şekilde bulmayı kolaylaştırmak için sayısız diğer metadata stratejilerini kullanmak anlamına gelir.

- **Saklama (Storing)**: Verileriniz indekslendikten sonra, yeniden indeksleme yapmak zorunda kalmamak için indeksinizi ve diğer metadatalarınızı neredeyse her zaman saklamak isteyeceksiniz.

- **Sorgulama (Querying)**: Belirli bir indeksleme stratejisi için, alt sorgular, çok adımlı sorgular ve hibrit stratejiler dahil olmak üzere sorgulama yapmak için LLM'leri ve LlamaIndex veri yapılarını kullanabileceğiniz birçok yol vardır.

- **Değerlendirme (Evaluation)**: Herhangi bir akıştaki kritik bir adım, diğer stratejilere göre veya değişiklik yaptığınızda akışınızın ne kadar etkili olduğunu kontrol etmektir. Değerlendirme; sorgulara verdiğiniz yanıtların ne kadar doğru, sadık ve hızlı olduğuna dair nesnel ölçümler sağlar.

![](./../../_static/getting_started/stages.png)

### RAG İçindeki Önemli Kavramlar

Ayrıca bu aşamaların her birindeki adımları ifade eden bazı terimlerle karşılaşacaksınız.

#### Yükleme Aşaması

[**Node'lar ve Document'lar**](/python/framework/module_guides/loading/documents_and_nodes): Bir `Document`, herhangi bir veri kaynağı (örneğin bir PDF, bir API çıktısı veya bir veritabanından alınan veriler) etrafındaki bir kapsayıcıdır. Bir `Node`, LlamaIndex'teki atomik veri birimidir ve kaynak bir `Document`'ın bir "parçasını" (chunk) temsil eder. Node'ların, içinde bulundukları dökümanla ve diğer Node'larla ilişkilerini gösteren metadataları vardır.

[**Bağlayıcılar (Connectors)**](/python/framework/module_guides/loading/connector): Bir veri bağlayıcısı (genellikle `Reader` olarak adlandırılır), farklı veri kaynaklarından ve veri formatlarından verileri `Document`'lara ve `Node`'lara aktarır (ingest).

#### İndeksleme Aşaması

[**İndeksler (Indexes)**](/python/framework/module_guides/indexing): Verilerinizi aktardıktan sonra LlamaIndex, verileri getirilmesi kolay bir yapıda indekslemenize yardımcı olur. Bu genellikle, `vektör deposu` (vector store) adı verilen özel bir veritabanında saklanan `vektör gömmeleri` (vector embeddings) oluşturmayı içerir. İndeksler ayrıca verileriniz hakkında çeşitli metadatalar da saklayabilir.

[**Gömmeler (Embeddings)**](/python/framework/module_guides/models/embeddings): LLM'ler, verilerin `embeddings` adı verilen sayısal temsillerini oluşturur. Verilerinizi alaka düzeyine göre filtrelerken LlamaIndex, sorguları embedding'lere dönüştürecek ve vektör deponuz, sorgunuzun embedding'ine sayısal olarak benzeyen verileri bulacaktır.

#### Sorgulama Aşaması

[**Getiriciler (Retrievers)**](/python/framework/module_guides/querying/retriever): Bir getirici (retriever), bir sorgu verildiğinde bir indeksten ilgili bağlamın nasıl verimli bir şekilde getirileceğini tanımlar. Getirme stratejiniz, getirilen verilerin alaka düzeyi ve bunun gerçekleştirilme verimliliği için kilit öneme sahiptir.

[**Yönlendiriciler (Routers)**](/python/framework/module_guides/querying/router): Bir yönlendirici, bilgi tabanından ilgili bağlamı getirmek için hangi getiricinin kullanılacağını belirler. Daha spesifik olarak `RouterRetriever` sınıfı, bir sorguyu yürütmek için bir veya birden fazla aday getiriciyi seçmekten sorumludur. Her adayın metadatasını ve sorguyu temel alarak en iyi seçeneği seçmek için bir seçici (selector) kullanırlar.

[**Node Son İşleyiciler (Node Postprocessors)**](/python/framework/module_guides/querying/node_postprocessors): Bir node son işleyicisi, getirilen bir dizi node'u alır ve onlara dönüştürme, filtreleme veya yeniden sıralama (re-ranking) mantığı uygular.

[**Yanıt Sentezleyiciler (Response Synthesizers)**](/python/framework/module_guides/querying/response_synthesizers): Bir yanıt sentezleyici, bir kullanıcı sorgusu ve verilen bir dizi getirilen metin parçasını kullanarak bir LLM'den yanıt oluşturur.