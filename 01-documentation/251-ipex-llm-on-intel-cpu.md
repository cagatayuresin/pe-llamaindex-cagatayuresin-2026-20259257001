# Intel CPU Üzerinde IPEX-LLM

[IPEX-LLM](https://github.com/intel-analytics/ipex-llm/), LLM'leri (Büyük Dil Modelleri) Intel CPU ve GPU'larda (örneğin iGPU'lu yerel bilgisayarlar, Arc, Flex ve Max gibi harici GPU'lar) çok düşük gecikmeyle çalıştırmak için kullanılan bir PyTorch kütüphanesidir.

Bu örnek, Intel CPU üzerinde metin oluşturma ve sohbet işlemleri için LlamaIndex'in [ipex-llm](https://github.com/intel-analytics/ipex-llm/) ile nasıl kullanılacağını göstermektedir.


IpexLLM'in tüm örnekleri için [buraya](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-ipex-llm/examples) bakabilirsiniz. Intel CPU üzerinde çalıştırırken, lütfen örnekleri çalıştırırken komut argümanında `-d 'cpu'` belirttiğinizden emin olun.


## Kurulum

`llama-index-llms-ipex-llm` paketini kurun. Bu işlem aynı zamanda `ipex-llm` ve bağımlılıklarını da kuracaktır.

```bash
%pip install llama-index-llms-ipex-llm
```

Bu örnekte gösterim amacıyla [HuggingFaceH4/zephyr-7b-alpha](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha) modelini kullanacağız. Bu model, `transformers` ve `tokenizers` paketlerinin güncellenmesini gerektirir.

```bash
%pip install -U transformers==4.37.0 tokenizers==0.15.2
```

## İstem Formatlama

Zephyr modelini yüklemeden önce, istemleri formatlamak için `completion_to_prompt` ve `messages_to_prompt` fonksiyonlarını tanımlamanız gerekir. Bu, modelin girdileri doğru bir şekilde yorumlaması için gereklidir.

```python
# Bir dizeyi Zephyr'e özel girdi formatına dönüştürür
def completion_to_prompt(completion):
    return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

# Sohbet mesajları listesini Zephyr'e özel girdi formatına dönüştürür
def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == "system":
            prompt += f"<|system|>\n{message.content}</s>\n"
        elif message.role == "user":
            prompt += f"<|user|>\n{message.content}</s>\n"
        elif message.role == "assistant":
            prompt += f"<|assistant|>\n{message.content}</s>\n"
    
    # Bir sistem istemiyle başladığımızdan emin olun, gerekirse boş ekleyin
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n</s>\n" + prompt
    
    # Son asistan istemini ekleyin
    prompt = prompt + "<|assistant|>\n"
    return prompt
```

## Temel Kullanım

Zephyr modelini `IpexLLM.from_model_id` kullanarak yerel olarak yükleyin. Modeli doğrudan Hugging Face formatında yükleyecek ve çıkarım (inference) için otomatik olarak düşük bit formatına dönüştürecektir.

```python
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*padding_mask.*")

from llama_index.llms.ipex_llm import IpexLLM

llm = IpexLLM.from_model_id(
    model_name="HuggingFaceH4/zephyr-7b-alpha",
    tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",
    context_window=512,
    max_new_tokens=128,
    generate_kwargs={"do_sample": False},
    completion_to_prompt=completion_to_prompt,
    messages_to_prompt=messages_to_prompt,
)
```

Artık yüklenen modeli metin tamamlama ve etkileşimli sohbet için kullanabilirsiniz.

### Metin Tamamlama (Text Completion)

```python
completion_response = llm.complete("Bir zamanlar, ")
print(completion_response.text)
```

### Akışlı Metin Tamamlama (Streaming Text Completion)

```python
response_iter = llm.stream_complete("Bir zamanlar küçük bir kız vardı")
for response in response_iter:
    print(response.delta, end="", flush=True)
```

### Sohbet (Chat)

```python
from llama_index.core.llms import ChatMessage

message = ChatMessage(role="user", content="Big Bang Teorisi'ni kısaca açıkla")
resp = llm.chat([message])
print(resp)
```

### Akışlı Sohbet (Streaming Chat)

```python
message = ChatMessage(role="user", content="Yapay zeka nedir?")
resp = llm.stream_chat([message], max_tokens=256)
for r in resp:
    print(r.delta, end="")
```

## Düşük Bit Modeli Kaydetme/Yükleme

Alternatif olarak, düşük bit modelini bir kez diske kaydedebilir ve daha sonra (hatta farklı makinelerde) yeniden yüklemek için `from_model_id` yerine `from_model_id_low_bit` kullanabilirsiniz. Bu yöntem, düşük bit modelleri orijinal modelden önemli ölçüde daha az disk alanı gerektirdiği için alan tasarrufu sağlar. Ayrıca `from_model_id_low_bit`, model dönüştürme adımını atladığı için hız ve bellek kullanımı açısından `from_model_id`'den daha verimlidir.

Düşük bit modelini kaydetmek için `save_low_bit` fonksiyonunu şu şekilde kullanın:

```python
saved_lowbit_model_path = "./zephyr-7b-alpha-low-bit" # düşük bit modelin kaydedileceği yol
llm._model.save_low_bit(saved_lowbit_model_path)
del llm
```

Modeli kaydedilen yoldan şu şekilde yükleyin:

**Not:** Düşük bit modeli için kaydedilen yol yalnızca modelin kendisini içerir, tokenizer'ları içermez. Her şeyin tek bir yerde olmasını istiyorsanız, tokenizer dosyalarını orijinal modelin dizininden düşük bit modelinin kaydedildiği konuma manuel olarak indirmeniz veya kopyalamanız gerekir.

```python
llm_lowbit = IpexLLM.from_model_id_low_bit(
    model_name=saved_lowbit_model_path,
    tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",
    # tokenizer_name=saved_lowbit_model_path, # tokenizer'ları kayıt yoluna kopyaladıysanız bu şekilde kullanabilirsiniz
    context_window=512,
    max_new_tokens=64,
    completion_to_prompt=completion_to_prompt,
    generate_kwargs={"do_sample": False},
)
```

Yüklenen düşük bit modeliyle akışlı tamamlamayı deneyin:

```python
response_iter = llm_lowbit.stream_complete("Büyük Dil Modeli (LLM) nedir?")
for response in response_iter:
    print(response.delta, end="", flush=True)
```
