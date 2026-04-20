# Oracle Cloud Infrastructure (OCI) Data Science Hizmeti

Oracle Cloud Infrastructure (OCI) [Data Science](https://www.oracle.com/artificial-intelligence/data-science), veri bilimi ekiplerinin Oracle Cloud Infrastructure'da makine öğrenimi modelleri oluşturması, eğitmesi ve yönetmesi için tamamen yönetilen, sunucusuz bir platformdur.

OCI Data Science'da gömme (embedding) modellerini dağıtmak için kullanılabilecek [AI Quick Actions](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm) sunar. AI Quick Actions, yapay zekanın yeteneklerinden hızlıca yararlanmak isteyen kullanıcıları hedefler. Temel modellerle çalışmak için kolaylaştırılmış, kodsuz ve verimli bir ortam sağlayarak temel modellerin erişimini daha geniş bir kullanıcı kitlesine yaymayı amaçlarlar. AI Quick Actions'a Data Science Notebook üzerinden erişilebilir.

OCI Data Science'da AI Quick Actions kullanarak gömme modellerinin nasıl dağıtılacağına ilişkin ayrıntılı dokümantasyon [burada](https://github.com/oracle-samples/oci-data-science-ai-samples/blob/main/ai-quick-actions/model-deployment-tips.md) ve [burada](https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm) mevcuttur.

Bu not defteri, OCI'ın Data Science gömme modellerinin LlamaIndex ile nasıl kullanılacağını açıklamaktadır.

## Kurulum

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-oci-data-science
```

```python
!pip install llama-index
```

Ayrıca [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) SDK'sını da kurmanız gerekecektir.

```python
!pip install -U oracle-ads
```

## Kimlik Doğrulama

LlamaIndex için desteklenen kimlik doğrulama yöntemleri, diğer OCI hizmetlerinde kullanılanlarla eşdeğerdir ve standart SDK kimlik doğrulama yöntemlerini (özellikle API Anahtarı, oturum belirteci, örnek prensibi ve kaynak prensibi) takip eder. Daha fazla ayrıntı [burada](https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html) bulunabilir. OCI Data Science Model Dağıtımı (Model Deployment) uç noktasına erişmek için gerekli [politikalara](https://docs.oracle.com/en-us/iaas/data-science/using/model-dep-policies-auth.htm) sahip olduğunuzdan emin olun. [oracle-ads](https://accelerated-data-science.readthedocs.io/en/latest/index.html) paketi, OCI Data Science içindeki kimlik doğrulamasını basitleştirmeye yardımcı olur.

## Temel Kullanım

```python
import ads
from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding

ads.set_auth(auth="security_token", profile="<profilinizle-degistirin>")

embedding = OCIDataScienceEmbedding(
    endpoint="https://<MD_OCID>/predict",
)

e1 = embedding.get_text_embedding("Bu bir test belgesidir")
print(e1)

e2 = embedding.get_text_embedding_batch(
    ["Bu bir test belgesidir", "Bu başka bir test belgesidir"]
)
print(e2)
```

## Asenkron

```python
import ads
from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding

ads.set_auth(auth="security_token", profile="<profilinizle-degistirin>")

embedding = OCIDataScienceEmbedding(
    endpoint="https://<MD_OCID>/predict",
)

e1 = await embedding.aget_text_embedding("Bu bir test belgesidir")
print(e1)

e2 = await embedding.aget_text_embedding_batch(
    ["Bu bir test belgesidir", "Bu başka bir test belgesidir"]
)
print(e2)
```
