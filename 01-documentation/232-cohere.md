# Cohere

## Temel Kullanım

#### Bir istemle `complete` çağrısı yapın

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.


```python
%pip install llama-index-llms-openai
%pip install llama-index-llms-cohere
```


```python
!pip install llama-index
```


```python
from llama_index.llms.cohere import Cohere

api_key = "API anahtarınız"
resp = Cohere(api_key=api_key).complete("Paul Graham bir ")
```

    Metninizde sonda bir boşluk var; bu boşluk, yüksek kaliteli üretimler sağlamak için kırpıldı.



```python
print(resp)
```

    İngiliz bir bilgisayar bilimcisi, girişimci ve yatırımcıdır. En çok tohum hızlandırıcısı Y Combinator'ın kurucu ortaklarından biri olarak yaptığı çalışmalarla tanınır. Ayrıca ücretsiz startup tavsiye bloğu "Startups.com"un yazarıdır. Paul Graham hayırseverlik çabalarıyla da bilinir. İyi amaçlar için yüz milyonlarca dolar bağışlamıştır.


#### Bir mesaj listesiyle `chat` çağrısı yapın


```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.cohere import Cohere

messages = [
    ChatMessage(role="user", content="merhaba"),
    ChatMessage(
        role="assistant", content="Arrrr, ahbap! Bugün sana nasıl yardımcı olabilirim?"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]

resp = Cohere(api_key=api_key).chat(
    messages, preamble_override="Renkli bir kişiliğe sahip bir korsansın"
)
```


```python
print(resp)
```

    assistant: Geleneksel olarak ye (siz), her cinsiyetten cinsiyet uyumsuz insanlara ve cinsiyetsiz olanlara hitap ederken; matey (ahbap), bir arkadaşa, genellikle bir korsan arkadaşa hitap etmek için kullanılır. Popüler kültürde "Karayip Korsanları" gibi eserlerde, Jack Sparrow'un romantik ilgisi kendisinden cinsiyetsiz "ye" zamirini kullanarak bahseder.
    
    Korsan kültürü hakkında daha fazla bilgi edinmek ister misin?


## Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma


```python
from llama_index.llms.cohere import Cohere

llm = Cohere(api_key=api_key)
resp = llm.stream_complete("Paul Graham bir ")
```


```python
for r in resp:
    print(r.delta, end="")
```

     İngiliz bir bilgisayar bilimcisi, deneme yazarı ve risk sermayedaridir. En çok bir girişim hızlandırıcısı olan Y Combinator'ın kurucu ortaklarından biri olarak yaptığı çalışmalarla ve girişim topluluğunda yaygın olarak okunan ve etkili olan denemeleriyle tanınır.

`stream_chat` bitiş noktasını kullanma


```python
from llama_index.llms.openai import OpenAI

llm = Cohere(api_key=api_key)
messages = [
    ChatMessage(role="user", content="merhaba"),
    ChatMessage(
        role="assistant", content="Arrrr, ahbap! Bugün sana nasıl yardımcı olabilirim?"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.stream_chat(
    messages, preamble_override="Renkli bir kişiliğe sahip bir korsansın"
)
```


```python
for r in resp:
    print(r.delta, end="")
```

    Arrrr, ahbap! Görgü kurallarına göre önce isimlerimizi paylaşmamız gerekir! Benimki şimdilik bir sır olarak kalsın.

## Modeli Yapılandırma


```python
from llama_index.llms.cohere import Cohere

llm = Cohere(model="command", api_key=api_key)
```


```python
resp = llm.complete("Paul Graham bir ")
```

    Metninizde sonda bir boşluk var; bu boşluk, yüksek kaliteli üretimler sağlamak için kırpıldı.



```python
print(resp)
```

    İngiliz bir bilgisayar bilimcisi, girişimci ve yatırımcıdır. En çok tohum hızlandırıcısı Y Combinator'ın kurucu ortaklarından biri olarak yaptığı çalışmalarla tanınır. Ayrıca çevrimiçi arkadaşlık platformu Match.com'un kurucu ortağıdır.


## Asenkron (Async)


```python
from llama_index.llms.cohere import Cohere

llm = Cohere(model="command", api_key=api_key)
```


```python
resp = await llm.acomplete("Paul Graham bir ")
```

    Metninizde sonda bir boşluk var; bu boşluk, yüksek kaliteli üretimler sağlamak için kırpıldı.



```python
print(resp)
```

    İngiliz bir bilgisayar bilimcisi, girişimci ve yatırımcıdır. En çok bir girişim hızlandırıcısı ve tohum fonu olan Y Combinator'ın ve programlama dili Lisp'in kurucu ortaklarından biri olarak yaptığı çalışmalarla tanınır. Ayrıca, birçoğu yazılım mühendisliği alanında oldukça etkili olan çok sayıda deneme yazmıştır.



```python
resp = await llm.astream_complete("Paul Graham bir ")
```


```python
async for delta in resp:
    print(delta.delta, end="")
```

     İngiliz bir bilgisayar bilimcisi, deneme yazarı ve iş adamıdır. En çok girişim hızlandırıcısı Y Combinator'ın kurucu ortaklarından biri olarak yaptığı çalışmalarıyla ve "Ortalamaları Alt Etmek (Beating the Averages)" adlı denemesiyle tanınır.

## Örnek düzeyinde API Anahtarını Ayarlayın
İstenirse, ayrı LLM örneklerinin ayrı API anahtarları kullanmasını sağlayabilirsiniz.


```python
from llama_index.llms.cohere import Cohere

llm_good = Cohere(api_key=api_key)
llm_bad = Cohere(model="command", api_key="HATALI_ANAHTAR")

resp = llm_good.complete("Paul Graham bir ")
print(resp)

resp = llm_bad.complete("Paul Graham bir ")
print(resp)
```

    Metninizde sonda bir boşluk var; bu boşluk, yüksek kaliteli üretimler sağlamak için kırpıldı.


    İngiliz bir bilgisayar bilimcisi, girişimci ve yatırımcıdır. En çok hızlandırma programı Y Combinator'ın kurucu ortaklarından biri olarak yaptığı çalışmalarla tanınır. Ayrıca bilgisayar bilimleri ve girişimcilik konularında kapsamlı yazılar yazmıştır. İsmiyle nerede karşılaştınız? 



    ---------------------------------------------------------------------------

    CohereAPIError                            Traceback (most recent call last)

    Cell In[17], line 9
          6 resp = llm_good.complete("Paul Graham bir ")
          7 print(resp)
    ----> 9 resp = llm_bad.complete("Paul Graham bir ")
         10 print(resp)


    File /workspaces/llama_index/gllama_index/llms/base.py:277, in llm_completion_callback.<locals>.wrap.<locals>.wrapped_llm_predict(_self, *args, **kwargs)
        267 with wrapper_logic(_self) as callback_manager:
        268     event_id = callback_manager.on_event_start(
        269         CBEventType.LLM,
        270         payload={
       (...)
        274         },
        275     )
    --> 277     f_return_val = f(_self, *args, **kwargs)
        278     if isinstance(f_return_val, Generator):
        279         # intercept the generator and add a callback to the end
        280         def wrapped_gen() -> CompletionResponseGen:


    File /workspaces/llama_index/gllama_index/llms/cohere.py:139, in Cohere.complete(self, prompt, **kwargs)
        136 @llm_completion_callback()
        137 def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        138     all_kwargs = self._get_all_kwargs(**kwargs)
    --> 139     response = completion_with_retry(
        140         client=self._client,
        141         max_retries=self.max_retries,
        142         chat=False,
        143         prompt=prompt,
        144         **all_kwargs
        145     )
        147     return CompletionResponse(
        148         text=response.generations[0].text,
        149         raw=response.__dict__,
        150     )


    File /workspaces/llama_index/gllama_index/llms/cohere_utils.py:74, in completion_with_retry(client, max_retries, chat, **kwargs)
         71     else:
         72         return client.generate(**kwargs)
    ---> 74     return _completion_with_retry(**kwargs)


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:289, in BaseRetrying.wraps.<locals>.wrapped_f(*args, **kw)
        287 @functools.wraps(f)
        288 def wrapped_f(*args: t.Any, **kw: t.Any) -> t.Any:
    --> 289     return self(f, *args, **kw)


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:379, in Retrying.__call__(self, fn, *args, **kwargs)
        377 retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)
        378 while True:
    --> 379     do = self.iter(retry_state=retry_state)
        380     if isinstance(do, DoAttempt):
        381         try:


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:314, in BaseRetrying.iter(self, retry_state)
        312 is_explicit_retry = fut.failed and isinstance(fut.exception(), TryAgain)
        313 if not (is_explicit_retry or self.retry(retry_state)):
    --> 314     return fut.result()
        316 if self.after is not None:
        317     self.after(retry_state)


    File /usr/lib/python3.10/concurrent/futures/_base.py:449, in Future.result(self, timeout)
        447     raise CancelledError()
        448 elif self._state == FINISHED:
    --> 449     return self.__get_result()
        451 self._condition.wait(timeout)
        453 if self._state in [CANCELLED, CANCELLED_AND_NOTIFIED]:


    File /usr/lib/python3.10/concurrent/futures/_base.py:401, in Future.__get_result(self)
        399 if self._exception:
        400     try:
    --> 401         raise self._exception
        402     finally:
        403         # Break a reference cycle with the exception in self._exception
        404         self = None


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:382, in Retrying.__call__(self, fn, *args, **kwargs)
        380 if isinstance(do, DoAttempt):
        381     try:
    --> 382         result = fn(*args, **kwargs)
        383     except BaseException:  # noqa: B902
        384         retry_state.set_exception(sys.exc_info())  # type: ignore[arg-type]


    File /workspaces/llama_index/gllama_index/llms/cohere_utils.py:72, in completion_with_retry.<locals>._completion_with_retry(**kwargs)
         70     return client.chat(**kwargs)
         71 else:
    ---> 72     return client.generate(**kwargs)


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/cohere/client.py:221, in Client.generate(self, prompt, prompt_vars, model, preset, num_generations, max_tokens, temperature, k, p, frequency_penalty, presence_penalty, end_sequences, stop_sequences, return_likelihoods, truncate, logit_bias, stream)
        164 """Generate endpoint.
        165 See https://docs.cohere.ai/reference/generate for advanced arguments
        166 
       (...)
        200         >>>     print(token)
        201 """
        202 json_body = {
        203     "model": model,
        204     "prompt": prompt,
       (...)
        219     "stream": stream,
        220 }
    --> 221 response = self._request(cohere.GENERATE_URL, json=json_body, stream=stream)
        222 if stream:
        223     return StreamingGenerations(response)


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/cohere/client.py:927, in Client._request(self, endpoint, json, files, method, stream, params)
        924     except jsonlib.decoder.JSONDecodeError:  # CohereAPIError will capture status
        925         raise CohereAPIError.from_response(response, message=f"Failed to decode json body: {response.text}")
    --> 927     self._check_response(json_response, response.headers, response.status_code)
        928 return json_response


    File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/cohere/client.py:869, in Client._check_response(self, json_response, headers, status_code)
        867     logger.warning(headers["X-API-Warning"])
        868 if "message" in json_response:  # has errors
    --> 869     raise CohereAPIError(
        870         message=json_response["message"],
        871         http_status=status_code,
        872         headers=headers,
        873     )
        874 if 400 <= status_code < 500:
        875     raise CohereAPIError(
        876         message=f"Unexpected client error (status {status_code}): {json_response}",
        877         http_status=status_code,
        878         headers=headers,
        879     )


    CohereAPIError: geçersiz api belirteci