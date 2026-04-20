# LlamaIndex ile Amazon SageMaker Uç Noktasında (Endpoint) Dağıtılan Gömmelerle (Embeddings) Etkileşim Kurma

Bir Amazon SageMaker uç noktası, yeni veriler üzerinde tahminler yapmak amacıyla makine öğrenimi modellerinin dağıtılmasını sağlayan tam yönetilen bir kaynaktır.

Bu not defteri, `SageMakerEmbedding` kullanarak Gömme uç noktalarıyla nasıl etkileşim kurulacağını gösterir ve ek LlamaIndex özelliklerinin kullanımını mümkün kılar.
Bu doğrultuda, bir SageMaker uç noktasında bir Gömme modelinin dağıtılmış olduğu varsayılmaktadır.

## Kurulum
Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-sagemaker-endpoint
```

```python
! pip install llama-index
```

Etkileşim kurulacak olan uç nokta (endpoint) adını belirtmeniz gerekmektedir.

```python
ENDPOINT_NAME = "<-UC-NOKTA-ADINIZ->"
```

Uç noktaya bağlanmak için kimlik bilgileri (credentials) sağlanmalıdır. Şunlardan birini yapabilirsiniz:
- `profile_name` parametresini belirterek bir AWS profili kullanabilirsiniz; belirtilmezse varsayılan kimlik bilgisi profili (default profile) kullanılacaktır.
- Kimlik bilgilerini parametre olarak geçirebilirsiniz (`aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`, `region_name`).

Daha fazla ayrıntı için [bu bağlantıyı](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) kontrol edin.

**AWS profil adı**

```python
from llama_index.embeddings.sagemaker_endpoint import SageMakerEmbedding

AWS_ACCESS_KEY_ID = "<-AWS-ERISIM-ANAHTARI-KIMLIGI->"
AWS_SECRET_ACCESS_KEY = "<-AWS-GIZLI-ERISIM-ANAHTARI->"
AWS_SESSION_TOKEN = "<-AWS-OTURUM-BELIRTECI->"
REGION_NAME = "<-UC-NOKTA-BOLGE-ADI->"
```

```python
embed_model = SageMakerEmbedding(
    endpoint_name=ENDPOINT_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=REGION_NAME,
)
```

**Kimlik bilgileri ile**:

```python
from llama_index.embeddings.sagemaker_endpoint import SageMakerEmbedding

ENDPOINT_NAME = "<-UC-NOKTA-ADINIZ->"
PROFILE_NAME = "<-PROFIL-ADINIZ->"
embed_model = SageMakerEmbedding(
    endpoint_name=ENDPOINT_NAME, profile_name=PROFILE_NAME
)  # Varsayılan profili kullanmak için profil adını atlayın
```

## Temel Kullanım

### `get_text_embedding` Çağrısı

```python
embeddings = embed_model.get_text_embedding(
    "Bir Amazon SageMaker uç noktası, yeni veriler üzerinde tahminler yapmak amacıyla makine öğrenimi modellerinin, özellikle de LLM'lerin (Büyük Dil Modelleri) dağıtılmasını sağlayan tamamen yönetilen bir kaynaktır."
)
```

```python
embeddings
```

    [0.021565623581409454,
    ...
     0.019147753715515137,]

### `get_text_embedding_batch` Çağrısı

```python
embeddings = embed_model.get_text_embedding_batch(
    [
        "Bir Amazon SageMaker uç noktası, makine öğrenimi modellerinin dağıtılmasını sağlayan tamamen yönetilen bir kaynaktır",
        "Sagemaker, llamaIndex ile entegre edilmiştir",
    ]
)
```

```python
len(embeddings)
```

    2
