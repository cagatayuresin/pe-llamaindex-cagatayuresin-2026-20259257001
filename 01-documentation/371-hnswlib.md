---
title: Hnswlib
 | LlamaIndex OSS Belgeleri
---

# Hnswlib

Hnswlib, hızlı bir yaklaşık en yakın komşu (approximate nearest neighbor) arama indeksidir. C++11 dışında hiçbir bağımlılığı olmayan, hafif, yalnızca başlıktan oluşan (header-only) bir C++ HNSW uygulamasıdır. Hnswlib, Python bağlamaları sağlar.

```bash
%pip install llama-index
%pip install llama-index-vector-stores-hnswlib
%pip install llama-index-embeddings-huggingface
%pip install hnswlib
```

### Paket bağımlılıklarını içe aktarın

```python
from llama_index.vector_stores.hnswlib import HnswlibVectorStore
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
```

### Örnek veriyi yükleyin

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Veriyi okuyun

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
print(f"Toplam belge sayısı: {len(documents)}")
print(f"İlk belge, kimlik (id): {documents[0].doc_id}")
print(f"İlk belge, hash: {documents[0].hash}")
print(
    "İlk belge metni"
    f" ({len(documents[0].text)} karakter):\n{'='*20}\n{documents[0].text[:360]} ..."
)
```

### Gömme (embedding) modelini yükleyin

```python
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    normalize=True,
)
```

### Hnswlib.Index parametrelerinden HnswlibVectorStore nesnesi oluşturun

```python
hnswlib_vector_store = HnswlibVectorStore.from_params(
    space="ip",
    dimension=embed_model._model.get_sentence_embedding_dimension(),
    max_elements=1000,
)
```

Alternatif olarak, kendiniz bir `Hnswlib.Index` nesnesi oluşturabilirsiniz.

```python
import hnswlib


index = hnswlib.Index(
    "ip", embed_model._model.get_sentence_embedding_dimension()
)
index.init_index(max_elements=1000)


hnswlib_vector_store = HnswlibVectorStore(index)
```

### Belgelerden indeks oluşturun

```python
hnswlib_storage_context = StorageContext.from_defaults(
    vector_store=hnswlib_vector_store
)
hnswlib_index = VectorStoreIndex.from_documents(
    documents,
    storage_context=hnswlib_storage_context,
    embed_model=embed_model,
    show_progress=True,
)
```

### İndeksi sorgulayın

```python
k = 5
query = "Üniversiteden önce yeni başlayanların yazması gerekenleri yazdım."
hnswlib_vector_retriever = hnswlib_index.as_retriever(similarity_top_k=k)
nodes_with_scores = hnswlib_vector_retriever.retrieve(
    query
)
for node in nodes_with_scores:
    print(f"Düğüm (Node) {node.id_} | Puan (Score): {node.score:.3f} - {node.text[:120]}...")
```
