# Tonic Validate

## Tonic Validate Nedir?

Tonic Validate, erişimle zenginleştirilmiş üretim (RAG) sistemleri geliştiren kişilerin sistemlerinin performansını değerlendirmeleri için bir araçtır. LlamaIndex kurulumunuzun performansının tek seferlik spot kontrolleri için Tonic Validate'i kullanabilir veya hatta onu Github Actions gibi mevcut bir CI/CD sistemi içinde kullanabilirsiniz. Tonic Validate'in iki bölümü vardır:

1. Açık Kaynak SDK
2. [Web Arayüzü](https://validate.tonic.ai/)

Tercih ederseniz Web Arayüzünü kullanmadan SDK'yı kullanabilirsiniz. SDK, RAG sisteminizi değerlendirmek için gereken tüm araçları içerir. Web arayüzünün amacı, sonuçlarınızı görselleştirmek için SDK'nın üzerinde bir katman sağlamaktır. Bu, sadece ham sayıları görüntülemek yerine sisteminizin performansı hakkında daha iyi bir fikir edinmenizi sağlar.

Web arayüzünü kullanmak istiyorsanız, ücretsiz bir hesaba kaydolmak için [buraya](https://validate.tonic.ai/) gidebilirsiniz.

## Tonic Validate Nasıl Kullanılır?

### Tonic Validate Kurulumu

Tonic Validate'i aşağıdaki komutla yükleyebilirsiniz:

```bash
pip install tonic-validate
```

Tonic Validate'i kullanmak için bir OpenAI anahtarı sağlamanız gerekir, çünkü puan hesaplamaları arka uçta bir LLM kullanır. `OPENAI_API_KEY` çevre değişkenini OpenAI API anahtarınıza ayarlayarak bir OpenAI anahtarı belirleyebilirsiniz.

```python
import os

os.environ["OPENAI_API_KEY"] = "openai-api-anahtarinizi-buraya-koyun"
```

Sonuçlarınızı arayüze yüklüyorsanız, [web arayüzü](https://validate.tonic.ai/) için hesap kurulumu sırasında aldığınız Tonic Validate API anahtarınızı da ayarladığınızdan emin olun. Web arayüzünde henüz hesabınızı oluşturmadıysanız [buradan](https://validate.tonic.ai/) yapabilirsiniz. API anahtarını aldıktan sonra onu `TONIC_VALIDATE_API_KEY` çevre değişkeni aracılığıyla ayarlayabilirsiniz.

```python
import os

os.environ["TONIC_VALIDATE_API_KEY"] = "validate-api-anahtarinizi-buraya-koyun"
```

### Tek Soru Kullanım Örneği

Bu örnek için, LLM yanıt cevabıyla eşleşmeyen referans doğru cevabı olan bir soru örneğimiz var. Doğru cevabı içeren iki adet erişilen bağlam parçası (context chunks) bulunmaktadır.

```python
question = "Sam Altman'ı iyi bir kurucu yapan nedir?"
reference_answer = "Zekidir ve büyük bir irade gücüne sahiptir."
llm_answer = "Zeki olduğu için iyi bir kurucudur."
retrieved_context_list = [
    "Sam Altman iyi bir kurucudur. Çok zekidir.",
    "Sam Altman'ı bu kadar iyi bir kurucu yapan şey büyük irade gücüdür.",
]
```

Yanıt benzerliği puanı (answer similarity score), LLM yanıtının referans yanıtla ne kadar eşleştiğini puanlayan 0 ile 5 arasında bir puandır. Bu durumda mükemmel bir şekilde eşleşmedikleri için yanıt benzerliği puanı mükemmel bir 5 değildir.

```python
answer_similarity_evaluator = AnswerSimilarityEvaluator()
score = await answer_similarity_evaluator.aevaluate(
    question,
    llm_answer,
    retrieved_context_list,
    reference_response=reference_answer,
)
print(score)
# >> EvaluationResult(query="Sam Altman'ı iyi bir kurucu yapan nedir?", contexts=['Sam Altman iyi bir kurucudur. Çok zekidir.', "Sam Altman'ı bu kadar iyi bir kurucu yapan şey büyük irade gücüdür."], response='Zeki olduğu için iyi bir kurucudur.', passing=None, feedback=None, score=4.0, pairwise_source=None, invalid_result=False, invalid_reason=None)
```

Yanıt tutarlılığı puanı (answer consistency score) 0.0 ile 1.0 arasındadır ve yanıtın erişilen bağlamda görünmeyen bilgiler içerip içermediğini ölçer. Bu durumda yanıt erişilen bağlamda görünmektedir, bu nedenle puan 1'dir.

```python
answer_consistency_evaluator = AnswerConsistencyEvaluator()


score = await answer_consistency_evaluator.aevaluate(
    question, llm_answer, retrieved_context_list
)
print(score)
# >> EvaluationResult(query="Sam Altman'ı iyi bir kurucu yapan nedir?", contexts=['Sam Altman iyi bir kurucudur. Çok zekidir.', "Sam Altman'ı bu kadar iyi bir kurucu yapan şey büyük irade gücüdür."], response='Zeki olduğu için iyi bir kurucudur.', passing=None, feedback=None, score=1.0, pairwise_source=None, invalid_result=False, invalid_reason=None)
```

Zenginleştirme doğruluğu (augmentation accuracy), erişilen bağlamın yanıtta yer alan yüzdesini ölçer. Bu durumda erişilen bağlamlardan biri yanıtta yer almaktadır, bu nedenle bu puan 0.5'tir.

```python
augmentation_accuracy_evaluator = AugmentationAccuracyEvaluator()


score = await augmentation_accuracy_evaluator.aevaluate(
    question, llm_answer, retrieved_context_list
)
print(score)
# >> EvaluationResult(query="Sam Altman'ı iyi bir kurucu yapan nedir?", contexts=['Sam Altman iyi bir kurucudur. Çok zekidir.', "Sam Altman'ı bu kadar iyi bir kurucu yapan şey büyük irade gücüdür."], response='Zeki olduğu için iyi bir kurucudur.', passing=None, feedback=None, score=0.5, pairwise_source=None, invalid_result=False, invalid_reason=None)
```

Zenginleştirme hassasiyeti (augmentation precision), ilgili erişilen bağlamın yanıta girip girmediğini ölçer. Erişilen bağlamların her ikisi de ilgilidir ancak sadece biri yanıta girer. Bu nedenle bu puan 0.5'tir.

```python
augmentation_precision_evaluator = AugmentationPrecisionEvaluator()


score = await augmentation_precision_evaluator.aevaluate(
    question, llm_answer, retrieved_context_list
)
print(score)
# >> EvaluationResult(query="Sam Altman'ı iyi bir kurucu yapan nedir?", contexts=['Sam Altman iyi bir kurucudur. Çok zekidir.', "Sam Altman'ı bu kadar iyi bir kurucu yapan şey büyük irade gücüdür."], response='Zeki olduğu için iyi bir kurucudur.', passing=None, feedback=None, score=0.5, pairwise_source=None, invalid_result=False, invalid_reason=None)
```

Erişim hassasiyeti (retrieval precision), erişilen bağlamın soruyu cevaplamak için ilgili olan yüzdesini ölçer. Bu durumda her iki erişilen bağlam da soruyu cevaplamak için ilgilidir, bu nedenle puan 1.0'dır.

```python
retrieval_precision_evaluator = RetrievalPrecisionEvaluator()


score = await retrieval_precision_evaluator.aevaluate(
    question, llm_answer, retrieved_context_list
)
print(score)
# >> EvaluationResult(query="Sam Altman'ı iyi bir kurucu yapan nedir?", contexts=['Sam Altman iyi bir kurucudur. Çok zekidir.', "Sam Altman'ı bu kadar iyi bir kurucu yapan şey büyük irade gücüdür."], response='Zeki olduğu için iyi bir kurucudur.', passing=None, feedback=None, score=1.0, pairwise_source=None, invalid_result=False, invalid_reason=None)
```

TonicValidateEvaluator, Tonic Validate'in tüm metriklerini bir kerede hesaplayabilir.

```python
tonic_validate_evaluator = TonicValidateEvaluator()


scores = await tonic_validate_evaluator.aevaluate(
    question,
    llm_answer,
    retrieved_context_list,
    reference_response=reference_answer,
)
print(scores.score_dict)
# >> {
#     'answer_consistency': 1.0,
#     'answer_similarity': 4.0,
#     'augmentation_accuracy': 0.5,
#     'augmentation_precision': 0.5,
#     'retrieval_precision': 1.0
# }
```

### Aynı anda birden fazla soruyu değerlendirme

TonicValidateEvaluator'ı kullanarak aynı anda birden fazla sorgu ve yanıtı değerlendirebilir ve [Tonic Validate Arayüzüne](https://validate.tonic.ai) kaydedilebilen bir `tonic_validate` Run nesnesi döndürebilirsiniz.

Bunu yapmak için soruları, LLM yanıtlarını, erişilen bağlam listelerini ve referans yanıtları listelere koyar ve `evaluate_run` metodunu çağırırsınız.

```python
questions = ["Fransa'nın başkenti neresidir?", "İspanya'nın başkenti neresidir?"]
reference_answers = ["Paris", "Madrid"]
llm_answers = ["Paris", "Madrid"]
retrieved_context_lists = [
    [
        "Paris, Fransa'nın başkenti ve en kalabalık şehridir.",
        "Fransa'nın başkenti Paris, büyük bir Avrupa şehri ve sanat, moda, gastronomi ve kültür için küresel bir merkezdir.",
    ],
    [
        "Madrid, İspanya'nın başkenti ve en büyük şehridir.",
        "İspanya'nın merkezi başkenti Madrid, zarif bulvarların ve Buen Retiro gibi geniş, bakımlı parkların şehridir.",
    ],
]


tonic_validate_evaluator = TonicValidateEvaluator()


scores = await tonic_validate_evaluator.aevaluate_run(
    [questions], [llm_answers], [retrieved_context_lists], [reference_answers]
)
print(scores.run_data[0].scores)
# >> {
#     'answer_consistency': 1.0,
#     'answer_similarity': 3.0,
#     'augmentation_accuracy': 0.5,
#     'augmentation_precision': 0.5,
#     'retrieval_precision': 1.0
# }
```

### Sonuçları Arayüze Yükleme

Puanlarınızı arayüze yüklemek istiyorsanız Tonic Validate API'sini kullanabilirsiniz. Bunu yapmadan önce, [Tonic Validate Kurulumu](#tonic-validate-kurulumu) bölümünde açıklandığı gibi `TONIC_VALIDATE_API_KEY`'in ayarlandığından emin olun. Ayrıca Tonic Validate arayüzünde bir proje oluşturduğunuzdan ve proje kimliğini kopyaladığınızdan emin olmanız gerekir. API Anahtarı ve proje ayarlandıktan sonra Validate API'sini başlatabilir ve sonuçları yükleyebilirsiniz.

```python
validate_api = ValidateApi()
project_id = "proje-id-niz"
validate_api.upload_run(project_id, scores)
```

Artık sonuçlarınızı Tonic Validate arayüzünde görebilirsiniz!

![Tonic Validate Grafiği](./../../_static/integrations/tonic-validate-graph.png)

### Uçtan Uça Örnek (End to End Example)

Burada size Tonic Validate'i Llama Index ile uçtan uca nasıl kullanacağınızı göstereceğiz. İlk olarak, Llama Index CLI'yı kullanarak üzerinde çalışmak üzere Llama Index için bir veri kümesi indirelim.

```bash
llamaindex-cli download-llamadataset EvaluatingLlmSurveyPaperDataset --download-dir ./data
```

Şimdi, `llama.py` adında bir python dosyası oluşturabilir ve içine aşağıdaki kodu koyabiliriz.

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex


documents = SimpleDirectoryReader(input_dir="./data/source_files").load_data()
index = VectorStoreIndex.from_documents(documents=documents)
query_engine = index.as_query_engine()
```

Bu kod aslında sadece veri kümesi dosyalarını yükler ve ardından Llama Index'i başlatır.

Llama Index'in CLI'sı ayrıca örnek veri kümelerinde test etmek için kullanabileceğiniz bir soru ve yanıt listesi de indirir. Bu soruları ve yanıtları kullanmak istiyorsanız aşağıdaki kodu kullanabilirsiniz.

```python
from llama_index.core.llama_dataset import LabelledRagDataset

rag_dataset = LabelledRagDataset.from_json("./data/rag_dataset.json")


# Mevcut tüm seti çalıştırmak çok uzun sürdüğü için sadece 10 soru üzerinde işlem yapacağız
questions = [item.query for item in rag_dataset.examples][:10]
reference_answers = [item.reference_answer for item in rag_dataset.examples][
    :10
]
```

Şimdi Llama Index'ten yanıtları alabiliriz.

```python
llm_answers = []
retrieved_context_lists = []
for question in questions:
    response = query_engine.query(question)
    context_list = [x.text for x in response.source_nodes]
    retrieved_context_lists.append(context_list)
    llm_answers.append(response.response)
```

Şimdi puanlamak için aşağıdakini yapabiliriz:

```python
from tonic_validate.metrics import AnswerSimilarityMetric
from llama_index.evaluation.tonic_validate import TonicValidateEvaluator


tonic_validate_evaluator = TonicValidateEvaluator(
    metrics=[AnswerSimilarityMetric()], model_evaluator="gpt-4-1106-preview"
)

scores = tonic_validate_evaluator.evaluate_run(
    questions, retrieved_context_lists, reference_answers, llm_answers
)
print(scores.overall_scores)
```

Puanlarınızı arayüze yüklemek istiyorsanız Tonic Validate API'sini kullanabilirsiniz. Bunu yapmadan önce [Tonic Validate Kurulumu](#tonic-validate-kurulumu) bölümünde açıklandığı gibi `TONIC_VALIDATE_API_KEY`'in ayarlandığından emin olun. Ayrıca Tonic Validate arayüzünde bir proje oluşturduğunuzdan ve proje kimliğini kopyaladığınızdan emin olmanız gerekir. API Anahtarı ve proje ayarlandıktan sonra Validate API'sini başlatabilir ve sonuçları yükleyebilirsiniz.

```python
validate_api = ValidateApi()
project_id = "proje-id-niz"
validate_api.upload_run(project_id, run)
```

## Daha Fazla Belgelendirme

Buradaki dökümantasyona ek olarak, sonuçları yüklemek için API'mizle nasıl etkileşim kuracağınız hakkında daha fazla dökümantasyon için [Tonic Validate'in Github sayfasını](https://github.com/TonicAI/tonic_validate) da ziyaret edebilirsiniz.