# Oracle Cloud Infrastructure Generative AI

Oracle Cloud Infrastructure (OCI) Generative AI, tek bir API aracılığıyla sunulan ve çok çeşitli kullanım senaryolarını kapsayan, son teknoloji ürünü, özelleştirilebilir geniş dil modelleri (LLM'ler) sağlayan tam yönetilen bir hizmettir.

OCI Generative AI hizmetini kullanarak kullanıma hazır önceden eğitilmiş modellere erişebilir veya ayrılmış yapay zeka kümelerinde (dedicated AI clusters) kendi verilerinize dayalı olarak ince ayar yapılmış (fine-tuned) özel modellerinizi oluşturabilir ve barındırabilirsiniz. Hizmetin ve API'nin ayrıntılı dokümantasyonu __[burada](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)__ ve __[burada](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai/20231130/)__ mevcuttur.

Bu not defteri, OCI'ın Generative AI gömme (embedding) modellerinin LlamaIndex ile nasıl kullanılacağını açıklamaktadır.

## Kurulum

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-oci-genai
```

```python
!pip install llama-index
```

Ayrıca OCI SDK'sını da kurmanız gerekecektir.

```python
!pip install -U oci
```

## Temel Kullanım

```python
from llama_index.embeddings.oci_genai import OCIGenAIEmbeddings

embedding = OCIGenAIEmbeddings(
    model_name="cohere.embed-english-light-v3.0",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="MY_OCID",
)

e1 = embedding.get_text_embedding("Bu bir test belgesidir")
print(e1[-5:])

e2 = embedding.get_query_embedding("Bu bir test belgesidir")
print(e2[-5:])

docs = ["Bu bir test belgesidir", "Bu başka bir test belgesidir"]
e3 = embedding.get_text_embedding_batch(docs)
print(e3)
```
