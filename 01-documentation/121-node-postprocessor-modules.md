# Node Postprocessor Modülleri

## SimilarityPostprocessor

Benzerlik puanı eşiğinin altındaki node'ları kaldırmak için kullanılır.

```python
from llama_index.core.postprocessor import SimilarityPostprocessor

postprocessor = SimilarityPostprocessor(similarity_cutoff=0.7)

postprocessor.postprocess_nodes(nodes)
```

## KeywordNodePostprocessor

Belirli anahtar kelimelerin hariç tutulduğundan veya dahil edildiğinden emin olmak için kullanılır.

```python
from llama_index.core.postprocessor import KeywordNodePostprocessor

postprocessor = KeywordNodePostprocessor(
    required_keywords=["kelime1", "kelime2"], exclude_keywords=["kelime3", "kelime4"]
)

postprocessor.postprocess_nodes(nodes)
```

## MetadataReplacementPostProcessor

Node içeriğini, node meta verilerinden bir alanla değiştirmek için kullanılır. Eğer alan meta verilerde yoksa, node metni değişmeden kalır. En çok `SentenceWindowNodeParser` ile birlikte kullanıldığında yararlıdır.

```python
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

postprocessor = MetadataReplacementPostProcessor(
    target_metadata_key="window",
)

postprocessor.postprocess_nodes(nodes)
```

## LongContextReorder

Modeller, genişletilmiş bağlamların merkezinde bulunan önemli ayrıntılara erişmekte zorlanırlar. [Bir çalışma](https://arxiv.org/abs/2307.03172), en iyi performansın tipik olarak kritik veriler girdi bağlamının başında veya sonunda yer aldığında ortaya çıktığını gözlemlemiştir. Ayrıca, girdi bağlamı uzadıkça, uzun bağlamlar için tasarlanmış modellerde bile performans belirgin şekilde düşer.

Bu modül, büyük bir top-k gerektiği durumlarda yardımcı olabilecek şekilde getirilen node'ları yeniden sıralayacaktır.

```python
from llama_index.core.postprocessor import LongContextReorder

postprocessor = LongContextReorder()

postprocessor.postprocess_nodes(nodes)
```

## SentenceEmbeddingOptimizer

Bu postprocessor, sorguyla ilgili olmayan cümleleri kaldırarak token kullanımını optimize eder (bu işlem embedding'ler kullanılarak yapılır).

Yüzdelik eşiği (percentile cutoff), ilgili cümlelerin en üst yüzdesini kullanmak için bir ölçüdür.

Bunun yerine, hangi cümlelerin tutulacağını seçmek için ham bir benzerlik eşiği kullanan `threshold_cutoff` da belirtilebilir.

```python
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer

postprocessor = SentenceEmbeddingOptimizer(
    embed_model=service_context.embed_model,
    percentile_cutoff=0.5,
    # threshold_cutoff=0.7
)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/optimizerdemo) ulaşabilirsiniz.

## CohereRerank

Node'ları yeniden sıralamak için "Cohere ReRank" işlevini kullanır ve en üstteki N node'u döndürür.

```python
from llama_index.postprocessor.cohere_rerank import CohereRerank

postprocessor = CohereRerank(
    top_n=2, model="rerank-english-v2.0", api_key="COHERE API ANAHTARINIZ"
)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/coherererank) ulaşabilirsiniz.

## SentenceTransformerRerank

Node'ları yeniden sıralamak için `sentence-transformer` paketindeki cross-encoder'ları kullanır ve en üstteki N node'u döndürür.

```python
from llama_index.core.postprocessor import SentenceTransformerRerank

# Nispeten yüksek hıza ve düzgün doğruluğa sahip bir model seçiyoruz.
postprocessor = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=3
)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/sentencetransformerrerank) ulaşabilirsiniz.

Lütfen daha eksiksiz bir model listesi (hız/doğruluk dengelerini de gösteren) için [`sentence-transformer` dökümanlarına](https://www.sbert.net/docs/pretrained-models/ce-msmarco.html) bakın. Varsayılan model, en yüksek hızı sağlayan `cross-encoder/ms-marco-TinyBERT-L-2-v2` modelidir.

## LLM Rerank

LLM'den ilgili dökümanları ve ne kadar ilgili olduklarına dair bir puan döndürmesini isteyerek node'ları yeniden sıralamak için bir LLM kullanır. En üstteki N sıralanmış node'u döndürür.

```python
from llama_index.core.postprocessor import LLMRerank

postprocessor = LLMRerank(top_n=2, service_context=service_context)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzu; [Gatsby için burada](/python/examples/node_postprocessor/llmreranker-gatsby) ve [Lyft 10K dökümanları için burada](/python/examples/node_postprocessor/llmreranker-lyft-10k) mevcuttur.

## JinaRerank

Node'ları yeniden sıralamak için "Jina ReRank" işlevini kullanır ve en üstteki N node'u döndürür.

```python
from llama_index.postprocessor.jinaai_rerank import JinaRerank

postprocessor = JinaRerank(
    top_n=2, model="jina-reranker-v1-base-en", api_key="JINA API ANAHTARINIZ"
)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/jinarerank) ulaşabilirsiniz.

## FixedRecencyPostprocessor

Bu postprocessor, tarihe göre sıralanmış en üstteki K node'u döndürür. Her node'un meta verilerinde ayrıştırılacak bir `date` (tarih) alanı olduğu varsayılır.

```python
from llama_index.core.postprocessor import FixedRecencyPostprocessor

postprocessor = FixedRecencyPostprocessor(
    tok_k=1, date_key="date"  # tarihin bulunacağı meta veri anahtarı
)

postprocessor.postprocess_nodes(nodes)
```

![](./../../../_static/node_postprocessors/recency.png)

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/recencypostprocessordemo) ulaşabilirsiniz.

## EmbeddingRecencyPostprocessor

Bu postprocessor; tarihe göre sıraladıktan ve embedding benzerliğini ölçtükten sonra birbirine çok benzeyen daha eski node'ları kaldırdıktan sonra en üstteki K node'u döndürür.

```python
from llama_index.core.postprocessor import EmbeddingRecencyPostprocessor

postprocessor = EmbeddingRecencyPostprocessor(
    service_context=service_context, date_key="date", similarity_cutoff=0.7
)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/recencypostprocessordemo) ulaşabilirsiniz.

## TimeWeightedPostprocessor

Bu postprocessor, her bir node'a zaman ağırlıklı bir yeniden sıralama (rerank) uygulayarak en üstteki K node'u döndürür. Bir node her getirildiğinde, getirildiği zaman kaydedilir. Bu, aramayı henüz bir sorguda döndürülmemiş olan bilgileri tercih edecek şekilde yönlendirir.

```python
from llama_index.core.postprocessor import TimeWeightedPostprocessor

postprocessor = TimeWeightedPostprocessor(time_decay=0.99, top_k=1)

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/timeweightedpostprocessordemo) ulaşabilirsiniz.

## (Beta) PIINodePostprocessor

PII (Personal Identifiable Information - Kişisel Tanımlanabilir Bilgi) postprocessor'ı, güvenlik riski oluşturabilecek bilgileri kaldırır. Bunu; (özel bir NER modeliyle veya yerel bir LLM modeliyle) NER (Named Entity Recognition - Varlık İsmi Tanıma) kullanarak yapar.

### LLM Versiyonu

```python
from llama_index.core.postprocessor import PIINodePostprocessor

postprocessor = PIINodePostprocessor(
    service_context=service_context  # bu, güvendiğiniz bir LLM ile kurulmalıdır
)

postprocessor.postprocess_nodes(nodes)
```

### NER Versiyonu

Bu versiyon, `pipeline("ner")` çalıştırdığınızda yüklenen Hugging Face'in varsayılan yerel modelini kullanır.

```python
from llama_index.core.postprocessor import NERPIINodePostprocessor

postprocessor = NERPIINodePostprocessor()

postprocessor.postprocess_nodes(nodes)
```

Her iki sürüm için de not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/pii) ulaşabilirsiniz.

## (Beta) PrevNextNodePostprocessor

`Node` ilişkilerini okumak ve önceki, sonraki veya her iki node'u da getirmek için önceden tanımlanmış ayarları kullanır.

Bu özellik; ilişkilerin, o node getirildiğinde LLM'e gönderilmesi gereken önemli verilere (öncesindeki, sonrasındaki veya her ikisi) işaret ettiğini bildiğiniz durumlarda yararlıdır.

```python
from llama_index.core.postprocessor import PrevNextNodePostprocessor

postprocessor = PrevNextNodePostprocessor(
    docstore=index.docstore,
    num_nodes=1,  # ileri veya geri bakarken getirilecek node sayısı
    mode="next",  # 'next', 'previous' veya 'both' olabilir
)

postprocessor.postprocess_nodes(nodes)
```

![](./../../../_static/node_postprocessors/prev_next.png)

## (Beta) AutoPrevNextNodePostprocessor

PrevNextNodePostprocessor ile aynıdır ancak modun (sonraki, önceki veya her ikisi) seçilmesini LLM'e bırakır.

```python
from llama_index.core.postprocessor import AutoPrevNextNodePostprocessor

postprocessor = AutoPrevNextNodePostprocessor(
    docstore=index.docstore,
    service_context=service_context,
    num_nodes=1,  # ileri veya geri bakarken getirilecek node sayısı
)
postprocessor.postprocess_nodes(nodes)
```

Tam bir örnek not defterine [buradan](/python/examples/node_postprocessor/prevnextpostprocessordemo) ulaşabilirsiniz.

## (Beta) RankGPT

Dökümanları uygunluğa göre yeniden sıralamak için RankGPT ajanını kullanır. En üstteki N sıralanmış node'u döndürür.

```python
from llama_index.postprocessor.rankgpt_rerank import RankGPTRerank

postprocessor = RankGPTRerank(top_n=3, llm=OpenAI(model="gpt-3.5-turbo-16k"))

postprocessor.postprocess_nodes(nodes)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/rankgpt) ulaşabilirsiniz.

## Colbert Reranker

Sorgu token'ları ile pasaj token'ları arasındaki ince ayarlı (fine-grained) benzerliğe göre dökümanları yeniden sıralamak için bir reranker olarak Colbert V2 modelini kullanır. En üstteki N sıralanmış node'u döndürür.

```python
from llama_index.postprocessor.colbert_rerank import ColbertRerank

colbert_reranker = ColbertRerank(
    top_n=5,
    model="colbert-ir/colbertv2.0",
    tokenizer="colbert-ir/colbertv2.0",
    keep_retrieval_score=True,
)

query_engine = index.as_query_engine(
    similarity_top_k=10,
    node_postprocessors=[colbert_reranker],
)
response = query_engine.query(
    query_str,
)
```

Tam not defteri kılavuzuna [buradan](/python/examples/node_postprocessor/colbertrerank) ulaşabilirsiniz.

## rankLLM

Dökümanları yeniden sıralamak için [rankLLM](https://github.com/castorini/rank_llm) modellerini kullanır. En üstteki N sıralanmış node'u döndürür.

```python
from llama_index.postprocessor.rankllm_rerank import RankLLMRerank

# RankZephyr reranker, en iyi 5 adayı döndür
reranker = RankLLMRerank(model="rank_zephyr", top_n=5)
reranker.postprocess_nodes(nodes)
```

Tam bir [not defteri örneğine buradan](/python/examples/node_postprocessor/rankllm) ulaşabilirsiniz.

## Tüm Not Defterleri

-   [Cümle Optimize Edici (Sentence Optimizer)](/python/examples/node_postprocessor/optimizerdemo)
-   [Cohere Rerank](/python/examples/node_postprocessor/coherererank)
-   [LLM Reranker Lyft 10k](/python/examples/node_postprocessor/llmreranker-lyft-10k)
-   [LLM Reranker Gatsby](/python/examples/node_postprocessor/llmreranker-gatsby)
-   [Güncellik (Recency)](/python/examples/node_postprocessor/recencypostprocessordemo)
-   [Zaman Ağırlıklı (Time Weighted)](/python/examples/node_postprocessor/timeweightedpostprocessordemo)
-   [PII](/python/examples/node_postprocessor/pii)
-   [ÖncekiSonraki (PrevNext)](/python/examples/node_postprocessor/prevnextpostprocessordemo)
-   [Meta Veri Değiştirme (Metadata Replacement)](/python/examples/node_postprocessor/metadatareplacementdemo)
-   [Uzun Bağlam Yeniden Sıralama (Long Context Reorder)](/python/examples/node_postprocessor/longcontextreorder)
-   [RankGPT](/python/examples/node_postprocessor/rankgpt)
-   [Colbert Rerank](/python/examples/node_postprocessor/colbertrerank)
-   [JinaAI Rerank](/python/examples/node_postprocessor/jinarerank)
-   [MixedBread Rerank](/python/examples/cookbooks/mixedbread_reranker)
-   [RankLLM](/python/examples/node_postprocessor/rankllm)