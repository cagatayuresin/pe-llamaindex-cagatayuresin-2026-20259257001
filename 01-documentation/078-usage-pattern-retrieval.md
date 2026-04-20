# Kullanım Kalıbı (Usage Pattern - Getirme/Retrieval)

## `RetrieverEvaluator` Kullanımı

Bu, bir getirici (retriever) verildiğinde tek bir sorgu + temel gerçeklik döküman seti üzerinden değerlendirme çalıştırır.

Standart uygulama, `from_metric_names` ile bir dizi geçerli metrik belirtmektir.

```python
from llama_index.core.evaluation import RetrieverEvaluator

# getiriciyi bir yerde tanımlayın (örneğin indeksten)
# retriever = index.as_retriever(similarity_top_k=2)
retriever = ...

retriever_evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"], retriever=retriever
)

retriever_evaluator.evaluate(
    query="sorgu", expected_ids=["node_id1", "node_id2"]
)
```

## Değerlendirme Veri Kümesi Oluşturma

Soru + node kimliklerinden oluşan bir getirme değerlendirme veri kümesini manuel olarak düzenleyebilirsiniz. Ayrıca `generate_question_context_pairs` fonksiyonumuzla mevcut bir metin külliyatı (corpus) üzerinden sentetik veri kümesi oluşturma imkanı sunuyoruz:

```python
from llama_index.core.evaluation import generate_question_context_pairs

qa_dataset = generate_question_context_pairs(
    nodes, llm=llm, num_questions_per_chunk=2
)
```

Döndürülen sonuç bir `EmbeddingQAFinetuneDataset` nesnesidir (`queries`, `relevant_docs` ve `corpus` içerir).

### `RetrieverEvaluator` ile Entegre Etme

Bir veri kümesi üzerinde `RetrieverEvaluator`'ı toplu modda (batch mode) çalıştırmak için kolaylık sağlayan bir fonksiyon sunuyoruz.

```python
eval_results = await retriever_evaluator.aevaluate_dataset(qa_dataset)
```

Bu, her sorgu için ayrı ayrı `.evaluate` çağırmaya çalışmanızdan çok daha hızlı sonuç verecektir.