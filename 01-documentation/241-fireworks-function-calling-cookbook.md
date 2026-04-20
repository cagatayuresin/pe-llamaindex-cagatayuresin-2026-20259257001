# Fireworks Fonksiyon Çağırma Tarif Defteri (Cookbook)

Fireworks.ai, OpenAI'ya benzer şekilde LLM'leri için fonksiyon çağırmayı (function calling) destekler. Bu, kullanıcıların mevcut araç/fonksiyon setini doğrudan tanımlamasına ve modelin; kullanıcı tarafında karmaşık istemlere (prompting) gerek kalmadan, çağrılacak doğru fonksiyonları dinamik olarak seçmesine olanak tanır.

Fireworks LLM'imiz doğrudan OpenAI'nın bir alt sınıfı (subclass) olduğu için Fireworks ile mevcut soyutlamalarımızı kullanabiliriz.

Bunu üç seviyede gösteriyoruz: doğrudan model API'si üzerinden, bir Pydantic Programının (yapılandırılmış çıktı çıkarma) bir parçası olarak ve bir ajanın parçası olarak.

```python
%pip install llama-index-llms-fireworks
```

```python
%pip install llama-index
```

```python
import os

os.environ["FIREWORKS_API_KEY"] = "fw_3ZkvBpQyjRzbicpihhrihaEP"
```

```python
from llama_index.llms.fireworks import Fireworks

## fireworks modelini tanımlayın, fonksiyon çağırma modellerinin listesi için bkz: https://app.fireworks.ai/models/?filter=LLM&functionCalling=true
llm = Fireworks(
    model="accounts/fireworks/models/deepseek-v3p1-terminus", temperature=0
)
```

## LLM Modülü Üzerinde Fonksiyon Çağırma

Fonksiyon çağrılarını doğrudan LLM modülü üzerinden gerçekleştirebilirsiniz.

```python
import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field
from llama_index.llms.openai.utils import to_openai_tool


class Song(BaseModel):
    """Adı ve sanatçısı olan bir şarkı"""

    name: str = Field(description="Şarkının adı")
    artist: str = Field(description="Şarkıyı seslendiren sanatçı")


song_fn = to_openai_tool(Song)

# Fireworks istemcisini başlatın
client = OpenAI(
    api_key=os.environ.get("FIREWORKS_API_KEY"),
    base_url="https://api.fireworks.ai/inference/v1",
)

response = client.chat.completions.create(
    model="accounts/fireworks/models/kimi-k2-instruct-0905",
    messages=[{"role": "user", "content": "Beyonce'den bir şarkı oluştur"}],
    tools=[song_fn],
    temperature=0.1,
)

print(response)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"\nÇağrılan araç: {tool_call.function.name}")

    # Yapılandırılmış çıktıyı almak için argümanları ayrıştırın
    arguments = json.loads(tool_call.function.arguments)
    print(f"Argümanlar: {arguments}")

    # Yapılandırılmış çıktıdan Song örneği oluşturun
    song = Song(**arguments)
    print(f"\nAyrıştırılan Şarkı:")
    print(f"Ad: {song.name}")
    print(f"Sanatçı: {song.artist}")
```

    ChatCompletion(id='07921e74-5dca-409c-a4d3-1a2e0c7cd1e7', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='```json\n{\n  "name": "Halo",\n  "artist": "Beyoncé"\n}\n```', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None))], created=1761704700, model='accounts/fireworks/models/kimi-k2-instruct-0905', object='chat.completion', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=25, prompt_tokens=145, total_tokens=170, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0)))
