# NVIDIA NIM'leri

---
title: NVIDIA NIM'leri
 | LlamaIndex OSS Belgeleri
---

`llama-index-llms-nvidia` paketi, NVIDIA NIM çıkarım mikro hizmetindeki modellerle uygulamalar oluşturmak için LlamaIndex entegrasyonlarını içerir. NIM; topluluğun yanı sıra NVIDIA'nın sunduğu sohbet, eşleme (embedding) ve yeniden sıralama (re-ranking) modelleri gibi farklı alanlardaki modelleri destekler. Bu modeller, NVIDIA tarafından hızlandırılmış altyapıda en iyi performansı sunmak üzere optimize edilmiş ve NVIDIA hızlandırılmış altyapısında tek bir komutla her yere dağıtılabilen, kullanımı kolay, önceden oluşturulmuş konteynerler olan NIM'ler olarak dağıtılmıştır.

NIM'lerin NVIDIA tarafından barındırılan dağıtımları [NVIDIA API kataloğu](https://build.nvidia.com/) üzerinden test edilebilir. Test işleminden sonra NIM'ler, NVIDIA AI Enterprise lisansı kullanılarak NVIDIA'nın API kataloğundan dışa aktarılabilir ve kurum bünyesinde (on-premises) veya bulutta çalıştırılarak işletmelere fikri mülkiyetleri ve yapay zeka uygulamaları üzerinde sahiplik ve tam kontrol sağlar.

NIM'ler, model bazında konteyner imajları olarak paketlenir ve NVIDIA NGC Kataloğu aracılığıyla NGC konteyner imajları olarak dağıtılır. Temelde NIM'ler, bir yapay zeka modeli üzerinde çıkarım (inference) yapmak için kolay, tutarlı ve tanıdık API'ler sağlar.

```bash
%pip install --upgrade --quiet llama-index-core llama-index-readers-file llama-index-llms-nvidia llama-index-embeddings-nvidia llama-index-postprocessor-nvidia-rerank
```

Bir test veri kümesi getirelim; 2021'de San Francisco'daki konut inşaatıyla ilgili bir PDF.

```bash
!mkdir data
!wget "https://www.dropbox.com/scl/fi/p33j9112y0ysgwg77fdjz/2021_Housing_Inventory.pdf?rlkey=yyok6bb18s5o31snjd2dxkxz3&dl=0" -O "data/housing_data.pdf"
```

## Yapılandırma

Bağımlılıkları içe aktarın ve [NVIDIA API Kataloğu](https://build.nvidia.com) üzerinden aldığınız NVIDIA API anahtarınızı ayarlayın.

**Başlamak için:**

1. NVIDIA AI Foundation modellerini barındıran [NVIDIA](https://build.nvidia.com/) üzerinden ücretsiz bir hesap oluşturun.

2. İstediğiniz modeli seçin.

3. **Input** (Girdi) kısmından **Python** sekmesini seçin ve **Get API Key** (API Anahtarı Al) düğmesine tıklayın. Ardından **Generate Key** (Anahtarı Oluştur) düğmesine tıklayın.

4. Oluşturulan anahtarı kopyalayın ve `NVIDIA_API_KEY` olarak kaydedin. Buradan itibaren uç noktalara erişiminiz olmalıdır.

```python
from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from google.colab import userdata
import os


os.environ["NVIDIA_API_KEY"] = userdata.get("nvidia-api-key")
```

Eşleme (embedding) modeli için NVIDIA tarafından barındırılan bir NIM kullanın.

NVIDIA'nın varsayılan eşlemeleri yalnızca ilk 512 belirteci eşler, bu nedenle eşlemelerin doğruluğunu en üst düzeye çıkarmak için parça boyutunu (chunk size) 500 olarak ayarlayın.

```python
Settings.text_splitter = SentenceSplitter(chunk_size=500)


documents = SimpleDirectoryReader("./data").load_data()
```

Eşleme modelini NVIDIA'nın varsayılanına ayarlayın. Bir parça, modelin kodlayabileceği belirteç sayısını aşarsa, varsayılan davranış hata fırlatmaktır; bu nedenle limiti aşan belirteçleri atmak için `truncate="END"` değerini ayarlayın.

```python
Settings.embed_model = NVIDIAEmbedding(model="NV-Embed-QA", truncate="END")


index = VectorStoreIndex.from_documents(documents)
```

Veriler bellekte eşlendikten ve indekslendikten sonra LLM'yi kurun. NIM, [NIM hızlı başlangıç kılavuzu](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html) takip edilerek Docker kullanılarak 5 dakika içinde yerel olarak barındırılabilir.

Aşağıdaki örnek şunların nasıl yapılacağını gösterir:

- Meta'nın açık kaynaklı `meta/llama-3.1-8b-instruct` modelini yerel bir NIM olarak kullanma.
- `meta/llama-3.1-70b-instruct` modelini NVIDIA tarafından barındırılan API Kataloğu üzerinden bir NIM olarak kullanma.

Yerel bir NIM kullanıyorsanız, `base_url` değerini dağıtılmış NIM URL'nizle değiştirin.

Örnek, soruyu yanıtlamak için en alakalı ilk 20 parçayı getirir.

```python
# Kurum bünyesinde barındırılan (Self-hosted) NIM: Aşağıdaki satırı açın ve API Kataloğu satırını yorum haline getirin
# Settings.llm = NVIDIA(model="meta/llama-3.1-8b-instruct", base_url="http://your-nim-host-address:8000/v1")


# API Kataloğu NIM: Kurum bünyesinde barındırılan bir NIM kullanıyorsanız bu satırı yorum yapın
Settings.llm = NVIDIA(model="meta/llama-3.1-70b-instruct")


query_engine = index.as_query_engine(similarity_top_k=20)
```

Belgede tek bir yerde (sayfa 18'de) yanıtlanan basit bir soru sorun.

```python
response = query_engine.query(
    "2021 yılında San Francisco'da kaç yeni konut birimi inşa edildi?"
)
print(response)
```

```
2021 yılında Şehir konut stokuna net 4.649 birim eklenmiştir.
```

Şimdi bir tablo okunmasını gerektiren (belgenin 41. sayfasında) daha karmaşık bir soru sorun:

```python
response = query_engine.query(
    "2021 yılında Mission'da konut birimlerindeki net kazanç neydi?"
)
print(response)
```

```
2021 yılında Mission'daki konut birimlerindeki net kazanç hakkında spesifik bir bilgi bulunmamaktadır. Sağlanan veriler şehrin genel konut stoku ve üretimi hakkındadır, ancak Mission dahil olmak üzere mahalle bazında bir döküm sunmamaktadır.
```

Bu doğru cevap değil. Daha gelişmiş bir PDF ayrıştırıcısı olan LlamaParse'ı deneyin:

```bash
!pip install llama-parse
```

```python
from llama_parse import LlamaParse


# bir not defterinde, LlamaParse'ın çalışması için bu gereklidir
import nest_asyncio


nest_asyncio.apply()


# cloud.llamaindex.ai adresinden bir anahtar alabilirsiniz
os.environ["LLAMA_CLOUD_API_KEY"] = userdata.get("llama-cloud-key")


# ayrıştırıcıyı kur
parser = LlamaParse(
    result_type="markdown"  # "markdown" ve "text" seçenekleri mevcuttur
)


# dosyamızı ayrıştırmak için SimpleDirectoryReader kullanın
file_extractor = {".pdf": parser}
documents2 = SimpleDirectoryReader(
    "./data", file_extractor=file_extractor
).load_data()
```

```python
index2 = VectorStoreIndex.from_documents(documents2)
query_engine2 = index2.as_query_engine(similarity_top_k=20)
```

```python
response = query_engine2.query(
    "2021 yılında Mission'da konut birimlerindeki net kazanç neydi?"
)
print(response)
```

```
2021 yılında Mission'daki konut birimlerindeki net kazanç 1.305 birimdi.
```

Daha iyi bir ayrıştırıcı ile LLM soruyu doğru cevaplayabiliyor.

Şimdi daha zor bir soru deneyin:

```python
response = query_engine2.query(
    "2021 yılında kaç adet uygun fiyatlı konut birimi tamamlandı?"
)
print(response)
```

```
Tekrar: 110
```

LLM'in kafası karışıyor; bu durum konut birimlerindeki yüzde artış gibi görünüyor.

LLM'e daha fazla bağlam vermeyi (20 yerine 40) ve ardından bu parçaları bir yeniden sıralayıcı (reranker) ile sıralamayı deneyin. Bunun için NVIDIA'nın yeniden sıralayıcısını kullanın:

```python
from llama_index.postprocessor.nvidia_rerank import NVIDIARerank


query_engine3 = index2.as_query_engine(
    similarity_top_k=40, node_postprocessors=[NVIDIARerank(top_n=10)]
)
```

```python
response = query_engine3.query(
    "2021 yılında kaç adet uygun fiyatlı konut birimi tamamlandı?"
)
print(response)
```

```
1.495
```

Mükemmel! Artık rakam doğru (merak ediyorsanız bu 35. sayfadadır).
