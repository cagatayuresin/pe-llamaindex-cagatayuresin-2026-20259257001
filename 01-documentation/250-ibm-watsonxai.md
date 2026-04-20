# IBM watsonx.ai

> WatsonxLLM, IBM [watsonx.ai](https://www.ibm.com/products/watsonx-ai) temel modelleri (foundation models) için bir sarmalayıcıdır.

Bu örneklerin amacı, `LlamaIndex` LLM API'sini kullanarak `watsonx.ai` modelleriyle nasıl iletişim kurulacağını göstermektir.

## Kurulum

`llama-index-llms-ibm` paketini kurun:

```python
!pip install -qU llama-index-llms-ibm
```

Aşağıdaki hücre, watsonx Temel Model çıkarımı ile çalışmak için gerekli kimlik bilgilerini (credentials) tanımlar.

**Eylem:** IBM Cloud kullanıcı API anahtarını sağlayın. Detaylar için [Kullanıcı API anahtarlarını yönetme](https://cloud.ibm.com/docs/account?topic=account-userapikey&interface=ui) bölümüne bakın.

```python
import os
from getpass import getpass

watsonx_api_key = getpass()
os.environ["WATSONX_APIKEY"] = watsonx_api_key
```

Ek olarak, diğer gizli bilgileri bir ortam değişkeni olarak iletebilirsiniz:

```python
import os

os.environ["WATSONX_URL"] = "servis örneği url'niz"
os.environ["WATSONX_TOKEN"] = "CPD kümesine erişmek için token'ınız"
os.environ["WATSONX_PASSWORD"] = "CPD kümesine erişmek için şifreniz"
os.environ["WATSONX_USERNAME"] = "CPD kümesine erişmek için kullanıcı adınız"
os.environ[
    "WATSONX_INSTANCE_ID"
] = "CPD kümesine erişmek için instance_id'niz"
```

## Modeli Yükleme

Farklı modeller veya görevler için model parametrelerini (`parameters`) ayarlamanız gerekebilir. Detaylar için [Available MetaNames](https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html#metanames.GenTextParamsMetaNames) sayfasına bakın.

```python
temperature = 0.5
max_new_tokens = 50
additional_params = {
    "decoding_method": "sample",
    "min_new_tokens": 1,
    "top_k": 50,
    "top_p": 1,
}
```

Daha önce ayarlanan parametrelerle `WatsonxLLM` sınıfını başlatın.

**Not**: 

- API çağrısı için bağlam sağlamak üzere `project_id` veya `space_id` değerini iletmeniz gerekir. Proje veya alan kimliğinizi almak için projenizi veya alanınızı açın, **Yönet (Manage)** sekmesine gidin ve **Genel (General)** seçeneğine tıklayın. Daha fazla bilgi için [Proje dokümantasyonu](https://www.ibm.com/docs/en/watsonx-as-a-service?topic=projects) veya [Dağıtım alanı dokümantasyonu](https://www.ibm.com/docs/en/watsonx/saas?topic=spaces-creating-deployment) bölümlerine bakın.
- Tahsis edilen servis örneğinizin bölgesine bağlı olarak, [watsonx.ai API Kimlik Doğrulama](https://ibm.github.io/watsonx-ai-python-sdk/setup_cloud.html#authentication) sayfasında listelenen URL'lerden birini kullanın.

Bu örnekte `project_id` ve Dallas URL'sini kullanacağız.

Çıkarım (inferencing) için kullanılacak `model_id` değerini belirtmeniz gerekir. Desteklenen tüm modellerin listesini [Desteklenen temel modeller](https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html#ibm_watsonx_ai.foundation_models.utils.enums.ModelTypes) sayfasında bulabilirsiniz.

```python
from llama_index.llms.ibm import WatsonxLLM

watsonx_llm = WatsonxLLM(
    model_id="ibm/granite-13b-instruct-v2",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="PROJE_ID_NIZI BURAYA YAPIŞTIRIN",
    temperature=temperature,
    max_new_tokens=max_new_tokens,
    additional_params=additional_params,
)
```

Alternatif olarak, Cloud Pak for Data kimlik bilgilerini kullanabilirsiniz. Detaylar için [watsonx.ai yazılım kurulumu](https://ibm.github.io/watsonx-ai-python-sdk/setup_cpd.html) sayfasına bakın.    

```python
watsonx_llm = WatsonxLLM(
    model_id="ibm/granite-13b-instruct-v2",
    url="URL'NIZI BURAYA YAPIŞTIRIN",
    username="KULLANICI ADINIZI BURAYA YAPIŞTIRIN",
    password="ŞİFRENİZİ BURAYA YAPIŞTIRIN",
    instance_id="openshift",
    version="4.8",
    project_id="PROJE_ID_NIZI BURAYA YAPIŞTIRIN",
    temperature=temperature,
    max_new_tokens=max_new_tokens,
    additional_params=additional_params,
)
```

`model_id` yerine, önceden ince ayarı (tuning) yapılmış modelin `deployment_id` değerini de iletebilirsiniz. Tüm model ince ayar iş akışı [TuneExperiment ve PromptTuner ile çalışma](https://ibm.github.io/watsonx-ai-python-sdk/pt_working_with_class_and_prompt_tuner.html) sayfasında açıklanmaktadır.

```python
watsonx_llm = WatsonxLLM(
    deployment_id="DEPOYMENT_ID_NIZI BURAYA YAPIŞTIRIN",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="PROJE_ID_NIZI BURAYA YAPIŞTIRIN",
    temperature=temperature,
    max_new_tokens=max_new_tokens,
    additional_params=additional_params,
)
```

## Tamamlama (Completion) Oluşturma
Dize türü bir istem (prompt) kullanarak modeli doğrudan çağırın:

```python
response = watsonx_llm.complete("Üretken yapay zeka (Generative AI) nedir?")
print(response)
```

    Üretken yapay zeka, yeni metin, görüntü veya diğer içerik türlerini oluşturabilen bir bilgisayar programıdır. Bu programlar, mevcut içeriklerin büyük veri kümeleri üzerinde eğitilir ve bu verileri, eğitim verilerine benzeyen yeni içerikler üretmek için kullanırlar.

`CompletionResponse` nesnesinden, servis tarafından döndürülen ham yanıtı da alabilirsiniz:

```python
print(response.raw)
```

    {'model_id': 'ibm/granite-13b-instruct-v2', 'created_at': '2024-05-20T07:11:57.984Z', 'results': [{'generated_text': 'A generative AI is a computer program that can create new text, images, or other types of content...', 'generated_token_count': 50, 'input_token_count': 7, 'stop_reason': 'max_tokens', 'seed': 494448017}]}

Bir istem şablonu (prompt template) sağlayan bir modeli de çağırabilirsiniz:

```python
from llama_index.core import PromptTemplate

template = "{object} nedir ve nasıl çalışır?"
prompt_template = PromptTemplate(template=template)

prompt = prompt_template.format(object="Kredi")

response = watsonx_llm.complete(prompt)
print(response)
```

    Kredi, bir ev veya araba gibi bir şey satın almak için ödünç alınan bir miktar paradır. Borçlu, krediyi artı faizini geri ödemelidir. Faiz, parayı kullanmak için alınan bir ücrettir. Faiz oranı...

## Mesaj listesiyle `chat` fonksiyonunu çağırma
Mesajların bir listesini sağlayarak `chat` tamamlamaları oluşturun:

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="system", content="Sen bir yapay zeka asistanısın"),
    ChatMessage(role="user", content="Sen kimsin?"),
]
response = watsonx_llm.chat(
    messages, max_new_tokens=20, decoding_method="greedy"
)
print(response)
```

    assistant: Ben bir yapay zeka asistanıyım.

Burada `max_new_tokens` parametresini `20` ve `decoding_method` parametresini `greedy` (açgözlü) olarak değiştirdiğimize dikkat edin.

## Model çıktısını akış (streaming) olarak alma

Modelin yanıtını akış olarak alın:

```python
for chunk in watsonx_llm.stream_complete(
    "En sevdiğin şehri ve nedenini açıkla."
):
    print(chunk.delta, end="")
```

    New York'u seviyorum çünkü hayallerin şehri. Burada istediğin her şeyi başarabilirsin.

Benzer şekilde, `chat` tamamlamalarını akış olarak almak için aşağıdaki kodu kullanın:

```python
messages = [
    ChatMessage(role="system", content="Sen bir yapay zeka asistanısın"),
    ChatMessage(role="user", content="Sen kimsin?"),
]

for chunk in watsonx_llm.stream_chat(messages):
    print(chunk.delta, end="")
```

    Ben bir yapay zeka asistanıyım.