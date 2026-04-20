# Alibaba Cloud OpenSearch Vektör Deposu (Vector Store)

---
title: Alibaba Cloud OpenSearch Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

> [Alibaba Cloud OpenSearch Vektör Arama Sürümü](https://help.aliyun.com/zh/open-search/vector-search-edition/product-overview), Alibaba Group tarafından geliştirilen büyük ölçekli bir dağıtılmış arama motorudur. Alibaba Cloud OpenSearch Vektör Arama Sürümü; Taobao, Tmall, Cainiao, Youku ve Çin ana karası dışındaki bölgelerdeki müşterilere sunulan diğer e-ticaret platformları dahil olmak üzere tüm Alibaba Group için arama hizmetleri sağlar. Alibaba Cloud OpenSearch Vektör Arama Sürümü aynı zamanda Alibaba Cloud OpenSearch'ün temel motorudur. Yıllar süren geliştirmelerin ardından Alibaba Cloud OpenSearch Vektör Arama Sürümü; yüksek kullanılabilirlik, yüksek güncellik ve maliyet etkinliği iş gereksinimlerini karşılamıştır. Ayrıca, iş özelliklerinize göre özel bir arama hizmeti oluşturabileceğiniz otomatik bir operasyon ve bakım (O&M) sistemi sunar.

Çalıştırmak için bir örneğiniz (instance) olmalıdır.

### Kurulum (Setup)

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-alibabacloud-opensearch
```

```bash
%pip install llama-index
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

### Lütfen OpenAI erişim anahtarını sağlayın

OpenAI gömmelerini (embeddings) kullanmak için bir OpenAI API Anahtarı sağlamanız gerekir:

```python
import openai
import getpass


OPENAI_API_KEY = getpass.getpass("OpenAI API Anahtarı:")
openai.api_key = OPENAI_API_KEY
```

#### Veriyi İndir (Download Data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Belgeleri Yükle (Load documents)

```python
from llama_index.core import SimpleDirectoryReader
from IPython.display import Markdown, display
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print(f"Toplam belge: {len(documents)}")
```

```text
Toplam belge: 1
```

### Alibaba Cloud OpenSearch Vektör Deposu nesnesini oluşturun:

Bir sonraki adımı çalıştırmak için bir Alibaba Cloud OpenSearch Vektör Servisi örneğiniz olmalı ve bir tablo yapılandırmalısınız.

```python
# aşağıdaki hücreleri çalıştırmak asenkron g/ç istisnası (async io exception) oluşturursa bunu çalıştırın
import nest_asyncio


nest_asyncio.apply()
```

```python
# metaveri filtresi olmadan başlat
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.alibabacloud_opensearch import (
    AlibabaCloudOpenSearchStore,
    AlibabaCloudOpenSearchConfig,
)


config = AlibabaCloudOpenSearchConfig(
    endpoint="*****",
    instance_id="*****",
    username="kullanici_adiniz",
    password="sifreniz",
    table_name="llama",
)


vector_store = AlibabaCloudOpenSearchStore(config)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgula (Query Index)

```python
# daha ayrıntılı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken neler yaptı?")
```

```python
display(Markdown(f"<b>{response}</b>"))
```

**Üniversite öncesinde yazar, yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve 9. sınıfta Fortran'ın erken bir sürümünü kullanarak IBM 1401'de programlar yazmayı denedi.**

### Mevcut bir depoya bağlanma (Connecting to an existing store)

Bu depo Alibaba Cloud OpenSearch tarafından desteklendiği için doğası gereği kalıcıdır. Bu nedenle, daha önce oluşturulmuş ve doldurulmuş bir depoya bağlanmak isterseniz şu şekilde yapabilirsiniz:

```python
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.alibabacloud_opensearch import (
    AlibabaCloudOpenSearchStore,
    AlibabaCloudOpenSearchConfig,
)


config = AlibabaCloudOpenSearchConfig(
    endpoint="***",
    instance_id="***",
    username="kullanici_adiniz",
    password="sifreniz",
    table_name="llama",
)


vector_store = AlibabaCloudOpenSearchStore(config)


# Mevcut depolanmış vektörlerden indeks oluşturun
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
response = query_engine.query(
    "Yazar AI üzerinde çalışmadan önce ne okudu?"
)


display(Markdown(f"<b>{response}</b>"))
```

### Metaveri filtreleme (Metadata filtering)

Alibaba Cloud OpenSearch vektör deposu, sorgu sırasında metaveri filtrelemeyi destekler. Tamamen yeni bir tablo üzerinde çalışan aşağıdaki hücreler bu özelliği göstermektedir.

Bu demoda, kısalık adına tek bir kaynak belge yüklenir (`../data/paul_graham/paul_graham_essay.txt` metin dosyası). Bununla birlikte, belgelere eklenen metaveriler üzerindeki koşullarla sorguları nasıl kısıtlayabileceğinizi göstermek için belgeye bazı özel metaveriler ekleyeceksiniz.

```python
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.alibabacloud_opensearch import (
    AlibabaCloudOpenSearchStore,
    AlibabaCloudOpenSearchConfig,
)


config = AlibabaCloudOpenSearchConfig(
    endpoint="****",
    instance_id="****",
    username="kullanici_adiniz",
    password="sifreniz",
    table_name="llama",
)


md_storage_context = StorageContext.from_defaults(
    vector_store=AlibabaCloudOpenSearchStore(config)
)




def my_file_metadata(file_name: str):
    """Giriş dosyası adına bağlı olarak farklı bir metaveri ilişkilendirir."""
    if "essay" in file_name:
        source_type = "essay"
    elif "dinosaur" in file_name:
        # bu (ne yazık ki) bu demoda gerçekleşmeyecek
        source_type = "dinos"
    else:
        source_type = "other"
    return {"source_type": source_type}




# Belgeleri yükle ve indeks oluştur
md_documents = SimpleDirectoryReader(
    "../data/paul_graham", file_metadata=my_file_metadata
)
md_documents = md_documents.load_data()
md_index = VectorStoreIndex.from_documents(
    md_documents, storage_context=md_storage_context
)
```

Sorgu motoruna filtre ekleyin:

```python
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters


md_query_engine = md_index.as_query_engine(
    filters=MetadataFilters(
        filters=[MetadataFilter(key="source_type", value="essay")]
    )
)
md_response = md_query_engine.query(
    "Yazarın tezini yazması ne kadar sürdü?"
)


display(Markdown(f"<b>{md_response}</b>"))
```

Filtrelemenin devrede olduğunu test etmek için bunu yalnızca `"dinos"` belgelerini kullanacak şekilde değiştirmeyi deneyin... bu sefer yanıt gelmeyecektir :)
