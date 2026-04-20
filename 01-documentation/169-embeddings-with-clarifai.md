# Clarifai ile Embedding'ler

LlamaIndex, Clarifai embedding modellerini destekler.

Bir Clarifai hesabınızın ve bir Kişisel Erişim Belirteci (Personal Access Token - PAT) anahtarınızın olması gerekir.
Bir PAT almak veya oluşturmak için [burayı kontrol edin](https://clarifai.com/settings/security).

`CLARIFAI_PAT`'i bir ortam değişkeni olarak ayarlayın veya PAT'i `ClarifaiEmbedding` sınıfına bağımsız değişken (argument) olarak geçirebilirsiniz.

```python
%pip install llama-index-embeddings-clarifai
```

```python
!export CLARIFAI_PAT=ANAHTARINIZ
```

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
!pip install llama-index
```

Modellere tam URL ile veya model_name, user ID ve app ID kombinasyonu ile atıfta bulunulabilir.

```python
from llama_index.embeddings.clarifai import ClarifaiEmbedding

# CLARIFAI_PAT'in bir ortam değişkeni olarak ayarlandığını varsayarak yalnızca model_url ile bir clarifai embedding sınıfı oluşturun
embed_model = ClarifaiEmbedding(
    model_url="https://clarifai.com/clarifai/main/models/BAAI-bge-base-en"
)

# Alternatif olarak sınıfı model_name, user_id, app_id ve pat ile de başlatabilirsiniz.
embed_model = ClarifaiEmbedding(
    model_name="BAAI-bge-base-en",
    user_id="clarifai",
    app_id="main",
    pat=CLARIFAI_PAT,
)
```

```python
embeddings = embed_model.get_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

Metin listesini embedding'e dönüştürme:

```python
text = "güller kırmızıdır menekşeler mavidir."
text2 = "Demir tavında dövülür."
```

```python
embeddings = embed_model._get_text_embeddings([text2, text])
print(len(embeddings))
print(embeddings[0][:5])
print(embeddings[1][:5])
```