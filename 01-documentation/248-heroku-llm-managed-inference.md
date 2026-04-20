# Heroku LLM Yönetilen Çıkarım (Managed Inference)

`llama-index-llms-heroku` paketi, Heroku'nun Yönetilen Çıkarım (Managed Inference) platformundaki modellerle uygulamalar oluşturmak için LlamaIndex entegrasyonlarını içerir. Bu entegrasyon, Heroku'nun altyapısında konuşlandırılan AI modellerine kolayca bağlanmanıza ve bunları kullanmanıza olanak tanır.

## Kurulum

```python
%pip install llama-index-llms-heroku
```

## Kurulum (Setup)

### 1. Bir Heroku Uygulaması Oluşturun

Öncelikle, Heroku'da bir uygulama oluşturun:

```bash
heroku create $APP_NAME
```

### 2. AI Modelleri Oluşturun ve Bağlayın

Uygulamanıza bir sohbet modeli oluşturun ve bağlayın:

```bash
heroku ai:models:create -a $APP_NAME claude-3-5-haiku
```

### 3. Yapılandırma Değişkenlerini Dışa Aktarın

Gerekli yapılandırma değişkenlerini dışa aktarın:

```bash
export INFERENCE_KEY=$(heroku config:get INFERENCE_KEY -a $APP_NAME)
export INFERENCE_MODEL_ID=$(heroku config:get INFERENCE_MODEL_ID -a $APP_NAME)
export INFERENCE_URL=$(heroku config:get INFERENCE_URL -a $APP_NAME)
```

## Kullanım

### Temel Kullanım

```python
from llama_index.llms.heroku import Heroku
from llama_index.core.llms import ChatMessage, MessageRole

# Heroku LLM'i başlatın
llm = Heroku()

# Sohbet mesajları oluşturun
messages = [
    ChatMessage(
        role=MessageRole.SYSTEM, content="Yardımsever bir asistansın."
    ),
    ChatMessage(
        role=MessageRole.USER,
        content="Kuzey Amerika'daki en popüler evcil hayvanlar nelerdir?",
    ),
]

# Yanıtı alın
response = llm.chat(messages)
print(response)
```

### Ortam Değişkenlerini Kullanma

Entegrasyon otomatik olarak ortam değişkenlerinden okuma yapar:

```python
import os

# Ortam değişkenlerini ayarlayın
os.environ["INFERENCE_KEY"] = "inference-anahtarınız"
os.environ["INFERENCE_URL"] = "https://us.inference.heroku.com"
os.environ["INFERENCE_MODEL_ID"] = "claude-3-5-haiku"

# Parametre belirtmeden başlatın
llm = Heroku()
```

### Parametreleri Kullanma

Parametreleri doğrudan da iletebilirsiniz:

```python
import os

llm = Heroku(
    model=os.getenv("INFERENCE_MODEL_ID", "claude-3-5-haiku"),
    api_key=os.getenv("INFERENCE_KEY", "inference-anahtarınız"),
    inference_url=os.getenv(
        "INFERENCE_URL", "https://us.inference.heroku.com"
    ),
    max_tokens=1024,
)
```

## Mevcut Modeller

Mevcut modellerin tam listesi için [Heroku Yönetilen Çıkarım dokümantasyonuna](https://devcenter.heroku.com/articles/heroku-inference#available-models) bakın.

## Hata Yönetimi

Entegrasyon, yaygın sorunlar için uygun hata yönetimini içerir:

- Eksik API anahtarı
- Geçersiz çıkarım URL'si
- Eksik model yapılandırması

## Ek Bilgiler

Heroku Yönetilen Çıkarım (Managed Inference) hakkında daha fazla bilgi için [resmi dokümantasyonu](https://devcenter.heroku.com/articles/heroku-inference) ziyaret edin.