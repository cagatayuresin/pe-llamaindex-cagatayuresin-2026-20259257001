---
title: Gel Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Gel Vektör Deposu

[Gel](https://www.geldata.com/), geliştirmeden üretime hızlı geçiş döngüsü için optimize edilmiş, açık kaynaklı bir PostgreSQL veri katmanıdır. Üst düzey kesin tipli graf benzeri bir veri modeli, birleştirilebilir hiyerarşik sorgu dili, tam SQL desteği, göçler (migrations), kimlik doğrulama (Auth) ve AI modülleri ile birlikte gelir.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
! pip install gel llama-index-vector-stores-gel
```

```bash
! pip install llama-index
```

```python
# import logging
# import sys


# Hata ayıklama günlüklerini görmek için yorum satırını kaldırın
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.gel import GelVectorStore
import textwrap
import openai
```

### OpenAI Kurulumu

İlk adım OpenAI anahtarını yapılandırmaktır. Bu anahtar, indekse yüklenen belgeler için gömmeler (embeddings) oluşturmak amacıyla kullanılacaktır.

```python
import os


os.environ["OPENAI_API_KEY"] = "<anahtarınız>"
openai.api_key = os.environ["OPENAI_API_KEY"]
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükleme

`SimpleDirectoryReader` kullanarak `data/paul_graham/` dizininde saklanan belgeleri yükleyin

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

### Veritabanını Oluşturma

Gel'i vektör deponuz için bir arka uç (backend) olarak kullanmak için çalışan bir Gel örneğine ihtiyacınız olacaktır. Neyse ki, istemediğiniz sürece Docker konteynerleri veya karmaşık bir şey içermesi gerekmez!

Yerel bir örnek kurmak için şunu çalıştırın:

```bash
! gel project init --non-interactive
```

Eğer [Gel Cloud](cloud.geldata.com) kullanıyorsanız (ki kullanmalısınız!), bu komuta bir argüman daha ekleyin:

Terminal penceresi

```bash
gel project init --server-instance <kurum-adi>/<ornek-adi>
```

Gel'i çalıştırmanın tüm yollarını içeren kapsamlı bir liste için başvuru belgelerinin [Gel'i Çalıştırma (Running Gel)](https://docs.geldata.com/reference/running) bölümüne göz atın.

### Şemayı Ayarlama

[Gel şeması](https://docs.geldata.com/reference/datamodel), uygulamanızın veri modelinin açık, üst düzey bir açıklamasıdır. Verilerinizin tam olarak nasıl düzenleneceğini tanımlamanıza olanak tanımasının yanı sıra; bağlantılar, erişim politikaları, fonksiyonlar, tetikleyiciler, kısıtlamalar, indeksler ve daha fazlası gibi Gel'in birçok güçlü özelliğini de yönetir.

LlamaIndex'in `GelVectorStore` sınıfı, şema için aşağıdaki düzeni bekler:

```python
schema_content = """
using extension pgvector;


module default {
    scalar type EmbeddingVector extending ext::pgvector::vector<1536>;


    type Record {
        required collection: str;
        text: str;
        embedding: EmbeddingVector;
        external_id: str {
            constraint exclusive;
        };
        metadata: json;


        index ext::pgvector::hnsw_cosine(m := 16, ef_construction := 128)
            on (.embedding)
    }
}
""".strip()


with open("dbschema/default.gel", "w") as f:
    f.write(schema_content)
```

Şema değişikliklerini veritabanına uygulamak için Gel'in [göç aracını (migration tool)](https://docs.geldata.com/reference/datamodel/migrations) kullanarak göçü çalıştırın:

```bash
! gel migration create --non-interactive
! gel migrate
```

Bu noktadan itibaren `GelVectorStore`, LlamaIndex'te bulunan diğer tüm vektör depolarının doğrudan yerine kullanılabilir.

### İndeksi Oluşturma

```python
vector_store = GelVectorStore()


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
query_engine = index.as_query_engine()
```

### İndeksi Sorgulama

Artık indeksimizi kullanarak sorular sorabiliriz.

```python
response = query_engine.query("Yazar neler yaptı?")
```

```python
print(textwrap.fill(str(response), 100))
```

```python
response = query_engine.query("1980'lerin ortalarında neler oldu?")
```

```python
print(textwrap.fill(str(response), 100))
```

### Meta Veri Filtreleri

`GelVectorStore`, düğümlerde meta veri saklamayı ve erişim adımı sırasında bu meta verilere göre filtreleme yapmayı destekler.

#### Git commit'leri veri kümesini indir

```bash
!mkdir -p 'data/git_commits/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/csv/commit_history.csv' -O 'data/git_commits/commit_history.csv'
```

```python
import csv


with open("data/git_commits/commit_history.csv", "r") as f:
    commits = list(csv.DictReader(f))


print(commits[0])
print(len(commits))
```

#### Özel meta verili düğümler ekleyin

```python
# İlk 100 commit'in her biri için TextNode oluşturun
from llama_index.core.schema import TextNode
from datetime import datetime
import re


nodes = []
dates = set()
authors = set()
for commit in commits[:100]:
    author_email = commit["author"].split("<")[1][:-1]
    commit_date = datetime.strptime(
        commit["date"], "%a %b %d %H:%M:%S %Y %z"
    ).strftime("%Y-%m-%d")
    commit_text = commit["change summary"]
    if commit["change details"]:
        commit_text += "\n\n" + commit["change details"]
    fixes = re.findall(r"#(\d+)", commit_text, re.IGNORECASE)
    nodes.append(
        TextNode(
            text=commit_text,
            metadata={
                "commit_date": commit_date,
                "author": author_email,
                "fixes": fixes,
            },
        )
    )
    dates.add(commit_date)
    authors.add(author_email)


print(nodes[0])
print(min(dates), "-", max(dates))
print(authors)
```

```python
vector_store = GelVectorStore()


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
index.insert_nodes(nodes)
```

```python
print(index.as_query_engine().query("Lakshmi segfault hatasını nasıl düzeltti?"))
```

#### Meta veri filtrelerini uygula

Düğümleri getirirken artık commit yazarına veya tarihe göre filtreleme yapabiliriz.

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
)


filters = MetadataFilters(
    filters=[
        MetadataFilter(key="author", value="mats@timescale.com"),
        MetadataFilter(key="author", value="sven@timescale.com"),
    ],
    condition="or",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkındadır?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="commit_date", value="2023-08-15", operator=">="),
        MetadataFilter(key="commit_date", value="2023-08-25", operator="<="),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkındadır?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

#### İç içe (nested) filtreleri uygula

Yukarıdaki örneklerde VE (AND) veya VEYA (OR) kullanarak birden fazla filtreyi birleştirdik. Ayrıca birden fazla filtre setini de birleştirebiliriz.

```python
filters = MetadataFilters(
    filters=[
        MetadataFilters(
            filters=[
                MetadataFilter(
                    key="commit_date", value="2023-08-01", operator=">="
                ),
                MetadataFilter(
                    key="commit_date", value="2023-08-15", operator="<="
                ),
            ],
            condition="and",
        ),
        MetadataFilters(
            filters=[
                MetadataFilter(key="author", value="mats@timescale.com"),
                MetadataFilter(key="author", value="sven@timescale.com"),
            ],
            condition="or",
        ),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkındadır?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

Yukarıdaki işlem `IN` operatörü kullanılarak basitleştirilebilir. `GelVectorStore`, bir öğeyi bir listeyle karşılaştırmak için `in`, `nin` (not in) ve `contains` operatörlerini destekler.

```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="commit_date", value="2023-08-01", operator=">="),
        MetadataFilter(key="commit_date", value="2023-08-15", operator="<="),
        MetadataFilter(
            key="author",
            value=["mats@timescale.com", "sven@timescale.com"],
            operator="in",
        ),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkındadır?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

```python
# Aynısı, nin (NOT IN) ile
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="commit_date", value="2023-08-01", operator=">="),
        MetadataFilter(key="commit_date", value="2023-08-15", operator="<="),
        MetadataFilter(
            key="author",
            value=["mats@timescale.com", "sven@timescale.com"],
            operator="nin",
        ),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkındadır?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

```python
# CONTAINS (İÇERİR)
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="fixes", value="5680", operator="contains"),
    ]
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu commit'ler sorunu nasıl düzeltti?")
for node in retrieved_nodes:
    print(node.node.metadata)
```
