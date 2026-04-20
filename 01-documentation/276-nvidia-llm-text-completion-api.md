# NVIDIA LLM Metin Tamamlama API'si

---
title: NVIDIA LLM Metin Tamamlama API'si
 | LlamaIndex OSS Belgeleri
---

`llama-index-llms-nvidia` paketi, aşağıdaki gibi kod tamamlama modelleri için `/completions` API'sini desteklemek üzere `NVIDIA` sınıfını genişletir:

- `bigcode/starcoder2-7b`
- `bigcode/starcoder2-15b`

## Kurulum

```bash
%pip install --upgrade --quiet llama-index-llms-nvidia
```

## Yapılandırma

**Başlamak için:**

1. NVIDIA AI Foundation modellerini barındıran [NVIDIA](https://build.nvidia.com/) üzerinden ücretsiz bir hesap oluşturun.

2. İstediğiniz modeli seçin.

3. Input (Girdi) kısmından Python sekmesini seçin ve `Get API Key` düğmesine tıklayın. Ardından `Generate Key` düğmesine tıklayın.

4. Oluşturulan anahtarı kopyalayın ve NVIDIA\_API\_KEY olarak kaydedin. Buradan itibaren uç noktalara erişiminiz olmalıdır.

```python
import getpass
import os


# os.environ['NVIDIA_API_KEY'] silerek sıfırlayabilirsiniz
if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    print("Geçerli NVIDIA_API_KEY zaten ortamda mevcut. Sıfırlamak için silin.")
else:
    nvapi_key = getpass.getpass("NVAPI Anahtarı (nvapi- ile başlar): ")
    assert nvapi_key.startswith(
        "nvapi-"
    ), f"{nvapi_key[:5]}... geçerli bir anahtar değil"
    os.environ["NVIDIA_API_KEY"] = nvapi_key
```

```python
# llama-parse asenkron-önceliklidir, bir not defterinde asenkron kodu çalıştırmak için nest_asyncio kullanımı gerekir
import nest_asyncio


nest_asyncio.apply()
```

## NVIDIA API Kataloğu ile Çalışma

### `use_chat_completions` bağımsız değişkeninin kullanımı

Sorgu anahtar kelime argümanlarıyla `/chat/completions` veya `/completions` uç noktalarından hangisinin kullanılacağına çağrı başına karar vermek için `None` (varsayılan) olarak ayarlayın.

- `/completions` uç noktasını kullanmak için `False` olarak ayarlayın.
- `/chat/completions` uç noktasını kullanmak için `True` olarak ayarlayın.

```python
from llama_index.llms.nvidia import NVIDIA


llm = NVIDIA(model="bigcode/starcoder2-15b", use_chat_completions=False)
```

### Mevcut modeller

Mevcut metin tamamlama modellerini filtrelemek için `is_chat_model` özelliğini kullanın:

```python
print([model for model in llm.available_models if model.is_chat_model])
```

## NVIDIA NIM'leri ile Çalışma

Barındırılan [NVIDIA NIM'lerine](https://ai.nvidia.com) bağlanmanın yanı sıra, bu bağlayıcı yerel NIM örneklerine bağlanmak için de kullanılabilir. Bu, gerektiğinde uygulamalarınızı yerel ortama taşımanıza yardımcı olur.

Yerel NIM örneklerinin nasıl kurulacağına ilişkin talimatlar için [NVIDIA NIM](https://developer.nvidia.com/nim) sayfasına bakın.

```python
from llama_index.llms.nvidia import NVIDIA


# localhost:8080 üzerinde çalışan bir NIM'e bağlanın
llm = NVIDIA(base_url="http://localhost:8080/v1")
```

### Tamamlama (Complete): `.complete()`

Seçilen modelden bir yanıt almak için `.complete()`/`.acomplete()` (bir dize alır) yöntemini kullanabiliriz.

Bu görev için varsayılan modelimizi kullanalım.

```python
print(llm.complete("# Quicksort yapan fonksiyon:"))
```

Beklendiği gibi, LlamaIndex bir `CompletionResponse` döndürür.

#### Asenkron Tamamlama: `.acomplete()`

Aynı şekilde kullanılabilecek bir asenkron uygulama da mevcuttur!

```python
await llm.acomplete("# Quicksort yapan fonksiyon:")
```

#### Akış (Streaming)

```python
x = llm.stream_complete(prompt="# Python'da dizeyi tersine çevirme:", max_tokens=512)
```

```python
for t in x:
    print(t.delta, end="")
```

#### Asenkron Akış (Async Streaming)

```python
x = await llm.astream_complete(
    prompt="# Python'da tersine çevirme programı:", max_tokens=512
)
```

```python
async for t in x:
    print(t.delta, end="")
```
