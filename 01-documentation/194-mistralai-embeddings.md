# MistralAI Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-mistralai
```

```python
!pip install llama-index
```

```python
# içe aktarmalar
from llama_index.embeddings.mistralai import MistralAIEmbedding
```

```python
# API anahtarını al ve embedding oluştur
api_key = "API ANAHTARINIZ"
model_name = "mistral-embed"
embed_model = MistralAIEmbedding(model_name=model_name, api_key=api_key)

embeddings = embed_model.get_text_embedding("La Plateforme - Platform")
```

```python
print(f"Embedding boyutu: {len(embeddings)}")
```

    Dimension of embeddings: 1024

```python
embeddings[:5]
```

    [-0.0299224853515625,
     -0.0028362274169921875,
     0.0282745361328125,
     -0.034759521484375,
     -0.0017366409301757812]