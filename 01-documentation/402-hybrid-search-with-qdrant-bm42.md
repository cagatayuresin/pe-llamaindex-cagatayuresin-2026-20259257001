---
title: Qdrant BM42 ile Hibrit Arama
 | LlamaIndex OSS Belgeleri
---

# Qdrant BM42 ile Hibrit Arama

Qdrant yakın zamanda seyrek gömmelere (sparse embeddings) yönelik yeni ve hafif bir yaklaşım olan [BM42](https://qdrant.tech/articles/bm42/)'yi yayınladı.

Bu not defterinde, verimli bir hibrit arama için BM42'nin llama-index ile nasıl kullanılacağını adım adım inceleyeceğiz.

## Kurulum

Öncelikle birkaç pakete ihtiyacımız var:

- `llama-index`
- `llama-index-vector-stores-qdrant`
- `fastembed` veya `fastembed-gpu`

`llama-index`, gerekli kütüphaneler kuruluysa fastembed modellerini otomatik olarak GPU üzerinde çalıştıracaktır. Kapsamlı kurulum rehberlerini [buradan](https://qdrant.github.io/fastembed/examples/FastEmbed_GPU/) inceleyebilirsiniz.

```bash
%pip install llama-index llama-index-vector-stores-qdrant fastembed
```

## (İsteğe Bağlı) fastembed paketini test etme

Kurulumun başarılı olduğunu onaylamak (ve kullanılıyorsa GPU kullanımını doğrulamak) için aşağıdaki kodu çalıştırabiliriz.

Bu kod öncelikle modeli yerel olarak indirecek (ve önbelleğe alacak), ardından gömme (embedding) işlemini gerçekleştirecektir.

```python
from fastembed import SparseTextEmbedding


model = SparseTextEmbedding(
    model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
    # cuda+onnx kurulu olan fastembed-gpu kullanılıyorsa
    # providers=["CudaExecutionProvider"],
)


embeddings = model.embed(["merhaba dünya", "hoşça kal dünya"])


indices, values = zip(
    *[
        (embedding.indices.tolist(), embedding.values.tolist())
        for embedding in embeddings
    ]
)


print(indices[0], values[0])
```

```bash
Fetching 6 files:   0%|          | 0/6 [00:00<?, ?it/s]




[613153351, 74040069] [0.3703993395381275, 0.3338314745830077]
```

## Hibrit İndeksimizi Oluşturma

llama-index'te sadece birkaç satır kodla hibrit bir indeks oluşturabiliriz.

Geçmişte splade ile hibrit aramayı denediyseniz, bunun çok daha hızlı olduğunu fark edeceksiniz!

### Veri Yükleme

Burada, Llama2 makalesini okumak için `llama-parse` kullanıyoruz! JSON sonuç modunu kullanarak, mizanpaj (layout) ve görseller dahil olmak üzere her sayfa hakkında detaylı veriler elde edebiliriz. Şimdilik sayfa numaralarını ve metni kullanacağız.

`llama-parse` için ücretsiz bir API anahtarını [https://cloud.llamaindex.ai](https://cloud.llamaindex.ai) adresini ziyaret ederek alabilirsiniz.

```bash
!mkdir -p 'data/'
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
```

```python
import nest_asyncio


nest_asyncio.apply()
```

```python
from llama_parse import LlamaParse
from llama_index.core import Document


parser = LlamaParse(result_type="text", api_key="llx-...")


# Her sayfa için sonuçların yanı sıra detaylı mizanpaj bilgisini ve meta veriyi alın
json_data = parser.get_json_result("data/llama2.pdf")


documents = []
for document_json in json_data:
    for page in document_json["pages"]:
        documents.append(
            Document(text=page["text"], metadata={"page_number": page["page"]})
        )
```

```bash
Started parsing the file under job_id cac11eca-4058-4a89-a94a-5603dea3d851
```

### Qdrant ile İndeks Oluşturma

Düğümlerimizle birlikte, Qdrant ve BM42 kullanarak indeksimizi oluşturabiliriz!

Bu senaryoda Qdrant bir docker konteynerı içinde barındırılacaktır.

En son sürümü şu şekilde çekebilirsiniz:

```bash
docker pull qdrant/qdrant
```

Ve ardından başlatmak için:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

```python
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore


client = qdrant_client.QdrantClient("http://localhost:6333")
aclient = qdrant_client.AsyncQdrantClient("http://localhost:6333")


# Koleksiyon mevcutsa sil
if client.collection_exists("llama2_bm42"):
    client.delete_collection("llama2_bm42")


vector_store = QdrantVectorStore(
    collection_name="llama2_bm42",
    client=client,
    aclient=aclient,
    fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions",
)
```

```bash
Hem client (istemci) hem de aclient sağlanmıştır. `:memory:` modu kullanıldığında, istemciler arasındaki veri senkronize edilmez.
```

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    # yoğun gömme (dense embedding) modelimiz
    embed_model=OpenAIEmbedding(
        model_name="text-embedding-3-small", api_key="sk-proj-..."
    ),
    storage_context=storage_context,
)
```

Gördüğümüz üzere, hem yoğun (dense) hem de seyrek (sparse) gömmeler süper hızlı bir şekilde oluşturuldu!

Seyrek model (sparse model) yerel bir CPU üzerinde çalışıyor olmasına rağmen çok küçük ve hızlıdır.

## İndeksi Test Etme

Seyrek gömmelerin gücünü kullanarak çok özel ve spesifik gerçekleri sorgulayabilir ve doğru verileri elde edebiliriz.

```python
from llama_index.llms.openai import OpenAI


chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    llm=OpenAI(model="gpt-4o", api_key="sk-proj-..."),
)
```

```python
response = chat_engine.chat("Llama2 için hangi eğitim donanımı kullanıldı?")
print(str(response))
```

```bash
Llama 2 için eğitim donanımı olarak Meta'nın Araştırma Süper Kümesi (Research Super Cluster - RSC) ve dahili üretim kümeleri yer aldı. Her iki küme de NVIDIA A100 GPU'larını kullandı. Bu kümeler arasında iki önemli fark vardı:


1. **Bağlantı Türü (Interconnect Type)**:
   - RSC, NVIDIA Quantum InfiniBand kullandı.
   - Dahili üretim kümesi, tüketici sınıfı (commodity) Ethernet anahtarlarına dayanan bir RoCE (RDMA over Converged Ethernet) çözümü kullandı.


2. **GPU Başına Güç Tüketim Sınırı**:
   - RSC'de GPU başına güç tüketimi üst sınırı 400W idi.
   - Dahili üretim kümesinde GPU başına güç tüketimi üst sınırı 350W idi.


Bu kurulum, bahsi geçen farklı bağlantı türlerinin büyük ölçekli eğitime olan uygunluğunu karşılaştırmaya olanak tanıdı.
```

```python
response = chat_engine.chat("Llama2'nin ana fikri nedir?")
print(str(response))
```

```bash
Llama 2'nin ana fikri, orijinal Llama modelinin, araştırma ve ticari kullanımlar da dahil olmak üzere çeşitli uygulamalar için daha verimli, ölçeklenebilir ve güvenli olacak şekilde tasarlanmış, güncellenmiş ve geliştirilmiş bir sürümünü sunmaktır. Llama 2'nin temel yönleri şunlardır:


1. **Geliştirilmiş Ön Eğitim**: Llama 2, Llama 1'e kıyasla ön eğitim derlem boyutunda %40 artışla, halka açık verilerin yeni bir karışımı üzerinde eğitilmiştir. Bu, modelin performansını ve bilgi tabanını iyileştirmeyi amaçlamaktadır.


2. **İyileştirilmiş Mimari**: Model, çıkarım ölçeklenebilirliğini ve genel performansı artırmak için daha büyük bağlam uzunluğu (context length) ve gruplandırılmış sorgu dikkati (grouped-query attention - GQA) gibi çeşitli mimari geliştirmeler içerir.


3. **Güvenlik ve Yanıt Verme (Responsiveness)**: Llama 2'nin ince ayarlarla (fine-tune) belirlenmiş bir versiyonu olan Llama 2-Chat, diyalog kullanım senaryoları için optimize edilmiştir. Daha güvenli ve daha yararlı etkileşimler sağlamak için Denetimli İnce Ayar (Supervised Fine-Tuning) ve İnsan Geri Bildirimiyle Pekiştirmeli Öğrenme (RLHF) kullanılarak yinelemeli olarak iyileştirmeden geçer.


4. **Açık Sürüm**: Meta, şeffaflığı ve yapay zeka topluluğundaki iş birliğini teşvik etmek amacıyla Llama 2'nin 7B, 13B ve 70B parametre modellerini araştırma ve ticari kullanım için genel kamuoyuna sunuyor.


5. **Sorumlu Kullanım**: Sürüm paketi, Llama 2 ve Llama 2-Chat'in güvenli dağıtımını kolaylaştırmak için kılavuzlar ve kod örnekleri içerir ve güvenli test ortamlarının ve belirli uygulamalara uyarlanmış ayarlamaların önemini vurgular.


Genel olarak Llama 2, yapay zeka topluluğu tarafından geniş çapta kullanılabilen ve daha da geliştirilebilen daha güçlü, ölçeklenebilir ve daha güvenli bir büyük dil modeli (LLM) olmayı hedefler.
```

```python
response = chat_engine.chat("Llama2 nelerde değerlendirildi ve nelerle karşılaştırıldı?")
print(str(response))
```

```bash
Llama 2, farklı birçok kıyaslama (benchmark) kategorisinde hem açık kaynaklı (open-source) hem de kapalı kaynaklı çeşitli diğer modellerle değerlendirildi ve onlarla karşılaştırıldı. İşte önemli kıyaslamalar:


### Açık Kaynaklı (Open-Source) Modeller:
1. **Llama 1**: Llama 2 modelleri kendinden öncekiler olan Llama 1 modelleriyle karşılaştırıldı. Örneğin, Llama 2 70B, Llama 1 65B'ye kıyasla MMLU'da yaklaşık 5 puanlık ve BBH'de 8 puanlık iyileşme gösterdi.
2. **MPT Modelleri**: Llama 2 7B ve 30B modelleri, kod kıyaslamaları (code benchmarks) hariç tüm kategorilerde aynı boyuttaki MPT modellerinden daha iyi performans gösterdi.
3. **Falcon Modelleri**: Llama 2 7B ve 34B modelleri, tüm kıyaslama kategorilerinde Falcon 7B ve 40B modellerine üstünlük sağladı.


### Kapalı Kaynaklı Modeller:
1. **GPT-3.5**: Llama 2 70B, GPT-3.5 ile karşılaştırıldı ve MMLU ile GSM8K'da yakın bir performans gösterirken, kodlama kıyaslamalarında ciddi bir fark yaşadı.
2. **PaLM (540B)**: Llama 2 70B, neredeyse tüm kıyaslamalarda PaLM'e (540B) denk veya ondan daha iyi bir performans gösterdi.
3. **GPT-4 ve PaLM-2-L**: Llama 2 70B ile bu daha gelişmiş modeller arasında hala büyük bir performans farkı (gap) bulunuyor.


### Kıyaslamalar (Benchmarks):
Llama 2, aralarında şunlar da olan çeşitli kıyaslamalarda değerlendirildi:
1. **MMLU (Massive Multitask Language Understanding)**: 5 adımlı (5-shot) bir ortamda değerlendirildi.
2. **BBH (Big Bench Hard)**: 3 adımlı (3-shot) bir ortamda değerlendirildi.
3. **AGI Eval**: 3-5 adımlı (shot) ortamlarda, İngilizce görevlere odaklanılarak değerlendirildi.
4. **GSM8K**: Matematik problemi çözümü için.
5. **Human-Eval ve MBPP**: Kod üretimi için.
6. **NaturalQuestions ve TriviaQA**: Genel dünya bilgisi için.
7. **SQUAD ve QUAC**: Okuduğunu anlama için.
8. **BoolQ, PIQA, SIQA, Hella-Swag, ARC-e, ARC-c, NQ, TQA**: Dil anlama ve mantık yürütmenin (reasoning) farklı yönleri için diğer çeşitli kıyaslamalar.


Bu değerlendirmeler, Llama 2 modellerinin genel olarak kendilerinden öncekileri ve diğer açık kaynaklı modelleri geride bıraktıklarını ve aynı zamanda önde gelen bazı kapalı kaynaklı modellerle rekabet edebilir olduklarını göstermektedir.
```

## Mevcut depodan yükleme

Vektör indeksinizi oluşturduktan sonra, onu yeniden kolayca bağlayabiliriz!

```python
import qdrant_client
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore


client = qdrant_client.QdrantClient("http://localhost:6333")
aclient = qdrant_client.AsyncQdrantClient("http://localhost:6333")


# Koleksiyon mevcutsa sil
if client.collection_exists("llama2_bm42"):
    client.delete_collection("llama2_bm42")


vector_store = QdrantVectorStore(
    collection_name="llama2_bm42",
    client=client,
    aclient=aclient,
    fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions",
)


loaded_index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=OpenAIEmbedding(
        model="text-embedding-3-small", api_key="sk-proj-..."
    ),
)
```
