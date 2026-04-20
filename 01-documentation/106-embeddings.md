# Embedding'ler (Embeddings)

## Kavram

LlamaIndex'te dökümanlarınızı gelişmiş bir sayısal temsil kullanarak ifade etmek için Embedding'ler kullanılır. Embedding modelleri girdiyi metin olarak alır ve metnin anlamsal içeriğini yakalamak için kullanılan uzun bir sayı listesi döndürür. Bu embedding modelleri, metni bu şekilde temsil etmek üzere eğitilmiştir ve arama dahil birçok uygulamanın gerçekleştirilmesine yardımcı olur!

Yüksek seviyede, eğer bir kullanıcı köpekler hakkında bir soru sorarsa, o sorunun embedding'i köpeklerden bahseden metinlerle yüksek benzerlik gösterecektir.

Embedding'ler arasındaki benzerliği hesaplarken birçok yöntem kullanılabilir (nokta çarpım (dot product), kosinüs benzerliği (cosine similarity) vb.). LlamaIndex, embedding'leri karşılaştırırken varsayılan olarak kosinüs benzerliğini kullanır.

Seçilebilecek birçok embedding modeli vardır. LlamaIndex varsayılan olarak OpenAI'ın `text-embedding-ada-002` modelini kullanır. Ayrıca Langchain tarafından sunulan tüm embedding modellerini [buradan](https://python.langchain.com/docs/modules/data_connection/text_embedding/) desteklediğimiz gibi, kendi embedding'lerinizi uygulamanız için kolayca genişletilebilir bir temel sınıf da sunuyoruz.

## Kullanım Kalıbı (Usage Pattern)

LlamaIndex'te en yaygın olarak, embedding modelleri `Settings` nesnesinde belirtilir ve ardından bir vektör indeksinde kullanılır. Embedding modeli, indeks oluşturma sırasında kullanılan dökümanları embedding işlemine tabi tutmak ve daha sonra sorgu motorunu kullanarak yaptığınız sorguları embedding işleminden geçirmek için kullanılacaktır. Ayrıca indeks başına da embedding modelleri belirleyebilirsiniz.

Eğer embedding kütüphanelerini henüz yüklemediyseniz:

```bash
pip install llama-index-embeddings-openai
```

Ardından:

```python
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings

# küresel varsayılanı değiştirme
Settings.embed_model = OpenAIEmbedding()

# yerel kullanım
embedding = OpenAIEmbedding().get_text_embedding("merhaba dünya")
embeddings = OpenAIEmbedding().get_text_embeddings(
    ["merhaba dünya", "merhaba dünya"]
)

# indeks başına
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
```

Maliyetlerden tasarruf etmek için yerel bir model kullanmak isteyebilirsiniz.

```bash
pip install llama-index-embeddings-huggingface
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

Bu, [Hugging Face](https://huggingface.co/models?library=sentence-transformers) üzerinde iyi performans gösteren ve hızlı olan bir varsayılan modeli kullanacaktır.

Daha fazla kullanım detayı ve mevcut özelleştirme seçeneklerini aşağıda bulabilirsiniz.

## Başlarken

Bir embedding modeli için en yaygın kullanım, onu küresel `Settings` nesnesinde ayarlamak ve ardından bir indeks oluşturup sorgulama yapmak için kullanmaktır. Giriş dökümanları node'lara bölünecek ve embedding modeli her bir node için bir embedding oluşturacaktır.

Varsayılan olarak LlamaIndex `text-embedding-ada-002` kullanacaktır; aşağıdaki örnek bunu sizin için manuel olarak kurar.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# küresel varsayılan
Settings.embed_model = OpenAIEmbedding()

documents = SimpleDirectoryReader("./data").load_data()

index = VectorStoreIndex.from_documents(documents)
```

Ardından, sorgu zamanında, sorgu metnini embedding işleminden geçirmek için embedding modeli tekrar kullanılacaktır.

```python
query_engine = index.as_query_engine()

response = query_engine.query("sorgu dizesi")
```

## Özelleştirme

### Grup Boyutu (Batch Size)

Varsayılan olarak, embedding istekleri OpenAI'a 10'luk gruplar (batches) halinde gönderilir. Bazı kullanıcılar için bu (nadiren) bir hız sınırına (rate limit) neden olabilir. Birçok dökümanı embedding işleminden geçiren diğer kullanıcılar için ise bu grup boyutu çok küçük olabilir.

```python
# grup boyutunu 42 olarak ayarlayın
embed_model = OpenAIEmbedding(embed_batch_size=42)
```

### Yerel Embedding Modelleri

Yerel bir model kullanmanın en kolay yolu, `llama-index-embeddings-huggingface` paketinden [`HuggingFaceEmbedding`](https://docs.llamaindex.ai/en/stable/api_reference/embeddings/huggingface/#llama_index.embeddings.huggingface.HuggingFaceEmbedding) sınıfını kullanmaktır:

```python
# pip install llama-index-embeddings-huggingface
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

Bu kod, [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) embedding modelini yükler. [Hugging Face üzerindeki herhangi bir Sentence Transformers embedding modelini](https://huggingface.co/models?library=sentence-transformers) kullanabilirsiniz.

[`HuggingFaceEmbedding`](https://docs.llamaindex.ai/en/stable/api_reference/embeddings/huggingface/#llama_index.embeddings.huggingface.HuggingFaceEmbedding) yapılandırıcısındaki anahtar kelime argümanlarının ötesinde; `backend`, `model_kwargs`, `truncate_dim`, `revision` gibi ek argümanlar alt katmandaki [`SentenceTransformer` örneğine](https://sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html) aktarılır.

### ONNX veya OpenVINO Optimizasyonları

LlamaIndex, [Sentence Transformers](https://sbert.net) ve [Optimum](https://huggingface.co/docs/optimum/index) kütüphanelerine güvenerek yerel çıkarımı (inference) hızlandırmak için ONNX veya OpenVINO kullanımını da destekler.

Bazı ön gereksinimler:

```bash
pip install llama-index-embeddings-huggingface
# Artı aşağıdakilerden herhangi biri:
pip install optimum[onnxruntime-gpu] # GPU'larda ONNX için
pip install optimum[onnxruntime]     # CPU'larda ONNX için
pip install optimum-intel[openvino]  # OpenVINO için
```

Model ve çıktı yolunu belirterek oluşturma:

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    backend="onnx",  # veya "openvino"
)
```

Eğer model deposu zaten bir ONNX veya OpenVINO modeli içermiyorsa, Optimum kullanılarak otomatik olarak dönüştürülecektir.
Çeşitli seçeneklerin kıyaslamaları (benchmarks) için [Sentence Transformers dökümantasyonuna](https://sbert.net/docs/sentence_transformer/usage/efficiency.html#benchmarks) bakın.

<details><summary>Peki ya yerine optimize edilmiş veya kuantize edilmiş bir model kontrol noktası (checkpoint) kullanmak istersem?</summary>
Embedding modellerinin birden fazla ONNX ve/veya OpenVINO kontrol noktasına sahip olması yaygındır; örneğin <a href="https://huggingface.co/sentence-transformers/all-mpnet-base-v2/tree/main">sentence-transformers/all-mpnet-base-v2</a> modelinin <a href="https://huggingface.co/sentence-transformers/all-mpnet-base-v2/tree/main/openvino">2 adet OpenVINO kontrol noktası</a> ve <a href="https://huggingface.co/sentence-transformers/all-mpnet-base-v2/tree/main/onnx">9 adet ONNX kontrol noktası</a> vardır. Bu seçeneklerin her biri ve beklenen performansları hakkında daha fazla detay için <a href="https://sbert.net/docs/sentence_transformer/usage/efficiency.html">Sentence Transformers dökümantasyonuna</a> bakın.

Belirli bir kontrol noktasını yüklemek için <code>model_kwargs</code> argümanında bir <code>file_name</code> belirtebilirsiniz. Örneğin, <code>sentence-transformers/all-mpnet-base-v2</code> model deposundan <code>openvino/openvino_model_qint8_quantized.xml</code> kontrol noktasını yüklemek için:

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

quantized_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2",
    backend="openvino",
    device="cpu",
    model_kwargs={"file_name": "openvino/openvino_model_qint8_quantized.xml"},
)
Settings.embed_model = quantized_model
```

</details>

<details><summary>CPU'larda hangi seçeneği kullanmalıyım?</summary>

Sentence Transformers dökümantasyonunda gösterildiği gibi, int8'e kuantize edilmiş OpenVINO (<code>openvino_model_qint8_quantized.xml</code>), doğrulukta küçük bir kayıp karşılığında son derece performanslıdır. Özdeş sonuçlar elde etmek istiyorsanız, temel <code>backend="openvino"</code> veya <code>backend="onnx"</code> en güçlü seçenekler olabilir.

<img src="https://sbert.net/_images/backends_benchmark_cpu.png" alt="CPU Arka Uç Kıyaslaması">

Bu sorgu ve bu dökümanlar göz önüne alındığında, int8 kuantize edilmiş OpenVINO ile varsayılan Hugging Face modeli karşılaştırıldığında aşağıdaki sonuçlar elde edilmiştir:

```python
query = "Hangi gezegen Kızıl Gezegen olarak bilinir?"
documents = [
    "Venüs, benzer boyutu ve yakınlığı nedeniyle genellikle Dünya'nın ikizi olarak adlandırılır.",
    "Kırmızımsı görünümüyle bilinen Mars, genellikle Kızıl Gezegen olarak anılır.",
    "Güneş sistemimizdeki en büyük gezegen olan Jüpiter belirgin bir kırmızı lekeye sahiptir.",
    "Halkalarıyla ünlü olan Satürn, bazen Kızıl Gezegen ile karıştırılır.",
]
```

```
HuggingFaceEmbedding(device='cpu'):
- Ortalama çıktı (throughput): 38.20 sorgu/sn (5 çalışma üzerinden)
- Sorgu-döküman benzerlikleri tensor([[0.7783, 0.4654, 0.6919, 0.7010]])

HuggingFaceEmbedding(backend='openvino', device='cpu', model_kwargs={'file_name': 'openvino_model_qint8_quantized.xml'}):
- Ortalama çıktı (throughput): 266.08 sorgu/sn (5 çalışma üzerinden)
- Sorgu-döküman benzerlikleri tensor([[0.7492, 0.4623, 0.6606, 0.6556]])
```

Bu, aynı döküman sıralamasını korurken 6.97 kat hızlanma demektir.

<details><summary>Yeniden üretim (reproduction) betiğini görmek için tıklayın</summary>

```python
import time
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

quantized_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2",
    backend="openvino",
    device="cpu",
    model_kwargs={"file_name": "openvino/openvino_model_qint8_quantized.xml"},
)
quantized_model_desc = "HuggingFaceEmbedding(backend='openvino', device='cpu', model_kwargs={'file_name': 'openvino_model_qint8_quantized.xml'})"
baseline_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2",
    device="cpu",
)
baseline_model_desc = "HuggingFaceEmbedding(device='cpu')"

query = "Hangi gezegen Kızıl Gezegen olarak bilinir?"


def bench(model, query, description):
    for _ in range(3):
        model.get_agg_embedding_from_queries([query] * 32)

    sentences_per_second = []
    for _ in range(5):
        queries = [query] * 512
        start_time = time.time()
        model.get_agg_embedding_from_queries(queries)
        sentences_per_second.append(len(queries) / (time.time() - start_time))

    print(
        f"{description:<120}: Ortalama çıktı: {sum(sentences_per_second) / len(sentences_per_second):.2f} sorgu/sn (5 çalışma üzerinden)"
    )


bench(baseline_model, query, baseline_model_desc)
bench(quantized_model, query, quantized_model_desc)

# Benzerlik karşılaştırması için örnek dökümanlar. İlki doğru olan, diğerleri çeldiricidir.
docs = [
    "Kırmızımsı görünümüyle bilinen Mars, genellikle Kızıl Gezegen olarak anılır.",
    "Venüs, benzer boyutu ve yakınlığı nedeniyle genellikle Dünya'nın ikizi olarak adlandırılır.",
    "Güneş sistemimizdeki en büyük gezegen olan Jüpiter belirgin bir kırmızı lekeye sahiptir.",
    "Halkalarıyla ünlü olan Satürn, bazen Kızıl Gezegen ile karıştırılır.",
]

baseline_query_embedding = baseline_model.get_query_embedding(query)
baseline_doc_embeddings = baseline_model.get_text_embedding_batch(docs)

quantized_query_embedding = quantized_model.get_query_embedding(query)
quantized_doc_embeddings = quantized_model.get_text_embedding_batch(docs)

baseline_similarity = baseline_model._model.similarity(
    baseline_query_embedding, baseline_doc_embeddings
)
print(
    f"{baseline_model_desc:<120}: Sorgu-döküman benzerlikleri {baseline_similarity}"
)
quantized_similarity = quantized_model._model.similarity(
    quantized_query_embedding, quantized_doc_embeddings
)
print(
    f"{quantized_model_desc:<120}: Sorgu-döküman benzerlikleri {quantized_similarity}"
)
```

</details>

</details>

<details><summary>GPU'larda hangi seçeneği kullanmalıyım?</summary>

GPU'larda OpenVINO pek ilgi çekici değildir ve ONNX, varsayılan <code>torch</code> arka ucunda çalışan kuantize edilmiş bir modeli mutlaka geçemez.

<img src="https://sbert.net/_images/backends_benchmark_gpu.png" alt="GPU Arka Uç Kıyaslaması">

Bu, GPU'larda güçlü bir hızlanma için ek bağımlılıklara ihtiyacınız olmadığı anlamına gelir; modeli yüklerken daha düşük bir hassasiyet (precision) kullanmanız yeterlidir:

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cuda",
    model_kwargs={"torch_dtype": "float16"},
)
```

</details>

<details><summary>Ya istediğim modelde istediğim arka uç ve optimizasyon veya kuantizasyon yoksa?</summary>

<a href="https://huggingface.co/spaces/sentence-transformers/backend-export">backend-export</a> Hugging Face Alanı (Space), herhangi bir Sentence Transformers modelini ONNX veya OpenVINO'ya, kuantizasyon veya optimizasyon uygulanmış olarak dönüştürmek için kullanılabilir. Bu, dönüştürülmüş model dosyalarıyla model deposuna bir çekme isteği (pull request) oluşturacaktır. Daha sonra LlamaIndex'te bu modeli <code>revision</code> argümanını kullanarak şu şekilde kullanabilirsiniz:

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    backend="openvino",
    revision="refs/pr/16",  # çekme isteği 16 için: https://huggingface.co/BAAI/bge-small-en-v1.5/discussions/16
    model_kwargs={"file_name": "openvino_model_qint8_quantized.xml"},
)
```

</details>

### LangChain Entegrasyonları

Ayrıca Langchain tarafından sunulan tüm embedding'leri de destekliyoruz ([burada](https://python.langchain.com/docs/modules/data_connection/text_embedding/) bulabilirsiniz).

Aşağıdaki örnek, Langchain'in embedding sınıfını kullanarak Hugging Face'ten bir model yükler.

```bash
pip install llama-index-embeddings-langchain
```

```python
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index.core import Settings

Settings.embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en")
```

### Özel Embedding Modeli

Eğer LlamaIndex veya Langchain tarafından sunulmayan embedding'leri kullanmak isterseniz, temel embedding sınıfımızı genişletebilir ve kendi sınıfınızı uygulayabilirsiniz!

Aşağıdaki örnek Instructor Embedding'leri kullanır ([kurulum/ayarlar burada](https://huggingface.co/hkunlp/instructor-large)) ve özel bir embedding sınıfı uygular. Instructor embedding'leri, metni ve embedding işleminin yapılacağı metnin alanına (domain) dair "talimatları" (instructions) sağlayarak çalışır. Bu, çok spesifik ve uzmanlık gerektiren bir konudan metin embedding işlemi yaparken yardımcı olur.

```python
from typing import Any, List
from InstructorEmbedding import INSTRUCTOR
from llama_index.core.embeddings import BaseEmbedding


class InstructorEmbeddings(BaseEmbedding):
    def __init__(
        self,
        instructor_model_name: str = "hkunlp/instructor-large",
        instruction: str = "Bilgisayar Bilimi dökümanını veya sorusunu temsil et:",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._model = INSTRUCTOR(instructor_model_name)
        self._instruction = instruction

    def _get_query_embedding(self, query: str) -> List[float]:
        embeddings = self._model.encode([[self._instruction, query]])
        return embeddings[0]

    def _get_text_embedding(self, text: str) -> List[float]:
        embeddings = self._model.encode([[self._instruction, text]])
        return embeddings[0]

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self._model.encode(
            [[self._instruction, text] for text in texts]
        )
        return embeddings

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)
```

## Bağımsız Kullanım (Standalone Usage)

Embedding'leri projeniz, mevcut uygulamanız veya genel test ve keşif işlemleriniz için bağımsız bir modül olarak da kullanabilirsiniz.

```python
embeddings = embed_model.get_text_embedding(
    "Burada bardaktan boşalırcasına yağmur yağıyor!"
)
```

## Desteklenen Embedding Listesi

OpenAI, Azure ve LangChain'in sunduğu her şeyle entegrasyonu destekliyoruz.

-   [Azure OpenAI](/python/examples/customization/llms/azureopenai)
-   [Clarifai](/python/examples/embeddings/clarifai)
-   [Cohere](/python/examples/embeddings/cohereai)
-   [Özel (Custom)](/python/examples/embeddings/custom_embeddings)
-   [Dashscope](/python/examples/embeddings/dashscope_embeddings)
-   [ElasticSearch](/python/examples/embeddings/elasticsearch)
-   [FastEmbed](/python/examples/embeddings/fastembed)
-   [Google Palm](/python/examples/embeddings/google_palm)
-   [Anyscale](/python/examples/embeddings/anyscale)
-   [Huggingface](/python/examples/embeddings/huggingface)
-   [JinaAI](/python/examples/embeddings/jinaai_embeddings)
-   [Langchain](/python/examples/embeddings/langchain)
-   [LLM Rails](/python/examples/embeddings/llm_rails)
-   [MistralAI](/python/examples/embeddings/mistralai)
-   [OpenAI](/python/examples/embeddings/openai)
-   [Sagemaker](/python/examples/embeddings/sagemaker_embedding_endpoint)
-   [Text Embedding Inference](/python/examples/embeddings/text_embedding_inference)
-   [TogetherAI](/python/examples/embeddings/together)
-   [Upstage](/python/examples/embeddings/upstage)
-   [VoyageAI](/python/examples/embeddings/voyageai)
-   [Nomic](/python/examples/embeddings/nomic)
-   [Fireworks AI](/python/examples/embeddings/fireworks)