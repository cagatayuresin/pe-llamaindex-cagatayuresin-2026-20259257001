# ChatGPT Eklenti Entegrasyonları (ChatGPT Plugin Integrations)

**NOT**: Bu çalışma devam etmektedir, bu konudaki heyecan verici güncellemeler için takipte kalın!

## ChatGPT Erişim Eklentisi Entegrasyonları (ChatGPT Retrieval Plugin Integrations)

[OpenAI ChatGPT Erişim Eklentisi (Retrieval Plugin)](https://github.com/openai/chatgpt-retrieval-plugin), herhangi bir döküman saklama sisteminin ChatGPT ile etkileşime girmesi için merkezi bir API spesifikasyonu sunar. Bu herhangi bir servis üzerinde konuşlandırılabildiğinden, giderek daha fazla döküman erişim servisinin bu spesifikasyonu uygulayacağı anlamına gelir; bu da onların sadece ChatGPT ile değil, aynı zamanda bir erişim servisi kullanabilecek herhangi bir LLM araç seti ile de etkileşime girmesine olanak tanır.

LlamaIndex, ChatGPT Erişim Eklentisi ile çeşitli entegrasyonlar sağlar.

### LlamaHub'dan ChatGPT Erişim Eklentisine Veri Yükleme

ChatGPT Erişim Eklentisi, kullanıcıların döküman yüklemesi için bir `/upsert` uç noktası (endpoint) tanımlar. Bu, çeşitli API'lerden ve döküman formatlarından 65'in üzerinde veri yükleyici sunan LlamaHub ile doğal bir entegrasyon noktası sunar.

İşte LlamaHub'dan bir dökümanın `/upsert` uç noktasının beklediği JSON formatına nasıl yükleneceğini gösteren örnek bir kod parçası:

```python
from llama_index.core import download_loader, Document
from typing import Dict, List
import json

# yükleyiciyi indir, dökümanları yükle
from llama_index.readers.web import SimpleWebPageReader

loader = SimpleWebPageReader(html_to_text=True)
url = "http://www.paulgraham.com/worked.html"
documents = loader.load_data(urls=[url])


# LlamaIndex Dökümanlarını JSON formatına dönüştür
def dump_docs_to_json(documents: List[Document], out_path: str) -> Dict:
    """LlamaIndex Dökümanlarını JSON formatına dönüştür ve kaydet."""
    result_json = []
    for doc in documents:
        cur_dict = {
            "text": doc.get_text(),
            "id": doc.get_doc_id(),
            # NOT: diğer alanları istediğiniz gibi özelleştirebilirsiniz
            # alanlar şuradan alınmıştır: https://github.com/openai/chatgpt-retrieval-plugin/tree/main/scripts/process_json#usage
            # "source": ...,
            # "source_id": ...,
            # "url": url,
            # "created_at": ...,
            # "author": "Paul Graham",
        }
        result_json.append(cur_dict)

    json.dump(result_json, open(out_path, "w"))
```

Daha fazla detay için [tam örnek not defterine](https://github.com/jerryjliu/llama_index/blob/main/examples/chatgpt_plugin/ChatGPT_Retrieval_Plugin_Upload.ipynb) göz atın.

### ChatGPT Erişim Eklentisi Veri Yükleyicisi (Data Loader)

ChatGPT Erişim Eklentisi veri yükleyicisine [LlamaHub üzerinden erişilebilir](https://llamahub.ai/l/chatgpt_plugin).

Eklenti API'sini uygulayan herhangi bir döküman deposundan (docstore) LlamaIndex veri yapısına kolayca veri yüklemenizi sağlar.

Örnek kod:

```python
from llama_index.readers.chatgpt_plugin import ChatGPTRetrievalPluginReader
import os

# dökümanları yükle
bearer_token = os.getenv("BEARER_TOKEN")
reader = ChatGPTRetrievalPluginReader(
    endpoint_url="http://localhost:8000", bearer_token=bearer_token
)
documents = reader.load_data("Yazar büyürken ne yaptı?")

# indeksi oluştur ve sorgula
from llama_index.core import SummaryIndex

index = SummaryIndex.from_documents(documents)
# daha detaylı çıktılar için Logging'i DEBUG olarak ayarlayın
query_engine = index.as_query_engine(response_mode="compact")
response = query_engine.query(
    "Erişilen içeriği özetle ve yazarın büyürken ne yaptığını açıkla",
)
```

Daha fazla detay için [tam örnek not defterine](https://github.com/jerryjliu/llama_index/blob/main/examples/chatgpt_plugin/ChatGPTRetrievalPluginReaderDemo.ipynb) göz atın.

### ChatGPT Erişim Eklentisi İndeksi (Index)

ChatGPT Erişim Eklentisi İndeksi, ChatGPT uç noktasını uygulayan bir döküman deposu tarafından desteklenen saklama alanı ile herhangi bir döküman üzerinde kolayca bir vektör indeksi oluşturmanıza olanak tanır.

Not: Bu indeks bir vektör indeksidir ve top-k erişimine (retrieval) olanak tanır.

Örnek kod:

```python
from llama_index.core.indices.vector_store import ChatGPTRetrievalPluginIndex
from llama_index.core import SimpleDirectoryReader
import os

# dökümanları yükle
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()

# indeksi oluştur
bearer_token = os.getenv("BEARER_TOKEN")
# meta veri filtresi olmadan başlat
index = ChatGPTRetrievalPluginIndex(
    documents,
    endpoint_url="http://localhost:8000",
    bearer_token=bearer_token,
)

# indeksi sorgula
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact",
)
response = query_engine.query("Yazar büyürken ne yaptı?")
```

Daha fazla detay için [tam örnek not defterine](https://github.com/jerryjliu/llama_index/blob/main/examples/chatgpt_plugin/ChatGPTRetrievalPluginIndexDemo.ipynb) göz atın.