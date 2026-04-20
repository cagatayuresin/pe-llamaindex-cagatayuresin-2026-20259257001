# IBM watsonx.ai

> WatsonxEmbeddings, IBM [watsonx.ai](https://www.ibm.com/products/watsonx-ai) embedding modelleri için bir sarmalayıcıdır (wrapper).

Bu örnek, `LlamaIndex` Embeddings API'sini kullanarak `watsonx.ai` embedding modelleriyle nasıl iletişim kurulacağını gösterir.

## Kurulum

`llama-index-embeddings-ibm` paketini kurun:

```python
!pip install -qU llama-index-embeddings-ibm
```

Aşağıdaki hücre, watsonx Embedding'leri ile çalışmak için gerekli kimlik bilgilerini tanımlar.

**Eylem:** IBM Cloud kullanıcı API anahtarını sağlayın. Ayrıntılar için bkz:
[Kullanıcı API anahtarlarını yönetme](https://cloud.ibm.com/docs/account?topic=account-userapikey&interface=ui).

```python
import os
from getpass import getpass

watsonx_api_key = getpass()
os.environ["WATSONX_APIKEY"] = watsonx_api_key
```

Ek olarak, diğer gizli bilgileri bir ortam değişkeni olarak geçirebilirsiniz:

```python
import os

os.environ["WATSONX_URL"] = "hizmet örneği url'niz"
os.environ["WATSONX_TOKEN"] = "CPD kümesine erişim için belirteciniz"
os.environ["WATSONX_PASSWORD"] = "CPD kümesine erişim için parolanız"
os.environ["WATSONX_USERNAME"] = "CPD kümesine erişim için kullanıcı adınız"
os.environ[
    "WATSONX_INSTANCE_ID"
] = "CPD kümesine erişim için instance_id değeriniz"
```

## Modeli Yükleme

Farklı görevler için embedding parametrelerini ayarlamanız gerekebilir:

```python
truncate_input_tokens = 3
```

`WatsonxEmbeddings` sınıfını önceden ayarlanan parametre ile başlatın.

**Not**: 

- API çağrısı için bağlam sağlamak amacıyla `project_id` veya `space_id` geçirmelisiniz. Proje veya alan (space) kimliğinizi almak için projenizi veya alanınızı açın, **Manage** sekmesine gidin ve **General**'e tıklayın. Daha fazla bilgi için bkz: [Proje dökümantasyonu](https://www.ibm.com/docs/en/watsonx-as-a-service?topic=projects) veya [Dağıtım alanı dökümantasyonu](https://www.ibm.com/docs/en/watsonx/saas?topic=spaces-creating-deployment).
- Sağlanan hizmet örneğinizin bölgesine bağlı olarak, [watsonx.ai API Kimlik Doğrulaması](https://ibm.github.io/watsonx-ai-python-sdk/setup_cloud.html#authentication) sayfasında listelenen URL'lerden birini kullanın.

Bu örnekte `project_id` ve Dallas URL'sini kullanacağız.

Çıkarım (inference) için kullanılacak `model_id` değerini belirtmeniz gerekir. Mevcut tüm modellerin listesini [Desteklenen temel modeller](https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html#ibm_watsonx_ai.foundation_models.utils.enums.ModelTypes) sayfasında bulabilirsiniz.

```python
from llama_index.embeddings.ibm import WatsonxEmbeddings

watsonx_embedding = WatsonxEmbeddings(
    model_id="ibm/slate-125m-english-rtrvr",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="PROJE_ID_NİZİ BURAYA YAPIŞTIRIN",
    truncate_input_tokens=truncate_input_tokens,
)
```

Alternatif olarak, Cloud Pak for Data kimlik bilgilerini de kullanabilirsiniz. Ayrıntılar için bkz: [watsonx.ai yazılım kurulumu](https://ibm.github.io/watsonx-ai-python-sdk/setup_cpd.html).

```python
watsonx_embedding = WatsonxEmbeddings(
    model_id="ibm/slate-125m-english-rtrvr",
    url="URL'NİZİ BURAYA YAPIŞTIRIN",
    username="KULLANICI ADINIZI BURAYA YAPIŞTIRIN",
    password="PAROLANIZI BURAYA YAPIŞTIRIN",
    instance_id="openshift",
    version="4.8",
    project_id="PROJE_ID_NİZİ BURAYA YAPIŞTIRIN",
    truncate_input_tokens=truncate_input_tokens,
)
```

## Kullanım

### Sorgu Embedding'i Oluşturma

```python
query = "Örnek sorgu."

query_result = watsonx_embedding.get_query_embedding(query)
print(query_result[:5])
```

    [-0.05538924, 0.05161056, 0.01207759, 0.0017501727, -0.017691258]

### Metin Listesi için Embedding Oluşturma

```python
texts = ["Bu bir belgenin içeriğidir", "Bu başka bir belgedir"]

doc_result = watsonx_embedding.get_text_embedding_batch(texts)
print(doc_result[0][:5])
```

    [0.009447167, -0.024981938, -0.02601326, -0.04048393, -0.05780444]