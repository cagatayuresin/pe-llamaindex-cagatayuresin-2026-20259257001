---
title: Supabase Vektör Deposu (Supabase Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Supabase Vektör Deposu (Supabase Vector Store)

Bu not defterimizde (notebook); aramaları vektör bağlamında (vector searches) LlamaIndex içinde icra ve tatbik edebilmek/edinim sağlamak üzere [Vecs'i](https://supabase.github.io/vecs/) nasıl değerlendirip kullanabileceğimizi göstereceğiz. \
Supabase tabanı / arayüzü üzerinde veritabanı (database) barındırmaya (hosting) ilişkin talimatları detaylandırmak üzere [bu rehbere](https://supabase.github.io/vecs/hosting/) göz atabilirsiniz.

Eğer bu Not Defterini (Notebook) Colab ortamında açıyorsanız, muhtemelen LlamaIndex'i 🦙 sisteminize kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-supabase
```

```bash
!pip install llama-index
```

```python
import logging
import sys


# Hata ayıklama (debug) günlüklerini (logs) görmek/incelemek için yorum satırını kaldırarak aktif (uncomment) edin
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import SimpleDirectoryReader, Document, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore
import textwrap
```

### OpenAI Ayarları (Setup OpenAI)

En başta ilk aşamanız; OpenAI lisans anahtarını yapılandırmaktır (configure). İndeks yığınına (index) yönlendirilip yüklenecek olan verilerin gömmelerini (embeddings) tesis/var etmek için kullanılacaktır.

```python
import os


os.environ["OPENAI_API_KEY"] = "[sizin_openai_api_anahtariniz]"
```

Veriyi İndirin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükleme (Loading documents)

SimpleDirectoryReader üzerinden/aracılığıyla; bu yoldaki `./data/paul_graham/` evrakı / o dizin içindeki ilgili belgeleri (documents) içeriye yükleyin.

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(
    "Belge Kimliği (Document ID):",
    documents[0].doc_id,
    "Belge Özeti / Karma Değeri (Document Hash):",
    documents[0].doc_hash,
)
```

```bash
Belge Kimliği (Document ID): fb056993-ee9e-4463-80b4-32cf9509d1d8 Belge Özeti / Karma (Document Hash): 77ae91ab542f3abb308c4d7c77c9bc4c9ad0ccd63144802b7cbe7e1bb3a4094e
```

### Supabase’in vektör deposu vasıtasıyla desteklenerek desteklenen bir indeks oluşturun.

Bu; sistem içinde yer alan ve tam destekli `pgvector` kütüphanesini benimseyen tüm kurgu ve Postgres tabanlı tedarikçiler ile formların tümünde işleyiş yapıp uyumla (with all Postgres providers) çalışacaktır. Şayet dökülen veya dahil o koleksiyon var olmaz yahut da bulunmazsa da, biz de sıfırdan / taze (a new collection) yeni bir koleksiyon yaratmaya gayret edeceğiz (attempt).

> Bilgi Kapsamında (Note): Eklentinizin bir OpenAI menşeli `text-embedding-ada-002` formuna ait bir sistemi/dosyayı kullanmamanız hâlinde gömme mekanizmasının boyut/ebat yapısını dahil etmeniz / ona (pass in) iletmeniz de lazımdır. Mesela `vector_store = SupabaseVectorStore(..., dimension=...)` misalindeki / ibaresindeki gibi.

```python
vector_store = SupabaseVectorStore(
    postgres_connection_string=(
        "postgresql://<kullanici>:<sifre>@<sunucu_adresi>:<port_numarasi>/<veritabani_adi>"
    ),
    collection_name="base_demo",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### İndeksi / Dizini sorgulayın (Query the index)

Sözü edilen eklentilere / indekse sırtımızı dayayarak, şimdi gönül rahatlığıyla birtakım sorgulamalar yöneltebilir (ask questions using our index) ve sualler sorabiliriz.

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar kim? (Who is the author?)")
```

```bash
/Users/suo/miniconda3/envs/llama/lib/python3.9/site-packages/vecs/collection.py:182: UserWarning: Atılan / çekilen sorgu (Query); `cosine_distance` (kosinüs mesafesi) yönünde mevcut kapsayıcı (covering index) evsaflı olan / büründüren bir indekse dahi malik / ve o şarta sahip değil. Bakınız: Collection.create_index (adresine bir göz atın)
  warnings.warn(
```

```python
print(textwrap.fill(str(response), 100))
```

```bash
 Bu eldeki metin ve eser Paul Graham tarafında / yazar Paul Graham tarafından kaleme alınmıştır (The author of this text is Paul Graham).
```

```python
response = query_engine.query("Yazar büyürken neler yaptı? (What did the author do growing up?)")
```

```python
print(textwrap.fill(str(response), 100))
```

```bash
 Yazar makaleler döküp onları bizzat yazıya aktararak, dahası İtalyanca öğreneyazıp üstüne Floransa (Florence) dolaylarını sokağıyla / veyahut tüm evre / safhasıyla iyice kolaçan / bir seyyah formunda keşfedip; bunlara eş akabinde / o evre formunda / kişileri (people) tablollara-portrelere çizen ("painting people"); devamındası bilgisayarlar formuna tabiata dâhil işlerle girişen / uğraşan ("working with computers"), eğitim hanesine RISD dahil dahi eden, bununla beraber / de kira statüsü ve kontrolü yasa tabiatlı regüle ("rent-stabilized") bir hanede yaşam sürerek; üstüne sistemli formda internet ("online store builder/çevrimiçi ürün satım inşası") pazarı inşası yapısıyla iştiraklerine zemin koyup da "Lisp" işlevlerinin kod bloklarını dahi yayına hazırlayıp ("editing Lisp expressions"); üslup olarak hem kompozisyon/ve mektuplarını internet mecrası yayınına sokan; yanısıra resimli eser dökümlerine vararak, üstüne isimsiz cinsten / istenmeyen kirlerin (spam filters) barikatlarına/süzeckilerine zaman yaran / çalışıp dökümler yaran, de misafir yığına (cooking for groups / o yığın kitle formundaki dost zümresine) ocak ve aşçılığına geçip, dahi dahi ("buying a building in Cambridge") Cambridge bünyesinde yeni bina satın alma faaliyetlerine evre tutmuştur.
```

## Meta veri filtrelerini (metadata filters) kullanma

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        **{
            "text": "Esaretin Bedeli (The Shawshank Redemption)",
            "metadata": {
                "author": "Stephen King",
                "theme": "Dostluk (Friendship)",
            },
        }
    ),
    TextNode(
        **{
            "text": "Baba (The Godfather)",
            "metadata": {
                "director": "Francis Ford Coppola",
                "theme": "Mafya (Mafia)",
            },
        }
    ),
    TextNode(
        **{
            "text": "Başlangıç (Inception)",
            "metadata": {
                "director": "Christopher Nolan",
            },
        }
    ),
]
```

```python
vector_store = SupabaseVectorStore(
    postgres_connection_string=(
        "postgresql://<kullanici>:<sifre>@<sunucu_adresi>:<port_numarasi>/<veritabani_adi>"
    ),
    collection_name="metadata_filters_demo",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

Meta veri filtrelerini tanımlayın (Define)

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="theme", value="Mafya/Mafia")]
)
```

Filtrelere takılan / maruz kalmış vektörler deposu verilerini merkeze alıp çekin / retrieve eylemine atın (Retrieve from vector store with filters)

```python
retriever = index.as_retriever(filters=filters)
retriever.retrieve("Inception (Başlangıç) ne/neler hakkındadır?")
```

```bash
[NodeWithScore(node=Node(text='Baba (The Godfather)', doc_id='f837ed85-aacb-4552-b88a-7c114a5be15d', embedding=None, doc_hash='f8ee912e238a39fe2e620fb232fa27ade1e7f7c819b6d5b9cb26f3dddc75b6c0', extra_info={'theme': 'Mafya/Mafia', 'director': 'Francis Ford Coppola'}, node_info={'_node_type': '1'}, relationships={}), score=0.20671339734643313)]
```
