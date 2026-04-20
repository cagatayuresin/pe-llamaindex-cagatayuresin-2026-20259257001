# DashScope Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-core
%pip install llama-index-embeddings-dashscope
```

```python
# API anahtarını ayarla
%env DASHSCOPE_API_KEY=DASHSCOPE_API_ANAHTARINIZ

# API anahtarını parametre olarak da ayarlayabilirsiniz: DashScopeTextEmbedding(model=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2, api_key=api_key)
```

```python
# içe aktarmalar
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)

# Embedding'leri oluştur
# indeks oluşturmak için text_type=`document`
embedder = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
)
text_to_embedding = ["风急天高猿啸哀", "渚清沙白鸟飞回", "无边落木萧萧下", "不尽长江滚滚来"]
# Metin Embedding'ini çağır
result_embeddings = embedder.get_text_embedding_batch(text_to_embedding)
# istekler ve embedding sonucu indeksi birbirine karşılık gelir.
for index, embedding in enumerate(result_embeddings):
    if embedding is None:  # ilgili istek için embedding başarısız olursa.
        print("%s için embedding başarısız oldu." % text_to_embedding[index])
    else:
        print("Embedding boyutu: %s" % len(embedding))
        print(
            "Girdi: %s, embedding sonucu: %s"
            % (text_to_embedding[index], embedding[:5])
        )
```

    Dimension of embeddings: 1536
    Input: 风急天高猿啸哀, embedding is: [-0.0016666285653348784, 0.008690492014557004, 0.02894828715284365, -0.01774133615134858, 0.03627544697161321]
    Dimension of embeddings: 1536
    Input: 渚清沙白鸟飞回, embedding is: [0.018255604113922633, 0.030631669725945727, 0.0031333343045102462, 0.014323813963475412, 0.009666154862176396]
    Dimension of embeddings: 1536
    Input: 无边落木萧萧下, embedding is: [-0.01270165436681136, 0.011355212676752505, -0.007090375205285297, 0.008317427977013809, 0.0341982923839579]
    Dimension of embeddings: 1536
    Input: 不尽长江滚滚来, embedding is: [0.003449439128962428, 0.02667092110022496, -0.0010223853088419568, -0.00971414215183749, 0.0035561228133633277]

```python
# içe aktarmalar
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)

# Embedding'leri oluştur
# ilgili bağlamı getirmek için text_type=`query`
embedder = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_QUERY,
)
# Metin Embedding'ini çağır
embedding = embedder.get_text_embedding("衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买")
print(f"Embedding boyutu: {len(embedding)}")
print(embedding[:5])
```

    Dimension of embeddings: 1536
    [-0.00838587212517078, 0.01004877272531103, 0.0015754734226650637, -0.04273583173235969, -0.05209946086276315]

```python
# toplu metin embedding'ini çağır
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeBatchTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)

embedder = DashScopeEmbedding(
    model_name=DashScopeBatchTextEmbeddingModels.TEXT_EMBEDDING_ASYNC_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
)

embedding_result_file_url = embedder.get_batch_text_embedding(
    embedding_file_url="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/text/text-embedding-test.txt"
)
print(embedding_result_file_url)
```

    https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/5fc5c860/2024-01-29/644ccedb-0b14-481c-a975-16bb5249282d_output_1706517940902.txt.gz?Expires=1706777144&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=g%2B0qcmOSwxEj8Cb2zXlvBbA6Fas%3D

```python
# çok modlu (multimodal) embedding servisini çağır
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeMultiModalEmbeddingModels,
)

embedder = DashScopeEmbedding(
    model_name=DashScopeMultiModalEmbeddingModels.MULTIMODAL_EMBEDDING_ONE_PEACE_V1,
)

embedding = embedder.get_image_embedding(
    img_file_path="https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
)
print(f"Embedding boyutu: {len(embedding)}")
print(embedding[:5])
```

    Dimension of embeddings: 1536
    [-0.03515625, 0.05035400390625, 0.008087158203125, 0.0163116455078125, 0.01064300537109375]

```python
# çok modlu (multimodal) embedding servisini çağır
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeMultiModalEmbeddingModels,
)

embedder = DashScopeEmbedding(
    model_name=DashScopeMultiModalEmbeddingModels.MULTIMODAL_EMBEDDING_ONE_PEACE_V1,
)

input = [
    {"factor": 1, "text": "Merhaba"},
    {
        "factor": 2,
        "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/cow.flac",
    },
    {
        "factor": 3,
        "image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png",
    },
]

embedding = embedder.get_multimodal_embedding(input=input)
print(f"Embedding boyutu: {len(embedding)}")
print(embedding[:5])
```

    Dimension of embeddings: 1536
    [-0.0200169887393713, 0.041749317198991776, 0.01004155445843935, 0.03983306884765625, -0.006652673240751028]