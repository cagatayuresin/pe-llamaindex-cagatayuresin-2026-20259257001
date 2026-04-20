# Topluluk Erişimi Rehberi (Ensemble Retrieval Guide)

---
title: Topluluk Erişimi Rehberi (Ensemble Retrieval Guide)
 | LlamaIndex OSS Belgeleri
---

RAG uygulamaları oluştururken, karar verilmesi gereken birçok erişim parametresi/stratejisi vardır (örneğin; parça boyutundan -chunk size-, vektör aramaya karşı anahtar kelime veya hibrit arama seçimine kadar).

Düşünce: Ya aynı anda bir dizi stratejiyi deneyebilseydik ve sonuçları herhangi bir AI/reranker (yeniden sıralayıcı)/LLM'e eletebilseydik?

Bu iki amaca hizmet eder:

- Yeniden sıralayıcının iyi olduğu varsayımıyla, birden fazla stratejiden sonuçları havuzda toplayarak daha iyi (ancak daha maliyetli) erişim sonuçları elde etmek.
- Farklı erişim stratejilerini birbirleriyle (yeniden sıralayıcıya göre) kıyaslamak için bir yol sunmak.

Bu rehber, Llama 2 makalesi üzerinden bunu göstermektedir. Farklı parça boyutları (chunk sizes) ve ayrıca farklı indeksler üzerinden topluluk erişimi (ensemble retrieval) gerçekleştiriyoruz.

**NOT**: Yakından ilgili bir rehber, [Topluluk Sorgu Motoru Rehberimizdir (Ensemble Query Engine Guide)](https://gpt-index.readthedocs.io/en/stable/examples/query_engine/ensemble_qury_engine.html) - ona da göz atmayı unutmayın!

```bash
%pip install llama-index-llms-openai
%pip install llama-index-postprocessor-cohere-rerank
%pip install llama-index-readers-file pymupdf
```

```python
%load_ext autoreload
%autoreload 2
```

## Kurulum (Setup)

Burada gerekli içe aktarmaları (imports) tanımlıyoruz.

Eğer bu Notebook'u Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i kurmanız gerekecektir 🦙.

```bash
!pip install llama-index
```

```python
# NOT: Bu SADECE jupyter notebook'ta gereklidir.
# Detaylar: Jupyter arka planda bir olay döngüsü (event-loop) çalıştırır.
#          Bu, asenkron sorgular yapmak için bir olay döngüsü başlattığımızda iç içe geçmiş olay döngülerine neden olur.
#          Buna normalde izin verilmez, kolaylık sağlaması için nest_asyncio kullanıyoruz.
import nest_asyncio


nest_asyncio.apply()
```

```python
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().handlers = []
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.core import SummaryIndex
from llama_index.core.response.notebook_utils import display_response
from llama_index.llms.openai import OpenAI
```

```text
Not: NumExpr 12 çekirdek tespit etti ancak "NUMEXPR_MAX_THREADS" ayarlanmadı, bu nedenle 8 olan güvenli sınır uygulanıyor.
NumExpr varsayılan olarak 8 iş parçacığına (threads) ayarlandı.
```

## Veri Yükleme (Load Data)

Bu bölümde ilk olarak Llama 2 makalesini tek bir belge olarak yüklüyoruz. Ardından, farklı parça boyutlarına göre (chunk sizes) birden çok kez parçalara ayırıyoruz. Her parça boyutuna karşılık gelen ayrı bir vektör indeksi (vector index) oluşturuyoruz.

```bash
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
```

```text
--2023-09-28 12:56:38--  https://arxiv.org/pdf/2307.09288.pdf
Resolving arxiv.org (arxiv.org)... 128.84.21.199
Connecting to arxiv.org (arxiv.org)|128.84.21.199|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 13661300 (13M) [application/pdf]
Saving to: ‘data/llama2.pdf’


data/llama2.pdf     100%[===================>]  13.03M   521KB/s    in 42s


2023-09-28 12:57:20 (320 KB/s) - ‘data/llama2.pdf’ saved [13661300/13661300]
```

```python
from pathlib import Path
from llama_index.core import Document
from llama_index.readers.file import PyMuPDFReader
```

```python
loader = PyMuPDFReader()
docs0 = loader.load(file_path=Path("./data/llama2.pdf"))
doc_text = "\n\n".join([d.get_content() for d in docs0])
docs = [Document(text=doc_text)]
```

Burada farklı parça boyutlarını deniyoruz: 128, 256, 512 ve 1024.

```python
# modülleri ilklendir (initialize)
llm = OpenAI(model="gpt-4")
chunk_sizes = [128, 256, 512, 1024]
nodes_list = []
vector_indices = []
for chunk_size in chunk_sizes:
    print(f"Parça Boyutu (Chunk Size): {chunk_size}")
    splitter = SentenceSplitter(chunk_size=chunk_size)
    nodes = splitter.get_nodes_from_documents(docs)


    # daha sonra takip etmek için parçalara parça boyutunu ekle
    for node in nodes:
        node.metadata["chunk_size"] = chunk_size
        node.excluded_embed_metadata_keys = ["chunk_size"]
        node.excluded_llm_metadata_keys = ["chunk_size"]


    nodes_list.append(nodes)


    # vektör indeksi oluştur
    vector_index = VectorStoreIndex(nodes)
    vector_indices.append(vector_index)
```

```text
Parça Boyutu: 128
Parça Boyutu: 256
Parça Boyutu: 512
Parça Boyutu: 1024
```

## Topluluk Erişicisinin Tanımlanması (Define Ensemble Retriever)

Öncelikle özyinelemeli erişim (recursive retrieval) soyutlamamızı kullanarak bir "topluluk" erişicisi kuruyoruz. Bu şu şekilde çalışır:

- Her parça boyutu için vektör erişicisine karşılık gelen ayrı bir `IndexNode` tanımlayın (128 parça boyutu için erişici, 256 parça boyutu için erişici ve dahası).
- Tüm `IndexNode` nesnelerini tek bir `SummaryIndex` içine yerleştirin; ilgili erişici çağrıldığında *tüm* düğümler döndürülür.
- Kök düğümü (root node) özet indeks erişicisi (summary index retriever) olan bir Özyinelemeli Erişici (Recursive Retriever) tanımlayın. Bu, önce özet indeks erişicisinden tüm düğümleri getirecek ve ardından her parça boyutu için vektör erişicisini özyinelemeli olarak çağıracaktır.
- Nihai sonuçları yeniden sıralayın (rerank).

Sonuç olarak, bir sorgu çalıştırıldığında tüm vektör erişicileri çağrılmış olur.

```python
# topluluk erişimini (ensemble retrieval) dene


from llama_index.core.tools import RetrieverTool
from llama_index.core.schema import IndexNode


# retriever_tools = []
retriever_dict = {}
retriever_nodes = []
for chunk_size, vector_index in zip(chunk_sizes, vector_indices):
    node_id = f"chunk_{chunk_size}"
    node = IndexNode(
        text=(
            "Llama 2 makalesinden ilgili bağlamı getirir (parça boyutu"
            f" {chunk_size})"
        ),
        index_id=node_id,
    )
    retriever_nodes.append(node)
    retriever_dict[node_id] = vector_index.as_retriever()
```

Özyinelemeli erişiciyi tanımlayın.

```python
from llama_index.core.selectors import PydanticMultiSelector


from llama_index.core.retrievers import RouterRetriever
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core import SummaryIndex


# türetilmiş erişici (derived retriever) sadece tüm düğümleri getirecektir
summary_index = SummaryIndex(retriever_nodes)


retriever = RecursiveRetriever(
    root_id="root",
    retriever_dict={"root": summary_index.as_retriever(), **retriever_dict},
)
```

Erişiciyi örnek bir sorgu üzerinde test edelim.

```python
nodes = await retriever.aretrieve(
    "Bana güvenlik ince ayarının (safety fine-tuning) ana yönlerinden bahset"
)
```

```python
print(f"Düğüm sayısı: {len(nodes)}")
for node in nodes:
    print(node.node.metadata["chunk_size"])
    print(node.node.get_text())
```

Nihai getirilen düğüm kümesini işlemek için bir yeniden sıralayıcı (reranker) tanımlayın.

```python
# yeniden sıralayıcıyı (reranker) tanımla
from llama_index.core.postprocessor import LLMRerank, SentenceTransformerRerank
from llama_index.postprocessor.cohere_rerank import CohereRerank


# reranker = LLMRerank()
# reranker = SentenceTransformerRerank(top_n=10)
reranker = CohereRerank(top_n=10)
```

Özyinelemeli erişiciyi + yeniden sıralayıcıyı bir araya getirmek için `retriever sorgu motorunu` (retriever query engine) tanımlayın.

```python
# RetrieverQueryEngine tanımla
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine(retriever, node_postprocessors=[reranker])
```

```python
response = query_engine.query(
    "Bana güvenlik ince ayarının (safety fine-tuning) ana yönlerinden bahset"
)
```

```python
display_response(
    response, show_source=True, source_length=500, show_source_metadata=True
)
```

### Her Parçanın Göreli Öneminin Analiz Edilmesi (Analyzing the Relative Importance of each Chunk)

Topluluk tabanlı erişimin (ensemble-based retrieval) ilginç bir özelliği, yeniden sıralama yoluyla, nihai getirilen kümedeki parçaların sıralamasını kullanarak her parça boyutunun önemini belirleyebilmemizdir. Örneğin, belirli parça boyutları her zaman en üstte yer alıyorsa, bunlar muhtemelen sorguyla daha ilgilidir.

```python
# birleşik sıralamadaki konumlara göre her parça boyutu için ortalama hassasiyeti (average precision) hesapla
from collections import defaultdict
import pandas as pd




def mrr_all(metadata_values, metadata_key, source_nodes):
    # source_nodes sıralı bir listedir
    # her bir değerin üzerinden geç ve source_nodes içindeki konumunu bul
    value_to_mrr_dict = {}
    for metadata_value in metadata_values:
        mrr = 0
        for idx, source_node in enumerate(source_nodes):
            if source_node.node.metadata[metadata_key] == metadata_value:
                mrr = 1 / (idx + 1)
                break
            else:
                continue


        # AP'yi normalleştir, sözlüğe ekle
        value_to_mrr_dict[metadata_value] = mrr


    df = pd.DataFrame(value_to_mrr_dict, index=["MRR"])
    df.style.set_caption("Ortalama Karşılıklı Sıralama (Mean Reciprocal Rank)")
    return df
```

```python
# Her parça boyutu için Ortalama Karşılıklı Sıralamayı hesaplayın (yüksek olan daha iyidir)
# 256 parça boyutunun en yüksek dereceli sonuçlara sahip olduğunu görebiliriz.
print("Her Parça Boyutu İçin Ortalama Karşılıklı Sıralama (Mean Reciprocal Rank)")
mrr_all(chunk_sizes, "chunk_size", response.source_nodes)
```

```text
Her Parça Boyutu İçin Ortalama Karşılıklı Sıralama
```

```css
.dataframe tbody tr th {
    vertical-align: top;
}


.dataframe thead th {
    text-align: right;
}
```

|     | 128      | 256 | 512 | 1024 |
| --- | -------- | --- | --- | ---- |
| MRR | 0.333333 | 1.0 | 0.5 | 0.25 |

## Değerlendirme (Evaluation)

Bir topluluk erişicisinin "temel" (baseline) erişiciye kıyasla ne kadar iyi çalıştığını daha titiz bir şekilde değerlendiriyoruz.

Bir değerlendirme kıyaslama veri seti tanımlıyoruz/yüklüyoruz ve ardından üzerinde farklı değerlendirmeler çalıştırıyoruz.

**UYARI**: Bu işlem, özellikle GPT-4 ile *pahalı* olabilir. Dikkatli olun ve örneklem boyutunu bütçenize göre ayarlayın.

```
from llama_index.core.evaluation import DatasetGenerator, QueryResponseDataset
from llama_index.llms.openai import OpenAI
import nest_asyncio


nest_asyncio.apply()
```

```
# NOTE: run this if the dataset isn't already saved
eval_llm = OpenAI(model="gpt-4")
# generate questions from the largest chunks (1024)
dataset_generator = DatasetGenerator(
    nodes_list[-1],
    llm=eval_llm,
    show_progress=True,
    num_questions_per_chunk=2,
)
```

```
eval_dataset = await dataset_generator.agenerate_dataset_from_nodes(num=60)
```

```
eval_dataset.save_json("data/llama2_eval_qr_dataset.json")
```

```
# optional
eval_dataset = QueryResponseDataset.from_json(
    "data/llama2_eval_qr_dataset.json"
)
```

### Compare Results

```
import asyncio
import nest_asyncio


nest_asyncio.apply()
```

```
from llama_index.core.evaluation import (
    CorrectnessEvaluator,
    SemanticSimilarityEvaluator,
    RelevancyEvaluator,
    FaithfulnessEvaluator,
    PairwiseComparisonEvaluator,
)


# NOTE: can uncomment other evaluators
evaluator_c = CorrectnessEvaluator(llm=eval_llm)
evaluator_s = SemanticSimilarityEvaluator(llm=eval_llm)
evaluator_r = RelevancyEvaluator(llm=eval_llm)
evaluator_f = FaithfulnessEvaluator(llm=eval_llm)


pairwise_evaluator = PairwiseComparisonEvaluator(llm=eval_llm)
```

```
from llama_index.core.evaluation.eval_utils import (
    get_responses,
    get_results_df,
)
from llama_index.core.evaluation import BatchEvalRunner


max_samples = 60


eval_qs = eval_dataset.questions
qr_pairs = eval_dataset.qr_pairs
ref_response_strs = [r for (_, r) in qr_pairs]


# resetup base query engine and ensemble query engine
# base query engine
base_query_engine = vector_indices[-1].as_query_engine(similarity_top_k=2)
# ensemble query engine
reranker = CohereRerank(top_n=4)
query_engine = RetrieverQueryEngine(retriever, node_postprocessors=[reranker])
```

```
base_pred_responses = get_responses(
    eval_qs[:max_samples], base_query_engine, show_progress=True
)
```

```
pred_responses = get_responses(
    eval_qs[:max_samples], query_engine, show_progress=True
)
```

```
import numpy as np


pred_response_strs = [str(p) for p in pred_responses]
base_pred_response_strs = [str(p) for p in base_pred_responses]
```

```
evaluator_dict = {
    "correctness": evaluator_c,
    "faithfulness": evaluator_f,
    # "relevancy": evaluator_r,
    "semantic_similarity": evaluator_s,
}
batch_runner = BatchEvalRunner(evaluator_dict, workers=1, show_progress=True)
```

```
eval_results = await batch_runner.aevaluate_responses(
    queries=eval_qs[:max_samples],
    responses=pred_responses[:max_samples],
    reference=ref_response_strs[:max_samples],
)
```

```
base_eval_results = await batch_runner.aevaluate_responses(
    queries=eval_qs[:max_samples],
    responses=base_pred_responses[:max_samples],
    reference=ref_response_strs[:max_samples],
)
```

```
results_df = get_results_df(
    [eval_results, base_eval_results],
    ["Ensemble Retriever", "Base Retriever"],
    ["correctness", "faithfulness", "semantic_similarity"],
)
display(results_df)
```

```
.dataframe tbody tr th {
    vertical-align: top;
}


.dataframe thead th {
    text-align: right;
}
```

|   | names              | correctness | faithfulness | semantic\_similarity |
| - | ------------------ | ----------- | ------------ | -------------------- |
| 0 | Ensemble Retriever | 4.375000    | 0.983333     | 0.964546             |
| 1 | Base Retriever     | 4.066667    | 0.983333     | 0.956692             |

```
batch_runner = BatchEvalRunner(
    {"pairwise": pairwise_evaluator}, workers=3, show_progress=True
)


pairwise_eval_results = await batch_runner.aevaluate_response_strs(
    queries=eval_qs[:max_samples],
    response_strs=pred_response_strs[:max_samples],
    reference=base_pred_response_strs[:max_samples],
)
```

```
results_df = get_results_df(
    [eval_results, base_eval_results],
    ["Ensemble Retriever", "Base Retriever"],
    ["pairwise"],
)
display(results_df)
```

```
.dataframe tbody tr th {
    vertical-align: top;
}


.dataframe thead th {
    text-align: right;
}
```

|   | names               | pairwise |
| - | ------------------- | -------- |
| 0 | Pairwise Comparison | 0.5      |
