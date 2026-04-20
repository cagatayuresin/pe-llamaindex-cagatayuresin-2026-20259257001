# Azure OpenAI

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-azure-openai
```

```python
!pip install llama-index
```

## Ön Koşullar

1. Bir Azure aboneliği kurun - [buradan](https://azure.microsoft.com/en-us/free/cognitive-services/) ücretsiz bir tane oluşturabilirsiniz.
2. Azure OpenAI Hizmetine erişim için [buradan](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOFA5Qk1UWDRBMjg0WFhPMkIzTzhKQ1dWNyQlQCN0PWcu) başvurun.
3. Azure portalında [buradan](https://portal.azure.com/?microsoft_azure_marketplace_ItemHideKey=microsoft_openai_tip#create/Microsoft.CognitiveServicesOpenAI) bir kaynak oluşturun.
4. [Buradaki](https://oai.azure.com/) Azure OpenAI Studio'da bir model dağıtın.

[Bu kılavuzda](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal) daha fazla ayrıntı bulabilirsiniz.

LLM'nize bağlanırken ihtiyacınız olacağından **"model adı"** ve **"dağıtım adı"** bilgilerini not edin.

## Ortam Kurulumu

### Kurulum bilgilerinizi bulun - API tabanı (base), API anahtarı, dağıtım adı (yani engine) vb.

Gerekli kurulum bilgilerini bulmak için şu adımları izleyin:
1. [Buradan](https://oai.azure.com/) Azure OpenAI Studio'ya gidin.
2. Sohbet (chat) veya tamamlama (completions) oyun alanına (playground) gidin (hangi LLM'yi kurduğunuza bağlı olarak).
3. "Kodu görüntüle" (view code) düğmesine tıklayın (aşağıdaki resimde gösterilmiştir).

```python
from IPython.display import Image

Image(filename="./azure_playground.png")
```

![png](output_10_0.png)

4. `api_type`, `api_base`, `api_version`, `engine` (bu, önceki "dağıtım adı" ile aynı olmalıdır) ve `key` (anahtar) bilgilerini not edin.

```python
from IPython.display import Image

Image(filename="./azure_env.png")
```

![png](output_12_0.png)

### Ortam değişkenlerini yapılandırın

OpenAI modellerinin Azure dağıtımını kullanmak, normal OpenAI kullanımına çok benzer. Sadece birkaç ortam değişkenini daha yapılandırmanız gerekir.

- `OPENAI_API_VERSION`: Bunu `2023-07-01-preview` olarak ayarlayın. Bu bilgi gelecekte değişebilir.
- `AZURE_OPENAI_ENDPOINT`: Uç noktanız şuna benzemelidir:
    https://KAYNAK_ADINIZ.openai.azure.com/
- `AZURE_OPENAI_API_KEY`: API anahtarınız

```python
import os

os.environ["AZURE_OPENAI_API_KEY"] = "<api-anahtarınız>"
os.environ[
    "AZURE_OPENAI_ENDPOINT"
] = "https://<kaynak-adınız>.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
```

## LLM'nizi Kullanın

```python
from llama_index.llms.azure_openai import AzureOpenAI
```

Normal `OpenAI`'den farklı olarak, `model` argümanına ek olarak bir `engine` argümanı geçmeniz gerekir. `engine`, Azure OpenAI Studio'da seçtiğiniz model dağıtımınızın adıdır. Daha fazla ayrıntı için "kurulum bilgilerinizi bulun" başlıklı önceki bölüme bakın.

```python
llm = AzureOpenAI(
    engine="simon-llm", model="gpt-35-turbo-16k", temperature=0.0
)
```

Alternatif olarak, ortam değişkenlerini ayarlamayı atlayabilir ve parametreleri doğrudan yapıcı (constructor) aracılığıyla geçebilirsiniz.

```python
llm = AzureOpenAI(
    engine="ozel-llm-adim",
    model="gpt-35-turbo-16k",
    temperature=0.0,
    azure_endpoint="https://<kaynak-adınız>.openai.azure.com/",
    api_key="<api-anahtarınız>",
    api_version="2023-07-01-preview",
)
```

Metin tamamlama için `complete` uç noktasını kullanın

```python
response = llm.complete("Gökyüzü güzel bir mavi ve")
print(response)
```

    güneş parlıyor. Kabarık beyaz bulutlar gökyüzünde tembelce süzülüyor, pitoresk bir manzara oluşturuyor. Gökyüzünün canlı mavi rengi sakinlik ve huzur hissi veriyor. Güneşin sıcaklığının ve hafif esintinin tadını çıkarmak için dışarıda olmak için mükemmel bir gün. Gökyüzü sonsuzca uzanıyor gibi görünüyor, bize etrafımızdaki dünyanın enginliğini ve güzelliğini hatırlatıyor. Hayattaki basit zevklerin değerini bilmek ve etrafımızı saran doğal mucizelere hayran kalmak için bir an durup düşünmek gerektiğini hatırlatıyor.

```python
response = llm.stream_complete("Gökyüzü güzel bir mavi ve")
for r in response:
    print(r.delta, end="")
```

    güneş parlıyor. Kabarık beyaz bulutlar gökyüzünde tembelce süzülüyor, pitoresk bir manzara oluşturuyor. Gökyüzünün canlı mavi rengi sakinlik ve huzur hissi veriyor. Güneşin sıcaklığının ve hafif esintinin tadını çıkarmak için dışarıda olmak için mükemmel bir gün. Gökyüzü sonsuzca uzanıyor gibi görünüyor, bize etrafımızdaki dünyanın enginliğini ve güzelliğini hatırlatıyor. Hayattaki basit zevklerin değerini bilmek ve durup etrafımızı çevreleyen doğal mucizelere hayran kalmak için bir an durup düşünmek gerektiğini hatırlatıyor.

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

    assistant: Ahoy oradaki, ahbap! Bu güzel günde nasılsın? Ben Kaptan Jolly Roger, gördüğün en renkli korsanım! Gemime seni ne getirdi?

```python
response = llm.stream_chat(messages)
for r in response:
    print(r.delta, end="")
```

    Ahoy oradaki, ahbap! Bu güzel günde nasılsın? Ben Kaptan Jolly Roger, gördüğün en renkli korsanım! Gemime seni ne getirdi?

Her sohbet veya tamamlama çağrısına aynı parametreleri eklemek yerine, bunları `additional_kwargs` ile örnek bazında ayarlayabilirsiniz.

```python
llm = AzureOpenAI(
    engine="simon-llm",
    model="gpt-35-turbo-16k",
    temperature=0.0,
    additional_kwargs={"user": "kullanici_id_niz"},
)
```
