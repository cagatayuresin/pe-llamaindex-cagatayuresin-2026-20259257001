# Saklama (Storing)

## Kavram

LlamaIndex; harici verilerinizi almak, indekslemek ve sorgulamak için üst düzey bir arayüz sağlar.

Arka planda LlamaIndex, aşağıdakileri özelleştirmenize olanak tanıyan değiştirilebilir (swappable) **saklama bileşenlerini** (storage components) de destekler:

-   **Döküman depoları (Document stores)**: Alınan dökümanların (yani `Node` nesnelerinin) saklandığı yer.
-   **İndeks depoları (Index stores)**: İndeks meta verilerinin saklandığı yer.
-   **Vektör depoları (Vector stores)**: Embedding vektörlerinin saklandığı yer.
-   **Özellik Grafiği (Property Graph) depoları**: Bilgi grafiklerinin saklandığı yer (örneğin `PropertyGraphIndex` için).
-   **Sohbet depoları (Chat Stores)**: Sohbet mesajlarının saklandığı ve düzenlendiği yer.

Döküman/İndeks depoları, aşağıda detaylandırılan ortak bir Anahtar-Değer (Key-Value) deposu soyutlamasına dayanır.

LlamaIndex, verilerin [fsspec](https://filesystem-spec.readthedocs.io/en/latest/index.html) tarafından desteklenen herhangi bir saklama arka ucuna (storage backend) kalıcı olarak kaydedilmesini destekler.
Aşağıdaki saklama arka uçları için desteği onayladık:

-   Yerel dosya sistemi
-   AWS S3
-   Cloudflare R2

![](./../../_static/storage/storage.png)

## Kullanım Kalıbı (Usage Pattern)

Birçok vektör deposu (FAISS hariç), hem verileri hem de indeksi (embedding'leri) saklayacaktır. Bu, ayrı bir döküman deposu veya indeks deposu kullanmanıza gerek kalmayacağı anlamına gelir. Bu _ayrıca_, bu verileri açıkça kalıcı hale getirmenize gerek kalmayacağı -bunun otomatik olarak gerçekleşeceği- anlamına da gelir. Yeni bir indeks oluşturmak veya mevcut olanı yeniden yüklemek için kullanım aşağıdaki gibi görünecektir:

```python
## yeni bir indeks oluştur
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.deeplake import DeepLakeVectorStore

# vektör deposunu oluştur ve saklama bağlamını (storage context) özelleştir
vector_store = DeepLakeVectorStore(dataset_path="<dataset_yolu>")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Dökümanları yükle ve indeksi oluştur
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)


## mevcut olanı yeniden yükle
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
```

Daha fazla detay için aşağıdaki [Vektör Deposu Modül Kılavuzumuza](/python/framework/module_guides/storing/vector_stores) bakın.

Genel olarak saklama soyutlamalarını kullanmak için bir `StorageContext` nesnesi tanımlamanız gerektiğini unutmayın:

```python
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import StorageContext

# varsayılan depoları kullanarak saklama bağlamı oluştur
storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore(),
    vector_store=SimpleVectorStore(),
    index_store=SimpleIndexStore(),
)
```

Özelleştirme/kalıcılık (persistence) hakkında daha fazla detay aşağıdaki kılavuzlarda bulunabilir:

-   [Özelleştirme (Customization)](/python/framework/module_guides/storing/customization)
-   [Kaydetme/Yükleme (Save/Load)](/python/framework/module_guides/storing/save_load)

## Modüller

Farklı saklama bileşenleri üzerine derinlemesine kılavuzlar sunuyoruz:

-   [Vektör Depoları (Vector Stores)](/python/framework/module_guides/storing/vector_stores)
-   [Döküman Depoları (Docstores)](/python/framework/module_guides/storing/docstores)
-   [İndeks Depoları (Index Stores)](/python/framework/module_guides/storing/index_stores)
-   [Anahtar-Değer Depoları (Key-Val Stores)](/python/framework/module_guides/storing/kv_stores)
-   [Özellik Grafiği Depoları (Property Graph Stores)](/python/framework/module_guides/indexing/lpg_index_guide#storage)
-   [Sohbet Depoları (ChatStores)](/python/framework/module_guides/storing/chat_stores)