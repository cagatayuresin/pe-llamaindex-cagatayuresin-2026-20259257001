# Bileşen Kılavuzları (Component Guides)

LlamaIndex bileşen kılavuzlarına hoş geldiniz! Bu bölüm, LlamaIndex çerçevesinin tüm temel modülleri ve bileşenleri için ayrıntılı belgeler sağlar.

## Temel Bileşenler

### Modeller (Models)

-   [Modellere Giriş](/python/framework/module_guides/models) - Model bileşenlerine genel bakış
-   [LLM'ler](/python/framework/module_guides/models/llms) - Metin oluşturma ve akıl yürütme için dil modelleri
-   [Embedding'ler](/python/framework/module_guides/models/embeddings) - Metni vektör temsillerine dönüştürme
-   [Çok Modlu (Multi Modal)](/python/framework/module_guides/models/multi_modal) - Görüntüler, ses ve diğer metin dışı verilerle çalışma

### İstemler (Prompts)

-   [İstemlere Giriş](/python/framework/module_guides/models/prompts) - İstem mühendisliğine (prompt engineering) genel bakış
-   [Kullanım Kalıpları](/python/framework/module_guides/models/prompts/usage_pattern) - İstemlerin etkili bir şekilde nasıl kullanılacağını öğrenin

### Yükleme (Loading)

-   [Yüklemeye Giriş](/python/framework/module_guides/loading) - Veri yükleme yeteneklerine genel bakış
-   [Dökümanlar ve Node'lar](/python/framework/module_guides/loading/documents_and_nodes) - Temel veri yapıları
-   [SimpleDirectoryReader](/python/framework/module_guides/loading/simpledirectoryreader) - Kolay döküman yükleme
-   [Veri Bağlayıcıları (Data Connectors)](/python/framework/module_guides/loading/connector) - Harici veri kaynaklarına bağlanma
-   [Node Ayrıştırıcılar / Metin Bölücüler](/python/framework/module_guides/loading/node_parsers) - Dökümanları parçalara ayırma
-   [Veri Alma Boru Hattı (Ingestion Pipeline)](/python/framework/module_guides/loading/ingestion_pipeline) - Uçtan uca döküman işleme

### İndeksleme (Indexing)

-   [İndekslemeye Giriş](/python/framework/module_guides/indexing) - İndeksleme yaklaşımlarına genel bakış
-   [İndeks Kılavuzu](/python/framework/module_guides/indexing/index_guide) - İndekslere dair kapsamlı kılavuz
-   [Vektör Deposu İndeksi (Vector Store Index)](/python/framework/module_guides/indexing/vector_store_index) - Vektörlerle anlamsal arama
-   [Özellik Grafiği İndeksi (Property Graph Index)](/python/framework/module_guides/indexing/lpg_index_guide) - Grafik tabanlı indeksleme

### Saklama (Storing)

-   [Saklamaya Giriş](/python/framework/module_guides/storing) - Depolama bileşenlerine genel bakış
-   [Vektör Depoları (Vector Stores)](/python/framework/module_guides/storing/vector_stores) - Getirme için embedding'leri saklama
-   [Döküman Depoları (Document Stores)](/python/framework/module_guides/storing/docstores) - Döküman koleksiyonlarını kalıcı hale getirme
-   [İndeks Depoları (Index Stores)](/python/framework/module_guides/storing/index_stores) - İndeks meta verilerini saklama

### Sorgulama (Querying)

-   [Sorgulamaya Giriş](/python/framework/module_guides/querying) - Sorgu bileşenlerine genel bakış
-   [Sorgu Motorları (Query Engines)](/python/framework/module_guides/deploying/query_engine) - Sorguları işleme ve yanıtlama
-   [Sohbet Motorları (Chat Engines)](/python/framework/module_guides/deploying/chat_engines) - Diyalog bazlı arayüzler oluşturma
-   [Getirme (Retrieval)](/python/framework/module_guides/querying/retriever) - İlgili bağlamı getirme
-   [Yanıt Sentezleme (Response Synthesis)](/python/framework/module_guides/querying/response_synthesizers) - Tutarlı yanıtlar oluşturma

## Gelişmiş Bileşenler

### Ajanlar (Agents)

-   [Ajanlara Giriş](/python/framework/module_guides/deploying/agents) - Ajan yeteneklerine genel bakış
-   [Bellek (Memory)](/python/framework/module_guides/deploying/agents/memory) - Ajanlara diyalog belleği ekleme
-   [Araçlar (Tools)](/python/framework/module_guides/deploying/agents/tools) - Harici araçlarla yetenekleri genişletme

### İş Akışları (Workflows)

-   [İş Akışlarına Giriş](/python/framework/module_guides/workflow) - Karmaşık, çok adımlı yapay zeka iş akışları oluşturun

### Değerlendirme (Evaluation)

-   [Değerlendirmeye Giriş](/python/framework/module_guides/evaluating) - Değerlendirme çerçevelerine genel bakış
-   [Kullanım Kalıpları](/python/framework/module_guides/evaluating/usage_pattern) - Uygulamalarınızı test edin ve iyileştirin
-   [LlamaDatasets](/python/framework/module_guides/evaluating/contributing_llamadatasets) - Standartlaştırılmış değerlendirme veri kümeleri

### Gözlemlenebilirlik (Observability)

-   [Gözlemlenebilirliğe Giriş](/python/framework/module_guides/observability) - İzleme yeteneklerine genel bakış
-   [Enstrümantasyon (Instrumentation)](/python/framework/module_guides/observability/instrumentation) - Uygulamalarınızı izleyin ve hatalarını ayıklayın

### Ayarlar (Settings)

-   [Ayarlar Yapılandırması (Settings Configuration)](/python/framework/module_guides/supporting_modules/settings) - Küresel LlamaIndex ayarlarını yapılandırın