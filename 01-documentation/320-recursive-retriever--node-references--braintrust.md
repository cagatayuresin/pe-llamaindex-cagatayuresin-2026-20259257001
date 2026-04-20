# Özyinelemeli Erişici + Düğüm Referansları + Braintrust (Recursive Retriever + Node References + Braintrust)

---
title: Özyinelemeli Erişici + Düğüm Referansları + Braintrust (Recursive Retriever + Node References + Braintrust)
 | LlamaIndex OSS Belgeleri
---

Bu kılavuz, düğüm ilişkilerini gezinmek ve "referanslara" dayalı düğümleri getirmek için özyinelemeli erişimin (recursive retrieval) nasıl kullanılacağını gösterir.

Düğüm referansları güçlü bir kavramdır. İlk erişimi gerçekleştirdiğinizde, ham metin yerine referansı getirmek isteyebilirsiniz. Aynı düğüme işaret eden birden fazla referansınız olabilir.

Bu kılavuzda düğüm referanslarının bazı farklı kullanımlarını keşfediyoruz:

- **Parça referansları (Chunk references)**: Daha büyük bir parçaya atıfta bulunan farklı parça boyutları.
- **Metaveri referansları (Metadata references)**: Daha büyük bir parçaya atıfta bulunan Özetler + Üretilen Sorular.

Özyinelemeli erişim + düğüm referansı yöntemlerimizin ne kadar iyi çalıştığını [Braintrust](https://www.braintrustdata.com/) kullanarak değerlendiriyoruz. Braintrust, yapay zeka ürünleri oluşturmak için kurumsal düzeyde bir yığındır (stack). Değerlendirmelerden istem (prompt) alanına, veri yönetimine kadar, yapay zekayı işinize dahil etme konusundaki belirsizliği ve zahmeti ortadan kaldırıyoruz.

Aşağıdakiler için örnek değerlendirme panolarını burada görebilirsiniz:

- [Temel erişici (base retriever)](https://www.braintrustdata.com/app/braintrustdata.com/p/llamaindex-recurisve-retrievers/baseRetriever)
- [Özyinelemeli metaveri erişicisi (recursive metadata retreiver)](https://www.braintrustdata.com/app/braintrustdata.com/p/llamaindex-recurisve-retrievers/recursiveMetadataRetriever)
- [Özyinelemeli parça erişicisi (recursive chunk retriever)](https://www.braintrustdata.com/app/braintrustdata.com/p/llamaindex-recurisve-retrievers/recursiveChunkRetriever)

```bash
%pip install llama-index-llms-openai
%pip install llama-index-readers-file
```

```python
%load_ext autoreload
%autoreload 2
# NOT: YOUR_OPENAI_API_KEY kısmını OpenAI API Anahtarınızla ve YOUR_BRAINTRUST_API_KEY kısmını BrainTrust API anahtarınızla değiştirin. Tırnak içine almayın.
# Braintrust'a https://braintrustdata.com/ adresinden kaydolun ve API anahtarınızı https://www.braintrustdata.com/app/braintrustdata.com/settings/api-keys adresinden alın.
%env OPENAI_API_KEY=
%env BRAINTRUST_API_KEY=
%env TOKENIZERS_PARALLELISM=true # Bu, Chroma'dan bir uyarı mesajı almamak için gereklidir
```

```bash
%pip install -U llama_hub llama_index braintrust autoevals pypdf pillow transformers torch torchvision
```

## Veriyi Yükleme + Kurulum (Load Data + Setup)

Bu bölümde Llama 2 makalesini indiriyoruz ve bir dizi başlangıç düğümü oluşturuyoruz (parça boyutu 1024).

```bash
!mkdir data
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
```

```python
from pathlib import Path
from llama_index.readers.file import PDFReader
from llama_index.core.response.notebook_utils import display_source_node
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
import json
```

```python
loader = PDFReader()
docs0 = loader.load_data(file=Path("./data/llama2.pdf"))
```

```python
from llama_index.core import Document


doc_text = "\n\n".join([d.get_content() for d in docs0])
docs = [Document(text=doc_text)]
```

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import IndexNode
```

```python
node_parser = SentenceSplitter(chunk_size=1024)
```

```python
base_nodes = node_parser.get_nodes_from_documents(docs)
# düğüm kimliklerini (ID) sabit olarak ayarla
for idx, node in enumerate(base_nodes):
    node.id_ = f"node-{idx}"
```

```python
from llama_index.core.embeddings import resolve_embed_model


embed_model = resolve_embed_model("local:BAAI/bge-small-en")
llm = OpenAI(model="gpt-3.5-turbo")
```

## Temel Erişici (Baseline Retriever)

Gömme benzerliğine göre en iyi k ham metin düğümünü getiren temel bir erişici tanımlayın.

```python
base_index = VectorStoreIndex(base_nodes, embed_model=embed_model)
base_retriever = base_index.as_retriever(similarity_top_k=2)
```

```python
retrievals = base_retriever.retrieve(
    "Can you tell me about the key concepts for safety finetuning"
)
```

```python
for n in retrievals:
    display_source_node(n, source_length=1500)
```

```python
query_engine_base = RetrieverQueryEngine.from_args(base_retriever, llm=llm)
```

```python
response = query_engine_base.query(
    "Can you tell me about the key concepts for safety finetuning"
)
print(str(response))
```

## Parça Referansları: Daha Büyük Ana Parçaya Atıfta Bulunan Küçük Alt Parçalar

Bu kullanım örneğinde, daha büyük ana parçaları işaret eden daha küçük parçalardan oluşan bir grafiğin nasıl oluşturulacağını gösteriyoruz.

Sorgu zamanında, daha küçük parçaları getiriyoruz ancak daha büyük parçalara olan referansları takip ediyoruz. Bu, sentez için daha fazla bağlama sahip olmamızı sağlar.

```python
sub_chunk_sizes = [128, 256, 512]
sub_node_parsers = [SentenceSplitter(chunk_size=c) for c in sub_chunk_sizes]


all_nodes = []


for base_node in base_nodes:
    for n in sub_node_parsers:
        sub_nodes = n.get_nodes_from_documents([base_node])
        sub_inodes = [
            IndexNode.from_text_node(sn, base_node.node_id) for sn in sub_nodes
        ]
        all_nodes.extend(sub_inodes)


    # orijinal düğümü de ekle
    original_node = IndexNode.from_text_node(base_node, base_node.node_id)
    all_nodes.append(original_node)
```

```python
all_nodes_dict = {n.node_id: n for n in all_nodes}
```

```python
vector_index_chunk = VectorStoreIndex(all_nodes, embed_model=embed_model)
```

```python
vector_retriever_chunk = vector_index_chunk.as_retriever(similarity_top_k=2)
```

```python
retriever_chunk = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever_chunk},
    node_dict=all_nodes_dict,
    verbose=True,
)
```

```python
nodes = retriever_chunk.retrieve(
    "Can you tell me about the key concepts for safety finetuning"
)
for node in nodes:
    display_source_node(node, source_length=2000)
```

```python
query_engine_chunk = RetrieverQueryEngine.from_args(retriever_chunk, llm=llm)
```

```python
response = query_engine_chunk.query(
    "Can you tell me about the key concepts for safety finetuning"
)
print(str(response))
```

## Metaveri Referansları: Daha Büyük Bir Parçaya Atıfta Bulunan Özetler + Üretilen Sorular

Bu kullanım örneğinde, kaynak düğüme atıfta bulunan ek bağlamın (metadata) nasıl tanımlanacağını gösteriyoruz.

Bu ek bağlam, özetlerin yanı sıra üretilen soruları da içerir.

Sorgu zamanında, daha küçük parçaları getiriyoruz ancak daha büyük parçalara olan referansları takip ediyoruz. Bu, sentez için daha fazla bağlama sahip olmamızı sağlar.

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import IndexNode
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
)
```

```python
extractors = [
    SummaryExtractor(summaries=["self"], show_progress=True),
    QuestionsAnsweredExtractor(questions=5, show_progress=True),
]
```

```python
# temel düğümler üzerinde metaveri çıkarıcıyı çalıştır, sözlükleri geri al
metadata_dicts = []
for extractor in extractors:
    metadata_dicts.extend(extractor.extract(base_nodes))
```

```python
# metaveri sözlüklerini önbelleğe al
def save_metadata_dicts(path):
    with open(path, "w") as fp:
        for m in metadata_dicts:
            fp.write(json.dumps(m) + "\n")




def load_metadata_dicts(path):
    with open(path, "r") as fp:
        metadata_dicts = [json.loads(l) for l in fp.readlines()]
        return metadata_dicts
```

```python
save_metadata_dicts("data/llama2_metadata_dicts.jsonl")
```

```python
metadata_dicts = load_metadata_dicts("data/llama2_metadata_dicts.jsonl")
```

```python
# tüm düğümler, metaverilerle birlikte kaynak düğümlerden oluşur
import copy


all_nodes = copy.deepcopy(base_nodes)
for idx, d in enumerate(metadata_dicts):
    inode_q = IndexNode(
        text=d["questions_this_excerpt_can_answer"],
        index_id=base_nodes[idx].node_id,
    )
    inode_s = IndexNode(
        text=d["section_summary"], index_id=base_nodes[idx].node_id
    )
    all_nodes.extend([inode_q, inode_s])
```

```python
all_nodes_dict = {n.node_id: n for n in all_nodes}
```

```python
## İndeksi vektör indeksine yükle
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo")


vector_index_metadata = VectorStoreIndex(all_nodes)
```

```python
vector_retriever_metadata = vector_index_metadata.as_retriever(
    similarity_top_k=2
)
```

```python
retriever_metadata = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever_metadata},
    node_dict=all_nodes_dict,
    verbose=True,
)
```

```python
nodes = retriever_metadata.retrieve(
    "Can you tell me about the key concepts for safety finetuning"
)
for node in nodes:
    display_source_node(node, source_length=2000)
```

```python
query_engine_metadata = RetrieverQueryEngine.from_args(
    retriever_metadata, llm=llm
)
```

```python
response = query_engine_metadata.query(
    "Can you tell me about the key concepts for safety finetuning"
)
print(str(response))
```

## Değerlendirme (Evaluation)

Özyinelemeli erişim + düğüm referansı yöntemlerimizin ne kadar iyi çalıştığını [Braintrust](https://www.braintrustdata.com/) kullanarak değerlendiriyoruz. Braintrust, yapay zeka ürünleri oluşturmak için kurumsal düzeyde bir yığındır. Değerlendirmelerden istem alanına, veri yönetimine kadar, yapay zekayı işinize dahil etme konusundaki belirsizliği ve zahmeti ortadan kaldırıyoruz.

Hem parça referanslarını hem de metaveri referanslarını değerlendiriyoruz. Referans düğümlerini getirmek için gömme benzerliği aramasını kullanıyoruz. Her iki yöntemi de, ham düğümleri doğrudan getirdiğimiz temel bir erişiciyle karşılıyoruz. Metrikler açısından hem isabet oranını (hit-rate) hem de MRR'ı değerlendiriyoruz.

Aşağıdakiler için örnek değerlendirme panolarını burada görebilirsiniz:

- [Temel erişici (base retriever)](https://www.braintrustdata.com/app/braintrustdata.com/p/llamaindex-recurisve-retrievers/baseRetriever)
- [Özyinelemeli metaveri erişicisi (recursive metadata retreiver)](https://www.braintrustdata.com/app/braintrustdata.com/p/llamaindex-recurisve-retrievers/recursiveMetadataRetriever)
- [Özyinelemeli parça erişicisi (recursive chunk retriever)](https://www.braintrustdata.com/app/braintrustdata.com/p/llamaindex-recurisve-retrievers/recursiveChunkRetriever)

### Veri Kümesi Üretimi (Dataset Generation)

Önce metin parçaları kümesinden bir soru veri kümesi oluşturuyoruz.

```python
from llama_index.core.evaluation import (
    generate_question_context_pairs,
    EmbeddingQAFinetuneDataset,
)
import nest_asyncio


nest_asyncio.apply()
```

```python
eval_dataset = generate_question_context_pairs(base_nodes)
```

```python
eval_dataset.save_json("data/llama2_eval_dataset.json")
```

```python
# isteğe bağlı
eval_dataset = EmbeddingQAFinetuneDataset.from_json(
    "data/llama2_eval_dataset.json"
)
```

### Sonuçları Karşılaştır (Compare Results)

İsabet oranını ve MRR'ı ölçmek için erişicilerin her biri üzerinde değerlendirmeler yapıyoruz.

Düğüm referanslarına (parça veya metaveri) sahip erişicilerin, ham parçaları getirmekten daha iyi performans gösterme eğiliminde olduğunu görüyoruz.

```python
import pandas as pd


# vektör erişici similarity top k değerini daha yükseğe ayarla
top_k = 10




def display_results(names, results_arr):
    """Değerlendirmeden gelen sonuçları göster."""


    hit_rates = []
    mrrs = []
    for name, eval_results in zip(names, results_arr):
        metric_dicts = []
        for eval_result in eval_results:
            metric_dict = eval_result.metric_vals_dict
            metric_dicts.append(metric_dict)
        results_df = pd.DataFrame(metric_dicts)


        hit_rate = results_df["hit_rate"].mean()
        mrr = results_df["mrr"].mean()
        hit_rates.append(hit_rate)
        mrrs.append(mrr)


    final_df = pd.DataFrame(
        {"erişiciler": names, "isabet_oranı": hit_rates, "mrr": mrrs}
    )
    display(final_df)
```

Bazı puanlama fonksiyonları tanımlayalım ve veri kümesi veri değişkenimizi belirleyelim.

```python
queries = eval_dataset.queries
relevant_docs = eval_dataset.relevant_docs
data = [
    ({"input": queries[query], "expected": relevant_docs[query]})
    for query in queries.keys()
]




def hitRateScorer(input, expected, output=None):
    is_hit = any([id in expected for id in output])
    return 1 if is_hit else 0




def mrrScorer(input, expected, output=None):
    for i, id in enumerate(output):
        if id in expected:
            return 1 / (i + 1)
    return 0
```

```python
import braintrust


# Parça erişicisini değerlendir
vector_retriever_chunk = vector_index_chunk.as_retriever(similarity_top_k=10)
retriever_chunk = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever_chunk},
    node_dict=all_nodes_dict,
    verbose=False,
)




def runChunkRetriever(input, hooks):
    retrieved_nodes = retriever_chunk.retrieve(input)
    retrieved_ids = [node.node.node_id for node in retrieved_nodes]
    return retrieved_ids




chunkEval = await braintrust.Eval(
    name="llamaindex-recurisve-retrievers",
    data=data,
    task=runChunkRetriever,
    scores=[hitRateScorer, mrrScorer],
)
```

```python
# Metaveri erişicisini değerlendir


vector_retriever_metadata = vector_index_metadata.as_retriever(
    similarity_top_k=10
)
retriever_metadata = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever_metadata},
    node_dict=all_nodes_dict,
    verbose=False,
)




def runMetaDataRetriever(input, hooks):
    retrieved_nodes = retriever_metadata.retrieve(input)
    retrieved_ids = [node.node.node_id for node in retrieved_nodes]
    return retrieved_ids




metadataEval = await braintrust.Eval(
    name="llamaindex-recurisve-retrievers",
    data=data,
    task=runMetaDataRetriever,
    scores=[hitRateScorer, mrrScorer],
)
```

```python
# Temel erişiciyi değerlendir
base_retriever = base_index.as_retriever(similarity_top_k=10)




def runBaseRetriever(input, hooks):
    retrieved_nodes = base_retriever.retrieve(input)
    retrieved_ids = [node.node.node_id for node in retrieved_nodes]
    return retrieved_ids




baseEval = await braintrust.Eval(
    name="llamaindex-recurisve-retrievers",
    data=data,
    task=runBaseRetriever,
    scores=[hitRateScorer, mrrScorer],
)
```
