# Ollama Gömmeleri (Embeddings)

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.


```python
%pip install llama-index-embeddings-ollama
```


```python
from llama_index.embeddings.ollama import OllamaEmbedding

ollama_embedding = OllamaEmbedding(
    model_name="embeddinggemma",
    base_url="http://localhost:11434",
    # İsteğe bağlı olarak ollama'ya ek anahtar kelime argümanları (kwargs) geçirebilirsiniz
    # ollama_additional_kwargs={"mirostat": 0},
)
```

Şu yöntemlerden birini kullanarak gömmeler oluşturabilirsiniz:

- `get_text_embedding_batch`
- `get_text_embedding`
- `get_query_embedding`

Ayrıca asenkron versiyonları:
- `aget_text_embedding_batch`
- `aget_text_embedding`
- `aget_query_embedding`


```python
embeddings = ollama_embedding.get_text_embedding_batch(
    ["Bu bir pasajdır!", "Bu başka bir pasajdır"], show_progress=True
)
print(f"{len(embeddings[0])} uzunluğunda vektörler alındı")
print(embeddings[0][:10])
```

    Gömmeler oluşturuluyor: 100%|██████████| 2/2 [00:00<00:00,  3.66it/s]

    768 uzunluğunda vektörler alındı
    [-0.19284482, -0.0048683924, 0.011490762, -0.035292886, 0.0018508184, 0.013227936, -0.045588765, 0.027076142, 0.03387062, -0.030585105]


    



```python
embedding = ollama_embedding.get_text_embedding(
    "Bu bir metin parçasıdır!",
)
print(f"{len(embedding)} uzunluğunda vektörler alındı")
print(embedding[:10])
```

    768 uzunluğunda vektörler alındı
    [-0.18305846, -0.009758809, 0.022796445, -0.038445882, -0.00894579, 0.023117013, -0.05166001, 0.037556227, 0.03699912, -0.017603736]



```python
embedding = ollama_embedding.get_query_embedding(
    "Bu bir sorgudur!",
)
print(f"{len(embedding)} uzunluğunda vektörler alındı")
print(embedding[:10])
```

    768 uzunluğunda vektörler alındı
    [-0.19484262, -0.014648143, 0.02743501, -0.015000358, 0.0027351314, 0.019096522, -0.071097225, 0.033618074, 0.05173764, -0.024861954]