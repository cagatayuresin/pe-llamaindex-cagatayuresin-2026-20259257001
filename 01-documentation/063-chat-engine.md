# Sohbet Motoru (Chat Engine)

## Kavram

Sohbet motoru, verilerinizle bir diyalog kurmak için (tek bir soru ve cevap yerine birden fazla karşılıklı etkileşim) üst düzey bir arayüzdür. Kendi bilgi tabanınızla zenginleştirilmiş ChatGPT gibi düşünebilirsiniz.

Kavramsal olarak, bir [Sorgu Motorunun (Query Engine)](/python/framework/module_guides/deploying/query_engine) **durum bilgisi koruyan (stateful)** benzeridir. Sohbet geçmişini takip ederek, geçmiş bağlamı göz önünde bulundurarak soruları yanıtlayabilir.

> **İpucu:** Verileriniz üzerinden bağımsız bir soru sormak istiyorsanız (yani sohbet geçmişini takip etmeden), bunun yerine [Sorgu Motorunu (Query Engine)](/python/framework/module_guides/deploying/query_engine) kullanın.

## Kullanım Kalıbı (Usage Pattern)

Şununla başlayın:

```python
chat_engine = index.as_chat_engine()
response = chat_engine.chat("Bana bir fıkra anlat.")
```

Yanıtı akış (stream) şeklinde almak için:

```python
chat_engine = index.as_chat_engine()
streaming_response = chat_engine.stream_chat("Bana bir fıkra anlat.")
for token in streaming_response.response_gen:
    print(token, end="")
```

Daha fazla ayrıntıyı tam [kullanım kalıbı kılavuzunda](/python/framework/module_guides/deploying/chat_engines/usage_pattern) bulabilirsiniz.

## Modüller

[Modüller bölümümüzde](/python/framework/module_guides/deploying/chat_engines/modules), mevcut sohbet motorlarını iş başında görmek için ilgili eğitimleri bulabilirsiniz.