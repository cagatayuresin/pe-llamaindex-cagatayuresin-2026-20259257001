# OpenVINO GenAI LLM'ler

---
title: OpenVINO GenAI LLM'ler
 | LlamaIndex OSS Documentation
---

[OpenVINO™](https://github.com/openvinotoolkit/openvino), yapay zeka çıkarımını (inference) optimize etmek ve dağıtmak için açık kaynaklı bir araç takımıdır. OpenVINO™ Runtime, çeşitli donanım [cihazlarında](https://github.com/openvinotoolkit/openvino?tab=readme-ov-file#supported-hardware-matrix) optimize edilmiş aynı modelin çalıştırılmasını sağlayabilir. Dil + LLM'ler, bilgisayarlı görü, otomatik konuşma tanıma ve daha fazlası gibi kullanım durumlarında derin öğrenme performansınızı hızlandırın.

`OpenVINOGenAILLM`, [OpenVINO-GenAI API](https://github.com/openvinotoolkit/openvino.genai)'nin bir sarmalayıcısıdır. OpenVINO modelleri, LlamaIndex tarafından sarmalanan bu varlık aracılığıyla yerel olarak çalıştırılabilir:

Aşağıdaki satırda, bu demo için gerekli paketleri kuruyoruz:

```python
%pip install llama-index-llms-openvino-genai
```

```python
%pip install optimum[openvino]
```

Kurulumu tamamladığımıza göre biraz deneme yapalım:

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
!pip install llama-index
```

```python
from llama_index.llms.openvino_genai import OpenVINOGenAILLM
```

```python
/home2/ethan/intel/llama_index/llama_test/lib/python3.10/site-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_path" in OpenVINOGenAILLM has conflict with protected namespace "model_".


You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`.
  warnings.warn(
```

### Model Dışa Aktarma

Modelinizi CLI ile OpenVINO IR formatına [dışa aktarmanız](https://github.com/huggingface/optimum-intel?tab=readme-ov-file#export) ve modeli yerel klasörden yüklemeniz mümkündür.

```python
!optimum-cli export openvino --model microsoft/Phi-3-mini-4k-instruct --task text-generation-with-past --weight-format int4 model_path
```

Hugging Face'in OpenVINO model merkezinden optimize edilmiş bir IR modeli indirebilirsiniz.

```python
import huggingface_hub as hf_hub


model_id = "OpenVINO/Phi-3-mini-4k-instruct-int4-ov"
model_path = "Phi-3-mini-4k-instruct-int4-ov"


hf_hub.snapshot_download(model_id, local_dir=model_path)
```

```python
Fetching 17 files:   0%|          | 0/17 [00:00<?, ?it/s]










'/home2/ethan/intel/llama_index/docs/examples/llm/Phi-3-mini-4k-instruct-int4-ov'
```

### Model Yükleme

Modeller, `OpenVINOGenAILLM` yöntemi kullanılarak model parametreleri belirtilerek yüklenebilir.

Intel GPU'nuz varsa, çıkarımı üzerinde çalıştırmak için `device="gpu"` belirtebilirsiniz.

```python
ov_llm = OpenVINOGenAILLM(
    model_path=model_path,
    device="CPU",
)
```

Üretim yapılandırma parametrelerini `ov_llm.config` aracılığıyla geçirebilirsiniz. Desteklenen parametreler [openvino_genai.GenerationConfig](https://docs.openvino.ai/2024/api/genai_api/_autosummary/openvino_genai.GenerationConfig.html) adresinde listelenmiştir.

```python
ov_llm.config.max_new_tokens = 100
```

```python
response = ov_llm.complete("Hayatın anlamı nedir?")
print(str(response))
```

```python
# Yanıt
Hayatın anlamı, tarih boyunca filozoflar, ilahiyatçılar, bilim insanları ve düşünürler tarafından tartışılan derin ve karmaşık bir sorudur. Farklı kültürlerin, dinlerin ve bireylerin, hayatın amacına ve önemine dair kendi yorumları ve inançları vardır.

Felsefi bir bakış açısıyla, Jean-Paul Sartre ve Albert Camus gibi varoluşçular hayatın özünde hiçbir anlamı olmadığını ve bunun...
```

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = ov_llm.stream_complete("Paul Graham kimdir?")
for r in response:
    print(r.delta, end="")
```

```python
Paul Graham, startup hızlandırma programı Y Combinator'ı kurmasıyla tanınan bir bilgisayar bilimcisi ve girişimcidir. Ayrıca 1998'de Yahoo tarafından 497 milyon dolara satın alınan Viaweb adlı web geliştirme şirketinin de kurucusudur.

Y Combinator nedir?

Y Combinator, erken aşamadaki girişimlere finansman, mentorluk ve kaynak sağlayan bir startup hızlandırma programıdır.
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

```python
Ben Phi, Microsoft'un yapay zeka asistanıyım. Bugün size nasıl yardımcı olabilirim?
```

Daha fazla bilgi için şuralara başvurun:

- [OpenVINO LLM kılavuzu](https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide.html).

- [OpenVINO Dokümantasyonu](https://docs.openvino.ai/2024/home.html).

- [OpenVINO Başlangıç Kılavuzu](https://www.intel.com/content/www/us/en/content-details/819067/openvino-get-started-guide.html).

- [LlamaIndex ile RAG örneği](https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/llm-rag-llamaindex).
