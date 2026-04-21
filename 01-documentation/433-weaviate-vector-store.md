# Weaviate Vektör Deposu

---
title: Weaviate Vektör Deposu
 | LlamaIndex OSS Documentation
---

Bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```
%pip install llama-index-vector-stores-weaviate
```

```
!pip install llama-index
```

#### Weaviate İstemcisi Oluşturma

```
import os
import openai


os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.environ["OPENAI_API_KEY"]
```

```
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```
import weaviate
```

```
# cloud
cluster_url = ""
api_key = ""


client = weaviate.connect_to_wcs(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)


# local
# client = connect_to_local()
```

#### Belgeleri yükleme, VectorStoreIndex oluşturma

```
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from IPython.display import Markdown, display
```

Veriyi İndir

```
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```
from llama_index.core import StorageContext


# İndeksi daha sonra yüklemek istiyorsanız, ona bir isim verdiğinizden emin olun!
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)


# NOT: Dilerseniz manuel olarak bir index_name de tanımlayabilirsiniz.
 # index_name = "test_prefix"
 # vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)
```

#### Özel bir toplu işlem (batch) yapılandırması kullanma

LlamaIndex, çoğu yaygın senaryo için optimize edilmiş olan Weaviate'in dinamik toplu işleme (dynamic batching) özelliğini varsayılan olarak kullanır. Ancak, düşük gecikmeli kurulumlarda bu durum sunucuyu aşırı yükleyebilir veya mevcut GRPC Mesaj limitlerini zorlayabilir. Daha fazla kontrol ve daha iyi bir veri alımı (ingestion) süreci için, sabit boyutlu toplu işlemi (fixed size batch) kullanarak toplu işlem boyutunu ayarlamayı düşünebilirsiniz.
 
 İşte WeaviateVectorStore'da nasıl ince ayar yapabileceğiniz ve özel bir toplu işlem (batch) tanımlayabileceğiniz:

```
from weaviate.classes.config import ConsistencyLevel


custom_batch = client.batch.fixed_size(
    batch_size=123,
    concurrent_requests=3,
    consistency_level=ConsistencyLevel.ALL,
)
vector_store_fixed = WeaviateVectorStore(
    weaviate_client=client,
    index_name="LlamaIndex",
    # özel toplu işlemimizi (custom batch) client_kwargs olarak geçiriyoruz
    client_kwargs={"custom_batch": custom_batch},
)
```

#### Sorgu İndeksi

```
# daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
```

```
display(Markdown(f"<b>{response}</b>"))
```

## İndeksi yükleme

Burada, başlangıç indeksini oluştururken kullandığımız indeks adının aynısını kullanıyoruz. Bu, indeksin otomatik olarak oluşturulmasını engeller ve ona kolayca yeniden bağlanmamızı sağlar.

```
cluster_url = ""
api_key = ""


client = weaviate.connect_to_wcs(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)


# local
# client = weaviate.connect_to_local()
```

```
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex"
)


loaded_index = VectorStoreIndex.from_vector_store(vector_store)
```

```
# daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = loaded_index.as_query_engine()
response = query_engine.query("What happened at interleaf?")
display(Markdown(f"<b>{response}</b>"))
```

## Meta Veri Filtreleme

Hadi sahte bir belge ekleyelim ve sadece o belgenin döndürülmesi için filtrelemeyi deneyelim.

```
from llama_index.core import Document


doc = Document.example()
print(doc.metadata)
print("-----")
print(doc.text[:100])
```

```
loaded_index.insert(doc)
```

```
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="filename", value="README.md")]
)
query_engine = loaded_index.as_query_engine(filters=filters)
response = query_engine.query("What is the name of the file?")
display(Markdown(f"<b>{response}</b>"))
```

# İndeksi tamamen silme

Vektör deposu tarafından oluşturulan indeksi `delete_index` fonksiyonunu kullanarak silebilirsiniz.

```
vector_store.delete_index()
```

```
vector_store.delete_index()  # fonksiyonu tekrar çağırmak hiçbir şey yapmaz
```

# Bağlantıyı Sonlandırma

İstemci bağlantılarınızın kapatıldığından emin olmalısınız:

```
client.close()
```
