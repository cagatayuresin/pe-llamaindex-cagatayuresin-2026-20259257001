# Predibase

---
title: Predibase
 | LlamaIndex OSS Documentation
---

Bu not defteri, Predibase tarafından barındırılan LLM'leri LlamaIndex içinde nasıl kullanabileceğinizi gösterir. [Predibase](https://predibase.com)'i mevcut LlamaIndex iş akışınıza şunlar için ekleyebilirsiniz:

1. Önceden eğitilmiş veya özel açık kaynaklı LLM'leri zahmetsizce dağıtın ve sorgulayın
2. Uçtan uca bir Geri Getirme Artırılmış Üretim (RAG) sistemini operasyonel hale getirin
3. Sadece birkaç satır kodla kendi LLM'nizi ince ayarlayın (fine-tune)

## Başlarken

1. [Buradan](https://predibase.com/free-trial) ücretsiz bir Predibase hesabı için kaydolun
2. Bir Hesap Oluşturun
3. Ayarlar (Settings) > Profilim (My profile) bölümüne gidin ve yeni bir API Belirteci (Token) oluşturun.

```python
%pip install llama-index-llms-predibase
```

```python
!pip install llama-index --quiet
!pip install predibase --quiet
!pip install sentence-transformers --quiet
```

```python
import os


os.environ["PREDIBASE_API_TOKEN"] = "{PREDIBASE_API_TOKEN}"
from llama_index.llms.predibase import PredibaseLLM
```

## Akış 1: Predibase LLM'yi doğrudan sorgulayın

```python
# Predibase'de barındırılan ince ayarlı adaptör örneği
llm = PredibaseLLM(
    model_name="mistral-7b",
    predibase_sdk_version=None,  # isteğe bağlı parametre (belirtilmezse varsayılan olarak en son Predibase SDK sürümüne ayarlanır)
    adapter_id="e2e_nlg",  # adapter_id isteğe bağlıdır
    adapter_version=1,  # isteğe bağlı parametre (yalnızca Predibase için geçerlidir)
    api_token=None,  # adaptörleri barındıran hizmetlere (örneğin HuggingFace) erişmek için isteğe bağlı parametre
    max_new_tokens=512,
    temperature=0.3,
)
# `model_name` parametresi, Predibase "sunucusuz" base_model kimliğidir
# (katalog için https://docs.predibase.com/user-guide/inference/models sayfasına bakın).
# Ayrıca isteğe bağlı olarak Predibase veya HuggingFace üzerinde barındırılan ince ayarlı bir adaptör de belirtebilirsiniz
# Predibase'de barındırılan adaptörler durumunda, adapter_version'u da belirtmelisiniz
```

```python
# HuggingFace'de barındırılan ince ayarlı adaptör örneği
llm = PredibaseLLM(
    model_name="mistral-7b",
    predibase_sdk_version=None,  # isteğe bağlı parametre (belirtilmezse varsayılan olarak en son Predibase SDK sürümüne ayarlanır)
    adapter_id="predibase/e2e_nlg",  # adapter_id isteğe bağlıdır
    api_token=os.environ.get(
        "HUGGING_FACE_HUB_TOKEN"
    ),  # adaptörleri barındıran hizmetlere (örneğin HuggingFace) erişmek için isteğe bağlı parametre
    max_new_tokens=512,
    temperature=0.3,
)
# `model_name` parametresi, Predibase "sunucusuz" base_model kimliğidir
# (katalog için https://docs.predibase.com/user-guide/inference/models sayfasına bakın).
# Ayrıca isteğe bağlı olarak Predibase veya HuggingFace üzerinde barındırılan ince ayarlı bir adaptör de belirtebilirsiniz
# Predibase'de barındırılan adaptörler durumunda, adapter_version'u da belirtebilirsiniz (belirtilmezse en sonuncusu varsayılır)
```

```python
result = llm.complete("Bana güzel bir sek beyaz şarap önerebilir misin?")
print(result)
```

## Akış 2: Predibase LLM ile Geri Getirme Artırılmış Üretim (RAG)

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.node_parser import SentenceSplitter
```

#### Veriyi İndir

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

### Belgeleri Yükle

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

### Predibase LLM'yi Yapılandırma

```python
# Predibase'de barındırılan ince ayarlı adaptör
llm = PredibaseLLM(
    model_name="mistral-7b",
    predibase_sdk_version=None,  # isteğe bağlı parametre (belirtilmezse varsayılan olarak en son Predibase SDK sürümüne ayarlanır)
    adapter_id="e2e_nlg",  # adapter_id isteğe bağlıdır
    api_token=None,  # adaptörleri barındıran hizmetlere (örneğin HuggingFace) erişmek için isteğe bağlı parametre
    temperature=0.3,
    context_window=1024,
)
```

```python
# HuggingFace'de barındırılan ince ayarlı adaptör
llm = PredibaseLLM(
    model_name="mistral-7b",
    predibase_sdk_version=None,  # isteğe bağlı parametre (belirtilmezse varsayılan olarak en son Predibase SDK sürümüne ayarlanır)
    adapter_id="predibase/e2e_nlg",  # adapter_id isteğe bağlıdır
    api_token=os.environ.get(
        "HUGGING_FACE_HUB_TOKEN"
    ),  # adaptörleri barındıran hizmetlere (örneğin HuggingFace) erişmek için isteğe bağlı parametre
    temperature=0.3,
    context_window=1024,
)
```

```python
embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
splitter = SentenceSplitter(chunk_size=1024)
```

### İndeksi Kur ve Sorgula

```python
index = VectorStoreIndex.from_documents(
    documents, transformations=[splitter], embed_model=embed_model
)
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Yazar büyürken ne yaptı?")
```

```python
print(response)
```
