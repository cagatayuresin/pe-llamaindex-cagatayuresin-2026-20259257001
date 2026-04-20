# Çok Modlu (Multi-modal) Modeller

## Kavram

Büyük dil modelleri (LLM'ler) "metin gir, metin al" şeklinde çalışır. Büyük Çok Modlu Modeller (LMM'ler) bunu metin haricindeki modaliteleri (türleri) de kapsayacak şekilde genelleştirir. Örneğin, GPT-4V gibi modeller hem görselleri hem de metni ortaklaşa girdi olarak almanıza ve metin çıktısı vermenize olanak tanır.

Metin+görsel modellerine izin vermek için temel bir `MultiModalLLM` soyutlaması ekledik. **NOT**: Bu isimlendirme değişebilir!

## Kullanım Kalıbı (Usage Pattern)

1. Aşağıdaki kod parçası, GPT-4V gibi LMM'leri kullanmaya nasıl başlayabileceğinizi gösterir.

```python
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls
from llama_index.core import SimpleDirectoryReader

# görsel dökümanlarını URL'lerden yükle
image_documents = load_image_urls(image_urls)

# görsel dökümanlarını yerel dizinden yükle
image_documents = SimpleDirectoryReader(yerel_dizin).load_data()

# akışsız (non-streaming)
openai_mm_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview", api_key=OPENAI_API_KEY, max_new_tokens=300
)
response = openai_mm_llm.complete(
    prompt="görselde ne var?", image_documents=image_documents
)
```

2. Aşağıdaki kod parçası, Çok Modlu Vektör Depoları/İndeksleri nasıl oluşturabileceğinizi gösterir.

```python
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import SimpleDirectoryReader, StorageContext

import qdrant_client
from llama_index.core import SimpleDirectoryReader

# Yerel bir Qdrant vektör deposu oluştur
client = qdrant_client.QdrantClient(path="qdrant_mm_db")

# eğer görsel getirme için sadece image_store'a ihtiyacınız varsa,
# text_store'u kaldırabilirsiniz
text_store = QdrantVectorStore(
    client=client, collection_name="metin_koleksiyonu"
)
image_store = QdrantVectorStore(
    client=client, collection_name="gorsel_koleksiyonu"
)

storage_context = StorageContext.from_defaults(
    vector_store=text_store, image_store=image_store
)

# Yerel klasörden metin ve görsel dökümanlarını yükle
documents = SimpleDirectoryReader("./veri_klasoru/").load_data()
# Çok Modlu indeksi oluştur
index = MultiModalVectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
```

3. Aşağıdaki kod parçası, Çok Modlu Retriever ve Sorgu Motorunu (Query Engine) nasıl kullanabileceğinizi gösterir.

```python
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core import PromptTemplate
from llama_index.core.query_engine import SimpleMultiModalQueryEngine

retriever_engine = index.as_retriever(
    similarity_top_k=3, image_similarity_top_k=3
)

# GPT4V yanıtından daha fazla bilgi getir
retrieval_results = retriever_engine.retrieve(response)

# eğer metin getirme olmadan sadece görsel getirmeye ihtiyacınız varsa
# `text_to_image_retrieve` kullanabilirsiniz
# retrieval_results = retriever_engine.text_to_image_retrieve(response)

qa_tmpl_str = (
    "Bağlam bilgisi aşağıdadır.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Bağlam bilgisini kullanarak ve önceden bildiklerinize dayanmadan, "
    "sorguyu yanıtlayın.\n"
    "Sorgu: {query_str}\n"
    "Yanıt: "
)
qa_tmpl = PromptTemplate(qa_tmpl_str)

query_engine = index.as_query_engine(
    multi_modal_llm=openai_mm_llm, text_qa_template=qa_tmpl
)

query_str = "Bana Porsche hakkında daha fazla bilgi ver"
response = query_engine.query(query_str)
```

**Gösterge**

-   ✅ = sorunsuz çalışmalı
-   ⚠️ = bazen güvenilmezdir, iyileştirilmesi için daha fazla ayarlama gerekebilir
-   🛑 = şu an için mevcut değil.

### Uçtan Uca Çok Modlu İş Akışı

Aşağıdaki tablolar, kendi Çok Modlu RAG'lerinizi (Getirme ile Güçlendirilmiş Üretim) oluşturmak için çeşitli LlamaIndex özelliklerini kullanan **başlangıç** adımlarını göstermeyi amaçlamaktadır. Kendi Çok Modlu RAG orkestrasyonunuzu oluşturmak için farklı modülleri/adımları bir araya getirebilirsiniz.

| Sorgu Türü | Çok Modlu Vektör Deposu/İndeksi için Veri Kaynakları | Çok Modlu Embedding | Retriever | Sorgu Motoru | Çıktı Veri Türü |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Metin ✅ | Metin ✅ | Metin ✅ | Top-k getirme ✅<br>Basit Füzyon (Simple Fusion) getirme ✅ | Basit Sorgu Motoru ✅ | Getirilen Metin ✅<br>Oluşturulan Metin ✅ |
| Görsel ✅ | Görsel ✅ | Görsel ✅<br>Görselden Metne Embedding ✅ | Top-k getirme ✅<br>Basit Füzyon (Simple Fusion) getirme ✅ | Basit Sorgu Motoru ✅ | Getirilen Görsel ✅<br>Oluşturulan Görsel 🛑 |
| Ses 🛑 | Ses 🛑 | Ses 🛑 | 🛑 | 🛑 | Ses 🛑 |
| Video 🛑 | Video 🛑 | Video 🛑 | 🛑 | 🛑 | Video 🛑 |

### Çok Modlu LLM Modelleri

Bu not defterleri; Çok Modlu RAG orkestrasyonu oluşturmak için Çok Modlu LLM modelini, Çok Modlu embedding'leri, Çok Modlu vektör depolarını, Retriever'ı ve Sorgu motorunu nasıl kullanabileceğinize ve entegre edebileceğinize dair örnekler sunar.

| Çok Modlu Görü Modelleri | Tek Görsel Muhakemesi | Çoklu Görsel Muhakemesi | Görsel Embedding'leri | Basit Sorgu Motoru | Pydantic Yapılandırılmış Çıktı |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [GPT4V](/python/examples/multi_modal/gpt4v_multi_modal_retrieval)<br>(OpenAI API) | ✅ | ✅ | 🛑 | ✅ | ✅ |
| [GPT4V-Azure](/python/examples/multi_modal/azure_openai_multi_modal)<br>(Azure API) | ✅ | ✅ | 🛑 | ✅ | ✅ |
| [Gemini](/python/examples/multi_modal/gemini)<br>(Google) | ✅ | ✅ | 🛑 | ✅ | ✅ |
| [CLIP](/python/examples/multi_modal/image_to_image_retrieval)<br>(Yerel host) | 🛑 | 🛑 | ✅ | 🛑 | 🛑 |
| [LLaVa](/python/examples/multi_modal/llava_multi_modal_tesla_10q)<br>(replicate) | ✅ | 🛑 | 🛑 | ✅ | ⚠️ |
| [Fuyu-8B](/python/examples/multi_modal/replicate_multi_modal)<br>(replicate) | ✅ | 🛑 | 🛑 | ✅ | ⚠️ |
| [ImageBind<br>](https://imagebind.metademolab.com/)[Entegre edilecek] | 🛑 | 🛑 | ✅ | 🛑 | 🛑 |
| [MiniGPT-4<br>](/python/examples/multi_modal/replicate_multi_modal) | ✅ | 🛑 | 🛑 | ✅ | ⚠️ |
| [CogVLM<br>](https://github.com/THUDM/CogVLM) | ✅ | 🛑 | 🛑 | ✅ | ⚠️ |
| [Qwen-VL<br>](https://arxiv.org/abs/2308.12966)[Entegre edilecek] | ✅ | 🛑 | 🛑 | ✅ | ⚠️ |

### Çok Modlu Vektör Depoları

Aşağıdaki tablo, Çok Modlu kullanım durumlarını destekleyen bazı vektör depolarını listeler. LlamaIndex bünyesindeki `MultiModalVectorStoreIndex`, görsel ve metin embedding vektör depoları için ayrı vektör depoları oluşturmayı destekler. `MultiModalRetriever` ve `SimpleMultiModalQueryEngine`; metinden metne/görsele ve görselden görsele getirmeyi ve metin ile görsel getirme sonuçlarını birleştirmek için basit sıralama füzyon fonksiyonlarını destekler.

| Çok Modlu Vektör Depoları | Tek Vektör Deposu | Çoklu Vektör Deposu | Metin Embedding | Görsel Embedding |
| :--- | :--- | :--- | :--- | :--- |
| [LlamaIndex Kendi Yapımı Çok Modlu İndeks](/python/examples/multi_modal/gpt4v_multi_modal_retrieval) | 🛑 | ✅ | Herhangi bir metin embedding olabilir (Varsayılan GPT3.5) | Herhangi bir görsel embedding olabilir (Varsayılan CLIP) |
| [Chroma](/python/examples/multi_modal/chromamultimodaldemo) | ✅ | 🛑 | CLIP ✅ | CLIP ✅ |
| [Weaviate](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/multi2vec-bind)<br>[Entegre edilecek] | ✅ | 🛑 | CLIP ✅<br>ImageBind ✅ | CLIP ✅<br>ImageBind ✅ |

## Çok Modlu LLM Modülleri

GPT4-V, Anthropic (Opus, Sonnet), Gemini (Google), CLIP (OpenAI), BLIP (Salesforce) ve Replicate (LLaVA, Fuyu-8B, MiniGPT-4, CogVLM) ve daha fazlasıyla entegrasyonları destekliyoruz.

-   [OpenAI](/python/examples/multi_modal/openai_multi_modal)
-   [Gemini](/python/examples/multi_modal/gemini)
-   [Anthropic](/python/examples/multi_modal/anthropic_multi_modal)
-   [Replicate](/python/examples/multi_modal/replicate_multi_modal)
-   [Pydantic Çok Modlu](/python/examples/multi_modal/multi_modal_pydantic)
-   [GPT-4v COT Deneyleri](/python/examples/multi_modal/gpt4v_experiments_cot)
-   [Llava Tesla 10q](/python/examples/multi_modal/llava_multi_modal_tesla_10q)

## Çok Modlu Getirme ile Güçlendirilmiş Üretim (RAG)

Farklı Çok Modlu LLM'ler ve Çok Modlu vektör depoları ile Çok Modlu Getirme ile Güçlendirilmiş Üretim desteği sunuyoruz.

-   [GPT-4v Getirme](/python/examples/multi_modal/gpt4v_multi_modal_retrieval)
-   [Çok Modlu Getirme](/python/examples/multi_modal/multi_modal_retrieval)
-   [Görselden Görsele Getirme](/python/examples/multi_modal/image_to_image_retrieval)
-   [Chroma Çok Modlu](/python/examples/multi_modal/chromamultimodaldemo)

## Değerlendirme

Çok Modlu LLM ve Getirme ile Güçlendirilmiş Üretim için temel değerlendirme desteği sunuyoruz.

-   [Çok Modlu RAG Değerlendirmesi](/python/examples/evaluation/multi_modal/multi_modal_rag_evaluation)