---
title: Milvus Vektör Deposu - Meta Veri Filtreleme
 | LlamaIndex OSS Belgeleri
---

# Milvus Vektör Deposu - Meta Veri Filtreleme

Bu not defteri, LlamaIndex'te Milvus vektör deposunun kullanımını, meta veri filtreleme yeteneklerine odaklanarak açıklamaktadır. Belgeleri meta verilerle nasıl indeksleyeceğinizi, LlamaIndex'in yerleşik meta veri filtreleriyle vektör aramalarını nasıl gerçekleştireceğinizi ve Milvus'un yerel filtreleme ifadelerini vektör deposuna nasıl uygulayacağınızı öğreneceksiniz.

Bu not defterinin sonunda, arama sonuçlarını belge meta verilerine göre daraltmak için Milvus'un filtreleme özelliklerinden nasıl yararlanacağınızı anlamış olacaksınız.

## Ön Koşullar

**Bağımlılıkları kurun**

Başlamadan önce aşağıdaki bağımlılıkların kurulu olduğundan emin olun:

```bash
! pip install llama-index-vector-stores-milvus llama-index
```

> Google Colab kullanıyorsanız, **çalışma zamanını yeniden başlatmanız** gerekebilir (Arayüzün üst kısmındaki "Runtime" menüsüne gidin ve açılır menüden "Restart session" seçeneğini seçin.)

**Hesapları ayarlayın**

Bu eğitim; metin gömmeleri ve cevap oluşturma için OpenAI kullanır. [OpenAI API anahtarını](https://platform.openai.com/api-keys) hazırlamanız gerekir.

```python
import openai


openai.api_key = "sk-"
```

Milvus vektör deposunu kullanmak için Milvus sunucu `URI` (ve isteğe bağlı olarak `TOKEN`) bilginizi belirtin. Bir Milvus sunucusu başlatmak için [Milvus kurulum kılavuzunu](https://milvus.io/docs/install-overview.md) takip ederek bir Milvus sunucusu kurabilir veya ücretsiz olarak [Zilliz Cloud](https://docs.zilliz.com/docs/register-with-zilliz-cloud)'u deneyebilirsiniz.

```python
URI = "./milvus_filter_demo.db"  # Demo amacıyla Milvus-Lite kullanın
# TOKEN = ""
```

**Verileri hazırlayın**

Bu örnek için, örnek veri olarak benzer veya aynı başlıklara ancak farklı meta verilere (yazar, tür ve yayın yılı) sahip birkaç kitabı kullanacağız. Bu, Milvus'un belgeleri hem vektör benzerliği hem de meta veri niteliklerine göre nasıl filtreleyebileceğini ve getirebileceğini göstermeye yardımcı olacaktır.

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="Life: A User's Manual",
        metadata={
            "author": "Georges Perec",
            "genre": "Postmodern Fiction",
            "year": 1978,
        },
    ),
    TextNode(
        text="Life and Fate",
        metadata={
            "author": "Vasily Grossman",
            "genre": "Historical Fiction",
            "year": 1980,
        },
    ),
    TextNode(
        text="Life",
        metadata={
            "author": "Keith Richards",
            "genre": "Memoir",
            "year": 2010,
        },
    ),
    TextNode(
        text="The Life",
        metadata={
            "author": "Malcolm Knox",
            "genre": "Literary Fiction",
            "year": 2011,
        },
    ),
]
```

## İndeks Oluşturma

Bu bölümde, örnek verileri varsayılan gömme modelini (OpenAI'nin `text-embedding-ada-002` modeli) kullanarak Milvus'ta saklayacağız. Başlıklar metin gömmelerine dönüştürülecek ve yoğun bir gömme alanında saklanacak, tüm meta veriler ise skaler alanlarda saklanacaktır.

```python
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext, VectorStoreIndex


vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    collection_name="test_filter_collection",  # Koleksiyon adını buradan değiştirebilirsiniz
    dim=1536,  # Vektör boyutu gömme modeline bağlıdır
    overwrite=True,  # Varsa koleksiyonu sil
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

## Meta Veri Filtreleri (Metadata Filters)

Bu bölümde, LlamaIndex'in yerleşik meta veri filtrelerini ve koşullarını Milvus aramasına uygulayacağız.

**Meta veri filtrelerini tanımlayın**

```python
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)


filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="year", value=2000, operator=FilterOperator.GT
        )  # yıl > 2000
    ]
)
```

**Filtrelerle vektör deposundan veri getirin**

```python
retriever = index.as_retriever(filters=filters, similarity_top_k=5)
result_nodes = retriever.retrieve("Yaşam hakkında kitaplar")
for node in result_nodes:
    print(node.text)
    print(node.metadata)
    print("\n")
```

```text
The Life
{'author': 'Malcolm Knox', 'genre': 'Literary Fiction', 'year': 2011}


Life
{'author': 'Keith Richards', 'genre': 'Memoir', 'year': 2010}
```

### Çoklu Meta Veri Filtreleri

Daha karmaşık sorgular oluşturmak için birden fazla meta veri filtresini de birleştirebilirsiniz. LlamaIndex, filtreleri birleştirmek için hem `AND` hem de `OR` koşullarını destekler. Bu, belgelerin meta veri niteliklerine göre daha kesin ve esnek bir şekilde getirilmesine olanak tanır.

**`AND` Koşulu**

1979 ile 2010 yılları arasında yayınlanan kitapları filtreleyen bir örneği deneyin (özel olarak; 1979 < yıl ≤ 2010):

```python
from llama_index.core.vector_stores import FilterCondition


filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="year", value=1979, operator=FilterOperator.GT
        ),  # yıl > 1979
        MetadataFilter(
            key="year", value=2010, operator=FilterOperator.LTE
        ),  # yıl <= 2010
    ],
    condition=FilterCondition.AND,
)


retriever = index.as_retriever(filters=filters, similarity_top_k=5)
result_nodes = retriever.retrieve("Yaşam hakkında kitaplar")
for node in result_nodes:
    print(node.text)
    print(node.metadata)
    print("\n")
```

```text
Life and Fate
{'author': 'Vasily Grossman', 'genre': 'Historical Fiction', 'year': 1980}


Life
{'author': 'Keith Richards', 'genre': 'Memoir', 'year': 2010}
```

**`OR` Koşulu**

Georges Perec veya Keith Richards tarafından yazılan kitapları filtreleyen başka bir örneği deneyin:

```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="author", value="Georges Perec", operator=FilterOperator.EQ
        ),  # yazar Georges Perec
        MetadataFilter(
            key="author", value="Keith Richards", operator=FilterOperator.EQ
        ),  # yazar Keith Richards
    ],
    condition=FilterCondition.OR,
)


retriever = index.as_retriever(filters=filters, similarity_top_k=5)
result_nodes = retriever.retrieve("Yaşam hakkında kitaplar")
for node in result_nodes:
    print(node.text)
    print(node.metadata)
    print("\n")
```

```text
Life
{'author': 'Keith Richards', 'genre': 'Memoir', 'year': 2010}


Life: A User's Manual
{'author': 'Georges Perec', 'genre': 'Postmodern Fiction', 'year': 1978}
```

## Milvus’un Anahtar Kelime Argümanlarını (Keyword Arguments) Kullanma

Yerleşik filtreleme özelliklerine ek olarak, `string_expr` anahtar kelime argümanı ile Milvus'un yerel filtreleme ifadelerini de kullanabilirsiniz. Bu, arama işlemleri sırasında belirli filtre ifadelerini doğrudan Milvus'a iletmenize olanak tanıyarak Milvus'un gelişmiş filtreleme yeteneklerine erişmek için standart meta veri filtrelemesinin ötesine geçer.

Milvus, vektör verilerinizin kesin bir şekilde sorgulanmasını sağlayan güçlü ve esnek filtreleme seçenekleri sunar:

- Temel Operatörler: Karşılaştırma operatörleri, aralık filtreleri, aritmetik operatörler ve mantıksal operatörler.
- Filtre İfadesi Şablonları: Yaygın filtreleme senaryoları için önceden tanımlanmış desenler.
- Özelleşmiş Operatörler: JSON veya dizi alanları için veri tipine özel operatörler.

Milvus filtreleme ifadelerinin kapsamlı dokümantasyonu ve örnekleri için [Milvus Filtreleme](https://milvus.io/docs/boolean.md) resmi kılavuzuna bakın.

```python
retriever = index.as_retriever(
    vector_store_kwargs={
        "string_expr": "genre like '%Fiction'",
    },
    similarity_top_k=5,
)
result_nodes = retriever.retrieve("Yaşam hakkında kitaplar")
for node in result_nodes:
    print(node.text)
    print(node.metadata)
    print("\n")
```

```text
The Life
{'author': 'Malcolm Knox', 'genre': 'Literary Fiction', 'year': 2011}


Life and Fate
{'author': 'Vasily Grossman', 'genre': 'Historical Fiction', 'year': 1980}


Life: A User's Manual
{'author': 'Georges Perec', 'genre': 'Postmodern Fiction', 'year': 1978}
```
