# `LabelledRagDataset`'ler ile Değerlendirme

LLM tabanlı uygulamaların veya RAG sistemleri dahil sistemlerin çeşitli değerlendirme metodolojilerini sağlayan Değerlendirme (Evaluation) modülündeki temel soyutlamaların üzerinden geçtik. Elbette, bir sistemi değerlendirmek için bir değerlendirme yöntemine, sistemin kendisine ve değerlendirme veri kümelerine ihtiyaç vardır. LLM uygulamasını farklı kaynaklardan ve alanlardan gelen birkaç farklı veri kümesinde test etmek en iyi uygulama olarak kabul edilir. Bunu yapmak, sistemin genel sağlamlığını (yani sistemin görülmemiş, yeni durumlarda ne derece çalışacağını) sağlamaya yardımcı olur.

Bu amaçla, kütüphanemize `LabelledRagDataset` soyutlamasını ekledik. Bu soyutlamanın temel amacı; veri kümelerinin oluşturulmasını kolaylaştırmak, kullanımını basit tutmak ve geniş çapta erişilebilir kılarak sistemlerin çeşitli veri kümeleri üzerinde değerlendirilmesini sağlamaktır.

Bu veri kümesi, her biri bir `query` (sorgu), bir `reference_answer` (referans cevap) ve `reference_contexts` (referans bağlamlar) taşıyan örneklerden oluşur. Bir `LabelledRagDataset` kullanmanın ana nedeni; önce verilen bir sorguya bir yanıt tahmin ederek ve ardından bu tahmin edilen (veya oluşturulan) yanıtı referans cevapla karşılaştırarak bir RAG sisteminin performansını test etmektir.

```python
from llama_index.core.llama_dataset import (
    LabelledRagDataset,
    CreatedBy,
    CreatedByType,
    LabelledRagDataExample,
)

example1 = LabelledRagDataExample(
    query="Bu bir kullanıcı sorgusudur.",
    query_by=CreatedBy(type=CreatedByType.HUMAN),
    reference_answer="Bu bir referans cevaptır. Diğer adıyla temel gerçeklik (ground-truth) cevabı.",
    reference_contexts=[
        "Bu, referans cevabı",
        "oluşturmak için kullanılan",
        "bağlamların listesidir.",
    ],
    reference_by=CreatedBy(type=CreatedByType.HUMAN),
)

# sadece bir örnekten oluşan hüzünlü bir veri kümesi
rag_dataset = LabelledRagDataset(examples=[example1])
```

## Bir `LabelledRagDataset` Oluşturma

Bir önceki bölümün sonunda gördüğümüz gibi, bir `LabelledRagDataset`'i teker teker `LabelledRagDataExample` nesneleri oluşturarak manuel olarak inşa edebiliriz. Ancak bu biraz zahmetlidir ve insan tarafından etiketlenmiş veri kümeleri son derece değerli olsa da, güçlü LLM'ler tarafından oluşturulan veri kümeleri de oldukça faydalıdır.

Bu bağlamda `llama_dataset` modülü, bir dizi kaynak `Document` (Döküman) üzerinden bir `LabelledRagDataset` oluşturabilen `RagDatasetGenerator` ile donatılmıştır.

```python
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
from llama_index.llms.openai import OpenAI
import nest_asyncio

nest_asyncio.apply()

documents = ...  # örneğin bir Reader kullanılarak yüklenmiş bir dizi döküman

llm = OpenAI(model="gpt-4")

dataset_generator = RagDatasetGenerator.from_documents(
    documents=documents,
    llm=llm,
    num_questions_per_chunk=10,  # parça başına soru sayısını ayarlayın
)

rag_dataset = dataset_generator.generate_dataset_from_nodes()
```

## Bir `LabelledRagDataset` Kullanma

Daha önce de belirtildiği gibi, bir `LabelledRagDataset`'i, aynı kaynak dökümanlar üzerine kurulu bir RAG sisteminin performansını değerlendirmek için kullanmak istiyoruz. Bunu yapmak iki adım gerektirir: (1) veri kümesi üzerinde tahminler yapmak (yani her bir örneğin sorgusuna yanıtlar oluşturmak) ve (2) tahmin edilen yanıtı referans cevapla karşılaştırarak değerlendirmek. İkinci adımda ayrıca RAG sisteminin getirdiği bağlamları da değerlendirir ve bunları referans bağlamlarla karşılaştırırız; böylece RAG sisteminin getirme (retrieval) bileşeni hakkında bir değerlendirme elde ederiz.

Kolaylık sağlamak için, bu değerlendirme sürecini kolaylaştıran `RagEvaluatorPack` adında bir `LlamaPack` sunuyoruz!

```python
from llama_index.core.llama_pack import download_llama_pack

RagEvaluatorPack = download_llama_pack("RagEvaluatorPack", "./pack")

rag_evaluator = RagEvaluatorPack(
    query_engine=query_engine,  # rag_dataset ile aynı kaynak Dökümanlar ile oluşturulmuş
    rag_dataset=rag_dataset,
)
benchmark_df = await rag_evaluator.run()
```

Yukarıdaki `benchmark_df`, daha önce tanıtılan değerlendirme ölçütlerinin ortalama puanlarını içerir: `Correctness` (Doğruluk), `Relevancy` (İlgililik), `Faithfulness` (Sadakat) ve yanı sıra referans bağlamlar ile RAG sisteminin tahmini yanıtı oluşturmak için getirdiği bağlamlar arasındaki anlamsal benzerliği ölçen `Context Similarity`.

## `LabelledRagDataset`'ler Nerede Bulunur?

Tüm `LabelledRagDataset`'leri [LlamaHub](https://llamahub.ai) adresinde bulabilirsiniz. Bunların her birine göz atabilir ve RAG iş akışınızı kıyaslamak için kullanmaya karar verirseniz, hem veri kümesini hem de kaynak dökümanları şu iki yoldan biriyle kolayca indirebilirsiniz: `llamaindex-cli` veya `download_llama_dataset` yardımcı fonksiyonunu kullanarak Python kodu üzerinden.

```bash
# cli kullanarak
llamaindex-cli download-llamadataset PaulGrahamEssayDataset --download-dir ./data
```

```python
# python kullanarak
from llama_index.core.llama_dataset import download_llama_dataset

# bir LabelledRagDataset ve kaynak Dökümanların bir listesi
rag_dataset, documents = download_llama_dataset(
    "PaulGrahamEssayDataset", "./data"
)
```

### `LabelledRagDataset` ile Katkıda Bulunma

Ayrıca [LlamaHub](https://llamahub.ai) adresine bir `LabelledRagDataset` ile katkıda bulunabilirsiniz. Bir `LabelledRagDataset` ile katkıda bulunmak iki üst düzey adım içerir. Genel olarak, `LabelledRagDataset`'i oluşturmalı, JSON olarak kaydetmeli ve hem bu JSON dosyasını hem de kaynak metin dosyalarını [llama-datasets](https://github.com/run-llama/llama_datasets) Github depomuza göndermelisiniz. Ek olarak, veri kümesinin gerekli meta verilerini [llama-hub](https://github.com/run-llama/llama-hub) Github depomuza yüklemek için bir çekme isteği (pull request) oluşturmanız gerekecektir.

Lütfen aşağıda bağlantısı verilen "LlamaDataset Gönderim Şablonu Notebook'una" bakın.

## Şimdi, Sağlam LLM Uygulamaları İnşa Edin

Umarız bu sayfa, sağlam ve yüksek performanslı LLM uygulamaları oluşturmak için `LlamaDataset`'lerini oluşturmanız, indirmeniz ve kullanmanız için iyi bir başlangıç noktası olmuştur. Daha fazlasını öğrenmek için aşağıda sunulan notebook kılavuzlarını okumanızı öneririz.

## Kaynaklar

-   [Etiketlenmiş (Labelled) RAG veri kümeleri](/python/examples/llama_dataset/labelled-rag-datasets)
-   [Llama veri kümelerini indirme](/python/examples/llama_dataset/downloading_llama_datasets)