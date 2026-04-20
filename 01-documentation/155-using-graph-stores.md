# Grafik Depolarını (Graph Stores) Kullanma

## `Neo4jGraphStore`

`Neo4j`, bir grafik deposu entegrasyonu olarak desteklenmektedir. LlamaIndex ve Neo4j kullanarak grafikleri kalıcı hale getirebilir, görselleştirebilir ve sorgulayabilirsiniz. Ayrıca, mevcut Neo4j grafikleri `text2cypher` ve `KnowledgeGraphQueryEngine` kullanılarak doğrudan desteklenir.

Daha önce hiç Neo4j kullanmadıysanız, masaüstü istemcisini [buradan](https://neo4j.com/download/) indirebilirsiniz.

İstemciyi açtıktan sonra yeni bir proje oluşturun ve `apoc` entegrasyonunu kurun. Tam talimatlar [burada](https://neo4j.com/labs/apoc/4.1/installation/). Sadece projenize tıklayın, sol menüden `Plugins` öğesini seçin, APOC'u kurun ve sunucunuzu yeniden başlatın.

[Neo4j Grafik Deposu (Neo4j Graph Store)](/python/examples/index_structs/knowledge_graph/neo4jkgindexdemo) kullanım örneğine bakın.

## `NebulaGraphStore`

Grafikleri doğrudan Nebula'da kalıcı hale getirmek için bir `NebulaGraphStore` entegrasyonunu destekliyoruz! Ayrıca, `KnowledgeGraphQueryEngine` kullanarak Nebula grafikleriniz için cypher sorguları oluşturabilir ve doğal dilde yanıtlar döndürebilirsiniz.

Aşağıdaki ilgili kılavuzlara bakın:

-   [Nebula Grafik Deposu (Nebula Graph Store)](/python/examples/index_structs/knowledge_graph/nebulagraphkgindexdemo)
-   [Bilgi Grafiği Sorgu Motoru (Knowledge Graph Query Engine)](/python/examples/query_engine/knowledge_graph_query_engine)

## `FalkorDBGraphStore`

Grafikleri doğrudan FalkorDB'de kalıcı hale getirmek için bir `FalkorDBGraphStore` entegrasyonunu destekliyoruz! Ayrıca, `KnowledgeGraphQueryEngine` kullanarak FalkorDB grafikleriniz için cypher sorguları oluşturabilir ve doğal dilde yanıtlar döndürebilirsiniz.

Aşağıdaki ilgili kılavuzlara bakın:

-   [FalkorDB Grafik Deposu (FalkorDB Graph Store)](/python/examples/index_structs/knowledge_graph/falkordbgraphdemo)

## `Amazon Neptune Grafik Depoları`

Grafik deposu entegrasyonu olarak hem [Neptune Database](https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview.html) hem de [Neptune Analytics](https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html) için `Amazon Neptune` entegrasyonlarını destekliyoruz.

Aşağıdaki ilgili kılavuzlara bakın:

-   [Amazon Neptune Grafik Deposu (Amazon Neptune Graph Store)](/python/examples/index_structs/knowledge_graph/neptunedatabasekgindexdemo).

## `TiDB Grafik Deposu`

Grafikleri doğrudan [TiDB](https://docs.pingcap.com/tidb/stable/overview) üzerinde kalıcı hale getirmek için bir `TiDBGraphStore` entegrasyonunu destekliyoruz!

Aşağıdaki ilgili kılavuzlara bakın:

-   [TiDB Grafik Deposu (TiDB Graph Store)](/python/examples/index_structs/knowledge_graph/tidbkgindexdemo)