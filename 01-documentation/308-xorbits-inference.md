# Xorbits Inference

---
title: Xorbits Inference
 | LlamaIndex OSS Documentation
---

Bu demo not defterinde, yerel LLM'leri üç adımda dağıtmak için Xorbits Inference'ın (kısaca Xinference) nasıl kullanılacağını gösteriyoruz.

Örnekte GGML formatındaki Llama 2 sohbet (chat) modelini kullanacağız, ancak kod Xinference tarafından desteklenen tüm LLM sohbet modellerine kolayca uyarlanabilir. Aşağıda birkaç örnek verilmiştir:

| Ad            | Tür        | Dil    | Format | Boyut (milyar parametre) | Kuantizasyon                                |
| ------------- | ---------- | -------- | ------ | ------------------ | ------------------------------------------- |
| llama-2-chat  | RLHF Model | en       | ggmlv3 | 7, 13, 70          | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’   |
| chatglm       | SFT Model  | en, zh   | ggmlv3 | 6                  | ’q4\_0’, ‘q4\_1’, ‘q5\_0’, ‘q5\_1’, ‘q8\_0’ |
| chatglm2      | SFT Model  | en, zh   | ggmlv3 | 6                  | ’q4\_0’, ‘q4\_1’, ‘q5\_0’, ‘q5\_1’, ‘q8\_0’ |
| wizardlm-v1.0 | SFT Model  | en       | ggmlv3 | 7, 13, 33          | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’   |
| wizardlm-v1.1 | SFT Model  | en       | ggmlv3 | 13                 | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’   |
| vicuna-v1.3   | SFT Model  | en       | ggmlv3 | 7, 13              | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’   |

Desteklenen modellerin güncel ve tam listesi Xorbits Inference'ın [resmi GitHub sayfasında](https://github.com/xorbitsai/inference/blob/main/README.md) bulunabilir.

## 🤖 Xinference'ı Yükleyin

i. Terminal penceresinde `pip install "xinference[all]"` komutunu çalıştırın.

ii. Kurulum tamamlandıktan sonra bu jupyter not defterini yeniden başlatın.

iii. Yeni bir terminal penceresinde `xinference` komutunu çalıştırın.

iv. Aşağıdakine benzer bir çıktı görmelisiniz:

```text
INFO:xinference:Xinference successfully started. Endpoint: http://127.0.0.1:9997
INFO:xinference.core.service:Worker 127.0.0.1:21561 has been added successfully
INFO:xinference.deploy.worker:Xinference worker successfully started.
```

v. Uç nokta (endpoint) açıklamasında, iki noktadan sonraki uç nokta port numarasını bulun. Yukarıdaki durumda bu port `9997`'dir.

vi. Port numarasını aşağıdaki hücre ile ayarlayın:

```python
%pip install llama-index-llms-xinference
```

```python
port = 9997  # uç nokta port numaranızla değiştirin
```

## 🚀 Yerel Modelleri Başlatın

Bu adımda, ilgili kütüphaneleri `llama_index` içerisinden içe aktararak başlıyoruz.

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
!pip install llama-index
```

```python
# Eğer Xinference içe aktarılamıyorsa, jupyter not defterini yeniden başlatmanız gerekebilir
from llama_index.core import SummaryIndex
from llama_index.core import (
    TreeIndex,
    VectorStoreIndex,
    KeywordTableIndex,
    KnowledgeGraphIndex,
    SimpleDirectoryReader,
)
from llama_index.llms.xinference import Xinference
from xinference.client import RESTfulClient
from IPython.display import Markdown, display
```

Ardından, bir model başlatıyor ve kullanıyoruz. Bu, modeli sonraki adımlarda belgelere ve sorgulara bağlamamıza olanak tanır.

Daha iyi performans için parametreleri değiştirmekten çekinmeyin! En iyi sonuçları elde etmek için 13B boyutunun üzerindeki modellerin kullanılması önerilir. Bununla birlikte, bu kısa demo için 7B modelleri fazlasıyla yeterlidir.

GGML formatındaki Llama 2 sohbet modeli için, en az alan kaplayandan en fazla kaynak tüketen ancak yüksek performanslı olana doğru sıralanmış bazı parametre seçenekleri aşağıdadır.

model\_size\_in\_billions:

`7`, `13`, `70`

7B ve 13B modelleri için kuantizasyon:

`q2_K`, `q3_K_L`, `q3_K_M`, `q3_K_S`, `q4_0`, `q4_1`, `q4_K_M`, `q4_K_S`, `q5_0`, `q5_1`, `q5_K_M`, `q5_K_S`, `q6_K`, `q8_0`

70B modelleri için kuantizasyon:

`q4_0`

```python
# xinference'a komut göndermek için bir istemci tanımlayın
client = RESTfulClient(f"http://localhost:{port}")


# Bir model indirin ve başlatın, bu ilk seferde biraz zaman alabilir
model_uid = client.launch_model(
    model_name="llama-2-chat",
    model_size_in_billions=7,
    model_format="ggmlv3",
    quantization="q2_K",
)


# LLM'yi kullanmak için Xinference nesnesini başlatın
llm = Xinference(
    endpoint=f"http://localhost:{port}",
    model_uid=model_uid,
    temperature=0.0,
    max_tokens=512,
)
```

## 🕺 Verileri İndeksleyin... ve Sohbet Edin!

Bu adımda, bir sorgu motoru oluşturmak için model ve verileri birleştiriyoruz. Sorgu motoru daha sonra bir sohbet robotu olarak kullanılabilir ve verilen verilere dayanarak sorgularımızı yanıtlayabilir.

Nispeten hızlı olduğu için `VectorStoreIndex` kullanacağız. Bununla birlikte, farklı deneyimler için indeksi değiştirmekten çekinmeyin. Bir önceki adımda içe aktarılan bazı kullanılabilir indeksler şunlardır:

`ListIndex`, `TreeIndex`, `VectorStoreIndex`, `KeywordTableIndex`, `KnowledgeGraphIndex`

İndeksi değiştirmek için, aşağıdaki koddaki `VectorStoreIndex` yerine başka bir indeks yazmanız yeterlidir.

Tüm kullanılabilir indekslerin güncel ve tam listesi Llama Index'in [resmi dokümanlarında](https://gpt-index.readthedocs.io/en/latest/core_modules/data_modules/index/modules.html) bulunabilir.

```python
# verilerden indeks oluştur
documents = SimpleDirectoryReader("../data/paul_graham").load_data()


# aşağıdaki satırda indeks adını değiştirin
index = VectorStoreIndex.from_documents(documents=documents)


# sorgu motorunu oluştur
query_engine = index.as_query_engine(llm=llm)
```

İsteğe bağlı olarak, bir soru sormadan önce `temperature` ve maksimum yanıt uzunluğunu (token cinsinden) doğrudan `Xinference` nesnesi üzerinden ayarlayabiliriz. Bu, sorgu motorunu her seferinde yeniden oluşturmadan farklı sorular için parametreleri değiştirmemize olanak tanır.

`temperature`, yanıtların rastgeleliğini kontrol eden 0 ile 1 arasında bir sayıdır. Daha yüksek değerler yaratıcılığı artırır ancak konu dışı yanıtlara yol açabilir. Sıfıra ayarlamak her seferinde aynı yanıtın alınmasını garanti eder.

`max_tokens`, yanıt uzunluğu için bir üst sınır belirleyen bir tamsayıdır. Yanıtlar kesilmiş gibi görünüyorsa bu değeri artırın, ancak çok uzun bir yanıtın bağlam penceresini aşabileceğini ve hatalara neden olabileceğini unutmayın.

```python
# isteğe bağlı olarak, sıcaklığı ve maksimum yanıt uzunluğunu (token cinsinden) güncelleyin
llm.__dict__.update({"temperature": 0.0})
llm.__dict__.update({"max_tokens": 2048})


# bir soru sorun ve yanıtı görüntüleyin
question = "Yazar, Y Combinator'daki vaktinden sonra ne yaptı?"


response = query_engine.query(question)
display(Markdown(f"<b>{response}</b>"))
```
