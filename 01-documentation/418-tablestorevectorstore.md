---
title: Tablestore Vektör Deposu (TablestoreVectorStore)
 | LlamaIndex OSS Belgeleri
---

# Tablestore Vektör Deposu (TablestoreVectorStore)

> [Tablestore](https://www.aliyun.com/product/ots); temelde olan/istenen yapılandırılmış (structured) ve yarı yapılandırılmış verilerin devasa bir meblağda ve yekünde barındırılıp (storage) depolanmasını / tutulmasını etkin kılan, tamamıyla altyapısı yönetilen, denetimi sağlanan NoSQL tabanlı bir bulut veritabanı platformu ve hizmetidir.

Bu not defteri (notebook), `Tablestore` vektör veritabanına bağlı/ilişkin birtakım işlevlerin ve opsiyonların nasıl kullanılacağını gösterir.

Tablestore'u aktif/etkin edebilmek için halihazırda varlığı olan bir örneği / nesne referansını / oturumu (instance) atamanız (oluşturmanız) gerekir. Referans/kaynak oluşturma (örnek ataması - instancing) yönergeleri için [örnek/oturum oluşturma talimatlarına](https://help.aliyun.com/zh/tablestore/getting-started/manage-the-wide-column-model-in-the-tablestore-console) göz atabilirsiniz.

## Kurulum (Install)

```bash
%pip install llama-index-vector-stores-tablestore
```

```python
import getpass
import os


os.environ["end_point"] = getpass.getpass("Tablestore end_point (bitis/uç noktasi):")
os.environ["instance_name"] = getpass.getpass("Tablestore instance_name (örnek/oturum adi):")
os.environ["access_key_id"] = getpass.getpass("Tablestore access_key_id (erisim_kodu_kimligi):")
os.environ["access_key_secret"] = getpass.getpass(
    "Tablestore access_key_secret (erisim_kodu_gizli_anahtari):"
)
```

## Örnek (Example)

Vektör deposu (vector store) oluşturun.

```python
import os


from llama_index.core import MockEmbedding
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import (
    VectorStoreQuery,
    MetadataFilters,
    MetadataFilter,
    FilterCondition,
    FilterOperator,
)
from llama_index.core.vector_stores.types import (
    VectorStoreQueryMode,
)
from tablestore import FieldSchema, FieldType, VectorMetricType


from llama_index.vector_stores.tablestore import TablestoreVectorStore


vector_dimension = 4


store = TablestoreVectorStore(
    endpoint=os.getenv("end_point"),
    instance_name=os.getenv("instance_name"),
    access_key_id=os.getenv("access_key_id"),
    access_key_secret=os.getenv("access_key_secret"),
    vector_dimension=vector_dimension,
    vector_metric_type=VectorMetricType.VM_COSINE,
    # isteğe bağlı (optional): metadatalar (meta veriler) için vektörel olmayan alanları süzüp/ayrıştırarak elekten geçirmek (filter non-vector fields) niyeti doğrultusunda, bir özel mod (custom) eşlemesi (metadata mapping) tatbik edilir (used).
    metadata_mappings=[
        FieldSchema(
            "type", FieldType.KEYWORD, index=True, enable_sort_and_agg=True
        ),
        FieldSchema(
            "time", FieldType.LONG, index=True, enable_sort_and_agg=True
        ),
    ],
)
```

Tablo formu ve bir indeks oluşturun (Create table and index).

```python
store.create_table_if_not_exist()
store.create_search_index_if_not_exist()
```

Deneme/Test maksatlı sahte (mock) ama işlevli yeni bir gömme (embedding) yaratın (New a mock embedding for test).

```python
embedder = MockEmbedding(vector_dimension)
```

Birtakım metin evrakları veya belgeleri (doküman) hazırlayın/tertipleyin.

```python
texts = [
    TextNode(
        id_="1",
        text="İki gangster tetikçisinin (hitmen), bir boksörün, mafya patronunun (gangster) ve de onun eşiyle, dahi yemek yiyen soygunculardan müteşekkil ikilisinin bizzat şiddet ve günahlardan/ezalardan arınmaya (redemption) uzanan o paralel hattında dahi harmanlanıp kesiştiği harika dört efsane/hikaye (tales).",
        metadata={"type": "a", "time": 1995},
    ),
    TextNode(
        id_="2",
        text="Toplum nezdindeki o Joker adı denilen/lakaplı bela musibeti taa tüm Gotham şehrini birbirine atıp hallaç pamuğu gibi de darmaduman ederek dehşet rüzgarlarını pervasızlığa attığında; evet Batman de dahi durmayacak ve tüm varlığını, aklaki gücünü kötülüğe ve rezilliklere direnmekteki psikolojik yahut fiziksel/bedensel limitinin ta doruklarına dahi o büyük eyleme atacak (greatest test of his ability) ve ona kafa koyacaktır.",
        metadata={"type": "a", "time": 1990},
    ),
    TextNode(
        id_="3",
        text="Bir vakit uyku dahi çekemeyen (insomniac) bir adet düz kurumsal ofis yakalı / çalışanı (office worker) ile onun tam zıttındaki umursamaz bir vurdumduymazlığa / bana neci ("devil-may-care") olan/atfedilen sabun mucidi / ustası ikilisinin teşkil eyleyip yola serdiği tüm yer altına inen o kurumsal kavga dahi seremonisinin (dövüş kulübü - fight club) dahi evrelerin tüm seyrinde bilhassa nasıl formlardan ta büyük evrelere dahi kaydıklarını vs.",
        metadata={"type": "a", "time": 2009},
    ),
    TextNode(
        id_="4",
        text="Dünyada dahi olan/atfedilen (dream-sharing technology) o uykudaki daldıkları ve rüyana da misafir olduğu gibi tüm hayalleri kopyalayan yapıları aracılığıyla usta formlu / ve oldukça kurnaz olan sirket sırrına göz dikmiş (corporate secrets thief) adama; şimdilerde tek bir şart takdim edildi... Ve bu zıt tabanlı hedefte bir patronların şahı konumunda olan CEO nezdindeki asıl akıla (beyne / fikre) yepyeni de bir kıvılcımı yahut asım zembereğini resmen ekip yeşertmesidir (planting an idea).",
        metadata={"type": "a", "time": 2023},
    ),
    TextNode(
        id_="5",
        text="Bilgisayar sarsıcı ustası (hacker) dahi; kendi büründüğü nezdinde o şatafatlı evrenlerin sahteliğinden arınarak; gizeme boğulu sistem başkaldırıcı isyancılarından (rebels); evrenindeki ve yaşadığı gerçekliğin ve de o devasa makinelerin evresine dahi kafa atmanın o isyankar dahi yapısını keşfeder.",
        metadata={"type": "b", "time": 2018},
    ),
    TextNode(
        id_="6",
        text="Biri tamı tamına yepyeni stajından sıyrılmış / çömez (rookie) bir dedektif; birisi evrenini devirmiş kaşar dahi/kurt (veteran) evresindeki dedektif de; evrenin yedi tepe / yahut yedi asıl mühim temel ve ölümcül cezasındaki eylemi (seven deadly sins) dahi güdülerindeki tek (motives) tabana dahi çekerek kendine yol atfeden seri cinayetli (katil) ile oynadığı o dev cümbüş... (hunt a serial killer).",
        metadata={"type": "c", "time": 2010},
    ),
    TextNode(
        id_="7",
        text="Ailenin şatafatı ile / köken teşkil etmiş ve yapılanma / kök de salmış koca bir suç krallığı/suç mafya tabanındaki hanedanın (organized crime dynasty's); vaktine, demine yahut kocalmasına evrilen demdeki / yaşı dahi kemale (aging) basmış reisinin, dahi elinde var olan / işlettiğine hükmettiği tekmil krallığını/örtülü gücünü (clandestine empire) kendi bu isteklere pek yüz dahi eylem vermeyen oğlunun tepesine devretmesi.",
        metadata={"type": "a", "time": 2023},
    ),
]
for t in texts:
    t.embedding = embedder.get_text_embedding(t.text)
```

Biraz / bazı (birkaç tane) doküman yazın (Write some docs).

```python
store.add(texts)
```

```bash
['1', '2', '3', '4', '5', '6', '7']
```

Belgeleri (docs) silin.

```python
store.delete("1")
```

Filtreler eşliğinde sorgulayın.

```python
store.query(
    query=VectorStoreQuery(
        query_embedding=embedder.get_text_embedding("doğa (nature) harp/kavga (fight) bedenle/fiziki (physical)"),
        similarity_top_k=5,
        filters=MetadataFilters(
            filters=[
                MetadataFilter(
                    key="type", value="a", operator=FilterOperator.EQ
                ),
                MetadataFilter(
                    key="time", value=2020, operator=FilterOperator.LTE
                ),
            ],
            condition=FilterCondition.AND,
        ),
    ),
)
```

```bash
VectorStoreQueryResult(nodes=[TextNode(id_='1', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1995, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='2', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1990, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='3', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2009, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}')], similarities=[1.0, 1.0, 1.0], ids=['1', '2', '3'])
```

Tam/tüm metin araması (Full text search): sorgulama metodu / query mode = METİN (TEXT).

```python
query_result = store.query(
    query=VectorStoreQuery(
        mode=VectorStoreQueryMode.TEXT_SEARCH,
        query_str="computer",
        similarity_top_k=5,
    ),
)
print(query_result)
```

```bash
VectorStoreQueryResult(nodes=[TextNode(id_='5', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2018, 'type': 'b'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}')], similarities=[2.673976421356201], ids=['5'])
```

HİBRİT / MELEZ sorgu (HYBRID query).

```python
query_result = store.query(
    query=VectorStoreQuery(
        mode=VectorStoreQueryMode.HYBRID,
        query_embedding=embedder.get_text_embedding("doğa (nature) harp/kavga (fight) bedenle/fiziki (physical)"),
        query_str="python",
        similarity_top_k=5,
    ),
)
print(query_result)
```

```bash
VectorStoreQueryResult(nodes=[TextNode(id_='1', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1995, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='2', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 1990, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='3', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2009, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='4', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2023, 'type': 'a'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}'), TextNode(id_='5', embedding=[0.5, 0.5, 0.5, 0.5], metadata={'time': 2018, 'type': 'b'}, excluded_embed_metadata_keys=[], excluded_llm_metadata_keys=[], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text='...', mimetype='text/plain', start_char_idx=None, end_char_idx=None, metadata_seperator='\n', text_template='{metadata_str}\n\n{content}')], similarities=[1.0, 1.0, 1.0, 1.0, 1.0], ids=['1', '2', '3', '4', '5'])
```
