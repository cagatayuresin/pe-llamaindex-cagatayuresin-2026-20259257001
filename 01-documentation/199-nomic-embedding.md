# Nomic Embedding'leri

Nomic; matryoshka öğrenimi (matryoshka learning), 8192 bağlam uzunluğu ve 64 ile 768 arasında değişen boyutlarla uyumlu v1.5 sürümünü yayınladı.

Bu not defterinde, Nomic v1.5 embedding'lerini farklı boyutlarda kullanmayı keşfedeceğiz.

### Kurulum

```python
%pip install -U llama-index llama-index-embeddings-nomic
```

### API Anahtarlarını Ayarlama

```python
nomic_api_key = "<NOMIC API ANAHTARINIZ>"
```

```python
import nest_asyncio

nest_asyncio.apply()

from llama_index.embeddings.nomic import NomicEmbedding
```

#### 128 Boyutunda

```python
embed_model = NomicEmbedding(
    api_key=nomic_api_key,
    dimensionality=128,
    model_name="nomic-embed-text-v1.5",
)

embedding = embed_model.get_text_embedding("Nomic Embedding'leri")
```

```python
print(len(embedding))
```

    128

```python
embedding[:5]
```

    [0.05569458, 0.057922363, -0.30126953, -0.09832764, 0.05947876]

#### 256 Boyutunda

```python
embed_model = NomicEmbedding(
    api_key=nomic_api_key,
    dimensionality=256,
    model_name="nomic-embed-text-v1.5",
)

embedding = embed_model.get_text_embedding("Nomic Embedding'leri")
```

```python
print(len(embedding))
```

    256

```python
embedding[:5]
```

    [0.044708252, 0.04650879, -0.24182129, -0.07897949, 0.04776001]

#### 768 Boyutunda

```python
embed_model = NomicEmbedding(
    api_key=nomic_api_key,
    dimensionality=768,
    model_name="nomic-embed-text-v1.5",
)

embedding = embed_model.get_text_embedding("Nomic Embedding'leri")
```

```python
print(len(embedding))
```

    768

```python
embedding[:5]
```

    [0.027282715, 0.028381348, -0.14758301, -0.048187256, 0.029144287]

#### Hala v1 Nomic Embedding'lerini kullanabilirsiniz

768 sabit embedding boyutuna sahiptir.

```python
embed_model = NomicEmbedding(
    api_key=nomic_api_key, model_name="nomic-embed-text-v1"
)

embedding = embed_model.get_text_embedding("Nomic Embedding'leri")
```

```python
print(len(embedding))
```

    768

```python
embedding[:5]
```

    [0.0059013367, 0.03744507, 0.0035305023, -0.047180176, 0.0154418945]

### Nomic v1.5 Embedding ile uçtan uca bir RAG boru hattı inşa edelim.

Gerektirme (Generation) adımı için OpenAI kullanacağız.

#### Embedding modelini ve LLM'i ayarlayın.

```python
from llama_index.core import settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

import os

os.environ["OPENAI_API_KEY"] = "<OPENAI API ANAHTARINIZ>"

embed_model = NomicEmbedding(
    api_key=nomic_api_key,
    dimensionality=128,
    model_name="nomic-embed-text-v1.5",
)

llm = OpenAI(model="gpt-3.5-turbo")

settings.llm = llm
settings.embed_model = embed_model
```

#### Veriyi İndir

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

    --2024-02-16 18:37:03--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
    Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8001::154, 2606:50c0:8003::154, 2606:50c0:8000::154, ...
    Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8001::154|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 75042 (73K) [text/plain]
    Saving to: 'data/paul_graham/paul_graham_essay.txt'
    
    data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    in 0.02s   
    
    2024-02-16 18:37:03 (3.87 MB/s) - 'data/paul_graham/paul_graham_essay.txt' saved [75042/75042]

#### Veriyi Yükle

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

#### İndeks Oluşturma

```python
index = VectorStoreIndex.from_documents(documents)
```

#### Sorgu Motoru (Query Engine)

```python
query_engine = index.as_query_engine()
```

```python
response = query_engine.query("yazar büyürken ne yaptı?")
print(response)
```

    Yazar, büyürken yazma ve programlama üzerine çalıştı. Kısa hikayeler yazdı ve ayrıca bir IBM 1401 bilgisayarında programlar yazmayı denedi. Daha sonra bir mikrobilgisayar aldı ve daha kapsamlı programlamaya başlayarak basit oyunlar ve bir kelime işlemci yazdı.