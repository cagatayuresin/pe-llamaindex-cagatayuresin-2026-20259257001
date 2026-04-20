# Retriever Modları (Retriever Modes)

Burada `retriever_mode` yapılandırmasından seçilen retriever sınıfına olan eşlemeyi gösteriyoruz.

> `retriever_mode` değerinin farklı indeks sınıfları için farklı anlamlar taşıyabileceğini unutmayın.

## Vektör İndeksi (Vector Index)

`retriever_mode` belirtmenin bir etkisi yoktur (sessizce yoksayılır).
`vector_index.as_retriever(...)` her zaman bir VectorIndexRetriever döndürür.

## Özet İndeksi (Summary Index)

-   `default`: SummaryIndexRetriever
-   `embedding`: SummaryIndexEmbeddingRetriever
-   `llm`: SummaryIndexLLMRetriever

## Ağaç İndeksi (Tree Index)

-   `select_leaf`: TreeSelectLeafRetriever
-   `select_leaf_embedding`: TreeSelectLeafEmbeddingRetriever
-   `all_leaf`: TreeAllLeafRetriever
-   `root`: TreeRootRetriever

## Anahtar Kelime Tablosu İndeksi (Keyword Table Index)

-   `default`: KeywordTableGPTRetriever
-   `simple`: KeywordTableSimpleRetriever
-   `rake`: KeywordTableRAKERetriever

## Bilgi Grafiği İndeksi (Knowledge Graph Index)

-   `keyword`: KGTableRetriever
-   `embedding`: KGTableRetriever
-   `hybrid`: KGTableRetriever

## Döküman Özeti İndeksi (Document Summary Index)

-   `llm`: DocumentSummaryIndexLLMRetriever
-   `embedding`: DocumentSummaryIndexEmbeddingRetrievers