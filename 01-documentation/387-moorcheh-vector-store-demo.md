---
title: Moorcheh Vektör Deposu Demosu
 | LlamaIndex OSS Belgeleri
---

# Moorcheh Vektör Deposu Demosu

## Gerekli Paketleri Kurun

```bash
!pip install llama_index
!pip install moorcheh_sdk
```

## Gerekli Kütüphaneleri İçe Aktarın

demo.py

```python
# --- Moorcheh Vektör Deposu Demosuna Hoş Geldiniz ---
# --- Aşağıdaki paketleri içe aktarın ---
import logging
import sys
import os
from moorcheh_sdk import MoorchehClient
from IPython.display import Markdown, display
from typing import Any, Callable, Dict, List, Optional, cast
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)
from llama_index.core.base.embeddings.base_sparse import BaseSparseEmbedding
from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.schema import BaseNode, MetadataMode, TextNode
from llama_index.core.vector_stores.types import (
    BasePydanticVectorStore,
    MetadataFilters,
    VectorStoreQuery,
    VectorStoreQueryMode,
    VectorStoreQueryResult,
)
from llama_index.core.vector_stores.utils import (
    DEFAULT_TEXT_KEY,
    legacy_metadata_dict_to_node,
    metadata_dict_to_node,
    node_to_metadata_dict,
)
from llama_index.core.vector_stores.types import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
    FilterCondition,
)
```

## Günlüğü (Logging) Yapılandırın

```python
# --- Günlük Kurulumu ---
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

## Moorcheh API Anahtarını Yükleyin

```python
# --- API Anahtarlarının değerlerini Ortam Değişkenlerinize ayarlayın ---
from google.colab import userdata


api_key = os.environ["MOORCHEH_API_KEY"] = userdata.get("MOORCHEH_API_KEY")


if "MOORCHEH_API_KEY" not in os.environ:
    raise EnvironmentError("MOORCHEH_API_KEY ortam değişkeni ayarlanmadı")
```

## Belgeleri Yükleyin ve Parçalayın

```python
# --- Belgeleri Yükle ---
documents = SimpleDirectoryReader("./documents").load_data()


# --- Parça boyutunu ve çakışmayı (overlap) ayarla ---
Settings.chunk_size = 1024
Settings.chunk_overlap = 20
```

## Vektör Deposunu Başlatın ve İndeks Oluşturun

```python
# --- Moorcheh Vektör Deposunu Başlatın ---
__all__ = ["MoorchehVectorStore"]


# Aşağıdaki parametrelerle bir Moorcheh Vektör Deposu oluşturur
# Metin tabanlı ad alanları (namespaces) için namespace_type'ı "text" ve vector_dimension'ı None olarak ayarlayın
# Vektör tabanlı ad alanları için namespace_type'ı "vector" ve vector_dimension'ı yüklediğiniz vektörlerin boyutuna ayarlayın
vector_store = MoorchehVectorStore(
    api_key=api_key,
    namespace="llamaindex_moorcheh",
    namespace_type="text",
    vector_dimension=None,
    add_sparse_vector=False,
    batch_size=100,
)


# --- Vektör Deposunu ve verilen Belgeleri kullanarak bir Vektör Depo İndeksi oluşturun ---
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

## Vektör Deposunu Sorgulayın

```python
# --- Yanıt Oluştur ---
# --- Daha Detaylı Çıktılar için Günlük Kaydını DEBUG olarak ayarlayın ---
query_engine = index.as_query_engine()
response = vector_store.generate_answer(
    query="2025'te hangi şirket en yüksek gelire sahip oldu ve neden?"
)
moorcheh_response = vector_store.get_generative_answer(
    query="2025'te hangi şirket en yüksek gelire sahip oldu ve neden?",
    ai_model="anthropic.claude-3-7-sonnet-20250219-v1:0",
)


display(Markdown(f"<b>{response}</b>"))
print(
    "\n\n================================\n\n",
    response,
    "\n\n================================\n\n",
)
print(
    "\n\n================================\n\n",
    moorcheh_response,
    "\n\n================================\n\n",
)


# --- Meta Veri Filtreleri ---
filter = MetadataFilters(
    filters=[
        MetadataFilter(
            key="file_path",
            value="buraya belgenin dosya yolunu ekleyin",
            operator=FilterOperator.EQ,
        )
    ],
    condition=FilterCondition.AND,
)
```
