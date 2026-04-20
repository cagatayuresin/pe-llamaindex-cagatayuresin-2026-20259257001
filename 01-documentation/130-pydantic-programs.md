# Pydantic Programları (Pydantic Programs)

<Aside type="tip">
  Pydantic Programları, yapılandırılmış çıktı çıkarma (extraction) için daha düşük seviyeli bir soyutlamadır. Yapılandırılmış çıktı çıkarma işlemini gerçekleştirmenin varsayılan yolu, bu LLM'leri daha üst düzey iş akışlarına kolayca bağlamanıza olanak tanıyan LLM sınıflarımızdır. [Yapılandırılmış veri çıkarma eğitimimize](/python/understanding/extraction) göz atın.
</Aside>

Bir Pydantic programı, bir girdi dizesini alan ve onu yapılandırılmış bir Pydantic nesne türüne dönüştüren genel bir soyutlamadır.

Bu soyutlama çok genel olduğu için geniş bir LLM iş akışı yelpazesini kapsar. Programlar birleştirilebilir (composable) özelliktedir ve daha genel veya özel kullanım durumları için olabilirler.

Birkaç genel Pydantic Programı türü vardır:

-   **Metin Tamamlama Pydantic Programları**: Bunlar, bir metin tamamlama API'si + çıktı ayrıştırma (output parsing) aracılığıyla girdi metnini kullanıcı tarafından belirtilen yapılandırılmış bir nesneye dönüştürür.
-   **Fonksiyon Çağırma Pydantic Programları**: Bunlar, bir LLM fonksiyon çağırma (function calling) API'si aracılığıyla girdi metnini kullanıcı tarafından belirtilen yapılandırılmış bir nesneye dönüştürür.
-   **Önceden Paketlenmiş Pydantic Programlar**: Bunlar, girdi metnini önceden belirlenmiş yapılandırılmış nesnelere dönüştürür.

## Metin Tamamlama Pydantic Programları (Text Completion Pydantic Programs)

[LLM Metin Tamamlama programları](/python/examples/output_parsing/llm_program) hakkındaki örnek not defterine bakın.

## Fonksiyon Çağırma Pydantic Programları (Function Calling Pydantic Programs)

-   [Fonksiyon Çağırma Pydantic Programı](/python/examples/output_parsing/function_program)
-   [OpenAI Pydantic Programı](/python/examples/output_parsing/openai_pydantic_program)
-   [Guidance Pydantic Programı](/python/examples/output_parsing/guidance_pydantic_program)
-   [Guidance Alt Soru Üreticisi (Sub-Question Generator)](/python/examples/output_parsing/guidance_sub_question)

## Önceden Paketlenmiş Pydantic Programlar (Prepackaged Pydantic Programs)

-   [DF Programı](/python/examples/output_parsing/df_program)
-   [Evaporate Programı](/python/examples/output_parsing/evaporate_program)