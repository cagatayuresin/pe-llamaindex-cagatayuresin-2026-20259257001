# Intel GPU üzerinde IPEX-LLM ile Yerel (Local) Embedding'ler

> [IPEX-LLM](https://github.com/intel-analytics/ipex-llm/), Intel CPU ve GPU'larda (örneğin iGPU'lu yerel PC, Arc, Flex ve Max gibi ayrık GPU'lar) LLM'leri çok düşük gecikmeyle çalıştırmak için geliştirilmiş bir PyTorch kütüphanesidir.

Bu örnek, Intel GPU üzerinde `ipex-llm` optimizasyonları ile embedding görevlerini yürütmek için LlamaIndex'in nasıl kullanılacağını gösterir. Bu, RAG, döküman bazlı soru-cevap vb. uygulamalarda yardımcı olacaktır.

> **Not**
>
> `IpexLLMEmbedding`'in tam örnekleri için [buraya](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/embeddings/llama-index-embeddings-ipex-llm/examples) bakabilirsiniz. Intel GPU üzerinde çalıştırmak için, örnekleri yürütürken komut argümanında lütfen `-d 'xpu'` veya `-d 'xpu:<cihaz_id>'` belirttiğinizden emin olun.

## Ön Koşulların Kurulumu

Intel GPU'larda IPEX-LLM'den yararlanmak için araç kurulumu ve ortam hazırlığına yönelik birkaç ön koşul adımı vardır.

Bir Windows kullanıcısıysanız, [Intel GPU ile Windows'ta IPEX-LLM Kurulum Kılavuzu](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html) sayfasını ziyaret edin ve GPU sürücüsünü güncellemek (isteğe bağlı) ve Conda'yı kurmak için [**Ön Koşulları Kur**](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html#install-prerequisites) bölümünü izleyin.

Bir Linux kullanıcısıysanız, [Intel GPU ile Linux'ta IPEX-LLM Kurulumu](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html) sayfasını ziyaret edin ve GPU sürücüsünü, Intel® oneAPI Base Toolkit 2024.0'ı ve Conda'yı kurmak için [**Ön Koşulları Kur**](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html#install-prerequisites) bölümünü izleyin.

## `llama-index-embeddings-ipex-llm` Kurulumu

Ön koşul kurulumlarından sonra, tüm ön koşulların kurulu olduğu bir conda ortamı oluşturmuş olmalısınız; conda ortamınızı etkinleştirin ve `llama-index-embeddings-ipex-llm` paketini aşağıdaki gibi kurun:

```bash
conda activate <conda-ortam-adiniz>

pip install llama-index-embeddings-ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

Bu adım ayrıca `ipex-llm` ve bağımlılıklarını da kuracaktır.

> **Not**
>
> `extra-index-url` olarak `https://pytorch-extension.intel.com/release-whl/stable/xpu/cn/` adresini de kullanabilirsiniz.

## Çalışma Zamanı Yapılandırması (Runtime Configuration)

Optimal performans için cihazınıza bağlı olarak birkaç ortam değişkeni ayarlamanız önerilir:

### Intel Core Ultra entegre GPU'ya sahip Windows Kullanıcıları için

Anaconda Komut Satırı'nda:

```
set SYCL_CACHE_PERSISTENT=1
set BIGDL_LLM_XMX_DISABLED=1
```

### Intel Arc A-Serisi GPU'ya sahip Linux Kullanıcıları için

```bash
# oneAPI ortam değişkenlerini yapılandırın. APT veya çevrimdışı kurulu bir oneAPI için gerekli adımdır.
# Ortam zaten LD_LIBRARY_PATH içinde yapılandırıldığı için PIP ile kurulan oneAPI için bu adımı atlayın.
source /opt/intel/oneapi/setvars.sh

# Optimal performans için önerilen Ortam Değişkenleri
export USE_XETLA=OFF
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1
export SYCL_CACHE_PERSISTENT=1
```

> **Not**
>
> Her modelin Intel iGPU/Intel Arc A300-Serisi veya Pro A60 üzerinde ilk kez çalışması sırasında derleme işlemi birkaç dakika sürebilir.
>
> Diğer GPU türleri için Windows kullanıcıları [buraya](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#runtime-configuration), Linux kullanıcıları ise [buraya](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#id5) bakabilir.

## `IpexLLMEmbedding`

`IpexLLMEmbedding` başlatılırken `device="xpu"` ayarının yapılması, embedding modelini Intel GPU'ya yerleştirecek ve IPEX-LLM optimizasyonlarından yararlanacaktır:

```python
from llama_index.embeddings.ipex_llm import IpexLLMEmbedding

embedding_model = IpexLLMEmbedding(
    model_name="BAAI/bge-large-en-v1.5", device="xpu"
)
```

> Lütfen `IpexLLMEmbedding`'in şu anda yalnızca Hugging Face Bge modelleri için optimizasyon sağladığını unutmayın.
>
> Mevcut birden fazla Intel GPU'nuz varsa, `device="xpu:<cihaz_id>"` ayarını yapabilirsiniz; burada `cihaz_id` 0'dan başlar. Varsayılan olarak `device="xpu"`, `device="xpu:0"` ile eşdeğerdir.

Ardından embedding görevlerini normal şekilde yürütebilirsiniz:

```python
sentence = "IPEX-LLM, Intel CPU ve GPU'larda (örneğin iGPU'lu yerel PC, Arc, Flex ve Max gibi ayrık GPU'lar) LLM'leri çok düşük gecikmeyle çalıştırmak için geliştirilmiş bir PyTorch kütüphanesidir."
query = "IPEX-LLM nedir?"

text_embedding = embedding_model.get_text_embedding(sentence)
print(f"embedding[:10]: {text_embedding[:10]}")

text_embeddings = embedding_model.get_text_embedding_batch([sentence, query])
print(f"text_embeddings[0][:10]: {text_embeddings[0][:10]}")
print(f"text_embeddings[1][:10]: {text_embeddings[1][:10]}")

query_embedding = embedding_model.get_query_embedding(query)
print(f"query_embedding[:10]: {query_embedding[:10]}")
```