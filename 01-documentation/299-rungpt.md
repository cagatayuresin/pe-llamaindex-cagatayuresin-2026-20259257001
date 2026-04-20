# RunGPT

---
title: RunGPT
 | LlamaIndex OSS Documentation
---

RunGPT; açık kaynaklı, bulut yerlisi, büyük ölçekli çok modlu modeller (LMM'ler) sunan bir çerçevedir. Dağıtılmış bir GPU kümesi üzerinde büyük dil modellerinin dağıtımını ve yönetimini basitleştirmek için tasarlanmıştır. RunGPT, büyük ölçekli çok modlu modelleri optimize etmeye yönelik teknikleri toplamak ve bunları herkes için kullanımı kolay hale getirmek için merkezi ve erişilebilir bir yerde tek duraklı bir çözüm olmayı hedeflemektedir. RunGPT'de; LLaMA, Pythia, StableLM, Vicuna, MOSS gibi bir dizi LLM'yi ve ek olarak MiniGPT-4 ve OpenFlamingo gibi Büyük Çok Modlu Modelleri (LMM'ler) destekledik.

# Kurulum

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-rungpt
```

```python
!pip install llama-index
```

Python ortamınıza `pip install` ile `rungpt` paketini kurmanız gerekir:

```python
!pip install rungpt
```

Başarıyla yüklendikten sonra, RunGPT tarafından desteklenen modeller tek satırlık bir komutla dağıtılabilir. Bu seçenek, hedef dil modelini açık kaynak platformdan indirecek ve onu http veya grpc istekleriyle erişilebilen bir localhost portunda bir servis olarak dağıtacaktır. Bu komutu jupyter not defterinde değil, bunun yerine komut satırında çalıştırmanızı öneririm.

```bash
!rungpt serve decapoda-research/llama-7b-hf --precision fp16 --device_map balanced
```

## Temel Kullanım

#### Bir istem (prompt) ile `complete` fonksiyonunu çağırın

```python
from llama_index.llms.rungpt import RunGptLLM


llm = RunGptLLM()
prompt = "Bir şehirde hangi toplu taşıma araçları mevcut olabilir?"
response = llm.complete(prompt)
```

```python
print(response)
```

```text
İşe gitmek istemiyorum, ne yapmalıyım?
Pazartesi günü bir iş görüşmem var. Profesyonel görünen ama çok sıkıcı veya durağan olmayan ne giyebilirim?
```

#### Bir mesaj listesi ile `chat` fonksiyonunu çağırın

```python
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.rungpt import RunGptLLM


messages = [
    ChatMessage(
        role=MessageRole.USER,
        content="Şimdi benim için biraz matematik yapmanı istiyorum.",
    ),
    ChatMessage(
        role=MessageRole.ASSISTANT, content="Tabii, size yardımcı olmak isterim."
    ),
    ChatMessage(
        role=MessageRole.USER,
        content="Bir doğruyu kaç nokta belirler?",
    ),
]
llm = RunGptLLM()
response = llm.chat(messages=messages, temperature=0.8, max_tokens=15)
```

```python
print(response)
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
prompt = "Bir şehirde hangi toplu taşıma araçları mevcut olabilir?"
response = RunGptLLM().stream_complete(prompt)
for item in response:
    print(item.text)
```

`stream_chat` uç noktasını kullanma

```python
from llama_index.llms.rungpt import RunGptLLM


messages = [
    ChatMessage(
        role=MessageRole.USER,
        content="Şimdi benim için biraz matematik yapmanı istiyorum.",
    ),
    ChatMessage(
        role=MessageRole.ASSISTANT, content="Tabii, size yardımcı olmak isterim."
    ),
    ChatMessage(
        role=MessageRole.USER,
        content="Bir doğruyu kaç nokta belirler?",
    ),
]
response = RunGptLLM().stream_chat(messages=messages)
```

```python
for item in response:
    print(item.message)
```
