# GigaChat

```python
%pip install llama-index-embeddings-gigachat
```

```python
!pip install llama-index
```

```python
from llama_index.embeddings.gigachat import GigaChatEmbedding

gigachat_embedding = GigaChatEmbedding(
    auth_data="yetkilendirme-veriniz",
    scope="kapsamınız",  # Bireysel kullanım için 'GIGACHAT_API_PERS', kurumsal kullanım için 'GIGACHAT_API_CORP' kapsamını seçin.
)

queries_embedding = gigachat_embedding._get_query_embeddings(
    ["Bu bir pasajdır!", "Bu başka bir pasajdır"]
)
print(queries_embedding)

text_embedding = gigachat_embedding._get_text_embedding("Mavi nerede?")
print(text_embedding)
```