# Helicone AI Gateway

Helicone, istekleri gözlemlenebilirlik, kontrol ve önbelleğe alma özellikleri ile birçok sağlayıcıya yönlendiren OpenAI uyumlu bir AI Geçididir (AI Gateway). [Helicone dokümanlarından](https://docs.helicone.ai/) daha fazla bilgi edinebilir ve mevcut [modelleri](https://www.helicone.ai/models) görebilirsiniz.

Eğer bu Notebook'u Colab üzerinde açıyorsanız, muhtemelen aşağıdaki entegrasyon paketlerini kurmanız gerekecektir.

Notlar:
- Sadece Helicone API anahtarınız gereklidir (`HELICONE_API_KEY`); sağlayıcı anahtarlarına gerek yoktur.
- Varsayılan temel URL `https://ai-gateway.helicone.ai/v1` adresidir. `api_base` veya `HELICONE_API_BASE` ile bunu değiştirebilirsiniz.

```python
%pip install llama-index-llms-helicone
```

```python
!pip install llama-index
```

```python
from llama_index.llms.helicone import Helicone
from llama_index.core.llms import ChatMessage
```

## ChatMessage Listesi ile `chat` Çağrısı
`HELICONE_API_KEY` ortam değişkenini ayarlamanız veya kurucuya (constructor) `api_key` parametresini iletmeniz gerekir.

```python
# import os
# os.environ["HELICONE_API_KEY"] = "<helicone-api-anahtarınız>"

llm = Helicone(
    api_key="<helicone-api-anahtarınız>",  # veya HELICONE_API_KEY ayarlayın
    model="gpt-4o-mini",  # Helicone AI Gateway üzerinden yönlendirilir
    max_tokens=256,
)
```

```python
message = ChatMessage(role="user", content="Bana bir fıkra anlat")
resp = llm.chat([message])
print(resp)
```

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Bana 200 kelimelik bir hikaye anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

## API Desteği (Sadece Chat; eski Completions desteklenmez)
Helicone, OpenAI uyumlu Chat Completions ve daha yeni olan Responses API'sini destekler. Eski (legacy) Completions API'si desteklenmemektedir.

LlamaIndex'te `llm.chat(...)` ve `llm.stream_chat(...)` fonksiyonlarını kullanın.

## Model Yapılandırması

```python
# Helicone tarafından yönlendirilen herhangi bir OpenAI uyumlu modeli seçin.
# Seçenekler için https://www.helicone.ai/models adresine bakın.

# Eğer HELICONE_API_KEY ortamınızda ayarlanmışsa, burada api_key'i atlayabilirsiniz.
llm = Helicone(model="gpt-4o-mini")
message = ChatMessage(
    role="user", content="Rust ejderhalarının kod yazması hakkında bir cümle yaz."
)
resp = llm.chat([message])
print(resp)
```