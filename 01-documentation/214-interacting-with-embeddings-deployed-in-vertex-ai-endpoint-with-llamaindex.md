# LlamaIndex ile Vertex AI Uç Noktasında (Endpoint) Dağıtılan Gömmelerle (Embeddings) Etkileşim Kurma

Bir Vertex AI uç noktası, yeni veriler üzerinde tahminler yapmak amacıyla gömmeler (embeddings) gibi makine öğrenimi modellerinin dağıtılmasını sağlayan yönetilen bir kaynaktır.

Bu not defteri, LlamaIndex'ten yararlanarak `VertexEndpointEmbedding` sınıfı ile gömme uç noktalarıyla nasıl etkileşim kurulacağını gösterir.

## Kurulum
Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-vertex-endpoint
```

```python
! pip install llama-index
```

Vertex AI'da dağıtılan modelle etkileşim kurmak için uç nokta bilgilerini (uç nokta kimliği, proje kimliği ve bölge) belirtmeniz gerekir.

```python
ENDPOINT_ID = "<-UC-NOKTA-KIMLIGINIZ->"
PROJECT_ID = "<-PROJE-KIMLIGINIZ->"
LOCATION = "<-GCP-BOLGENIZ->"
```

Uç noktaya bağlanmak için kimlik bilgileri (credentials) sağlanmalıdır. Şunlardan birini yapabilirsiniz:

- `service_account_file` parametresini belirterek bir servis hesabı JSON dosyası kullanabilirsiniz.
- Servis hesabı bilgilerini `service_account_info` parametresi aracılığıyla doğrudan sağlayabilirsiniz.

**Bir servis hesabı dosyası kullanma örneği:**

```python
from llama_index.embeddings.vertex_endpoint import VertexEndpointEmbedding

SERVICE_ACCOUNT_FILE = "<-SERVIS-HESABI-DOSYA-YOLUNUZ->.json"

embed_model = VertexEndpointEmbedding(
    endpoint_id=ENDPOINT_ID,
    project_id=PROJECT_ID,
    location=LOCATION,
    service_account_file=SERVICE_ACCOUNT_FILE,
)
```

**Doğrudan servis hesabı bilgilerini kullanma örneği:**

```python
from llama_index.embeddings.vertex_endpoint import VertexEndpointEmbedding

SERVICE_ACCOUNT_INFO = {
    "private_key": "<-OZEL-ANAHTAR->",
    "client_email": "<-SERVIS-HESABI-EPOSTASI->",
    "token_uri": "https://oauth2.googleapis.com/token",
}

embed_model = VertexEndpointEmbedding(
    endpoint_id=ENDPOINT_ID,
    project_id=PROJECT_ID,
    location=LOCATION,
    service_account_info=SERVICE_ACCOUNT_INFO,
)
```

## Temel Kullanım

### `get_text_embedding` Çağrısı

```python
embeddings = embed_model.get_text_embedding(
    "Vertex AI, Google Cloud tarafından sunulan yönetilen bir makine öğrenimi (ML) platformudur. Veri bilimcilerin ve geliştiricilerin, Google'ın ML altyapısından yararlanarak makine öğrenimi modellerini verimli bir şekilde oluşturmasına, dağıtmasına ve ölçeklendirmesine olanak tanır."
)
```

```python
embeddings[:10]
```

    [0.011612358,
     0.01030837,
     -0.04710829,
     -0.030719217,
     0.027658276,
     -0.031597693,
     0.012065322,
     -0.037609763,
     0.02321099,
     0.012868305]

### `get_text_embedding_batch` Çağrısı

```python
embeddings = embed_model.get_text_embedding_batch(
    [
        "Vertex AI, Google Cloud tarafından sunulan yönetilen bir makine öğrenimi (ML) platformudur. Veri bilimcilerin ve geliştiricilerin, Google'ın ML altyapısından yararlanarak makine öğrenimi modellerini verimli bir şekilde oluşturmasına, dağıtmasına ve ölçeklendirmesine olanak tanır.",
        "Vertex, llamaIndex ile entegre edilmiştir",
    ]
)
```

```python
len(embeddings)
```

    2
