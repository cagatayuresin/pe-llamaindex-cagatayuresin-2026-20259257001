# LangChain Embedding'leri

LlamaIndex, `LangchainEmbedding` sarmalayıcısı (wrapper) aracılığıyla tüm LangChain embedding modellerini kullanmanıza olanak tanır.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-langchain
%pip install langchain
```

```python
!pip install llama-index
```

## LangChain Embedding Modelini Kurma

Aşağıdaki örnekte, LangChain'in `HuggingFaceEmbeddings` modelini LlamaIndex ile nasıl kullanacağınızı görebilirsiniz.

```python
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings

# LangChain modelini oluşturun
lc_embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# LlamaIndex sarmalayıcısı ile paketleyin
embed_model = LangchainEmbedding(lc_embed_model)
```

## Kullanım

```python
embeddings = embed_model.get_text_embedding("Bu bir test metnidir.")
print(len(embeddings))
print(embeddings[:5])
```

## RAG Boru Hattında Kullanım

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

# Global ayar olarak atayın
Settings.embed_model = embed_model

# İndeks oluşturun
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Sorgulama yapın
query_engine = index.as_query_engine()
response = query_engine.query("Metin ne hakkında?")
print(response)
```