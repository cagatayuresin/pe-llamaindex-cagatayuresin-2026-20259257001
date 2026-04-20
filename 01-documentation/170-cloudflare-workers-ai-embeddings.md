# Cloudflare Workers AI Embedding'leri

## Kurulum

Kütüphaneyi pip aracılığıyla kurun

```python
%pip install llama-index-embeddings-cloudflare-workersai
# %pip install -e ~/llama_index/llama-index-integrations/embeddings/llama-index-embeddings-cloudflare-workersai
```

Cloudflare Workers AI'a erişmek için hem Cloudflare hesap kimliği (account ID) hem de API belirteci (API token) gereklidir. Hesap kimliğinizi ve API belirtecinizi almak için lütfen [bu dökümandaki](https://developers.cloudflare.com/workers-ai/get-started/rest-api/) talimatları izleyin.

```python
# Hesap kimliği ve API belirteci ile başlatın

# import os

# my_account_id = "örnek_id"
# my_api_token = "örnek_belirteç"
# os.environ["CLOUDFLARE_AUTH_TOKEN"] = "my_api_token"

import getpass

my_account_id = getpass.getpass("Cloudflare hesap kimliğinizi (account ID) girin:\n\n")
my_api_token = getpass.getpass("Cloudflare API belirtecinizi (API token) girin:\n\n")
```

## Metin Embedding Örneği

```python
from llama_index.embeddings.cloudflare_workersai import CloudflareEmbedding

my_embed = CloudflareEmbedding(
    account_id=my_account_id,
    auth_token=my_api_token,
    model="@cf/baai/bge-small-en-v1.5",
)

embeddings = my_embed.get_text_embedding("Gökyüzü neden mavidir")

print(len(embeddings))
print(embeddings[:5])
```

    384
    [-0.04786296561360359, -0.030788540840148926, -0.07126234471797943, -0.04107927531003952, 0.02904760278761387]

#### Toplu Olarak (Batch) Embedding Oluşturma

Toplu işlem boyutu (batch size) konusunda Cloudflare'in sınırı, 31 Mart 2024 itibarıyla en fazla 100'dür.

```python
embeddings = my_embed.get_text_embedding_batch(
    ["Gökyüzü neden mavidir", "Güller neden kırmızıdır"]
)
print(len(embeddings))
print(len(embeddings[0]))
print(embeddings[0][:5])
print(embeddings[1][:5])
```

    2
    384
    [-0.04786296561360359, -0.030788540840148926, -0.07126234471797943, -0.04107927531003952, 0.02904760278761387]
    [-0.08951402455568314, -0.015274363569915295, 0.04728245735168457, 0.05478525161743164, 0.05978189781308174]