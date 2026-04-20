---
title: Asenkron (Async) API ile Milvus Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Asenkron (Async) API ile Milvus Vektör Deposu

Bu eğitim, RAG için asenkron belge işleme boru hattı (pipeline) oluşturmak amacıyla [LlamaIndex](https://www.llamaindex.ai/)'in [Milvus](https://milvus.io/) ile nasıl kullanılacağını göstermektedir. LlamaIndex, belgeleri işlemek ve Milvus gibi vektör veritabanlarında saklamak için bir yol sağlar. LlamaIndex ve Milvus Python istemci kütüphanesinin asenkron API'lerinden yararlanarak, büyük hacimli verileri verimli bir şekilde işlemek ve indekslemek için boru hattının verimini (throughput) artırabiliriz.

Bu eğitimde, önce LlamaIndex ve Milvus ile asenkron yöntemleri kullanarak yüksek düzeyde (high-level) bir RAG oluşturmayı, ardından düşük düzeyli (low-level) yöntemlerin kullanımını ve senkron ile asenkron işlemlerin performans karşılaştırmasını tanıtacağız.

## Başlamadan Önce

Bu sayfadaki kod parçacıkları `pymilvus` ve `llamaindex` bağımlılıklarını gerektirir. Bunları aşağıdaki komutları kullanarak kurabilirsiniz:

```bash
! pip install -U pymilvus llama-index-vector-stores-milvus llama-index nest-asyncio
```

> Google Colab kullanıyorsanız, yeni kurulan bağımlılıkları etkinleştirmek için **çalışma zamanını yeniden başlatmanız** gerekebilir (ekranın üst kısmındaki "Runtime" menüsüne tıklayın ve açılır menüden "Restart session" seçeneğini seçin).

OpenAI modellerini kullanacağız. `OPENAI_API_KEY` [api anahtarını](https://platform.openai.com/docs/quickstart) bir ortam değişkeni olarak hazırlamalısınız.

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-***********"
```

Jupyter Notebook kullanıyorsanız, asenkron kodu çalıştırmadan önce bu kod satırını çalıştırmanız gerekir.

```python
import nest_asyncio


nest_asyncio.apply()
```

### Verileri Hazırlayın

Örnek verileri aşağıdaki komutlarla indirebilirsiniz:

```bash
! mkdir -p 'data/'
! wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham_essay.txt'
! wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf' -O 'data/uber_2021.pdf'
```

## Asenkron İşleme ile RAG Oluşturma

Bu bölüm, belgeleri asenkron bir şekilde işleyebilen bir RAG sisteminin nasıl oluşturulacağını gösterir.

Gerekli kütüphaneleri içe aktarın ve Milvus URI'sini ve gömme (embedding) boyutunu tanımlayın.

```python
import asyncio
import random
import time


from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.vector_stores.milvus import MilvusVectorStore


URI = "http://localhost:19530"
DIM = 768
```

> - Büyük ölçekli verileriniz varsa, [docker veya kubernetes](https://milvus.io/docs/quickstart.md) üzerinde performanslı bir Milvus sunucusu kurabilirsiniz. Bu kurulumda, lütfen sunucu uri'sini (örneğin `http://localhost:19530`) `uri` olarak kullanın.
> - Milvus için tamamen yönetilen bulut hizmeti olan [Zilliz Cloud](https://zilliz.com/cloud)'u kullanmak istiyorsanız, Zilliz Cloud'daki [Public Endpoint ve Api key](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details) bilgilerine karşılık gelen `uri` ve `token` bilgilerini ayarlayın.
> - Karmaşık sistemlerde (ağ iletişimi gibi), asenkron işleme senkronizasyona kıyasla performans iyileştirmesi getirebilir. Bu nedenle Milvus-Lite'ın asenkron arayüzler kullanmak için pek uygun olmadığını düşünüyoruz çünkü kullanım senaryoları buna uygun değildir.

Milvus koleksiyonunu yeniden oluşturmak için tekrar kullanabileceğimiz bir başlatma işlevi tanımlayın.

```python
def init_vector_store():
    return MilvusVectorStore(
        uri=URI,
        # token=TOKEN,
        dim=DIM,
        collection_name="test_collection",
        embedding_field="embedding",
        id_field="id",
        similarity_metric="COSINE",
        consistency_level="Strong",
        overwrite=True,  # Koleksiyon zaten varsa üzerine yazmak için
    )




vector_store = init_vector_store()
```

`paul_graham_essay.txt` dosyasından bir LlamaIndex belge nesnesi sarmalamak için `SimpleDirectoryReader` kullanın.

```python
from llama_index.core import SimpleDirectoryReader


# belgeleri yükle
documents = SimpleDirectoryReader(
    input_files=["./data/paul_graham_essay.txt"]
).load_data()


print("Belge Kimliği:", documents[0].doc_id)
```

Yerel olarak bir Hugging Face gömme (embedding) modeli örneği oluşturun. Yerel bir model kullanmak, asenkron veri ekleme sırasında API hız sınırlarına (rate limits) ulaşma riskini önler; çünkü eşzamanlı API istekleri hızla birikebilir ve genel API'deki bütçenizi tüketebilir. Ancak, yüksek bir hız sınırınız varsa, bunun yerine uzak bir model servisi kullanmayı tercih edebilirsiniz.

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding




embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
```

Bir indeks oluşturun ve belgeyi ekleyin.

Asenkron ekleme modunu etkinleştirmek için `use_async` parametresini `True` olarak ayarlıyoruz.

```python
# Belgeler üzerinde bir indeks oluşturun
from llama_index.core import VectorStoreIndex, StorageContext


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    use_async=True,
)
```

LLM'yi başlatın.

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo")
```

Sorgu motorunu oluştururken, asenkron aramayı etkinleştirmek için `use_async` parametresini `True` olarak da ayarlayabilirsiniz.

```python
query_engine = index.as_query_engine(use_async=True, llm=llm)
response = await query_engine.aquery("Yazar ne öğrendi?")
```

```python
print(response)
```

**"Yazar, o dönemde uygulandığı şekliyle yapay zeka alanının başlangıçta inanıldığı kadar umut verici olmadığını öğrendi. YZ'de kavramları temsil etmek için açık veri yapılarını kullanma yaklaşımı, doğal dilin gerçek anlamda anlaşılmasını sağlamada etkili değildi. Bu farkındalık, yazarı odağını Lisp'e ve sonunda sanat alanını keşfetmeye kaydırmaya yöneltti."**

## Asenkron API'yi Keşfedin

Bu bölümde, daha düşük düzeyli (low level) API kullanımını tanıtacağız ve senkron ile asenkron çalışmaların performansını karşılaştıracağız.

### Asenkron ekleme (Async add)

Vektör deposunu yeniden başlatın.

```python
vector_store = init_vector_store()
```

İndeks için çok sayıda test düğümü (node) oluşturmak üzere kullanılacak bir düğüm üretme işlevi tanımlayalım.

```python
def random_id():
    random_num_str = ""
    for _ in range(16):
        random_digit = str(random.randint(0, 9))
        random_num_str += random_digit
    return random_num_str




def produce_nodes(num_adding):
    node_list = []
    for i in range(num_adding):
        node = TextNode(
            id_=random_id(),
            text=f"n{i}_metin",
            embedding=[0.5] * (DIM - 1) + [random.random()],
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id=f"n{i+1}")
            },
        )
        node_list.append(node)
    return node_list
```

Vektör deposuna belge eklemek için asenkron bir işlev tanımlayın. Milvus vektör deposu örneğindeki `async_add()` işlevini kullanıyoruz.

```python
async def async_add(num_adding):
    node_list = produce_nodes(num_adding)
    start_time = time.time()
    tasks = []
    for i in range(num_adding):
        sub_nodes = node_list[i]
        task = vector_store.async_add([sub_nodes])  # async_add() kullan
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    return end_time - start_time
```

```python
add_counts = [10, 100, 1000]
```

Olay döngüsünü (event loop) alın.

```python
loop = asyncio.get_event_loop()
```

Belgeleri vektör deposuna asenkron olarak ekleyin.

```python
for count in add_counts:


    async def measure_async_add():
        async_time = await async_add(count)
        print(f"{count} öğe için asenkron ekleme {async_time:.2f} saniye sürdü")
        return async_time


    loop.run_until_complete(measure_async_add())
```

```text
10 öğe için asenkron ekleme 0.19 saniye sürdü
100 öğe için asenkron ekleme 0.48 saniye sürdü
1000 öğe için asenkron ekleme 3.22 saniye sürdü
```

```python
vector_store = init_vector_store()
```

#### Senkron ekleme ile karşılaştırın

Senkron bir ekleme işlevi tanımlayın. Ardından aynı koşul altında çalışma süresini ölçün.

```python
def sync_add(num_adding):
    node_list = produce_nodes(num_adding)
    start_time = time.time()
    for node in node_list:
        result = vector_store.add([node])
    end_time = time.time()
    return end_time - start_time
```

```python
for count in add_counts:
    sync_time = sync_add(count)
    print(f"{count} öğe için senkron ekleme {sync_time:.2f} saniye sürdü")
```

```text
10 öğe için senkron ekleme 0.56 saniye sürdü
100 öğe için senkron ekleme 5.85 saniye sürdü
1000 öğe için senkron ekleme 62.91 saniye sürdü
```

Sonuç, senkron ekleme işleminin asenkron olandan çok daha yavaş olduğunu göstermektedir.

### Asenkron arama (Async search)

Vektör deposunu yeniden başlatın ve aramayı çalıştırmadan önce bazı belgeler ekleyin.

```python
vector_store = init_vector_store()
node_list = produce_nodes(num_adding=1000)
inserted_ids = vector_store.add(node_list)
```

Asenkron bir arama işlevi tanımlayın. Milvus vektör deposu örneğindeki `aquery()` işlevini kullanıyoruz.

```python
async def async_search(num_queries):
    start_time = time.time()
    tasks = []
    for _ in range(num_queries):
        query = VectorStoreQuery(
            query_embedding=[0.5] * (DIM - 1) + [0.6], similarity_top_k=3
        )
        task = vector_store.aquery(query=query)  # aquery() kullan
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    return end_time - start_time
```

```python
query_counts = [10, 100, 1000]
```

Milvus deposundan asenkron olarak arama yapın.

```python
for count in query_counts:


    async def measure_async_search():
        async_time = await async_search(count)
        print(
            f"{count} sorgu için asenkron arama {async_time:.2f} saniye sürdü"
        )
        return async_time


    loop.run_until_complete(measure_async_search())
```

```text
10 sorgu için asenkron arama 0.55 saniye sürdü
100 sorgu için asenkron arama 1.39 saniye sürdü
1000 sorgu için asenkron arama 8.81 saniye sürdü
```

#### Senkron arama ile karşılaştırın

Senkron bir arama işlevi tanımlayın. Ardından aynı koşul altında çalışma süresini ölçün.

```python
def sync_search(num_queries):
    start_time = time.time()
    for _ in range(num_queries):
        query = VectorStoreQuery(
            query_embedding=[0.5] * (DIM - 1) + [0.6], similarity_top_k=3
        )
        result = vector_store.query(query=query)
    end_time = time.time()
    return end_time - start_time
```

```python
for count in query_counts:
    sync_time = sync_search(count)
    print(f"{count} sorgu için senkron arama {sync_time:.2f} saniye sürdü")
```

```text
10 sorgu için senkron arama 3.29 saniye sürdü
100 sorgu için senkron arama 30.80 saniye sürdü
1000 sorgu için senkron arama 308.80 saniye sürdü
```

Sonuç, senkron arama işleminin asenkron olandan çok daha yavaş olduğunu göstermektedir.
