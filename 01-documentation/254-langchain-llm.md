# LangChain LLM

---
title: LangChain LLM
 | LlamaIndex OSS Belgeleri
---

```bash
%pip install llama-index-llms-langchain
```

```python
from langchain.llms import OpenAI
```

```python
from llama_index.llms.langchain import LangChainLLM
```

```python
llm = LangChainLLM(llm=OpenAI())
```

```python
response_gen = llm.stream_complete("Hi this is")
```

```python
for delta in response_gen:
    print(delta.delta, end="")
```

```
 a test


Hello! Welcome to the test. What would you like to learn about?
```
