# DeepEval ile LLM'ler/RAG için Birim Testi (Unit Testing)

[DeepEval](https://github.com/confident-ai/deepeval), AI ajanları ve LLM destekli uygulamalar için birim testi sağlar. LlamaIndex kullanıcılarının LLM çıktıları için testler yazması için gerçekten basit bir arayüz sunar ve geliştiricilerin üretimdeki bozucu değişiklikleri (breaking changes) yakalamasına yardımcı olur.

DeepEval, yanıtları ölçmek için görüş bildiren (opinionated) bir çerçeve sunar ve tamamen açık kaynaklıdır.

### Kurulum ve Kurulum (Installation and Setup)

[DeepEval](https://github.com/confident-ai/deepeval) eklemek basittir ve 0 kurulum gerektirir. Yüklemek için:

```sh
pip install -U deepeval
# İsteğe bağlı adım: Daha sonra testleriniz için güzel bir panel (dashboard) elde etmek için giriş yapın!
deepeval login
```

Yüklendikten sonra bir `test_rag.py` oluşturabilir ve test yazmaya başlayabilirsiniz.

```python title="test_rag.py"
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase


def test_case():
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    test_case = LLMTestCase(
        input="Bu ayakkabılar uymazsa ne olur?",
        # Bunu LLM uygulamanızdan gelen gerçek çıktı ile değiştirin
        actual_output="Ek ücret ödemeden 30 günlük tam iade sunuyoruz.",
        retrieval_context=[
            "Tüm müşteriler ek ücret ödemeden 30 günlük tam iade hakkına sahiptir."
        ],
    )
    assert_test(test_case, [answer_relevancy_metric])
```

Daha sonra testleri şu şekilde çalıştırabilirsiniz:

```bash
deepeval test run test_rag.py
```

Eğer giriş yaptıysanız, değerlendirme sonuçlarını `deepeval`'in panelinden analiz edebilirsiniz:

![Örnek panel](https://d2lsxfc3p6r9rv.cloudfront.net/confident-test-cases.png)

## Metrik Türleri

DeepEval, RAG uygulamalarının birim testi için görüş bildiren bir çerçeve sunar. Değerlendirmeleri test senaryolarına ayırır ve her test senaryosu için serbestçe değerlendirebileceğiniz bir dizi değerlendirme metriği sunar:

- G-Eval
- Özetleme (Summarization)
- Yanıt Uygunluğu (Answer Relevancy)
- Sadakat (Faithfulness)
- Bağlamsal Geri Çağırma (Contextual Recall)
- Bağlamsal Hassasiyet (Contextual Precision)
- Bağlamsal Uygunluk (Contextual Relevancy)
- RAGAS
- Halüsinasyon (Hallucination)
- Yanlılık (Bias)
- Toksisite (Toxicity)

[DeepEval](https://github.com/confident-ai/deepeval), değerlendirme metriklerine en son araştırmaları dahil eder. Metriklerin tam listesi ve nasıl hesaplandıkları hakkında [buradan](https://docs.confident-ai.com/docs/metrics-introduction) daha fazla bilgi edinebilirsiniz.

## LlamaIndex Uygulamanız İçin RAG Değerlendirmesi

DeepEval, LlamaIndex'in `BaseEvaluator` sınıfıyla güzel bir şekilde entegre olur. Aşağıda, LlamaIndex değerlendiricisi formunda DeepEval'in değerlendirme metriklerinin örnek kullanımı yer almaktadır.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from deepeval.integrations.llama_index import DeepEvalAnswerRelevancyEvaluator

# Daha fazla detay için LlamaIndex'in hızlı başlangıç kılavuzunu okuyun
documents = SimpleDirectoryReader("VERI_DIZININIZ").load_data()
index = VectorStoreIndex.from_documents(documents)
rag_application = index.as_query_engine()

# RAG uygulamanıza örnek bir girdi
user_input = "LlamaIndex nedir?"

# LlamaIndex, hem çıktı dizesini hem de erişilen node'ları içeren
# bir yanıt nesnesi döndürür
response_object = rag_application.query(user_input)

evaluator = DeepEvalAnswerRelevancyEvaluator()
```

Daha sonra şu şekilde değerlendirme yapabilirsiniz:

```python
evaluation_result = evaluator.evaluate_response(
    query=user_input, response=response_object
)
print(evaluation_result)
```

### Değerlendiricilerin Tam Listesi

`deepeval` içindeki 6 değerlendiricinin tamamını şu şekilde içe aktarabilirsiniz:

```python
from deepeval.integrations.llama_index import (
    DeepEvalAnswerRelevancyEvaluator,
    DeepEvalFaithfulnessEvaluator,
    DeepEvalContextualRelevancyEvaluator,
    DeepEvalSummarizationEvaluator,
    DeepEvalBiasEvaluator,
    DeepEvalToxicityEvaluator,
)
```

Tüm değerlendirici tanımları ve DeepEval'in test paketiyle nasıl entegre olduğunu anlamak için [buraya tıklayın.](https://docs.confident-ai.com/docs/integrations-llamaindex)

### Yararlı Bağlantılar

- [DeepEval Hızlı Başlangıç](https://docs.confident-ai.com/docs/getting-started)
- [LLM değerlendirme metrikleri hakkında bilmeniz gereken her şey](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation)