# Aleph Alpha Embedding'leri

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-alephalpha
```

```python
!pip install llama-index
```

```python
# AA belirtecinizle (AA token) başlatın
import os

os.environ["AA_TOKEN"] = "your_token_here"
```

#### `luminous-base` embedding'leri ile.

-   representation="Document" (Belge): Bunu vektör veritabanınızda saklamak istediğiniz metinler (belgeler) için kullanın.
-   representation="Query" (Sorgu): Bunu vektör veritabanınızdaki en alakalı dökümanları bulmak amacıyla kullanılan arama sorguları için kullanın.
-   representation="Symmetric" (Simetrik): Bunu kümeleme, sınıflandırma, anomali tespiti veya görselleştirme görevleri için kullanın.

```python
from llama_index.embeddings.alephalpha import AlephAlphaEmbedding

# Belirtecinizi özelleştirmek için şunu yapın
# aksi takdirde ortam değişkeninizden AA_TOKEN'ı arayacaktır
# embed_model = AlephAlpha(token="<aa_token>")

# representation='Query' ile
embed_model = AlephAlphaEmbedding(
    model="luminous-base",
    representation="Query",
)

embeddings = embed_model.get_text_embedding("Merhaba Aleph Alpha!")

print(len(embeddings))
print(embeddings[:5])
```

    representation_enum: SemanticRepresentation.Query

    5120
    [0.14257812, 2.59375, 0.33203125, -0.33789062, -0.94140625]

```python
# representation='Document' ile
embed_model = AlephAlphaEmbedding(
    model="luminous-base",
    representation="Document",
)

embeddings = embed_model.get_text_embedding("Merhaba Aleph Alpha!")

print(len(embeddings))
print(embeddings[:5])
```

    representation_enum: SemanticRepresentation.Document

    5120
    [0.14257812, 2.59375, 0.33203125, -0.33789062, -0.94140625]