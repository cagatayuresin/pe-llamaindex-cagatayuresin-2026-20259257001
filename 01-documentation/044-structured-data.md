# Yapılandırılmış Veriler (Structured Data)

# LlamaIndex + Yapılandırılmış Veriler Kılavuzu

Modern veri sistemlerinin çoğu, Postgres DB veya Snowflake veri ambarı gibi yapılandırılmış verilere dayanır. LlamaIndex; LLM'ler tarafından desteklenen birçok gelişmiş özellik sunarak hem yapılandırılmamış verilerden yapılandırılmış veriler oluşturmanıza hem de gelişmiş metinden SQL'e (text-to-SQL) özellikleri aracılığıyla bu yapılandırılmış verileri analiz etmenize olanak tanır.

**NOT:** Herhangi bir Metinden SQL'e uygulamasında, keyfi SQL sorgularının yürütülmesinin bir güvenlik riski olabileceği unutulmamalıdır. Kısıtlı roller, salt okunur (read-only) veritabanları, korumalı alanlar (sandboxing) vb. gibi önlemlerin alınması önerilir.

Bu kılavuz, bu yeteneklerin her birini incelemeye yardımcı olur. Özellikle aşağıdaki konuları ele alıyoruz:

-   **Kurulum**: Örnek SQL tablomuzun tanımlanması.
-   **Tablo İndeksimizi Oluşturma**: SQL veritabanından Tablo Şema İndeksine (Table Schema Index) nasıl geçilir?
-   **Doğal dilde SQL sorgularını kullanma**: Doğal dil kullanarak SQL veritabanımızı nasıl sorgularız?

Şehir/nüfus/ülke bilgilerini içeren basit bir örnek tablo üzerinden ilerleyeceğiz. Bu eğitim için bir notebook [burada mevcuttur](/python/examples/index_structs/struct_indices/sqlindexdemo).

## Kurulum

İlk olarak, basit bir sqlite veritabanı kurmak için SQLAlchemy kullanıyoruz:

```python
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
)

engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()
```

Ardından basit bir `city_stats` (şehir_istatistikleri) tablosu oluşturuyoruz:

```python
# şehir SQL tablosunu oluştur
table_name = "city_stats"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("country", String(16), nullable=False),
)
metadata_obj.create_all(engine)
```

Şimdi bazı veri noktaları ekleme zamanı!

Yapılandırılmamış verilerden yapılandırılmış veri noktalarını çıkararak bu tabloyu doldurmak istiyorsanız, aşağıdaki bölüme göz atın. Aksi takdirde, bu tabloyu doğrudan doldurmayı seçebilirsiniz:

```python
from sqlalchemy import insert

rows = [
    {"city_name": "Toronto", "population": 2731571, "country": "Canada"},
    {"city_name": "Tokyo", "population": 13929286, "country": "Japan"},
    {"city_name": "Berlin", "population": 600000, "country": "Germany"},
]
for row in rows:
    stmt = insert(city_stats_table).values(**row)
    with engine.begin() as connection:
        cursor = connection.execute(stmt)
```

Son olarak, SQLAlchemy motorunu `SQLDatabase` sarmalayıcımızla sarmalayabiliriz; bu, veritabanının LlamaIndex içinde kullanılmasına olanak tanır:

```python
from llama_index.core import SQLDatabase

sql_database = SQLDatabase(engine, include_tables=["city_stats"])
```

## Doğal Dilde SQL (Natural Language SQL)

SQL veritabanımızı oluşturduktan sonra, SQL sorgularına dönüştürülen doğal dil sorguları oluşturmak için `NLSQLTableQueryEngine` kullanabiliriz.

Bu sorgu motoruyla kullanmak istediğimiz tabloları belirtmemiz gerektiğini unutmayın. Belirtmezsek, sorgu motoru tüm şema bağlamını çekecektir; bu da LLM'in bağlam penceresini (context window) taşırabilir.

```python
from llama_index.core.query_engine import NLSQLTableQueryEngine

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["city_stats"],
)
query_str = "Hangi şehir en yüksek nüfusa sahip?"
response = query_engine.query(query_str)
```

Bu sorgu motoru; sorgulamak istediğiniz tabloları önceden belirtebildiğiniz her durumda veya tüm tablo şemalarının toplam boyutu ile istemin geri kalanının bağlam pencerenize sığdığı durumlarda kullanılmalıdır.

## Tablo İndeksimizi Oluşturma

Hangi tabloyu kullanmak istediğimizi önceden bilmiyorsak ve tablo şemasının toplam boyutu bağlam penceresi boyutunuzu aşıyorsa, sorgu sırasında doğru şemayı getirebilmek için tablo şemasını bir indekste saklamalıyız.

Bunu yapmanın yolu, bir `SQLDatabase` alan ve `ObjectIndex` yapıcısına geçirilen her `SQLTableSchema` nesnesi için bir `Node` nesnesi üreten `SQLTableNodeMapping` nesnesini kullanmaktır.

```python
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    (SQLTableSchema(table_name="city_stats")),
    ...,
]  # her tablo için bir SQLTableSchema
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
```

Burada `table_node_mapping`'i ve "city_stats" tablo adıyla tek bir `SQLTableSchema` tanımladığımızı görebilirsiniz. Bunları, kullanmak istediğimiz `VectorStoreIndex` sınıf tanımıyla birlikte `ObjectIndex` yapıcısına geçiriyoruz. Bu bize, her bir `Node`'un tablo şemasını ve diğer bağlam bilgilerini içerdiği bir `VectorStoreIndex` verecektir. Ayrıca istediğiniz herhangi bir ek bağlam bilgisini de ekleyebilirsiniz.

```python
# ek bağlam metnini manuel olarak ayarla
city_stats_text = (
    "Bu tablo, belirli bir şehrin nüfusu ve ülkesi hakkında bilgi verir.\n"
    "Kullanıcı kod sözcükleriyle sorgu yapacaktır; burada 'foo' nüfusa ve 'bar' "
    "şehre karşılık gelir."
)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    (SQLTableSchema(table_name="city_stats", context_str=city_stats_text))
]
```

## Doğal Dilde SQL Sorgularını Kullanma

Tablo şema indeksimiz `obj_index`'i tanımladıktan sonra, `SQLDatabase`'imizi ve nesne indeksimizden oluşturulan bir retriever'ı (getirici) geçirerek bir `SQLTableRetrieverQueryEngine` oluşturabiliriz.

```python
from llama_index.core.indices.struct_store import SQLTableRetrieverQueryEngine

query_engine = SQLTableRetrieverQueryEngine(
    sql_database, obj_index.as_retriever(similarity_top_k=1)
)
response = query_engine.query("Hangi şehir en yüksek nüfusa sahip?")
print(response)
```

Şimdi retriever sorgu motorunu sorguladığımızda, ilgili tablo şemasını getirecek ve bir SQL sorgusu sentezleyerek o sorgunun sonuçlarından bir yanıt oluşturacaktır.

## Son Düşünceler

Şimdilik bu kadar! Yapılandırılmış veri desteğimizi iyileştirmenin yollarını sürekli arıyoruz. Sorularınız varsa [Discord kanalımızda](https://discord.gg/dGcwcsnxhU) bize bildirin.