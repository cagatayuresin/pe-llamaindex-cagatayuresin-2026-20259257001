# OpenVINO LLM'ler

---
title: OpenVINO LLM'ler
 | LlamaIndex OSS Documentation
---

[OpenVINO™](https://github.com/openvinotoolkit/openvino), yapay zeka çıkarımını (inference) optimize etmek ve dağıtmak için açık kaynaklı bir araç takımıdır. OpenVINO™ Runtime, çeşitli donanım [cihazlarında](https://github.com/openvinotoolkit/openvino?tab=readme-ov-file#supported-hardware-matrix) optimize edilmiş aynı modelin çalıştırılmasını sağlayabilir. Dil + LLM'ler, bilgisayarlı görü, otomatik konuşma tanıma ve daha fazlası gibi kullanım durumlarında derin öğrenme performansınızı hızlandırın.

OpenVINO modelleri, LlamaIndex tarafından sarmalanan `OpenVINOLLM` varlığı aracılığıyla yerel olarak çalıştırılabilir:

Aşağıdaki satırda, bu demo için gerekli paketleri kuruyoruz:

```python
%pip install llama-index-llms-openvino transformers huggingface_hub
```

Kurulumu tamamladığımıza göre biraz deneme yapalım:

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
!pip install llama-index
```

```python
from llama_index.llms.openvino import OpenVINOLLM
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

Modeller, `OpenVINOLLM` yöntemi kullanılarak model parametreleri belirtilerek yüklenebilir.

Intel GPU'nuz varsa, çıkarımı üzerinde çalıştırmak için `device_map="gpu"` belirtebilirsiniz.

```python
ov_config = {
    "PERFORMANCE_HINT": "LATENCY",
    "NUM_STREAMS": "1",
    "CACHE_DIR": "",
}


ov_llm = OpenVINOLLM(
    model_id_or_path="HuggingFaceH4/zephyr-7b-beta",
    context_window=3900,
    max_new_tokens=256,
    model_kwargs={"ov_config": ov_config},
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map="cpu",
)
```

```python
response = ov_llm.complete("Hayatın anlamı nedir?")
print(str(response))
```

### Yerel OpenVINO modeli ile çıkarım

Modelinizi CLI ile OpenVINO IR formatına [dışa aktarmanız](https://github.com/huggingface/optimum-intel?tab=readme-ov-file#export) ve modeli yerel klasörden yüklemeniz mümkündür.

```python
!optimum-cli export openvino --model HuggingFaceH4/zephyr-7b-beta ov_model_dir
```

`--weight-format` kullanarak çıkarım gecikmesini ve model boyutunu azaltmak için 8 veya 4 bitlik ağırlık kuantizasyonu (quantization) uygulanması önerilir:

```python
!optimum-cli export openvino --model HuggingFaceH4/zephyr-7b-beta --weight-format int8 ov_model_dir
```

```python
!optimum-cli export openvino --model HuggingFaceH4/zephyr-7b-beta --weight-format int4 ov_model_dir
```

```python
ov_llm = OpenVINOLLM(
    model_id_or_path="ov_model_dir",
    context_window=3900,
    max_new_tokens=256,
    model_kwargs={"ov_config": ov_config},
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map="gpu",
)
```

Dinamik aktivasyon kuantizasyonu ve KV-cache kuantizasyonu ile ek çıkarım hızı iyileştirmesi elde edebilirsiniz. Bu seçenekler `ov_config` ile aşağıdaki gibi etkinleştirilebilir:

```python
ov_config = {
    "KV_CACHE_PRECISION": "u8",
    "DYNAMIC_QUANTIZATION_GROUP_SIZE": "32",
    "PERFORMANCE_HINT": "LATENCY",
    "NUM_STREAMS": "1",
    "CACHE_DIR": "",
}
```

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = ov_llm.stream_complete("Paul Graham kimdir?")
for r in response:
    print(r.delta, end="")
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage


messages = [
    ChatMessage(
        role="system", content="Sen renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne"),
]
resp = ov_llm.stream_chat(messages)


for r in resp:
    print(r.delta, end="")
```

Daha fazla bilgi için şuralara başvurun:

- [OpenVINO LLM kılavuzu](https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide.html).

- [OpenVINO Dokümantasyonu](https://docs.openvino.ai/2024/home.html).

- [OpenVINO Başlangıç Kılavuzu](https://www.intel.com/content/www/us/en/content-details/819067/openvino-get-started-guide.html).

- [LlamaIndex ile RAG örneği](https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/llm-rag-llamaindex).
