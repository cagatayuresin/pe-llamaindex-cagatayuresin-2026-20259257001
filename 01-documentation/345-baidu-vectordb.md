# Baidu VectorDB

---
title: Baidu VectorDB
 | LlamaIndex OSS Belgeleri
---

> [Baidu VectorDB](https://cloud.baidu.com/product/vdb.html), Baidu Intelligent Cloud tarafından titizlikle geliştirilen ve tamamen yönetilen, sağlam, kurumsal düzeyde dağıtık bir veritabanı hizmetidir. Çok boyutlu vektör verilerini depolama, geri çağırma ve analiz etme konusundaki olağanüstü yeteneğiyle öne çıkar. Temelinde, yüksek performans, kullanılabilirlik ve güvenliğin yanı sıra dikkat çekici ölçeklenebilirlik ve kullanıcı dostu olma sağlayan Baidu'nun tescilli "Mochow" vektör veritabanı çekirdeği üzerinde çalışır.

> Bu veritabanı hizmeti, çeşitli kullanım durumlarına hitap eden geniş bir indeks türü ve benzerlik hesaplama yöntemleri yelpazesini destekler. VectorDB'nin öne çıkan bir özelliği, etkileyici sorgu performansını korurken 10 milyar seviyesine kadar devasa bir vektör ölçeğini yönetebilmesi ve milisaniye düzeyinde sorgu gecikmesiyle saniyede milyonlarca sorguyu (QPS) destekleyebilmesidir.

**Bu not defteri, BaiduVectorDB'nin LlamaIndex'te bir Vektör Deposu olarak temel kullanımını göstermektedir.**

Çalıştırmak için bir [veritabanı örneğine (instance)](https://cloud.baidu.com/doc/VDB/s/hlrsoazuf) sahip olmalısınız.

## Kurulum (Setup)

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-baiduvectordb
```

```bash
!pip install llama-index
```

```bash
!pip install pymochow
```

```python
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.vector_stores.baiduvectordb import (
    BaiduVectorDB,
    TableParams,
    TableField,
)
import pymochow
```

### Lütfen OpenAI erişim anahtarını sağlayın

OpenAI tarafından sunulan gömmeleri (embeddings) kullanmak için bir OpenAI API Anahtarı sağlamanız gerekir:

```python
import openai
import getpass


OPENAI_API_KEY = getpass.getpass("OpenAI API Anahtarı:")
openai.api_key = OPENAI_API_KEY
```

## Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Vektör Deposunu Oluşturma ve Doldurma

Şimdi Paul Graham'a ait bazı makaleleri yerel bir dosyadan yükleyecek ve bunları Baidu VectorDB'de saklayacaksınız.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print(f"Toplam belge: {len(documents)}")
print(f"İlk belge, kimlik (id): {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    f"İlk belge, metin ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

### Baidu VectorDB'yi Başlatma

Vektör deposunun oluşturulması, henüz mevcut değilse alt plandaki veritabanı koleksiyonunun (koleksiyon yapısının) oluşturulmasını içerir:

```python
vector_store = BaiduVectorDB(
    endpoint="http://192.168.X.X",
    api_key="*******",
    table_params=TableParams(dimension=1536, drop_exists=True),
)
```

Şimdi bu depoyu, daha sonra sorgulama yapmak üzere bir LlamaIndex soyutlaması olan `index` içine sarın:

```python
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Yukarıdaki `from_documents` çağrısının aynı anda birkaç şey yaptığına dikkat edin: giriş belgelerini yönetilebilir boyuttaki parçalara ("düğümler") ayırır, her düğüm için gömme vektörlerini hesaplar ve bunların hepsini Baidu VectorDB'de saklar.

## Depoyu Sorgulama

### Temel sorgulama

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden AI üzerinde çalışmayı seçti?")
print(response)
```

### MMR tabanlı sorgular

MMR (maksimal marjinal alaka düzeyi - maximal marginal relevance) yöntemi, depodan hem sorguyla alakalı hem de birbirinden olabildiğince farklı metin parçalarını getirmek için tasarlanmıştır; buradaki amaç, nihai yanıtın oluşturulması için daha geniş bir bağlam sağlamaktır:

```python
query_engine = index.as_query_engine(vector_store_query_mode="mmr")
response = query_engine.query("Yazar neden AI üzerinde çalışmayı seçti?")
print(response)
```

## Mevcut bir depoya bağlanma

Bu depo Baidu VectorDB tarafından desteklendiği için tanımı gereği kalıcıdır (persistent). Bu nedenle, daha önce oluşturulmuş ve doldurulmuş bir depoya bağlanmak isterseniz yapmanız gerekenler şunlardır:

```python
vector_store = BaiduVectorDB(
    endpoint="http://192.168.X.X",
    api_key="*******",
    table_params=TableParams(dimension=1536, drop_exists=False),
)


# İndeks oluşturma (önceden depolanmış vektörlerden)
new_index_instance = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)


# artık sorgulama vb. yapabilirsiniz:
query_engine = new_index_instance.as_query_engine(similarity_top_k=5)
response = query_engine.query(
    "Yazar AI üzerinde çalışmadan önce ne okudu?"
)
print(response)
```

## Metaveri filtreleme (Metadata filtering)

Baidu VectorDB vektör deposu, sorgu sırasında tam eşleşen `anahtar=değer` çiftleri şeklinde metaveri filtrelemeyi destekler. Tamamen yeni bir koleksiyon üzerinde çalışan aşağıdaki hücreler bu özelliği göstermektedir.

Bu demoda, kısa tutmak adına tek bir kaynak belge yüklenmiştir (`../data/paul_graham/paul_graham_essay.txt` metin dosyası). Bununla birlikte, belgelere eklenen metaveriler üzerindeki koşullarla sorguları nasıl kısıtlayabileceğinizi göstermek için belgeye bazı özel metaveriler ekleyeceksiniz.

```python
filter_fields = [
    TableField(name="source_type"),
]


md_storage_context = StorageContext.from_defaults(
    vector_store=BaiduVectorDB(
        endpoint="http://192.168.X.X",
        api_key="*******",
        table_params=TableParams(
            dimension=1536, drop_exists=True, filter_fields=filter_fields
        ),
    )
)




def my_file_metadata(file_name: str):
    """Giriş dosyası adına bağlı olarak farklı bir metaveri ilişkilendir."""
    if "essay" in file_name:
        source_type = "essay"
    elif "dinosaur" in file_name:
        # bu (maalesef) bu demoda gerçekleşmeyecek
        source_type = "dinos"
    else:
        source_type = "other"
    return {"source_type": source_type}




# Belgeleri yükle ve indeks oluştur
md_documents = SimpleDirectoryReader(
    "../data/paul_graham", file_metadata=my_file_metadata
).load_data()
md_index = VectorStoreIndex.from_documents(
    md_documents, storage_context=md_storage_context
)
```

```python
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
```

```python
md_query_engine = md_index.as_query_engine(
    filters=MetadataFilters(
        filters=[MetadataFilter(key="source_type", value="essay")]
    )
)
md_response = md_query_engine.query(
    "Yazarın tezini yazması ne kadar sürdü?"
)
print(md_response.response)
```
