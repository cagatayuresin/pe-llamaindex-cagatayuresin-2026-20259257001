# Intel GPU Üzerinde IPEX-LLM

[IPEX-LLM](https://github.com/intel-analytics/ipex-llm/), LLM'leri (Büyük Dil Modelleri) Intel CPU ve GPU'larda (örneğin iGPU'lu yerel bilgisayarlar, Arc, Flex ve Max gibi harici GPU'lar) çok düşük gecikmeyle çalıştırmak için kullanılan bir PyTorch kütüphanesidir.

Bu örnek, Intel GPU üzerinde metin oluşturma ve sohbet işlemleri için LlamaIndex'in [ipex-llm](https://github.com/intel-analytics/ipex-llm/) ile nasıl kullanılacağını göstermektedir.


IpexLLM'in tüm örnekleri için [buraya](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-ipex-llm/examples) bakabilirsiniz. Intel GPU üzerinde çalıştırırken, lütfen örnekleri çalıştırırken komut argümanında `-d 'xpu'` veya `-d 'xpu:<cihaz_id>'` belirttiğinizden emin olun.


## Ön Koşulların Kurulumu

Intel GPU'larda IPEX-LLM'den yararlanmak için araç kurulumu ve ortam hazırlığına yönelik birkaç ön koşul adımı vardır.

**Windows kullanıcısıysanız:** [Intel GPU ile Windows'ta IPEX-LLM Kurulum Kılavuzu](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html) sayfasını ziyaret edin ve GPU sürücüsünü güncellemek (isteğe bağlı) ve Conda'yı kurmak için [Ön Koşulların Kurulumu](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html#install-prerequisites) adımlarını izleyin.

**Linux kullanıcısıysanız:** [Intel GPU ile Linux'ta IPEX-LLM Kurulum Kılavuzu](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html) sayfasını ziyaret edin ve GPU sürücüsünü, Intel® oneAPI Base Toolkit 2024.0'ı ve Conda'yı kurmak için [Ön Koşulların Kurulumu](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html#install-prerequisites) adımlarını izleyin.

## llama-index-llms-ipex-llm Kurulumu

Ön koşul kurulumlarından sonra, tüm ön koşulların kurulu olduğu bir conda ortamı oluşturmuş olmalısınız. Conda ortamınızı etkinleştirin ve `llama-index-llms-ipex-llm` paketini şu şekilde kurun:

```bash
conda activate <conda-ortam-adiniz>
pip install llama-index-llms-ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

Bu adım aynı zamanda `ipex-llm` ve bağımlılıklarını da kuracaktır.


Ayrıca `extra-index-url` olarak `https://pytorch-extension.intel.com/release-whl/stable/xpu/cn/` adresini de kullanabilirsiniz.


## Çalışma Zamanı Yapılandırması (Runtime Configuration)

Optimum performans için cihazınıza göre birkaç ortam değişkeni ayarlamanız önerilir:

### Intel Core Ultra Yerleşik GPU'lu Windows Kullanıcıları İçin
Anaconda Prompt içerisinde:

```cmd
set SYCL_CACHE_PERSISTENT=1
set BIGDL_LLM_XMX_DISABLED=1
```

### Intel Arc A-Serisi GPU'lu Linux Kullanıcıları İçin

```bash
# oneAPI ortam değişkenlerini yapılandırın. APT veya çevrimdışı kurulan oneAPI için gerekli adımdır.
# PIP ile kurulan oneAPI için bu adımı atlayın.
source /opt/intel/oneapi/setvars.sh

# Optimum performans için önerilen ortam değişkenleri
export USE_XETLA=OFF
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1
export SYCL_CACHE_PERSISTENT=1
```


Her modelin Intel iGPU/Intel Arc A300-Serisi veya Pro A60 üzerinde ilk kez çalışması birkaç dakika sürebilir (derleme işlemi nedeniyle).


## IpexLLM Kullanımı

`IpexLLM` başlatılırken `device_map="xpu"` ayarının yapılması, LLM modelini Intel GPU üzerine yerleştirecek ve IPEX-LLM optimizasyonlarından yararlanacaktır.

Eğer birden fazla Intel GPU'nuz varsa, `device="xpu:<cihaz_id>"` (0'dan başlayarak) ayarını yapabilirsiniz. Varsayılan olarak `device="xpu"`, `device="xpu:0"`'a eşittir.

```python
from llama_index.llms.ipex_llm import IpexLLM

# İstem formatlama fonksiyonlarını tanımlayın (Zephyr-7b-alpha için)
def completion_to_prompt(completion):
    return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"

def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == "system":
            prompt += f"<|system|>\n{message.content}</s>\n"
        elif message.role == "user":
            prompt += f"<|user|>\n{message.content}</s>\n"
        elif message.role == "assistant":
            prompt += f"<|assistant|>\n{message.content}</s>\n"
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n</s>\n" + prompt
    prompt = prompt + "<|assistant|>\n"
    return prompt

# Modeli yükle
llm = IpexLLM.from_model_id(
    model_name="HuggingFaceH4/zephyr-7b-alpha",
    tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",
    context_window=512,
    max_new_tokens=128,
    generate_kwargs={"do_sample": False},
    completion_to_prompt=completion_to_prompt,
    messages_to_prompt=messages_to_prompt,
    device_map="xpu",
)
```

Artık tamamlama veya sohbet görevlerini normal bir şekilde yürütebilirsiniz:

```python
# Tamamlama
response = llm.complete("Bir zamanlar, ")
print(response.text)

# Akışlı Tamamlama
response_iter = llm.stream_complete("Bir zamanlar küçük bir kız vardı")
for r in response_iter:
    print(r.delta, end="", flush=True)

# Sohbet
from llama_index.core.llms import ChatMessage
message = ChatMessage(role="user", content="Big Bang Teorisi'ni kısaca açıkla")
resp = llm.chat([message])
print(resp)
```

## Düşük Bit Modeli Kaydetme/Yükleme

Orijinal modelden çok daha az disk alanı kaplayan düşük bit versiyonunu kaydedip daha sonra `from_model_id_low_bit` ile yükleyebilirsiniz. Bu hem hız hem de bellek açısından daha verimlidir.

```python
saved_lowbit_model_path = "./zephyr-7b-alpha-low-bit"
# Modeli kaydet
llm._model.save_low_bit(saved_lowbit_model_path)
del llm

# Modeli düşük bit olarak yükle (XPU kullanarak)
llm_lowbit = IpexLLM.from_model_id_low_bit(
    model_name=saved_lowbit_model_path,
    tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",
    context_window=512,
    max_new_tokens=64,
    completion_to_prompt=completion_to_prompt,
    generate_kwargs={"do_sample": False},
    device_map="xpu",
)

# Akışlı tamamlama testi
response_iter = llm_lowbit.stream_complete("Büyük Dil Modeli (LLM) nedir?")
for r in response_iter:
    print(r.delta, end="", flush=True)
```
