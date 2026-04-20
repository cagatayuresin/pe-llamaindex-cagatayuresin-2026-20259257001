---
title: ClickHouse Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Bu not defterinde, ClickHouseVectorStore kullanımına dair hızlı bir demo göstereceğiz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
!pip install llama-index
!pip install clickhouse_connect
```

#### ClickHouse İstemcisi (Client) Oluşturma

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
    host="localhost",
    port=8123,
    username="default",
    password="",
)
```

#### Belgeleri yükleme, ClickHouseVectorStore ile VectorStoreIndex oluşturma ve saklama

Burada, gömme (embedding) haline getirilecek metni sağlamak, bir `ClickHouseVectorStore` içinde saklamak ve LLM Soru-Cevap (QnA) döngümüz için bağlam bulmak amacıyla bir dizi Paul Graham makalesini kullanacağız.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.clickhouse import ClickHouseVectorStore
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("../data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
print("Belge Sayısı: ", len(documents))
```

```text
Belge Kimliği (Document ID): d03ac7db-8dae-4199-bc38-445dec51a534
Belge Sayısı:  1
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
    # Burası herhangi bir ön işleme (preprocessing) yapacağınız yerdir
```

```text
data/paul_graham/paul_graham_essay.txt
```

```python
# meta veri filtresi ile başlat ve indeksleri sakla
from llama_index.core import StorageContext


for document in documents:
    document.metadata = {"user_id": "123", "favorite_color": "blue"}
vector_store = ClickHouseVectorStore(clickhouse_client=client)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

Artık ClickHouse vektör deposu, filtreli aramayı ve hibrit aramayı desteklemektedir.

[sorgu\_motoru (query\_engine)](/module_guides/deploying/query_engine/index.md) ve [erişici (retriever)](/module_guides/querying/retriever/index.md) hakkında daha fazla bilgi edinebilirsiniz.

```python
import textwrap


from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


# Daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
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

**Yazar, Interleaf'te geçirdiği süre boyunca; teknoloji şirketlerinin satış elemanlarından ziyade ürün odaklı kişiler tarafından yönetilmesinin önemini, çok fazla kişinin kod düzenlemesinin dezavantajlarını, koridor konuşmalarının planlı toplantılardan daha değerli olduğunu, büyük bürokratik müşterilerle uğraşmanın zorluklarını ve bir pazarda "giriş seviyesi" seçeneği olmanın önemini içeren birkaç şey öğrendi.**

#### Tüm İndeksleri Temizle

```python
for document in documents:
    index.delete_ref_doc(document.doc_id)
```
