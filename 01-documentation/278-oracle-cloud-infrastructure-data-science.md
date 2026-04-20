# Oracle Cloud Infrastructure Veri Bilimi (Data Science)

---
title: Oracle Cloud Infrastructure Veri Bilimi (Data Science) 
 | LlamaIndex OSS Belgeleri
---

Oracle Cloud Infrastructure [(OCI) Data Science](https://www.oracle.com/artificial-intelligence/data-science), veri bilimi ekiplerinin Oracle Cloud Infrastructure'da makine öğrenimi modelleri oluşturması, eğitmesi ve yönetmesi için tam olarak yönetilen, sunucusuz bir platformdur.

OCI Data Science'da temel LLM modellerini dağıtmak, değerlendirmek ve ince ayar yapmak (fine-tune) için kullanılabilecek [AI Quick Actions](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm) özelliğini sunar. AI Quick Actions, yapay zekanın yeteneklerinden hızla yararlanmak isteyen kullanıcıları hedefler. Temel modellerle çalışmak için basitleştirilmiş, kodsuz ve verimli bir ortam sağlayarak temel modellerin erişimini daha geniş bir kullanıcı kitlesine yaymayı amaçlarlar. AI Quick Actions'a Veri Bilimi Not Defteri'nden (Data Science Notebook) erişilebilir.

AI Quick Actions kullanılarak OCI Data Science'da LLM modellerinin nasıl dağıtılacağına ilişkin ayrıntılı belgelere [buradan](https://github.com/oracle-samples/oci-data-science-ai-samples/blob/main/ai-quick-actions/model-deployment-tips.md) ve [buradan](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm) ulaşılabilir.

Bu not defteri, OCI'nın Data Science modellerinin LlamaIndex ile nasıl kullanılacağını açıklar.

## Kurulum

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-oci-data-science
```

```bash
!pip install llama-index
```

Ayrıca [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) SDK'sını da kurmanız gerekecektir.

```bash
!pip install -U oracle-ads
```

## Kimlik Doğrulama

LlamaIndex için desteklenen kimlik doğrulama yöntemleri, diğer OCI hizmetleriyle kullanılanlarla eşdeğerdir ve standart SDK kimlik doğrulama yöntemlerini (özellikle API Anahtarı, oturum belirteci, örnek sorumlusu - instance principal ve kaynak sorumlusu - resource principal) takip eder. Daha fazla ayrıntıya [buradan](https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html) ulaşabilirsiniz. OCI Data Science Model Dağıtım uç noktasına erişmek için gerekli [politikalara](https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm) sahip olduğunuzdan emin olun. [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) kütüphanesi, OCI Data Science içindeki kimlik doğrulamasını basitleştirmeye yardımcı olur.

## Temel Kullanım

OCI Data Science AI tarafından sunulan LLM'leri LlamaIndex ile kullanmak için sadece `OCIDataScience` arayüzünü Veri Bilimi Model Dağıtım uç noktanız ve model kimliğinizle başlatmanız yeterlidir. Varsayılan olarak AI Quick Actions'daki tüm dağıtılmış modeller `odsc-model` kimliğini alır. Ancak bu kimlik dağıtım sırasında değiştirilebilir.

#### Bir istem (prompt) ile `complete` çağrısı

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)
response = llm.complete("Bana bir fıkra anlat")


print(response)
```

### Bir mesaj listesiyle `chat` çağrısı

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.base.llms.types import ChatMessage


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)
response = llm.chat(
    [
        ChatMessage(role="user", content="Bana bir fıkra anlat"),
        ChatMessage(
            role="assistant", content="Tavuk neden yolun karşısına geçti?"
        ),
        ChatMessage(role="user", content="Bilmiyorum, neden?"),
    ]
)


print(response)
```

## Akış (Streaming)

**Özel Akış (Streaming) uç noktasını kullanma**

```python
from llama_index.llms.oci_data_science import OCIDataScience
import ads


ads.set_auth(auth="security_token", profile="OC1")


llm = OCIDataScience(
    endpoint="https://<MD_OCID>/predictWithResponseStream",
    model="odsc-llm",
)


prompt = "Fransa'nın başkenti neresidir?"
response = llm.stream_complete(prompt)
for chunk in response:
    print(chunk.delta, end="")
```

### `stream_complete` uç noktasını kullanma

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)


for chunk in llm.stream_complete("Bana bir fıkra anlat"):
    print(chunk.delta, end="")
```

### `stream_chat` uç noktasını kullanma

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.base.llms.types import ChatMessage


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)
response = llm.stream_chat(
    [
        ChatMessage(role="user", content="Bana bir fıkra anlat"),
        ChatMessage(
            role="assistant", content="Tavuk neden yolun karşısına geçti?"
        ),
        ChatMessage(role="user", content="Bilmiyorum, neden?"),
    ]
)


for chunk in response:
    print(chunk.delta, end="")
```

## Asenkron (Async)

### Bir istem ile `acomplete` çağrısı

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)
response = await llm.acomplete("Bana bir fıkra anlat")


print(response)
```

### Bir mesaj listesiyle `achat` çağrısı

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.base.llms.types import ChatMessage


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)
response = await llm.achat(
    [
        ChatMessage(role="user", content="Bana bir fıkra anlat"),
        ChatMessage(
            role="assistant", content="Tavuk neden yolun karşısına geçti?"
        ),
        ChatMessage(role="user", content="Bilmiyorum, neden?"),
    ]
)


print(response)
```

### `astream_complete` uç noktasını kullanma

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)


async for chunk in await llm.astream_complete("Bana bir fıkra anlat"):
    print(chunk.delta, end="")
```

### `astream_chat` uç noktasını kullanma

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.base.llms.types import ChatMessage


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
)
response = await llm.stream_chat(
    [
        ChatMessage(role="user", content="Bana bir fıkra anlat"),
        ChatMessage(
            role="assistant", content="Tavuk neden yolun karşısına geçti?"
        ),
        ChatMessage(role="user", content="Bilmiyorum, neden?"),
    ]
)


async for chunk in response:
    print(chunk.delta, end="")
```

## Modeli Yapılandırma

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
    temperature=0.2,
    max_tokens=500,
    timeout=120,
    context_window=2500,
    additional_kwargs={
        "top_p": 0.75,
        "logprobs": True,
        "top_logprobs": 3,
    },
)
response = llm.chat(
    [
        ChatMessage(role="user", content="Bana bir fıkra anlat."),
    ]
)
print(response)
```

## Fonksiyon Çağırma (Function Calling)

[AI Quick Actions](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm), büyük bir dil modelini dağıtmayı ve sunmayı çok kolaylaştıran önceden oluşturulmuş hizmet konteynerleri sunar. Modeli barındırmak için hizmet konteynerinde vLLM (LLM'ler için yüksek verimli ve bellek verimli bir çıkarım ve sunum motoru) veya TGI (popüler açık kaynaklı LLM'ler için yüksek performanslı bir metin oluşturma sunucusu) kullanılır, oluşturulan uç nokta OpenAI API protokolünü destekler. Bu, model dağıtımının OpenAI API kullanan uygulamalar için bir drop-in (doğrudan) ikame olarak kullanılmasına olanak tanır. Dağıtılan model fonksiyon çağırmayı destekliyorsa, LlamaIndex araçlarıyla entegrasyon, LLM üzerindeki `predict_and_call` fonksiyonu aracılığıyla herhangi bir aracın eklenmesine ve hangi araçların çağrılacağına LLM'nin karar vermesine olanak tanır.

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.tools import FunctionTool


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
    temperature=0.2,
    max_tokens=500,
    timeout=120,
    context_window=2500,
    additional_kwargs={
        "top_p": 0.75,
        "logprobs": True,
        "top_logprobs": 3,
    },
)




def multiply(a: float, b: float) -> float:
    print(f"---> {a} * {b}")
    return a * b




def add(a: float, b: float) -> float:
    print(f"---> {a} + {b}")
    return a + b




def subtract(a: float, b: float) -> float:
    print(f"---> {a} - {b}")
    return a - b




def divide(a: float, b: float) -> float:
    print(f"---> {a} / {b}")
    return a / b




multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
sub_tool = FunctionTool.from_defaults(fn=subtract)
divide_tool = FunctionTool.from_defaults(fn=divide)


response = llm.predict_and_call(
    [multiply_tool, add_tool, sub_tool, divide_tool],
    user_msg="`8 + 2 - 6` işleminin sonucunu hesapla.",
    verbose=True,
)


print(response)
```

### `FunctionAgent` Kullanımı

```python
import ads
from llama_index.llms.oci_data_science import OCIDataScience
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent


ads.set_auth(auth="security_token", profile="<profilinizle-değiştirin>")


llm = OCIDataScience(
    model="odsc-llm",
    endpoint="https://<MD_OCID>/predict",
    temperature=0.2,
    max_tokens=500,
    timeout=120,
    context_window=2500,
    additional_kwargs={
        "top_p": 0.75,
        "logprobs": True,
        "top_logprobs": 3,
    },
)




def multiply(a: float, b: float) -> float:
    print(f"---> {a} * {b}")
    return a * b




def add(a: float, b: float) -> float:
    print(f"---> {a} + {b}")
    return a + b




def subtract(a: float, b: float) -> float:
    print(f"---> {a} - {b}")
    return a - b




def divide(a: float, b: float) -> float:
    print(f"---> {a} / {b}")
    return a / b




multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
sub_tool = FunctionTool.from_defaults(fn=subtract)
divide_tool = FunctionTool.from_defaults(fn=divide)


agent = FunctionAgent(
    tools=[multiply_tool, add_tool, sub_tool, divide_tool],
    llm=llm,
)
response = await agent.run(
    "`8 + 2 - 6` işleminin sonucunu hesapla. Araçları kullan. Hesaplanan sonucu döndür."
)


print(response)
```
