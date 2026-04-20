# LlamaCloudIndex + LlamaCloudRetriever

LlamaCloud; LLM ve RAG uygulamalarınıza üretim kalitesinde (production-grade) bağlam zenginleştirme getirmek için tasarlanmış, yönetilen yeni nesil ayrıştırma (parsing), veri alma (ingestion) ve getirme (retrieval) hizmetidir.

Şu anda LlamaCloud şunları desteklemektedir:

-   **Yönetilen Veri Alma (Managed Ingestion) API'si**: Ayrıştırma ve döküman yönetimini üstlenir.
-   **Yönetilen Getirme (Managed Retrieval) API'si**: RAG sisteminiz için en uygun getirme işlemini yapılandırır.

LlamaCloud ve özellikle bu entegrasyon hakkında ek dökümantasyon için lütfen [resmi LlamaCloud dökümanlarımıza](https://docs.cloud.llamaindex.ai/llamacloud/guides/framework_integration) bakın.

## Erişim

Yönetilen veri alma ve getirme API'si için sınırlı sayıda kurumsal ortağımıza özel bir beta süreci açıyoruz. Veri boru hatlarınızı merkezileştirmek ve asıl RAG kullanım durumlarınız üzerinde daha fazla zaman geçirmekle ilgileniyorsanız, bizimle [iletişime geçin.](https://www.llamaindex.ai/contact)

LlamaCloud'a erişiminiz varsa, oturum açmak ve bir API anahtarı almak için [LlamaCloud](https://cloud.llamaindex.ai) adresini ziyaret edebilirsiniz.

## Kurulum

Öncelikle en son LlamaIndex sürümünün yüklü olduğundan emin olun.

```bash
pip uninstall llama-index  # v0.9.x veya daha eski bir sürümden yükseltme yapıyorsanız bunu çalıştırın
pip install -U llama-index --upgrade --no-cache-dir --force-reinstall
```

`llama-cloud-services` paketi yukarıdaki yükleme ile birlikte gelir, ancak doğrudan da yükleyebilirsiniz:

```bash
pip install -U llama-cloud-services
```

## Kullanım

Aşağıdaki kodu kullanarak LlamaCloud üzerinde bir indeks oluşturabilirsiniz:

```python
import os

os.environ[
    "LLAMA_CLOUD_API_KEY"
] = "llx-..."  # API anahtarını ortam değişkeninde (env) veya daha sonra yapılandırıcıda (constructor) sağlayabilirsiniz

from llama_index.core import SimpleDirectoryReader
from llama_cloud_services import LlamaCloudIndex

# yeni bir indeks oluştur
index = LlamaCloudIndex.from_documents(
    documents,
    "ilk_indeksim",
    project_name="default",
    api_key="llx-...",
    verbose=True,
)

# mevcut bir indekse bağlan
index = LlamaCloudIndex("ilk_indeksim", project_name="default")
```

Ayrıca yönetilen getirme için bir getirici (retriever) yapılandırabilirsiniz:

```python
# mevcut indeksten
index.as_retriever()

# sıfırdan
from llama_cloud_services import LlamaCloudRetriever

retriever = LlamaCloudRetriever("ilk_indeksim", project_name="default")
```

Ve tabii ki, yeni yönetilen indeksinizden yararlanmak için diğer indeks kısayollarını kullanabilirsiniz:

```python
query_engine = index.as_query_engine(llm=llm)

chat_engine = index.as_chat_engine(llm=llm)
```

## Getirici Ayarları (Retriever Settings)

Getirici ayarlarının / anahtar kelime argümanlarının (kwargs) tam listesi aşağıdadır:

-   `dense_similarity_top_k`: Optional[int] -- 0'dan büyükse, yoğun getirme (dense retrieval) kullanarak `k` adet node getirir.
-   `sparse_similarity_top_k`: Optional[int] -- 0'dan büyükse, seyrek getirme (sparse retrieval) kullanarak `k` adet node getirir.
-   `enable_reranking`: Optional[bool] -- Yeniden sıralamanın (reranking) etkinleştirilip etkinleştirilmeyeceği. Doğruluk için bir miktar hızdan feragat eder.
-   `rerank_top_n`: Optional[int] -- İlk getirme sonuçlarını yeniden sıraladıktan sonra döndürülecek node sayısı.
-   `alpha` Optional[float] -- Yoğun ve seyrek getirme arasındaki ağırlıklandırma. 1 = Tam yoğun getirme, 0 = Tam seyrek getirme.

## Bileşik Getirme (Composite Retrieval) Kullanımı

Çeşitli veri türlerini alan birden fazla indeks kurduğunuzda, tüm indekslerinizdeki veriler üzerinden sorgulama yapabilen bir uygulama oluşturmak isteyebilirsiniz.

Burası `LlamaCloudCompositeRetriever` sınıfını kullanabileceğiniz yerdir. Aşağıdaki kod parçası bileşik getiricinin nasıl kurulacağını gösterir:

```python
import os
from llama_cloud import CompositeRetrievalMode, RetrieverPipeline
from llama_cloud_services import (
    LlamaCloudIndex,
    LlamaCloudCompositeRetriever,
)

llama_cloud_api_key = os.environ["LLAMA_CLOUD_API_KEY"]
project_name = "Denemeler"

# İndekslerinizi kurun
pg_documents = SimpleDirectoryReader("./examples/data/paul_graham").load_data()
pg_index = LlamaCloudIndex.from_documents(
    documents=pg_documents,
    name="PG Indeksi",
    project_name=project_name,
    api_key=llama_cloud_api_key,
)

sama_documents = SimpleDirectoryReader(
    "./examples/data/sam_altman"
).load_data()
sama_index = LlamaCloudIndex.from_documents(
    documents=sama_documents,
    name="Sam Indeksi",
    project_name=project_name,
    api_key=llama_cloud_api_key,
)

retriever = LlamaCloudCompositeRetriever(
    name="Denemeler Getiricisi",
    project_name=project_name,
    api_key=llama_cloud_api_key,
    # "Denemeler Getiricisi" adında bir Getirici zaten yoksa bir tane oluşturulur
    create_if_not_exists=True,
    # CompositeRetrievalMode.FULL modu, her indeksi ayrı ayrı sorgular ve sonunda sonuçları küresel olarak yeniden sıralar
    mode=CompositeRetrievalMode.FULL,
    rerank_top_n=5,
)

# Yukarıdaki indeksleri bileşik getiriciye ekleyin
# CompositeRetrievalMode.ROUTING kullanıldığında bir sorguyu bağlı bir alt indekse yönlendirmek için dahili olarak
# kullanıldığından, açıklamayı (description) dikkatlice oluşturun
retriever.add_index(pg_index, description="Paul Graham denemelerinden oluşan bir koleksiyon")
retriever.add_index(
    sama_index, description="Sam Altman denemelerinden oluşan bir koleksiyon"
)

# Sorgularınız için bağlam getirmeye başlayın
# asenkron .aretrieve() de mevcuttur
nodes = retriever.retrieve("YC ne yapar?")
```

### Bileşik Getirme ile İlgili Parametreler

Bileşik getirme parametrelerini ayarlamaya özgü birkaç parametre vardır:

-   `mode`: `Optional[CompositeRetrievalMode]` -- `CompositeRetrievalMode.FULL` veya `CompositeRetrievalMode.ROUTING` olabilir.
    -   `full`: Bu modda, bağlı tüm alt indeksler sorgulanır ve bu alt indekslerden alınan tüm node'lar arasında yeniden sıralama gerçekleştirilir.
    -   `routing`: Bu modda, bir ajan sağlanan sorgu için hangi alt indekslerin en ilgili olduğunu belirler (sağladığınız alt indeksin `name` ve `description` alanlarına dayanarak) ve yalnızca ilgili olduğu düşünülen indeksleri sorgular. Yalnızca seçilen bu indeks kümesinden gelen node'lar, getirme yanıtında döndürülmeden önce yeniden sıralanır.
-   `rerank_top_n`: `Optional[int]` -- Tüm indekslerden getirilen node'lar arasında yeniden sıralama yapıldıktan sonra kaç adet node döndürüleceğini belirler.