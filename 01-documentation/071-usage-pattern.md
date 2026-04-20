# Kullanım Kalıbı (Usage Pattern)

## Başlarken

İndeksten bir sorgu motoru oluşturun:

```python
query_engine = index.as_query_engine()
```

> **İpucu:** İndeks oluşturmayı öğrenmek için [İndeksleme](/python/framework/module_guides/indexing) bölümüne bakın.

Verileriniz üzerinde bir soru sorun:

```python
response = query_engine.query("Paul Graham kimdir?")
```

## Bir Sorgu Motorunu Yapılandırma

### Üst Düzey API (High-Level API)

Tek satır kodla bir indeksten doğrudan bir sorgu motoru oluşturabilir ve yapılandırabilirsiniz:

```python
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
    verbose=True,
)
```

> Not: Üst düzey API kullanım kolaylığı için optimize edilmiş olsa da, tüm yapılandırma seçeneklerini _SUNMAZ_.

Yanıt modlarının tam listesi ve ne işe yaradıkları için [**Yanıt Modları**](/python/framework/module_guides/deploying/query_engine/response_modes) bölümüne bakın.

### Düşük Düzey Bileşim API'si (Low-Level Composition API)

Daha ince taneli bir kontrole ihtiyacınız varsa düşük düzey bileşim API'sini kullanabilirsiniz. Somut olarak konuşursak, `index.as_query_engine(...)` çağırmak yerine açıkça bir `QueryEngine` nesnesi oluşturursunuz.

> Not: API referanslarına veya örnek notebook'lara bakmanız gerekebilir.

Aşağıdakileri yapılandırdığımız bir örnek:

```python
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# indeks oluştur
index = VectorStoreIndex.from_documents(documents)

# getiriciyi (retriever) yapılandır
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2,
)

# yanıt sentezleyiciyi yapılandır
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize",
)

# sorgu motorunu birleştir
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

# sorgula
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

### Akış (Streaming)

Akışı etkinleştirmek için bir `streaming=True` bayrağı geçmeniz yeterlidir:

```python
query_engine = index.as_query_engine(
    streaming=True,
)
streaming_response = query_engine.query(
    "Yazar büyürken ne yaptı?",
)
streaming_response.print_response_stream()
```

-   Tam [akış kılavuzunu](/python/framework/module_guides/deploying/query_engine/streaming) okuyun.
-   Uçtan uca bir [örneğe](/python/examples/customization/streaming/simpleindexdemo-streaming) göz atın.

## Özel Sorgu Motoru Tanımlama

Ayrıca özel bir sorgu motoru da tanımlayabilirsiniz. Sadece `CustomQueryEngine` sınıfını alt sınıfa ayırın, sahip olmak istediğiniz öznitelikleri tanımlayın (bir Pydantic sınıfı tanımlamaya benzer şekilde) ve bir `Response` nesnesi veya bir dize döndüren bir `custom_query` fonksiyonu uygulayın.

```python
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import BaseSynthesizer


class RAGQueryEngine(CustomQueryEngine):
    """RAG Sorgu Motoru."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)
        return response_obj
```

Daha fazla ayrıntı için [Özel Sorgu Motoru kılavuzuna](/python/examples/query_engine/custom_query_engine) bakın.