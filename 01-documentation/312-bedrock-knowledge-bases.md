# Bedrock (Bilgi Tabanları)

---
title: Bedrock (Knowledge Bases)
 | LlamaIndex OSS Documentation
---

[Amazon Bedrock için Bilgi Tabanları (Knowledge bases)](https://aws.amazon.com/bedrock/knowledge-bases/), özel verilerinizi kullanarak Temel Model (FM) yanıtlarını özelleştirmenize ve hızlı bir şekilde RAG uygulamaları oluşturmanıza olanak tanıyan bir Amazon Web Servisleri (AWS) çözümüdür.

`RAG` uygulamak, kuruluşların verileri vektörlere (embedding) dönüştürmek, bu vektörleri özel bir vektör veritabanında saklamak ve kullanıcının sorgusuyla ilgili metni arayıp getirmek için veritabanına özel entegrasyonlar oluşturmak gibi birkaç zahmetli adımı gerçekleştirmesini gerektirir. Bu süreç zaman alıcı ve verimsiz olabilir.

`Amazon Bedrock için Bilgi Tabanları` ile verilerinizin `Amazon S3` üzerindeki konumunu belirtmeniz yeterlidir; Amazon Bedrock, verilerin vektör veritabanınıza aktarılması (ingestion) iş akışının tamamını üstlenir. Mevcut bir vektör veritabanınız yoksa, Amazon Bedrock sizin yerinize bir Amazon OpenSearch Serverless vektör deposu oluşturur.

Bilgi tabanı, [AWS Konsolu](https://aws.amazon.com/console/) üzerinden veya [AWS SDK'ları](https://aws.amazon.com/developer/tools/) kullanılarak yapılandırılabilir.

Bu not defterinde, bir kullanıcı sorgusu için bilgi tabanlarından ilgili sonuçları getirmek amacıyla Retrieve API aracılığıyla Llama Index'teki Amazon Bedrock entegrasyonu olan AmazonKnowledgeBasesRetriever'ı tanıtıyoruz.

## Bilgi Tabanı Erişimcisini (Knowledge Base Retriever) Kullanma

```python
%pip install --upgrade --quiet  boto3 botocore
%pip install llama-index
%pip install llama-index-retrievers-bedrock
```

`retrieval_config` için desteklenen parametreler hakkında daha fazla bilgi için lütfen boto3 belgelerini inceleyin: [bağlantı](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve.html)

`retrieval_config` içinde filtre kullanmak için veri kaynağınız için bir metadata.json dosyası oluşturmanız gerekecektir. Daha fazla bilgi için: [bağlantı](https://aws.amazon.com/blogs/machine-learning/knowledge-bases-for-amazon-bedrock-now-supports-metadata-filtering-to-improve-retrieval-accuracy/)

```python
from llama_index.retrievers.bedrock import AmazonKnowledgeBasesRetriever


retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="<knowledge-base-id>",
    retrieval_config={
        "vectorSearchConfiguration": {
            "numberOfResults": 4,
            "overrideSearchType": "HYBRID",
            "filter": {"equals": {"key": "tag", "value": "space"}},
        }
    },
)
```

```python
query = "Samanyolu, tüm evrenle karşılaştırıldığında ne kadar büyüktür?"
retrieved_results = retriever.retrieve(query)


# Getirilen ilk sonucu yazdırır
print(retrieved_results[0].get_content())
```

## Erişimciyi Bedrock LLM'leri ile Sorgulama Yapmak İçin Kullanma

```python
%pip install llama-index-llms-bedrock
```

```python
from llama_index.core import get_response_synthesizer
from llama_index.llms.bedrock.base import Bedrock


llm = Bedrock(model="anthropic.claude-v2", temperature=0, max_tokens=3000)
response_synthesizer = get_response_synthesizer(
    response_mode="compact", llm=llm
)
response_obj = response_synthesizer.synthesize(query, retrieved_results)
print(response_obj)
```
