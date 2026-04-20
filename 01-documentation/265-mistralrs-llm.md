# MistralRS LLM

---
title: MistralRS LLM
 | LlamaIndex OSS Belgeleri
---

**NOT:** MistralRS, `cargo` adlı bir Rust paket yöneticisinin kurulu olmasını gerektirir. Kurulum detayları için <https://rustup.rs/> adresini ziyaret edin.

```bash
%pip install llama-index-core
%pip install llama-index-readers-file
%pip install llama-index-llms-mistral-rs
%pip install llama-index-llms-huggingface
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.mistral_rs import MistralRS
from mistralrs import Which, Architecture


documents = SimpleDirectoryReader("data").load_data()


# bge gömme (embedding) modeli
Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
```

MistralRS, HuggingFace Hub'daki model kimliklerini kullanır.

```python
# Tam Model (Full Model)
Settings.llm = MistralRS(
    which=Which.Plain(
        model_id="mistralai/Mistral-7B-Instruct-v0.1",
        arch=Architecture.Mistral,
        tokenizer_json=None,
        repeat_last_n=64,
    ),
    max_new_tokens=4096,
    context_window=1024 * 5,
)


# GGUF Modeli, Kuantize edilmiş (Quantized)
Settings.llm = MistralRS(
    which=Which.GGUF(
        tok_model_id="mistralai/Mistral-7B-Instruct-v0.1",
        quantized_model_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        quantized_filename="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        tokenizer_json=None,
        repeat_last_n=64,
    ),
    max_new_tokens=4096,
    context_window=1024 * 5,
)
```

```python
index = VectorStoreIndex.from_documents(
    documents,
)
```

```python
query_engine = index.as_query_engine()
response = query_engine.query("Grafeni nasıl telaffuz ederim?")
print(response)
```
