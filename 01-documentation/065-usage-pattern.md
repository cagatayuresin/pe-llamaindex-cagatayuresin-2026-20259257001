# Kullanım Kalıbı (Usage Pattern)

## Başlarken

İndeksten bir sohbet motoru oluşturun:

```python
chat_engine = index.as_chat_engine()
```

> **İpucu:** İndeks oluşturmayı öğrenmek için [İndeksleme](/python/framework/module_guides/indexing/index_guide) bölümüne bakın.

Verilerinizle bir diyalog kurun:

```python
response = chat_engine.chat("Bana bir fıkra anlat.")
```

Yeni bir görüşmeye başlamak için sohbet geçmişini sıfırlayın:

```python
chat_engine.reset()
```

Etkileşimli bir sohbet REPL'ine girin:

```python
chat_engine.chat_repl()
```

## Bir Sohbet Motorunu Yapılandırma

Sohbet motorunu yapılandırmak, sorgu motorunu yapılandırmaya çok benzer.

### Üst Düzey API (High-Level API)

Tek satır kodla bir indeksten doğrudan bir sohbet motoru oluşturabilir ve yapılandırabilirsiniz:

```python
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
```

> Not: `chat_mode` argümanını belirterek farklı sohbet motorlarına erişebilirsiniz. `condense_question`, `CondenseQuestionChatEngine`'e; `react`, `ReActChatEngine`'e; `context`, `ContextChatEngine`'e karşılık gelir.

> Not: Üst düzey API kullanım kolaylığı için optimize edilmiş olsa da, tüm yapılandırma seçeneklerini _SUNMAZ_.

#### Mevcut Sohbet Modları

-   `best`: LLM'inizin neyi desteklediğine bağlı olarak, bir `ReAct` veri ajanı veya bir `OpenAI` veri ajanıyla kullanılmak üzere sorgu motorunu bir araca dönüştürür. `OpenAI` veri ajanları, OpenAI'ın fonksiyon çağırma API'sini kullandıkları için `gpt-3.5-turbo` veya `gpt-4` gerektirir.
-   `condense_question`: Sohbet geçmişine bakar ve kullanıcı mesajını indeks için bir sorgu olacak şekilde yeniden yazar. Sorgu motorundan gelen yanıtı okuduktan sonra yanıtı döndürür.
-   `context`: Her kullanıcı mesajını kullanarak indeksten node'ları getirir. Getirilen metin sistem istemine (system prompt) eklenir, böylece sohbet motoru ya doğal bir şekilde yanıt verebilir ya da sorgu motorundan gelen bağlamı kullanabilir.
-   `condense_plus_context`: `condense_question` ve `context` kombinasyonudur. Sohbet geçmişine bakar ve kullanıcı mesajını indeks için bir getirme sorgusu olacak şekilde yeniden yazar. Getirilen metin sistem istemine eklenir, böylece sohbet motoru ya doğal bir şekilde yanıt verebilir ya da sorgu motorundan gelen bağlamı kullanabilir.
-   `simple`: Doğrudan LLM ile yapılan basit bir sohbet, herhangi bir sorgu motoru dahil değildir.
-   `react`: `best` ile aynıdır, ancak bir `ReAct` veri ajanı kullanmaya zorlar.
-   `openai`: `best` ile aynıdır, ancak bir `OpenAI` veri ajanı kullanmaya zorlar.

### Düşük Düzey Bileşim API'si (Low-Level Composition API)

Daha ince taneli bir kontrole ihtiyacınız varsa düşük düzey bileşim API'sini kullanabilirsiniz. Somut olarak konuşursak, `index.as_chat_engine(...)` çağırmak yerine açıkça `ChatEngine` nesnesi oluşturursunuz.

> Not: API referanslarına veya örnek notebook'lara bakmanız gerekebilir.

Aşağıdakileri yapılandırdığımız bir örnek:

-   Sorgu yoğunlaştırma istemini (condense question prompt) yapılandırın,
-   Görüşmeyi mevcut bir geçmişle başlatın,
-   Ayrıntılı (verbose) hata ayıklama mesajlarını yazdırın.

```python
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.chat_engine import CondenseQuestionChatEngine

custom_prompt = PromptTemplate(
    """\
Bir görüşme (İnsan ve Asistan arasında) ve İnsan'dan gelen bir takip mesajı verildiğinde, \
mesajı görüşmedeki tüm ilgili bağlamı yakalayan bağımsız bir soru olacak şekilde \
yeniden yazın.

<Sohbet Geçmişi>
{chat_history}

<Takip Mesajı>
{question}

<Bağımsız soru>
"""
)

# `ChatMessage` nesnelerinin listesi
custom_chat_history = [
    ChatMessage(
        role=MessageRole.USER,
        content="Merhaba asistan, bugün Paul Graham hakkında ufuk açıcı bir tartışma yapıyoruz.",
    ),
    ChatMessage(role=MessageRole.ASSISTANT, content="Tamam, kulağa hoş geliyor."),
]

query_engine = index.as_query_engine()
chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
    condense_question_prompt=custom_prompt,
    chat_history=custom_chat_history,
    verbose=True,
)
```

### Akış (Streaming)

Akış özelliğini etkinleştirmek için, `chat` uç noktası yerine `stream_chat` uç noktasını çağırmanız yeterlidir.

> **Uyarı:** Bu durum, sorgu motoruyla (burada bir `streaming=True` bayrağı geçirirsiniz) biraz tutarsızdır. Bu davranışı daha tutarlı hale getirmek için çalışıyoruz!

**Senkron (`stream_chat`):**

```python
chat_engine = index.as_chat_engine()
streaming_response = chat_engine.stream_chat("Bana bir fıkra anlat.")

for token in streaming_response.response_gen:
    print(token, end="")
```

**Asenkron (`astream_chat`):**

Asenkron çerçeveler (FastAPI gibi) kullanırken `astream_chat` kullanın. Çağrıyı bekletmeniz (await) ve sağlanan asenkron akış arayüzü (örneğin `async_response_gen()` veya `achat_stream`) üzerinden yineleme yapmanız gerektiğini unutmayın.

```python
chat_engine = index.as_chat_engine()
streaming_response = await chat_engine.astream_chat("Bana bir fıkra anlat.")

async for token in streaming_response.async_response_gen():
    print(token, end="")
```

Uçtan uca bir [eğitime](/python/examples/customization/streaming/chat_engine_condense_question_stream_response) göz atın.