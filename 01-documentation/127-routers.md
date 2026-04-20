# Yönlendiriciler (Routers)

## Kavram

Yönlendiriciler (Routers); bir kullanıcı sorgusunu ve (meta verilerle tanımlanmış) bir grup "seçeneği" (choices) alan ve bir veya daha fazla seçilmiş seçeneği döndüren modüllerdir.

Tek başlarına ("seçici modüller" olarak) kullanılabilecekleri gibi, bir sorgu motoru veya retriever olarak da (örneğin; diğer sorgu motorlarının/retriever'ların üzerinde) kullanılabilirler.

Karar verme yetenekleri için LLM'leri kullanan basit ama güçlü modüllerdir. Aşağıdaki kullanım durumları ve daha fazlası için kullanılabilirler:

-   Çeşitli veri kaynakları arasından doğru veri kaynağını seçmek.
-   Özetleme (örneğin; summary index sorgu motoru kullanarak) mi yoksa semantik arama (örneğin; vector index sorgu motoru kullanarak) mı yapılacağına karar vermek.
-   Aynı anda bir dizi seçeneği "deneyip" sonuçları birleştirip birleştirmemeye (çoklu yönlendirme yeteneklerini kullanarak) karar vermek.

Temel yönlendirici modülleri aşağıdaki formlarda mevcuttur:

-   LLM seçiciler (selectors), seçenekleri bir metin dökümü (text dump) olarak bir istemin içine koyar ve karar vermek için LLM metin tamamlama uç noktasını kullanır.
-   Pydantic seçiciler, seçenekleri Pydantic şemaları olarak bir fonksiyon çağırma (function calling) uç noktasına aktarır ve Pydantic nesneleri döndürür.

## Kullanım Kalıbı (Usage Pattern)

Yönlendirici modülümüzü bir sorgu motorunun parçası olarak kullanmaya dair basit bir örnek aşağıda verilmiştir.

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import QueryEngineTool


list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Veri kaynağıyla ilgili özetleme soruları için yararlıdır",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Veri kaynağıyla ilgili spesifik bağlamı getirmek için yararlıdır",
)

query_engine = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(),
    query_engine_tools=[
        list_tool,
        vector_tool,
    ],
)
query_engine.query("<sorgu>")
```

## Kullanım Kalıbı

Bir "seçici" (selector) tanımlamak, bir yönlendiriciyi tanımlamanın merkezinde yer alır.

Yönlendiricilerimizi kolayca bir sorgu motoru veya retriever olarak kullanabilirsiniz. Bu durumlarda yönlendirici; kullanıcı sorgusunu yönlendirmek için sorgu motorlarını veya retriever'ları "seçmekten" sorumlu olacaktır.

Ayrıca, getirme destekli yönlendirme (retrieval-augmented routing) için `ToolRetrieverRouterQueryEngine` modülümüzü de vurguluyoruz - bu, seçenek kümesinin kendisinin çok büyük olabileceği ve indekslenmesi gerekebileceği durumlar içindir. **NOT**: Bu bir beta özelliğidir.

Ayrıca yönlendiricimizi bağımsız bir modül olarak kullanmayı da gösteriyoruz.

## Bir Seçici (Selector) Tanımlama

LLM ve Pydantic tabanlı tekli/çoklu seçicilerle ilgili bazı örnekler aşağıda verilmiştir:

```python
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector
from llama_index.core.selectors import (
    PydanticMultiSelector,
    PydanticSingleSelector,
)

# pydantic seçiciler, pydantic nesnelerini bir fonksiyon çağırma API'sine besler
# tekli seçici (pydantic)
selector = PydanticSingleSelector.from_defaults()
# çoklu seçici (pydantic)
selector = PydanticMultiSelector.from_defaults()

# LLM seçiciler metin tamamlama uç noktalarını kullanır
# tekli seçici (LLM)
selector = LLMSingleSelector.from_defaults()
# çoklu seçici (LLM)
selector = LLMMultiSelector.from_defaults()
```

## Sorgu Motoru Olarak Kullanma

Bir `RouterQueryEngine`, araç olarak kullanılan diğer sorgu motorlarının üzerine inşa edilir.

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.selectors.pydantic_selectors import Pydantic
from llama_index.core.tools import QueryEngineTool
from llama_index.core import VectorStoreIndex, SummaryIndex

# sorgu motorlarını tanımla
...

# araçları başlat
list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Veri kaynağıyla ilgili özetleme soruları için yararlıdır",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Veri kaynağıyla ilgili spesifik bağlamı getirmek için yararlıdır",
)

# yönlendirici sorgu motorunu başlat (tekli seçim, pydantic)
query_engine = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(),
    query_engine_tools=[
        list_tool,
        vector_tool,
    ],
)
query_engine.query("<sorgu>")
```

## Retriever Olarak Kullanma

Benzer şekilde, bir `RouterRetriever` diğer retriever'ların üzerine araç olarak inşa edilir. Aşağıda bir örnek verilmiştir:

```python
from llama_index.core.retrievers import RouterRetriever
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import RetrieverTool

# indeksleri tanımla
...

# retriever'ları tanımla
vector_retriever = vector_index.as_retriever()
keyword_retriever = keyword_index.as_retriever()

# araçları başlat
vector_tool = RetrieverTool.from_defaults(
    retriever=vector_retriever,
    description="Paul Graham'ın 'Neler Üzerine Çalıştım' makalesinden spesifik bağlam getirmek için yararlıdır.",
)
keyword_tool = RetrieverTool.from_defaults(
    retriever=keyword_retriever,
    description="Paul Graham'ın 'Neler Üzerine Çalıştım' makalesinden spesifik bağlam getirmek için yararlıdır (sorguda geçen varlıkları kullanarak).",
)

# retriever'ı tanımla
retriever = RouterRetriever(
    selector=PydanticSingleSelector.from_defaults(llm=llm),
    retriever_tools=[
        vector_tool,
        keyword_tool,
    ],
)
```

## Seçiciyi Bağımsız Bir Modül Olarak Kullanma

Seçicileri bağımsız modüller olarak kullanabilirsiniz. Seçenekleri bir `ToolMetadata` listesi veya bir dize (string) listesi olarak tanımlayın.

```python
from llama_index.core.tools import ToolMetadata
from llama_index.core.selectors import LLMSingleSelector


# seçenekleri bir araç meta verisi listesi olarak tanımlayın
choices = [
    ToolMetadata(description="seçenek 1 için açıklama", name="secenek_1"),
    ToolMetadata(description="seçenek 2 için açıklama", name="secenek_2"),
]

# seçenekleri bir dize listesi olarak tanımlayın
choices = [
    "seçenek 1 - seçenek 1 için açıklama",
    "seçenek 2: seçenek 2 için açıklama",
]

selector = LLMSingleSelector.from_defaults()
selector_result = selector.select(
    choices, query="IBM'in 2007'deki gelir artışı nedir?"
)
print(selector_result.selections)
```

Daha fazla örnek:

-   [Yönlendirici Sorgu Motoru](/python/examples/query_engine/routerqueryengine)
-   [Retriever Yönlendirici Sorgu Motoru](/python/examples/query_engine/retrieverrouterqueryengine)
-   [SQL Yönlendirici Sorgu Motoru](/python/examples/query_engine/sqlrouterqueryengine)
-   [Yönlendirici Retriever](/python/examples/retrievers/router_retriever)