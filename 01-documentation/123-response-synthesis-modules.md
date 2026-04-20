# Yanıt Sentezi Modülleri (Response Synthesis Modules)

Her bir yanıt sentezleyici için ayrıntılı girdi/çıktı bilgileri aşağıda yer almaktadır.

## API Örneği (API Example)

Aşağıdakiler, tüm anahtar kelime argümanlarını (kwargs) kullanan kurulumu göstermektedir.

-   `response_mode`: Hangi yanıt sentezleyicinin kullanılacağını belirtir.
-   `service_context`: Sentezleme için LLM ve ilgili ayarları tanımlar.
-   `text_qa_template` ve `refine_template`: Çeşitli aşamalarda kullanılan istemlerdir.
-   `use_async`: Şu anda sadece `tree_summarize` yanıt modu için, özet ağacını asenkron olarak oluşturmak üzere kullanılır.
-   `streaming`: Bir akış (streaming) yanıt nesnesi döndürülüp döndürülmeyeceğini yapılandırır.
-   `structured_answer_filtering`: Belirli bir soruyla ilgili olmayan metin parçalarının aktif olarak filtrelenmesini sağlar.

`synthesize`/`asynthesize` fonksiyonlarında, isteğe bağlı olarak `response.source_nodes` listesine eklenecek ek kaynak node'lar sağlayabilirsiniz.

```python
from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore
from llama_index.core import get_response_synthesizer

response_synthesizer = get_response_synthesizer(
    response_mode="refine",
    service_context=service_context,
    text_qa_template=text_qa_template,
    refine_template=refine_template,
    use_async=False,
    streaming=False,
)

# senkron
response = response_synthesizer.synthesize(
    "sorgu metni",
    nodes=[NodeWithScore(node=Node(text="metin"), score=1.0), ...],
    additional_source_nodes=[
        NodeWithScore(node=Node(text="metin"), score=1.0),
        ...,
    ],
)

# asenkron
response = await response_synthesizer.asynthesize(
    "sorgu metni",
    nodes=[NodeWithScore(node=Node(text="metin"), score=1.0), ...],
    additional_source_nodes=[
        NodeWithScore(node=Node(text="metin"), score=1.0),
        ...,
    ],
)
```

Ayrıca, daha düşük seviyeli `get_response` ve `aget_response` fonksiyonlarını kullanarak doğrudan bir dize (string) döndürebilirsiniz.

```python
response_str = response_synthesizer.get_response(
    "sorgu metni", text_chunks=["metin1", "metin2", ...]
)
```

## Örnek Not Defterleri

-   [İyileştirme (Refine)](/python/examples/response_synthesizers/refine)
-   [Yapılandırılmış İyileştirme (Structured Refine)](/python/examples/response_synthesizers/structured_refine)
-   [Ağaç Özetleme (Tree Summarize)](/python/examples/response_synthesizers/tree_summarize)
-   [Özel İstemleme (Custom Prompting)](/python/examples/response_synthesizers/custom_prompt_synthesizer)