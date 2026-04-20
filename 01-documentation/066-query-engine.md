# Sorgu Motoru (Query Engine)

## Kavram

Sorgu motoru, verileriniz üzerinde soru sormanıza olanak tanıyan genel bir arayüzdür.

Bir sorgu motoru, doğal dilde bir sorgu alır ve zengin bir yanıt döndürür. Çoğu zaman (ancak her zaman değil) [getiriciler (retrievers)](/python/framework/module_guides/querying/retriever) aracılığıyla bir veya daha fazla [indeks](/python/framework/module_guides/indexing) üzerine inşa edilir. Daha gelişmiş yetenekler elde etmek için birden fazla sorgu motorunu birleştirebilirsiniz.

> **İpucu:** Verilerinizle bir diyalog kurmak istiyorsanız (tek bir soru ve cevap yerine birden fazla karşılıklı etkileşim), [Sohbet Motoruna (Chat Engine)](/python/framework/module_guides/deploying/chat_engines) göz atın.

## Kullanım Kalıbı (Usage Pattern)

Şununla başlayın:

```python
query_engine = index.as_query_engine()
response = query_engine.query("Paul Graham kimdir?")
```

Yanıtı akış şeklinde almak için:

```python
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("Paul Graham kimdir?")
streaming_response.print_response_stream()
```

Daha fazla ayrıntı için tam [kullanım kalıbına](/python/framework/module_guides/deploying/query_engine/usage_pattern) bakın.

## Modüller

Tüm modülleri [modül kılavuzunda](/python/framework/module_guides/deploying/query_engine/modules) bulabilirsiniz.

## Destekleyici Modüller

Ayrıca [destekleyici modüller](/python/framework/module_guides/deploying/query_engine/supporting_modules) de mevcuttur.