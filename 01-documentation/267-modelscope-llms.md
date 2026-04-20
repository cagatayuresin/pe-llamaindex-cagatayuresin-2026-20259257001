# ModelScope LLM'leri

---
title: ModelScope LLM'leri
 | LlamaIndex OSS Belgeleri
---

Bu not defterinde, LlamaIndex'te ModelScope LLM modellerinin nasıl kullanılacağını gösteriyoruz. [ModelScope sitesine](https://www.modelscope.cn/) göz atın.

Bu Not Defterini (Notebook) Colab'da açıyorsanız, LlamaIndex 🦙 ve modelscope'u kurmanız gerekecektir.

```bash
!pip install llama-index-llms-modelscope
```

## Temel Kullanım

```python
import sys
from llama_index.llms.modelscope import ModelScopeLLM


llm = ModelScopeLLM(model_name="qwen/Qwen3-8B", model_revision="master")


rsp = llm.complete("Merhaba, sen kimsin?")
print(rsp)
```

#### Mesaj isteği kullanma

```python
from llama_index.core.base.llms.types import MessageRole, ChatMessage


messages = [
    ChatMessage(
        role=MessageRole.SYSTEM, content="Yardımsever bir asistansın."
    ),
    ChatMessage(role=MessageRole.USER, content="Kek nasıl yapılır?"),
]
resp = llm.chat(messages)
print(resp)
```
