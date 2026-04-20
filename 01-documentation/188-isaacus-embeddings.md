# Isaacus Embedding'leri

`llama-index-embeddings-isaacus` paketi, Isaacus'un hukuki yapay zeka embedding modelleriyle uygulamalar oluşturmak için LlamaIndex entegrasyonlarını içerir. Bu entegrasyon, [Massive Legal Embedding Benchmark (MLEB)](https://isaacus.com/blog/introducing-mleb) üzerindeki dünyanın en isabetli hukuki embedding modeli olan **Kanon 2 Embedder**'a kolayca bağlanmanıza ve kullanmanıza olanak tanır.

Isaacus embedding'leri göreve özel optimizasyonu destekler:
- `task="retrieval/query"`: Arama sorguları için embedding'leri optimize et
- `task="retrieval/document"`: İndekslenecek dökümanlar için embedding'leri optimize et

Bu not defterinde, hukuki döküman erişimi için Isaacus Embedding'lerinin kullanımını göstereceğiz.

## Kurulum

Gerekli entegrasyonları kurun.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-isaacus
%pip install llama-index-llms-openai
```

```python
%pip install llama-index
```

## Kurulum (Setup)

### Isaacus API anahtarınızı alın

1. [Isaacus Platformunda](https://platform.isaacus.com/accounts/signup/) hesap oluşturun
2. [Ücretsiz kredilerinizi](https://docs.isaacus.com/pricing/credits) talep etmek için bir [ödeme yöntemi](https://platform.isaacus.com/billing/) ekleyin
3. Bir [API anahtarı](https://platform.isaacus.com/users/api-keys/) oluşturun

```python
import os

# Isaacus API anahtarınızı ayarlayın
isaacus_api_key = "ISAACUS_API_ANAHTARINIZ"
os.environ["ISAACUS_API_KEY"] = isaacus_api_key
```

## Temel Kullanım

### Tek Bir Embedding Alın

```python
from llama_index.embeddings.isaacus import IsaacusEmbedding

# Isaacus Embedding modelini başlatın
embed_model = IsaacusEmbedding(
    api_key=isaacus_api_key,
    model="kanon-2-embedder",
)

# Tek bir embedding al
embedding = embed_model.get_text_embedding(
    "Bu sözleşme Delaware yasalarına tabi olacaktır."
)

print(f"Embedding boyutu: {len(embedding)}")
print(f"İlk 5 değer: {embedding[:5]}")
```

### Toplu (Batch) Embedding'leri Alın

```python
# Birden fazla hukuki metin için embedding al
legal_texts = [
    "Taraflar bağlayıcı tahkimi kabul ederler.",
    "Gizli bilgiler ifşa edilmeyecektir.",
    "Bu sözleşme 30 gün önceden bildirimde bulunarak feshedilebilir.",
]

embeddings = embed_model.get_text_embedding_batch(legal_texts)

print(f"Embedding sayısı: {len(embeddings)}")
print(f"Her bir embedding {len(embeddings[0])} boyuta sahiptir")
```

## Göreve Özel (Task-Specific) Embedding'ler

Isaacus embedding'leri optimal performans için farklı görevleri destekler:
- **`retrieval/document`**: İndekslenecek dökümanlar için
- **`retrieval/query`**: Arama sorguları için

Uygun görevin kullanılması erişim isabetini artırır.

```python
# Dökümanlar için (indeksleme yaparken kullanın)
doc_embed_model = IsaacusEmbedding(
    api_key=isaacus_api_key,
    task="retrieval/document",
)

doc_embedding = doc_embed_model.get_text_embedding(
    "Şirket bu sözleşmeyi feshetme hakkına sahiptir."
)

print(f"Döküman embedding boyutu: {len(doc_embedding)}")
```

```python
# Sorgular için (get_query_embedding tarafından otomatik olarak kullanılır)
query_embedding = embed_model.get_query_embedding(
    "Fesih koşulları nelerdir?"
)

print(f"Sorgu embedding boyutu: {len(query_embedding)}")
```

## Boyut Azaltma (Dimensionality Reduction)

Daha hızlı arama ve daha düşük depolama maliyetleri için embedding boyutunu azaltabilirsiniz:

```python
# Azaltılmış boyutları kullan (varsayılan 1792'dir)
embed_model_512 = IsaacusEmbedding(
    api_key=isaacus_api_key,
    dimensions=512,
)

embedding_512 = embed_model_512.get_text_embedding("Hukuki metin örneği")

print(f"Azaltılmış embedding boyutu: {len(embedding_512)}")
```

## Hukuki Dökümanlarla Tam RAG Örneği

Şimdi bir hukuki döküman (Uber'in 10-K SEC raporu) ile Isaacus embedding'lerini kullanarak tam bir RAG boru hattı oluşturalım.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.response.notebook_utils import display_source_node
from IPython.display import Markdown, display
```

### Hukuki Döküman Verilerini İndir

Hukuki ve düzenleyici bilgiler içeren Uber'in 10-K SEC raporunu kullanacağız; bu, Kanon 2'nin hukuk alanı uzmanlığını göstermek için mükemmeldir.

```python
!mkdir -p 'data/10k/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10k/uber_2021.pdf' -O 'data/10k/uber_2021.pdf'
```

### Hukuki Dökümanı Yükle

```python
documents = SimpleDirectoryReader("./data/10k/").load_data()
print(f"{len(documents)} döküman yüklendi")
```

### Döküman Görevi ile İndeks İnşa Et

Döküman depolaması için embedding'leri optimize etmek amacıyla indeksi oluştururken `task="retrieval/document"` parametresini kullanıyoruz.

```python
# Dökümanlar için embedding modelini başlatın
embed_model = IsaacusEmbedding(
    api_key=isaacus_api_key,
    model="kanon-2-embedder",
    task="retrieval/document",
)

# İndeksi inşa et
index = VectorStoreIndex.from_documents(
    documents=documents,
    embed_model=embed_model,
)
```

### Hukuki Sorularla Sorgulama

Şimdi indeksi hukuki nitelikteki sorularla sorgulayacağız. `get_query_embedding` yönteminin optimal sorgu performansı için otomatik olarak `task="retrieval/query"` kullandığını unutmayın.

```python
# Bir erişici (retriever) oluşturun
retriever = index.as_retriever(similarity_top_k=3)

# Risk faktörleri hakkında sorgu
retrieved_nodes = retriever.retrieve(
    "Dökümanda belirtilen ana risk faktörleri nelerdir?"
)

print(f"{len(retrieved_nodes)} düğüm (node) getirildi\n")

for i, node in enumerate(retrieved_nodes):
    print(f"\n--- Düğüm {i+1} (Skor: {node.score:.4f}) ---")
    display_source_node(node, source_length=500)
```

### Yasal İşlemler Hakkında Sorgulama

```python
# Yasal işlemler hakkında sorgu
retrieved_nodes = retriever.retrieve(
    "Şirket hangi yasal işlemler veya davalarla ilgileniyor?"
)

print(f"{len(retrieved_nodes)} düğüm (node) getirildi\n")

for i, node in enumerate(retrieved_nodes):
    print(f"\n--- Düğüm {i+1} (Skor: {node.score:.4f}) ---")
    display_source_node(node, source_length=500)
```

### LLM ile Sorgu Motoru İnşa Edin

Eksiksiz bir soru-cevap sistemi için Isaacus embeddinglerini bir LLM ile birleştirin:

```python
import os

# OpenAI API anahtarınızı ayarlayın
openai_api_key = "OPENAI_API_ANAHTARINIZ"
os.environ["OPENAI_API_KEY"] = openai_api_key
```

```python
# LLM'i kurun
llm = OpenAI(model="gpt-4o-mini", temperature=0)

# Sorgu motorunu oluşturun
query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k=5,
)

# Hukuki bir soru sorun
response = query_engine.query(
    "Şirketin ana düzenleyici ve hukuki riskleri nelerdir?"
)

display(Markdown(f"**Cevap:** {response}"))
```

### Başka Bir Hukuki Sorgu

```python
response = query_engine.query(
    "Şirket hangi fikri mülkiyet haklarına güveniyor?"
)

display(Markdown(f"**Cevap:** {response}"))
```

## Asenkron (Async) Kullanım

Isaacus embedding'leri, asenkron uygulamalarda daha iyi performans için asenkron işlemleri de destekler:

```python
import asyncio


async def get_embeddings_async():
    embed_model = IsaacusEmbedding(
        api_key=isaacus_api_key,
    )

    # Asenkron tekli embedding al
    embedding = await embed_model.aget_text_embedding(
        "Asenkron hukuki döküman metni"
    )

    # Asenkron toplu embedding al
    embeddings = await embed_model.aget_text_embedding_batch(
        ["Metin 1", "Metin 2", "Metin 3"]
    )

    return embedding, embeddings


# Asenkron fonksiyonu çalıştır
embedding, embeddings = await get_embeddings_async()

print(f"Asenkron tekli embedding boyutu: {len(embedding)}")
print(
    f"Asenkron toplu işlem: her biri {len(embeddings[0])} boyutta {len(embeddings)} adet embedding"
)
```

## Özet

Bu not defterinde şunları gösterdik:

1. **Temel kullanım** - Tekli ve toplu embedding alma
2. **Göreve özel optimizasyon** - İndeksleme için `retrieval/document` ve arama için `retrieval/query` kullanımı
3. **Boyut azaltma** - Verimlilik için embedding boyutunu küçültme
4. **Hukuki RAG boru hattı** - Hukuki dökümanlarla (Uber 10-K) eksiksiz bir erişim sistemi inşa etme
5. **Asenkron işlemler** - Daha iyi performans için asenkron yöntemlerin kullanımı

Kanon 2 Embedder, hukuki döküman anlama ve getirme konularında üstündür; bu da onu legal tech uygulamaları, uyumluluk (compliance) araçları, sözleşme analizi ve daha fazlası için ideal kılar.

## Ek Kaynaklar

- [Isaacus Dökümantasyonu](https://docs.isaacus.com)
- [Kanon 2 Embedder Duyurusu](https://isaacus.com/blog/introducing-kanon-2-embedder)
- [Massive Legal Embedding Benchmark (MLEB)](https://isaacus.com/blog/introducing-mleb)
- [Isaacus Platformu](https://platform.isaacus.com)