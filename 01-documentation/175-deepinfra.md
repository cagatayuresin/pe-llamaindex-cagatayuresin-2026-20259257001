# DeepInfra

Bu entegrasyon ile metin verileriniz için embedding'ler elde etmek üzere DeepInfra embedding modellerini kullanabilirsiniz. İşte [embedding modellerinin](https://deepinfra.com/models/embeddings) bağlantısı.

Öncelikle [DeepInfra web sitesinde](https://deepinfra.com/) kaydolmanız ve API belirtecini (token) almanız gerekir. Model kartlarından `model_ids` değerlerini kopyalayabilir ve bunları kodunuzda kullanmaya başlayabilirsiniz.

### Kurulum

```python
!pip install llama-index llama-index-embeddings-deepinfra
```

### Başlatma (Initialization)

```python
from dotenv import load_dotenv, find_dotenv
from llama_index.embeddings.deepinfra import DeepInfraEmbeddingModel

_ = load_dotenv(find_dotenv())

model = DeepInfraEmbeddingModel(
    model_id="BAAI/bge-large-en-v1.5",  # Özel model kimliği kullanın
    api_token="API_ANAHTARINIZ",       # İsteğe bağlı olarak belirteci buradan sağlayın
    normalize=True,                    # İsteğe bağlı normalizasyon
    text_prefix="text: ",              # İsteğe bağlı metin ön eki
    query_prefix="query: ",            # İsteğe bağlı sorgu ön eki
)
```

### Senkronize İstekler

#### Metin Embedding'ini Al

```python
response = model.get_text_embedding("merhaba dünya")
print(response)
```

#### Toplu (Batch) İstekler

```python
texts = ["merhaba dünya", "elveda dünya"]
response_batch = model.get_text_embedding_batch(texts)
print(response_batch)
```

#### Sorgu İstekleri

```python
query_response = model.get_query_embedding("merhaba dünya")
print(query_response)
```

### Asenkronize İstekler

#### Metin Embedding'ini Al

```python
async def main():
    text = "merhaba dünya"
    async_response = await model.aget_text_embedding(text)
    print(async_response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

---

Her türlü soru veya geri bildiriminiz için lütfen feedback@deepinfra.com adresinden bizimle iletişime geçin.