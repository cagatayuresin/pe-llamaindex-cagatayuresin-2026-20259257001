# `LabelledEvaluatorDataset`'ler ile Değerlendiricileri Değerlendirme

Llama-dataset'lerinin amacı, geliştiricilere LLM sistemlerini veya görevlerini hızlı bir şekilde kıyaslama (benchmark) imkanı sunmaktır. Bu anlayışla `LabelledEvaluatorDataset`, değerlendiricilerin (evaluators) değerlendirilmesini sorunsuz ve zahmetsiz bir şekilde kolaylaştırmak için mevcuttur.

Bu veri kümesi, temel olarak şu öznitelikleri taşıyan örneklerden oluşur: `query` (sorgu), `answer` (cevap), `ground_truth_answer` (temel gerçeklik cevabı), `reference_score` (referans puan) ve `reference_feedback` (referans geri bildirim) ile birlikte bazı diğer tamamlayıcı öznitelikler. Bu veri kümesiyle değerlendirme yapma süreci; sağlanan bir LLM değerlendiricisiyle veri kümesi üzerinde tahminler yürütmeyi ve ardından bu tahminleri ilgili referanslarla hesaplamalı olarak karşılaştırarak değerlendirmelerin iyiliğini ölçen metrikleri hesaplamayı içerir.

Aşağıda, bahsedilen süreç akışını kolayca yönetmek için `EvaluatorBenchmarkerPack` kullanan bir kod parçası bulunmaktadır.

```python
from llama_index.core.llama_dataset import download_llama_dataset
from llama_index.core.llama_pack import download_llama_pack
from llama_index.core.evaluation import CorrectnessEvaluator
from llama_index.llms.gemini import Gemini

# veri kümesini indir
evaluator_dataset, _ = download_llama_dataset(
    "MiniMtBenchSingleGradingDataset", "./mini_mt_bench_data"
)

# değerlendiriciyi tanımla
gemini_pro_llm = Gemini(model="models/gemini-pro", temperature=0)
evaluator = CorrectnessEvaluator(llm=gemini_pro_llm)

# EvaluatorBenchmarkerPack'i indir ve kıyaslayıcıyı (benchmarker) tanımla
EvaluatorBenchmarkerPack = download_llama_pack(
    "EvaluatorBenchmarkerPack", "./pack"
)
evaluator_benchmarker = EvaluatorBenchmarkerPack(
    evaluator=evaluators["gpt-3.5"],
    eval_dataset=evaluator_dataset,
    show_progress=True,
)

# kıyaslama sonucunu üret
benchmark_df = await evaluator_benchmarker.arun(
    batch_size=5, sleep_time_in_seconds=0.5
)
```

## İlgili `LabelledPairwiseEvaluatorDataset`

İlgili bir llama-dataset, yine bir değerlendiriciyi değerlendirmeyi amaçlayan `LabelledPairwiseEvaluatorDataset` veri kümesidir. Ancak bu sefer değerlendiriciden, verilen bir sorguya verilen bir çift LLM yanıtını karşılaştırması ve aralarından daha iyi olanı belirlemesi istenir. Yukarıda açıklanan kullanım akışı, `LabelledEvaluatorDataset` ile tamamen aynıdır; tek fark, LLM değerlendiricisinin ikili karşılaştırma (pairwise) görevi yapabilecek donanımda olması gerektiğidir; yani bir `PairwiseComparisonEvaluator` olmalıdır.

## Daha fazla öğrenme materyali

Bu veri kümelerini iş başında görmek için, MT-Bench veri kümesinin hafifçe uyarlanmış versiyonları üzerinde LLM değerlendiricilerini kıyaslayan aşağıda listelenen notebook'lara mutlaka göz atın.

-   [MTBench Tekli Derecelendirme (Single Grading)](/python/examples/evaluation/mt_bench_single_grading)
-   [MTBench İnsan Hakem (Human Judge)](/python/examples/evaluation/mt_bench_human_judgement)