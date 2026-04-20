---
title: Postgres Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Postgres Vektör Deposu

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için [Postgresql](https://www.postgresql.org) ve [pgvector](https://github.com/pgvector/pgvector)'un nasıl kullanılacağını göstereceğiz.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-postgres
```

```bash
!pip install llama-index
```

Aşağıdaki hücreyi çalıştırmak, Colab'da Postgres'i PGVector ile kuracaktır.

```bash
!sudo apt update
!echo | sudo apt install -y postgresql-common
!echo | sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
!echo | sudo apt install postgresql-15-pgvector
!sudo service postgresql start
!sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
!sudo -u postgres psql -c "CREATE DATABASE vector_db;"
```

```python
# import logging
# import sys


# Hata ayıklama (debug) günlüklerini görmek için yorum satırlarını kaldırın
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap
```

### OpenAI Kurulumu

İlk adım, OpenAI anahtarını yapılandırmaktır. İndekse yüklenen belgeler için gömmeler oluşturmada kullanılacaktır.

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri yükleme

`SimpleDirectoryReader` kullanarak `data/paul_graham/` içinde depolanan belgeleri yükleyin.

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)
```

```bash
Document ID: 56e70c8c-0fb7-4250-99be-b953d0185a01
```

### Veritabanını Oluşturma

Yerel bilgisayarda (localhost) çalışan mevcut bir postgres'i kullanarak, kullanacağımız veritabanını oluşturun.

```python
import psycopg2


connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "vector_db"
conn = psycopg2.connect(connection_string)
conn.autocommit = True


with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")
```

### İndeksi oluşturma

Burada, daha önce yüklenen belgeleri kullanarak Postgres destekli bir indeks oluşturuyoruz. PGVectorStore birkaç argüman alır. Aşağıdaki örnek, `vector_cosine_ops` yöntemi ile m = 16, ef_construction = 64 ve ef_search = 40 olan bir HNSW indeksi ile bir PGVectorStore oluşturur.

```python
from sqlalchemy import make_url


url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai gömme boyutu
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
query_engine = index.as_query_engine()
```

```bash
Parsing nodes:   0%|          | 0/1 [00:00<?, ?it/s]






Generating embeddings:   0%|          | 0/22 [00:00<?, ?it/s]




2025-09-11 16:47:21,725 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
```

### İndeksi sorgulama

Artık indeksimizi kullanarak sorular sorabiliriz.

```python
response = query_engine.query("Yazar neler yaptı?")
```

```bash
2025-09-11 16:47:30,412 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2025-09-11 16:47:31,665 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

```python
print(textwrap.fill(str(response), 100))
```

```bash
Yazar denemeler yazmak, programlama yapmak, mikro bilgisayarlar oluşturmak, roket yüksekliklerini tahmin etmek, bir kelime işlemci geliştirmek ve bir girişim başlatmak üzerine konuşmalar yapmak gibi işler üzerinde çalıştı.
```

```python
response = query_engine.query("1980'lerin ortalarında ne oldu?")
```

```bash
2025-09-11 16:47:37,531 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2025-09-11 16:47:38,352 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
```

```python
print(textwrap.fill(str(response), 100))
```

```bash
1980'lerin ortalarında yapay zeka havada uçuşuyordu ve bu alanda çalışma arzusunu etkileyen iki şey vardı: Heinlein'ın Mike adında zeki bir bilgisayarı içeren Ay Zalim Bir Sevgilidir romanı ve Terry Winograd'ın SHRDLU kullandığını gösteren bir PBS belgeseli.
```

### Mevcut indeksi sorgulama

```python
vector_store = PGVectorStore.from_params(
    database="vector_db",
    host="localhost",
    password="password",
    port=5432,
    user="postgres",
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai gömme boyutu
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine()
```

```python
response = query_engine.query("Yazar neler yaptı?")
```

```python
print(textwrap.fill(str(response), 100))
```

```bash
Yazar denemeler yazmak, programlama yapmak, mikro bilgisayarlar oluşturmak, yazılım geliştirmek, konuşmalar yapmak ve bir girişim başlatmak üzerine çalıştı.
```

### Hibrit Arama

Hibrit aramayı etkinleştirmek için yapmanız gerekenler:

1. `PGVectorStore` oluşturulurken `hybrid_search=True` parametresini iletin (ve isteğe bağlı olarak istenilen dille `text_search_config` yapılandırın).
2. Sorgu motorunu oluştururken `vector_store_query_mode="hybrid"` parametresini iletin (bu yapılandırma arka planda erişiciye, yani retriever'a iletilir). İsteğe bağlı olarak, seyrek metin araması (sparse text search) sonuçlarından kaç tane elde edeceğimizi yapılandırmak için `sparse_top_k` parametresini de ayarlayabilirsiniz (varsayılan olarak `similarity_top_k` ile aynı değeri kullanır).

```python
from sqlalchemy import make_url


url = make_url(connection_string)
hybrid_vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="paul_graham_essay_hybrid_search",
    embed_dim=1536,  # openai gömme boyutu
    hybrid_search=True,
    text_search_config="english",
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)


storage_context = StorageContext.from_defaults(
    vector_store=hybrid_vector_store
)
hybrid_index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
hybrid_query_engine = hybrid_index.as_query_engine(
    vector_store_query_mode="hybrid", sparse_top_k=2
)
hybrid_response = hybrid_query_engine.query(
    "Paul Graham 'schtick' kelimesiyle kimi düşünüyor"
)
```

```python
print(hybrid_response)
```

```bash
Roy Lichtenstein
```

#### QueryFusionRetriever ile hibrit aramayı geliştirme

Metin araması ve vektör araması puanları farklı şekilde hesaplandığından, yalnızca metin araması tarafından bulunan düğümlerin puanı çok daha düşük olacaktır.

Müşterek bilgiyi düğümleri sıralamak için daha iyi kullanan `QueryFusionRetriever` aracılığıyla hibrit arama performansını genellikle artırabilirsiniz.

```python
from llama_index.core.response_synthesizers import CompactAndRefine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


vector_retriever = hybrid_index.as_retriever(
    vector_store_query_mode="default",
    similarity_top_k=5,
)
text_retriever = hybrid_index.as_retriever(
    vector_store_query_mode="sparse",
    similarity_top_k=5,  # bu bağlamda sparse_top_k ile birbirinin yerine kullanılabilir
)
retriever = QueryFusionRetriever(
    [vector_retriever, text_retriever],
    similarity_top_k=5,
    num_queries=1,  # sorgu oluşturmayı devre dışı bırakmak için bunu 1 olarak ayarlayın
    mode="relative_score",
    use_async=False,
)


response_synthesizer = CompactAndRefine()
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)
```

```python
response = query_engine.query(
    "Paul Graham 'schtick' kelimesiyle kimi düşünüyor ve neden?"
)
print(response)
```

```bash
Paul Graham, "schtick" kelimesini kullanırken Roy Lichtenstein'ı düşünür çünkü Lichtenstein'ın resimlerindeki kendine özgü imzası, işini hemen kendi eseri olarak tanımlar.
```

### Meta veri filtreleri

PGVectorStore, düğümlerde meta veri depolamayı ve geri getirme (retrieval) adımında bu meta verilere göre filtreleme yapmayı destekler.

#### Git commit'leri veri setini indir

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

```bash
{'commit': '44e41c12ab25e36c202f58e068ced262eadc8d16', 'author': 'Lakshmi Narayanan Sreethar<lakshmi@timescale.com>', 'date': 'Tue Sep 5 21:03:21 2023 +0530', 'change summary': 'Fix segfault in set_integer_now_func', 'change details': 'When an invalid function oid is passed to set_integer_now_func, it finds out that the function oid is invalid but before throwing the error, it calls ReleaseSysCache on an invalid tuple causing a segfault. Fixed that by removing the invalid call to ReleaseSysCache.  Fixes #6037 '}
4167
```

#### Özel meta verilerle düğümler ekleme

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
print(min(dates), "ile", max(dates))
print(authors)
```

```bash
Node ID: 9c2c2f17-d763-4ce8-bb02-83cb176008e4
Text: Fix segfault in set_integer_now_func  When an invalid function
oid is passed to set_integer_now_func, it finds out that the function
oid is invalid but before throwing the error, it calls ReleaseSysCache
on an invalid tuple causing a segfault. Fixed that by removing the
invalid call to ReleaseSysCache.  Fixes #6037
2023-03-22 ile 2023-09-05
{'konstantina@timescale.com', 'nikhil@timescale.com', 'satish.8483@gmail.com', 'mats@timescale.com', 'fabriziomello@gmail.com', 'erik@timescale.com', 'sven@timescale.com', 'lakshmi@timescale.com', 'dmitry@timescale.com', 'engel@sero-systems.de', 'rafia.sabih@gmail.com', '36882414+akuzm@users.noreply.github.com', 'jguthrie@timescale.com', 'jan@timescale.com', 'me@noctarius.com'}
```

```python
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="metadata_filter_demo3",
    embed_dim=1536,  # openai gömme boyutu
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
index.insert_nodes(nodes)
```

```bash
2025-09-11 16:48:11,383 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
```

```python
print(index.as_query_engine().query("Lakshmi segfault sorununu nasıl düzeltti?"))
```

```bash
2025-09-11 16:48:15,149 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2025-09-11 16:48:15,687 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"




Lakshmi, soruna neden olan ReleaseSysCache'e yapılan geçersiz çağrıyı kaldırarak segfault sorununu düzeltti.
```

#### Meta veri filtrelerini uygulayın

Artık düğümleri alırken commit yazarına veya tarihe göre filtreleme yapabiliriz.

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

```bash
2025-09-11 16:48:31,673 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-07', 'author': 'mats@timescale.com', 'fixes': []}
{'commit_date': '2023-08-27', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-07-13', 'author': 'mats@timescale.com', 'fixes': []}
{'commit_date': '2023-08-07', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-30', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-23', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-10', 'author': 'mats@timescale.com', 'fixes': []}
{'commit_date': '2023-07-25', 'author': 'mats@timescale.com', 'fixes': ['5892']}
{'commit_date': '2023-08-21', 'author': 'sven@timescale.com', 'fixes': []}
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

```bash
2025-09-11 16:48:40,347 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-23', 'author': 'erik@timescale.com', 'fixes': []}
{'commit_date': '2023-08-17', 'author': 'konstantina@timescale.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []}
{'commit_date': '2023-08-24', 'author': 'lakshmi@timescale.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-23', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-21', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-20', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-21', 'author': 'sven@timescale.com', 'fixes': []}
```

#### İç içe geçmiş filtreler uygulayın

Yukarıdaki örneklerde, VEYA ve VE (OR/AND) kullanarak birden çok filtreyi birleştirdik. Ayrıca birkaç farklı filtre kümesini de birleştirebiliriz.

SQL'deki örneği:

```sql
WHERE (commit_date >= '2023-08-01' AND commit_date <= '2023-08-15') AND (author = 'mats@timescale.com' OR author = 'sven@timescale.com')
```

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

```bash
2025-09-11 16:48:45,021 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-07', 'author': 'mats@timescale.com', 'fixes': []}
{'commit_date': '2023-08-07', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-10', 'author': 'mats@timescale.com', 'fixes': []}
```

Yukarıdaki işlemler IN operatörü kullanılarak basitleştirilebilir. `PGVectorStore`, bir öğeyi bir listeyle karşılaştırmak için `in`, `nin` ve `contains` operatörlerini destekler.

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

```bash
2025-09-11 16:48:49,129 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-07', 'author': 'mats@timescale.com', 'fixes': []}
{'commit_date': '2023-08-07', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': 'sven@timescale.com', 'fixes': []}
{'commit_date': '2023-08-10', 'author': 'mats@timescale.com', 'fixes': []}
```

```python
# Aynı şeyin NOT IN (Olmayanlar) ile yapılışı
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

```bash
2025-09-11 16:48:51,587 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-09', 'author': 'me@noctarius.com', 'fixes': ['5805']}
{'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []}
{'commit_date': '2023-08-15', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []}
{'commit_date': '2023-08-11', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []}
{'commit_date': '2023-08-09', 'author': 'konstantina@timescale.com', 'fixes': ['5923', '5680', '5774', '5786', '5906', '5912']}
{'commit_date': '2023-08-03', 'author': 'dmitry@timescale.com', 'fixes': []}
{'commit_date': '2023-08-03', 'author': 'dmitry@timescale.com', 'fixes': ['5908']}
{'commit_date': '2023-08-01', 'author': 'nikhil@timescale.com', 'fixes': []}
{'commit_date': '2023-08-10', 'author': 'konstantina@timescale.com', 'fixes': []}
{'commit_date': '2023-08-10', 'author': '36882414+akuzm@users.noreply.github.com', 'fixes': []}
```

```python
# CONTAINS (İçerir)
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

```bash
2025-09-11 16:48:56,822 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-09', 'author': 'konstantina@timescale.com', 'fixes': ['5923', '5680', '5774', '5786', '5906', '5912']}
```

### Sorguları özelleştirme

Diğer tabloları birleştirmek (join) gibi daha karmaşık sorgular oluşturmak mümkündür. Bu işlem, işlevinizi `customize_query_fn` argümanına ayarlayarak yapılır. Öncelikle, bir kullanıcı tablosu oluşturalım ve onu dolduralım.

```python
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    String,
    Integer,
    create_engine,
    insert,
)


engine = create_engine(url=connection_string + "/" + db_name)


metadata = MetaData()


user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False),
)


user_table.drop(engine, checkfirst=True)
user_table.create(engine)


with engine.begin() as conn:
    stmt = insert(user_table)
    conn.execute(
        stmt, [{"name": "Konstantina", "email": "konstantina@timescale.com"}]
    )
```

Ardından, bir sorgu özelleştirme işlevi (query customization function) oluşturabilir ve `PGVectorStore`u `customize_query_fn` ile somutlaştırabilir, başlatabiliriz.

```python
from typing import Any
from sqlalchemy import Select




def customize_query(query: Select, table_class: Any, **kwargs: Any) -> Select:
    # E-posta adresleri üzerinden kullanıcı tablosunu birleştir ve select ifadesine 'name' sütununu ekle
    return query.add_columns(user_table.c.name).join(
        user_table,
        user_table.c.email == table_class.metadata_["author"].astext,
    )




vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="metadata_filter_demo3",
    embed_dim=1536,  # openai gömme boyutu
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
    customize_query_fn=customize_query,
)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
```

Daha sonra vektör deposunu sorgulayabiliriz ve 'select' (seçme/bulma) ifadesine eklenen herhangi bir ek alanı, düğüm meta verilerinde bulunan `custom_fields` adlı bir sözlük (dictionary) içinde erişebiliriz.

```python
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

```bash
2025-09-11 17:06:43,812 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"




{'commit_date': '2023-08-09', 'author': 'konstantina@timescale.com', 'fixes': ['5923', '5680', '5774', '5786', '5906', '5912'], 'custom_fields': {'name': 'Konstantina'}}
```

### PgVector Sorgu Seçenekleri

#### IVFFlat Probları (IVFFlat Probes)

[IVFFlat problarının](https://github.com/pgvector/pgvector?tab=readme-ov-file#query-options) sayısını belirleyin (varsayılan: 1)

İndeksten veri çekerken (retrieving), uygun sayıda IVFFlat probu belirtebilirsiniz (geri çağırma veya 'recall' için daha yüksek sayılar daha iyidir; hız için ise daha düşük sayılar daha iyidir).

```python
retriever = index.as_retriever(
    vector_store_query_mode="hybrid",
    similarity_top_k=5,
    vector_store_kwargs={"ivfflat_probes": 10},
)
```

#### HNSW EF Arama (HNSW EF Search)

Arama için dinamik [aday listesinin](https://github.com/pgvector/pgvector?tab=readme-ov-file#query-options-1) boyutunu belirleyin (varsayılan: 40)

```python
retriever = index.as_retriever(
    vector_store_query_mode="hybrid",
    similarity_top_k=5,
    vector_store_kwargs={"hnsw_ef_search": 300},
)
```
