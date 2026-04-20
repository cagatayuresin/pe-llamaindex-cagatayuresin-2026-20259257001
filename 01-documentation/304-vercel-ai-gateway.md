# Vercel AI Gateway

---
title: Vercel AI Gateway
 | LlamaIndex OSS Documentation
 ---

AI Gateway, çeşitli AI sağlayıcılarına yönelik model isteklerini yönlendiren, Vercel tarafından sunulan bir proxy hizmetidir. Birden fazla sağlayıcıya birleşik bir API sunar ve bütçe ayarlama, kullanımı izleme, istekleri yük dengeleme ve yedekleri yönetme yeteneği sağlar. Daha fazlasını [dokümanlarından](https://vercel.com/docs/ai-gateway) öğrenebilirsiniz.

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-vercel-ai-gateway
```

```python
!pip install llama-index
```

```python
from llama_index.llms.vercel_ai_gateway import VercelAIGateway
from llama_index.core.llms import ChatMessage


llm = VercelAIGateway(
    model="anthropic/claude-4-sonnet",
    max_tokens=64000,
    context_window=200000,
    api_key="api-anahtarınız",
    default_headers={
        "http-referer": "https://myapp.com/",  # Opsiyonel: Uygulama URL'niz
        "x-title": "Uygulamam",  # Opsiyonel: Uygulama adınız
    },
)


print(llm.model)
```

## ChatMessage Listesi ile `chat` Çağrısı

`VERCEL_AI_GATEWAY_API_KEY` veya `VERCEL_OIDC_TOKEN` ortam değişkenini ayarlamanız ya da sınıf yapıcısında (constructor) `api_key` değerini belirtmeniz gerekir.

```python
# import os
# os.environ['VERCEL_AI_GATEWAY_API_KEY'] = '<api-anahtarınız>'


llm = VercelAIGateway(
    api_key="pBiuCWfswZCDxt8D50DSoBfU",
    max_tokens=64000,
    context_window=200000,
    model="anthropic/claude-4-sonnet",
)
```

```python
message = ChatMessage(role="user", content="Bana bir fıkra anlat")
resp = llm.chat([message])
print(resp)
```

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Bana yaklaşık 250 kelimelik bir hikaye anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

## İstem (Prompt) ile `complete` Çağrısı

```python
resp = llm.complete("Bana bir fıkra anlat")
print(resp)
```

```python
resp = llm.stream_complete("Bana yaklaşık 250 kelimelik bir hikaye anlat")
for r in resp:
    print(r.delta, end="")
```

## Model Yapılandırması

```python
# Bu örnek Anthropic'in Claude 4 Sonnet modelini kullanır (modeller `sağlayıcı/model` şeklinde belirtilir):
llm = VercelAIGateway(
    model="anthropic/claude-4-sonnet",
    api_key="pBiuCWfswZCDxt8D50DSoBfU",
)
```

```python
resp = llm.complete("Rust dilinde kod yazabilen bir ejderha hakkında bir hikaye yaz")
print(resp)
```
