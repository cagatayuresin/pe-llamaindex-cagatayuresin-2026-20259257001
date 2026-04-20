---
title: Opensearch Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Opensearch Vektör Deposu

Elasticsearch yalnızca Lucene indekslerini destekler, bu nedenle yalnızca Opensearch desteklenmektedir.

**Kurulum üzerine not**: Aşağıdaki doküman aracılığıyla yerel bir Opensearch örneği kuruyoruz. <https://opensearch.org/docs/1.0/>

SSL sorunlarıyla karşılaşırsanız, bunun yerine aşağıdaki `docker run` komutunu deneyin:

```bash
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "plugins.security.disabled=true" opensearchproject/opensearch:1.0.1
```

Referans: <https://github.com/opensearch-project/OpenSearch/issues/1598>

Veriyi İndir

```bash
%pip install llama-index-readers-elasticsearch
%pip install llama-index-vector-stores-opensearch
%pip install llama-index-embeddings-ollama
```

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from os import getenv
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.opensearch import (
    OpensearchVectorStore,
    OpensearchVectorClient,
)
from llama_index.core import VectorStoreIndex, StorageContext


# kümeniz için http uç noktası (vektör indeksi kullanımı için opensearch gereklidir)
endpoint = getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")
# VectorStore uygulamasını göstermek için kullanılacak indeks
idx = getenv("OPENSEARCH_INDEX", "gpt-index-demo")
# bazı örnek verileri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
# OpensearchVectorClient metni varsayılan olarak bu alanda saklar
text_field = "content"
# OpensearchVectorClient gömmeleri varsayılan olarak bu alanda saklar
embedding_field = "embedding"
# OpensearchVectorClient, vektör araması etkinleştirilmiş tek bir opensearch 
# indeksi için mantığı kapsüller
client = OpensearchVectorClient(
    endpoint, idx, 1536, embedding_field=embedding_field, text_field=text_field
)
# vektör deposunu başlat
vector_store = OpensearchVectorStore(client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# örnek verilerimizi ve az önce oluşturduğumuz istemciyi kullanarak bir indeks başlatın
index = VectorStoreIndex.from_documents(
    documents=documents, storage_context=storage_context
)
```

```python
# sorguyu çalıştır
query_engine = index.as_query_engine()
res = query_engine.query("Yazar büyürken neler yaptı?")
print(res.response)
```

OpenSearch vektör deposu [filtre bağlamlı sorguları (filter-context queries)](https://opensearch.org/docs/latest/query-dsl/query-filter-context/) destekler.

```python
from llama_index.core import Document
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
import regex as re
```

```python
# Metni paragraflara böl.
text_chunks = documents[0].text.split("\n\n")


# Her dipnot için bir belge oluştur
footnotes = [
    Document(
        text=chunk,
        id=documents[0].doc_id,
        metadata={"is_footnote": bool(re.search(r"^\s*\[\d+\]\s*", chunk))},
    )
    for chunk in text_chunks
    if bool(re.search(r"^\s*\[\d+\]\s*", chunk))
]
```

```python
# Dipnotları indekse ekleyin
for f in footnotes:
    index.insert(f)
```

```python
# Sadece belirli dipnotları arayan bir sorgu motoru oluşturun.
footnote_query_engine = index.as_query_engine(
    filters=MetadataFilters(
        filters=[
            ExactMatchFilter(
                key="term", value='{"metadata.is_footnote": "true"}'
            ),
            ExactMatchFilter(
                key="query_string",
                value='{"query": "content: space AND content: lisp"}',
            ),
        ]
    )
)


res = footnote_query_engine.query(
    "Yazar uzaylılar ve lisp hakkında ne dedi?"
)
print(res.response)
```

**"Yazar, yeterince gelişmiş herhangi bir uzaylı medeniyetinin Pisagor teoremini ve muhtemelen McCarthy'nin 1960 tarihli makalesindeki Lisp'i bileceğine inanıyor."**

## VectorStoreIndex'in indeksimizde ne oluşturduğunu kontrol etmek için reader kullanın.

Reader, temel arama özelliklerini kullandığı için Elasticsearch ile de çalışır.

```python
# önceki bölümde kullanılan indeksi kontrol etmek için bir reader oluşturun.
from llama_index.readers.elasticsearch import ElasticsearchReader


rdr = ElasticsearchReader(endpoint, idx)
# elasticsearch indeksinden gömme verilerini okumak için opsiyonel olarak embedding_field'ı ayarlayın
docs = rdr.load_data(text_field, embedding_field=embedding_field)
# belgelerin (docs) içinde gömmeler var
print("gömme boyutu:", len(docs[0].embedding))
# tam belge meta verilerde saklanır
print("indeksteki tüm alanlar:", docs[0].metadata.keys())
```

```python
# metnin GPTOpensearchIndex tarafından nasıl parçalandığını kontrol edebiliriz
print("oluşturulan toplam parça sayısı:", len(docs))
```

```python
# standart elasticsearch sorgu DSL'sini kullanarak indeksi arayın
docs = rdr.load_data(text_field, {"query": {"match": {text_field: "Lisp"}}})
print("Lisp'ten bahseden parçalar:", len(docs))
docs = rdr.load_data(text_field, {"query": {"match": {text_field: "Yahoo"}}})
print("Yahoo'dan bahseden parçalar:", len(docs))
```

## Opensearch vektör deposu için hibrit sorgu

Hibrit sorgu, OpenSearch 2.10'dan beri desteklenmektedir. Vektör araması ve metin aramasının birleşimidir. Belirli bir metni aramak ve aynı zamanda sonuçları vektör benzerliğine göre filtrelemek istediğinizde kullanışlıdır. Daha fazla detay: <https://opensearch.org/docs/latest/query-dsl/compound/hybrid/>.

### Arama Boru Hattını (Search Pipeline) Hazırlayın

[Puan normalizasyonu ve ağırlıklı harmonik ortalama birleşimi](https://opensearch.org/docs/latest/search-plugins/search-pipelines/normalization-processor/) ile yeni bir [arama boru hattı](https://opensearch.org/docs/latest/search-plugins/search-pipelines/creating-search-pipeline/) oluşturun.

```bash
PUT /_search/pipeline/hybrid-search-pipeline
{
  "description": "Hibrit arama için son işlemci (post processor)",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "harmonic_mean",
          "parameters": {
            "weights": [
              0.3,
              0.7
            ]
          }
        }
      }
    }
  ]
}
```

### Arama boru hattı detaylarıyla hibrit sorguyu destekleyen bir OpenSearch istemcisi ve vektör deposu başlatın

```python
from os import getenv
from llama_index.vector_stores.opensearch import (
    OpensearchVectorStore,
    OpensearchVectorClient,
)


# kümeniz için http uç noktası (vektör indeksi kullanımı için opensearch gereklidir)
endpoint = getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")
# VectorStore uygulamasını göstermek için kullanılacak indeks
idx = getenv("OPENSEARCH_INDEX", "auto_retriever_movies")


# OpensearchVectorClient metni varsayılan olarak bu alanda saklar
text_field = "content"
# OpensearchVectorClient gömmeleri varsayılan olarak bu alanda saklar
embedding_field = "embedding"
# OpensearchVectorClient, hibrit arama boru hattı ile vektör araması 
# etkinleştirilmiş tek bir opensearch indeksi için mantığı kapsüller
client = OpensearchVectorClient(
    endpoint,
    idx,
    4096,
    embedding_field=embedding_field,
    text_field=text_field,
    search_pipeline="hybrid-search-pipeline",
)


from llama_index.embeddings.ollama import OllamaEmbedding


embed_model = OllamaEmbedding(model_name="llama2")


# vektör deposunu başlat
vector_store = OpensearchVectorStore(client)
```

### İndeksi hazırlayın

```python
from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex, StorageContext


storage_context = StorageContext.from_defaults(vector_store=vector_store)


nodes = [
    TextNode(
        text="The Shawshank Redemption (Esaretin Bedeli)",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
        },
    ),
    TextNode(
        text="The Godfather (Baba)",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
        },
    ),
    TextNode(
        text="Inception (Başlangıç)",
        metadata={
            "director": "Christopher Nolan",
        },
    ),
]


index = VectorStoreIndex(
    nodes, storage_context=storage_context, embed_model=embed_model
)
```

### Filtrelerle vektör deposu sorgu modunu belirterek (VectorStoreQueryMode.HYBRID) indeksi hibrit sorgu ile arayın:

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
from llama_index.core.vector_stores.types import VectorStoreQueryMode


filters = MetadataFilters(
    filters=[
        ExactMatchFilter(
            key="term", value='{"metadata.theme.keyword": "Mafia"}'
        )
    ]
)


retriever = index.as_retriever(
    filters=filters, vector_store_query_mode=VectorStoreQueryMode.HYBRID
)


result = retriever.retrieve("Inception (Başlangıç) ne hakkındadır?")


print(result)
```
