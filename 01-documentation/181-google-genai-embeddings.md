# Google GenAI Embedding'leri

Google'ın `google-genai` paketini kullanan LlamaIndex, hem Gemini hem de Vertex AI API'lerinden gelen Google GenAI modellerini kullanarak metinleri gömmenize (embed) olanak tanıyan bir `GoogleGenAIEmbedding` sınıfı sunar.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-google-genai
```

```python
import os

os.environ["GOOGLE_API_KEY"] = "..."
```

## Kurulum

`GoogleGenAIEmbedding`, `google-genai` paketi için bir sarmalayıcıdır (wrapper); bu da hem Gemini hem de Vertex AI API'lerini kutudan çıktığı gibi desteklediği anlamına gelir.

`api_key` değerini doğrudan geçirebilir veya Vertex AI API'sini kullanmak için bir `vertexai_config` geçirebilirsiniz.

Diğer seçenekler arasında `embed_batch_size`, `model_name` ve `embedding_config` bulunur.

Varsayılan model `text-embedding-004`'tür.

```python
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from google.genai.types import EmbedContentConfig

embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    embed_batch_size=100,
    # api anahtarını doğrudan geçirebilirsiniz
    # api_key="...",
    # veya bir vertexai_config geçirebilirsiniz
    # vertexai_config={
    #     "project": "...",
    #     "location": "...",
    # }
    # bir embedding_config de geçirebilirsiniz
    # embedding_config=EmbedContentConfig(...)
)
```

## Kullanım

### Senkronize (Sync)

```python
embeddings = embed_model.get_text_embedding("Google Gemini Embedding'leri.")
print(embeddings[:5])
print(f"Embedding boyutu: {len(embeddings)}")
```

    [0.031099992, 0.02192731, -0.06523498, 0.016788177, 0.0392835]
    Dimension of embeddings: 768

```python
embeddings = embed_model.get_query_embedding("Google Gemini Embedding'lerini Sorgula.")
print(embeddings[:5])
print(f"Embedding boyutu: {len(embeddings)}")
```

    [0.022199392, 0.03671178, -0.06874573, 0.02195774, 0.05475164]
    Dimension of embeddings: 768

```python
embeddings = embed_model.get_text_embedding_batch(
    [
        "Google Gemini Embedding'leri.",
        "Google harikadır.",
        "Llamaindex harikadır.",
    ]
)
print(f"{len(embeddings)} adet embedding alındı")
print(f"Embedding boyutu: {len(embeddings[0])}")
```

    Got 3 embeddings
    Dimension of embeddings: 768

### Asenkronize (Async)

```python
embeddings = await embed_model.aget_text_embedding("Google Gemini Embedding'leri.")
print(embeddings[:5])
print(f"Embedding boyutu: {len(embeddings)}")
```

    [0.031099992, 0.02192731, -0.06523498, 0.016788177, 0.0392835]
    Dimension of embeddings: 768

```python
embeddings = await embed_model.aget_query_embedding(
    "Google Gemini Embedding'lerini Sorgula."
)
print(embeddings[:5])
print(f"Embedding boyutu: {len(embeddings)}")
```

    [0.022199392, 0.03671178, -0.06874573, 0.02195774, 0.05475164]
    Dimension of embeddings: 768

```python
embeddings = await embed_model.aget_text_embedding_batch(
    [
        "Google Gemini Embedding'leri.",
        "Google harikadır.",
        "Llamaindex harikadır.",
    ]
)
print(f"{len(embeddings)} adet embedding alındı")
print(f"Embedding boyutu: {len(embeddings[0])}")
```

    Got 3 embeddings
    Dimension of embeddings: 768