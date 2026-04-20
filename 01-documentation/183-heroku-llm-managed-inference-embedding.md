# Heroku LLM Yönetilen Çıkarım (Managed Inference) Embedding'leri

`llama-index-embeddings-heroku` paketi, Heroku'nun Yönetilen Çıkarım (Managed Inference) platformundaki embedding modelleriyle uygulamalar oluşturmak için LlamaIndex entegrasyonlarını içerir. Bu entegrasyon, Heroku'nun altyapısında konuşlandırılmış yapay zeka modellerine kolayca bağlanmanıza ve bunları kullanmanıza olanak tanır.

## Kurulum

```python
%pip install llama-index-embeddings-heroku
```

## Kurulum (Setup)

### 1. Bir Heroku Uygulaması Oluşturun

Öncelikle Heroku'da bir uygulama oluşturun:

```bash
heroku create $APP_NAME
```

### 2. Yapay Zeka Modelleri Oluşturun ve Bağlayın

Uygulamanıza bir sohbet modeli oluşturun ve bağlayın:

```bash
heroku ai:models:create -a $APP_NAME cohere-embed-multilingual --as EMBEDDING
```

### 3. Yapılandırma Değişkenlerini Dışa Aktarın (Export)

Gerekli yapılandırma değişkenlerini dışa aktarın:

```bash
export EMBEDDING_KEY=$(heroku config:get EMBEDDING_KEY -a $APP_NAME)
export EMBEDDING_MODEL_ID=$(heroku config:get EMBEDDING_MODEL_ID -a $APP_NAME)
export EMBEDDING_URL=$(heroku config:get EMBEDDING_URL -a $APP_NAME)
```

## Kullanım

### Temel Kullanım

```python
# Heroku LLM'i başlatın
from llama_index.embeddings.heroku import HerokuEmbedding

# Heroku Embedding'i başlatın
embedding_model = HerokuEmbedding()

# Tek bir embedding al
embedding = embedding_model.get_text_embedding("Merhaba dünya!")
print(f"Embedding boyutu: {len(embedding)}")

# Birden fazla metin için embedding al
texts = ["Merhaba", "dünya", "Heroku'dan", "selamlar"]
embeddings = embedding_model.get_text_embedding_batch(texts)
print(f"Embedding sayısı: {len(embeddings)}")
```

### Ortam Değişkenlerini Kullanma

Entegrasyon, ortam değişkenlerinden otomatik olarak okuma yapar:

```python
import os

# Ortam değişkenlerini ayarla
os.environ["EMBEDDING_KEY"] = "embedding-anahtarınız"
os.environ["EMBEDDING_URL"] = "https://us.inference.heroku.com"
os.environ["EMBEDDING_MODEL_ID"] = "claude-3-5-haiku"

# Parametre olmadan başlat
llm = HerokuEmbedding()
```

### Parametre Kullanımı

Parametreleri doğrudan da geçirebilirsiniz:

```python
import os
from llama_index.embeddings.heroku import HerokuEmbedding

embedding_model = HerokuEmbedding(
    model=os.getenv("EMBEDDING_MODEL_ID", "cohere-embed-multilingual"),
    api_key=os.getenv("EMBEDDING_KEY", "embedding-anahtarınız"),
    base_url=os.getenv("EMBEDDING_URL", "https://us.inference.heroku.com"),
    timeout=60.0,
)

print(embedding_model.get_text_embedding("Merhaba Heroku!"))
```

## Mevcut Modeller

Mevcut modellerin tam listesi için [Heroku Yönetilen Çıkarım (Managed Inference) dökümantasyonuna](https://devcenter.heroku.com/articles/heroku-inference#available-models) bakın.

## Hata Ayıklama

Entegrasyon, yaygın sorunlar için uygun hata ayıklama işlemlerini içerir:

-   Eksik API anahtarı
-   Geçersiz çıkarım (inference) URL'si
-   Eksik model yapılandırması

## Ek Bilgiler

Heroku Yönetilen Çıkarım hakkında daha fazla bilgi için [resmi dökümantasyonu](https://devcenter.heroku.com/articles/heroku-inference) ziyaret edin.