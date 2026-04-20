# Basit Vektör Deposu - Asenkron İndeks Oluşturma

---
title: Basit Vektör Deposu - Asenkron İndeks Oluşturma
 | LlamaIndex OSS Belgeleri
---

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-readers-wikipedia
```

```bash
!pip install llama-index
```

```python
import time


# Asyncio'nun Jupyter içinde çalışmasına yardımcı olur
import nest_asyncio


nest_asyncio.apply()


# OpenAI Anahtarım
import os


os.environ["OPENAI_API_KEY"] = "[API_ANAHTARINIZ]"
```

```python
from llama_index.core import VectorStoreIndex, download_loader


from llama_index.readers.wikipedia import WikipediaReader


loader = WikipediaReader()
documents = loader.load_data(
    pages=[
        "Berlin",
        "Santiago",
        "Moscow",
        "Tokyo",
        "Jakarta",
        "Cairo",
        "Bogota",
        "Shanghai",
        "Damascus",
    ]
)
```

```python
len(documents)
```

```text
9
```

Belge olarak indirilen 9 Wikipedia makalesi.

```python
start_time = time.perf_counter()
index = VectorStoreIndex.from_documents(documents)
duration = time.perf_counter() - start_time
print(duration)
```

```text
INFO:root:> [build_index_from_documents] Toplam LLM jeton (token) kullanımı: 0 jeton
INFO:root:> [build_index_from_documents] Toplam gömme (embedding) jeton kullanımı: 142295 jeton




7.691995083000052
```

Standart indeks oluşturma 7.69 saniye sürdü.

```python
start_time = time.perf_counter()
index = VectorStoreIndex(documents, use_async=True)
duration = time.perf_counter() - start_time
print(duration)
```

```text
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=245 request_id=314b145a07f65fd34e707f633cc1a444 response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=432 request_id=bb9e796d0b8f9c2365b68de8a56009ff response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=433 request_id=7a94707fe2f8916e9cdd8276a5748207 response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=499 request_id=cda679215293c3a13ed57c2eae3dc582 response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=527 request_id=5e1c3e74aa3f9f950e4035f81a0f0a15 response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=585 request_id=81983fe76eab95f73f82df881ff7b2d9 response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=574 request_id=702a182b54a29a33719205f722378c8e response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=575 request_id=d1df11775c59a3ba403dda253081f8eb response_code=200
INFO:openai:message='OpenAI API yanıtı' path=https://api.openai.com/v1/engines/text-embedding-ada-002/embeddings processing_ms=575 request_id=47929f13469569527505b51958cd8e71 response_code=200
INFO:root:> [build_index_from_documents] Toplam LLM jeton kullanımı: 0 jeton
INFO:root:> [build_index_from_documents] Toplam gömme jeton kullanımı: 142295 jeton




2.3730635830000892
```

Asenkron indeks oluşturma 2.37 saniye sürdü.

```python
query_engine = index.as_query_engine()
query_engine.query("Jakarta'nın etimolojisi nedir?")
```

```text
INFO:root:> [query] Toplam LLM jeton kullanımı: 4075 jeton
INFO:root:> [query] Toplam gömme jeton kullanımı: 8 jeton




Response(response="\n\n'Jakarta' ismi, nihayetinde Sanskritçe jay (zafer) ve krt (başarılmış, elde edilmiş) kelimelerinden türetilen Jayakarta (Devanagari: जयकर्त) kelimesinden türetilmiştir; bu nedenle Jayakarta 'zafer dolu eylem', 'tamamlanmış eylem' veya 'tam zafer' olarak tercüme edilir. 1527 yılında Portekizlileri şehirden başarıyla mağlup eden ve uzaklaştıran Fatahillah'ın Müslüman birlikleri onuruna bu isim verilmiştir. Jayakarta olarak adlandırılmadan önce şehir 'Sunda Kelapa' olarak biliniyordu. Portekizli bir eczacı olan Tomé Pires, Doğu Hint Adaları yolculuğu sırasında başyapıtında şehrin adını Jacatra veya Jacarta olarak yazmıştır. Şehir, deniz seviyesinden ortalama 8 m (26 ft) yükseklikte, -2 ile 91 m (-7 ile 299 ft) arasında değişen alçak bir bölgede yer almakta olup, tarihsel olarak geniş bataklık alanlara sahiptir. Şehrin bazı kısımları, bölge çevresinde oluşan geri kazanılmış gelgit düzlükleri üzerine inşa edilmiştir. Ciliwung Nehri, Kalibaru, Pesanggra dahil olmak üzere on üç nehir Jakarta'dan geçmektedir.", source_nodes=[...])
```
