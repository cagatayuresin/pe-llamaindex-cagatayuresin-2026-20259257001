---
title: Neo4j Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Neo4j Vektör Deposu

Eğer bu Not Defterini colab'de açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-neo4jvector
```

```bash
!pip install llama-index
```

```python
import os
import openai


os.environ["OPENAI_API_KEY"] = "OPENAI_API_ANAHTARINIZ"
openai.api_key = os.environ["OPENAI_API_KEY"]
```

## Neo4j Vektör Sarmalayıcısını Başlatın

```python
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore


username = "neo4j"
password = "sifre"
url = "bolt://localhost:7687"
embed_dim = 1536


neo4j_vector = Neo4jVectorStore(username, password, url, embed_dim)
```

## Belgeleri Yükleyin, VectorStoreIndex Oluşturun

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from IPython.display import Markdown, display
```

Veriyi İndir

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
# belgeleri yükle
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
```

```python
from llama_index.core import StorageContext


storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Interleaf'te ne oldu?")
display(Markdown(f"<b>{response}</b>"))
```

**Interleaf'te, Emacs'tan esinlenen bir betik dili eklediler ve bunu Lisp'in bir lehçesi yaptılar. Bu betik dilinde bir şeyler yazması için bir Lisp korsanı (hacker) arıyorlardı. Metnin yazarı Interleaf'te çalışmıştı ve Lisp'lerinin dev bir C keki üzerindeki en ince krema tabakası olduğunu belirtmişti. Yazar ayrıca C bilmediğini ve öğrenmek istemediğini, bu yüzden Interleaf'teki yazılımların çoğunu asla anlamadığını söylemişti. Ek olarak yazar, kötü bir çalışan olduğunu ve zamanının çoğunu "On Lisp" adlı ayrı bir proje üzerinde çalışarak geçirdiğini itiraf etmişti.**

## Hibrit arama

Hibrit arama, anahtar kelime ve vektör aramasının bir kombinasyonunu kullanır. Hibrit aramayı kullanmak için `hybrid_search` parametresini `True` olarak ayarlamanız gerekir.

```python
neo4j_vector_hybrid = Neo4jVectorStore(
    username, password, url, embed_dim, hybrid_search=True
)
```

```python
storage_context = StorageContext.from_defaults(
    vector_store=neo4j_vector_hybrid
)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
query_engine = index.as_query_engine()
response = query_engine.query("Interleaf'te ne oldu?")
display(Markdown(f"<b>{response}</b>"))
```

**Interleaf'te, Emacs'tan esinlenen bir betik dili eklediler ve bunu Lisp'in bir lehçesi yaptılar. Bu betik dilinde bir şeyler yazacak bir Lisp korsanı arıyorlardı. Makalenin yazarı Interleaf'te çalışmıştı ancak C bilmediği ve öğrenmek istemediği için yazılımların çoğunu anlamamıştı. Ayrıca Lisp'lerinin dev bir C keki üzerindeki en ince krema tabakası olduğunu belirtmişti. Yazar, kötü bir çalışan olduğunu ve zamanının çoğunu "On Lisp" kitabını yayınlamak için bir sözleşme üzerinde çalışarak geçirdiğini itiraf etmişti.**

## Mevcut vektör indeksini yükleyin

Mevcut bir vektör indeksine bağlanmak için `index_name` ve `text_node_property` parametrelerini tanımlamanız gerekir:

- `index_name`: Mevcut vektör indeksinin adı (varsayılan: `vector`)
- `text_node_property`: Metin değerini içeren özelliğin (property) adı (varsayılan: `text`)

```python
index_name = "existing_index"
text_node_property = "text"
existing_vector = Neo4jVectorStore(
    username,
    password,
    url,
    embed_dim,
    index_name=index_name,
    text_node_property=text_node_property,
)


loaded_index = VectorStoreIndex.from_vector_store(existing_vector)
```

## Yanıtları özelleştirme

`retrieval_query` parametresini kullanarak bilgi grafından (knowledge graph) getirilen bilgileri özelleştirebilirsiniz.

Erişim sorgusu (retrieval query) aşağıdaki dört sütunu döndürmelidir:

- `text:str` - Döndürülen belgenin metni
- `score:str` - benzerlik puanı
- `id:str` - düğüm (node) kimliği
- `metadata: Dict` - ek meta verilere sahip sözlük (`_node_type` ve `_node_content` anahtarlarını içermelidir)

```python
retrieval_query = (
    "RETURN 'Interleaf Tomaz'i ise aldi' AS text, score, node.id AS id, "
    "{author: 'Tomaz', _node_type:node._node_type, _node_content:node._node_content} AS metadata"
)
neo4j_vector_retrieval = Neo4jVectorStore(
    username, password, url, embed_dim, retrieval_query=retrieval_query
)
```

```python
loaded_index = VectorStoreIndex.from_vector_store(
    neo4j_vector_retrieval
).as_query_engine()
response = loaded_index.query("Interleaf'te ne oldu?")
display(Markdown(f"<b>{response}</b>"))
```

**Interleaf, Tomaz'ı işe aldı.**
