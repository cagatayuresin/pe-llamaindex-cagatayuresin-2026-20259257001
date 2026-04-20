# Metin Gömme Çıkarımı (Text Embedding Inference)

Bu not defteri, `TextEmbeddingInference` gömmelerinin (embeddings) nasıl yapılandırılacağını gösterir.

İlk adım, gömme sunucusunu dağıtmaktır. Ayrıntılı talimatlar için [Text Embeddings Inference resmi deposuna](https://github.com/huggingface/text-embeddings-inference) bakın. Eğer Habana Gaudi/Gaudi 2 üzerinde dağıtım yapıyorsanız [tei-gaudi deposuna](https://github.com/huggingface/tei-gaudi) bakın.

Sunucu dağıtıldıktan sonra, aşağıdaki kod çıkarım (inference) için sunucuya bağlanacak ve gömmeleri iletecektir.

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-text-embeddings-inference
```

```python
!pip install llama-index
```

```python
from llama_index.embeddings.text_embeddings_inference import (
    TextEmbeddingsInference,
)

embed_model = TextEmbeddingsInference(
    model_name="BAAI/bge-large-en-v1.5",  # Çıkarım metnini biçimlendirmek için gereklidir,
    timeout=60,  # saniye cinsinden zaman aşımı
    embed_batch_size=10,  # gömme için toplu işlem boyutu
)
```

```python
embeddings = embed_model.get_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.010597229, 0.05895996, 0.022445679, -0.012046814, -0.03164673]

```python
embeddings = await embed_model.aget_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.010597229, 0.05895996, 0.022445679, -0.012046814, -0.03164673]
