# LlamaIndex ile Opus 4.1 Kullanımı

---
title: LlamaIndex ile Opus 4.1 Kullanımı
 | LlamaIndex OSS Documentation
---

Bu not defterinde, sevimli bir web sitesi oluşturmak için [Anthropic'in Claude Opus 4.1](https://www.anthropic.com/news/claude-opus-4-1) gelişmiş kodlama yeteneklerinden yararlanacağız ve bunu LlamaIndex içerisinde yapacağız!

## Opus 4.1 ile LLM tabanlı bir asistan oluşturun

**1. Gerekli bağımlılıkları yükleyin**

```python
! pip install -q llama-index-llms-anthropic get-code-from-markdown
```

Markdown'dan kodu çekmemize yardımcı olacak bir yardımcı fonksiyon tanımlayalım:

```python
from get_code_from_markdown import get_code_from_markdown




def fetch_code_from_markdown(markdown: str) -> str:
    return get_code_from_markdown(markdown, language="html")
```

Şimdi LLM'imizi başlatalım:

```python
import os
import getpass


os.environ["ANTHROPIC_API_KEY"] = getpass.getpass()
```

```python
from llama_index.llms.anthropic import Anthropic


llm = Anthropic(model="claude-opus-4-1-20250805", max_tokens=12000)
```

```python
res = llm.complete(
    "Can you build a llama-themed static HTML page, with cute little bouncing animations and blue/white/indigo as theme colors?"
)
```

Şimdi kodu alalım ve bir HTML dosyasına yazalım!

```python
html_code = fetch_code_from_markdown(res.text)


with open("index.html", "w") as f:
    for block in html_code:
        f.write(block)
```

Şimdi `index.html` dosyasını indirebilir ve sonuçlara göz atabilirsiniz :)

![Llama Paradise HTML](/_astro/llama_paradise.D7N9h-yu_2jOzoG.png)

## Opus 4.1 ile bir ajan (agent) oluşturun

Claude Opus 4.1 kullanarak basit bir hesap makinesi ajanı da oluşturabiliriz

```python
from llama_index.core.agent.workflow import FunctionAgent




def multiply(a: int, b: int) -> int:
    """İki tam sayıyı çarpar ve bir tam sayı döndürür"""
    return a * b




def add(a: int, b: int) -> int:
    """İki tam sayıyı toplar ve bir tam sayı döndürür"""
    return a + b




agent = FunctionAgent(
    name="CalculatorAgent",
    description="Temel aritmetik işlemleri gerçekleştirmek için kullanışlıdır",
    system_prompt="Siz bir hesap makinesi ajanısınız, elinizdeki araçları kullanarak aritmetik işlemleri gerçekleştirmelisiniz.",
    tools=[multiply, add],
    llm=llm,
)
```

Şimdi ajanı çalıştıralım ve bir çarpma işleminin sonucunu alalım:

```python
from llama_index.core.agent.workflow import ToolCall, ToolCallResult


handler = agent.run("What is 60 multiplied by 95?")


async for event in handler.stream_events():
    if isinstance(event, ToolCallResult):
        print(
            f"{event.tool_name} aracının çağrılmasından gelen sonuç:\n\n{event.tool_output}"
        )
    if isinstance(event, ToolCall):
        print(
            f"{event.tool_name} aracı şu argümanlarla çağrılıyor:\n\n{event.tool_kwargs}"
        )


response = await handler


print("Final yanıtı")
print(response)
```

```python
multiply aracı şu argümanlarla çağrılıyor:


{'a': 60, 'b': 95}
multiply aracının çağrılmasından gelen sonuç:


5700
Final yanıtı
60'ın 95 ile çarpımı 5.700 eder.
```

Ayrıca bir toplama işlemi ile çalıştıralım!

```python
from llama_index.core.agent.workflow import ToolCall, ToolCallResult


handler = agent.run("What is 1234 plus 5678?")


async for event in handler.stream_events():
    if isinstance(event, ToolCallResult):
        print(
            f"{event.tool_name} aracının çağrılmasından gelen sonuç:\n\n{event.tool_output}"
        )
    if isinstance(event, ToolCall):
        print(
            f"{event.tool_name} aracı şu argümanlarla çağrılıyor:\n\n{event.tool_kwargs}"
        )


response = await handler


print("Final yanıtı")
print(response)
```

```python
add aracı şu argümanlarla çağrılıyor:


{'a': 1234, 'b': 5678}
add aracının çağrılmasından gelen sonuç:


6912
Final yanıtı
1234 artı 5678 eşittir 6912.
```

Anthropic hakkında daha fazla içerik istiyorsanız, [genel örnek not defterimize](./anthropic.ipynb) göz atmayı unutmayın.
