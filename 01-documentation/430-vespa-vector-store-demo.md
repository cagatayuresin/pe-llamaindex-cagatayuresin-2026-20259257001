# Vespa Vektör Deposu (Vector Store) demosu

---
title: Vespa Vektör Deposu demosu
 | LlamaIndex OSS Documentation
---

Bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```
%pip install llama-index-vector-stores-vespa llama-index pyvespa
```

#### API anahtarını ayarlama

```
import os
import openai


os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = os.environ["OPENAI_API_KEY"]
```

#### Belgeleri yükleme, VectorStoreIndex oluşturma

```
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.vespa import VespaVectorStore
from IPython.display import Markdown, display
```

## Bazı örnek verileri tanımlama

Hadi biraz belge ekleyelim.

```
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="The Shawshank Redemption",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
            "year": 1994,
        },
    ),
    TextNode(
        text="The Godfather",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
            "year": 1972,
        },
    ),
    TextNode(
        text="Inception",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Fiction",
            "year": 2010,
        },
    ),
    TextNode(
        text="To Kill a Mockingbird",
        metadata={
            "author": "Harper Lee",
            "theme": "Mafia",
            "year": 1960,
        },
    ),
    TextNode(
        text="1984",
        metadata={
            "author": "George Orwell",
            "theme": "Totalitarianism",
            "year": 1949,
        },
    ),
    TextNode(
        text="The Great Gatsby",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "The American Dream",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter and the Sorcerer's Stone",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Fiction",
            "year": 1997,
        },
    ),
]
```

### VespaVectorStore'un Başlatılması

Başlamayı gerçekten kolaylaştırmak için, vektör deposu başlatıldığında dağıtılacak (deploy edilecek) bir şablon Vespa uygulaması sunuyoruz.
 
 Bu büyük bir soyutlamadır ve Vespa uygulamasını ihtiyaçlarınıza göre uyarlamak ve özelleştirmek için sonsuz fırsat vardır. Ancak şimdilik işleri basit tutalım ve varsayılan şablonla başlatalım.

```
from llama_index.core import StorageContext


vector_store = VespaVectorStore()
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

### Belgeleri silme

```
node_to_delete = nodes[0].node_id
node_to_delete
```

```
vector_store.delete(ref_doc_id=node_to_delete)
```

## Sorgulama

```
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryMode,
)
```

```
query = VectorStoreQuery(
    query_str="Great Gatsby",
    mode=VectorStoreQueryMode.TEXT_SEARCH,
    similarity_top_k=1,
)
result = vector_store.query(query)
```

```
result
```

## Getirici (retriever) olarak

### Varsayılan sorgu modu (metin araması)

```
retriever = index.as_retriever(vector_store_query_mode="default")
results = retriever.retrieve("Who directed inception?")
display(Markdown(f"**Retrieved nodes:**\n {results}"))
```

```
retriever = index.as_retriever(vector_store_query_mode="semantic_hybrid")
results = retriever.retrieve("Who wrote Harry Potter?")
display(Markdown(f"**Retrieved nodes:**\n {results}"))
```

### Sorgu motoru olarak

```
query_engine = index.as_query_engine()
response = query_engine.query("Who directed inception?")
display(Markdown(f"**Response:** {response}"))
```

```
query_engine = index.as_query_engine(
    vector_store_query_mode="semantic_hybrid", verbose=True
)
response = query_engine.query(
    "When was the book about the wizard boy published and what was it called?"
)
display(Markdown(f"**Response:** {response}"))
display(Markdown(f"**Sources:** {response.source_nodes}"))
```

## Meta veri filtrelerini kullanma

**NOT**: Bu meta veri filtreleme işlemi, Vespa'nın dışında llama-index tarafından gerçekleştirilir. Yerel ve çok daha yüksek performanslı filtreleme için Vespa'nın kendi filtreleme yeteneklerini kullanmalısınız.
 
 Daha fazla bilgi için [Vespa dökümantasyonuna](https://docs.vespa.ai/en/reference/query-language-reference.html) bakın.

```
from llama_index.core.vector_stores import (
    FilterOperator,
    FilterCondition,
    MetadataFilter,
    MetadataFilters,
)


# Sadece teması "Fiction" OLAN VEYA 1997'den sonra yayınlanan düğümlere izin verecek bir filtre tanımlayalım.


filters = MetadataFilters(
    filters=[
        MetadataFilter(key="theme", value="Fiction"),
        MetadataFilter(key="year", value=1997, operator=FilterOperator.GT),
    ],
    condition=FilterCondition.OR,
)


retriever = index.as_retriever(filters=filters)
result = retriever.retrieve("Harry Potter")
display(Markdown(f"**Result:** {result}"))
```

## Bu entegrasyonun soyutlama düzeyi

Başlamayı gerçekten kolaylaştırmak için, vektör deposu başlatıldığında dağıtılacak bir şablon Vespa uygulaması sunuyoruz. Bu, Vespa'yı ilk kez kurmanın bazı karmaşıklıklarını ortadan kaldırır; ancak ciddi kullanım durumları için [Vespa dökümantasyonunu](docs.vespa.ai) okumanızı ve uygulamayı ihtiyaçlarınıza göre uyarlamanızı şiddetle tavsiye ederiz.

### Şablon

Sunulan şablon Vespa uygulaması aşağıda görülebilir:

```
from vespa.package import (
    ApplicationPackage,
    Field,
    Schema,
    Document,
    HNSW,
    RankProfile,
    Component,
    Parameter,
    FieldSet,
    GlobalPhaseRanking,
    Function,
)


hybrid_template = ApplicationPackage(
    name="hybridsearch",
    schema=[
        Schema(
            name="doc",
            document=Document(
                fields=[
                    Field(name="id", type="string", indexing=["summary"]),
                    Field(name="metadata", type="string", indexing=["summary"]),
                    Field(
                        name="text",
                        type="string",
                        indexing=["index", "summary"],
                        index="enable-bm25",
                        bolding=True,
                    ),
                    Field(
                        name="embedding",
                        type="tensor<float>(x[384])",
                        indexing=[
                            "input text",
                            "embed",
                            "index",
                            "attribute",
                        ],
                        ann=HNSW(distance_metric="angular"),
                        is_document_field=False,
                    ),
                ]
            ),
            fieldsets=[FieldSet(name="default", fields=["text", "metadata"])],
            rank_profiles=[
                RankProfile(
                    name="bm25",
                    inputs=[("query(q)", "tensor<float>(x[384])")],
                    functions=[Function(name="bm25sum", expression="bm25(text)")],
                    first_phase="bm25sum",
                ),
                RankProfile(
                    name="semantic",
                    inputs=[("query(q)", "tensor<float>(x[384])")],
                    first_phase="closeness(field, embedding)",
                ),
                RankProfile(
                    name="fusion",
                    inherits="bm25",
                    inputs=[("query(q)", "tensor<float>(x[384])")],
                    first_phase="closeness(field, embedding)",
                    global_phase=GlobalPhaseRanking(
                        expression="reciprocal_rank_fusion(bm25sum, closeness(field, embedding))",
                        rerank_count=1000,
                    ),
                ),
            ],
        )
    ],
    components=[
        Component(
            id="e5",
            type="hugging-face-embedder",
            parameters=[
                Parameter(
                    "transformer-model",
                    {
                        "url": "https://github.com/vespa-engine/sample-apps/raw/master/simple-semantic-search/model/e5-small-v2-int8.onnx"
                    },
                ),
                Parameter(
                    "tokenizer-model",
                    {
                        "url": "https://raw.githubusercontent.com/vespa-engine/sample-apps/master/simple-semantic-search/model/tokenizer.json"
                    },
                ),
            ],
        )
    ],
)
```

Entegrasyonun çalışması için `id`, `metadata`, `text` ve `embedding` alanlarının gerekli olduğunu unutmayın. Şema adı `doc` olmalı ve sıralama profilleri (rank profiles) `bm25`, `semantic` ve `fusion` olarak adlandırılmalıdır.
 
 Bunun dışında, yerleştirme (embedding) modellerini değiştirerek, daha fazla alan ekleyerek veya sıralama ifadelerini değiştirerek uygun gördüğünüz şekilde düzenleme yapmakta özgürsünüz.
 
 Daha fazla ayrıntı için, [hibrit arama](https://pyvespa.readthedocs.io/en/latest/getting-started-pyvespa.html) hakkındaki bu Pyvespa örnek not defterine göz atın.
