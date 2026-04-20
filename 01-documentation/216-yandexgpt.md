# YandexGPT

```python
%pip install llama-index-embeddings-yandexgpt
```

```python
!pip install llama-index
```

```python
from llama_index.embeddings.yandexgpt import YandexGPTEmbedding

yandexgpt_embedding = YandexGPTEmbedding(
    api_key="api-anahtarınız", folder_id="klasör-kimliğiniz"
)

text_embedding = yandexgpt_embedding._get_text_embeddings(
    ["Bu bir pasajdır!", "Bu başka bir pasajdır"]
)
print(text_embedding)

query_embedding = yandexgpt_embedding._get_query_embedding("Mavi nerede?")
print(query_embedding)
```
