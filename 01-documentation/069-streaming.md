# Akış (Streaming)

LlamaIndex, yanıtın oluşturulurken akış şeklinde (streaming) alınmasını destekler. Bu, yanıtın tamamı bitmeden önce yanıtın başlangıcını yazdırmaya veya işlemeye başlamanıza olanak tanır. Bu özellik, sorguların algılanan gecikmesini (latency) önemli ölçüde azaltabilir.

### Kurulum

Akışı etkinleştirmek için, akışı destekleyen bir LLM kullanmanız gerekir. Şu anda akış; `OpenAI`, `HuggingFaceLLM` ve çoğu LangChain LLM'si (`LangChainLLM` aracılığıyla) tarafından desteklenmektedir.

> Not: Seçtiğiniz LLM tarafından akış desteklenmiyorsa bir `NotImplementedError` hatası fırlatılacaktır.

Üst düzey API'yi kullanarak sorgu motorunu akış kullanacak şekilde yapılandırmak için, sorgu motorunu oluştururken `streaming=True` olarak ayarlayın.

```python
query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
```

Sorgu motorunu oluşturmak için düşük düzey API kullanıyorsanız, `Response Synthesizer`'ı oluştururken `streaming=True` değerini geçirin:

```python
from llama_index.core import get_response_synthesizer

synth = get_response_synthesizer(streaming=True, ...)
query_engine = RetrieverQueryEngine(response_synthesizer=synth, ...)
```

### Akış Yanıtı (Streaming Response)

Hem LLM hem de sorgu motoru düzgün şekilde yapılandırıldıktan sonra, `query` çağrısı artık bir `StreamingResponse` nesnesi döndürür.

```python
streaming_response = query_engine.query(
    "Yazar büyürken ne yaptı?",
)
```

Yanıt, tam tamamlanmayı beklemeden LLM çağrısı _başladığında_ hemen döndürülür.

> Not: Sorgu motorunun birden fazla LLM çağrısı yaptığı durumlarda, yalnızca son LLM çağrısı akışla iletilecek ve yanıt son LLM çağrısı başladığında döndürülecektir.

Akış yanıtından bir `Generator` (Üreteç) elde edebilir ve gelen tokenler üzerinde döngü kurabilirsiniz:

```python
for text in streaming_response.response_gen:
    # gelen metinle bir şeyler yapın.
    pass
```

Alternatif olarak, metni sadece geldikçe yazdırmak istiyorsanız:

```python
streaming_response.print_response_stream()
```

Uçtan uca bir [örneğe](/python/examples/customization/streaming/simpleindexdemo-streaming) göz atın.