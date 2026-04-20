# Databricks

Databricks LLM API'leri ile entegrasyon sağlayın.

## Ön Koşullar

- Databricks model sunum uç noktalarını (serving endpoints) sorgulamak ve bunlara erişmek için [Databricks kişisel erişim belirteci (PAT)](https://docs.databricks.com/en/dev-tools/auth/pat.html).

- Foundation Model API'leri (token başına ödeme) için [desteklenen bir bölgede](https://docs.databricks.com/en/machine-learning/model-serving/model-serving-limits.html#regions) bulunan bir [Databricks çalışma alanı (workspace)](https://docs.databricks.com/en/workspace/index.html).

## Kurulum

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-databricks
```

```python
!pip install llama-index
```

```python
from llama_index.llms.databricks import Databricks
```

    PyTorch, TensorFlow >= 2.0 veya Flax bulunamadı. Modeller kullanılamayacak ve yalnızca tokenizer'lar, yapılandırma ve dosya/veri yardımcı programları kullanılabilecektir.

```bash
export DATABRICKS_TOKEN=<api anahtarınız>
export DATABRICKS_SERVING_ENDPOINT=<api sunum uç noktanız>
```

Alternatif olarak, başlatırken (init) API anahtarınızı ve sunum uç noktanızı LLM'ye geçirebilirsiniz:

```python
llm = Databricks(
    model="databricks-dbrx-instruct",
    api_key="api_anahtarınız",
    api_base="https://[calisma-alaniniz].cloud.databricks.com/serving-endpoints/",
)
```

Kullanılabilir LLM modellerinin bir listesi [burada](https://console.groq.com/docs/models) bulunabilir. (Not: Bağlantı Groq'a yönlendiriyor, orijinal dokümandaki bir hata olabilir).

```python
response = llm.complete("Açık kaynaklı LLM'lerin önemini açıkla")
```

```python
print(response)
```

#### Bir mesaj listesiyle `chat` çağrısı yapın

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

### Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
response = llm.stream_complete("Açık kaynaklı LLM'lerin önemini açıkla")
```

```python
for r in response:
    print(r.delta, end="")
```

`stream_chat` bitiş noktasını kullanma

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```
