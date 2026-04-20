---
title: MyScale Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# MyScale Vektör Deposu

Bu not defterinde, `MyScaleVectorStore` kullanımına dair hızlı bir demo göstereceğiz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-myscale
```

```bash
!pip install llama-index
```

#### MyScale İstemcisi Oluşturma

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

```python
from os import environ
import clickhouse_connect


environ["OPENAI_API_KEY"] = "sk-*"


# istemciyi başlat
client = clickhouse_connect.get_client(
    host="KUME_HOST_ADRESINIZ",
    port=8443,
    username="KULLANICI_ADINIZ",
    password="KUME_SIFRENIZ",
)
```

#### Belgeleri Yükleme, MyScaleVectorStore ile VectorStoreIndex Oluşturma ve Saklama

Burada, gömmelere dönüştürülecek metni sağlamak için Paul Graham makalelerinden oluşan bir set kullanacağız, bunları bir `MyScaleVectorStore`da saklayacağız ve LLM QnA (Soru-Cevap) döngümüz için bağlam bulmak üzere sorgulayacağız.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.myscale import MyScaleVectorStore
from IPython.display import Markdown, display
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("../data/paul_graham").load_data()
print("Belge Kimliği:", documents[0].doc_id)
print("Belge Sayısı: ", len(documents))
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

Dosyalarınızı [SimpleDirectoryReader](/examples/data_connectors/simple_directory_reader.ipynb) kullanarak tek tek işleyebilirsiniz:

```python
loader = SimpleDirectoryReader("./data/paul_graham/")
documents = loader.load_data()
for file in loader.input_files:
    print(file)
    # Burası herhangi bir ön işleme yapacağınız yerdir
```

```python
# meta veri filtresi ile başlatın ve indeksleri saklayın
from llama_index.core import StorageContext


for document in documents:
    document.metadata = {"user_id": "123", "favorite_color": "blue"}
vector_store = MyScaleVectorStore(myscale_client=client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

MyScale vektör deposu artık filtreli aramayı ve hibrit aramayı desteklemektedir.

[Sorgu motoru (query_engine)](/module_guides/deploying/query_engine/index.md) ve [erişici (retriever)](/module_guides/querying/retriever/index.md) hakkında daha fazla bilgi edinebilirsiniz.

```python
import textwrap


from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


# daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine(
    filters=MetadataFilters(
        filters=[
            ExactMatchFilter(key="user_id", value="123"),
        ]
    ),
    similarity_top_k=2,
    vector_store_query_mode="hybrid",
)
response = query_engine.query("Yazar ne öğrendi?")
print(textwrap.fill(str(response), 100))
```

#### Tüm İndeksleri Temizleme

```python
for document in documents:
    index.delete_ref_doc(document.doc_id)
```
