# Değerlendirme (Evaluating)

Değerlendirme ve kıyaslama (benchmarking), LLM geliştirmede kritik kavramlardır. Bir LLM uygulamasının (RAG, ajanlar) performansını iyileştirmek için onu ölçmenin bir yoluna sahip olmalısınız.

LlamaIndex, üretilen sonuçların kalitesini ölçmek için temel modüller sunar. Ayrıca getirme (retrieval) kalitesini ölçmek için de temel modüller sunuyoruz. LlamaIndex'te değerlendirmenin nasıl çalıştığı hakkında daha fazla bilgiyi [modül kılavuzlarımızda](/python/framework/module_guides/evaluating) bulabilirsiniz.

## Yanıt Değerlendirmesi

Yanıt, getirilen bağlamla (context) eşleşiyor mu? Ayrıca sorguyla eşleşiyor mu? Referans cevapla veya yönergelerle eşleşiyor mu? İşte tek bir yanıtı Sadakat (Faithfulness) açısından değerlendiren basit bir örnek; yani yanıtın bağlamla uyumlu olup olmadığı, örneğin halüsinasyonlardan arınmış olup olmadığı:

```python
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import FaithfulnessEvaluator

# llm oluştur
llm = OpenAI(model="gpt-4", temperature=0.0)

# indeks oluştur
...
vector_index = VectorStoreIndex(...)

# değerlendiriciyi (evaluator) tanımla
evaluator = FaithfulnessEvaluator(llm=llm)

# indeksi sorgula
query_engine = vector_index.as_query_engine()
response = query_engine.query(
    "Amerikan Devrimi'nde New York City'de hangi savaşlar gerçekleşti?"
)

# yanıtı değerlendir
eval_result = evaluator.evaluate_response(response=response)
print(str(eval_result.passing))
```

Yanıt hem cevabı hem de cevabın oluşturulduğu kaynağı içerir; değerlendirici bunları karşılaştırır ve yanıtın kaynağa sadık olup olmadığını belirler.

[Yanıt değerlendirmesi](/python/framework/module_guides/evaluating/usage_pattern) hakkında modül kılavuzlarımızdan daha fazla bilgi edinebilirsiniz.

## Getirme (Retrieval) Değerlendirmesi

Getirilen kaynaklar sorguyla alakalı mı? İşte tek bir getirme işlemini değerlendiren basit bir örnek:

```python
from llama_index.core.evaluation import RetrieverEvaluator

# getiriciyi (retriever) bir yerde tanımlayın (örneğin indeksten)
# retriever = index.as_retriever(similarity_top_k=2)
retriever = ...

retriever_evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"], retriever=retriever
)

retriever_evaluator.evaluate(
    query="sorgu", expected_ids=["node_id1", "node_id2"]
)
```

Bu, sorgu için getirilenleri, getirilmesi beklenen bir dizi node ile karşılaştırır.

Gerçekte, bütün bir getirme grubunu değerlendirmek istersiniz; bunu [getirme değerlendirmesi](/python/framework/module_guides/evaluating/usage_pattern_retrieval) hakkındaki modül kılavuzumuzdan öğrenebilirsiniz.

## İlgili kavramlar

Barındırılan, uzak bir LLM'e çağrılar yapıyorsanız [uygulamanızın maliyetini analiz etmekle](/python/framework/understanding/evaluating/cost_analysis) ilgilenebilirsiniz.