# Llamafile Embedding'leri

Bir LLM'i yerel olarak çalıştırmanın en basit yollarından biri [llamafile](https://github.com/Mozilla-Ocho/llamafile) kullanmaktır. llamafile'lar, model ağırlıklarını ve [`llama.cpp`](https://github.com/ggerganov/llama.cpp)'nin [özel olarak derlenmiş](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#technical-details) bir sürümünü, ek bir bağımlılık olmadan çoğu bilgisayarda çalışabilen tek bir dosyada birleştirir. Ayrıca, modelinizle etkileşim kurmanız için bir [API](https://github.com/Mozilla-Ocho/llamafile/blob/main/llama.cpp/server/README.md#api-endpoints) sağlayan gömülü bir çıkarım (inference) sunucusuyla birlikte gelirler.

## Kurulum

1.  [HuggingFace](https://huggingface.co/models?other=llamafile) üzerinden bir llamafile indirin.
2.  Dosyayı yürütülebilir (executable) hale getirin.
3.  Dosyayı çalıştırın.

İşte bu 3 kurulum adımını gösteren basit bir bash betiği:

```bash
# HuggingFace'den bir llamafile indirin
wget https://huggingface.co/jartine/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile

# Dosyayı yürütülebilir hale getirin. Windows'ta dosya adını sadece ".exe" ile bitecek şekilde değiştirin.
chmod +x TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile

# Model sunucusunu başlatın. Varsayılan olarak http://localhost:8080 adresini dinler.
./TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile --server --nobrowser --embedding
```

Modelinizin çıkarım sunucusu varsayılan olarak localhost:8080 adresini dinler.

```python
%pip install llama-index-embeddings-llamafile
```

```python
!pip install llama-index
```

```python
from llama_index.embeddings.llamafile import LlamafileEmbedding

embedding = LlamafileEmbedding(
    base_url="http://localhost:8080",
)

pass_embedding = embedding.get_text_embedding_batch(
    ["Bu bir pasajdır!", "Bu da başka bir pasajdır"], show_progress=True
)
print(len(pass_embedding), len(pass_embedding[0]))

query_embedding = embedding.get_query_embedding("Mavi nerede?")
print(len(query_embedding))
print(query_embedding[:10])
```