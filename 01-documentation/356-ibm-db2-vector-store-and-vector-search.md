---
title: IBM Db2 Vektör Deposu ve Vektör Araması
 | LlamaIndex OSS Belgeleri
---

# IBM Db2 Vektör Deposu ve Vektör Araması

LlamaIndex'in Db2 entegrasyonu (`llama-index-vector-stores-db2`), MIT lisansı altında dağıtılan IBM ilişkisel veritabanı Db2 sürüm v12.1.2 ve üzeri ile çalışmak için vektör deposu ve vektör araması yetenekleri sağlar. Kullanıcılar sağlanan uygulamaları olduğu gibi kullanabilir veya belirli ihtiyaçlar için özelleştirebilirler. Temel özellikler şunları içerir:

- Meta verilerle vektör depolama
- Vektör benzerlik araması ve filtreleme seçenekleri
- EUCLIDEAN\_DISTANCE, DOT\_PRODUCT, COSINE, MANHATTAN\_DISTANCE, HAMMING\_DISTANCE ve EUCLIDEAN\_SQUARED mesafe metrikleri için destek
- İndeks oluşturma ve Yaklaşık en yakın komşu (Approximate nearest neighbors) araması ile performans optimizasyonu (Yakında eklenecektir).

### Db2 Vektör Deposu ve Arama ile LlamaIndex Kullanımı İçin Ön Koşullar

Db2 LlamaIndex Vektör Deposu ve Araması için entegrasyon paketi olan `llama-index-vector-stores-db2` paketini kurun.

```bash
# pip install llama-index-vector-stores-db2
```

### Db2 Vektör Deposuna Bağlanma

Aşağıdaki örnek kod, Db2 Veritabanına nasıl bağlanılacağını gösterecektir. Yukarıdaki bağımlılıkların yanı sıra, vektör veri tipi desteğine sahip bir Db2 veritabanı örneğinin (v12.1.2+ sürümü ile) çalışıyor olması gerekir.

```python
import ibm_db
import ibm_db_dbi


database = "" # Veritabanı adı
username = "" # Kullanıcı adı
password = "" # Parola


try:
    connection = ibm_db_dbi.connect(database, username, password)
    print("Bağlantı başarılı!")
except Exception as e:
    print("Bağlantı başarısız!", e)
```

### Gerekli bağımlılıkları içe aktarın

```python
from llama_index.core.schema import NodeRelationship, RelatedNodeInfo, TextNode
from llama_index.core.vector_stores.types import (
    ExactMatchFilter,
    MetadataFilters,
    VectorStoreQuery,
)


from llama_index.vector_stores.db2 import base as db2llamavs
from llama_index.vector_stores.db2 import DB2LlamaVS, DistanceStrategy
```

### Belgeleri Yükleme

```python
# Bir belge listesi tanımlayın (Bu sahte örnekler 4 rastgele belgedir)
text_json_list = [
    {
        "text": "Db2, LOB verilerini diğer veri türlerinden farklı şekilde işler. Sonuç olarak, LOB sütunlarını tanımlarken ve LOB verilerini eklerken bazen ek adımlar atmanız gerekebilir.",
        "id_": "doc_1_2_P4",
        "embedding": [1.0, 0.0],
        "relationships": "test-0",
        "metadata": {
            "weight": 1.0,
            "rank": "a",
            "url": "https://www.ibm.com/docs/en/db2-for-zos/12?topic=programs-storing-lob-data-in-tables",
        },
    },
    {
        "text": "Db2 13 ile tanıtılan SQL Data Insights, Db2 for z/OS motoruna yapay zeka (AI) işlevselliği getirdi. Db2 verilerinizde gizli değerli içgörüleri bulmak için SQL AI sorgusu çalıştırma yeteneği sağlayarak daha iyi iş kararları almanıza yardımcı olur.",
        "id_": "doc_15.5.1_P1",
        "embedding": [0.0, 1.0],
        "relationships": "test-1",
        "metadata": {
            "weight": 2.0,
            "rank": "c",
            "url": "https://community.ibm.com/community/user/datamanagement/blogs/neena-cherian/2023/03/07/accelerating-db2-ai-queries-with-the-new-vector-pr",
        },
    },
    {
        "text": "Veri yapıları, DB2® kullanımı için gerekli olan ögelerdir. Verilerinizi düzenlemek için bu ögelere erişebilir ve kullanabilirsiniz. Veri yapılarına örnek olarak tablolar, tablo alanları (table spaces), indeksler, anahtarlar, görünümler (views) ve veritabanları verilebilir.",
        "id_": "id_22.3.4.3.1_P2",
        "embedding": [1.0, 1.0],
        "relationships": "test-2",
        "metadata": {
            "weight": 3.0,
            "rank": "d",
            "url": "https://www.ibm.com/docs/en/zos-basic-skills?topic=concepts-db2-data-structures",
        },
    },
    {
        "text": "DB2®, kontrol ettiği veriler hakkında bilgi içeren bir dizi tablo tutar. Bu tablolar toplu olarak katalog (catalog) olarak bilinir. Katalog tabloları tablolar, görünümler ve indeksler gibi DB2 nesneleri hakkında bilgi içerir. Bir nesne oluşturduğunuzda, değiştirdiğinizde veya sildiğinizde, DB2 kataloğun bu nesneyi tanımlayan satırlarını ekler, günceller veya siler.",
        "id_": "id_3.4.3.1_P3",
        "embedding": [2.0, 1.0],
        "relationships": "test-3",
        "metadata": {
            "weight": 4.0,
            "rank": "e",
            "url": "https://www.ibm.com/docs/en/zos-basic-skills?topic=objects-db2-catalog",
        },
    },
]
```

```python
# Llama Metin Düğümleri oluşturun
text_nodes = []
for text_json in text_json_list:
    # RelatedNodeInfo kullanarak ilişkileri kurun
    relationships = {
        NodeRelationship.SOURCE: RelatedNodeInfo(
            node_id=text_json["relationships"]
        )
    }


    # Meta veri sözlüğünü hazırlayın; gerekirse belirli alanları hariç tutabilirsiniz
    metadata = {
        "weight": text_json["metadata"]["weight"],
        "rank": text_json["metadata"]["rank"],
    }


    # Bir TextNode örneği oluşturun
    text_node = TextNode(
        text=text_json["text"],
        id_=text_json["id_"],
        embedding=text_json["embedding"],
        relationships=relationships,
        metadata=metadata,
    )


    text_nodes.append(text_node)
print(text_nodes)
```

### Farklı mesafe stratejileriyle Vektör Depoları oluşturun

İlk olarak, her biri farklı mesafe fonksiyonlarına sahip üç vektör deposu oluşturacağız.

Db2 Veritabanına manuel olarak bağlandığınızda Documents\_DOT, Documents\_COSINE ve Documents\_EUCLIDEAN adlı üç tablo göreceksiniz.

```python
# Farklı mesafe stratejileri kullanarak belgeleri Db2 Vektör Deposuna aktarın (Ingest)
vector_store_dot = DB2LlamaVS.from_documents(
    text_nodes,
    table_name="Documents_DOT",
    client=connection,
    distance_strategy=DistanceStrategy.DOT_PRODUCT,
    embed_dim=2,
)
vector_store_max = DB2LlamaVS.from_documents(
    text_nodes,
    table_name="Documents_COSINE",
    client=connection,
    distance_strategy=DistanceStrategy.COSINE,
    embed_dim=2,
)
vector_store_euclidean = DB2LlamaVS.from_documents(
    text_nodes,
    table_name="Documents_EUCLIDEAN",
    client=connection,
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
    embed_dim=2,
)
```

### Metinler için ekleme, silme ve temel benzerlik araması işlemlerinin gösterilmesi

```python
def manage_texts(vector_stores):
    for i, vs in enumerate(vector_stores, start=1):
        # Metin ekleme
        try:
            vs.add_texts(text_nodes, metadata)
            print(f"\n\n\nVektör deposu {i} için metin ekleme tamamlandı\n\n\n")
        except Exception as ex:
            print(
                f"\n\n\nVektör deposu {i} için yinelenen eklemede beklenen hata\n\n\n"
            )


        # 'doc_id' değerini kullanarak metin silme
        vs.delete("test-1")
        print(f"\n\n\nVektör deposu {i} için metin silme tamamlandı\n\n\n")


        # Benzerlik araması
        query = VectorStoreQuery(
            query_embedding=[1.0, 1.0], similarity_top_k=3
        )
        results = vs.query(query=query)
        print(
            f"\n\n\nVektör deposu {i} için benzerlik araması sonuçları: {results}\n\n\n"
        )




vector_store_list = [
    vector_store_dot,
    vector_store_max,
    vector_store_euclidean,
]
manage_texts(vector_store_list)
```

### Şimdi 3 vektör deposunun tamamında gelişmiş aramalar yapacağız.

```python
def conduct_advanced_searches(vector_stores):
    for i, vs in enumerate(vector_stores, start=1):


        def query_without_filters_returns_all_rows_sorted_by_similarity():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtresiz benzerlik araması
            print("\nFiltresiz benzerlik araması sonuçları:")
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], similarity_top_k=3
            )
            print(vs.query(query=query))


        query_without_filters_returns_all_rows_sorted_by_similarity()


        def query_with_filters_returns_multiple_matches():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtreli benzerlik araması
            print("\nFiltreli benzerlik araması sonuçları:")
            filters = MetadataFilters(
                filters=[ExactMatchFilter(key="rank", value="c")]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=3
            )
            result = vs.query(query)
            print(result.ids)


        query_with_filters_returns_multiple_matches()


        def query_with_filter_applies_top_k():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtreli benzerlik araması
            print("\nTop k filtreli benzerlik araması sonuçları:")
            filters = MetadataFilters(
                filters=[ExactMatchFilter(key="rank", value="c")]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=1
            )
            result = vs.query(query)
            print(result.ids)


        query_with_filter_applies_top_k()


        def query_with_filter_applies_node_id_filter():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtreli benzerlik araması
            print("\nnode_id filtreli benzerlik araması sonuçları:")
            filters = MetadataFilters(
                filters=[ExactMatchFilter(key="rank", value="c")]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0],
                filters=filters,
                similarity_top_k=3,
                node_ids=["452D24AB-F185-414C-A352-590B4B9EE51B"],
            )
            result = vs.query(query)
            print(result.ids)


        query_with_filter_applies_node_id_filter()


        def query_with_exact_filters_returns_single_match():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtreli benzerlik araması
            print("\nFiltreli benzerlik araması sonuçları:")
            filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="rank", value="c"),
                    ExactMatchFilter(key="weight", value=2),
                ]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], filters=filters
            )
            result = vs.query(query)
            print(result.ids)


        query_with_exact_filters_returns_single_match()


        def query_with_contradictive_filter_returns_no_matches():
            filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="weight", value=2),
                    ExactMatchFilter(key="weight", value=3),
                ]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], filters=filters
            )
            result = vs.query(query)
            print(result.ids)


        query_with_contradictive_filter_returns_no_matches()


        def query_with_filter_on_unknown_field_returns_no_matches():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtreli benzerlik araması
            print("\nFiltreli benzerlik araması sonuçları:")
            filters = MetadataFilters(
                filters=[ExactMatchFilter(key="unknown_field", value="c")]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], filters=filters
            )
            result = vs.query(query)
            print(result.ids)


        query_with_filter_on_unknown_field_returns_no_matches()


        def delete_removes_document_from_query_results():
            vs.delete("test-1")
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], similarity_top_k=2
            )
            result = vs.query(query)
            print(result.ids)


        delete_removes_document_from_query_results()




conduct_advanced_searches(vector_store_list)
```

### Uçtan Uca Demo
