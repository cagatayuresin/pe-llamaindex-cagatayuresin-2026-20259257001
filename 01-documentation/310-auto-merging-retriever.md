# Otomatik Birleşen Erişimci (Auto Merging Retriever)

---
title: Auto Merging Retriever
 | LlamaIndex OSS Documentation
---

Bu not defterinde, bir dizi yaprak düğüme (leaf nodes) bakan ve belirli bir eşiği aşan bir üst düğüme (parent node) referans veren yaprak düğüm alt kümelerini özyinelemeli olarak "birleştiren" `AutoMergingRetriever` yapımızı tanıtıyoruz. Bu, potansiyel olarak kopuk ve daha küçük bağlamları, sentezlemeye yardımcı olabilecek daha büyük bir bağlamda birleştirmemize olanak tanır.

Bu hiyerarşiyi bir dizi belge üzerinde kendiniz tanımlayabilir veya yepyeni metin ayrıştırıcımızı kullanabilirsiniz: `HierarchicalNodeParser`, aday bir belge setini alır ve "kabadan inceye" doğru tüm bir düğüm hiyerarşisini çıktı olarak verir.

```python
%pip install llama-index-llms-openai
%pip install llama-index-readers-file pymupdf
```

```python
%load_ext autoreload
%autoreload 2
```

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
!pip install llama-index
```

## Veri Yükleme

Önce Llama 2 makalesini yükleyelim: <https://arxiv.org/pdf/2307.09288.pdf>. Bu bizim test verimiz olacak.

```python
!mkdir -p 'data/'
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
```

```python
from pathlib import Path


from llama_index.readers.file import PDFReader
from llama_index.readers.file import PyMuPDFReader
```

```python
loader = PyMuPDFReader()
# docs0 = loader.load_data(file=Path("./data/llama2.pdf"))
docs0 = loader.load(file_path=Path("./data/llama2.pdf"))
```

Varsayılan olarak, PDF okuyucu her sayfa için ayrı bir belge oluşturur. Bu not defteri için, belgeleri tek bir belgede birleştiriyoruz. Bu, daha sonra parçaları birbirine "diken" otomatik birleşme yeteneklerini daha iyi vurgulamamıza yardımcı olacaktır.

```python
from llama_index.core import Document


doc_text = "\n\n".join([d.get_content() for d in docs0])
docs = [Document(text=doc_text)]
```

## Metinden Parça Hiyerarşisini Ayrıştırma, Depolamaya Yükleme

Bu bölümde `HierarchicalNodeParser` kullanıyoruz. Bu, daha büyük parça boyutlarına sahip üst düzey düğümlerden, daha küçük parça boyutlarına sahip alt düğümlere kadar bir düğüm hiyerarşisi çıktı verecektir; burada her alt düğümün daha büyük parça boyutuna sahip bir üst düğümü vardır.

Varsayılan hiyerarşi şöyledir:

- 1. seviye: parça boyutu 2048
- 2. seviye: parça boyutu 512
- 3. seviye: parça boyutu 128

Daha sonra bu düğümleri depolamaya yüklüyoruz. Yaprak düğümler bir vektör deposu aracılığıyla indekslenir ve erişilir - bunlar önce benzerlik araması yoluyla doğrudan erişilecek düğümlerdir. Diğer düğümler bir belge deposundan (docstore) alınacaktır.

```python
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    SentenceSplitter,
)
```

```python
node_parser = HierarchicalNodeParser.from_defaults()
```

```python
nodes = node_parser.get_nodes_from_documents(docs)
```

```python
len(nodes)
```

```text
1029
```

Burada, bir düğüm listesi içindeki "yaprak" (leaf) düğümleri getirmek için basit bir yardımcı işlev içe aktarıyoruz. Bunlar kendi alt düğümleri olmayan düğümlerdir.

```python
from llama_index.core.node_parser import get_leaf_nodes, get_root_nodes
```

```python
leaf_nodes = get_leaf_nodes(nodes)
```

```python
len(leaf_nodes)
```

```text
795
```

```python
root_nodes = get_root_nodes(nodes)
```

### Depolamaya Yükleme

Tüm düğümleri yüklediğimiz bir belge deposu (docstore) tanımlıyoruz.

Ardından sadece yaprak düzeyindeki düğümleri içeren bir `VectorStoreIndex` tanımlıyoruz.

```python
# depolama bağlamını tanımla
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI


docstore = SimpleDocumentStore()


# düğümleri belge deposuna ekle
docstore.add_documents(nodes)


# depolama bağlamını tanımla (varsayılan olarak vektör deposunu da içerecektir)
storage_context = StorageContext.from_defaults(docstore=docstore)


llm = OpenAI(model="gpt-3.5-turbo")
```

```python
## Dizini vektör dizinine yükle
from llama_index.core import VectorStoreIndex


base_index = VectorStoreIndex(
    leaf_nodes,
    storage_context=storage_context,
)
```

## Erişimciyi (Retriever) Tanımlama

```python
from llama_index.core.retrievers import AutoMergingRetriever
```

```python
base_retriever = base_index.as_retriever(similarity_top_k=6)
retriever = AutoMergingRetriever(base_retriever, storage_context, verbose=True)
```

```python
# query_str = "Red-teaming'den öğrenilen bazı dersler nelerdir?"
# query_str = "Güvenlik ince ayarı için temel kavramlar hakkında bilgi verebilir misiniz?"
query_str = (
    "RLHF aşamasında kullanılan güvenlik verisi miktarını ayarlamanın"
    " potansiyel sonuçları neler olabilir?"
)


nodes = retriever.retrieve(query_str)
base_nodes = base_retriever.retrieve(query_str)
```

```text
> Merging 4 nodes into parent node.
> Parent node id: caf5f81c-842f-46a4-b679-6be584bd6aff.
> Parent node text: We conduct RLHF by first collecting human preference data for safety similar to Section 3.2.2: an...
```

```python
len(nodes)
```

```text
3
```

```python
len(base_nodes)
```

```text
6
```

```python
from llama_index.core.response.notebook_utils import display_source_node


for node in nodes:
    display_source_node(node, source_length=10000)
```

**Düğüm ID:** d4d67180-71c8-4328-b3f1-1e98fa42ab69\
**Benzerlik:** 0.8694979150607424\
**Metin:** Ayrıca Tablo 35'te güvenlik ve yardımseverlik ödül modellerinin birbiriyle uyuşmadığı iki nitel örneği listeliyoruz. A.4.2 Güvenlik Verisi Ölçeklendirmesi Üzerine Nitel Sonuçlar Bölüm 4.2.3'te, model RLHF'sine daha fazla güvenlik verisi eklemenin etkisini nicel bir şekilde inceliyoruz. Burada, güvenlik verilerini ölçeklendirdiğimizde model davranışının evrimini nitel olarak incelemek için Tablo 36, 37 ve 38'de birkaç örnek gösteriyoruz. Genel olarak, daha fazla güvenlik verisi kullanıldığında Llama 2-Chat'in güvensiz istemlere yanıt verirken daha güvenli hale geldiğini gözlemliyoruz.

**Düğüm ID:** caf5f81c-842f-46a4-b679-6be584bd6aff\
**Benzerlik:** 0.86168727941324\
**Metin:** RLHF'yi ilk olarak Bölüm 3.2.2'ye benzer şekilde güvenlik için insan tercihi verileri toplayarak yürütüyoruz: anketörler güvensiz davranışlara yol açabileceğine inandıkları bir istem yazıyor ve ardından istemlere verilen çoklu model yanıtlarını karşılaştırarak bir dizi yönergeye göre en güvenli olan yanıtı seçiyor. Daha sonra insan tercihi verilerini bir güvenlik ödül modeli eğitmek için kullanıyoruz (bkz. Bölüm 3.2.2) ve ayrıca RLHF aşamasında modelden örnekleme yapmak için rakip istemleri yeniden kullanıyoruz. Yardımseverliğe Zarar Vermeden Daha İyi Uzun Kuyruk Güvenlik Sağlamlığı Güvenlik, zorluğun az sayıda çok spesifik vakadan kaynaklandığı doğası gereği uzun kuyruklu bir sorundur. RLHF aşamasında rakip istemleri olan ve olmayan iki orta seviye Llama 2-Chat kontrol noktası alarak ve test setlerimizdeki yanıtlarını güvenlik ve yardımseverlik ödül modellerimizi kullanarak puanlayarak Güvenlik RLHF'sinin etkisini inceliyoruz. Şekil 14'te, güvenlik test setindeki güvenlik RM puan dağılım kaymasını (solda) ve yardımseverlik test setindeki yardımseverlik RM puan dağılım kaymasını (sağda) çiziyoruz. Şekil 14'ün sol tarafında, güvenlik RM puanlarının dağılımının RLHF ile güvenlik ayarından sonra daha yüksek ödül puanlarına kaydığını ve dağılımın sıfıra yakın uzun kuyruğunun inceldiğini gözlemliyoruz. Sol üst köşede, model güvenliğindeki iyileşmeleri gösteren net bir kümelenme görülmektedir. Sağ tarafta, Şekil 14'ün sağ tarafındaki y = x çizgisinin altında herhangi bir toplanma modeli gözlemlemiyoruz; bu da yardımseverlik puan dağılımının RLHF ile güvenlik ayarından sonra korunduğunu gösterir. Başka bir deyişle, yeterli yardımseverlik eğitim verisi verildiğinde, ek bir güvenlik azaltma aşamasının eklenmesi, modelin yardımseverlik performansını kayda değer bir düşüşe neden olacak şekilde olumsuz etkilemez. Nitel bir örnek Tablo 12'de gösterilmiştir. Güvenlik Verisi Ölçeklendirmenin Etkisi. LLM'lerin yardımseverliği ve güvenliği arasındaki gerilim önceki çalışmalarda (Bai ve ark., 2022a) gözlemlenmiştir. Güvenlik eğitim verisi eklenmesinin genel model performansını, özellikle de yardımseverliği nasıl etkilediğini daha iyi anlamak için, RLHF aşamasında kullanılan güvenlik verisi miktarını ayarlayarak güvenlik verisi ölçeklendirme eğilimlerini araştırıyoruz.

**Düğüm ID:** d9893bef-a5a7-4248-a0a1-d7c28800ae59\
**Benzerlik:** 0.8546977459150967\
**Metin:** 0 0.2 0.4 0.6 0.8 1.0 Güvenlik RLHF öncesi Yardımseverlik RM Puanı 0.0 0.2 0.4 0.6 0.8 1.0 Güvenlik RLHF sonrası Yardımseverlik RM Puanı 0 1000 0 1000 Şekil 14: Ödül modeli puan dağılımlarıyla ölçülen güvenlik RLHF'sinin etkisi. Sol: Meta Güvenlik test setindeki nesillerin güvenlik ödül modeli puanları. Sol üst köşedeki örneklerin kümelenmesi, model güvenliğindeki iyileşmeleri göstermektedir.

```python
for node in base_nodes:
    display_source_node(node, source_length=10000)
```

**Düğüm ID:** 16328561-9ff7-4307-8d31-adf6bb74b71b\
**Benzerlik:** 0.8770715326726375\
**Metin:** Nitel bir örnek Tablo 12'de gösterilmiştir. Güvenlik Verisi Ölçeklendirmenin Etkisi. LLM'lerin yardımseverliği ve güvenliği arasındaki gerilim önceki çalışmalarda (Bai ve ark., 2022a) gözlemlenmiştir. Güvenlik eğitim verisi eklenmesinin genel model performansını, özellikle de yardımseverliği nasıl etkilediğini daha iyi anlamak için, RLHF aşamasında kullanılan güvenlik verisi miktarını ayarlayarak güvenlik verisi ölçeklendirme eğilimlerini araştırıyoruz.

**Düğüm ID:** e756d327-1a28-4228-ac38-f8a831b1bf77\
**Benzerlik:** 0.8728111844788112\
**Metin:** Sol üst köşede, model güvenliğindeki iyileşmeleri gösteren net bir kümelenme görülmektedir. Sağ tarafta, Şekil 14'ün sağ tarafındaki y = x çizgisinin altında herhangi bir toplanma modeli gözlemlemiyoruz; bu da yardımseverlik puan dağılımının RLHF ile güvenlik ayarından sonra korunduğunu gösterir. Başka bir deyişle, yeterli yardımseverlik eğitim verisi verildiğinde, ek bir güvenlik azaltma aşamasının eklenmesi, modelin yardımseverlik performansını kayda değer bir düşüşe neden olacak şekilde olumsuz etkilemez. Nitel bir örnek Tablo 12'de gösterilmiştir. Güvenlik Verisi Ölçeklendirmenin Etkisi.

**Düğüm ID:** d4d67180-71c8-4328-b3f1-1e98fa42ab69\
**Benzerlik:** 0.8697379697028405\
**Metin:** Ayrıca Tablo 35'te güvenlik ve yardımseverlik ödül modellerinin birbiriyle uyuşmadığı iki nitel örneği listeliyoruz. A.4.2 Güvenlik Verisi Ölçeklendirmesi Üzerine Nitel Sonuçlar Bölüm 4.2.3'te, model RLHF'sine daha fazla güvenlik verisi eklemenin etkisini nicel bir şekilde inceliyoruz. Burada, güvenlik verilerini ölçeklendirdiğimizde model davranışının evrimini nitel olarak incelemek için Tablo 36, 37 ve 38'de birkaç örnek gösteriyoruz. Genel olarak, daha fazla güvenlik verisi kullanıldığında Llama 2-Chat'in güvensiz istemlere yanıt verirken daha güvenli hale geldiğini gözlemliyoruz.

**Düğüm ID:** d9893bef-a5a7-4248-a0a1-d7c28800ae59\
**Benzerlik:** 0.855087365309258\
**Metin:** 0 0.2 0.4 0.6 0.8 1.0 Güvenlik RLHF öncesi Yardımseverlik RM Puanı 0.0 0.2 0.4 0.6 0.8 1.0 Güvenlik RLHF sonrası Yardımseverlik RM Puanı 0 1000 0 1000 Şekil 14: Ödül modeli puan dağılımlarıyla ölçülen güvenlik RLHF'sinin etkisi. Sol: Meta Güvenlik test setindeki nesillerin güvenlik ödül modeli puanları. Sol üst köşedeki örneklerin kümelenmesi, model güvenliğindeki iyileşmeleri göstermektedir.

**Düğüm ID:** d62ee107-9841-44b5-8b70-bc6487ad6315\
**Benzerlik:** 0.8492541852986794\
**Metin:** Yardımseverliğe Zarar Vermeden Daha İyi Uzun Kuyruk Güvenlik Sağlamlığı Güvenlik, zorluğun az sayıda çok spesifik vakadan kaynaklandığı doğası gereği uzun kuyruklu bir sorundur. RLHF aşamasında rakip istemleri olan ve olmayan iki orta seviye Llama 2-Chat kontrol noktası alarak ve test setlerimizdeki yanıtlarını güvenlik ve yardımseverlik ödül modellerimizi kullanarak puanlayarak Güvenlik RLHF'sinin etkisini inceliyoruz.

**Düğüm ID:** 312a63b3-5e28-4fbf-a3e1-4e8dc0c026ea\
**Benzerlik:** 0.8488371951811564\
**Metin:** RLHF'yi ilk olarak Bölüm 3.2.2'ye benzer şekilde güvenlik için insan tercihi verileri toplayarak yürütüyoruz: anketörler güvensiz davranışlara yol açabileceğine inandıkları bir istem yazıyor ve ardından istemlere verilen çoklu model yanıtlarını karşılaştırarak bir dizi yönergeye göre en güvenli olan yanıtı seçiyor. Daha sonra insan tercihi verilerini bir güvenlik ödül modeli eğitmek için kullanıyoruz (bkz. Bölüm 3.2.2) ve ayrıca RLHF aşamasında modelden örnekleme yapmak için rakip istemleri yeniden kullanıyoruz.

## Sorgu Motoruna Bağlama

```python
from llama_index.core.query_engine import RetrieverQueryEngine
```

```python
query_engine = RetrieverQueryEngine.from_args(retriever)
base_query_engine = RetrieverQueryEngine.from_args(base_retriever)
```

```python
response = query_engine.query(query_str)
```

```text
> Merging 4 nodes into parent node.
> Parent node id: 3671b20d-ea5e-4afc-983e-02be6ee8302d.
> Parent node text: We conduct RLHF by first collecting human preference data for safety similar to Section 3.2.2: an...
```

```python
print(str(response))
```

```text
RLHF aşamasında kullanılan güvenlik verisi miktarını ayarlamanın potansiyel olarak şu sonuçları olabilir:
1. İyileştirilmiş model güvenliği: RLHF'de kullanılan güvenlik verisi miktarının artırılması, model güvenliğinde iyileşmelere yol açabilir. Bu, modelin güvensiz istemlere yanıt vermede daha iyi hale geldiği ve güvensiz veya zararlı çıktılar üretmekten kaçındığı anlamına gelir.
2. Güvenlik RM puanlarının uzun kuyruğunun incelmesi: Güvenlik verisi miktarının artırılması, güvenlik ödül modeli (RM) puanlarının dağılımının daha yüksek ödül puanlarına doğru kaymasına neden olabilir. Bu, modelin güvenli yanıtlar üretmede daha tutarlı hale geldiği ve düşük güvenlik puanlarının oluşumunu azalttığı anlamına gelir.
3. Yardımseverlik performansının korunması: RLHF'de kullanılan güvenlik verisi miktarını ayarlamanın modelin yardımseverlik performansı üzerinde olumsuz bir etki yaratması beklenmemektedir. Bu, ek güvenlik azaltma önlemleri eklendikten sonra bile modelin yardımsever yanıtlar üretme yeteneğinin korunduğu anlamına gelir.
4. Yardımseverlik RM puanlarında toplanma modeli: RLHF ile güvenlik ayarından sonra yardımseverlik RM puanlarının dağılımında y = x çizgisinin altında gözlemlenen bir toplanma modeli yoktur. Bu, yardımseverlik puan dağılımının korunduğunu ve modelin yardımseverlik performansının güvenlik azaltma önlemlerinin eklenmesiyle önemli ölçüde azalmadığını gösterir.
Genel olarak, RLHF aşamasında kullanılan güvenlik verisi miktarını ayarlamak, yardımseverlik performansından ödün vermeden model güvenliğini artırmak arasında bir denge kurmayı amaçlar.
```

```python
base_response = base_query_engine.query(query_str)
```

```python
print(str(base_response))
```

```text
RLHF aşamasında kullanılan güvenlik verisi miktarını ayarlamak, potansiyel olarak model güvenliğinde iyileşmelere yol açabilir. Bu, sol üst köşede görünen ve gelişmiş model güvenliğini gösteren net bir kümelenme ile gözlemlenebilir. Ek olarak, yardımseverlik puan dağılımının RLHF ile güvenlik ayarından sonra korunduğu belirtilmektedir; bu da güvenlik verisi eklenmesinin modelin yardımseverlik performansı üzerinde olumsuz bir etkisi olmadığını gösterir.
```

## Değerlendirme

Hiyerarşik erişimcinin (hierarchical retriever) temel erişimciye (baseline retriever) kıyasla ne kadar iyi çalıştığını daha nicel bir şekilde değerlendiriyoruz.

**UYARI**: Bu işlem, özellikle GPT-4 ile *pahalı* olabilir. Dikkatli olun ve örneklem boyutunu bütçenize göre ayarlayın.

```python
from llama_index.core.evaluation import DatasetGenerator, QueryResponseDataset
from llama_index.llms.openai import OpenAI
import nest_asyncio


nest_asyncio.apply()
```

```python
# NOT: veri seti henüz kaydedilmemişse bunu çalıştırın
# Not: Sadece ilk 20 düğümden üretim yapıyoruz, çünkü geri kalanı referanslardır
eval_llm = OpenAI(model="gpt-4")
dataset_generator = DatasetGenerator(
    root_nodes[:20],
    llm=eval_llm,
    show_progress=True,
    num_questions_per_chunk=3,
)
```

```python
eval_dataset = await dataset_generator.agenerate_dataset_from_nodes(num=60)
```

```python
eval_dataset.save_json("data/llama2_eval_qr_dataset.json")
```

```python
# isteğe bağlı
eval_dataset = QueryResponseDataset.from_json(
    "data/llama2_eval_qr_dataset.json"
)
```

### Sonuçları Karşılaştırın

Erişimcilerin her biri üzerinde değerlendirmeler yapıyoruz: doğruluk (correctness), anlamsal benzerlik (semantic similarity), alaka düzeyi (relevancy) ve sadakat (faithfulness).

```python
import asyncio
import nest_asyncio


nest_asyncio.apply()
```

```python
from llama_index.core.evaluation import (
    CorrectnessEvaluator,
    SemanticSimilarityEvaluator,
    RelevancyEvaluator,
    FaithfulnessEvaluator,
    PairwiseComparisonEvaluator,
)




from collections import defaultdict
import pandas as pd


# NOT: diğer değerlendiricilerin yorum satırları kaldırılabilir
evaluator_c = CorrectnessEvaluator(llm=eval_llm)
evaluator_s = SemanticSimilarityEvaluator(llm=eval_llm)
evaluator_r = RelevancyEvaluator(llm=eval_llm)
evaluator_f = FaithfulnessEvaluator(llm=eval_llm)
# pairwise_evaluator = PairwiseComparisonEvaluator(llm=eval_llm)
```

```python
from llama_index.core.evaluation.eval_utils import (
    get_responses,
    get_results_df,
)
from llama_index.core.evaluation import BatchEvalRunner
```

```python
eval_qs = eval_dataset.questions
qr_pairs = eval_dataset.qr_pairs
ref_response_strs = [r for (_, r) in qr_pairs]
```

```python
pred_responses = get_responses(eval_qs, query_engine, show_progress=True)
```

```python
base_pred_responses = get_responses(
    eval_qs, base_query_engine, show_progress=True
)
```

```text
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60/60 [00:07<00:00,  8.17it/s]
```

```python
import numpy as np


pred_response_strs = [str(p) for p in pred_responses]
base_pred_response_strs = [str(p) for p in base_pred_responses]
```

```python
evaluator_dict = {
    "doğruluk": evaluator_c,
    "sadakat": evaluator_f,
    "alaka_düzeyi": evaluator_r,
    "anlamsal_benzerlik": evaluator_s,
}
batch_runner = BatchEvalRunner(evaluator_dict, workers=2, show_progress=True)
```

```python
eval_results = await batch_runner.aevaluate_responses(
    eval_qs, responses=pred_responses, reference=ref_response_strs
)
```

```python
base_eval_results = await batch_runner.aevaluate_responses(
    eval_qs, responses=base_pred_responses, reference=ref_response_strs
)
```

```python
results_df = get_results_df(
    [eval_results, base_eval_results],
    ["Auto Merging Retriever", "Base Retriever"],
    ["doğruluk", "alaka_düzeyi", "sadakat", "anlamsal_benzerlik"],
)
display(results_df)
```

```css
.dataframe tbody tr th {
    vertical-align: top;
}


.dataframe thead th {
    text-align: right;
}
```

|   | Adlar                  | doğruluk | alaka\_düzeyi | sadakat | anlamsal\_benzerlik |
| - | ---------------------- | ----------- | --------- | ------------ | -------------------- |
| 0 | Auto Merging Retriever | 4.266667    | 0.916667  | 0.95         | 0.962196             |
| 1 | Base Retriever         | 4.208333    | 0.916667  | 0.95         | 0.960602             |

**Analiz**: Sonuçlar kabaca aynıdır.

Ayrıca çiftli değerlendirmelerimizle (pairwise evals) GPT-4'ün hangi yanıtı tercih ettiğini görmeye çalışalım.

```python
batch_runner = BatchEvalRunner(
    {"pairwise": pairwise_evaluator}, workers=10, show_progress=True
)
```

```python
pairwise_eval_results = await batch_runner.aevaluate_response_strs(
    eval_qs,
    response_strs=pred_response_strs,
    reference=base_pred_response_strs,
)
pairwise_score = np.array(
    [r.score for r in pairwise_eval_results["pairwise"]]
).mean()
```

```python
pairwise_score
```

```text
0.525
```

**Analiz**: Çiftli karşılaştırma puanı, aday yanıtın (otomatik birleşen erişimci kullanılarak) temel yanıta (temel erişimci kullanılarak) tercih edilme yüzdesinin bir ölçüsüdür. Burada durumun kabaca eşit olduğunu görüyoruz.
