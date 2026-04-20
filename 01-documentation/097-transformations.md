# Dönüşümler (Transformations)

Bir dönüşüm, girdi olarak bir node listesi alan ve çıktı olarak bir node listesi döndüren yapıdır. `Transformation` temel sınıfını uygulayan her bileşen, hem senkron bir `__call__()` tanımına hem de asenkron bir `acall()` tanımına sahiptir.

Şu anda, aşağıdaki bileşenler `Transformation` nesneleridir:

-   [`TextSplitter`](/python/framework/module_guides/loading/node_parsers/modules#text-splitters)
-   [`NodeParser`](/python/framework/module_guides/loading/node_parsers/modules)
-   [`MetadataExtractor`](/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor)
-   `Embeddings` modeli (desteklenen [embedding listemize](/python/framework/module_guides/models/embeddings#list-of-supported-embeddings) göz atın)

## Kullanım Kalıbı (Usage Pattern)

Dönüşümler en iyi bir [`IngestionPipeline`](/python/framework/module_guides/loading/ingestion_pipeline) ile birlikte kullanılırken, doğrudan da kullanılabilirler.

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor

node_parser = SentenceSplitter(chunk_size=512)
extractor = TitleExtractor()

# dönüşümleri doğrudan kullanın
nodes = node_parser(documents)

# veya asenkron olarak bir dönüşüm kullanın
nodes = await extractor.acall(nodes)
```

## Bir İndeks ile Birleştirme

Dönüşümler bir indekse veya genel küresel ayarlara geçirilebilir ve bir indeks üzerinde `from_documents()` veya `insert()` çağrılırken kullanılacaktır.

```python
from llama_index.core import VectorStoreIndex
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

transformations = [
    TokenTextSplitter(chunk_size=512, chunk_overlap=128),
    TitleExtractor(nodes=5),
    QuestionsAnsweredExtractor(questions=3),
]

# küresel (global)
from llama_index.core import Settings

Settings.transformations = [text_splitter, title_extractor, qa_extractor]

# indeks başına
index = VectorStoreIndex.from_documents(
    documents, transformations=transformations
)
```

## Özel Dönüşümler (Custom Transformations)

Temel sınıfı uygulayarak herhangi bir dönüşümü kendiniz gerçekleştirebilirsiniz.

Aşağıdaki özel dönüşüm, metindeki tüm özel karakterleri veya noktalama işaretlerini kaldıracaktır.

```python
import re
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.schema import TransformComponent


class TextCleaner(TransformComponent):
    def __call__(self, nodes, **kwargs):
        for node in nodes:
            node.text = re.sub(r"[^0-9A-Za-z ]", "", node.text)
        return nodes
```

Bunlar daha sonra doğrudan veya herhangi bir `IngestionPipeline` içinde kullanılabilir.

```python
# bir boru hattında kullanın
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TextCleaner(),
        OpenAIEmbedding(),
    ],
)

nodes = pipeline.run(documents=[Document.example()])
```