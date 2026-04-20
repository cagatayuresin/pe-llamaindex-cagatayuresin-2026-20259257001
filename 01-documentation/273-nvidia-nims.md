# NVIDIA NIM'leri

---
title: NVIDIA NIM'leri
 | LlamaIndex OSS Belgeleri
---

`llama-index-llms-nvidia` paketi, [NVIDIA AI Foundation Modelleri](https://www.nvidia.com/en-us/ai-data-science/foundation-models/) tarafından desteklenen ve [NVIDIA API Kataloğu](https://build.nvidia.com/) üzerinde barındırılan sohbet modelleri ve eşlemeler (embeddings) için LlamaIndex entegrasyonlarını içerir. NVIDIA AI Foundation modelleri, NVIDIA tarafından hızlandırılmış altyapıda en iyi performansı sunmak üzere optimize edilmiş, topluluk ve NVIDIA yapımı modellerdir. DGX üzerinde barındırılan bulut bilişim ortamından hızlı sonuçlar almak için NVIDIA API Kataloğu'ndaki canlı uç noktaları sorgulayabilir veya NVIDIA AI Enterprise lisansına dahil olan NVIDIA NIM ile modelleri indirebilirsiniz. Modelleri kurum bünyesinde (on-premises) çalıştırma yeteneği, işletmenize özelleştirmelerinizin sahipliğini ve fikri mülkiyetiniz ile yapay zeka uygulamanız üzerinde tam kontrol sağlar.

NIM'ler, NVIDIA AI Enterprise lisansı kullanılarak NVIDIA'nın API kataloğundan dışa aktarılabilir ve kurum bünyesinde veya bulutta çalıştırılabilir.

NIM'ler, model bazında konteyner imajları olarak paketlenir ve NVIDIA NGC Kataloğu aracılığıyla NGC konteyner imajları olarak dağıtılır. Temelde NIM'ler, bir yapay zeka modeli üzerinde çıkarım (inference) yapmak için kolay, tutarlı ve tanıdık API'ler sağlar.

# NVIDIA’ın LLM bağlayıcısı

bu örnek, halka açık AI Foundation uç noktalarını kullanarak LLM destekli sistemler geliştirmek ve bunlarla etkileşim kurmak için LlamaIndex'in nasıl kullanılacağını ele almaktadır.

Bu bağlayıcı ile, barındırılan [NVIDIA NIM'leri](https://ai.nvidia.com) olarak sunulan uyumlu modellere bağlanabilir ve onlardan içerik üretebilirsiniz, örneğin:

- Google’ın [gemma-7b](https://build.nvidia.com/google/gemma-7b) modeli
- Mistal AI’nın [mistral-7b-instruct-v0.2](https://build.nvidia.com/mistralai/mistral-7b-instruct-v2) modeli
- Ve daha fazlası!

## Kurulum

```bash
%pip install --upgrade --quiet llama-index-llms-nvidia llama-index-embeddings-nvidia llama-index-readers-file
```

## Yapılandırma

**Başlamak için:**

1. NVIDIA AI Foundation modellerini barındıran [NVIDIA](https://build.nvidia.com/) üzerinden ücretsiz bir hesap oluşturun.

2. İstediğiniz modeli seçin.

3. "Input" (Girdi) kısmından "Python" sekmesini seçin ve `Get API Key` (API Anahtarı Al) düğmesine tıklayın. Ardından `Generate Key` (Anahtarı Oluştur) düğmesine tıklayın.

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

```python
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.llms import ChatMessage, MessageRole


llm = NVIDIA()


messages = [
    ChatMessage(
        role=MessageRole.SYSTEM, content=("Yardımsever bir asistansın.")
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=("Kuzey Amerika'daki en popüler evcil hayvanlar hangileridir?"),
    ),
]


llm.chat(messages)
```

## NVIDIA NIM'leri ile Çalışma

Barındırılan [NVIDIA NIM'lerine](https://ai.nvidia.com) bağlanmanın yanı sıra, bu bağlayıcı yerel mikro hizmet örneklerine bağlanmak için de kullanılabilir. Bu, gerektiğinde uygulamalarınızı yerel ortama taşımanıza yardımcı olur.

Yerel mikro hizmet örneklerinin nasıl kurulacağına ilişkin talimatlar için şu adrese bakın: <https://developer.nvidia.com/blog/nvidia-nim-offers-optimized-inference-microservices-for-deploying-ai-models-at-scale/>

```python
from llama_index.llms.nvidia import NVIDIA


# localhost:8080 üzerinde çalışan bir sohbet NIM'ine bağlanın ve belirli bir model belirtin
llm = NVIDIA(
    base_url="http://localhost:8080/v1", model="meta/llama3-8b-instruct"
)
```

## Belirli bir modeli yükleme

Şimdi, buradaki [belgelerde](https://docs.api.nvidia.com/nim/reference/) bulunan model adını geçerek `NVIDIA` LLM'imizi yükleyebiliriz.

> NOT: Varsayılan model `meta/llama3-8b-instruct`'dur.

```python
# varsayılan model
llm = NVIDIA()
llm.model
```

`llm` nesnemizin şu anda hangi modelle ilişkili olduğunu `.model` özniteliğiyle gözlemleyebiliriz.

```python
llm = NVIDIA(model="mistralai/mistral-7b-instruct-v0.2")
llm.model
```

## Temel İşlevsellik

Artık bağlayıcıyı LlamaIndex ekosistemi içinde kullanmanın farklı yollarını keşfedebiliriz!

Başlamadan önce, bazı yöntemler için beklenen girdi olan bir `ChatMessage` nesneleri listesi hazırlayalım.

Her örnek için aynı temel modeli takip edeceğiz:

1. `NVIDIA` LLM'imizi istediğimiz modele yönlendireceğiz.
2. İstenilen görevi başarmak için uç noktanın nasıl kullanılacağını inceleyeceğiz!

### Tamamlama (Complete): `.complete()`

Seçilen modelden bir yanıt almak için `.complete()`/`.acomplete()` (bir dize alır) yöntemini kullanabiliriz.

Bu görev için varsayılan modelimizi kullanalım.

```python
completion_llm = NVIDIA()
```

`.model` özniteliğini kontrol ederek bunun beklenen varsayılan olduğunu doğrulayabiliriz.

```python
completion_llm.model
```

Modelimiz üzerinde `"Merhaba!"` dizesiyle `.complete()` yöntemini çağıralım ve yanıtı gözlemleyelim.

```python
completion_llm.complete("Merhaba!")
```

LlamaIndex'ten beklendiği üzere - yanıt olarak bir `CompletionResponse` alırız.

#### Asenkron Tamamlama: `.acomplete()`

Aynı şekilde kullanılabilecek bir asenkron uygulama da mevcuttur!

```python
await completion_llm.acomplete("Merhaba!")
```

#### Sohbet (Chat): `.chat()`

Şimdi aynı şeyi `.chat()` yöntemini kullanarak deneyebiliriz. Bu yöntem bir sohbet mesajları listesi bekler - bu yüzden yukarıda oluşturduğumuzu kullanacağız.

Örnek için `mistralai/mixtral-8x7b-instruct-v0.1` modelini kullanacağız.

```python
chat_llm = NVIDIA(model="mistralai/mixtral-8x7b-instruct-v0.1")
```

Şimdi tek yapmamız gereken `ChatMessages` listemiz üzerinde `.chat()` yöntemini çağırmak ve yanıtımızı gözlemlemek.

Oluşturmayı etkileyebilecek birkaç ek anahtar kelime argümanı da geçebileceğimizi fark edeceksiniz - bu durumda, oluşturmamızı etkilemek için `seed` parametresini ve modelin belirli bir belirtece ulaştığında oluşturmayı durdurmasını istediğimizi belirtmek için `stop` parametresini kullandık!

> NOT: Seçilen modelin uç noktası tarafından hangi ek argümanların (kwargs) desteklendiğine dair bilgileri, modelin API belgelerine başvurarak bulabilirsiniz. Örnek olarak Mixtral'in belgeleri [buradadır](https://docs.api.nvidia.com/nim/reference/mistralai-mixtral-8x7b-instruct-infer)!

```python
chat_llm.chat(messages, seed=4, stop=["kedi", "kediler", "Kedi", "Kediler"])
```

Beklendiği gibi, yanıt olarak bir `ChatResponse` alırız.

#### Asenkron Sohbet: (`achat`)

Ayrıca aşağıdaki şekilde çağrılabilen `.chat()` yönteminin asenkron bir uygulamasına da sahibiz.

```python
await chat_llm.achat(messages)
```

### Akış (Stream): `.stream_chat()`

`build.nvidia.com` adresinde bulunan modelleri akış senaryoları için de kullanabiliriz!

Başka bir model seçelim ve bu davranışı gözlemleyelim. Bu görev için Google'ın `gemma-7b` modelini kullanacağız.

```python
stream_llm = NVIDIA(model="google/gemma-7b")
```

Modelimizi, yine bir `ChatMessage` nesneleri listesi bekleyen `.stream_chat()` ile çağıralım ve yanıtı yakalayalım.

```python
streamed_response = stream_llm.stream_chat(messages)
```

```python
streamed_response
```

Gördüğümüz gibi, yanıt akışlı yanıtı içeren bir oluşturucudur (generator).

Oluşturma tamamlandığında nihai yanıta bir göz atalım.

```python
last_element = None
for last_element in streamed_response:
    pass


print(last_element)
```

#### Asenkron Akış: `.astream_chat()`

Akış için, senkron uygulamaya benzer şekilde kullanılabilecek eşdeğer asenkron yönteme de sahibiz.

```python
streamed_response = await stream_llm.astream_chat(messages)
```

```python
streamed_response
```

```python
last_element = None
async for last_element in streamed_response:
    pass


print(last_element)
```

## Akışlı Sorgu Motoru Yanıtları

Sorgu motoru kullanarak biraz daha kapsamlı bir örneğe bakalım!

Bazı verileri yükleyerek başlayacağız ([Otostopçunun Galaksi Rehberi](https://web.eecs.utk.edu/~hqi/deeplearning/project/hhgttg.txt) belgesini kullanacağız).

### Veri Yükleme

Önce verilerimizin barınabileceği bir dizin oluşturalım.

```bash
!mkdir -p 'data/hhgttg'
```

Verilerimizi yukarıdaki kaynaktan indireceğiz.

```bash
!wget 'https://web.eecs.utk.edu/~hqi/deeplearning/project/hhgttg.txt' -O 'data/hhgttg/hhgttg.txt'
```

Bu adım için bir eşleme (embedding) modeline ihtiyacımız olacak! Bunu başarmak için NVIDIA `NV-Embed-QA` modelini kullanacağız ve bunu `Settings` içine kaydedeceğiz.

```python
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.core import Settings


embedder = NVIDIAEmbedding(model="NV-Embed-QA", truncate="END")
Settings.embed_model = embedder
```

Artık belgemizi yükleyebilir ve yukarıdaki modelden yararlanarak bir indeks oluşturabiliriz.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader("data/hhgttg").load_data()
index = VectorStoreIndex.from_documents(documents)
```

Şimdi basit bir sorgu motoru oluşturabilir ve `streaming` parametremizi `True` olarak ayarlayabiliriz.

```python
streaming_qe = index.as_query_engine(streaming=True)
```

Sorgu motorumuza bir sorgu gönderelim ve ardından yanıtı akış şeklinde alalım.

```python
streaming_response = streaming_qe.query(
    "42 sayısının önemi nedir?",
)
```

```python
streaming_response.print_response_stream()
```

### Araç çağırma (Tool calling)

v0.2.1'den itibaren NVIDIA, araç çağırmayı desteklemektedir.

NVIDIA, build.nvidia.com adresindeki çeşitli modellerin yanı sıra yerel NIM'lerle entegrasyon sağlar. Bu modellerin tümü araç çağırma için eğitilmemiştir. Deneyleriniz ve uygulamalarınız için araç çağırma yeteneğine sahip bir model seçtiğinizden emin olun.

Araç çağırmayı desteklediği bilinen modellerin bir listesini şu şekilde alabilirsiniz:

`NOT:` Daha fazla örnek için bakınız: [nvidia\_agent.ipynb](../agent/nvidia_agent.ipynb)

```python
tool_models = [
    model
    for model in NVIDIA().available_models
    if model.is_function_calling_model
]
```

Araç kabiliyeti olan bir modelle:

```python
from llama_index.core.tools import FunctionTool




def multiply(a: int, b: int) -> int:
    """İki tam sayıyı çarpar ve sonuç tam sayısını döndürür"""
    return a * b




multiply_tool = FunctionTool.from_defaults(fn=multiply)




def add(a: int, b: int) -> int:
    """İki tam sayıyı toplar ve sonuç tam sayısını döndürür"""
    return a + b




add_tool = FunctionTool.from_defaults(fn=add)


llm = NVIDIA("meta/llama-3.1-70b-instruct")
from llama_index.core.agent import FunctionAgent


agent_worker = FunctionAgent(
    tools=[multiply_tool, add_tool],
    llm=llm,
)


response = await agent_worker.run("(121 * 3) + 42 kaçtır?")
print(str(response))
```
