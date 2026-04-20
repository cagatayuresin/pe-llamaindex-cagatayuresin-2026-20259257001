# Kullanım Kalıbı (Usage Pattern - Yanıt Değerlendirmesi)

## `BaseEvaluator` Kullanımı

LlamaIndex'teki tüm değerlendirme modülleri, iki ana metotla `BaseEvaluator` sınıfını uygular:

1. `evaluate` metodu `query` (sorgu), `contexts` (bağlamlar), `response` (yanıt) ve ek anahtar kelime argümanlarını alır.

```python
    def evaluate(
        self,
        query: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        response: Optional[str] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
```

2. `evaluate_response` metodu; ayrı `contexts` ve `response` yerine bir LlamaIndex `Response` nesnesini (yanıt dizesini ve kaynak node'ları içeren) alan alternatif bir arayüz sağlar.

```python
def evaluate_response(
    self,
    query: Optional[str] = None,
    response: Optional[Response] = None,
    **kwargs: Any,
) -> EvaluationResult:
```

İşlevsel olarak `evaluate` ile aynıdır, sadece LlamaIndex nesneleriyle doğrudan çalışırken kullanımı daha basittir.

## `EvaluationResult` Kullanımı

Her değerlendirici çalıştırıldığında bir `EvaluationResult` çıktısı verir:

```python
eval_result = evaluator.evaluate(query=..., contexts=..., response=...)
eval_result.passing  # ikili (binary) geçme/kalma durumu
eval_result.score  # sayısal puan
eval_result.feedback  # dize formatında geri bildirim
```

Farklı değerlendiriciler, sonuç alanlarının bir alt kümesini doldurabilir.

## Yanıt Sadakatini Değerlendirme (Sadakat Ölçümü / Halüsinasyon Kontrolü)

`FaithfulnessEvaluator`, cevabın getirilen bağlamlara sadık olup olmadığını değerlendirir (başka bir deyişle, halüsinasyon olup olmadığını kontrol eder).

```python
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import FaithfulnessEvaluator

# llm oluştur
llm = OpenAI(model="gpt-4", temperature=0.0)

# indeks oluştur
...

# değerlendiriciyi tanımla
evaluator = FaithfulnessEvaluator(llm=llm)

# indeksi sorgula
query_engine = vector_index.as_query_engine()
response = query_engine.query(
    "Amerikan Devrimi'nde New York City'de hangi savaşlar gerçekleşti?"
)
eval_result = evaluator.evaluate_response(response=response)
print(str(eval_result.passing))
```

Ayrıca her bir kaynak bağlamı ayrı ayrı değerlendirmeyi de seçebilirsiniz:

```python
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import FaithfulnessEvaluator

# llm oluştur
llm = OpenAI(model="gpt-4", temperature=0.0)

# indeks oluştur
...

# değerlendiriciyi tanımla
evaluator = FaithfulnessEvaluator(llm=llm)

# indeksi sorgula
query_engine = vector_index.as_query_engine()
response = query_engine.query(
    "Amerikan Devrimi'nde New York City'de hangi savaşlar gerçekleşti?"
)
response_str = response.response
for source_node in response.source_nodes:
    eval_result = evaluator.evaluate(
        response=response_str, contexts=[source_node.get_content()]
    )
    print(str(eval_result.passing))
```

`response.source_nodes` içindeki her bir kaynak node'a karşılık gelen bir sonuç listesi alırsınız.

## Sorgu + Yanıt İlgililiğini Değerlendirme

`RelevancyEvaluator`, getirilen bağlamın ve cevabın verilen sorgu için ilgili ve tutarlı olup olmadığını değerlendirir.

Bu değerlendiricinin, `Response` nesnesine ek olarak `query` parametresinin de geçirilmesini gerektirdiğini unutmayın.

```python
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import RelevancyEvaluator

# llm oluştur
llm = OpenAI(model="gpt-4", temperature=0.0)

# indeks oluştur
...

# değerlendiriciyi tanımla
evaluator = RelevancyEvaluator(llm=llm)

# indeksi sorgula
query_engine = vector_index.as_query_engine()
query = "Amerikan Devrimi'nde New York City'de hangi savaşlar gerçekleşti?"
response = query_engine.query(query)
eval_result = evaluator.evaluate_response(query=query, response=response)
print(str(eval_result))
```

Benzer şekilde, belirli bir kaynak node üzerinde de değerlendirme yapabilirsiniz.

```python
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import RelevancyEvaluator

# llm oluştur
llm = OpenAI(model="gpt-4", temperature=0.0)

# indeks oluştur
...

# değerlendiriciyi tanımla
evaluator = RelevancyEvaluator(llm=llm)

# indeksi sorgula
query_engine = vector_index.as_query_engine()
query = "Amerikan Devrimi'nde New York City'de hangi savaşlar gerçekleşti?"
response = query_engine.query(query)
response_str = response.response
for source_node in response.source_nodes:
    eval_result = evaluator.evaluate(
        query=query,
        response=response_str,
        contexts=[source_node.get_content()],
    )
    print(str(eval_result.passing))
```

## Soru Oluşturma (Question Generation)

LlamaIndex, verilerinizi kullanarak cevaplanacak sorular da oluşturabilir. Yukarıdaki değerlendiricilerle birlikte kullanarak, verileriniz üzerinde tam otomatik bir değerlendirme akışı oluşturabilirsiniz.

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.llama_dataset.generator import RagDatasetGenerator

# llm oluştur
llm = OpenAI(model="gpt-4", temperature=0.0)

# dökümanları oluştur
documents = SimpleDirectoryReader("./data").load_data()

# üreteci (generator) tanımla, soruları oluştur
dataset_generator = RagDatasetGenerator.from_documents(
    documents=documents,
    llm=llm,
    num_questions_per_chunk=10,  # node başına soru sayısını ayarlayın
)

rag_dataset = dataset_generator.generate_questions_from_nodes()
questions = [e.query for e in rag_dataset.examples]
```

## Toplu Değerlendirme (Batch Evaluation)

Ayrıca birçok soru üzerinde bir dizi değerlendiriciyi çalıştırmak için bir toplu değerlendirme yürütücüsü (batch evaluation runner) sağlıyoruz.

```python
from llama_index.core.evaluation import BatchEvalRunner

runner = BatchEvalRunner(
    {"faithfulness": faithfulness_evaluator, "relevancy": relevancy_evaluator},
    workers=8,
)

eval_results = await runner.aevaluate_queries(
    vector_index.as_query_engine(), queries=questions
)
```

## Entegrasyonlar

Ayrıca topluluk değerlendirme araçlarıyla da entegre oluyoruz.

-   [UpTrain](https://github.com/uptrain-ai/uptrain)
-   [DeepEval](https://github.com/confident-ai/deepeval)
-   [Ragas](https://github.com/explodinggradients/ragas/blob/main/docs/howtos/integrations/llamaindex.ipynb)

### DeepEval

[DeepEval](https://github.com/confident-ai/deepeval), kendi tescilli değerlendirme metrikleri tarafından desteklenen 6 değerlendirici (hem getirici hem de üreteç değerlendirmesi için 3 RAG değerlendiricisi dahil) sunar. Başlamak için `deepeval`'i yükleyin:

```bash
pip install -U deepeval
```

Ardından `deepeval`'den değerlendiricileri içe aktarıp kullanabilirsiniz. Tam örnek:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from deepeval.integrations.llama_index import DeepEvalAnswerRelevancyEvaluator

documents = SimpleDirectoryReader("VERI_DIZININIZ").load_data()
index = VectorStoreIndex.from_documents(documents)
rag_application = index.as_query_engine()

# RAG uygulamanıza örnek bir girdi
user_input = "LlamaIndex nedir?"

# LlamaIndex, hem çıktı dizesini hem de getirilen node'ları içeren
# bir yanıt nesnesi döndürür
response_object = rag_application.query(user_input)

evaluator = DeepEvalAnswerRelevancyEvaluator()
evaluation_result = evaluator.evaluate_response(
    query=user_input, response=response_object
)
print(evaluation_result)
```

`deepeval`'den 6 değerlendiricinin tamamını şu şekilde içe aktarabilirsiniz:

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

`deepeval`'in değerlendirme metriklerini LlamaIndex ile nasıl kullanacağınız hakkında daha fazla bilgi edinmek ve tam LLM test paketinden yararlanmak için [dökümantasyonu](https://docs.confident-ai.com/docs/integrations-llamaindex) ziyaret edin.