# Özyinelemeli Erişici + Düğüm Referansları (Recursive Retriever + Node References)

---
title: Özyinelemeli Erişici + Düğüm Referansları (Recursive Retriever + Node References)
 | LlamaIndex OSS Belgeleri
---

Bu kılavuz, düğüm ilişkilerini gezinmek ve "referanslara" dayalı düğümleri getirmek için özyinelemeli erişimin (recursive retrieval) nasıl kullanılacağını gösterir.

Düğüm referansları güçlü bir kavramdır. İlk erişimi gerçekleştirdiğinizde, ham metin yerine referansı getirmek isteyebilirsiniz. Aynı düğüme işaret eden birden fazla referansınız olabilir.

Bu kılavuzda düğüm referanslarının bazı farklı kullanımlarını keşfediyoruz:

- **Parça referansları (Chunk references)**: Daha büyük bir parçaya atıfta bulunan farklı parça boyutları.
- **Metaveri referansları (Metadata references)**: Daha büyük bir parçaya atıfta bulunan Özetler + Üretilen Sorular.

```bash
%pip install llama-index-llms-openai
%pip install llama-index-readers-file
```

```python
%load_ext autoreload
%autoreload 2
%env OPENAI_API_KEY=YOUR_OPENAI_KEY
```

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i kurmanız gerekecektir 🦙.

```bash
!pip install llama-index pypdf
```

## Veriyi Yükleme + Kurulum (Load Data + Setup)

Bu bölümde Llama 2 makalesini indiriyoruz ve bir dizi başlangıç düğümü oluşturuyoruz (parça boyutu 1024).

```bash
!mkdir -p 'data/'
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
```

```text
Will not apply HSTS. The HSTS database must be a regular and non-world-writable file.
ERROR: could not open HSTS store at '/home/loganm/.wget-hsts'. HSTS will be disabled.
--2024-01-01 11:13:01--  https://arxiv.org/pdf/2307.09288.pdf
Resolving arxiv.org (arxiv.org)... 151.101.3.42, 151.101.131.42, 151.101.67.42, ...
Connecting to arxiv.org (arxiv.org)|151.101.3.42|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 13661300 (13M) [application/pdf]
Saving to: ‘data/llama2.pdf’


data/llama2.pdf     100%[===================>]  13.03M  27.3MB/s    in 0.5s


2024-01-01 11:13:02 (27.3 MB/s) - ‘data/llama2.pdf’ saved [13661300/13661300]
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
    "Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?"
)
```

```python
for n in retrievals:
    display_source_node(n, source_length=1500)
```

**Düğüm Kimliği (Node ID):** node-26\
**Benzerlik:** 0.8581930837671874\
**Metin:** AsLLMsareintegratedanddeployed,welookforwardto continuing research that will amplify their potential for positive impact on these important social issues. 4.2 Safety Fine-Tuning In this section, we describe our approach to safety fine-tuning, including safety categories, annotation guidelines,andthetechniquesweusetomitigatesafetyrisks. Weemployaprocesssimilartothegeneral fine-tuning methods as described in Section 3, with some notable differences related to safety concerns. Specifically, we use the following techniques in safety fine-tuning: 1.Supervised Safety Fine-Tuning : We initialize by gathering adversarial prompts and safe demonstra- tions that are then included in the general supervised fine-tuning process (Section 3.1). This teaches themodeltoalignwithoursafetyguidelinesevenbeforeRLHF,andthuslaysthefoundationfor high-quality human preference data annotation. 2.Safety RLHF : Subsequently, we integrate safety in the general RLHF pipeline described in Sec- tion 3.2.2. This includes training a safety-specific reward model and gathering more challenging adversarial prompts for rejection sampling style fine-tuning and PPO optimization. 3.SafetyContextDistillation : Finally,werefineourRLHFpipelinewithcontextdistillation(Askell etal.,2021b). Thisinvolvesgeneratingsafermodelresponsesbyprefixingapromptwithasafety preprompt, e.g., “You are a safe and responsible assistant,” and then fine-tuning the model on the safer responses without the preprompt, which essentially distill…

**Düğüm Kimliği (Node ID):** node-33\
**Benzerlik:** 0.8442806881920294\
**Metin:** Examples of evaluation prompts and responses can be found in Appendix A.4.6. We then asked raters to judge models for safety violations on a five-point Likert scale with the following definitions: •5- No safety violations and very helpful •4- No safety violations and only minor non-safety issues •3- No safety violations but not helpful or other major non-safety issues •2- Mild or moderate safety violations 29

(a)Overall violation percentage. (b)Overall safety and helpfulness mean rating. Figure17: Overallsafetymeasures. Left: Llama 2-Chat haslowviolationpercentageoverallacrossmodel sizes.Right: Llama 2-Chat has high safety and helpfulness mean rating overall across model sizes. It is important to note that these results are subject to limitations of the prompt set, subjectivity of the review guidelines, and subjectivity of individual raters. •1- Severe safety violations We consider a rating of 1 or 2 as violation and use violation percentage as our main evaluation metric, with themeanratingasasupplement. Eachexampleisannotatedbythreeannotatorsandwetakethemajority votetodetermineiftheresponseisviolatingornot. WeusedGwet’sAC1/2statistictomeasureinter-rater reliability(IRR)asinthehelpfulnesshumanevaluation. TheIRRscoresrangefrom 0.70to0.95depending on the annotation batch, indicating a high degree of agreement among annotators on safety assessments. OnLlama 2-Chat annotations, the average IRR is 0.92according to Gwet’s AC2 measure. We see lower IRR scoresonbatcheswherethemo…

```python
query_engine_base = RetrieverQueryEngine.from_args(base_retriever, llm=llm)
```

```python
response = query_engine_base.query(
    "Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?"
)
print(str(response))
```

```text
Güvenlik ince ayarı (safety fine-tuning) için temel kavramlar arasında denetimli güvenlik ince ayarı (supervised safety fine-tuning), güvenlik RLHF (İnsan Geri Bildiriminden Takviyeli Öğrenme - Reinforcement Learning from Human Feedback) ve güvenlik bağlam damıtması (safety context distillation) yer alır. Denetimli güvenlik ince ayarında, düşmanca istemler (adversarial prompts) ve güvenli gösterimler toplanır ve genel denetimli ince ayar sürecine dahil edilir. Bu, modelin güvenlik yönergeleriyle uyumlu hale gelmesine yardımcı olur ve yüksek kaliteli insan tercihi veri açıklaması için temel oluşturur. Güvenlik RLHF, güvenliği genel RLHF hattına entegre etmeyi içerir; bu da güvenliğe özgü bir ödül modelinin eğitilmesini ve reddetme örnekleme tarzı ince ayar ve PPO (Proximal Policy Optimization) optimizasyonu için daha zorlu düşmanca istemlerin toplanmasını kapsar. Güvenlik bağlam damıtması, RLHF hattının bağlam damıtması ile rafine edildiği son adımdır. Bu, bir istemin önüne bir güvenlik ön istemi (safety preprompt) ekleyerek daha güvenli model yanıtları üretmeyi ve ardından modeli bu ön istem olmadan daha güvenli yanıtlar üzerinde ince ayarlamayı içerir.
```

## Parça Referansları: Daha Büyük Ana Parçaya Atıfta Bulunan Küçük Alt Parçalar

Bu kullanım örneğinde, daha büyük ana parçaları işaret eden daha küçük parçalardan oluşan bir grafiğin nasıl oluşturulacağını gösteriyoruz.

Sorgu zamanında, daha küçük parçaları getiriyoruz ancak daha büyük parçalara olan referansları takip ediyoruz. Bu, sentez için daha fazla bağlama sahip olmamızı sağlar.

```python
sub_chunk_sizes = [128, 256, 512]
sub_node_parsers = [
    SentenceSplitter(chunk_size=c, chunk_overlap=20) for c in sub_chunk_sizes
]


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
    "Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?"
)
for node in nodes:
    display_source_node(node, source_length=2000)
```

```text
 [1;3;34mRetrieving with query id None: Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?
 [0m [1;3;38;5;200mRetrieved node with id, entering: node-26
 [0m [1;3;34mRetrieving with query id node-26: Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?
 [0m [1;3;38;5;200mRetrieved node with id, entering: node-1
 [0m [1;3;34mRetrieving with query id node-1: Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?
 [0m
```

**Düğüm Kimliği (Node ID):** node-26\
**Benzerlik:** 0.8809071991986446\
**Metin:** AsLLMsareintegratedanddeployed,welookforwardto continuing research that will amplify their potential for positive impact on these important social issues. 4.2 Safety Fine-Tuning In this section, we describe our approach to safety fine-tuning, including safety categories, annotation guidelines,andthetechniquesweusetomitigatesafetyrisks. Weemployaprocesssimilartothegeneral fine-tuning methods as described in Section 3, with some notable differences related to safety concerns. Specifically, we use the following techniques in safety fine-tuning: 1.Supervised Safety Fine-Tuning : We initialize by gathering adversarial prompts and safe demonstra- tions that are then included in the general supervised fine-tuning process (Section 3.1). This teaches themodeltoalignwithoursafetyguidelinesevenbeforeRLHF,andthuslaysthefoundationfor high-quality human preference data annotation. 2.Safety RLHF : Subsequently, we integrate safety in the general RLHF pipeline described in Sec- tion 3.2.2. This includes training a safety-specific reward model and gathering more challenging adversarial prompts for rejection sampling style fine-tuning and PPO optimization. 3.SafetyContextDistillation : Finally,werefineourRLHFpipelinewithcontextdistillation(Askell etal.,2021b). Thisinvolvesgeneratingsafermodelresponsesbyprefixingapromptwithasafety preprompt, e.g., “You are a safe and responsible assistant,” and then fine-tuning the model on the safer responses without the preprompt, which essentially distillsthe safety preprompt (context) into the model. Weuseatargetedapproachthatallowsoursafetyrewardmodeltochoosewhethertouse context distillation for each sample. 4.2.1 Safety Categories and Annotation Guidelines Based on limitations of LLMs known from prior work, we design instructions for our annotation team to createadversarialpromptsalongtwodimensions: a riskcategory ,orpotentialtopicaboutwhichtheLLM couldproduceunsafecontent;andan attackvector ,orquestionstyletocoverdifferentvarietiesofprompts …

**Düğüm Kimliği (Node ID):** node-1\
**Benzerlik:** 0.8744334039911964\
**Metin:** … … … … … … … … … … … … 9 3.2 Reinforcement Learning with Human Feedback (RLHF) … … … … … … … 9 3.3 System Message for Multi-Turn Consistency … … … … … … … … … . . 16 3.4 RLHF Results … … … … … … … … … … … … … … … . 17 4 Safety 20 4.1 Safety in Pretraining … … … … … … … … … … … … … … 20 4.2 Safety Fine-Tuning … … … … … … … … … … … … … … . 23 4.3 Red Teaming … … … … … … … … … … … … … … … . . 28 4.4 Safety Evaluation of Llama 2-Chat … … … … … … … … … … … . 29 5 Discussion 32 5.1 Learnings and Observations … … … … … … … … … … … … . . 32 5.2 Limitations and Ethical Considerations … … … … … … … … … … . 34 5.3 Responsible Release Strategy … … … … … … … … … … … … . 35 6 Related Work 35 7 Conclusion 36 A Appendix 46 A.1 Contributions … … … … … … … … … … … … …

```python
query_engine_chunk = RetrieverQueryEngine.from_args(retriever_chunk, llm=llm)
```

```python
response = query_engine_chunk.query(
    "Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?"
)
print(str(response))
```

```text
 [1;3;34mRetrieving with query id None: Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?
 [0m [1;3;38;5;200mRetrieved node with id, entering: node-26
 [0m [1;3;34mRetrieving with query id node-26: Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?
 [0m [1;3;38;5;200mRetrieved node with id, entering: node-1
 [0m [1;3;34mRetrieving with query id node-1: Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?
 [0mGüvenlik ince ayarı (safety fine-tuning) için temel kavramlar arasında denetimli güvenlik ince ayarı, güvenlik RLHF (İnsan Geri Bildiriminden Takviyeli Öğrenme) ve güvenlik bağlam damıtması yer alır. Denetimli güvenlik ince ayarı, modelin güvenlik yönergeleriyle uyumlu hale gelmesini öğretmek için düşmanca istemlerin ve güvenli gösterimlerin toplanmasını içerir. Güvenlik RLHF, güvenliğe özgü bir ödül modeli eğiterek ve reddetme örnekleme tarzı ince ayar ile PPO optimizasyonu için zorlu düşmanca istemler toplanarak güvenliği genel RLHF hattına entegre eder. Güvenlik bağlam damıtması, bir istemin önüne bir güvenlik ön istemi ekleyerek daha güvenli model yanıtları üretmeyi ve modeli ön istem olmadan daha güvenli yanıtlar üzerinde ince ayarlamayı içerir. Bu teknikler, güvenlik risklerini azaltmayı ve modelin güvenli ve sorumlu yanıtlar verme yeteneğini geliştirmeyi amaçlar.
```

## Metaveri Referansları: Daha Büyük Bir Parçaya Atıfta Bulunan Özetler + Üretilen Sorular

Bu kullanım örneğinde, kaynak düğüme atıfta bulunan ek bağlamın (metaveri) nasıl tanımlanacağını gösteriyoruz.

Bu ek bağlam, özetlerin yanı sıra üretilen soruları da içerir.

Sorgu zamanında, daha küçük parçalar getiriyoruz ancak daha büyük parçalara olan referansları takip ediyoruz. Bu, sentez için daha fazla bağlama sahip olmamızı sağlar.

```python
import nest_asyncio


nest_asyncio.apply()
```

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
node_to_metadata = {}
for extractor in extractors:
    metadata_dicts = extractor.extract(base_nodes)
    for node, metadata in zip(base_nodes, metadata_dicts):
        if node.node_id not in node_to_metadata:
            node_to_metadata[node.node_id] = metadata
        else:
            node_to_metadata[node.node_id].update(metadata)
```

```text
100%|██████████| 93/93 [01:13<00:00,  1.27it/s]
100%|██████████| 93/93 [00:49<00:00,  1.88it/s]
```

```python
# metaveri sözlüklerini önbelleğe al
def save_metadata_dicts(path, data):
    with open(path, "w") as fp:
        json.dump(data, fp)




def load_metadata_dicts(path):
    with open(path, "r") as fp:
        data = json.load(fp)
    return data
```

```python
save_metadata_dicts("data/llama2_metadata_dicts.json", node_to_metadata)
```

```python
metadata_dicts = load_metadata_dicts("data/llama2_metadata_dicts.json")
```

```python
# tüm düğümler, metaverilerle birlikte kaynak düğümlerden oluşur
import copy


all_nodes = copy.deepcopy(base_nodes)
for node_id, metadata in node_to_metadata.items():
    for val in metadata.values():
        all_nodes.append(IndexNode(text=val, index_id=node_id))
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
    verbose=False,
)
```

```python
nodes = retriever_metadata.retrieve(
    "Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?"
)
for node in nodes:
    display_source_node(node, source_length=2000)
```

**Düğüm Kimliği (Node ID):** node-26\
**Benzerlik:** 0.8727061238826861\
**Metin:** AsLLMsareintegratedanddeployed,welookforwardto continuing research that will amplify their potential for positive impact on these important social issues. 4.2 Safety Fine-Tuning In this section, we describe our approach to safety fine-tuning, including safety categories, annotation guidelines,andthetechniquesweusetomitigatesafetyrisks. Weemployaprocesssimilartothegeneral fine-tuning methods as described in Section 3, with some notable differences related to safety concerns. Specifically, we use the following techniques in safety fine-tuning: 1.Supervised Safety Fine-Tuning : We initialize by gathering adversarial prompts and safe demonstra- tions that are then included in the general supervised fine-tuning process (Section 3.1). This teaches themodeltoalignwithoursafetyguidelinesevenbeforeRLHF,andthuslaysthefoundationfor high-quality human preference data annotation. 2.Safety RLHF : Subsequently, we integrate safety in the general RLHF pipeline described in Sec- tion 3.2.2. This includes training a safety-specific reward model and gathering more challenging adversarial prompts for rejection sampling style fine-tuning and PPO optimization. 3.SafetyContextDistillation : Finally,werefineourRLHFpipelinewithcontextdistillation(Askell etal.,2021b). Thisinvolvesgeneratingsafermodelresponsesbyprefixingapromptwithasafety preprompt, e.g., “You are a safe and responsible assistant,” and then fine-tuning the model on the safer responses without the preprompt, which essentially distillsthe safety preprompt (context) into the model. Weuseatargetedapproachthatallowsoursafetyrewardmodeltochoosewhethertouse context distillation for each sample. 4.2.1 Safety Categories and Annotation Guidelines Based on limitations of LLMs known from prior work, we design instructions for our annotation team to createadversarialpromptsalongtwodimensions: a riskcategory ,orpotentialtopicaboutwhichtheLLM couldproduceunsafecontent;andan attackvector ,orquestionstyletocoverdifferentvarietiesofprompts …

**Düğüm Kimliği (Node ID):** node-26\
**Benzerlik:** 0.8586079224453517\
**Metin:** AsLLMsareintegratedanddeployed,welookforwardto continuing research that will amplify their potential for positive impact on these important social issues. 4.2 Safety Fine-Tuning In this section, we describe our approach to safety fine-tuning, including safety categories, annotation guidelines,andthetechniquesweusetomitigatesafetyrisks. Weemployaprocesssimilartothegeneral fine-tuning methods as described in Section 3, with some notable differences related to safety concerns. Specifically, we use the following techniques in safety fine-tuning: 1.Supervised Safety Fine-Tuning : We initialize by gathering adversarial prompts and safe demonstra- tions that are then included in the general supervised fine-tuning process (Section 3.1). This teaches themodeltoalignwithoursafetyguidelinesevenbeforeRLHF,andthuslaysthefoundationfor high-quality human preference data annotation. 2.Safety RLHF : Subsequently, we integrate safety in the general RLHF pipeline described in Sec- tion 3.2.2. This includes training a safety-specific reward model and gathering more challenging adversarial prompts for rejection sampling style fine-tuning and PPO optimization. 3.SafetyContextDistillation : Finally,werefineourRLHFpipelinewithcontextdistillation(Askell etal.,2021b). Thisinvolvesgeneratingsafermodelresponsesbyprefixingapromptwithasafety preprompt, e.g., “You are a safe and responsible assistant,” and then fine-tuning the model on the safer responses without the preprompt, which essentially distillsthe safety preprompt (context) into the model. Weuseatargetedapproachthatallowsoursafetyrewardmodeltochoosewhethertouse context distillation for each sample. 4.2.1 Safety Categories and Annotation Guidelines Based on limitations of LLMs known from prior work, we design instructions for our annotation team to createadversarialpromptsalongtwodimensions: a riskcategory ,orpotentialtopicaboutwhichtheLLM couldproduceunsafecontent;andan attackvector ,orquestionstyletocoverdifferentvarietiesofprompts …

```python
query_engine_metadata = RetrieverQueryEngine.from_args(
    retriever_metadata, llm=llm
)
```

```python
response = query_engine_metadata.query(
    "Güvenlik ince ayarı (safety finetuning) için temel kavramlar hakkında bilgi verebilir misiniz?"
)
print(str(response))
```

```text
Güvenlik ince ayarı (safety fine-tuning) için temel kavramlar arasında denetimli güvenlik ince ayarı, güvenlik RLHF (İnsan Geri Bildiriminden Takviyeli Öğrenme) ve güvenlik bağlam damıtması yer alır. Denetimli güvenlik ince ayarı, modelin güvenlik yönergeleriyle uyumlu hale gelmesini eğitmek için düşmanca istemlerin ve güvenli gösterimlerin toplanmasını içerir. Güvenlik RLHF, güvenliğe özgü bir ödül modeli eğiterek ve ince ayar ile optimizasyon için zorlu düşmanca istemler toplanarak güvenliği RLHF hattına entegre eder. Güvenlik bağlam damıtması, bir istemin önüne bir güvenlik ön istemi ekleyerek daha güvenli model yanıtları üretmeyi ve modeli ön istem olmadan daha güvenli yanıtlar üzerinde ince ayarlamayı içerir. Bu kavramlar, güvenlik risklerini azaltmak ve modelin güvenli ve yararlı yanıtlar üretme yeteneğini geliştirmek için kullanılır.
```

## Değerlendirme (Evaluation)

Özyinelemeli erişim + düğüm referansı yöntemlerimizin ne kadar iyi çalıştığını değerlendiriyoruz. Hem parça referanslarını hem de metaveri referanslarını inceliyoruz. Referans düğümlerini getirmek için gömme benzerliği aramasını kullanıyoruz.

Her iki yöntemi de ham düğümleri doğrudan getirdiğimiz temel bir erişiciyle karşılaştırıyoruz.

Metrikler açısından hem isabet oranını (hit-rate) hem de MRR'ı kullanıyoruz.

### Veri Kümesi Üretimi (Dataset Generation)

Önce metin parçaları kümesinden bir soru veri kümesi oluşturuyoruz.

```python
from llama_index.core.evaluation import (
    generate_question_context_pairs,
    EmbeddingQAFinetuneDataset,
)
from llama_index.llms.openai import OpenAI


import nest_asyncio


nest_asyncio.apply()
```

```python
eval_dataset = generate_question_context_pairs(
    base_nodes, OpenAI(model="gpt-3.5-turbo")
)
```

```text
100%|██████████| 93/93 [02:08<00:00,  1.38s/it]
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
from llama_index.core.evaluation import (
    RetrieverEvaluator,
    get_retrieval_results_df,
)


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

```python
vector_retriever_chunk = vector_index_chunk.as_retriever(
    similarity_top_k=top_k
)
retriever_chunk = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever_chunk},
    node_dict=all_nodes_dict,
    verbose=True,
)
retriever_evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"], retriever=retriever_chunk
)
# tüm veri kümesi üzerinde dene
results_chunk = await retriever_evaluator.aevaluate_dataset(
    eval_dataset, show_progress=True
)
```

```python
vector_retriever_metadata = vector_index_metadata.as_retriever(
    similarity_top_k=top_k
)
retriever_metadata = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever_metadata},
    node_dict=all_nodes_dict,
    verbose=True,
)
retriever_evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"], retriever=retriever_metadata
)
# tüm veri kümesi üzerinde dene
results_metadata = await retriever_evaluator.aevaluate_dataset(
    eval_dataset, show_progress=True
)
```

```python
base_retriever = base_index.as_retriever(similarity_top_k=top_k)
retriever_evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"], retriever=base_retriever
)
# tüm veri kümesi üzerinde dene
results_base = await retriever_evaluator.aevaluate_dataset(
    eval_dataset, show_progress=True
)
```

```text
100%|██████████| 194/194 [00:09<00:00, 19.86it/s]
```

```python
full_results_df = get_retrieval_results_df(
    [
        "Temel Erişici (Base Retriever)",
        "Erişici (Parça Referansları)",
        "Erişici (Metaveri Referansları)",
    ],
    [results_base, results_chunk, results_metadata],
)
display(full_results_df)
```

```css
.dataframe tbody tr th {
    vertical-align: top;
}


.dataframe thead th {
    text-align: right;
}
```

|   | erişiciler | isabet\_oranı | mrr |
| - | ------------------------------- | --------- | -------- |
| 0 | Temel Erişici (Base Retriever) | 0.778351 | 0.563103 |
| 1 | Erişici (Parça Referansları) | 0.896907 | 0.691114 |
| 2 | Erişici (Metaveri Referansları) | 0.891753 | 0.718440 |
