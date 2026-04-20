# Apache Cassandra Vektör Deposu (Vector Store)

---
title: Apache Cassandra Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

[Apache Cassandra®](https://cassandra.apache.org), NoSQL tabanlı, satır yönelimli (row-oriented), yüksek ölçüde ölçeklenebilir ve yüksek kullanılabilirliğe sahip bir veritabanıdır. Sürüm 5.0'dan itibaren veritabanı [vektör araması](https://cassandra.apache.org/doc/trunk/cassandra/vector-search/overview.html) yetenekleriyle birlikte sunulmaktadır.

DataStax [CQL aracılığıyla Astra DB](https://docs.datastax.com/en/astra-serverless/docs/vector-search/quickstart.html), Cassandra üzerine inşa edilmiş, aynı arayüzü ve güçlü yönleri sunan yönetilen bir sunucusuz (serverless) veritabanıdır.

**Bu not defteri, LlamaIndex'te Cassandra Vektör Deposu'nun temel kullanımını göstermektedir.**

Kodun tamamını çalıştırmak için vektör araması yetenekleriyle donatılmış çalışan bir Cassandra kümesine (cluster) veya bir DataStax Astra DB örneğine (instance) ihtiyacınız vardır.

## Kurulum (Setup)

```bash
%pip install llama-index-vector-stores-cassandra
```

```bash
!pip install --quiet "astrapy>=0.5.8"
```

```python
import os
from getpass import getpass


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    # StorageContext'i içe aktar
    StorageContext,
)
from llama_index.vector_stores.cassandra import CassandraVectorStore
```

Bir sonraki adım, CassIO'yu küresel bir DB bağlantısıyla başlatmaktır: Bu adım, bir Cassandra kümesi ve Astra DB için biraz farklı yapılan tek adımdır:

### Başlatma (Cassandra kümesi)

Bu durumda, öncelikle [Cassandra sürücü belgelerinde](https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/cluster/#module-cassandra.cluster) açıklandığı gibi bir `cassandra.cluster.Session` nesnesi oluşturmanız gerekir. Detaylar (örneğin ağ ayarları ve kimlik doğrulaması ile) değişiklik gösterir ancak şuna benzer bir şey olabilir:

```python
from cassandra.cluster import Cluster


cluster = Cluster(["127.0.0.1"])
session = cluster.connect()
```

```python
import cassio


CASSANDRA_KEYSPACE = input("CASSANDRA_KEYSPACE = ")


cassio.init(session=session, keyspace=CASSANDRA_KEYSPACE)
```

### Başlatma (CQL aracılığıyla Astra DB)

Bu durumda CassIO'yu aşağıdaki bağlantı parametreleriyle başlatırsınız:

- Veritabanı Kimliği (Database ID), örn. 01234567-89ab-cdef-0123-456789abcdef
- Belirteç (Token), örn. AstraCS:6gBhNmsk135… (bu bir "Veritabanı Yöneticisi - Database Administrator" belirteci olmalıdır)
- İsteğe bağlı olarak bir Keyspace adı (belirtilmezse veritabanı için varsayılan olan kullanılacaktır)

```python
ASTRA_DB_ID = input("ASTRA_DB_ID = ")
ASTRA_DB_TOKEN = getpass("ASTRA_DB_TOKEN = ")


desired_keyspace = input("ASTRA_DB_KEYSPACE (isteğe bağlı, boş bırakılabilir) = ")
if desired_keyspace:
    ASTRA_DB_KEYSPACE = desired_keyspace
else:
    ASTRA_DB_KEYSPACE = None
```

```python
import cassio


cassio.init(
    database_id=ASTRA_DB_ID,
    token=ASTRA_DB_TOKEN,
    keyspace=ASTRA_DB_KEYSPACE,
)
```

### OpenAI anahtarı

OpenAI tarafından sunulan gömmeleri (embeddings) kullanmak için bir OpenAI API Anahtarı sağlamanız gerekir:

```python
os.environ["OPENAI_API_KEY"] = getpass("OpenAI API Anahtarı:")
```

### Veriyi indir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Vektör Deposunu Oluşturma ve Doldurma

Şimdi Paul Graham'a ait bazı makaleleri yerel bir dosyadan yükleyecek ve bunları Cassandra Vektör Deposu'nda saklayacaksınız.

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge: {len(documents)}")
print(f"İlk belge, kimlik (id): {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    "İlk belge, metin"
    f" ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

### Cassandra Vektör Deposunu Başlatma

Vektör deposunun oluşturulması, mevcut değilse temel veritabanı tablosunun oluşturulmasını içerir:

```python
cassandra_store = CassandraVectorStore(
    table="cass_v_table", embedding_dimension=1536
)
```

Şimdi bu depoyu, daha sonra sorgulama yapmak üzere bir LlamaIndex soyutlaması olan `index` içine sarın:

```python
storage_context = StorageContext.from_defaults(vector_store=cassandra_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Yukarıdaki `from_documents` çağrısının aynı anda birkaç şey yaptığına dikkat edin: giriş belgelerini yönetilebilir boyuttaki parçalara ("düğümler") ayırır, her düğüm için gömme vektörlerini hesaplar ve bunların hepsini Cassandra Vektör Deposu'nda saklar.

## Depoyu Sorgulama

### Temel sorgulama

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar neden AI üzerinde çalışmayı seçti?")
print(response.response)
```

### MMR tabanlı sorgular

MMR (maksimal marjinal alaka düzeyi - maximal marginal relevance) yöntemi, depodan hem sorguyla alakalı hem de birbirinden olabildiğince farklı metin parçalarını getirmek için tasarlanmıştır; buradaki amaç, nihai yanıtın oluşturulması için daha geniş bir bağlam sağlamaktır:

```python
query_engine = index.as_query_engine(vector_store_query_mode="mmr")
response = query_engine.query("Yazar neden AI üzerinde çalışmayı seçti?")
print(response.response)
```

## Mevcut bir depoya bağlanma

Bu depo Cassandra tarafından desteklendiği için tanımı gereği kalıcıdır (persistent). Bu nedenle, daha önce oluşturulmuş ve doldurulmuş bir depoya bağlanmak isterseniz yapmanız gerekenler şunlardır:

```python
new_store_instance = CassandraVectorStore(
    table="cass_v_table", embedding_dimension=1536
)


# İndeks oluşturma (önceden depolanmış vektörlerden)
new_index_instance = VectorStoreIndex.from_vector_store(
    vector_store=new_store_instance
)


# artık sorgulama vb. yapabilirsiniz:
query_engine = new_index_instance.as_query_engine(similarity_top_k=5)
response = query_engine.query(
    "Yazar AI üzerinde çalışmadan önce ne okudu?"
)
```

```python
print(response.response)
```

## Belgeleri indeksten kaldırma

Öncelikle, indeksten oluşturulan bir `Retriever` kullanarak belgenin parçalarının veya "düğümlerinin" (nodes) açık bir listesini alın:

```python
retriever = new_index_instance.as_retriever(
    vector_store_query_mode="mmr",
    similarity_top_k=3,
    vector_store_kwargs={"mmr_prefetch_factor": 4},
)
nodes_with_scores = retriever.retrieve(
    "Yazar AI üzerinde çalışmadan önce ne okudu?"
)
```

```python
print(f"{len(nodes_with_scores)} düğüm bulundu.")
for idx, node_with_score in enumerate(nodes_with_scores):
    print(f"    [{idx}] puan = {node_with_score.score}")
    print(f"        id    = {node_with_score.node.node_id}")
    print(f"        metin  = {node_with_score.node.text[:90]} ...")
```

Ancak bekleyin! Vektör deposunu kullanırken, silinecek mantıklı birim olarak kendisine ait herhangi bir düğümü değil, **belgeyi** (document) düşünmelisiniz. Bu durumda, sadece tek bir metin dosyası eklediniz, dolayısıyla tüm düğümler aynı `ref_doc_id` değerine sahip olacaktır:

```python
print("Düğümlerin ref_doc_id değerleri:")
print("\n".join([nws.node.ref_doc_id for nws in nodes_with_scores]))
```

Şimdi yüklediğiniz metin dosyasını kaldırmanız gerektiğini varsayalım:

```python
new_store_instance.delete(nodes_with_scores[0].node.ref_doc_id)
```

Aynı sorguyu tekrarlayın ve şimdi sonuçları kontrol edin. *Hiçbir sonuç* bulunmadığını görmelisiniz:

```python
nodes_with_scores = retriever.retrieve(
    "Yazar AI üzerinde çalışmadan önce ne okudu?"
)


print(f"{len(nodes_with_scores)} düğüm bulundu.")
```

## Metaveri filtreleme (Metadata filtering)

Cassandra vektör deposu, sorgu sırasında tam eşleşen `anahtar=değer` çiftleri şeklinde metaveri filtrelemeyi destekler. Tamamen yeni bir Cassandra tablosu üzerinde çalışan aşağıdaki hücreler bu özelliği göstermektedir.

Bu demoda, kısa tutmak adına tek bir kaynak belge yüklenmiştir (`../data/paul_graham/paul_graham_essay.txt` metin dosyası). Bununla birlikte, belgelere eklenen metaveriler üzerindeki koşullarla sorguları nasıl kısıtlayabileceğinizi göstermek için belgeye bazı özel metaveriler ekleyeceksiniz.

```python
md_storage_context = StorageContext.from_defaults(
    vector_store=CassandraVectorStore(
        table="cass_v_table_md", embedding_dimension=1536
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
    "./data/paul_graham", file_metadata=my_file_metadata
).load_data()
md_index = VectorStoreIndex.from_documents(
    md_documents, storage_context=md_storage_context
)
```

Hepsi bu: artık sorgu motorunuza filtreleme ekleyebilirsiniz:

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
```

```python
md_query_engine = md_index.as_query_engine(
    filters=MetadataFilters(
        filters=[ExactMatchFilter(key="source_type", value="essay")]
    )
)
md_response = md_query_engine.query(
    "Yazar Lisp'e ve resme değer verdi mi?"
)
print(md_response.response)
```

Filtrelemenin devrede olduğunu test etmek için, filtreyi yalnızca `"dinos"` belgelerini kullanacak şekilde değiştirmeyi deneyin... bu sefer hiçbir cevap gelmeyecek :)
