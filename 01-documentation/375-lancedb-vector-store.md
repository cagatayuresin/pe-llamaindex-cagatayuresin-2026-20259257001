---
title: LanceDB Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# LanceDB Vektör Deposu

Bu not defterinde, LlamaIndex'te vektör aramaları gerçekleştirmek için [LanceDB](https://www.lancedb.com)'nin nasıl kullanılacağını göstereceğiz.

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index llama-index-vector-stores-lancedb
```

```bash
%pip install lancedb==0.6.13 # Sadece yukarıdaki hücre lancedb'nin eski bir sürümünü yüklüyorsa gereklidir
```

```bash
# Aynı not defterini yeniden başlatıyorsanız veya yeniden kullanıyorsanız vektör deposu URI'sini yenileyin
! rm -rf ./lancedb
```

```python
import logging
import sys


# Hata ayıklama günlüklerini görmek için yorum satırını kaldırın
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import SimpleDirectoryReader, Document, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.lancedb import LanceDBVectorStore
import textwrap
```

### OpenAI Kurulumu

İlk adım OpenAI anahtarını yapılandırmaktır. Bu anahtar, indekse yüklenen belgeler için gömmeler (embeddings) oluşturmak amacıyla kullanılacaktır.

```python
import openai


openai.api_key = "sk-"
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükleme

`SimpleDirectoryReader` kullanarak `data/paul_graham/` dizininde saklanan belgeleri yükleyin

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print("Belge Kimliği:", documents[0].doc_id, "Belge Hash'i:", documents[0].hash)
```

### İndeksi Oluşturma

Burada, önceden yüklenen belgeleri kullanarak LanceDB destekli bir indeks oluşturuyoruz. `LanceDBVectorStore` birkaç parametre alır:

- `uri` (str, gerekli): LanceDB'nin dosyalarını saklayacağı konum.

- `table_name` (str, isteğe bağlı): Gömmelerin saklanacağı tablo adı. Varsayılan olarak "vectors".

- `nprobes` (int, isteğe bağlı): Kullanılan prob sayısı. Daha yüksek bir sayı aramayı daha doğru ancak daha yavaş hale getirir. Varsayılan olarak 20.

- `refine_factor` (int, isteğe bağlı): Ekstra öğeler okuyarak ve bunları bellekte yeniden sıralayarak sonuçları iyileştirir. Varsayılan olarak None'dır.

- Daha fazla detayı [LanceDB belgelerinde](https://lancedb.github.io/lancedb/ann_indexes) bulabilirsiniz.

##### LanceDB Cloud için:

```python
vector_store = LanceDBVectorStore(
    uri="db://veritabani_adi", # uzak DB URI'niz
    api_key="sk_..", # lancedb cloud api anahtarı
    region="bolgeniz" # yapılandırdığınız bölge
    ...
)
```

```python
vector_store = LanceDBVectorStore(
    uri="./lancedb", mode="overwrite", query_type="hybrid"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

### İndeksi Sorgulama

Artık indeksimizi kullanarak sorular sorabiliriz. `MetadataFilters` aracılığıyla filtreleme yapabilir veya yerel Lance `where` ifadesini kullanabiliriz.

```python
from llama_index.core.vector_stores import (
    MetadataFilters,
    FilterOperator,
    FilterCondition,
    MetadataFilter,
)


from datetime import datetime




query_filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="creation_date",
            operator=FilterOperator.EQ,
            value=datetime.now().strftime("%Y-%m-%d"),
        ),
        MetadataFilter(
            key="file_size", value=75040, operator=FilterOperator.GT
        ),
    ],
    condition=FilterCondition.AND,
)
```

### Hibrit Arama (Hybrid Search)

LanceDB, yeniden sıralama (reranking) yetenekleri ile hibrit arama sunar. Tam belgeler için [buraya](https://lancedb.github.io/lancedb/hybrid_search/hybrid_search/) bakın.

bu örnek `colbert` reranker kullanır. Aşağıdaki hücre `colbert` için gerekli bağımlılıkları kurar. Farklı bir reranker seçerseniz, bağımlılıkları buna göre ayarladığınızdan emin olun.

```bash
! pip install -U torch transformers tantivy@git+https://github.com/quickwit-oss/tantivy-py#164adc87e1a033117001cf70e38c82a53014d985
```

Eğer vektör deposu başlatılırken bir reranker eklemek isterseniz, bunu aşağıdaki gibi parametrelerde iletebilirsiniz:

```python
from lancedb.rerankers import ColbertReranker
reranker = ColbertReranker()
vector_store = LanceDBVectorStore(uri="./lancedb", reranker=reranker, mode="overwrite")
```

```python
import lancedb
```

```python
from lancedb.rerankers import ColbertReranker


reranker = ColbertReranker()
vector_store._add_reranker(reranker)


query_engine = index.as_query_engine(
    filters=query_filters,
    # vector_store_kwargs={
    #     "query_type": "fts",
    # },
)


response = query_engine.query("Viaweb ayda ne kadar ücret alıyordu?")
```

```python
print(response)
print("meta veriler -", response.metadata)
```

**Viaweb, küçük bir mağaza için ayda 100 dolar ve büyük bir mağaza için ayda 300 dolar ücret alıyordu.**

##### `where` ifadesi aracılığıyla doğrudan Lance filtreleri (SQL benzeri):

```python
lance_filter = "metadata.file_name = 'paul_graham_essay.txt' "
retriever = index.as_retriever(vector_store_kwargs={"where": lance_filter})
response = retriever.retrieve("Yazar büyürken neler yaptı?")
```

```python
print(response[0].get_content())
print("meta veriler -", response[0].metadata)
```

```text
Neler Üzerine Çalıştım


Şubat 2021


Üniversiteden önce, okul dışında çalıştığım iki ana konu yazarlık ve programlamaydı. Makale yazmazdım. O zamanlar başlangıç seviyesindeki yazarların ne yazması gerekiyorsa onları yazardım (hâlâ da muhtemelen öyledir): kısa hikayeler. Hikayelerim berbattı. Neredeyse hiç olay örgüsü yoktu, sadece güçlü hisleri olan karakterler vardı ve bunun onları derin kıldığını hayal ederdim.


Yazmayı denediğim ilk programlar, okul bölgemizin o zamanlar "veri işleme" (data processing) dedikleri şey için kullandığı IBM 1401 üzerindeydi. Bu 9. sınıftaydı, yani 13 veya 14 yaşındaydım. Okul bölgesinin 1401'i tesadüfen ortaokulumuzun bodrumundaydı ve arkadaşım Rich Draves ile birlikte onu kullanmak için izin almıştık. Aşağısı küçük bir Bond kötüsünün sığınağı gibiydi; CPU, disk sürücüleri, yazıcı, kart okuyucu gibi tüm bu uzaylı görünümlü makineler, parlak floresan ışıklar altında yükseltilmiş bir zeminde duruyordu.


Kullandığımız dil, Fortran'ın erken bir sürümüydü. Programları delikli kartlara yazmanız, sonra onları kart okuyucuya istiflemeniz ve programı belleğe yükleyip çalıştırmak için bir düğmeye basmanız gerekiyordu. Sonuç normalde fevkalade gürültülü yazıcıda bir şeyler yazdırmak olurdu.


1401 kafamı karıştırmıştı. Onunla ne yapacağımı tam çözememiştim. Ve geriye dönüp baktığımda, onunla yapabileceğim pek bir şey de yoktu. Programlara tek girdi biçimi delikli kartlarda saklanan verilerdi ve bende delikli kartlarda saklanan hiç veri yoktu. Diğer tek seçenek, pi sayısının yaklaşımlarını hesaplamak gibi herhangi bir girdiye dayanmayan şeyler yapmaktı, ancak bu türden ilginç bir şey yapacak kadar matematik bilmiyordum. Bu yüzden yazdığım hiçbir programı hatırlamamam şaşırtıcı değil, çünkü pek bir şey yapmış olamazlar. En net hatırladığım an, programların sonlanmamasının mümkün olduğunu öğrendiğim andı; benimkilerden biri bitmek bilmemişti. Paylaşımlı zaman (time-sharing) olmayan bir makinede bu, veri merkezi yöneticisinin yüz ifadesinden de anlaşıldığı üzere, teknik olduğu kadar sosyal bir hataydı da.


Mikrobilgisayarlarla her şey değişti. Artık tam karşınızda, masanızın üstünde, bir deste delikli kartı işleyip durmak yerine, çalışırken tuş vuruşlarınıza yanıt verebilen bir bilgisayarınız olabilirdi. [1]


Mikrobilgisayar alan ilk arkadaşım onu kendi yapmıştı. Heathkit tarafından bir kit olarak satılıyordu. Bilgisayarın önünde oturup programları doğrudan bilgisayara yazdığını izlerken ne kadar etkilendiğimi ve kıskandığımı canlı bir şekilde hatırlıyorum.


O günlerde bilgisayarlar pahalıydı ve babamı bir tane (yaklaşık 1980'de bir TRS-80) almaya ikna etmem yıllarca dil dökmemi gerektirmişti. O zamanki altın standart Apple II idi, ancak bir TRS-80 yeterince iyiydi. Gerçekten programlamaya başladığım zaman buydu. Basit oyunlar, model roketlerimin ne kadar yükseğe uçacağını tahmin eden bir program ve babamın en az bir kitap yazmak için kullandığı bir kelime işlemci yazdım. Bellekte sadece yaklaşık 2 sayfalık metin için yer vardı, bu yüzden her seferinde 2 sayfa yazar ve sonra yazdırırdı ama bu bir daktilodan çok daha iyiydi.


Programlamayı sevsem de üniversitede okumayı planlamıyordum. Üniversitede, kulağa çok daha güçlü gelen felsefe okuyacaktım. Saf lise benliğim için felsefe, diğer alanlarda çalışılan şeylerin sadece alan bilgisi kalacağı mutlak gerçeklerin incelenmesi gibi görünüyordu. Üniversiteye gittiğimde keşfettiğim şey ise, diğer alanların fikir dünyasında o kadar çok yer kapladığıydı ki, bu sözde mutlak gerçekler için pek bir şey kalmamıştı. Felsefeye kalan tek şey, diğer alanlardaki insanların güvenle görmezden gelinebileceğini düşündüğü uç vakalardı.


18 yaşındaydım bunları kelimelere dökemezdim. O sırada tek bildiğim, felsefe dersleri almaya devam ettiğim ve bunların sıkıcı olmaya devam ettiğiydi. Ben de yapay zekaya (AI) geçmeye karar verdim.


1980'lerin ortalarında yapay zeka revaçtaydı ama üzerinde çalışmak istememe neden olan özellikle iki şey vardı: Heinlein'ın Mike adında zeki bir bilgisayarı konu alan "The Moon is a Harsh Mistress" (Ay Zalim Bir Sevgilidir) adlı romanı ve Terry Winograd'ın SHRDLU kullandığını gösteren bir PBS belgeseli. "The Moon is a Harsh Mistress"ı yeniden okumayı denemedim, bu yüzden ne kadar iyi eskidiğini bilmiyorum ama okuduğumda beni tamamen dünyasının içine çekmişti.
```

### Veri Ekleme

Ayrıca mevcut bir indekse veri ekleyebilirsiniz

```python
nodes = [node.node for node in response]
```

```python
del index


index = VectorStoreIndex.from_documents(
    [Document(text="Portland, Maine'de gökyüzü mor renktedir")],
    uri="/tmp/yeni_veri_kumesi",
)
```

```python
index.insert_nodes(nodes)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Gökyüzü nerede mor?")
print(textwrap.fill(str(response), 100))
```

**Portland, Maine**

Ayrıca mevcut bir tablodan da indeks oluşturabilirsiniz

```python
del index


vec_store = LanceDBVectorStore.from_table(vector_store._table)
index = VectorStoreIndex.from_vector_store(vec_store)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Yazar hangi şirketleri kurdu?")
print(textwrap.fill(str(response), 100))
```

**Yazar Viaweb ve Aspra şirketlerini kurdu.**
