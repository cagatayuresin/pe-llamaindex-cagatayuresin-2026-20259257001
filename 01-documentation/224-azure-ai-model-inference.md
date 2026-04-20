# Azure AI model çıkarımı (Azure AI model inference)

Bu not defteri, Azure AI Studio veya Azure Machine Learning'deki Azure AI model çıkarım (AI model inference) API'si ile dağıtılan modellerle `llama-index-llm-azure-inference` paketinin nasıl kullanılacağını açıklar. Paket ayrıca GitHub Modelleri (Önizleme) uç noktalarını da destekler.

```python
%pip install llama-index-llms-azure-inference
```

Eğer bu not defterini Google Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index
```

## Ön Koşullar

Azure AI model çıkarımı, geliştiricilerin tutarlı bir şema kullanarak Azure AI'da barındırılan çeşitli modellere erişmesini sağlayan bir API'dir. `llama-index-llms-azure-inference` entegrasyon paketini, Azure AI sunucusuz API uç noktalarına dağıtılan modeller ve Yönetilen Çıkarım'dan (Managed Inference) bir dizi model dahil olmak üzere bu API'yi destekleyen modellerle kullanabilirsiniz. API spesifikasyonu ve bunu destekleyen modeller hakkında daha fazla bilgi edinmek için [Azure AI model çıkarım API'si](https://aka.ms/azureai/modelinference) sayfasına bakabilirsiniz.

Bu öğreticiyi çalıştırmak için şunlara ihtiyacınız vardır:

1. Bir [Azure aboneliği](https://azure.microsoft.com) oluşturun.
2. [Azure AI Studio merkezi nasıl oluşturulur ve yönetilir](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-azure-ai-resource) sayfasında açıklandığı gibi bir Azure AI merkezi (hub) kaynağı oluşturun.
3. [Azure AI model çıkarım API'sini](https://aka.ms/azureai/modelinference) destekleyen bir model dağıtın. Bu örnekte bir `Mistral-Large` dağıtımı kullanıyoruz.

    * [Modelleri sunucusuz API'ler olarak dağıtma](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless) talimatlarını izleyebilirsiniz.

Alternatif olarak, ücretsiz kullanım deneyimi dahil olmak üzere bu entegrasyonla GitHub Modelleri uç noktalarını kullanabilirsiniz. [GitHub modelleri](https://github.com/marketplace/models) hakkında daha fazla bilgi edinin.

## Ortam Kurulumu

Kullanmak istediğiniz modelden ihtiyacınız olan bilgileri almak için şu adımları izleyin:

1. Kullandığınız ürüne bağlı olarak [Azure AI Foundry (eski adıyla Azure AI Studio)](https://ai.azure.com/) veya [Azure Machine Learning studio](https://ml.azure.com) adresine gidin.
2. Dağıtımlara (Azure Machine Learning'de uç noktalar) gidin ve ön koşullarda belirtildiği gibi dağıttığınız modeli seçin.
3. Uç nokta (endpoint) URL'sini ve anahtarı (key) kopyalayın.

> Modeliniz Microsoft Entra Kimlik desteğiyle dağıtıldıysa anahtara ihtiyacınız yoktur.

Bu senaryoda, hem uç nokta URL'sini hem de anahtarı aşağıdaki ortam değişkenlerine yerleştirdik:

```python
import os

os.environ["AZURE_INFERENCE_ENDPOINT"] = "<uc-noktaniz>"
os.environ["AZURE_INFERENCE_CREDENTIAL"] = "<kimlik-bilginiz>"
```

## Dağıtımınıza ve Uç Noktanıza Bağlanın

Azure AI Studio veya Azure Machine Learning'de dağıtılan LLM'leri kullanmak için uç noktaya ve ona bağlanmak için kimlik bilgilerine ihtiyacınız vardır. Managed Online Endpoints gibi tek bir modele hizmet veren uç noktalar için `model_name` parametresi gerekli değildir.

```python
from llama_index.llms.azure_inference import AzureAICompletionsModel
```

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

Alternatif olarak, uç noktanız Microsoft Entra Kimliğini destekliyorsa, istemciyi oluşturmak için aşağıdaki kodu kullanabilirsiniz:

```python
from azure.identity import DefaultAzureCredential

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

> Not: Microsoft Entra Kimliğini kullanırken, uç noktanın bu kimlik doğrulama yöntemiyle dağıtıldığından ve onu çağırmak için gerekli izinlere sahip olduğunuzdan emin olun.

Asenkron çağırma kullanmayı planlıyorsanız, kimlik bilgileri için asenkron sürümü kullanmak en iyi uygulamadır:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
)
```

Uç noktanız [GitHub Modelleri](https://github.com/marketplace/models) veya Azure AI Hizmetleri gibi birden fazla modele hizmet veriyorsa, `model_name` parametresini belirtmeniz gerekir:

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="mistral-large",  # kullanmak istediğiniz modele göre değiştirin
)
```

## Modeli Kullanma

Metin tamamlama için `complete` uç noktasını kullanın. `chat-completions` türündeki modeller için `complete` yöntemi hala mevcuttur. Bu durumlarda, giriş metniniz `role="user"` olan bir mesaja dönüştürülür.

```python
response = llm.complete("Gökyüzü güzel bir mavi ve")
print(response)
```

```python
response = llm.stream_complete("Gökyüzü güzel bir mavi ve")
for r in response:
    print(r.delta, end="")
```

Sohbet için `chat` uç noktasını kullanın

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın."
    ),
    ChatMessage(role="user", content="Merhaba"),
]

response = llm.chat(messages)
print(response)
```

```python
response = llm.stream_chat(messages)
for r in response:
    print(r.delta, end="")
```

Her sohbet veya tamamlama çağrısına aynı parametreleri eklemek yerine, bunları istemci örneğinde ayarlayabilirsiniz.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"top_p": 1.0},
)
```

```python
response = llm.complete("Gökyüzü güzel bir mavi ve")
print(response)
```

Azure AI model çıkarım API'si tarafından desteklenmeyen ancak temel modelde mevcut olan ek parametreler için `model_extras` argümanını kullanabilirsiniz. Aşağıdaki örnekte, yalnızca Mistral modelleri için mevcut olan `safe_prompt` parametresi geçilmektedir.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"model_extras": {"safe_prompt": True}},
)
```

```python
response = llm.complete("Gökyüzü güzel bir mavi ve")
print(response)
```

## Ek kaynaklar

bu entegrasyon hakkında daha fazla bilgi edinmek için [LlamaIndex ve Azure AI ile Başlarken](https://aka.ms/azureai/llamaindex) sayfasını ziyaret edin.
