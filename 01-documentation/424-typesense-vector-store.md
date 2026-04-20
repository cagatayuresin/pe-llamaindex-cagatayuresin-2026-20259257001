# Typesense Vector Store

---
title: Typesense Vector Store
 | LlamaIndex OSS Documentation
---

#### Veri İndirme

```
%pip install llama-index-embeddings-openai
%pip install llama-index-vector-stores-typesense
```

```
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Belgeleri yükleme, VectorStoreIndex oluşturma

```
# import logging
# import sys


# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from IPython.display import Markdown, display
```

```
# load documents
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```
from llama_index.vector_stores.typesense import TypesenseVectorStore
from typesense import Client


typesense_client = Client(
    {
        "api_key": "xyz",
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "connection_timeout_seconds": 2,
    }
)
typesense_vector_store = TypesenseVectorStore(typesense_client)
storage_context = StorageContext.from_defaults(
    vector_store=typesense_vector_store
)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

#### İndeksi Sorgulama

```
from llama_index.core import QueryBundle
from llama_index.embeddings.openai import OpenAIEmbedding


# Varsayılan olarak, typesense vektör depolama, vektör araması kullanır. Embedding (gömme) işlemini kendiniz sağlamalısınız.
query_str = "What did the author do growing up?"
embed_model = OpenAIEmbedding()
# Ayarları Settings nesnesinden de alabilirsiniz
from llama_index.core import Settings


# embed_model = Settings.embed_model
query_embedding = embed_model.get_agg_embedding_from_queries(query_str)
query_bundle = QueryBundle(query_str, embedding=query_embedding)
response = index.as_query_engine().query(query_bundle)


display(Markdown(f"<b>{response}</b>"))
```

****

**Yazar, bilgisayarların evriminde bir adımı atlayarak büyüdü, İtalyanca öğrendi, Floransa'da yürüdü, insanları resmetti, teknoloji şirketleriyle çalıştı, RISD'de imza stilleri aradı, kirası sabitlenmiş bir dairede yaşadı, yazılım başlattı, kodu düzenledi (Lisp ifadeleri dahil), makaleler yazdı, bunları çevrimiçi yayınladı ve öfkeli okuyuculardan geri bildirim aldı. Ayrıca, 1990'larda üst düzey, özel amaçlı donanım ve yazılım şirketlerini bir araya getiren meta işlemcilerin üstel büyümesini deneyimledi. Ayrıca soyut kavramları birkaç basit fiille birleştirerek biraz İtalyancanın nasıl uzun bir yol kat etmesini sağlayacağını da öğrendi. Ayrıca sanat dünyasında para ve havalılığın sıkı sıkıya bağlı olduğunu ve pahalı olan her şeyin havalı olarak görülmeye başlandığını, havalı olarak görülen her şeyin de yakında aynı derecede pahalı olacağını deneyimledi. Ayrıca, halka açık olarak başlatmadan önce ilk kullanıcı grubunu işe alması ve iyi görünen mağazalara sahip olduklarından emin olması gerektiğinden yazılım başlatmanın zorluğunu da deneyimledi. Ayrıca yorumları okuduğunda ve öfkeli insanlarla dolu olduklarını anladığında, günümüzde artık tanıdık gelen bir deneyimin ilk örneğini yaşadı. Ayrıca internete bir şey koymak ile onu internette yayınlamak arasındaki farkı deneyimledi. Son olarak, biriktirdiği konular hakkında makaleler yazdı ve başkalarının okuması için daha ayrıntılı bir versiyon yazdı.**

```
from llama_index.core.vector_stores.types import VectorStoreQueryMode


# Metin araması da kullanabilirsiniz


query_bundle = QueryBundle(query_str=query_str)
response = index.as_query_engine(
    vector_store_query_mode=VectorStoreQueryMode.TEXT_SEARCH
).query(query_bundle)
display(Markdown(f"<b>{response}</b>"))
```

****

**Yazar, İnternet Balonu sırasında büyüdü ve bir girişim yürütüyordu. Daha profesyonel görünmek için istediklerinden daha fazla insanı işe almak zorunda kaldılar ve Yahoo onları satın alana kadar yatırımcılarının insafına kaldılar. Perakende ve girişimler hakkında çok şey öğrendiler ve işlerini başarılı kılmak için mutlaka iyi olmadıkları birçok şeyi yapmak zorunda kaldılar.**
