# Retriever Modülleri (Retriever Modules)

Aktif olarak daha fazla özelleştirilmiş getirme (retrieval) kılavuzu ekliyoruz.
Bu sırada lütfen [API Referanslarına](/python/framework-api-reference/retrievers) göz atın.

## İndeks Retriever'lar (Index Retrievers)

Herhangi bir indeksten bir retriever'ın nasıl alınacağına dair daha fazla detay için lütfen [retriever modlarına](/python/framework/module_guides/querying/retriever/retriever_modes) bakın.

İlgili retriever'ları doğrudan içe aktarmak istiyorsanız lütfen [API referansımızı](/python/framework-api-reference/retrievers) kontrol edin.

## Kapsamlı Retriever Kılavuzları (Comprehensive Retriever Guides)

Birçoğu gelişmiş kavramları (otomatik getirme, yönlendirme, topluluk/ensembling ve daha fazlası) kapsayan çeşitli retriever modülleri hakkındaki kapsamlı kılavuzlarımıza göz atın.

### Gelişmiş Getirme ve Arama (Advanced Retrieval and Search)

Bu kılavuzlar gelişmiş getirme tekniklerini içerir. Bazıları anahtar kelime/hibrit arama, yeniden sıralama (reranking) ve daha fazlası gibi yaygın tekniklerdir. Bazıları ise small-to-big ve otomatik birleştirme (auto-merging) gibi LLM + RAG iş akışlarına özeldir.

-   [Özel Retriever Tanımlama](/python/examples/query_engine/customretrievers)
-   [BM25 Hibrit Retriever](/python/examples/retrievers/bm25_retriever)
-   [Basit Sorgu Füzyonu (Simple Query Fusion)](/python/examples/retrievers/simple_fusion)
-   [Karşılıklı Yeniden Sıralama Füzyonu (Reciprocal Rerank Fusion)](/python/examples/retrievers/reciprocal_rerank_fusion)
-   [Otomatik Birleştirme Retriever'ı (Auto Merging Retriever)](/python/examples/retrievers/auto_merging_retriever)
-   [Meta Veri Değiştirme (Metadata Replacement)](/python/examples/node_postprocessor/metadatareplacementdemo)
-   [Birleştirilebilir (Composable) Retriever'lar](/python/examples/retrievers/composable_retrievers)

### Otomatik Getirme (Auto-Retrieval)

Bu getirme teknikleri, semantik arama ile yapılandırılmış filtrelemeyi birleştiren **yarı yapılandırılmış** (semi-structured) sorgular gerçekleştirir.

-   [Otomatik Getirme (Pinecone ile)](/python/examples/vector_stores/pinecone_auto_retriever)
-   [Otomatik Getirme (Lantern ile)](/python/examples/vector_stores/lanternautoretriever)
-   [Otomatik Getirme (Chroma ile)](/python/examples/vector_stores/chroma_auto_retriever)
-   [Otomatik Getirme (BagelDB ile)](/python/examples/vector_stores/bagelautoretriever)
-   [Otomatik Getirme (Vectara ile)](/python/examples/retrievers/vectara_auto_retriever)
-   [Çoklu Döküman Otomatik Getirme](/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval)

### Bilgi Grafiği Retriever'lar (Knowledge Graph Retrievers)

-   [Bilgi Grafiği RAG Retriever'ı](/python/examples/query_engine/knowledge_graph_rag_query_engine)

### Birleşik Retriever'lar (Composed Retrievers)

Bunlar, diğer getirme tekniklerinin üzerine inşa edilen ve hiyerarşik getirme ile sorgu ayrıştırma (query decomposition) gibi daha üst düzey yetenekler sağlayan getirme teknikleridir.

-   [Sorgu Füzyonu (Query Fusion)](/python/examples/retrievers/reciprocal_rerank_fusion)
-   [Özyinelemeli Tablo Getirme (Recursive Table Retrieval)](/python/examples/query_engine/pdf_tables/recursive_retriever)
-   [Özyinelemeli Node Getirme (Recursive Node Retrieval)](/python/examples/retrievers/recursive_retriever_nodes)
-   [Braintrust](/python/examples/retrievers/recurisve_retriever_nodes_braintrust)
-   [Yönlendirici Retriever (Router Retriever)](/python/examples/retrievers/router_retriever)
-   [Topluluk Retriever'ı (Ensemble Retriever)](/python/examples/retrievers/ensemble_retrieval)
-   [Çoklu Döküman Otomatik Getirme](/python/examples/query_engine/multi_doc_auto_retrieval/multi_doc_auto_retrieval)

### Yönetilen Retriever'lar (Managed Retrievers)

-   [Google](/python/examples/managed/googledemo)
-   [Vectara](/python/examples/managed/vectarademo)
-   [VideoDB](/python/examples/retrievers/videodb_retriever)
-   [Amazon Bedrock](/python/examples/retrievers/bedrock_retriever)

### Diğer Retriever'lar

Bunlar herhangi bir kategoriye tam olarak uymayan ancak yine de vurgulanması gereken kılavuzlardır.

-   [Çoklu Döküman Hibrit](/python/examples/retrievers/multi_doc_together_hybrid)
-   [You Retriever](/python/examples/retrievers/you_retriever)
-   [Metinden SQL'e (Text-to-SQL)](/python/examples/index_structs/struct_indices/sqlindexdemo)
-   [DeepMemory (Activeloop)](/python/examples/retrievers/deep_memory)
-   [Pathway](/python/examples/retrievers/pathway_retriever)