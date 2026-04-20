---
title: Elasticsearch Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Elasticsearch Vektör Deposu

Elasticsearch, Apache Lucene üzerine inşa edilmiş dağıtık, RESTful bir arama ve analitik motorudur. Yoğun vektör erişimi (dense vector retrieval), seyrek vektör erişimi (sparse vector retrieval), anahtar kelime araması ve hibrit arama dahil olmak üzere farklı erişim seçenekleri sunar.

Elastic Cloud'un ücretsiz deneme sürümü için [kaydolun](https://cloud.elastic.co/registration?utm_source=llama-index\&utm_content=documentation) veya aşağıda açıklandığı gibi yerel bir sunucu çalıştırın.

Elasticsearch 8.9.0 veya üzeri sürüm ve AIOHTTP gerektirir.

```bash
%pip install -qU llama-index-vector-stores-elasticsearch llama-index openai
```

```python
import getpass
import os


import openai


os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Anahtarı:")


openai.api_key = os.environ["OPENAI_API_KEY"]
```

## Elasticsearch'ü Çalıştırma ve Bağlanma

Kullanım için bir Elasticsearch örneği kurmanın iki yolu vardır:

### Elastic Cloud

Elastic Cloud, yönetilen bir Elasticsearch servisidir. Ücretsiz deneme için [kaydolun](https://cloud.elastic.co/registration?utm_source=llama-index\&utm_content=documentation).

### Yerel Olarak (Locally)

Elasticsearch'ü yerel olarak çalıştırarak başlayın. En kolay yol resmi Elasticsearch Docker imajını kullanmaktır. Daha fazla bilgi için Elasticsearch Docker dokümantasyonuna bakın.

Terminal penceresi

```bash
docker run -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.license.self_generated.type=trial" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.2
```

## ElasticsearchStore Yapılandırması

`ElasticsearchStore` sınıfı, bir Elasticsearch örneğine bağlanmak için kullanılır. Aşağıdaki parametreleri gerektirir:

```text
    - index_name: Elasticsearch indeksinin adı. Gerekli.
    - es_client: İsteğe bağlı. Önceden var olan Elasticsearch istemcisi.
    - es_url: İsteğe bağlı. Elasticsearch URL'si.
    - es_cloud_id: İsteğe bağlı. Elasticsearch bulut kimliği (cloud ID).
    - es_api_key: İsteğe bağlı. Elasticsearch API anahtarı.
    - es_user: İsteğe bağlı. Elasticsearch kullanıcı adı.
    - es_password: İsteğe bağlı. Elasticsearch parolası.
    - text_field: İsteğe bağlı. Metni saklayan Elasticsearch alanının adı.
    - vector_field: İsteğe bağlı. Gömmeyi (embedding) saklayan Elasticsearch alanının adı.
    - batch_size: İsteğe bağlı. Toplu indeksleme için yığın boyutu. Varsayılan 200.
    - distance_strategy: İsteğe bağlı. Benzerlik araması için kullanılacak mesafe stratejisi.
                    Varsayılan "COSINE".
```

### Örnek: Yerel olarak bağlanma

```python
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


es = ElasticsearchStore(
    index_name="benim_indeksim",
    es_url="http://localhost:9200",
)
```

### Örnek: Kullanıcı adı ve parola ile Elastic Cloud'a bağlanma

```python
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


es = ElasticsearchStore(
    index_name="benim_indeksim",
    es_cloud_id="<cloud-id>", # dağıtım (deployment) sayfasında bulunur
    es_user="elastic",
    es_password="<parola>" # dağıtım oluşturulurken verilir. Alternatif olarak parola sıfırlanabilir.
)
```

### Örnek: API Anahtarı ile Elastic Cloud'a bağlanma

```python
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


es = ElasticsearchStore(
    index_name="benim_indeksim",
    es_cloud_id="<cloud-id>", # dağıtım sayfasında bulunur
    es_api_key="<api-key>" # Kibana içinden bir API anahtarı oluşturun (Security -> API Keys)
)
```

#### Örnek veri

```python
from llama_index.core.schema import TextNode


movies = [
    TextNode(
        text="İki mafya tetikçisinin, bir boksörün, bir gangster ve karısının ve bir çift lokanta haydutunun hayatları dört şiddet ve kurtuluş öyküsünde birbirine geçiyor.",
        metadata={"title": "Ucuz Roman (Pulp Fiction)"},
    ),
    TextNode(
        text="Joker olarak bilinen tehdit Gotham halkına yıkım ve kaos getirdiğinde, Batman adaletsizlikle savaşma yeteneğinin en büyük psikolojik ve fiziksel testlerinden birini kabul etmelidir.",
        metadata={"title": "Kara Şövalye (The Dark Knight)"},
    ),
    TextNode(
        text="Uykusuzluk çeken bir ofis çalışanı ve başına buyruk bir sabun üreticisi, çok ama çok daha fazlasına dönüşen bir yeraltı dövüş kulübü kurarlar.",
        metadata={"title": "Dövüş Kulübü (Fight Club)"},
    ),
    TextNode(
        text="Rüya paylaşım teknolojisini kullanarak kurumsal sırları çalan bir hırsıza, bir CEO'nun zihnine bir fikir yerleştirmek gibi ters bir görev verilir.",
        metadata={"title": "Başlangıç (Inception)"},
    ),
    TextNode(
        text="Bir bilgisayar korsanı, gizemli isyancılardan gerçekliğinin gerçek doğasını ve kontrolörlerine karşı savaştaki rolünü öğrenir.",
        metadata={"title": "Matrix (The Matrix)"},
    ),
    TextNode(
        text="Biri çaylak diğeri deneyimli iki dedektif, yedi ölümcül günahı motif olarak kullanan bir seri katilin peşine düşer.",
        metadata={"title": "Yedi (Se7en)"},
    ),
    TextNode(
        text="Organize bir suç hanedanının yaşlanan patriği, gizli imparatorluğunun kontrolünü isteksiz oğluna devreder.",
        metadata={"title": "Baba (The Godfather)", "theme": "Mafya"},
    ),
]
```

## Erişim Örnekleri

Bu bölüm, `ElasticsearchStore` aracılığıyla kullanılabilen farklı erişim seçeneklerini gösterir ve bunları bir `VectorStoreIndex` aracılığıyla kullanıma sunar.

```python
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
```

Önce kullanıcının sorgu girişi için sonuçları getiren ve yazdıran bir yardımcı fonksiyon tanımlıyoruz:

```python
def print_results(results):
    for rank, result in enumerate(results, 1):
        print(
            f"{rank}. başlık={result.metadata['title']} puan={result.get_score()} metin={result.get_text()}"
        )




def search(
    vector_store: ElasticsearchStore, nodes: list[TextNode], query: str
):
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)


    print(">>> Belgeler:")
    retriever = index.as_retriever()
    results = retriever.retrieve(query)
    print_results(results)


    print("\n>>> Cevap:")
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    print(response)
```

### Yoğun erişim (Dense retrieval)

Burada arama yapmak için OpenAI gömmelerini (embeddings) kullanıyoruz.

```python
from llama_index.vector_stores.elasticsearch import AsyncDenseVectorStrategy


dense_vector_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # Elastic Cloud kimlik doğrulaması için yukarıya bakın
    index_name="movies_dense",
    retrieval_strategy=AsyncDenseVectorStrategy(),
)


search(dense_vector_store, movies, "hangi film rüyalarla ilgili?")
```

```text
>>> Belgeler:
1. başlık=Başlangıç (Inception) puan=1.0 metin=Rüya paylaşım teknolojisini kullanarak kurumsal sırları çalan bir hırsıza, bir CEO'nun zihnine bir fikir yerleştirmek gibi ters bir görev verilir.


>>> Cevap:
Başlangıç (Inception)
```

Bu aynı zamanda varsayılan erişim stratejisidir:

```python
default_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # Elastic Cloud kimlik doğrulaması için yukarıya bakın
    index_name="movies_default",
)


search(default_store, movies, "hangi film rüyalarla ilgili?")
```

### Seyrek erişim (Sparse retrieval)

Bu örnek için önce Elasticsearch dağıtımınızda [ELSER modelinin](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html) ikinci sürümünü yayına almanız (deploy) gerekir.

```python
from llama_index.vector_stores.elasticsearch import AsyncSparseVectorStrategy


sparse_vector_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # Elastic Cloud kimlik doğrulaması için yukarıya bakın
    index_name="movies_sparse",
    retrieval_strategy=AsyncSparseVectorStrategy(model_id=".elser_model_2"),
)


search(sparse_vector_store, movies, "hangi film rüyalarla ilgili?")
```

### Anahtar kelime erişimi (Keyword retrieval)

Klasik tam metin aramasını kullanmak için BM25 stratejisini kullanabilirsiniz.

```python
from llama_index.vector_stores.elasticsearch import AsyncBM25Strategy


bm25_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # Elastic Cloud kimlik doğrulaması için yukarıya bakın
    index_name="movies_bm25",
    retrieval_strategy=AsyncBM25Strategy(),
)


search(bm25_store, movies, "joker")
```

### Hibrit erişim (Hybrid retrieval)

Hibrit erişim için yoğun erişim ve anahtar kelime aramasını birleştirmek bir bayrak (flag) ayarlanarak etkinleştirilebilir.

```python
from llama_index.vector_stores.elasticsearch import AsyncDenseVectorStrategy


hybrid_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # Elastic Cloud kimlik doğrulaması için yukarıya bakın
    index_name="movies_hybrid",
    retrieval_strategy=AsyncDenseVectorStrategy(hybrid=True),
)


search(hybrid_store, movies, "hangi film rüyalarla ilgili?")
```

### Meta Veri Filtreleri (Metadata Filters)

Belgelerimizin meta verilerine dayanarak sorgu motoruna filtreler de uygulayabiliriz.

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


metadata_store = ElasticsearchStore(
    es_url="http://localhost:9200",  # Elastic Cloud kimlik doğrulaması için yukarıya bakın
    index_name="movies_metadata",
)
storage_context = StorageContext.from_defaults(vector_store=metadata_store)
index = VectorStoreIndex(movies, storage_context=storage_context)


# Meta veri filtresi
filters = MetadataFilters(
    filters=[ExactMatchFilter(key="theme", value="Mafia")]
)
retriever = index.as_retriever(filters=filters)


results = retriever.retrieve("Başlangıç (Inception) ne hakkındadır?")
print_results(results)
```

```text
1. başlık=Baba (The Godfather) puan=1.0 metin=Organize bir suç hanedanının yaşlanan patriği, gizli imparatorluğunun kontrolünü isteksiz oğluna devreder.
```

## Özel Filtreler ve Sorguyu Geçersiz Kılma (Overriding Query)

Elasticsearch uygulaması şu anda yalnızca LlamaIndex'ten sağlanan `ExactMatchFilters`'ı desteklemektedir. Elasticsearch'ün kendisi; aralık filtreleri (range filters), coğrafi filtreler (geo filters) ve daha fazlasını içeren çok çeşitli filtreleri destekler. Bu filtreleri kullanmak için `es_filter` parametresine sözlükler listesi olarak iletebilirsiniz.

```python
def custom_query(query, query_str):
    print("özel sorgu (custom query)", query)
    return query




query_engine = index.as_query_engine(
    vector_store_kwargs={
        "es_filter": [{"match": {"title": "matrix"}}],
        "custom_query": custom_query,
    }
)
query_engine.query("bu film ne hakkında?")
```
