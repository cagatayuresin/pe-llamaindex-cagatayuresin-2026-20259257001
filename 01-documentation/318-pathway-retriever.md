# Pathway Erişicisi (Pathway Retriever)

---
title: Pathway Erişicisi (Pathway Retriever)
 | LlamaIndex OSS Belgeleri
---

> [Pathway](https://pathway.com/), açık bir veri işleme çerçevesidir. Canlı veri kaynakları ve değişen verilerle çalışan veri dönüştürme hatlarını ve Makine Öğrenimi uygulamalarını kolayca geliştirmenize olanak tanır.

Bu not defteri, `LlamaIndex` ile canlı bir veri indeksleme hattının nasıl kullanılacağını gösterir. Bu hattın sonuçlarını, sağlanan `PathwayRetriever`ı kullanarak LLM uygulamanızdan sorgulayabilirsiniz. Ancak Pathway perde arkasında, her veri değişikliğinde indeksi güncelleyerek size her zaman güncel yanıtlar sunar.

Bu not defterinde, aşağıdaki işlemleri gerçekleştiren [herkese açık bir demo belge işleme hattı](https://pathway.com/solutions/ai-pipelines#try-it-out) kullanacağız:

1. Veri değişiklikleri için çeşitli bulut veri kaynaklarını izler.
2. Veriler için bir vektör indeksi oluşturur.

Kendi belge işleme hattınıza sahip olmak için [barındırılan teklife](https://pathway.com/solutions/ai-pipelines) göz atın veya bu not defterini takip ederek [kendi hattınızı oluşturun](https://pathway.com/developers/user-guide/llm-xpack/vectorstore_pipeline/).

İndekse, `retrieve` arayüzünü uygulayan `llama_index.retrievers.pathway.PathwayRetriever` erişicisini kullanarak bağlanacağız.

Bu belgede açıklanan temel hat, bir bulut konumunda depolanan dosyaların basit bir indeksini zahmetsizce oluşturmanıza olanak tanır. Ancak Pathway; farklı veri kaynakları arasında birleştirmeler (joins) ve gruplandırılmış indirgemeler (groupby-reductions) gibi SQL benzeri işlemler, verilerin zamana dayalı gruplandırılması ve pencerelenmesi (windowing) ve çok çeşitli bağlayıcılar (connectors) dahil olmak üzere gerçek zamanlı veri hatları ve uygulamaları oluşturmak için gereken her şeyi sağlar.

Pathway veri alımı (ingestion) hattı ve vektör deposu hakkında daha fazla ayrıntı için [vektör deposu hattı (vector store pipeline)](https://pathway.com/developers/showcases/vectorstore_pipeline) sayfasını ziyaret edin.

## Ön Koşullar (Prerequisites)

`PathwayRetriever`ı kullanmak için `llama-index-retrievers-pathway` paketini kurmalısınız.

```bash
!pip install llama-index-retrievers-pathway
```

## llama-index için Erişici Oluşturma (Create Retriever for llama-index)

`PathwayRetriever`ı başlatmak ve yapılandırmak için belge indeksleme hattınızın `url` değerini veya `host` ve `port` bilgilerini sağlamanız gerekir. Aşağıdaki kodda, REST API'sine `https://demo-document-indexing.pathway.stream` adresinden erişebileceğiniz herkese açık bir [demo hattı](https://pathway.com/solutions/ai-pipelines#try-it-out) kullanıyoruz. Bu demo; [Google Drive](https://drive.google.com/drive/u/0/folders/1cULDv2OaViJBmOfG5WB0oWcgayNrGtVs) ve [Sharepoint](https://navalgo.sharepoint.com/sites/ConnectorSandbox/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FConnectorSandbox%2FShared%20Documents%2FIndexerSandbox\&p=true\&ga=1) üzerinden belgeleri alır ve belgeleri getirmek için bir indeksi güncel tutar.

```python
from llama_index.retrievers.pathway import PathwayRetriever


retriever = PathwayRetriever(
    url="https://demo-document-indexing.pathway.stream"
)
retriever.retrieve(str_or_query_bundle="pathway nedir")
```

**Sıra sizde!** [Kendi hattınızı edinin](https://pathway.com/solutions/ai-pipelines) veya demo hattına [yeni belgeler](https://chat-realtime-sharepoint-gdrive.demo.pathway.com/) yükleyin ve sorguyu tekrar deneyin!

## Sorgu Motorunda Kullanım (Use in Query Engine)

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine.from_args(
    retriever,
)
```

```python
response = query_engine.query("Bana Pathway hakkında bilgi ver")
print(str(response))
```

## Kendi veri işleme hattınızı oluşturma (Building your own data processing pipeline)

### Ön Koşullar (Prerequisites)

`pathway` paketini kurun. Ardından örnek verileri indirin.

```bash
%pip install pathway
%pip install llama-index-embeddings-openai
```

```bash
!mkdir -p 'data/'
!wget 'https://gist.githubusercontent.com/janchorowski/dd22a293f3d99d1b726eedc7d46d2fc0/raw/pathway_readme.md' -O 'data/pathway_readme.md'
```

### Pathway tarafından izlenen veri kaynaklarını tanımlama (Define data sources tracked by Pathway)

Pathway; yerel dosyalar, S3 klasörleri, bulut depolama ve veri değişiklikleri için herhangi bir veri akışı gibi birçok kaynağı aynı anda dinleyebilir.

Daha fazla bilgi için [pathway-io](https://pathway.com/developers/api-docs/pathway-io) sayfasını ziyaret edin.

```python
import pathway as pw


data_sources = []
data_sources.append(
    pw.io.fs.read(
        "./data",
        format="binary",
        mode="streaming",
        with_metadata=True,
    )  # Bu, ./data dizinindeki tüm dosyaları izleyen 
    # bir `pathway` bağlayıcısı (connector) oluşturur.
)


# Bu, Google Drive'daki dosyaları izleyen bir bağlayıcı oluşturur.
# Kimlik bilgilerini (credentials) almak için lütfen https://pathway.com/developers/tutorials/connectors/gdrive-connector/ 
# adresindeki talimatları izleyin.
# data_sources.append(
#     pw.io.gdrive.read(object_id="17H4YpBOAKQzEJ93xmC2z170l0bP2npMy", service_user_credentials_file="credentials.json", with_metadata=True))
```

### Belge indeksleme hattını oluşturma (Create the document indexing pipeline)

Belge indeksleme hattını oluşturalım. `transformations`, bir `Embedding` dönüşümü ile biten bir `TransformComponent` listesi olmalıdır.

Bu örnekte metni önce `TokenTextSplitter` kullanarak bölelim, ardından `OpenAIEmbedding` ile gömelim.

```python
from pathway.xpacks.llm.vector_store import VectorStoreServer
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import TokenTextSplitter


embed_model = OpenAIEmbedding(embed_batch_size=10)


transformations_example = [
    TokenTextSplitter(
        chunk_size=150,
        chunk_overlap=10,
        separator=" ",
    ),
    embed_model,
]


processing_pipeline = VectorStoreServer.from_llamaindex_components(
    *data_sources,
    transformations=transformations_example,
)


# Pathway'in üzerinde olacağı Host ve port bilgilerini tanımlayın
PATHWAY_HOST = "127.0.0.1"
PATHWAY_PORT = 8754


# `threaded` parametresi Pathway'i ayrılmış (detached) modda çalıştırır; 
# terminalden veya bir konteynerden çalıştırırken bunu False olarak ayarlamalıyız.
# `with_cache` hakkında daha fazla bilgi için bkz. https://pathway.com/developers/api-docs/persistence-api
processing_pipeline.run_server(
    host=PATHWAY_HOST, port=PATHWAY_PORT, with_cache=False, threaded=True
)
```

### Erişiciyi özel hatta bağlama (Connect the retriever to the custom pipeline)

```python
from llama_index.retrievers.pathway import PathwayRetriever


# Erişiciyi (retriever) oluştur ve host/port bilgilerini ver
retriever = PathwayRetriever(host=PATHWAY_HOST, port=PATHWAY_PORT)
retriever.retrieve(str_or_query_bundle="pathway nedir")
```
