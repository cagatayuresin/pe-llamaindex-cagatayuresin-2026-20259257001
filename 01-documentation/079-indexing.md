# İndeksleme (Indexing)

## Kavram

Bir "İndeks", bir kullanıcı sorgusu için ilgili bağlamı hızlı bir şekilde getirmemizi sağlayan bir veri yapısıdır. LlamaIndex için bu, getirme ile zenginleştirilmiş oluşturma (RAG) kullanım durumlarının temel dayanağıdır.

Üst düzeyde, `İndeksler`, [Dökümanlardan (Documents)](/python/framework/module_guides/loading/documents_and_nodes) oluşturulur. Verileriniz üzerinden soru-cevap ve sohbet imkanı sağlayan [Sorgu Motorlarını (Query Engines)](/python/framework/module_guides/deploying/query_engine) ve [Sohbet Motorlarını (Chat Engines)](/python/framework/module_guides/deploying/chat_engines) oluşturmak için kullanılırlar.

Perde arkasında `İndeksler`, verileri `Node` (asıl dökümanların parçalarını temsil eder) nesnelerinde saklar ve ek yapılandırma ile otomasyonu destekleyen bir [Retriever (Getirici)](/python/framework/module_guides/querying/retriever) arayüzü sunar.

Açık ara en yaygın indeks `VectorStoreIndex`'tir; başlamak için en iyi yer [VectorStoreIndex kullanım kılavuzudur](/python/framework/module_guides/indexing/vector_store_index).

Diğer indeksler için, kullanım durumunuza hangisinin uygun olduğuna karar vermenize yardımcı olacak [her bir indeksin nasıl çalıştığına](/python/framework/module_guides/indexing/index_guide) dair kılavuzumuza göz atın.

## Diğer İndeks Kaynakları

[Modül kılavuzuna](/python/framework/module_guides/indexing/modules) bakın.