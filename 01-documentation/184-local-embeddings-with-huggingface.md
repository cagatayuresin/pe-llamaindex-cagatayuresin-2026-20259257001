# HuggingFace ile Yerel (Local) Embedding'ler

LlamaIndex; BGE, Mixedbread, Nomic, Jina, E5 gibi Sentence Transformer modelleri dahil olmak üzere HuggingFace embedding modellerini destekler. Bu modelleri dökümanlarımız ve erişim sorgularımız için embedding oluşturmada kullanabiliriz.

Ayrıca, HuggingFace'in [Optimum kütüphanesini](https://huggingface.co/docs/optimum) kullanarak ONNX ve OpenVINO modelleri oluşturmak ve kullanmak için yardımcı araçlar sağlıyoruz.

## HuggingFaceEmbedding

Temel `HuggingFaceEmbedding` sınıfı, embedding işlemleri için herhangi bir HuggingFace modeli etrafında oluşturulmuş genel bir sarmalayıcıdır. Hugging Face üzerindeki tüm [embedding modelleri](https://huggingface.co/models?library=sentence-transformers) çalışmalıdır. Daha fazla öneri için [embedding liderlik tablosuna (leaderboard)](https://huggingface.co/spaces/mteb/leaderboard) bakabilirsiniz.

Bu sınıf, `pip install sentence-transformers` komutuyla kurabileceğiniz `sentence-transformers` paketine bağlıdır.

NOT: Daha önce LangChain'den `HuggingFaceEmbeddings` kullanıyorsanız, bu sınıf size eşdeğer sonuçlar verecektir.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-huggingface
```

```python
!pip install llama-index
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# https://huggingface.co/BAAI/bge-small-en-v1.5 adresini yükler
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

```python
embeddings = embed_model.get_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

    384
    [-0.003275700844824314, -0.011690810322761536, 0.041559211909770966, -0.03814814239740372, 0.024183044210076332]

## Kıyaslama (Benchmarking)

Klasik ve büyük bir döküman olan IPCC iklim raporu, bölüm 3'ü kullanarak karşılaştırma yapmayı deneyelim.

```python
!curl https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter03.pdf --output IPCC_AR6_WGII_Chapter03.pdf
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings

documents = SimpleDirectoryReader(
    input_files=["IPCC_AR6_WGII_Chapter03.pdf"]
).load_data()
```

### Temel HuggingFace Embedding'leri

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Varsayılan torch arka ucu (backend) ile BAAI/bge-small-en-v1.5'i yükler
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu",
    embed_batch_size=8,
)
test_embeds = embed_model.get_text_embedding("Merhaba Dünya!")

Settings.embed_model = embed_model
```

```python
%%timeit -r 1 -n 1
index = VectorStoreIndex.from_documents(documents, show_progress=True)
```

    Parsing nodes: 100%|██████████| 172/172 [00:00<00:00, 428.44it/s]
    Generating embeddings: 100%|██████████| 459/459 [00:19<00:00, 23.32it/s]

    20.2 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)

### ONNX Embedding'leri

```python
# pip install sentence-transformers[onnx]

# Onnx arka ucu (backend) ile BAAI/bge-small-en-v1.5'i yükler
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu",
    backend="onnx",
    model_kwargs={
        "provider": "CPUExecutionProvider"
    },  # ONNX için sağlayıcıyı (provider) belirtebilirsiniz, bkz: https://sbert.net/docs/sentence_transformer/usage/efficiency.html
)
test_embeds = embed_model.get_text_embedding("Merhaba Dünya!")

Settings.embed_model = embed_model
```

```python
%%timeit -r 1 -n 1
index = VectorStoreIndex.from_documents(documents, show_progress=True)
```

    Parsing nodes: 100%|██████████| 172/172 [00:00<00:00, 421.63it/s]
    Generating embeddings: 100%|██████████| 459/459 [00:31<00:00, 14.53it/s]

    32.1 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)

### OpenVINO Embedding'leri

```python
# pip install sentence-transformers[openvino]

# OpenVINO arka ucu (backend) ile BAAI/bge-small-en-v1.5'i yükler
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu",
    backend="openvino",  # OpenVINO, CPU'larda çok güçlüdür
    revision="refs/pr/16",  # BAAI/bge-small-en-v1.5'in kendisinin şu an bir OpenVINO modeli yok, ancak yükleyebileceğimiz bir PR (pull request) var: https://huggingface.co/BAAI/bge-small-en-v1.5/discussions/16
    model_kwargs={
        "file_name": "openvino_model_qint8_quantized.xml"
    },  # Optimize edilmiş/kuantize edilmiş (quantized) bir model kullanıyorsak, dosya adını bu şekilde belirtmemiz gerekir
)
test_embeds = embed_model.get_text_embedding("Merhaba Dünya!")

Settings.embed_model = embed_model
```

```python
%%timeit -r 1 -n 1
index = VectorStoreIndex.from_documents(documents, show_progress=True)
```

    Parsing nodes: 100%|██████████| 172/172 [00:00<00:00, 403.15it/s]
    Generating embeddings: 100%|██████████| 459/459 [00:08<00:00, 53.83it/s]

    9.03 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)

### Referanslar

-   [Yerel Embedding Modelleri](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/#local-embedding-models), bunlar gibi yerel modellerin kullanımı hakkında daha fazla bilgi verir.
-   [Sentence Transformers > Çıkarımı Hızlandırma](https://sbert.net/docs/sentence_transformer/usage/efficiency.html), ONNX ve OpenVINO için optimizasyon ve kuantizasyon dahil olmak üzere arka uç seçeneklerinin nasıl etkili bir şekilde kullanılacağına dair kapsamlı dökümantasyon içerir.