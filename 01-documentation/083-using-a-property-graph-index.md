# Özellik Grafiği İndeksi (Property Graph Index) Kullanımı

Bir özellik grafiği (property graph); etiketli node'lardan (yani varlık kategorileri, metin etiketleri vb.) ve özelliklerden (yani meta verilerden) oluşan, ilişkilerle birbirine bağlanarak yapılandırılmış yollar oluşturan bir bilgi koleksiyonudur.

LlamaIndex'te `PropertyGraphIndex`, şunlar etrafında temel orkestrasyon sağlar:

-   Bir grafik oluşturma
-   Bir grafiği sorgulama

## Kullanım

Temel kullanım, sınıfı içe aktarıp kullanmak kadar basittir:

```python
from llama_index.core import PropertyGraphIndex

# oluştur
index = PropertyGraphIndex.from_documents(
    documents,
)

# kullan
retriever = index.as_retriever(
    include_text=True,  # eşleşen yollarla birlikte kaynak parçayı (chunk) dahil et
    similarity_top_k=2,  # vektör kg node getirmesi için en yakın k değer
)
nodes = retriever.retrieve("Test")

query_engine = index.as_query_engine(
    include_text=True,  # eşleşen yollarla birlikte kaynak parçayı dahil et
    similarity_top_k=2,  # vektör kg node getirmesi için en yakın k değer
)
response = query_engine.query("Test")

# kaydet ve yükle
index.storage_context.persist(persist_dir="./storage")

from llama_index.core import StorageContext, load_index_from_storage

index = load_index_from_storage(
    StorageContext.from_defaults(persist_dir="./storage")
)

# mevcut grafik deposundan (ve isteğe bağlı vektör deposundan) yükleme
index = PropertyGraphIndex.from_existing(
    property_graph_store=graph_store, vector_store=vector_store, ...
)
```

### İnşa Etme (Construction)

LlamaIndex'te özellik grafiği inşası, her bir parça üzerinde bir dizi `kg_extractors` (kg çıkarıcılar) çalıştırarak ve varlıkları ile ilişkileri her bir LlamaIndex node'una meta veri olarak ekleyerek çalışır. Burada istediğiniz kadar çıkarıcı kullanabilirsiniz ve hepsi uygulanacaktır.

Eğer [veri alma boru hattı (ingestion pipeline)](/python/framework/module_guides/loading/ingestion_pipeline) ile dönüşümler (transformations) veya meta veri çıkarıcılar kullandıysanız, bu size çok tanıdık gelecektir (ve bu `kg_extractors` çıkarıcılar veri alma boru hattı ile uyumludur)!

Çıkarıcılar uygun argüman (kwarg) kullanılarak ayarlanır:

```python
index = PropertyGraphIndex.from_documents(
    documents,
    kg_extractors=[extractor1, extractor2, ...],
)

# ek dökümanlar / node'lar ekle
index.insert(document)
index.insert_nodes(nodes)
```

Belirtilmezse varsayılan değerler `SimpleLLMPathExtractor` ve `ImplicitPathExtractor`'dır.

Tüm `kg_extractors` detayları aşağıda verilmiştir.

#### (Varsayılan) `SimpleLLMPathExtractor`

(`varlık1`, `ilişki`, `varlık2`) formatındaki tek adımlı yolları (single-hop paths) çıkarmak ve ayrıştırmak için bir LLM kullanarak kısa ifadeler çıkarır.

```python
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor

kg_extractor = SimpleLLMPathExtractor(
    llm=llm,
    max_paths_per_chunk=10,
    num_workers=4,
    show_progress=False,
)
```

İsterseniz istemi (prompt) ve yolları ayrıştırmak için kullanılan fonksiyonu da özelleştirebilirsiniz.

İşte basit (ancak yüzeysel) bir örnek:

```python
prompt = (
    "Aşağıda bir metin verilmiştir. Metne dayanarak, her satırda `özne,yüklem,nesne` "
    "biçiminde en fazla {max_paths_per_chunk} bilgi üçlüsü çıkarın. "
    "Stopword'lerden kaçının.\n"
)


def parse_fn(response_str: str) -> List[Tuple[str, str, str]]:
    lines = response_str.split("\n")
    triples = [line.split(",") for line in lines]
    return triples


kg_extractor = SimpleLLMPathExtractor(
    llm=llm,
    extract_prompt=prompt,
    parse_fn=parse_fn,
)
```

#### (Varsayılan) `ImplicitPathExtractor`

Her bir LlamaIndex node nesnesi üzerindeki `node.relationships` özniteliğini kullanarak yolları çıkarır.

Bu çıkarıcı, LlamaIndex node nesnelerinde zaten var olan özellikleri ayrıştırdığı için çalıştırmak için bir LLM veya embedding modeline ihtiyaç duymaz.

```python
from llama_index.core.indices.property_graph import ImplicitPathExtractor

kg_extractor = ImplicitPathExtractor()
```

#### `DynamicLLMPathExtractor`

İsteğe bağlı izin verilen varlık türleri ve ilişki türleri listesine göre yolları (varlık türleri dahil!) çıkaracaktır. Eğer hiçbiri sağlanmazsa, LLM türleri uygun gördüğü şekilde atayacaktır. Eğer sağlanırlarsa, LLM'e rehberlik edecekler ancak tam olarak bu türleri zorunlu kılmayacaklardır.

```python
from llama_index.core.indices.property_graph import DynamicLLMPathExtractor

kg_extractor = DynamicLLMPathExtractor(
    llm=llm,
    max_triplets_per_chunk=20,
    num_workers=4,
    allowed_entity_types=["POLITICIAN", "POLITICAL_PARTY"],
    allowed_relation_types=["PRESIDENT_OF", "MEMBER_OF"],
)
```

#### `SchemaLLMPathExtractor`

İzin verilen varlıklar, ilişkiler ve hangi varlıkların hangi ilişkilere bağlanabileceği konusundaki katı bir şemayı takip ederek yolları çıkarır.

Pydantic, LLM'lerden gelen yapılandırılmış çıktılar ve bazı akıllı doğrulamalar kullanarak dinamik olarak bir şema belirleyebilir ve yol başına çıkarımları doğrulayabiliriz.

```python
from typing import Literal
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

# büyük harf ve alt çizgi ile ayrılmış olması önerilir
entities = Literal["PERSON", "PLACE", "THING"]
relations = Literal["PART_OF", "HAS", "IS_A"]
schema = {
    "PERSON": ["PART_OF", "HAS", "IS_A"],
    "PLACE": ["PART_OF", "HAS"],
    "THING": ["IS_A"],
}

kg_extractor = SchemaLLMPathExtractor(
    llm=llm,
    possible_entities=entities,
    possible_relations=relations,
    kg_validation_schema=schema,
    strict=True,  # false ise şema dışındaki üçlülere izin verir
    num_workers=4,
    max_triplets_per_chunk=10,
)
```

Bu çıkarıcı son derece özelleştirilebilirdir ve şu seçeneklere sahiptir:

-   Şemanın çeşitli yönlerini özelleştirme (yukarıda görüldüğü gibi)
-   `extract_prompt` istemini özelleştirme
-   Şema dışındaki üçlülere izin verip vermemek için `strict=False` ve `strict=True` seçenekleri
-   Eğer bir Pydantic uzmanıysanız ve özel doğrulamaya sahip kendi Pydantic sınıfınızı oluşturmak istiyorsanız kendi özel `kg_schema_cls` sınıfınızı geçirme.

### Getirme ve Sorgulama

Etiketli özellik grafikleri, node'ları ve yolları getirmek için birkaç şekilde sorgulanabilir. LlamaIndex'te, aynı anda birkaç node getirme yöntemini birleştirebiliriz!

```python
# bir getirici oluştur
retriever = index.as_retriever(sub_retrievers=[retriever1, retriever2, ...])

# bir sorgu motoru oluştur
query_engine = index.as_query_engine(
    sub_retrievers=[retriever1, retriever2, ...]
)
```

Hiçbir alt getirici sağlanmazsa varsayılanlar `LLMSynonymRetriever` ve (eğer embedding'ler etkinse) `VectorContextRetriever`'dır.

Şu anki tüm getiriciler şunları içerir:

-   `LLMSynonymRetriever` - LLM tarafından oluşturulan anahtar kelimelere/eş anlamlılara göre getirme yapar.
-   `VectorContextRetriever` - Gömülü (embedded) grafik node'larına göre getirme yapar.
-   `TextToCypherRetriever` - Özellik grafiğinin şemasına dayanarak LLM'den cypher oluşturmasını ister.
-   `CypherTemplateRetriever` - LLM tarafından tahmin edilen parametrelerle bir cypher şablonu kullanır.
-   `CustomPGRetriever` - Alt sınıfa ayırması ve özel getirme mantığını uygulaması kolaydır.

Genellikle, bu alt getiricilerden bir veya daha fazlasını tanımlar ve bunları `PGRetriever`'a geçirirsiniz:

```python
from llama_index.core.indices.property_graph import (
    PGRetriever,
    VectorContextRetriever,
    LLMSynonymRetriever,
)

sub_retrievers = [
    VectorContextRetriever(index.property_graph_store, ...),
    LLMSynonymRetriever(index.property_graph_store, ...),
]

retriever = PGRetriever(sub_retrievers=sub_retrievers)

nodes = retriever.retrieve("<sorgu>")
```

Tüm getiriciler hakkında daha fazla ayrıntı için aşağıyı okumaya devam edin.

#### (Varsayılan) `LLMSynonymRetriever`

`LLMSynonymRetriever`, sorguyu alır ve node'ları (ve dolayısıyla bu node'lara bağlı yolları) getirmek için anahtar kelimeler ve eş anlamlılar oluşturmaya çalışır.

Getiriciyi açıkça tanımlamak, birkaç seçeneği özelleştirmenize olanak tanır. İşte varsayılanlar:

```python
from llama_index.core.indices.property_graph import LLMSynonymRetriever

prompt = (
    "Verilen bir başlangıç sorgusu için, büyük/küçük harf, çoğul ekleri, "
    "yaygın ifadeler vb. olası durumları dikkate alarak toplamda {max_keywords} "
    "adedine kadar eş anlamlı veya ilgili anahtar kelime oluşturun.\n"
    "Tüm eş anlamlıları/anahtar kelimeleri '^' sembolüyle ayırarak sağlayın: "
    "'keyword1^keyword2^...'\n"
    "Not: Sonuç, '^' sembolüyle ayrılmış tek bir satırda olmalıdır."
    "----\n"
    "SORGUSU: {query_str}\n"
    "----\n"
    "ANAHTAR KELİMELER: "
)


def parse_fn(self, output: str) -> list[str]:
    matches = output.strip().split("^")

    # veri alma ile normalize etmek için büyük harfe çevir
    return [x.strip().capitalize() for x in matches if x.strip()]


synonym_retriever = LLMSynonymRetriever(
    index.property_graph_store,
    llm=llm,
    # getirilen yollarla birlikte kaynak parça metnini dahil et
    include_text=False,
    synonym_prompt=prompt,
    output_parsing_fn=parse_fn,
    max_keywords=10,
    # node getirmeden sonra takip edilecek ilişkilerin derinliği
    path_depth=1,
)

retriever = index.as_retriever(sub_retrievers=[synonym_retriever])
```

#### (Varsayılan, eğer destekleniyorsa) `VectorContextRetriever`

`VectorContextRetriever`, node'ları vektör benzerliklerine göre getirir ve ardından bu node'lara bağlı yolları çeker.

Grafik deponuz vektörleri destekliyorsa, depolama için yalnızca o grafik deposunu yönetmeniz yeterlidir. Aksi takdirde, grafik deposuna ek olarak bir vektör deposu sağlamanız gerekecektir (varsayılan olarak bellek içi `SimpleVectorStore` kullanır).

```python
from llama_index.core.indices.property_graph import VectorContextRetriever

vector_retriever = VectorContextRetriever(
    index.property_graph_store,
    # yalnızca grafik deposu vektör sorgularını desteklemediğinde gereklidir
    # vector_store=index.vector_store,
    embed_model=embed_model,
    # getirilen yollarla birlikte kaynak parça metnini dahil et
    include_text=False,
    # çekilecek node sayısı
    similarity_top_k=2,
    # node getirmeden sonra takip edilecek ilişkilerin derinliği
    path_depth=1,
    # VectorStoreQuery sınıfı için diğer her türlü anahtar kelime argümanını sağlayabilir
    ...,
)

retriever = index.as_retriever(sub_retrievers=[vector_retriever])
```

#### `TextToCypherRetriever`

`TextToCypherRetriever`, bir cypher sorgusu oluşturmak ve yürütmek için bir grafik deposu şeması, sorgunuz ve metinden cypher'a (text-to-cypher) dönüşüm için bir istem şablonu kullanır.

**NOT:** `SimplePropertyGraphStore` aslında bir grafik veritabanı olmadığı için cypher sorgularını desteklemez.

Şemayı `index.property_graph_store.get_schema_str()` kullanarak inceleyebilirsiniz.

```python
from llama_index.core.indices.property_graph import TextToCypherRetriever

DEFAULT_RESPONSE_TEMPLATE = (
    "Oluşturulan Cypher sorgusu:\n{query}\n\n" "Cypher Yanıtı:\n{response}"
)
DEFAULT_ALLOWED_FIELDS = ["text", "label", "type"]

DEFAULT_TEXT_TO_CYPHER_TEMPLATE = (
    index.property_graph_store.text_to_cypher_template,
)


cypher_retriever = TextToCypherRetriever(
    index.property_graph_store,
    # LLM'i özelleştirin, varsayılan Settings.llm'dir
    llm=llm,
    # metinden cypher'a şablonunu özelleştirin.
    # `schema` ve `question` şablon argümanlarını gerektirir
    text_to_cypher_template=DEFAULT_TEXT_TO_CYPHER_TEMPLATE,
    # cypher sonucunun bir metin node'una nasıl yerleştirileceğini özelleştirin.
    # `query` ve `response` şablon argümanlarını gerektirir
    response_template=DEFAULT_RESPONSE_TEMPLATE,
    # oluşturulan cypher'ı temizleyebilen/doğrulayabilen isteğe bağlı bir çağrılabilir
    cypher_validator=None,
    # sonuçtaki izin verilen alanlar
    allowed_output_field=DEFAULT_ALLOWED_FIELDS,
)
```

**NOT:** Rastgele cypher yürütmenin riskleri vardır. Üretim ortamında güvenli kullanımı sağlamak için gerekli önlemleri (salt okunur roller, sandbox ortamı vb.) aldığınızdan emin olun.

#### `CypherTemplateRetriever`

Bu, `TextToCypherRetriever`'ın daha kısıtlı bir versiyonudur. LLM'in herhangi bir cypher ifadesi oluşturmasına izin vermek yerine, bir cypher şablonu sağlayabilir ve LLM'in boşlukları doldurmasını sağlayabiliriz.

Bunun nasıl çalıştığını göstermek için küçük bir örnek:

```python
# NOT: güncel v1 sürümü gereklidir
from pydantic import BaseModel, Field
from llama_index.core.indices.property_graph import CypherTemplateRetriever

# şablon parametreleri içeren bir sorgu yazın
cypher_query = """
MATCH (c:Chunk)-[:MENTIONS]->(o)
WHERE o.name IN $names
RETURN c.text, o.name, o.label;
"""


# sorgumuzun parametrelerini temsil edecek bir pydantic sınıfı oluşturun
# sınıf alanları doğrudan cypher sorgusunu çalıştırmak için parametre olarak kullanılır
class TemplateParams(BaseModel):
    """Bir cypher sorgusu için şablon parametreleri."""

    names: list[str] = Field(
        description="Bilgi grafiğinde arama yapmak için kullanılacak varlık isimleri veya anahtar kelimelerin listesi."
    )


template_retriever = CypherTemplateRetriever(
    index.property_graph_store, TemplateParams, cypher_query
)
```

## Depolama (Storage)

Şu anda özellik grafikleri (property graphs) için desteklenen grafik depoları şunlardır:

|                            | Bellek İçi (In-Memory) | Yerel Embedding Desteği | Asenkron (Async) | Sunucu veya disk tabanlı? |
| -------------------------- | ---------------------- | ----------------------- | ---------------- | ------------------------- |
| SimplePropertyGraphStore   | ✅                     | ❌                      | ❌               | Disk                      |
| Neo4jPropertyGraphStore    | ❌                     | ✅                      | ❌               | Sunucu                    |
| NebulaPropertyGraphStore   | ❌                     | ❌                      | ❌               | Sunucu                    |
| TiDBPropertyGraphStore     | ❌                     | ✅                      | ❌               | Sunucu                    |
| FalkorDBPropertyGraphStore | ❌                     | ✅                      | ❌               | Sunucu                    |

### Diske Kaydetme ve Diskten Yükleme

Varsayılan özellik grafiği deposu olan `SimplePropertyGraphStore`, her şeyi bellekte saklar ve diske kaydeder/diskten yükler.

Varsayılan grafik deposuyla bir indeksi kaydetme/yükleme örneği:

```python
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.indices import PropertyGraphIndex

# oluştur
index = PropertyGraphIndex.from_documents(documents)

# kaydet
index.storage_context.persist("./storage")

# yükle
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### Entegrasyonlar ile Kaydetme ve Yükleme

Entegrasyonlar genellikle otomatik olarak kaydedilir. Bazı grafik depoları vektörleri desteklerken bazıları desteklemeyebilir. Bir grafik deposunu her zaman harici bir vektör veritabanıyla da birleştirebilirsiniz.

Bu örnek, Neo4j ve Qdrant kullanarak bir özellik grafiği indeksini nasıl kaydedebileceğinizi/yükleyebileceğinizi gösterir.

**Not:** Qdrant geçirilmeseydi, Neo4j embedding'leri kendi başına saklar ve kullanırdı. Bu örnek, bunun ötesindeki esnekliği göstermektedir.

`pip install llama-index-graph-stores-neo4j llama-index-vector-stores-qdrant`

```python
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.indices import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient

vector_store = QdrantVectorStore(
    "graph_collection",
    client=QdrantClient(...),
    aclient=AsyncQdrantClient(...),
)

graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="<sifre>",
    url="bolt://localhost:7687",
)

# bir indeks oluşturur
index = PropertyGraphIndex.from_documents(
    documents,
    property_graph_store=graph_store,
    # isteğe bağlı, neo4j de vektörleri doğrudan destekler
    vector_store=vector_store,
    embed_kg_nodes=True,
)

# mevcut grafik/vektör deposundan yükle
index = PropertyGraphIndex.from_existing(
    property_graph_store=graph_store,
    # isteğe bağlı, neo4j de vektörleri doğrudan destekler
    vector_store=vector_store,
    embed_kg_nodes=True,
)
```

### Özellik Grafiği Deposunu Doğrudan Kullanma

Özellik grafikleri için temel depolama sınıfı `PropertyGraphStore`'dur. Bu özellik grafiği depoları, farklı türdeki `LabeledNode` nesneleri kullanılarak inşa edilir ve `Relation` nesneleri kullanılarak birbirine bağlanır.

Bunları kendimiz oluşturabilir ve kendimiz ekleyebiliriz!

```python
from llama_index.core.graph_stores import (
    SimplePropertyGraphStore,
    EntityNode,
    Relation,
)
from llama_index.core.schema import TextNode

graph_store = SimplePropertyGraphStore()

entities = [
    EntityNode(name="llama", label="ANIMAL", properties={"key": "val"}),
    EntityNode(name="index", label="THING", properties={"key": "val"}),
]

relations = [
    Relation(
        label="HAS",
        source_id=entities[0].id,
        target_id=entities[1].id,
        properties={},
    )
]

graph_store.upsert_nodes(entities)
graph_store.upsert_relations(relations)

# isteğe bağlı olarak metin parçaları (chunks) da ekleyebiliriz
source_chunk = TextNode(id_="source", text="Llamamın bir indeksi var.")

# varlıklarımızın her biri için ilişki oluşturun
source_relations = [
    Relation(
        label="HAS_SOURCE",
        source_id=entities[0].id,
        target_id="source",
    ),
    Relation(
        label="HAS_SOURCE",
        source_id=entities[1].id,
        target_id="source",
    ),
]
graph_store.upsert_llama_nodes([source_chunk])
graph_store.upsert_relations(source_relations)
```

Grafik deposundaki diğer yardımcı metotlar şunlardır:

-   `graph_store.get(ids=[])` - kimliklere (ids) göre node'ları getirir
-   `graph_store.get(properties={"key": "val"})` - eşleşen özelliklere göre node'ları getirir
-   `graph_store.get_rel_map([entity_node], depth=2)` - belirli bir derinliğe kadar üçlüleri getirir
-   `graph_store.get_llama_nodes(['id1'])` - orijinal metin node'larını getirir
-   `graph_store.delete(ids=['id1'])` - kimliklere göre siler
-   `graph_store.delete(properties={"key": "val"})` - özelliklere göre siler
-   `graph_store.structured_query("<cypher sorgusu>")` - bir cypher sorgusu çalıştırır (grafik deposu destekliyorsa)

Ek olarak, bunların hepsinin asenkron destek için `a` versiyonları mevcuttur (yani `aget`, `adelete` vb.).

## Gelişmiş Özelleştirme

LlamaIndex'teki tüm bileşenlerde olduğu gibi, modülleri alt sınıflara ayırabilir ve tam ihtiyacınız olan şekilde çalışması için özelleştirebilir veya yeni fikirler ile yeni modülleri deneyebilirsiniz!

### Çıkarıcıları (Extractors) Alt Sınıflara Ayırma

LlamaIndex'teki grafik çıkarıcılar `TransformComponent` sınıfını alt sınıfa ayırır. Daha önce veri alma boru hattı (ingestion pipeline) ile çalıştıysanız, aynı sınıf olduğu için bu size tanıdık gelecektir.

Çıkarıcılar için gereksinim, grafik verilerini node'un meta verilerine yerleştirmeleridir; bu veriler daha sonra indeks tarafından işlenecektir.

İşte özel bir çıkarıcı oluşturmak için küçük bir alt sınıfa ayırma örneği:

```python
from llama_index.core.graph_store.types import (
    EntityNode,
    Relation,
    KG_NODES_KEY,
    KG_RELATIONS_KEY,
)
from llama_index.core.schema import BaseNode, TransformComponent


class MyGraphExtractor(TransformComponent):
    # init metodu isteğe bağlıdır
    # def __init__(self, ...):
    #     ...

    def __call__(
        self, llama_nodes: list[BaseNode], **kwargs
    ) -> list[BaseNode]:
        for llama_node in llama_nodes:
            # mevcut varlıkların/ilişkilerin üzerine yazmadığınızdan emin olun

            existing_nodes = llama_node.metadata.pop(KG_NODES_KEY, [])
            existing_relations = llama_node.metadata.pop(KG_RELATIONS_KEY, [])

            existing_nodes.append(
                EntityNode(
                    name="llama", label="ANIMAL", properties={"key": "val"}
                )
            )
            existing_nodes.append(
                EntityNode(
                    name="index", label="THING", properties={"key": "val"}
                )
            )

            existing_relations.append(
                Relation(
                    label="HAS",
                    source_id="llama",
                    target_id="index",
                    properties={},
                )
            )

            # meta verilere geri ekle

            llama_node.metadata[KG_NODES_KEY] = existing_nodes
            llama_node.metadata[KG_RELATIONS_KEY] = existing_relations

        return llama_nodes

    # isteğe bağlı asenkron metot
    # async def acall(self, llama_nodes: list[BaseNode], **kwargs) -> list[BaseNode]:
    #    ...
```

### Getiricileri (Retrievers) Alt Sınıflara Ayırma

Getirici, çıkarıcılardan biraz daha karmaşıktır ve alt sınıfa ayırmayı kolaylaştırmak için kendi özel sınıfına sahiptir.

Getirme işleminin dönüş türü son derece esnektir. Şunlar olabilir:

-   bir dize (string)
-   bir `TextNode`
-   bir `NodeWithScore`
-   yukarıdakilerden oluşan bir liste

İşte özel bir getirici oluşturmak için küçük bir alt sınıfa ayırma örneği:

```python
from llama_index.core.indices.property_graph import (
    CustomPGRetriever,
    CUSTOM_RETRIEVE_TYPE,
)


class MyCustomRetriever(CustomPGRetriever):
    def init(self, my_option_1: bool = False, **kwargs) -> None:
        """Sınıf yapılandırıcısından geçirilen tüm kwargs'ı kullanır."""
        self.my_option_1 = my_option_1
        # isteğe bağlı olarak self.graph_store ile bir şeyler yapın

    def custom_retrieve(self, query_str: str) -> CUSTOM_RETRIEVE_TYPE:
        # self.graph_store ile bazı işlemler yapın
        return "result"

    # isteğe bağlı asenkron metot
    # async def acustom_retrieve(self, query_str: str) -> str:
    #     ...


custom_retriever = MyCustomRetriever(graph_store, my_option_1=True)

retriever = index.as_retriever(sub_retrievers=[custom_retriever])
```

Daha karmaşık özelleştirmeler ve kullanım durumları için kaynak kodu incelemeniz ve doğrudan `BasePGRetriever` sınıfını alt sınıfa ayırmanız önerilir.

# Örnekler

Aşağıda, `PropertyGraphIndex`'i sergileyen bazı örnek notebook'ları bulabilirsiniz:

-   [Temel Kullanım](/python/examples/property_graph/property_graph_basic)
-   [Neo4j Kullanımı](/python/examples/property_graph/property_graph_neo4j)
-   [Nebula Kullanımı](/python/examples/property_graph/property_graph_nebula)
-   [Neo4j ve Yerel Modellerle Gelişmiş Kullanım](/python/examples/property_graph/property_graph_advanced)
-   [Özellik Grafiği Deposu Kullanımı](/python/examples/property_graph/graph_store)
-   [Özel Grafik Getiricisi Oluşturma](/python/examples/property_graph/property_graph_custom_retriever)
-   [KG Çıkarıcıları Karşılaştırma](/python/examples/property_graph/dynamic_kg_extraction)