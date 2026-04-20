---
title: Llama2 + Vektör Deposu İndeksi (VectorStoreIndex)
 | LlamaIndex OSS Belgeleri
---

# Llama2 + Vektör Deposu İndeksi (VectorStoreIndex)

Bu not defteri (notebook), llama-2'yi LlamaIndex ile birlikte kullanabilmek için gereken uygun kurulumu adım adım gösterir. Spesifik (Özel) olarak bir vektör deposu (vector store) indeksi kullanmaya odaklanıyoruz.

## Kurulum (Setup)

Bu Not Defterini şayet Colab üzerinde açtıysanız (çalıştıracaksanız), büyük ihtimalle sisteminize (kernel) LlamaIndex'i 🦙 kurmanız (install) gerekecektir.

```bash
%pip install llama-index-llms-replicate
```

```bash
!pip install llama-index
```

### Anahtarlar (Keys)

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["REPLICATE_API_TOKEN"] = "SİZİN_REPLICATE_ANAHTARINIZ"
```

### Belgeleri yükleyin, Vektör Deposu İndeksini (VectorStoreIndex) oluşturun

```python
# İsteğe Bağlı Olarak Günlük Kaydı (Optional logging)
# import logging
# import sys


# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


from IPython.display import Markdown, display
```

```python
from llama_index.llms.replicate import Replicate
from llama_index.core.llms.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)


# Replicate uç noktası (endpoint)
LLAMA_13B_V2_CHAT = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"




# llama-2'ye özel (custom) sistem komutunu (system prompt) yerleştir (inject)
def custom_completion_to_prompt(completion: str) -> str:
    return completion_to_prompt(
        completion,
        system_prompt=(
            "Sen bir Soru-Cevap (Q&A) asistanısın. Görevin ve hedefin (goal); "
            "soruları, sağlanan talimatlar (instructions) ve bağlama (context) en uygun ve doğru şekilde yanıtlamaktır."
        ),
    )




llm = Replicate(
    model=LLAMA_13B_V2_CHAT,
    temperature=0.01,
    # llama 2'de doğrudan jeton (max token) olarak ayarlamak/yorumlanmak
    # yerine, max token sınırını bağlam/pencere aralığına çevirdiğinden ez/kaldır
    context_window=4096,
    # llama 2 için komut tamamlamanın/düzeltmenin (completion representation) üzerini çiz (override)
    completion_to_prompt=custom_completion_to_prompt,
    # eğer veri ajanları (data agents) için llama 2'yi kullanıyorsanız, mesaj temsili/ifadesi aralığını da (message representation) geçersiz kılmalısınız! (override)
    messages_to_prompt=messages_to_prompt,
)
```

```python
from llama_index.core import Settings


Settings.llm = llm
```

Veriyi İndirin

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
index = VectorStoreIndex.from_documents(documents)
```

## Sorgulama (Querying)

```python
# Daha detaylı çıktılar için Günlük Kaydı modunu DEBUG olarak ayarlayın
query_engine = index.as_query_engine()
```

```python
response = query_engine.query("Yazar büyürken neler yaptı? (What did the author do growing up?)")
display(Markdown(f"<b>{response}</b>"))
```

**Bu kapsamda tedarik edilen (the context information provided) verilere istinaden yazar büyüme evresinde yazarın faaliyeti (activities) şunlardır:**

**1. "Hiçbir iyi olayı bulunmayan" kısa taslağa dökülmüş ("awful" / "hardly any plot") korkunç edebi karamalar ve senaryolar/hikayeler düzmek.
2. Keza okul takviminin 9. derecesindeyken, IBM imzası taşıyıp "1401" konfigürasyonuyla bezenmiş klasman bir yapıda, tam anlamıyla primitif sayılabilecek Fortran uzantısı aracılığıyla erken dönem programları kodlamak.
3. Kendi oyun simülasyonları tasarlarken (Building simple games), minyatür bazlı füzelerin yahut benzeri uçarcasına yükselen sistemlerin test edilebileceği formları birleştirmek ve dahi ebeveynine/babasına tahsis üzere bir döküm aracı (kelime sistemci: a word processor) işlemek.
4. "The Moon is a Harsh Mistress" ("Ay Zalim Bir Metres" - Heinlein tarafından yazılmış) eserleri ve edebi/kurgusal bilim senaryo odaklı içeriklerle kendini beslemek; ki bunun getirisi kendisine resmen ilham kaynağı olup AI yolunun da kapılarını açmış oldu (inspired him to work on AI).
5. Zamanını en çok geçirdiği mekanlardan ve duraklardan Floransa - İtalya bölgesinde/şehri yaşayıp, buradaki caddelerden Akademya (Accademia) mevkiine (binalarına doğru) turlamak (walking).**

**Lütfen metinde geçmeyen birtakım öngörülerinizi buradaki metnin içinde yazmamasına nazaran ön kanaat/varsayım bazlı değerlendirmeler üzerinden analiz/not etmeyiniz! (are not based on prior knowledge or assumptions)**

### Akış / Yayın Desteği (Streaming Support)

```python
query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("Interleaf'te ne oldu? (What happened at interleaf?)")
for token in response.response_gen:
    print(token, end="")
```

```bash
 Buradaki bilgi ve verili metne bakıldığında, anladığımız kadarıyla yazarın yolu kendi ürettiği sistemler ile (özellikle dokümanların - creating and managing documents tasarlanıp idare edilmesi bağlamında) hizmet sunan 'Interleaf' firmasından geçmiş gibi bir mana ifade ediyor (worked at Interleaf / the author mentions). Ancak döküm de yazılanlara referans sağladığımızda, belli ki kurumu (firmayı) temsil eden Interleaf bu aşamada ciddi bir sarsılma/tökezlenmeye ("on the way down") adım atıyordu (çöküşe doğru). Üstelik sistem yazılımcısına dönük Sürüm/Mühendislik ekibinden daha cüsseli (the company's Release Engineering group was large) bir yazılım takım ve grupsal yığınına sahip olduğu belli ve keza bu yapı dahi göz önündeydi. Bütün bu denklemler yazarı hem parasal manada strese sokmakla ve hem de net / sarih/ açık bir izahat/ifade vermemesinin dışında Interleaf'te bizzat da nelerin döndüğünün de açıklıkla yazılmamasında/bilinmemesinde bizleri yanıltmıyor.
```
