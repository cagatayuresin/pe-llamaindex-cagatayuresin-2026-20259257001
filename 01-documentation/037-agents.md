# Ajanlar (Agents)

LlamaIndex'te bir ajan oluşturmak, bir dizi araç (tools) tanımlayarak ve bunları ReActAgent veya FunctionAgent uygulamalarımıza sağlayarak yapılabilir. Burada OpenAI ile kullanıyoruz, ancak yeterince yetenekli herhangi bir LLM ile de kullanılabilir.

Genel olarak; API'larında yerleşik fonksiyon çağırma/araçlar (function calling/tools) bulunan Openai, Anthropic, Gemini vb. LLM'ler için FunctionAgent tercih edilmelidir.

```python
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import ReActAgent, FunctionAgent


# örnek bir Araç (Tool) tanımlayın
def multiply(a: int, b: int) -> int:
    """İki tamsayıyı çarpar ve sonuç tamsayıyı döndürür"""
    return a * b


# llm'i başlatın
llm = OpenAI(model="gpt-4o")

# ajanı başlatın
agent = FunctionAgent(
    tools=[multiply],
    system_prompt="Siz, kullanıcıya yardımcı olurken çarpma işlemi için bir aracı çağırabilen bir ajansınız.",
)
```

Bu araçlar yukarıda gösterildiği gibi Python fonksiyonları olabilir veya LlamaIndex sorgu motorları (query engines) olabilirler:

```python
from llama_index.core.tools import QueryEngineTool

query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=sql_agent,
        name="sql_agent",
        description="SQL sorgularını yürütebilen ajan.",
    ),
]

agent = FunctionAgent(
    tools=query_engine_tools,
    system_prompt="Siz, metinden SQL'e (text-to-SQL) yürütme için bir ajanı çağırabilen bir ajansınız.",
)
```

Daha fazlasını [Ajan Modülü Kılavuzumuzda](/python/framework/module_guides/deploying/agents) veya [uçtan uca ajan eğitimimizde](/python/framework/understanding/agent) öğrenebilirsiniz.