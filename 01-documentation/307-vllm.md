# vLLM

---
title: vLLM
 | LlamaIndex OSS Documentation
---

vLLM'i kullanmanın yerel (local) ve uzak (remote) olmak üzere iki modu vardır. Yerel olarak kullanılabilir bir CUDA ortamı gerektiren ilk moddan başlayalım.

### vLLM'i Yükleme

`pip install vllm`\
veya kendiniz derlemek isterseniz [kaynaktan derleyebilirsiniz](https://docs.vllm.ai/en/latest/getting_started/installation.html).

### Orca-7b Tamamlama Örneği (Completion Example)

```python
%pip install llama-index-llms-vllm
```

```python
import os


os.environ["HF_HOME"] = "model/"
```

```python
from llama_index.llms.vllm import Vllm, VllmServer
```

```python
llm = Vllm(
    model="microsoft/Orca-2-7b",
    tensor_parallel_size=4,
    max_new_tokens=100,
    vllm_kwargs={"swap_space": 1, "gpu_memory_utilization": 0.5},
)
```

```python
llm.complete("[INST]Yardımsever bir asistansın[/INST] Kara delik nedir?")
```

### LLama-2-7b Tamamlama Örneği (Completion Example)

```python
llm = Vllm(
    model="codellama/CodeLlama-7b-hf",
    dtype="float16",
    tensor_parallel_size=4,
    temperature=0,
    max_new_tokens=100,
    vllm_kwargs={
        "swap_space": 1,
        "gpu_memory_utilization": 0.5,
        "max_model_len": 4096,
    },
)
```

```python
llm.complete("import socket\n\ndef ping_exponential_backoff(host: str):")
```

### Mistral chat 7b Tamamlama Örneği (Completion Example)

```python
llm = Vllm(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    dtype="float16",
    tensor_parallel_size=4,
    temperature=0,
    max_new_tokens=100,
    vllm_kwargs={
        "swap_space": 1,
        "gpu_memory_utilization": 0.5,
        "max_model_len": 4096,
    },
)
```

```text
vLLM mock başlatıldı
```

```python
llm.complete(" Kara delik nedir?")
```

# vLLM'i HTTP Üzerinden Çağırma

Bu modda `vllm` modelini yüklemeye veya yerel olarak CUDA'ya sahip olmaya gerek yoktur. vLLM API-sini kurmak için [buradaki](https://docs.vllm.ai/en/latest/serving/distributed_serving.html) kılavuzu takip edebilirsiniz. Not: `llama-index-llms-vllm` modülü, yalnızca [bir demo](https://github.com/vllm-project/vllm/blob/abfc4f3387c436d46d6701e9ba916de8f9ed9329/vllm/entrypoints/api_server.py#L2) olan `vllm.entrypoints.api_server` için bir istemcidir.\
Eğer vLLM sunucusu [OpenAI Uyumlu Sunucu](https://docs.vllm.ai/en/latest/getting_started/quickstart.html#openai-compatible-server) olarak `vllm.entrypoints.openai.api_server` ile veya [Docker](https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html) aracılığıyla başlatıldıysa, `llama-index-llms-openai-like` [modülünden](localai.ipynb#llamaindex-interaction) `OpenAILike` sınıfına ihtiyacınız olacaktır.

### Tamamlama Yanıtı (Completion Response)

```python
from llama_index.core.llms import ChatMessage
```

```python
llm = VllmServer(
    api_url="http://localhost:8000/generate", max_new_tokens=100, temperature=0
)
```

```python
llm.complete("kara delik nedir?")
```

```python
message = [ChatMessage(content="merhaba", role="user")]
llm.chat(message)
```

### Akışlı Yanıt (Streaming Response)

```python
list(llm.stream_complete("kara delik nedir"))[-1]
```

```python
message = [ChatMessage(content="kara delik nedir", role="user")]
[x for x in llm.stream_chat(message)][-1]
```

### Asenkron Yanıt (Async Response)

```python
import asyncio


await llm.acomplete("Kara delik nedir")
```

```python
await llm.achat(message)
```

```python
[x async for x in await llm.astream_complete("kara delik nedir")][-1]
```

```python
[x async for x in await llm.astream_chat(message)][-1]
```
