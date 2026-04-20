# PremAI Gömmeleri (Embeddings)

[PremAI](https://premai.io/), Üretken Yapay Zeka (Generative AI) destekli sağlam, üretime hazır uygulamaların oluşturulmasını basitleştiren hepsi bir arada bir platformdur. PremAI, geliştirme sürecini kolaylaştırarak kullanıcı deneyimini iyileştirmeye ve uygulamanızın genel büyümesine odaklanmanıza olanak tanır. Platformumuzu [buradan](https://docs.premai.io/quick-start) hızlıca kullanmaya başlayabilirsiniz.

Bu bölümde, llama-index ile `PremAIEmbeddings` kullanarak farklı gömme modellerine nasıl erişebileceğimizi ele alacağız.

## Kurulum ve Hazırlık

`llama-index` ve `premai-sdk` kurulumu ile başlıyoruz. Kurmak için şu komutu yazabilirsiniz:

```bash
pip install premai llama-index
```

Devam etmeden önce lütfen PremAI üzerinde bir hesap oluşturduğunuzdan ve halihazırda bir proje oluşturduğunuzdan emin olun. Eğer yapmadıysanız, PremAI platformuna başlamak için lütfen [hızlı başlangıç](https://docs.premai.io/introduction) kılavuzuna bakın. İlk projenizi oluşturun ve API anahtarınızı alın.

```python
%pip install llama-index-llms-premai
```

```python
from llama_index.embeddings.premai import PremAIEmbeddings
```

## LlamaIndex'te PremAIEmbeddings Örneği Kurulumu

Gerekli modülleri içe aktardıktan sonra istemcimizi kuralım. Şimdilik `project_id` değerimizin `8` olduğunu varsayalım. Ancak mutlaka kendi proje kimliğinizi (project-id) kullandığınızdan emin olun, aksi takdirde hata verecektir.

Llama-index'i PremAI ile kullanmak için sohbet istemcimizde herhangi bir model adı geçirmeniz veya herhangi bir parametre ayarlamanız gerekmez. Varsayılan olarak [LaunchPad](https://docs.premai.io/get-started/launchpad) üzerinde kullanılan model adını ve parametreleri kullanacaktır.

Pek çok son teknoloji gömme modelini destekliyoruz. Desteklenen LLM'lerin ve gömme modellerinin listesini [buradan](https://docs.premai.io/get-started/supported-models) görüntüleyebilirsiniz. Şimdilik bu örnek için `text-embedding-3-large` modelini kullanalım.

```python
import os
import getpass

if os.environ.get("PREMAI_API_KEY") is None:
    os.environ["PREMAI_API_KEY"] = getpass.getpass("PremAI API Anahtarı:")

prem_embedding = PremAIEmbeddings(
    project_id=8, model_name="text-embedding-3-large"
)
```

## Gömme Modelini Çağırma

Artık her şey hazır. Şimdi önce tek bir sorgu, ardından birden fazla sorgu (belge olarak da adlandırılır) ile gömme modelimizi kullanmaya başlayalım.

```python
query = "Merhaba, bu bir test sorgusudur"
query_result = prem_embedding.get_text_embedding(query)
```

```python
print(f"Gömmelerin boyutu: {len(query_result)}")
```

    Gömmelerin boyutu: 3072

```python
query_result[:5]
```

    [-0.02129288576543331,
     0.0008162345038726926,
     -0.004556538071483374,
     0.02918623760342598,
     -0.02547479420900345]
