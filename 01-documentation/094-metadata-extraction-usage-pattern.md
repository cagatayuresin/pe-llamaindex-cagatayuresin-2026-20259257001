# Meta Veri Çıkarımı Kullanım Kalıbı

`Metadata Extractor` (Meta Veri Çıkarıcı) modüllerimizle meta veri çıkarımını otomatikleştirmek için LLM'leri kullanabilirsiniz.

Meta veri çıkarıcı modüllerimiz aşağıdaki "özellik çıkarıcıları" (feature extractors) içerir:

-   `SummaryExtractor` - Bir dizi node üzerinden otomatik olarak bir özet çıkarır.
-   `QuestionsAnsweredExtractor` - Her bir node'un cevaplayabileceği bir dizi soru çıkarır.
-   `TitleExtractor` - Her bir node'un bağlamı üzerinden bir başlık çıkarır.
-   `EntityExtractor` - Her bir node'un içeriğinde geçen varlıkları (yani yer, kişi, nesne isimleri) çıkarır.

Ardından `Metadata Extractor`'ları node parser'ımız (düğüm ayrıştırıcısı) ile zincirleyebilirsiniz:

```python
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.node_parser import TokenTextSplitter

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)
title_extractor = TitleExtractor(nodes=5)
qa_extractor = QuestionsAnsweredExtractor(questions=3)

# dökümanların tanımlandığını varsayalım -> node'ları çıkarın
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[text_splitter, title_extractor, qa_extractor]
)

nodes = pipeline.run(
    documents=documents,
    in_place=True,
    show_progress=True,
)
```

veya bir indekse ekleyin:

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(
    documents, transformations=[text_splitter, title_extractor, qa_extractor]
)
```

## Kaynaklar

-   [SEC Dökümanları Meta Veri Çıkarımı](/python/examples/metadata_extraction/metadataextractionsec)
-   [LLM Anketi Çıkarımı](/python/examples/metadata_extraction/metadataextraction_llmsurvey)
-   [Varlık Çıkarımı (Entity Extraction)](/python/examples/metadata_extraction/entityextractionclimate)
-   [Marvin Meta Veri Çıkarımı](/python/examples/metadata_extraction/marvinmetadataextractordemo)
-   [Pydantic Meta Veri Çıkarımı](/python/examples/metadata_extraction/pydanticextractor)