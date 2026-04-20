# Upstage Gömmeleri (Embeddings)

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.


```python
%pip install llama-index-embeddings-upstage==0.2.1
```


```python
!pip install llama-index
```


```python
import os

os.environ["UPSTAGE_API_KEY"] = "API_ANAHTARINIZ"
```


```python
from llama_index.embeddings.upstage import UpstageEmbedding
from llama_index.core import Settings

embed_model = UpstageEmbedding()
Settings.embed_model = embed_model
```

## Upstage Gömmelerini Kullanma

Not: openai istemcinizi güncellemeniz gerekebilir: `pip install -U openai`


```python
# API anahtarını alın ve gömmeleri oluşturun
from llama_index.embeddings.upstage import UpstageEmbedding

embed_model = UpstageEmbedding()

embeddings = embed_model.get_text_embedding(
    "Upstage'in yeni gömme modelleri harika."
)
```


```python
print(embeddings[:5])
```

    [0.02535058930516243, 0.007272760849446058, 0.015372460708022118, -0.007840132340788841, 0.0017625312320888042]



```python
print(len(embeddings))
```

    4096



```python
embeddings = embed_model.get_query_embedding(
    "Bazı harika gömme modelleri nelerdir?"
)
```


```python
print(embeddings[:5])
```

    [0.03518765792250633, 0.01018011849373579, 0.013282101601362228, -0.008568626828491688, -0.005505830980837345]



```python
print(len(embeddings))
```

    4096



```python
# belgeleri gömme
embeddings = embed_model.get_text_embedding_batch(
    [
        "Upstage'in yeni gömme modelleri müthiş.",
        "Upstage LLM de müthiş.",
    ]
)
```


```python
print(len(embeddings))
```

    2



```python
print(embeddings[0][:5])
```

    [0.028246860951185226, 0.008945596404373646, 0.01719627156853676, -0.005711239762604237, 0.0016300849383696914]