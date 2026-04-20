# Hugging Face LLM'leri

[Hugging Face](https://huggingface.co/) üzerindeki LLM'lerle yerel olarak veya Hugging Face’in [Çıkarım Sağlayıcıları (Inference Providers)](https://huggingface.co/docs/inference-providers) aracılığıyla etkileşim kurmanın birçok yolu vardır.
Hugging Face, erişimi sağlamak için birkaç Python paketi sunar ve LlamaIndex bunları `LLM` varlıkları olarak sarar:

- [`transformers`](https://github.com/huggingface/transformers) paketi:
  `llama_index.llms.HuggingFaceLLM` kullanın.
- [`huggingface_hub[inference]`](https://github.com/huggingface/huggingface_hub) tarafından sarılan [Hugging Face Çıkarım Sağlayıcıları](https://huggingface.co/docs/inference-providers):
  `llama_index.llms.HuggingFaceInferenceAPI` kullanın.

Bu ikisinin _birçok_ olası permütasyonu vardır, bu nedenle bu notebook sadece birkaçını detaylandırır.
Örnek olarak Hugging Face'in [Metin Oluşturma (Text Generation) görevini](https://huggingface.co/tasks/text-generation) kullanalım.

Aşağıdaki satırda, bu demo için gerekli paketleri kuruyoruz:

- `transformers[torch]`, `HuggingFaceLLM` için gereklidir.
- `huggingface_hub[inference]`, `HuggingFaceInferenceAPI` için gereklidir.
- Z shell (`zsh`) kullanıyorsanız tırnak işaretleri gereklidir.

```python
%pip install llama-index-llms-huggingface # yerel çıkarım için
%pip install llama-index-llms-huggingface-api # uzaktan çıkarım için
```

```python
!pip install "transformers[torch]" "huggingface_hub[inference]"
```

Eğer bu Notebook'u Colab üzerinde açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```python
!pip install llama-index
```

Artık hazır olduğumuza göre biraz deneme yapalım:

# Hugging Face Hesabını Kurma

Öncelikle bir Hugging Face hesabı oluşturmanız ve bir token almanız gerekir. [Buradan](https://huggingface.co/join) kaydolabilirsiniz. Ardından [buradan](https://huggingface.co/settings/tokens) bir token oluşturmanız gerekecektir.

```sh
export HUGGING_FACE_TOKEN=hf_tokeniniz_buraya
```

```python
import os
from typing import List, Optional

from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

HF_TOKEN: Optional[str] = os.getenv("HUGGING_FACE_TOKEN")
# NOT: Varsayılan olarak None atanması, bu token HuggingFaceInferenceAPI 
# içinde kullanıldığında Hugging Face'in token deposuna geri dönecektir.
```

## Çıkarım Sağlayıcıları (Inference Providers) aracılığıyla bir model kullanma

Açık kaynaklı bir modeli kullanmanın en kolay yolu, Hugging Face [Çıkarım Sağlayıcılarını (Inference Providers)](https://huggingface.co/docs/inference-providers) kullanmaktır. Karmaşık görevler için harika olan DeepSeek R1 modelini kullanalım.

Çıkarım sağlayıcıları ile modeli, sunucusuz (serverless) altyapı üzerinde çalıştırabilirsiniz.

```python
remotely_run = HuggingFaceInferenceAPI(
    model_name="deepseek-ai/DeepSeek-R1-0528",
    token=HF_TOKEN,
    provider="auto",  # bu, mevcut en iyi sağlayıcıyı kullanacaktır
)
```

Tercih ettiğimiz çıkarım sağlayıcısını da belirtebiliriz. [`together` sağlayıcısını](https://huggingface.co/togethercomputer) kullanalım.

```python
remotely_run = HuggingFaceInferenceAPI(
    model_name="Qwen/Qwen3-235B-A22B",
    token=HF_TOKEN,
    provider="together",  # bu, mevcut en iyi sağlayıcıyı kullanacaktır
)
```

## Açık kaynaklı bir modeli yerel olarak kullanma

İlk olarak, yerel çıkarım için optimize edilmiş açık kaynaklı bir model kullanacağız. Bu model (ilk çağrıda) yerel Hugging Face model önbelleğine indirilir ve modeli aslında yerel makinenizin donanımı üzerinde çalıştırır.

Yerel çıkarım için optimize edilmiş olan [Gemma 3N E4B](https://huggingface.co/google/gemma-3n-E4B-it) modelini kullanacağız.

```python
locally_run = HuggingFaceLLM(model_name="google/gemma-3n-E4B-it")
```

## Özel bir Çıkarım Uç Noktası (Inference Endpoint) kullanma

Bir model için özel bir Çıkarım Uç Noktası oluşturabilir ve modeli çalıştırmak için bunu kullanabiliriz.

```python
endpoint_server = HuggingFaceInferenceAPI(
    model="https://(<uç-noktanız>.eu-west-1.aws.endpoints.huggingface.cloud"
)
```

## Yerel bir çıkarım motoru (vLLM veya TGI) kullanma

Modeli çalıştırmak için [vLLM](https://github.com/vllm-project/vllm) veya [TGI](https://github.com/huggingface/text-generation-inference) gibi yerel bir çıkarım motoru da kullanabiliriz.

```python
# Yerel veya uzak bir Metin Oluşturma Çıkarımı (Text Generation Inference) 
# sunucusu tarafından sunulan bir modele de bağlanabilirsiniz.
tgi_server = HuggingFaceInferenceAPI(model="http://localhost:8080")
```

`HuggingFaceInferenceAPI` ile yapılan bir tamamlamanın (completion) temelinde Hugging Face'in [Metin Oluşturma (Text Generation) görevi](https://huggingface.co/tasks/text-generation) yatar.

```python
completion_response = remotely_run_recommended.complete("To infinity, and")
print(completion_response)
```

      beyond! (Sonsuzluğa ve ötesine!)
    The Infinity Wall Clock is a unique and stylish way to keep track of time...

## Bir tokenizer ayarlama

LLM'i değiştiriyorsanız, eşleşmesi için genel tokenizer'ı da değiştirmelisiniz!

```python
from llama_index.core import set_global_tokenizer
from transformers import AutoTokenizer

set_global_tokenizer(
    AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-alpha").encode
)
```

Merak ediyorsanız, sarılmış diğer Hugging Face Çıkarım API'si görevleri şunlardır:

- `llama_index.llms.HuggingFaceInferenceAPI.chat`: [Sohbet (Conversational) görevi](https://huggingface.co/tasks/conversational)
- `llama_index.embeddings.HuggingFaceInferenceAPIEmbedding`: [Özellik Çıkarımı (Feature Extraction) görevi](https://huggingface.co/tasks/feature-extraction)

Ve evet, Hugging Face gömme (embedding) modelleri şunlarla desteklenir:

- `transformers[torch]`: `HuggingFaceEmbedding` tarafından sarılmıştır.
- `huggingface_hub[inference]`: `HuggingFaceInferenceAPIEmbedding` tarafından sarılmıştır.

Yukarıdaki her ikisi de `llama_index.embeddings.base.BaseEmbedding` sınıfından türetilmiştir.