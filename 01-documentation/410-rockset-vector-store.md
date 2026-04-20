---
title: Rockset Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Rockset Vektör Deposu (Vector Store)

Gerçek zamanlı arama ve analitik (analytics) veri tabanı olarak Rockset; ölçeklenebilir ve performanslı kişiselleştirme (personalization), ürün arama, anlamsal (semantic) arama, sohbet botu (chatbot) uygulamaları ve daha fazlasını sunmak için indekslemeyi (indexing) kullanır. Rockset gerçek zamanlı kullanım için özel olarak oluşturulduğundan, bu duyarlı (responsive) uygulamaları sürekli güncellenen ve akan (streaming) veriler üzerinde oluşturabilirsiniz. Rockset'i LlamaIndex ile entegre ederek, üretime hazır (production-ready) vektör arama uygulamaları için kendi gerçek zamanlı verileriniz üzerinde Yüksek Lisans Modellerini (LLM'ler) kolayca kullanabilirsiniz.

LlamaIndex'te Rockset'in bir vektör deposu olarak nasıl kullanılacağına dair bir tanıtımı adım adım inceleyeceğiz.

## Eğitim (Tutorial)

Bu örnekte, gömmeler (embeddings) oluşturmak için OpenAI'nin `text-embedding-ada-002` modelini ve gömmeleri depolamak için de vektör deposu olarak Rockset'i kullanacağız. Bir dosyadan metin alacak (ingest) ve içerik hakkında sorular soracağız.

### Ortamınızı Kurma

1. Kaynağınız olarak [Yazma API'si (Write API)](https://rockset.com/docs/write-api/) ile Rockset konsolundan bir [koleksiyon (collection)](https://rockset.com/docs/collections) oluşturun. Koleksiyonunuzun adını `llamaindex_demo` koyun. Gömme (embeddings) alanınızı tanımlamak ve ayrıca performans ve depolama optimizasyonlarından yararlanmak için, [`VECTOR_ENFORCE`](https://rockset.com/docs/vector-functions) ile aşağıdaki [veri alma dönüşümünü (ingest transformation)](https://rockset.com/docs/ingest-transformation) yapılandırın:

```sql
SELECT
    _input.* EXCEPT(_meta),
    VECTOR_ENFORCE(
        _input.embedding,
        1536,
        'float'
    ) as embedding
FROM _input
```

2. Rockset konsolundan bir [API anahtarı (API key)](https://rockset.com/docs/iam) yaratın ve `ROCKSET_API_KEY` ortam değişkenini (environment variable) ayarlayın. API sunucunuzu [burada](http://rockset.com/docs/rest-api#introduction) bulun ve `ROCKSET_API_SERVER` ortam değişkenini ayarlayın. `OPENAI_API_KEY` ortam değişkenini ayarlayın.

3. Bağımlılıkları (dependencies) kurun.

Terminal penceresi

```bash
pip3 install llama_index rockset
```

4. LlamaIndex, çeşitli kaynaklardan veri almanızı sağlar. Bu örnekte için, [burada](https://www.archives.gov/founding-docs/constitution-transcript) bulunan Amerikan Anayasasının (American Constitution) bir transkripti olan `constitution.txt` adlı metin dosyasından okuma yapacağız.

### Veri alımı (Data ingestion)

Metin dosyasını `Document` nesnelerinin bir listesine dönüştürmek için LlamaIndex'in `SimpleDirectoryReader` sınıfını kullanın.

```bash
%pip install llama-index-llms-openai
%pip install llama-index-vector-stores-rocksetdb
```

```python
from llama_index.core import SimpleDirectoryReader


docs = SimpleDirectoryReader(
    input_files=["{patika/yol (path)}/consitution.txt"]
).load_data()
```

LLM'yi ve hizmet bağlamını (service context) başlatın (instantiate).

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI


Settings.llm = OpenAI(temperature=0.8, model="gpt-3.5-turbo")
```

Vektör deposunu (vector store) ve depolama bağlamını (storage context) başlatın.

```python
from llama_index.core import StorageContext
from llama_index.vector_stores.rocksetdb import RocksetVectorStore


vector_store = RocksetVectorStore(collection="llamaindex_demo")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

`llamaindex_demo` koleksiyonuna belgeler ekleyin ve bir indeks oluşturun.

```python
from llama_index.core import VectorStoreIndex


index = VectorStoreIndex.from_documents(
    docs,
    storage_context=storage_context,
)
```

### Sorgulama (Querying)

Belgeniz hakkında bir soru sorun ve bir yanıt oluşturun.

```python
response = index.as_query_engine().query("Başkanın görevi nedir?")


print(str(response))
```

Programı çalıştırın.

```bash
$ python3 main.py
Başkanın görevi Amerika Birleşik Devletleri Başkanlık Makamını (Office of President) sadakatle yürütmek, Amerika Birleşik Devletleri Anayasasını (Constitution of the United States) muhafaza etmek, korumak ve savunmak, Kara ve Deniz Kuvvetlerinin Başkomutanı (Commander in Chief) olarak hizmet etmek, Amerika Birleşik Devletleri'ne karşı işlenen suçlar için cezaları ertelemek ve aflar (pardons) vermek (görevden alma/suçlama (impeachment) durumları hariç), antlaşmalar (treaties) yapmak, büyükelçileri (ambassadors) ve diğer kamu bakanlarını (public ministers) atamak (appoint), yasaların sadakatle yürütülmesine özen göstermek ve Amerika Birleşik Devletleri'nin tüm memurlarını görevlendirmektir.
```

## Meta Veri Filtreleme (Metadata Filtering)

Meta veri filtreleme (Metadata filtering), belirli filtrelere uyan daha isabetli (relevant) belgeleri döküme almanıza / geri getirmenize olanak tanır.

1. Vektör deponuza düğümler (nodes) ekleyin ve bir indeks oluşturun.

```python
from llama_index.vector_stores.rocksetdb import RocksetVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.vector_stores.types import NodeWithEmbedding
from llama_index.core.schema import TextNode


nodes = [
    NodeWithEmbedding(
        node=TextNode(
            text="Elmalar mavidir",
            metadata={"type": "fruit"},
        ),
        embedding=[],
    )
]
index = VectorStoreIndex(
    nodes,
    storage_context=StorageContext.from_defaults(
        vector_store=RocksetVectorStore(collection="llamaindex_demo")
    ),
)
```

2. Meta veri filtrelerini tanımlayın.

```python
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters


filters = MetadataFilters(
    filters=[ExactMatchFilter(key="type", value="fruit")]
)
```

3. Filtreleri karşılayan alakalı (relevant) belgeleri kullanıma (retrieve) alın.

```python
retriever = index.as_retriever(filters=filters)
retriever.retrieve("Elmalar ne renktir?")
```

## Mevcut Bir Koleksiyondan İndeks Oluşturma

Mevcut koleksiyonlardan alınan verilerle indeksler oluşturabilirsiniz.

```python
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.rocksetdb import RocksetVectorStore


vector_store = RocksetVectorStore(collection="llamaindex_demo")


index = VectorStoreIndex.from_vector_store(vector_store)
```

## Yeni Bir Koleksiyondan İndeks Oluşturma

Vektör deposu olarak kullanmak için yeni bir Rockset koleksiyonu da oluşturabilirsiniz.

```python
from llama_index.vector_stores.rocksetdb import RocksetVectorStore


vector_store = RocksetVectorStore.with_new_collection(
    collection="llamaindex_demo",  # yeni koleksiyonun adı
    dimensions=1536,  # veri alma dönüştürme işleminde (ingest tranformation) vektörlerin uzunluğunu belirtir (isteğe bağlı)
    # diğer RocksetVectorStore argümanları (args)
)


index = VectorStoreIndex(
    nodes,
    storage_context=StorageContext.from_defaults(vector_store=vector_store),
)
```

## Yapılandırma (Configuration)

- **collection**: Sorgulanacak koleksiyonun adı (gerekli/zorunlu).

```python
RocksetVectorStore(collection="my_collection")
```

- **workspace**: Koleksiyonu içeren çalışma alanının (workspace) adı. Varsayılanı `"commons"`tır.

```python
RocksetVectorStore(worksapce="my_workspace")
```

- **api\_key**: Rockset isteklerinin (requests) kimliğini doğrulamak için kullanılacak API anahtarı. Eğer `client` değerden (passed in) girilirse bu yoksayılır (ignored). Varsayılan olarak `ROCKSET_API_KEY` ortam değişkenini esas alır.

```python
RocksetVectorStore(api_key="<benim anahtarim>")
```

- **api\_server**: Rockset taleplerini ve isteklerini iletmek adına (çalıştırmak için) kullanılacak API ortam sunucusu. Eğer `client` değerden (passed in) girilirse bu adım da göz ardı edilir (yoksayılır). Standart ayarlar bağlamında (default) ortam değişkeni `ROCKSET_API_KEY` dikkate alınır, ya da şayet bir `ROCKSET_API_SERVER` ayarlanmamışsa `"https://api.use1a1.rockset.com"` değerine ulaşır (geçer).

```python
from rockset import Regions
RocksetVectorStore(api_server=Regions.euc1a1)
```

- **client**: Rockset isteklerini/komutlarını yerine getirmek eylemi (execute) amacıyla tasarruf edilecek Rockset istemcisi (client) nesnesi. Herhangi bir belirleme (specification) olmadığı/yapılmadığı durumda sistem arka planı; iç/dahili bir eklenti vasıtasıyla `api_key` parametresiyle (yahut da `ROCKSET_API_SERVER` ortam (environment) değişkeni ile) bir nesne tesis eder. Ayrıca `api_server` parametresi de (veya yine `ROCKSET_API_SERVER` ortam değişkeni) yapı sürecinde yer bulur.

```python
from rockset import RocksetClient
RocksetVectorStore(client=RocksetClient(api_key="<benim anahtarim>"))
```

- **embedding\_col**: Yüklemelerin / Gömmelerin olduğu veri tabanı alanının (database field) ismi. Varsayılan olarak `"embedding"` şeklinde değerlendirilir.

```python
RocksetVectorStore(embedding_col="my_embedding")
```

- **metadata\_col**: Düğüm (node) özelliklerinin veya verilerinin barındığı altındaki veritabanı platformu (alan). Normal tanımı `"metadata"` şeklindedir.

```python
RocksetVectorStore(metadata_col="node")
```

- **distance\_func**: İkili ya da çoklu vektör korelasyonunu (ilişkisi/bağlantısı) hesaplama metriği. Varsayılan hesap mekanizması (metriği) cosine similarity (kosinüs benzerliği / yatkınlığı) üzerindendir.

```python
RocksetVectorStore(distance_func=RocksetVectorStore.DistanceFunc.DOT_PRODUCT)
```
