# Azure Postgres Vektör Deposu (Vector Store)

---
title: Azure Postgres Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için [Azure Postgresql](https://azure.microsoft.com/en-au/products/postgresql) ve [pg\_diskann](https://github.com/microsoft/DiskANN) eklentisinin nasıl kullanılacağını göstereceğiz. Lütfen bu belgenin, geçişi basitleştirmek için çoğunlukla [PostgreSQL entegrasyonu](https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres/) belgesine dayandığını unutmayın.

```bash
!pip install llama-index
```

```python
%load_ext sql
```

```python
import subprocess
import os
from urllib.parse import quote_plus


cmd = [
    "az",
    "account",
    "get-access-token",
    "--resource",
    "https://ossrdbms-aad.database.windows.net",
    "--query",
    "accessToken",
    "--output",
    "tsv",
]


try:
    token = subprocess.check_output(cmd, text=True).strip()
except subprocess.CalledProcessError as exc:
    raise RuntimeError(f"Komut çalıştırılamadı: {exc}") from exc
os.environ["PGPASSWORD"] = token
```

```python
%sql postgresql://
```

‘postgresql://’ adresine bağlanılıyor...

```python
%%sql
drop table if exists llamaindex_vectors;
```

‘postgresql://’ üzerinde sorgu çalıştırılıyor...

|   |
| - |

```python
import logging
import sys
import os


# Hata ayıklama günlüklerini görmek için yorum satırını kaldırın
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.settings import Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
import textwrap


# Yerel dosyadan içe aktar
from llama_index.vector_stores.azure_postgres import AzurePGVectorStore
from llama_index.vector_stores.azure_postgres.common import (
    AzurePGConnectionPool,
    DiskANN,
    VectorOpClass,
)
```

### OpenAI Kurulumu

İlk adım, Azure OpenAI anahtarını yapılandırmaktır. Bu, indekse yüklenen belgeler için gömmeler (embeddings) oluşturmak amacıyla kullanılacaktır.

```python
import os


# Yöntem 1: Yedek değerlerle os.environ.get() kullanma
aoai_api_key = os.environ.get("AOAI_API_KEY", "anahtar")
aoai_endpoint = os.environ.get("AOAI_ENDPOINT", "uc_noktasi")
aoai_api_version = os.environ.get("AOAI_API_VERSION", "2024-12-01-preview")


llm = AzureOpenAI(
    model="o4-mini",
    deployment_name="o4-mini",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)


# Kendi sohbet tamamlama modelinizin yanı sıra kendi gömme modelinizi de dağıtmanız gerekir
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-3-small",
    deployment_name="text-embedding-3-small",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükleme

`SimpleDirectoryReader` kullanarak `data/paul_graham/` içinde saklanan belgeleri yükleyin.

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Belge Kimliği (Document ID):", documents[0].doc_id)
```

### Veritabanını Oluşturma

Azure üzerinde çalışan mevcut bir postgres örneğini kullanarak, veritabanına bağlanmak için Microsoft Entra kimlik doğrulamasını kullanacağız. Lütfen Azure hesabınızda oturum açtığınızdan emin olun.

```python
host = os.environ.get("PGHOST", "<host_adresiniz>")
port = int(os.environ.get("PGPORT", 5432))
database = os.environ.get("PGDATABASE", "postgres")
from psycopg import Connection
from psycopg.rows import dict_row
from llama_index.vector_stores.azure_postgres.common import (
    ConnectionInfo,
    create_extensions,
    Extension,
)




def configure_connection(conn: Connection) -> None:
    conn.autocommit = True
    create_extensions(conn, [Extension(ext_name="vector")])
    create_extensions(conn, [Extension(ext_name="pg_diskann")])
    conn.row_factory = dict_row




azure_conn_info: ConnectionInfo = ConnectionInfo(
    host=host, port=port, dbname=database, configure=configure_connection
)
conn = AzurePGConnectionPool(
    azure_conn_info=azure_conn_info,
)
```

### Vektör Deposunu Oluşturma

Burada, daha önce yüklenen belgeleri kullanarak Postgres tarafından desteklenen bir indeks oluşturuyoruz. `AzurePGVectorStore` birkaç argüman alır. Aşağıdaki örnek, indeksi bulunmayan bir PGVectorStore oluşturur.

```python
vector_store = AzurePGVectorStore.from_params(
    connection_pool=conn,
    table_name="llamaindex_vectors",
    embed_dim=1536,  # openai gömme boyutu
)


Settings.llm = llm
Settings.embed_model = embed_model
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
query_engine = index.as_query_engine()
```

### Veri Kümesini Sorgulama

Artık sorular sorabiliriz.

```python
response = query_engine.query("Yazar ne yaptı?")
print(textwrap.fill(str(response), 100))
```

### Mevcut İndeksi Sorgulama

Şimdi, gömmelerimiz üzerinde `vector_cosine_ops` yöntemiyle `max_neighbors = 32`, `l_value_ib = 100` ve `l_value_is = 100` değerlerine sahip bir `pg_diskann` indeksi oluşturuyoruz ve bunu yeni bir vektör deposu ile kullanıyoruz.

```python
%%sql
create index on llamaindex_vectors
using diskann (embedding vector_cosine_ops)
with (
  max_neighbors = 32,
  l_value_ib = 100
);
set diskann.l_value_is to 100;
```

```python
diskann = DiskANN(
    op_class=VectorOpClass.vector_cosine_ops,
    max_neighbors=32,
    l_value_ib=100,
    l_value_is=100,
)
```

```python
vector_store = AzurePGVectorStore.from_params(
    connection_pool=conn,
    schema_name="public",
    table_name="llamaindex_vectors",
    embed_dim=1536,  # openai gömme boyutu
    embedding_index=diskann,
)


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine()
```

### Tekil Düğümlere Erişim

Belirli bir düğümü kimliğine (id) göre okuyun.

```python
nodes = vector_store.get_nodes()
print(len(nodes))
node_id = nodes[0].node_id
print(node_id)
nodes = vector_store.get_nodes([node_id])
print(nodes[0])
```

Tek bir düğümü ve ardından tüm tabloyu silin.

```python
vector_store.delete_nodes(node_ids=[node_id])
nodes = vector_store.get_nodes()
print(len(nodes))
vector_store.clear()  # hepsini sil
nodes = vector_store.get_nodes()
print(len(nodes))
```

### Metaveri Filtreleri (Metadata filters)

`AzurePGVectorStore`, düğümlerde metaveri saklamayı ve geri çağırma (retrieval) adımı sırasında bu metaverilere göre filtreleme yapmayı destekler.

#### Git commit veri kümesini indirin

```python
import builtins
import csv


# Veri dosyasını açın
with builtins.open("../data/csv/commit_history_2.csv", "r") as f:
    commits = list(csv.DictReader(f))


print(commits[0])
print(len(commits))
```

#### Özel metaverilerle düğüm ekleme

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
print(min(dates), "ile", max(dates), "arası")
print(authors)
```

```python
vector_store = AzurePGVectorStore.from_params(
    connection_pool=conn,
    schema_name="public",
    table_name="metadata_filter_demo3",
    embed_dim=1536,  # openai gömme boyutu
)


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
index.insert_nodes(nodes)
```

#### Metaveri filtrelerini uygulama

Artık düğümleri geri çağırırken commit yazarına veya tarihe göre filtreleme yapabiliriz.

```python
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
)


filters = MetadataFilters(
    filters=[
        MetadataFilter(key="author", value="matb@microsoft.com"),
        MetadataFilter(key="author", value="benjamin.pasero@microsoft.com"),
    ],
    condition="or",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkında?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="commit_date", value="2025-08-20", operator=">="),
        MetadataFilter(key="commit_date", value="2025-08-25", operator="<="),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkında?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

#### İç içe geçmiş (nested) filtreleri uygulama

Yukarıdaki örneklerde, AND veya OR kullanarak birden fazla filtreyi birleştirdik. Ayrıca birden fazla filtre setini de birleştirebiliriz.

Örneğin SQL'de:

```sql
WHERE (commit_date >= '2025-08-20' AND commit_date <= '2023-08-25') AND (author = 'matb@microsoft.com' OR author = 'benjamin.pasero@microsoft.com')
```

```python
filters = MetadataFilters(
    filters=[
        MetadataFilters(
            filters=[
                MetadataFilter(
                    key="commit_date", value="2025-08-20", operator=">="
                ),
                MetadataFilter(
                    key="commit_date", value="2025-08-25", operator="<="
                ),
            ],
            condition="and",
        ),
        MetadataFilters(
            filters=[
                MetadataFilter(key="author", value="matb@microsoft.com"),
                MetadataFilter(
                    key="author", value="benjamin.pasero@microsoft.com"
                ),
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


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkında?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

Yukarıdaki işlem `IN` operatörü kullanılarak basitleştirilebilir. `AzurePGVectorStore`, bir öğeyi bir listeyle karşılaştırmak için `in`, `nin` ve `contains` operatörlerini destekler.

```python
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="commit_date", value="2025-08-15", operator=">="),
        MetadataFilter(key="commit_date", value="2025-08-20", operator="<="),
        MetadataFilter(
            key="author",
            value=["matb@microsoft.com", "benjamin.pasero@microsoft.com"],
            operator="in",
        ),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkında?")


for node in retrieved_nodes:
    print(node.node.metadata)
```

```python
# Aynı şey, NOT IN (nin) ile
filters = MetadataFilters(
    filters=[
        MetadataFilter(key="commit_date", value="2025-08-15", operator=">="),
        MetadataFilter(key="commit_date", value="2025-08-20", operator="<="),
        MetadataFilter(
            key="author",
            value=["matb@microsoft.com", "benjamin.pasero@microsoft.com"],
            operator="nin",
        ),
    ],
    condition="and",
)


retriever = index.as_retriever(
    similarity_top_k=10,
    filters=filters,
)


retrieved_nodes = retriever.retrieve("Bu yazılım projesi ne hakkında?")


for node in retrieved_nodes:
    print(node.node.metadata)
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
