---
title: Yerel Llama2 + Vektör Deposu İndeksi (VectorStoreIndex)
 | LlamaIndex OSS Belgeleri
---

# Yerel Llama2 + Vektör Deposu İndeksi (VectorStoreIndex)

Bu not defteri (notebook), yerel olarak (locally) LlamaIndex ile llama-2'yi kullanmak için uygun kurulum adımlarını gösterir. Bu not defterini çalıştırmak için iyi ve yeterli bir GPU'ya (ideal olarak en az 40 GB belleğe sahip bir A100) ihtiyacınız olduğunu unutmayın.

Özellikle (Specifically), bir vektör deposu indeksinin (vector store index) kullanımına bakıyoruz.

## Kurulum (Setup)

```bash
%pip install llama-index-llms-huggingface
%pip install llama-index-embeddings-huggingface
```

```bash
!pip install llama-index ipywidgets
```

### Ayarlama (Set Up)

**ÖNEMLİ (IMPORTANT)**: Lütfen konsolunuzda `huggingface-cli login` komutunu kullanarak llama2 modellerine erişimi olan (yetkilendirilmiş) bir hesapla HF hub'da oturum açın (sign in). Daha fazla detay için lütfen [HTTPS://ai.meta.com/resources/models-and-libraries/llama-downloads/](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) adresine bakın.

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))




from IPython.display import Markdown, display
```

```python
import torch
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate


# Model isimleri (HF'de erişiminiz olduğundan emin olun)
LLAMA2_7B = "meta-llama/Llama-2-7b-hf"
LLAMA2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
LLAMA2_13B = "meta-llama/Llama-2-13b-hf"
LLAMA2_13B_CHAT = "meta-llama/Llama-2-13b-chat-hf"
LLAMA2_70B = "meta-llama/Llama-2-70b-hf"
LLAMA2_70B_CHAT = "meta-llama/Llama-2-70b-chat-hf"


selected_model = LLAMA2_13B_CHAT


SYSTEM_PROMPT = """Sen, verilen kaynak belgelere (source documents) dayanarak soruları dostane bir şekilde cevaplayan bir yapay zeka (AI) asistanısın. İşte her zaman uyman gereken bazı kurallar:
- İnsanlar tarafından okunabilir (human readable) çıktılar üret, anlamsız metinlere sahip (gibberish) çıktılar oluşturmaktan kaçın.
- Sadece talep edilen çıktıyı üret, istenen çıktıdan önce veya sonra başka herhangi bir şey/dil ekleme.
- Asla teşekkür etme, yardım etmekten mutlu olduğunu veya bir AI temsilcisi (ajani) olduğunu vb. söyleme. Sadece doğrudan (directly) cevap ver.
- Kuzey Amerika'daki iş/kurumsal (business) belgelerinde yaygın olarak kullanılan profesyonel (professional) bir dil yarat.
- Asla saldırgan (offensive) veya kaba / pis (foul) bir dil kullanma (üretme).
"""


query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)


llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=2048,
    generate_kwargs={"temperature": 0.0, "do_sample": False},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name=selected_model,
    model_name=selected_model,
    device_map="auto",
    # aşağıdaki ayarları GPU'nuza bağlı olarak değiştirebilirsiniz
    model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True},
)
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

```python
from llama_index.core import Settings


Settings.llm = llm
Settings.embed_model = embed_model
```

Veriyi İndirin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from llama_index.core import SimpleDirectoryReader


# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
from llama_index.core import VectorStoreIndex


index = VectorStoreIndex.from_documents(documents)
```

## Sorgulama (Querying)

```python
# Daha detaylı çıktılar için Günlük Kaydını (Logging) DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
```

```python
response = query_engine.query("Yazar büyürken neler yaptı? (What did the author do growing up?)")
display(Markdown(f"<b>{response}</b>"))
```

**Büyürken yazar, kısa öyküler yazdı, bir IBM 1401'de programlama yaptı ve nihayetinde babasını kendisine bir TRS-80 mikrobilgisayar satın almaya ikna etti. Basit oyunlar, maket roketlerinin ne kadar yükseğe uçacağını tahmin eden bir program ve bir kelime işlemci (word processor) yazdı. Kolejde felsefe okudu ama en sonunda (eventually) yapay zekaya (AI) yöneldi (geçti). Denemeler (essays) yazdı ve bunları çevrimiçi olarak (online) yayımladı, spam / istenmeyen posta filtreleri ve resim yapma (painting) üzerine çalıştı. Ayrıca her Perşembe akşamı bir grup arkadaşı için akşam yemeklerine ev sahipliği yaptı ve Cambridge'de bir bina satın aldı.**

### Akış / Yayın Desteği (Streaming Support)

```python
import time


query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("Interleaf'te ne oldu? (What happened at interleaf?)")


start_time = time.time()


token_count = 0
for token in response.response_gen:
    print(token, end="")
    token_count += 1


time_elapsed = time.time() - start_time
tokens_per_second = token_count / time_elapsed


print(f"\n\nSaniyede {tokens_per_second} belirteç değeri ile (tokens/s) çıktı akışı sağlandı (Streamed output)")
```

```bash
Interleaf'te bir grup insan müşteriler için birtakım projeler üzerinde yetkinlik sergiliyordu (worked). Dönem içinde bir çalışan; SGML dilinin türevi olarak karşımıza çıkan ve adına HTML denilen yepyeni bir şeyden anlatıcıya (narrator) bahsetti. Anlatıcı Interleaf'ten ayrılıp / ilişiğini o safhada keserek RISD adlı kolejde / sanat okulunda kariyerini devam ettirme serüvenine atıldı ama mezkûr gruba da (grup bazında projelere de) serbest zamanlı / freelancer şekilde çalışmaya ve dahil olmaya devam etti. Ve akabinde bir zaman gelince beraberindeki anlatıcı ile beraber Trevor ve Robert isminde olan onun iki yol arkadaşı; ağ / web üzerinden / tarayıcıyı da merkeze oturtmak suretiyle bizzat (tarayıcı bazlı/aracılığıyla) kullanıcıya sanal bir dükkanlar dizayn ettirme / kurma projesine yelken açarak Viaweb ismini verdikleri bir girişime başladılar (start a new company). Oluşum / Yazılım bütünü Ocak '96 tarihi itibarıyla ilk faaliyetine merhaba derken 6 işletmeyi yayına almıştı (6 stores). Ve tüm bu program ve yazılım aslında totalde üç ayrı sac ayağından / temrinden meydana geliyordu: düzenleyici (editor/yönetici), alışveriş sepeti ve menajer (yönetici mekanizması / the manager).


Saniyede 26.923490295496002 belirteçle (tokens/s) yayınlandı (açığa çıkarıldı)
```
