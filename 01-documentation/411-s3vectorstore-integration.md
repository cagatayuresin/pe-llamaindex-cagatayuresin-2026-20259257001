---
title: S3VectorStore Entegrasyonu
 | LlamaIndex OSS Belgeleri
---

# S3VectorStore Entegrasyonu

Bu, S3Vectors kullanan LlamaIndex için bir vektör deposu entegrasyonudur.

[S3Vectors hakkında daha fazla bilgi edinin](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-getting-started.html).

Bu not defteri (notebook), halihazırda bir S3 vektör paketi (bucket) (ve muhtemelen de bir indeks) oluşturduğunuzu varsayacaktır.

## Kurulum

```bash
%pip install llama-index-vector-stores-s3 llama-index-embeddings-openai
```

## Kullanım

### Vektör deposu nesnesini oluşturma

Mevcut bir S3 paketi (bucket) içinde yeni bir vektör indeksi yaratabilirsiniz.

Ortamınızda (environment) yapılandırılmış (configured) S3 kimlik bilgileriniz (credentials) yoksa, bu kimlik bilgilerini barındıran bir boto3 oturumu sağlayabilirsiniz.

```python
from llama_index.vector_stores.s3 import S3VectorStore
import boto3


vector_store = S3VectorStore.create_index_from_bucket(
    # S3 paketi adı veya ARN
    bucket_name_or_arn="test-bucket",
    # Yeni indeksin adı
    index_name="benim-indeksim",
    # Vektör boyutu (örn. OpenAI gömmeleri / embeddings için 1536)
    dimension=1536,
    # Mesafe / Uzaklık ölçütü: "cosine", "euclidean", vb.
    distance_metric="cosine",
    # Vektörler için veri türü
    data_type="float32",
    # Vektör eklemek (insert) için yığın (batch) boyutu (maksimum 500)
    insert_batch_size=500,
    # Filtrelenemeyecek (non-filterable) meta veri (metadata) anahtarları
    non_filterable_metadata_keys=["custom_field"],
    # İsteğe bağlı: Özel AWS konfigürasyonları / yapılandırmaları için bir boto3 oturumu verin
    # sync_session=boto3.Session(...)
)
```

Veya halihazırda bulunan mevcut bir S3 paketindeki yine kullanıma açık mevcut bir vektör indeksini kullanabilirsiniz.

```python
from llama_index.vector_stores.s3 import S3VectorStore
import boto3


vector_store = S3VectorStore(
    # İndeks adı veya ARN
    index_name_or_arn="benim-indeksim",
    # S3 paketi adı veya ARN
    bucket_name_or_arn="test-bucket",
    # Vektörler için geçerli veri türü (indeksle eşleşmelidir)
    data_type="float32",
    # Mesafe ölçütü / hesabı (indeksle eşleşmelidir)
    distance_metric="cosine",
    # Vektör kurulumu / yerleşimi adına yığın boyutu (maksimum 500)
    insert_batch_size=500,
    # İsteğe bağlı (Optional): Şayet önceden indeks doldurduysanız içinde metin bulunan meta verilerini belirtebilirsiniz. 
    # text_field="content",
    # İsteğe bağlı: AWS ayarları adına (custom) yeni bir boto3 oturumu başlatın
    # sync_session=boto3.Session(...),
)
```

### Vektör deposunu bir indeks ile beraber kullanmak

Elinizde geçerli bir vektör deponuz olduğunda, bunu bir indeks üzerine entegre edebilirsiniz:

```python
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
    Document,
)
from llama_index.embeddings.openai import OpenAIEmbedding


# Biraz veri yükleyin
# documents = SimpleDirectoryReader("data").load_data()


# Ya da yeni belgeler oluşturun
documents = [
    Document(text="Merhaba, dünya! (Hello, world!)", metadata={"key": "1"}),
    Document(text="Merhaba, dünya! 2 (Hello, world! 2)", metadata={"key": "2"}),
]


# Yeni bir indeks kurun (Create a new index)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=StorageContext.from_defaults(vector_store=vector_store),
    # isteğe bağlı: gömme (embed) modelini belirleyin
    embed_model=OpenAIEmbedding(model="text-embedding-3-small", api_key="..."),
)


# Veya zaten kullanımda olan mevcut bir indeksten yeniden çalıştırın (ya da yükleyin)
# index = VectorStoreIndex.from_vector_store(
#     vector_store=vector_store,
#     # optional: set the embed model
#     # embed_model=embed_model,
# )
```

```python
nodes = index.as_retriever(similarity_top_k=1).retrieve("Merhaba, dünya! (Hello, world!)")
print(nodes[0].text)
```

```bash
Merhaba, dünya! (Hello, world!)
```

Doğru ve net düğümleri (nodes) alabilmeniz ve tespit etmeniz adına filtrelerden de faydalanabilirsiniz!

```python
from llama_index.core.vector_stores.types import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator,
    FilterCondition,
)


nodes = index.as_retriever(
    similarity_top_k=2,
    filters=MetadataFilters(
        filters=[
            MetadataFilter(
                key="key",
                value="2",
                operator=FilterOperator.EQ,
            ),
        ],
        condition=FilterCondition.AND,
    ),
).retrieve("Merhaba, dünya! (Hello, world!)")


print(nodes[0].text)
```

```bash
Merhaba, dünya! 2 (Hello, world! 2)
```

### Vektör deposunu doğrudan kullanma

Ayrıca vektör deposunu hiçbir bileşenle ilişkilendirmeden, bilakis doğrudan kullanabilirsiniz:

```python
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import VectorStoreQuery
from llama_index.embeddings.openai import OpenAIEmbedding


# düğümleri (nodes) gömün
nodes = [
    TextNode(text="Merhaba, dünya! (Hello, world!)"),
    TextNode(text="Merhaba, dünya! 2 (Hello, world! 2)"),
]


embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key="...")
embeddings = embed_model.get_text_embedding_batch([n.text for n in nodes])
for node, embedding in zip(nodes, embeddings):
    node.embedding = embedding


# vektör deposuna bağlı haldeki düğümleri ekleyin
vector_store.add(nodes)


# vektör deposunu sorgulayın
query = VectorStoreQuery(
    query_embedding=embed_model.get_query_embedding("Merhaba, dünya! (Hello, world!)"),
    similarity_top_k=2,
)
results = vector_store.query(query)
print(results.nodes[0].text)
```

```bash
Merhaba, dünya! (Hello, world!)
```
