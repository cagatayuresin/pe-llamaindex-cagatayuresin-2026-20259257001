# Vektör Depoları (Vector Stores)

Vektör depoları (vector stores), alınan döküman parçalarının embedding vektörlerini (ve bazen döküman parçalarının kendilerini de) içerir.

## Basit Vektör Deposu (Simple Vector Store)

Varsayılan olarak LlamaIndex, hızlı denemeler için harika olan basit bir bellek içi (in-memory) vektör deposu kullanır.
`vector_store.persist()` (ve sırasıyla `SimpleVectorStore.from_persist_path(...)`) çağrılarak diskte kalıcı hale getirilebilirler (ve diskten yüklenebilirler).

## Vektör Deposu Seçenekleri ve Özellik Desteği

LlamaIndex 20'den fazla farklı vektör deposu seçeneğini destekler.
Aktif olarak daha fazla entegrasyon ekliyor ve her biri için özellik kapsamını geliştiriyoruz.

| Vektör Deposu              | Tür                            | Meta Veri Filtreleme | Hibrit Arama | Silme | Dökümanları Saklama | Asenkron                      |
| -------------------------- | ------------------------------ | -------------------- | ------------ | ----- | ------------------- | ----------------------------- |
| Alibaba Cloud OpenSearch   | bulut                          | ✓                    |              | ✓     | ✓                   | ✓                             |
| Apache Cassandra®         | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| Astra DB                   | bulut                          | ✓                    |              | ✓     | ✓                   |                               |
| Azure AI Search            | bulut                          | ✓                    | ✓            | ✓     | ✓                   |                               |
| Azure CosmosDB Mongo vCore | bulut                          |                      |              | ✓     | ✓                   |                               |
| Azure CosmosDB NoSql       | bulut                          |                      |              | ✓     | ✓                   |                               |
| BaiduVectorDB              | bulut                          | ✓                    | ✓            |       | ✓                   |                               |
| ChatGPT Retrieval Plugin   | birleştirici (aggregator)      |                      |              | ✓     | ✓                   |                               |
| Chroma                     | yerel barındırma               | ✓                    |              | ✓     | ✓                   |                               |
| Couchbase                  | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| DashVector                 | bulut                          | ✓                    | ✓            | ✓     | ✓                   |                               |
| Databricks                 | bulut                          | ✓                    |              | ✓     | ✓                   |                               |
| Deeplake                   | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| DocArray                   | birleştirici (aggregator)      | ✓                    |              | ✓     | ✓                   |                               |
| DuckDB                     | bellek içi / yerel barındırma  | ✓                    |              | ✓     | ✓                   |                               |
| DynamoDB                   | bulut                          |                      |              | ✓     |                     |                               |
| Elasticsearch              | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   | ✓                             |
| FAISS                      | bellek içi                     |                      |              |       |                     |                               |
| Google AlloyDB             | bulut                          | ✓                    |              | ✓     | ✓                   | ✓                             |
| Google Cloud SQL Postgres  | bulut                          | ✓                    |              | ✓     | ✓                   | ✓                             |
| Hnswlib                    | bellek içi                     |                      |              |       |                     |                               |
| txtai                      | bellek içi                     |                      |              |       |                     |                               |
| Jaguar                     | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| LanceDB                    | bulut                          | ✓                    |              | ✓     | ✓                   |                               |
| Lantern                    | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   | ✓                             |
| MongoDB Atlas              | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| MyScale                    | bulut                          | ✓                    | ✓            | ✓     | ✓                   |                               |
| Milvus / Zilliz            | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| Neo4jVector                | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| OpenSearch                 | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   | ✓                             |
| Pinecone                   | bulut                          | ✓                    | ✓            | ✓     | ✓                   |                               |
| Postgres                   | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   | ✓                             |
| pgvecto.rs                 | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| Qdrant                     | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   | ✓                             |
| Redis                      | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| S3                         | bulut                          | ✓                    |              | ✓     | ✓                   | ✓\* (asyncio.to_thread ile) |
| Simple                     | bellek içi                     | ✓                    |              | ✓     |                     |                               |
| SingleStore                | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| Supabase                   | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| Tablestore                 | bulut                          | ✓                    | ✓            | ✓     | ✓                   |                               |
| Tair                       | bulut                          | ✓                    |              | ✓     | ✓                   |                               |
| TiDB                       | bulut                          | ✓                    |              | ✓     | ✓                   |                               |
| TencentVectorDB            | bulut                          | ✓                    | ✓            | ✓     | ✓                   |                               |
| Timescale                  |                                | ✓                    |              | ✓     | ✓                   | ✓                             |
| Typesense                  | yerel barındırma / bulut       | ✓                    |              | ✓     | ✓                   |                               |
| Upstash                    | bulut                          |                      |              |       | ✓                   |                               |
| VectorX DB                 | bulut                          | ✓                    | ✓            | ✓     | ✓                   | ✓                             |
| Vearch                     | yerel barındırma               | ✓                    |              | ✓     | ✓                   |                               |
| Vespa                      | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| Vertex AI Vector Search    | bulut                          | ✓                    |              | ✓     | ✓                   |                               |
| Weaviate                   | yerel barındırma / bulut       | ✓                    | ✓            | ✓     | ✓                   |                               |
| WordLift                   | bulut                          | ✓                    | ✓            | ✓     | ✓                   | ✓                             |

Daha fazla detay için [Vektör Deposu Entegrasyonları](/python/framework/community/integrations/vector_stores) dökümanına bakın.

## Örnek Not Defterleri

-   [Alibaba Cloud OpenSearch](/python/examples/vector_stores/alibabacloudopensearchindexdemo)
-   [Astra DB](/python/examples/vector_stores/astradbindexdemo)
-   [Asenkron İndeks Oluşturma](/python/examples/vector_stores/asyncindexcreationdemo)
-   [Azure AI Search](/python/examples/vector_stores/azureaisearchindexdemo)
-   [Azure Cosmos DB Mongo vCore](/python/examples/vector_stores/azurecosmosdbmongodbvcoredemo)
-   [Azure Cosmos DB NoSql](/python/examples/vector_stores/azurecosmosdbnosqldemo)
-   [Baidu](/python/examples/vector_stores/baiduvectordbindexdemo)
-   [Cassandra](/python/examples/vector_stores/cassandraindexdemo)
-   [Chromadb](/python/examples/vector_stores/chromaindexdemo)
-   [Couchbase](/python/examples/vector_stores/couchbasevectorstoredemo)
-   [Dash](/python/examples/vector_stores/dashvectorindexdemo)
-   [Databricks](/python/examples/vector_stores/databricksvectorsearchdemo)
-   [Deeplake](/python/examples/vector_stores/deeplakeindexdemo)
-   [DocArray HNSW](/python/examples/vector_stores/docarrayhnswindexdemo)
-   [DocArray Bellek İçi](/python/examples/vector_stores/docarrayinmemoryindexdemo)
-   [DuckDB](/python/examples/vector_stores/duckdbdemo)
-   [Espilla](/python/examples/vector_stores/epsillaindexdemo)
-   [Google AlloyDB for PostgreSQL](/python/examples/vector_stores/alloydbvectorstoredemo)
-   [Google Cloud SQL for PostgreSQL](/python/examples/vector_stores/cloudsqlpgvectorstoredemo)
-   [Jaguar](/python/examples/vector_stores/jaguarindexdemo)
-   [LanceDB](/python/examples/vector_stores/lancedbindexdemo)
-   [Lantern](/python/examples/vector_stores/lanternindexdemo)
-   [Milvus](/python/examples/vector_stores/milvusindexdemo)
-   [Milvus Async API](/python/examples/vector_stores/milvusasyncapidemo)
-   [Milvus Tam Metin Arama](/python/examples/vector_stores/milvusfulltextsearchdemo)
-   [Milvus Hibrit Arama](/python/examples/vector_stores/milvushybridindexdemo)
-   [MyScale](/python/examples/vector_stores/myscaleindexdemo)
-   [ElasticSearch](/python/examples/vector_stores/elasticsearchindexdemo)
-   [FAISS](/python/examples/vector_stores/faissindexdemo)
-   [Hnswlib](/python/examples/vector_stores/hnswlibindexdemo)
-   [MongoDB Atlas](/python/examples/vector_stores/mongodbatlasvectorsearch)
-   [Neo4j](/python/examples/vector_stores/neo4jvectordemo)
-   [OpenSearch](/python/examples/vector_stores/opensearchdemo)
-   [Pinecone](/python/examples/vector_stores/pineconeindexdemo)
-   [Pinecone Hibrit Arama](/python/examples/vector_stores/pineconeindexdemo-hybrid)
-   [PGvectoRS](/python/examples/vector_stores/pgvectorsdemo)
-   [Postgres](/python/examples/vector_stores/postgres)
-   [Redis](/python/examples/vector_stores/redisindexdemo)
-   [Qdrant](/python/examples/vector_stores/qdrantindexdemo)
-   [Qdrant Hibrit Arama](/python/examples/vector_stores/qdrant_hybrid)
-   [Rockset](/python/examples/vector_stores/rocksetindexdemo)
-   [S3](/python/examples/vector_stores/s3vectorstore)
-   [Basit (Simple)](/python/examples/vector_stores/simpleindexdemo)
-   [Supabase](/python/examples/vector_stores/supabasevectorindexdemo)
-   [Tablestore](/python/examples/vector_stores/tablestoredemo)
-   [Tair](/python/examples/vector_stores/tairindexdemo)
-   [TiDB](/python/examples/vector_stores/tidbvector)
-   [Tencent](/python/examples/vector_stores/tencentvectordbindexdemo)
-   [Timescale](/python/examples/vector_stores/timescalevector)
-   [Upstash](/python/examples/vector_stores/upstashvectordemo)
-   [VectorX DB](/python/examples/vector_stores/vectorxdbdemo)
-   [Vearch](/python/examples/vector_stores/vearchdemo)
-   [Vespa](/python/examples/vector_stores/vespaindexdemo)
-   [Vertex AI Vector Search](/python/examples/vector_stores/vertexaivectorsearchdemo)
-   [Weaviate](/python/examples/vector_stores/weaviateindexdemo)
-   [Weaviate Hibrit Arama](/python/examples/vector_stores/weaviateindexdemo-hybrid)
-   [WordLift](/python/examples/vector_stores/wordliftdemo)
-   [Zep](/python/examples/vector_stores/zepindexdemo)