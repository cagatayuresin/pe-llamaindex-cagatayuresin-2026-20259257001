# IPEX arka ucu ile optimize edilmiş Optimum Intel LLM'ler

---
title: IPEX arka ucu ile optimize edilmiş Optimum Intel LLM'ler
 | LlamaIndex OSS Documentation
---

[Optimum Intel](https://github.com/rbrugaro/optimum-intel), [Intel Extension for Pytorch (IPEX)](https://github.com/intel/intel-extension-for-pytorch) optimizasyonlarından yararlanarak Intel mimarilerindeki Hugging Face işlem hatlarını (pipelines) hızlandırır.

Optimum Intel modelleri, LlamaIndex tarafından sarmalanan `OptimumIntelLLM` varlığı aracılığıyla yerel olarak çalıştırılabilir:

Aşağıdaki satırda, bu demo için gerekli paketleri kuruyoruz:

```python
%pip install llama-index-llms-optimum-intel
```

Kurulumu tamamladığımıza göre biraz deneme yapalım:

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
!pip install llama-index
```

```python
from llama_index.llms.optimum_intel import OptimumIntelLLM
```

```python
def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == "system":
            prompt += f"<|system|>\n{message.content}</s>\n"
        elif message.role == "user":
            prompt += f"<|user|>\n{message.content}</s>\n"
        elif message.role == "assistant":
            prompt += f"<|assistant|>\n{message.content}</s>\n"


    # bir sistem istemiyle başladığımızdan emin olun, gerekirse boş ekleyin
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n</s>\n" + prompt


    # son asistan istemini ekle
    prompt = prompt + "<|assistant|>\n"


    return prompt




def completion_to_prompt(completion):
    return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"
```

### Model Yükleme

Modeller, `OptimumIntelLLM` yöntemi kullanılarak model parametreleri belirtilerek yüklenebilir.

```python
oi_llm = OptimumIntelLLM(
    model_name="Intel/neural-chat-7b-v3-3",
    tokenizer_name="Intel/neural-chat-7b-v3-3",
    context_window=3900,
    max_new_tokens=256,
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map="cpu",
)
```

```python
response = oi_llm.complete("Hayatın anlamı nedir?")
print(str(response))
```

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = oi_llm.stream_complete("Rahibe Teresa kimdir?")
for r in response:
    print(r.delta, end="")
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system",
        content="Sen New Orleans'ta küçük bir restoranda çalışan Amerikalı bir şefsin",
    ),
    ChatMessage(role="user", content="Günün yemeği nedir?"),
]
resp = oi_llm.stream_chat(messages)


for r in resp:
    print(r.delta, end="")
```
