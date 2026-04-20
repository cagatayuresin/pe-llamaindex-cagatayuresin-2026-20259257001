# Vertex AI Arama Erişicisi (Vertex AI Search Retriever)

---
title: Vertex AI Arama Erişicisi (Vertex AI Search Retriever)
 | LlamaIndex OSS Belgeleri
---

Bu not defteri, Vertex AI arama veri deposundan (datastore) veri getirebilen bir Erişicinin (Retriever) nasıl kurulacağını anlatır.

### Ön Koşullar (Pre-requirements)

- Bir Google Cloud projesi kurun
- Bir Vertex AI Search veri deposu kurun
- Vertex AI API'sini etkinleştirin

### Kütüphaneyi Yükle (Install library)

```bash
%pip install llama-index-retrievers-vertexai-search
```

### Mevcut Çalışma Zamanını Yeniden Başlat (Restart current runtime)

Yeni yüklenen paketleri bu Jupyter çalışma zamanında kullanmak için çalışma zamanını yeniden başlatmalısınız. Bunu, mevcut çekirdeği (kernel) yeniden başlatacak olan aşağıdaki hücreyi çalıştırarak yapabilirsiniz.

```python
# Yalnızca Colab için
# Ortamınızın yeni paketlere erişebilmesi için yüklemelerden sonra çekirdeği otomatik olarak yeniden başlatın
import IPython


app = IPython.Application.instance()
app.kernel.do_shutdown(True)
```

### Not Defteri Ortamınızı Doğrulayın (Authenticate your notebook environment - Sadece Colab)

Bu not defterini Google Colab üzerinde çalıştırıyorsanız, ortamınızı doğrulamanız gerekecektir. Bunun için aşağıdaki yeni hücreyi çalıştırın. [Vertex AI Workbench](https://cloud.google.com/vertex-ai-workbench) kullanıyorsanız bu adım gerekli değildir.

```python
# Yalnızca Colab için
import sys


if "google.colab" in sys.modules:
    from google.colab import auth


    auth.authenticate_user()
```

```python
# Eğer bir JupyterLab örneği (instance) kullanıyorsanız, aşağıdaki kodun yorumunu kaldırın ve çalıştırın.
#!gcloud auth login
```

```python
from llama_index.retrievers.vertexai_search import VertexAISearchRetriever


# Lütfen vertexai_search kısmında alt çizgi '_' kullanıldığına dikkat edin
```

### Google Cloud Proje Bilgilerini Ayarlayın ve Vertex AI SDK'sını Başlatın (Set Google Cloud project information and initialize Vertex AI SDK)

Vertex AI kullanmaya başlamak için mevcut bir Google Cloud projeniz olmalı ve [Vertex AI API'sini etkinleştirmelisiniz](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com).

[Bir proje ve geliştirme ortamı kurma](https://cloud.google.com/vertex-ai/docs/start/cloud-environment) hakkında daha fazla bilgi edinin.

```python
PROJECT_ID = "{proje kimliğiniz}"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
import vertexai


vertexai.init(project=PROJECT_ID, location=LOCATION)
```

### Yapılandırılmış Veri Deposunu Test Et (Test Structured datastore)

```python
DATA_STORE_ID = "{id'niz}"  # @param {type:"string"}
LOCATION_ID = "global"
```

```python
struct_retriever = VertexAISearchRetriever(
    project_id=PROJECT_ID,
    data_store_id=DATA_STORE_ID,
    location_id=LOCATION_ID,
    engine_data_type=1,
)
```

```python
query = "harry potter"
retrieved_results = struct_retriever.retrieve(query)
```

```python
print(retrieved_results[0])
```

### Yapılandırılmamış Veri Deposunu Test Et (Test Unstructured datastore)

```python
DATA_STORE_ID = "{id'niz}"
LOCATION_ID = "global"
```

```python
unstruct_retriever = VertexAISearchRetriever(
    project_id=PROJECT_ID,
    data_store_id=DATA_STORE_ID,
    location_id=LOCATION_ID,
    engine_data_type=0,
)
```

```python
query = "alphabet 2018 earning"
retrieved_results2 = unstruct_retriever.retrieve(query)
```

```python
print(retrieved_results2[0])
```

### Web Sitesi Veri Deposunu Test Et (Test Website datastore)

```python
DATA_STORE_ID = "{id'niz}"
LOCATION_ID = "global"
website_retriever = VertexAISearchRetriever(
    project_id=PROJECT_ID,
    data_store_id=DATA_STORE_ID,
    location_id=LOCATION_ID,
    engine_data_type=2,
)
```

```python
query = "diamaxol nedir"
retrieved_results3 = website_retriever.retrieve(query)
```

```python
print(retrieved_results3[0])
```

## Sorgu Motorunda Kullanım (Use in Query Engine)

```python
# gerekli modülleri içe aktar
from llama_index.core import Settings
from llama_index.llms.vertex import Vertex
from llama_index.embeddings.vertex import VertexTextEmbedding
```

```python
vertex_gemini = Vertex(
    model="gemini-1.5-pro",
    temperature=0,
    context_window=100000,
    additional_kwargs={},
)
# indeks/sorgu llm'ini kur
Settings.llm = vertex_gemini
```

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine.from_args(struct_retriever)
```

```python
response = query_engine.query("Bana Harry Potter'dan bahset")
print(str(response))
```
