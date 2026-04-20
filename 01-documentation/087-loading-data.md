# Veri Yükleme (Loading Data)

LlamaIndex'te veri almanın (ingestion) anahtarı yükleme ve dönüşümlerdir (transformations). Dökümanları (Documents) bir kez yükledikten sonra, bunları dönüşümler yoluyla işleyebilir ve Node'lar olarak çıktı alabilirsiniz.

"Anlamak" (Understanding) bölümümüzde [veri yüklemenin temellerini öğrendikten](/python/framework/understanding/rag/loading) sonra, daha fazlasını öğrenmek için okumaya devam edebilirsiniz:

### Yükleme (Loading)

-   [SimpleDirectoryReader](/python/framework/module_guides/loading/simpledirectoryreader), yerel bir dizinden her türlü dosya türünü yüklemek için yerleşik yükleyicimiz.
-   [LlamaParse](/python/framework/module_guides/loading/connector/llama_parse), LlamaIndex'in PDF ayrıştırma (parsing) için sunduğu, yönetilen bir API olarak mevcut resmi aracı.
-   [LlamaHub](/python/framework/module_guides/loading/connector), herhangi bir kaynaktan veri almak için yüzlerce veri yükleme kütüphanesinden oluşan kayıt defterimiz (registry).

### Dönüşümler (Transformations)

Bu, metni bölme gibi yaygın işlemleri içerir.

-   [Node Parser Kullanım Kalıbı](/python/framework/module_guides/loading/node_parsers), node parser'larımızı (düğüm ayrıştırıcıları) nasıl kullanacağınızı gösterir.
-   [Node Parser Modülleri](/python/framework/module_guides/loading/node_parsers/modules), metin bölücülerimizi (cümle, token, HTML, JSON) ve diğer ayrıştırıcı modüllerimizi gösterir.

### Hepsini Bir Araya Getirmek

-   [Veri Alma Boru Hattı (Ingestion Pipeline)](/python/framework/module_guides/loading/ingestion_pipeline), veri yüklemek için tekrarlanabilir, önbellek optimizasyonlu bir süreç kurmanıza olanak tanır.

### Soyutlamalar (Abstractions)

-   [Döküman (Document) ve Node Nesneleri](/python/framework/module_guides/loading/documents_and_nodes) ve bunların daha gelişmiş kullanım durumları için nasıl özelleştirileceği.