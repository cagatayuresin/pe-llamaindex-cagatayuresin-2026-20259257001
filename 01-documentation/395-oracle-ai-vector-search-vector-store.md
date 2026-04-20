---
title: Oracle AI Vektör Araması: Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Oracle AI Vektör Araması: Vektör Deposu

Oracle AI Vektör Araması (AI Vector Search), anahtar kelimeler yerine anlambilime dayalı olarak veri sorgulamanıza olanak tanıyan Yapay Zeka (AI) iş yükleri için tasarlanmıştır. Oracle AI Vektör Araması'nın en büyük avantajlarından biri, yapılandırılmamış veriler üzerindeki anlamsal (semantik) aramanın, iş verileri üzerindeki ilişkisel arama ile tek bir sistemde birleştirilebilmesidir. Bu sadece güçlü değil, aynı zamanda çok daha etkilidir; çünkü özel bir vektör veritabanı eklemenize gerek kalmaz, böylece birden fazla sistem arasındaki veri parçalanması sorununu ortadan kaldırır.

Buna ek olarak vektörleriniz, Oracle Database'in aşağıdaki gibi en güçlü özelliklerinden yararlanabilir:

- [Bölümleme Desteği (Partitioning Support)](https://www.oracle.com/database/technologies/partitioning.html)
- [Gerçek Uygulama Kümeleri (Real Application Clusters - RAC) ölçeklenebilirliği](https://www.oracle.com/database/real-application-clusters/)
- [Exadata akıllı taramalar (smart scans)](https://www.oracle.com/database/technologies/exadata/software/smartscan/)
- [Coğrafi olarak dağıtılmış veritabanları arasında Shard işleme](https://www.oracle.com/database/distributed-database/)
- [İşlemler (Transactions)](https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/transactions.html)
- [Paralel SQL](https://docs.oracle.com/en/database/oracle/oracle-database/21/vldbg/parallel-exec-intro.html#GUID-D28717E4-0F77-44F5-BB4E-234C31D4E4BA)
- [Olağanüstü Durum Kurtarma (Disaster Recovery)](https://www.oracle.com/database/data-guard/)
- [Güvenlik (Security)](https://www.oracle.com/security/database-security/)
- [Oracle Makine Öğrenimi (Machine Learning)](https://www.oracle.com/artificial-intelligence/database-machine-learning/)
- [Oracle Graf Veritabanı (Graph Database)](https://www.oracle.com/database/integrated-graph-database/)
- [Oracle Mekansal ve Graf (Spatial and Graph)](https://www.oracle.com/database/spatial/)
- [Oracle Blok Zinciri (Blockchain)](https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/dbms_blockchain_table.html#GUID-B469E277-978E-4378-A8C1-26D3FF96C9A6)
- [JSON](https://docs.oracle.com/en/database/oracle/oracle-database/23/adjsn/json-in-oracle-database.html)

Bu kılavuz, Oracle AI Vektör Araması içindeki Vektör Yeteneklerinin nasıl kullanılacağını gösterir.

Oracle Database ile yeni başlıyorsanız, veritabanı ortamınızı kurmaya yönelik harika bir giriş sunan [ücretsiz Oracle 23 AI](https://www.oracle.com/database/free/#resources) sürümünü keşfetmeyi düşünün. Veritabanıyla çalışırken, güvenlik ve özelleştirme için varsayılan sistem kullanıcısı yerine kendi kullanıcınızı oluşturmanız tavsiye edilir. Kullanıcı oluşturma adımları için Oracle'da bir kullanıcının nasıl kurulacağını da gösteren [uçtan uca kılavuzumuza](https://github.com/run-llama/llama_index/blob/main/docs/examples/cookbooks/oracleai_demo.ipynb) bakabilirsiniz. Ayrıca kullanıcı ayrıcalıklarını anlamak, veritabanı güvenliğini verimli bir şekilde yönetmek için kritiktir. Kullanıcı hesaplarının yönetimi ve güvenliği hakkındaki resmi [Oracle kılavuzundan](https://docs.oracle.com/en/database/oracle/oracle-database/19/admqs/administering-user-accounts-and-security.html#GUID-36B21D72-1BBB-46C9-A0C9-F0D2A8591B8D) daha fazla bilgi edinebilirsiniz.

### Ön Karşılamalar

Llama Index'i Oracle AI Vektör Araması ile kullanmak için lütfen Oracle Python İstemci sürücüsünü kurun.

```bash
%pip install llama-index-vector-stores-oracledb
```

### Oracle AI Vektör Aramasına Bağlanın

Aşağıdaki örnek kod, Oracle Database'e nasıl bağlanılacağını gösterir. Varsayılan olarak python-oracledb, doğrudan Oracle Database'e bağlanan bir 'Thin' (İnce) modunda çalışır. Bu mod Oracle İstemci kütüphanelerine ihtiyaç duymaz. Ancak, python-oracledb bunları kullandığında bazı ek işlevler kullanılabilir hale gelir. Oracle İstemci kütüphaneleri kullanıldığında python-oracledb'nin 'Thick' (Kalın) modunda olduğu söylenir. Her iki mod da Python Veritabanı API v2.0 Spesifikasyonunu destekleyen kapsamlı işlevselliğe sahiptir. Her modda desteklenen özellikleri anlatan [kılavuza](https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html#featuresummary) bakın. Thin modunu kullanamıyorsanız Thick moduna geçmek isteyebilirsiniz.

```python
import oracledb


# lütfen kullanıcı adınızı, şifrenizi, ana makine adınızı (hostname) ve servis adınızı güncelleyin
username = "<kullanici_adi>"
password = "<sifre>"
dsn = "<ana_makine_adi>/<servis_adi>"


try:
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    print("Bağlantı başarılı!")
except Exception as ex:
    print("İndeks oluşturma sırasında istisna oluştu:", ex)
```

### Oracle AI Vektör Araması ile Oynamak İçin Gerekli Bağımlılıkları İçe Aktarın

```python
import sys
import os


from llama_index.core.schema import NodeRelationship, RelatedNodeInfo, TextNode
from llama_index.core.vector_stores.types import (
    ExactMatchFilter,
    MetadataFilters,
    VectorStoreQuery,
)


from llama_index.vector_stores.oracledb import base as orallamavs
from llama_index.vector_stores.oracledb import OraLlamaVS, DistanceStrategy
```

### Belgeleri Yükleyin

```python
# Bir belge listesi tanımlayın (Bu örnekler 4 rastgele belgedir)


text_json_list = [
    {
        "text": "Önceki sorulardan herhangi birinin yanıtı evet ise, veritabanı aramayı durdurur ve belirtilen tablo alanından (tablespace) yer ayırır; aksi takdirde yer, veritabanı varsayılan paylaşımlı geçici tablo alanından ayrılır.",
        "id_": "cncpt_15.5.3.2.2_P4",
        "embedding": [1.0, 0.0],
        "relationships": "test-0",
        "metadata": {
            "weight": 1.0,
            "rank": "a",
            "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/logical-storage-structures.html#GUID-5387D7B2-C0CA-4C1E-811B-C7EB9B636442",
        },
    },
    {
        "text": "Veritabanı açık olduğu her an bir tablo alanı çevrimiçi (erişilebilir) veya çevrimdışı (erişilemez) olabilir.\nVeriler kullanıcılara sunulsun diye bir tablo alanı genellikle çevrimiçidir. SYSTEM tablo alanı ve geçici tablo alanları çevrimdışına alınamaz.",
        "id_": "cncpt_15.5.5_P1",
        "embedding": [0.0, 1.0],
        "relationships": "test-1",
        "metadata": {
            "weight": 2.0,
            "rank": "c",
            "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/logical-storage-structures.html#GUID-D02B2220-E6F5-40D9-AFB5-BC69BCEF6CD4",
        },
    },
    {
        "text": "Veritabanı, LOB'ları diğer veri türlerinden farklı şekilde saklar. Bir LOB sütunu oluşturmak dolaylı olarak bir LOB segmenti ve bir LOB indeksi oluşturur. Her zaman birlikte saklanan LOB segmentini ve LOB indeksini içeren tablo alanı, tabloyu içeren tablo alanından farklı olabilir.\nBazen veritabanı, küçük miktarlardaki LOB verilerini ayrı bir LOB segmenti yerine tablonun kendisinde saklayabilir.",
        "id_": "cncpt_22.3.4.3.1_P2",
        "embedding": [1.0, 1.0],
        "relationships": "test-2",
        "metadata": {
            "weight": 3.0,
            "rank": "d",
            "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/concepts-for-database-developers.html#GUID-3C50EAB8-FC39-4BB3-B680-4EACCE49E866",
        },
    },
    {
        "text": "LOB segmenti verileri parça (chunk) adı verilen parçalarda saklar. Bir parça, mantıksal olarak bitişik bir veri blokları kümesidir ve bir LOB için ayrılan en küçük birimdir. Tablodaki bir satır, LOB indeksini işaret eden LOB locator adlı bir işaretçi (pointer) saklar. Tablo sorgulandığında, veritabanı LOB parçalarını hızlıca bulmak için LOB indeksini kullanır.",
        "id_": "cncpt_22.3.4.3.1_P3",
        "embedding": [2.0, 1.0],
        "relationships": "test-3",
        "metadata": {
            "weight": 4.0,
            "rank": "e",
            "url": "https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/concepts-for-database-developers.html#GUID-3C50EAB8-FC39-4BB3-B680-4EACCE49E866",
        },
    },
]
```

```python
# Llama Metin Düğümleri (Text Nodes) Oluşturun
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

### AI Vektör Araması Kullanarak Farklı Mesafe Stratejileriyle Bir Dizi Vektör Deposu Oluşturun

Öncelikle her biri farklı mesafe fonksiyonlarına sahip üç vektör deposu oluşturacağız. Henüz içlerinde indeks oluşturmadığımız için şimdilik sadece tablolar oluşturacaklar. Daha sonra bu vektör depolarını HNSW indeksleri oluşturmak için kullanacağız.

Oracle Veritabanına manuel olarak bağlanabilirsiniz ve `Documents_DOT`, `Documents_COSINE` ve `Documents_EUCLIDEAN` adlı üç tablo göreceksiniz.

Ardından, tablolar üzerinde HNSW indeksleri yerine IVF indeksleri oluşturmak için kullanılacak `Documents_DOT_IVF`, `Documents_COSINE_IVF` ve `Documents_EUCLIDEAN_IVF` adlı üç ek tablo daha oluşturacağız.

Oracle AI Vektör Araması'nın desteklediği farklı indeks türleri hakkında daha fazla bilgi edinmek için [bu kılavuza](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/manage-different-categories-vector-indexes.html) bakın.

```python
# Farklı mesafe stratejilerini kullanarak belgeleri Oracle Vektör Deposuna aktarın


vector_store_dot = OraLlamaVS.from_documents(
    text_nodes,
    table_name="Documents_DOT",
    client=connection,
    distance_strategy=DistanceStrategy.DOT_PRODUCT,
)
vector_store_max = OraLlamaVS.from_documents(
    text_nodes,
    table_name="Documents_COSINE",
    client=connection,
    distance_strategy=DistanceStrategy.COSINE,
)
vector_store_euclidean = OraLlamaVS.from_documents(
    text_nodes,
    table_name="Documents_EUCLIDEAN",
    client=connection,
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
)


# Farklı mesafe stratejilerini kullanarak belgeleri Oracle Vektör Deposuna aktarın
vector_store_dot_ivf = OraLlamaVS.from_documents(
    text_nodes,
    table_name="Documents_DOT_IVF",
    client=connection,
    distance_strategy=DistanceStrategy.DOT_PRODUCT,
)
vector_store_max_ivf = OraLlamaVS.from_documents(
    text_nodes,
    table_name="Documents_COSINE_IVF",
    client=connection,
    distance_strategy=DistanceStrategy.COSINE,
)
vector_store_euclidean_ivf = OraLlamaVS.from_documents(
    text_nodes,
    table_name="Documents_EUCLIDEAN_IVF",
    client=connection,
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
)
```

### Metinler İçin Ekleme, Silme İşlemlerini ve Temel Benzerlik Aramasını Gösterme

```python
def manage_texts(vector_stores):
    """
    Her vektör deposuna metinler ekler, dublike eklemeler için hata yönetimini gösterir
    ve metinlerin silinmesini gerçekleştirir. Her vektör deposu için benzerlik aramalarını
    ve indeks oluşturmayı sergiler.


    Args:
    - vector_stores (list): OracleVS örneklerinin bir listesi.
    """
    for i, vs in enumerate(vector_stores, start=1):
        # 'id' değerini kullanarak metinleri silme
        vs.delete("test-1")
        print(f"\n\n\nVektör deposu {i} için metinleri silme tamamlandı\n\n\n")


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
    vector_store_dot_ivf,
    vector_store_max_ivf,
    vector_store_euclidean_ivf,
]
manage_texts(vector_store_list)
```

### Her Mesafe Stratejisi İçin Belirli Parametrelerle İndeks Oluşturmayı Gösterme

```python
def create_search_indices(connection):
    """
    Vektör depoları için, her biri kendi mesafe stratejisine göre uyarlanmış
    belirli parametrelerle arama indeksleri oluşturur.
    """
    # DOT_PRODUCT stratejisi için indeks
    # Varsayılan parametrelerle bir HNSW indeksi oluşturuyoruz
    # Bu, varsayılan olarak 8 Paralel İşçi ile bir HNSW indeksi oluşturacak ve
    # Oracle AI Vektör Araması tarafından kullanılan Varsayılan Doğruluğu kullanacaktır.
    orallamavs.create_index(
        connection,
        vector_store_dot,
        params={"idx_name": "hnsw_idx1", "idx_type": "HNSW"},
    )


    # Belirli parametrelerle COSINE stratejisi için indeks
    # 16 paralellik ve %97 Hedef Doğruluğu Spesifikasyonu ile bir HNSW indeksi oluşturuyoruz
    orallamavs.create_index(
        connection,
        vector_store_max,
        params={
            "idx_name": "hnsw_idx2",
            "idx_type": "HNSW",
            "accuracy": 97,
            "parallel": 16,
        },
    )


    # Belirli parametrelerle EUCLIDEAN_DISTANCE stratejisi için indeks
    # neighbors = 64 ve efConstruction = 100 olarak İleri Düzey Kullanıcı Parametrelerini 
    # belirterek bir HNSW indeksi oluşturuyoruz
    orallamavs.create_index(
        connection,
        vector_store_euclidean,
        params={
            "idx_name": "hnsw_idx3",
            "idx_type": "HNSW",
            "neighbors": 64,
            "efConstruction": 100,
        },
    )


    # Belirli parametrelerle DOT_PRODUCT stratejisi için indeks
    # Varsayılan parametrelerle bir IVF indeksi oluşturuyoruz
    # Bu, varsayılan olarak 8 Paralel İşçi ile bir IVF indeksi oluşturacak ve 
    # Oracle AI Vektör Araması tarafından kullanılan Varsayılan Doğruluğu kullanacaktır.
    orallamavs.create_index(
        connection,
        vector_store_dot_ivf,
        params={
            "idx_name": "ivf_idx1",
            "idx_type": "IVF",
        },
    )


    # Belirli parametrelerle COSINE stratejisi için indeks
    # 32 paralellik ve %90 Hedef Doğruluğu Spesifikasyonu ile bir IVF indeksi oluşturuyoruz
    orallamavs.create_index(
        connection,
        vector_store_max_ivf,
        params={
            "idx_name": "ivf_idx2",
            "idx_type": "IVF",
            "accuracy": 90,
            "parallel": 32,
        },
    )


    # Belirli parametrelerle EUCLIDEAN_DISTANCE stratejisi için indeks
    # neighbor_part = 64 olarak İleri Düzey Kullanıcı Parametresini belirterek 
    # bir IVF indeksi oluşturuyoruz
    orallamavs.create_index(
        connection,
        vector_store_euclidean_ivf,
        params={
            "idx_name": "ivf_idx3",
            "idx_type": "IVF",
            "neighbor_part": 64,
        },
    )


    print("İndeks oluşturma tamamlandı.")


create_search_indices(connection)
```

### Şimdi altı vektör deposunun tamamında bir dizi gelişmiş arama yapacağız. Bu üç aramanın her birinin filtreli ve filtresiz versiyonu vardır. Filtre sadece id'si 'c' olan belgeyi seçer ve diğer her şeyi eler.

```python
# İndeksleri oluşturduktan sonra gelişmiş aramalar yapın
def conduct_advanced_searches(vector_stores):
    # Belge meta verilerine karşı doğrudan karşılaştırma için bir filtre oluşturma
    # Bu filtre, meta veri 'rank' değeri tam olarak 'c' olan belgeleri dahil etmeyi amaçlar


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
                query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=1
            )
            result = vs.query(query)
            print(result.ids)


        query_with_filters_returns_multiple_matches()


        def query_with_filter_applies_top_k():
            print(f"\n--- Vektör Deposu {i} Gelişmiş Aramalar ---")
            # Filtreli benzerlik araması
            print("\nFiltreyle arama sonuçları (top_k uygulanmış):")
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
            print("\nDüğüm Kimliği (node_id) filtresi uygulanmış sonuçlar:")
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
            print("\nKesin (exact) filtrelerle arama sonuçları:")
            filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="rank", value="c"),
                    ExactMatchFilter(key="weight", value=2.0),
                ]
            )
            query = VectorStoreQuery(
                query_embedding=[1.0, 1.0], filters=filters
            )
            result = vs.query(query)
            print(result.ids)


        query_with_exact_filters_returns_single_match()


        def query_with_contradictive_filter_returns_no_matches():
            # Çelişkili filtrelerle arama
            filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="weight", value=2.0),
                    ExactMatchFilter(key="weight", value=3.0),
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
            # Bilinmeyen alan üzerinde filtreyle arama
            print("\nBilinmeyen alan üzerinde filtreyle arama sonuçları:")
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
            # Silme işleminin sonuçlardan belgeyi kaldırdığını doğrulama
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

Oracle AI Vektör Araması yardımıyla uçtan uca bir RAG boru hattı oluşturmak için lütfen tam demo kılavuzumuza [Oracle AI Vektör Araması Uçtan Uca Demo Kılavuzu](https://github.com/run-llama/llama_index/blob/main/docs/examples/cookbooks/oracleai_demo.ipynb) bakın.
