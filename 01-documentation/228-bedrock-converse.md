# Bedrock Converse

## Temel Kullanım

#### Bir istemle `complete` çağrısı yapın

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-bedrock-converse
```

```python
!pip install llama-index
```

```python
from llama_index.llms.bedrock_converse import BedrockConverse

profile_name = "AWS profil adınız"
resp = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    profile_name=profile_name,
).complete("Paul Graham bir ")
```

```python
print(resp)
```

#### Bir mesaj listesiyle `chat` çağrısı yapın

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock_converse import BedrockConverse

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]

resp = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    profile_name=profile_name,
).chat(messages)
```

```python
print(resp)
```

## Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
from llama_index.llms.bedrock_converse import BedrockConverse

llm = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    profile_name=profile_name,
)
resp = llm.stream_complete("Paul Graham bir ")
```

```python
for r in resp:
    print(r.delta, end="")
```

`stream_chat` bitiş noktasını kullanma

```python
from llama_index.llms.bedrock_converse import BedrockConverse

llm = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    profile_name=profile_name,
)
messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

## Modeli Yapılandırma

```python
from llama_index.llms.bedrock_converse import BedrockConverse

llm = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    profile_name=profile_name,
)
```

```python
resp = llm.complete("Paul Graham bir ")
```

```python
print(resp)
```

## Erişim Anahtarları (Access Keys) ile Bedrock'a Bağlanma

```python
from llama_index.llms.bedrock_converse import BedrockConverse

llm = BedrockConverse(
    model="us.amazon.nova-lite-v1:0",
    aws_access_key_id="Kullanılacak AWS Erişim Anahtar Kimliği (Access Key ID)",
    aws_secret_access_key="Kullanılacak AWS Gizli Erişim Anahtarı (Secret Access Key)",
    aws_session_token="Kullanılacak AWS Oturum Belirteci (Session Token)",
    region_name="Kullanılacak AWS Bölgesi, örn. us-east-1",
)

resp = llm.complete("Paul Graham bir ")
```

```python
print(resp)
```

## Fonksiyon Çağırma (Function Calling)

Claude, Command ve Mistral Large modelleri, AWS Bedrock Converse aracılığıyla yerel fonksiyon çağırmayı destekler. `llm` üzerindeki `predict_and_call` fonksiyonu ile LlamaIndex araçlarıyla kusursuz bir entegrasyon sağlanır.

Bu, kullanıcının herhangi bir aracı eklemesine ve hangi araçların çağrılacağına (varsa) LLM'nin karar vermesine olanak tanır.

Eğer fonksiyon çağırmayı bir aracı döngüsünün (agentic loop) parçası olarak gerçekleştirmek istiyorsanız, bunun yerine [aracı kılavuzlarımıza](https://docs.llamaindex.ai/en/latest/module_guides/deploying/agents/) göz atın.

**NOT**: AWS Bedrock'taki modellerin tümü fonksiyon çağırmayı ve Converse API'yi desteklemez. [Her bir LLM'nin kullanılabilir özelliklerini buradan kontrol edin](https://docs.aws.amazon.com/bedrock/latest/userguide/models-features.html).

```python
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.core.tools import FunctionTool

def multiply(a: int, b: int) -> int:
    """İki tamsayıyı çarpar ve sonuç tamsayısını döndürür"""
    return a * b

def mystery(a: int, b: int) -> int:
    """İki tamsayı üzerinde gizemli fonksiyon."""
    return a * b + a + b

mystery_tool = FunctionTool.from_defaults(fn=mystery)
multiply_tool = FunctionTool.from_defaults(fn=multiply)

llm = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    profile_name=profile_name,
)
```

```python
response = llm.predict_and_call(
    [mystery_tool, multiply_tool],
    user_msg="5 ve 7 üzerinde gizemli fonksiyonu çalıştırırsam ne olur?",
)
```

```python
print(str(response))
```

```python
response = llm.predict_and_call(
    [mystery_tool, multiply_tool],
    user_msg=(
        """Aşağıdaki sayı çiftleri üzerinde gizemli fonksiyonu çalıştırırsam ne olur? Her satır için ayrı bir sonuç oluşturun:
- 1 ve 2
- 8 and 4
- 100 ve 20

NOT: Yukarıdaki tüm çiftler için gizemli fonksiyonu aynı anda çalıştırmanız gerekiyor \
"""
    ),
    allow_parallel_tool_calls=True,
)
```

```python
print(str(response))
```

```python
for s in response.sources:
    print(f"Ad: {s.tool_name}, Girdi: {s.raw_input}, Çıktı: {str(s)}")
```

## Asenkron (Async)

```python
from llama_index.llms.bedrock_converse import BedrockConverse

llm = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    aws_access_key_id="Kullanılacak AWS Erişim Anahtar Kimliği",
    aws_secret_access_key="Kullanılacak AWS Gizli Erişim Anahtarı",
    aws_session_token="Kullanılacak AWS Oturum Belirteci",
    region_name="Kullanılacak AWS Bölgesi, örn. us-east-1",
)
resp = await llm.acomplete("Paul Graham bir ")
```

```python
print(resp)
```
