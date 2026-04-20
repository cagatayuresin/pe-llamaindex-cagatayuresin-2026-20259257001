# Yapılandırılmış Çıktı (Structured Output) Kullanımı

Çoğu zaman bir ajandan sonuçları belirli bir formatta almanız gerekir. Ajan sonuçları iki şekilde yapılandırılmış JSON döndürebilir:

1.  `output_cls` – Çıktı şeması olarak kullanılacak bir Pydantic modeli.
2.  `structured_output_fn` – Daha gelişmiş kullanım durumları için, ajanın konuşmasını istediğiniz herhangi bir modele doğrulayan veya yeniden yazan özel bir fonksiyon.

Hem `FunctionAgent` ve `ReActAgent` gibi tekli ajanlar hem de çoklu ajanlı `AgentWorkflow` iş akışları bu seçenekleri destekler; gelin olasılıkları keşfedelim:

### `output_cls` Kullanımı

```python
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, Field

llm = OpenAI(model="gpt-4.1")


## yapılandırılmış çıktı formatını ve araçları tanımlayın
class MathResult(BaseModel):
    operation: str = Field(description="gerçekleştirilen işlem")
    result: int = Field(description="işlemin sonucu")


def multiply(x: int, y: int):
    """İki sayıyı çarpar"""
    return x * y


## ajanı tanımlayın
agent = FunctionAgent(
    tools=[multiply],
    name="calculator",
    system_prompt="Siz, `multiply` aracını kullanarak iki sayıyı çarpabilen bir hesap makinesi ajanısınız.",
    output_cls=MathResult,
    llm=llm,
)

response = await agent.run("3415 * 43144 nedir?")
print(response.structured_response)
print(response.get_pydantic_model(MathResult))
```

Bu özellik çoklu ajan iş akışlarıyla da çalışır:

```python
## yapılandırılmış çıktı formatını ve araçları tanımlayın
class Weather(BaseModel):
    location: str = Field(description="Konum")
    weather: str = Field(description="Hava durumu")


def get_weather(location: str):
    """Belirli bir konum için hava durumunu getirir"""
    return f"{location} konumunda hava güneşli"


## tekli ajanları tanımlayın
agent = FunctionAgent(
    llm=llm,
    tools=[get_weather],
    system_prompt="Siz belirli bir konum için hava durumunu alabilen bir hava durumu ajanısınız.",
    name="WeatherAgent",
    description="Hava durumu tahmin ajanı.",
)
main_agent = FunctionAgent(
    name="MainAgent",
    tools=[],
    description="Ana ajan",
    system_prompt="Siz ana ajansınız, göreviniz görevleri ikincil ajanlara, özellikle de WeatherAgent'a dağıtmaktır.",
    can_handoff_to=["WeatherAgent"],
    llm=llm,
)

## çoklu ajan iş akışını tanımlayın
workflow = AgentWorkflow(
    agents=[main_agent, agent],
    root_agent=main_agent.name,
    output_cls=Weather,
)

response = await workflow.run("Tokyo'da hava nasıl?")
print(response.structured_response)
print(response.get_pydantic_model(Weather))
```

### `structured_output_fn` Kullanımı

Özel fonksiyon, girdi olarak ajan iş akışı tarafından üretilen bir `ChatMessage` nesneleri dizisi almalı ve bir sözlük (bir `BaseModel` alt sınıfına dönüştürülebilen) döndürmelidir:

```python
import json
from llama_index.core.llms import ChatMessage
from typing import List, Dict, Any


class Flavor(BaseModel):
    flavor: str
    with_sugar: bool


async def structured_output_parsing(
    messages: List[ChatMessage],
) -> Dict[str, Any]:
    sllm = llm.as_structured_llm(Flavor)
    messages.append(
        ChatMessage(
            role="user",
            content="Önceki mesaj geçmişine dayanarak, çıktıyı sağlanan formata göre yapılandırın.",
        )
    )
    response = await sllm.achat(messages)
    return json.loads(response.message.content)


def get_flavor(ice_cream_shop: str):
    return "Strawberry with no extra sugar"


agent = FunctionAgent(
    tools=[get_flavor],
    name="ice_cream_shopper",
    system_prompt="Siz çeşitli dükkanlardaki dondurma aromalarını bilen bir ajansınız.",
    structured_output_fn=structured_output_parsing,
    llm=llm,
)

response = await agent.run(
    "Gelato Italia'da hangi çilek aroması mevcut?"
)
print(response.structured_response)
print(response.get_pydantic_model(Flavor))
```

### Yapılandırılmış Çıktı Akışı (Streaming)

İş akışı çalışırken `AgentStreamStructuredOutput` olayını kullanarak yapılandırılmış çıktıyı alabilirsiniz:

```python
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStreamStructuredOutput,
)

handler = agent.run("Gelato Italia'da hangi çilek aroması mevcut?")

async for event in handler.stream_events():
    if isinstance(event, AgentInput):
        print(event)
    elif isinstance(event, AgentStreamStructuredOutput):
        print(event.output)
        print(event.get_pydantic_model(Weather))
    elif isinstance(event, ToolCallResult):
        print(event)
    elif isinstance(event, ToolCall):
        print(event)
    elif isinstance(event, AgentOutput):
        print(event)
    else:
        pass

response = await handler
```

Ajanın yanıtındaki yapılandırılmış çıktıyı doğrudan bir sözlük olarak erişerek veya `get_pydantic_model` metodunu kullanarak bir `BaseModel` alt sınıfı olarak yükleyerek ayrıştırabilirsiniz:

```python
print(response.structured_response)
print(response.get_pydantic_model(Flavor))
```