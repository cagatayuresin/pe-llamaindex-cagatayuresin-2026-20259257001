# Geri Aramalar (Callbacks)

## Kavram

LlamaIndex, kütüphanenin dahili işleyişini hata ayıklamanıza, takip etmenize ve izlemenize yardımcı olmak için geri aramalar (callbacks) sağlar.
Geri arama yöneticisi (callback manager) kullanılarak, ihtiyaç duyulduğu kadar geri arama eklenebilir.

Olaylarla ilgili verileri günlüklemeye (logging) ek olarak, her bir olayın süresini ve oluşma sayısını da takip edebilirsiniz.

Ayrıca, olayların bir iz haritası (trace map) da kaydedilir ve geri aramalar bu verileri istedikleri gibi kullanabilirler. Örneğin, `LlamaDebugHandler`, çoğu işlemden sonra varsayılan olarak olayların izini yazdıracaktır.

**Geri Arama Olay Türleri**
Her geri arama her olay türünden yararlanmasa da, aşağıdaki olaylar takip edilebilir durumdadır:

-   `CHUNKING`: Metin bölme işleminin öncesi ve sonrası için günlükler.
-   `NODE_PARSING`: Dökümanlar ve bunların ayrıştırıldığı node'lar için günlükler.
-   `EMBEDDING`: Embed edilen metin sayısı için günlükler.
-   `LLM`: LLM çağrılarının şablonu (template) ve yanıtı için günlükler.
-   `QUERY`: Her sorgunun başlangıcını ve bitişini takip eder.
-   `RETRIEVE`: Bir sorgu için getirilen (retrieved) node'lar için günlükler.
-   `SYNTHESIZE`: Sentezleme (synthesize) çağrılarının sonuçları için günlükler.
-   `TREE`: Oluşturulan özetler ve özet seviyeleri için günlükler.
-   `SUB_QUESTION`: Oluşturulan alt soru ve yanıt için günlükler.

Bu olayları takip etmek ve izlemek için kendi geri aramanızı uygulayabilir veya mevcut bir geri aramayı kullanabilirsiniz.

## Modüller

Şu anda desteklenen geri aramalar şunlardır:

-   [TokenCountingHandler](/python/examples/observability/tokencountinghandler): İstem (prompt), tamamlama (completion) ve embedding token kullanımı için esnek token sayımı. [Migrasyon detaylarına](/python/framework/module_guides/observability/callbacks/token_counting_migration) göz atın.
-   [LlamaDebugHandler](/python/examples/observability/llamadebughandler): Olaylar için temel takip ve izleme. Örnek kullanım aşağıdaki not defterinde bulunabilir.
-   [WandbCallbackHandler](/python/examples/observability/wandbcallbackhandler): Wandb Prompts ön yüzünü kullanarak olayların ve izlerin takibi. Daha fazla detay aşağıdaki not defterinde veya [Wandb](https://docs.wandb.ai/guides/prompts/quickstart) sayfasında mevcuttur.
-   [AimCallback](/python/examples/observability/aimcallback): LLM giriş ve çıkışlarının takibi. Örnek kullanım aşağıdaki not defterinde bulunabilir.
-   [OpenInferenceCallbackHandler](/python/examples/observability/openinferencecallback): AI model çıkarımlarının (inferences) takibi. Örnek kullanım aşağıdaki not defterinde bulunabilir.
-   [OpenAIFineTuningHandler](https://github.com/jerryjliu/llama_index/blob/main/experimental/openai_fine_tuning/openai_fine_tuning.ipynb): Tüm LLM giriş ve çıkışlarını kaydeder. Ardından, giriş ve çıkışları OpenAI ile ince ayar (fine-tuning) yapmaya uygun bir formatta kaydetmek için `save_finetuning_events()` fonksiyonunu sunar.