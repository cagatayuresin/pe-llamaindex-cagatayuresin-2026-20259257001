# LLM'leri Bağımsız Modüller Olarak Kullanma (Using LLMs as standalone modules)

LLM modüllerimizi tek başlarına kullanabilirsiniz.

## Metin Tamamlama Örneği (Text Completion Example)

```python
from llama_index.llms.openai import OpenAI

# akışsız (non-streaming)
completion = OpenAI().complete("Paul Graham şöyledir: ")
print(completion)

# akışlı (streaming) uç noktayı kullanma
from llama_index.llms.openai import OpenAI

llm = OpenAI()
completions = llm.stream_complete("Paul Graham şöyledir: ")
for completion in completions:
    print(completion.delta, end="")
```

## Sohbet Örneği (Chat Example)

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = OpenAI().chat(messages)
print(resp)
```

Her bir LLM için kullanım kılavuzlarına [modüller bölümümüzden](/python/framework/module_guides/models/llms/modules) göz atabilirsiniz.