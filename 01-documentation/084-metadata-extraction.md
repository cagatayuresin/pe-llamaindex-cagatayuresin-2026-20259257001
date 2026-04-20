# Meta Veri Çıkarımı (Metadata Extraction)

## Giriş

Pek çok durumda, özellikle uzun belgelerde, bir metin parçası (chunk), o parçayı diğer benzer metin parçalarından ayırt etmek için gerekli bağlamdan yoksun olabilir.

Bununla mücadele etmek için, getirici (retriever) ve dil modellerinin birbirine benzeyen pasajları ayırt etmesine daha iyi yardımcı olmak amacıyla belgeyle ilgili belirli bağlamsal bilgileri çıkarmak üzere LLM'leri kullanıyoruz.

Bunu bir [örnek notebook](https://github.com/jerryjliu/llama_index/blob/main/docs/examples/metadata_extraction/MetadataExtractionSEC.ipynb) ile gösteriyor ve uzun belgeleri işlemedeki etkinliğini kanıtlıyoruz.

## Kullanım

İlk olarak, sırayla işlenecek bir dizi özellik çıkarıcıyı (feature extractors) alan bir meta veri çıkarıcı tanımlıyoruz.

Daha sonra bunu, her bir node'a ek meta verileri ekleyecek olan node parser'a besliyoruz.

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
)
from llama_index.extractors.entity import EntityExtractor

transformations = [
    SentenceSplitter(),
    TitleExtractor(nodes=5),
    QuestionsAnsweredExtractor(questions=3),
    SummaryExtractor(summaries=["prev", "self"]),
    KeywordExtractor(keywords=10),
    EntityExtractor(prediction_threshold=0.5),
]
```

Ardından, dönüşümlerimizi giriş dökümanları veya node'ları üzerinde çalıştırabiliriz:

```python
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(transformations=transformations)

nodes = pipeline.run(documents=documents)
```

İşte çıkarılan meta verilere bir örnek:

```text
{'page_label': '2',
 'file_name': '10k-132.pdf',
 'document_title': 'Uber Technologies, Inc. 2019 Yıllık Raporu: 69 Ülkede ve 111 Milyon MAPC ile 65 Milyar Dolarlık Brüt Rezervasyonla Hareketlilik ve Lojistikte Devrim Yaratıyor',
 'questions_this_excerpt_can_answer': '\n\n1. Uber Technologies, Inc. kaç ülkede faaliyet gösteriyor?\n2. Uber Technologies, Inc. tarafından hizmet verilen toplam MAPC sayısı kaçtır?\n3. Uber Technologies, Inc. 2019 yılında ne kadar brüt rezervasyon oluşturdu?',
 'prev_section_summary': "\n\n2019 Yıllık Raporu, geçtiğimiz yıl boyunca organizasyon için önemli olan temel konular ve varlıklar hakkında genel bir bakış sunmaktadır. Bunlar arasında mali performans, operasyonel öne çıkanlar, müşteri memnuniyeti, çalışan bağlılığı ve sürdürülebilirlik girişimleri yer almaktadır. Ayrıca organizasyonun önümüzdeki yıl için stratejik hedefleri ve amaçları hakkında bir genel bakış sunar.",
 'section_summary': '\nBu bölüm, temel teknoloji ve altyapıdan yararlanan ürünlerle trilyonlarca dolarlık birden fazla pazara hizmet veren küresel bir teknoloji platformunu tartışmaktadır. Tüketicilerin ve sürücülerin bir düğmeye basarak yolculuk yapmalarını veya çalışmalarını sağlar. Platform, araç paylaşımı ile kişisel hareketlilikte devrim yaratmıştır ve şimdi devasa yemek teslimatı ve lojistik endüstrilerini yeniden tanımlamak için platformundan yararlanmaktadır. Platformun temeli devasa ağı, lider teknolojisi, operasyonel mükemmelliği ve ürün uzmanlığıdır.',
 'excerpt_keywords': '\nAraç Paylaşımı, Hareketlilik, Yemek Teslimatı, Lojistik, Ağ, Teknoloji, Operasyonel Mükemmellik, Ürün Uzmanlığı, Nokta A, Nokta B'}
```

## Özel Çıkarıcılar (Custom Extractors)

Sağlanan çıkarıcılar ihtiyaçlarınıza uymuyorsa, şu şekilde özel bir çıkarıcı da tanımlayabilirsiniz:

```python
from llama_index.core.extractors import BaseExtractor


class CustomExtractor(BaseExtractor):
    async def aextract(self, nodes) -> List[Dict]:
        metadata_list = [
            {
                "custom": node.metadata["document_title"]
                + "\n"
                + node.metadata["excerpt_keywords"]
            }
            for node in nodes
        ]
        return metadata_list
```

`extractor.extract()` metodu, hem senkron hem de asenkron giriş noktaları sağlamak için arka planda otomatik olarak `aextract()` metodunu çağıracaktır.

Daha gelişmiş bir örnekte, node içeriğinden ve mevcut meta verilerden özellikler çıkarmak için bir `llm` de kullanabilir. Daha fazla ayrıntı için [sağlanan meta veri çıkarıcıların kaynak koduna](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/extractors/metadata_extractors.py) bakın.

## Modüller

Aşağıda çeşitli meta veri çıkarıcıları için kılavuzlar ve eğitimler bulacaksınız.

-   [SEC Dökümanları Meta Veri Çıkarımı](/python/examples/metadata_extraction/metadataextractionsec)
-   [LLM Anketi Çıkarımı](/python/examples/metadata_extraction/metadataextraction_llmsurvey)
-   [Varlık Çıkarımı (Entity Extraction)](/python/examples/metadata_extraction/entityextractionclimate)
-   [Marvin Meta Veri Çıkarımı](/python/examples/metadata_extraction/marvinmetadataextractordemo)
-   [Pydantic Meta Veri Çıkarımı](/python/examples/metadata_extraction/pydanticextractor)