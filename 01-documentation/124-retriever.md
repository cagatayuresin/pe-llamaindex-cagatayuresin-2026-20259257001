# Retriever

## Kavram

Retriever'lar, kullanıcı sorgusuna (veya sohbet mesajına) göre en alakalı bağlamı getirmekten sorumludur.

[İndekslerin](/python/indexing) üzerine inşa edilebilirler, ancak bağımsız olarak da tanımlanabilirler. İlgili bağlamı getirmek için [sorgu motorlarında](/python/deploying/query_engine) (ve [sohbet motorlarında](/python/deploying/chat_engines)) temel bir yapı taşı olarak kullanılırlar.

<Aside type="tip">
  Retriever'ın RAG iş akışında nereye oturduğu konusunda kafanız mı karıştı?
  [Üst düzey kavramlar](/python/getting_started/concepts) dökümanını okuyun.
</Aside>

## Kullanım Kalıbı (Usage Pattern)

Şununla başlayın:

```python
retriever = index.as_retriever()
nodes = retriever.retrieve("Paul Graham kimdir?")
```

## Başlarken

İndeksten bir retriever alın:

```python
retriever = index.as_retriever()
```

Bir soru için ilgili bağlamı getirin:

```python
nodes = retriever.retrieve("Paul Graham kimdir?")
```

> Not: İndeks oluşturmayı öğrenmek için [İndeksleme](/python/indexing) dökümanına bakın.

## Üst Seviye API (High-Level API)

### Bir Retriever Seçme

`retriever_mode` aracılığıyla indekse özel retriever sınıfını seçebilirsiniz.
Örneğin bir `SummaryIndex` ile:

```python
retriever = summary_index.as_retriever(
    retriever_mode="llm",
)
```

Bu, summary index üzerinde bir [SummaryIndexLLMRetriever](/python/framework-api-reference/retrievers/summary) oluşturur.

(İndekse özel) retriever modlarının tam listesi ve eşleştikleri retriever sınıfları için [**Retriever Modları**](/python/framework/module_guides/querying/retriever/retriever_modes) dökümanına bakın.

### Bir Retriever'ı Yapılandırma

Aynı şekilde, seçilen retriever'ı yapılandırmak için anahtar kelime argümanları (kwargs) geçirebilirsiniz.

> Not: Geçerli kwargs listesi için seçilen retriever sınıfının kurucu (constructor) parametrelerine API referansından göz atın.

Örneğin, "llm" retriever modunu seçtiysek aşağıdakini yapabiliriz:

```python
retriever = summary_index.as_retriever(
    retriever_mode="llm",
    choice_batch_size=5,
)
```

## Düşük Seviye Bileşim (Composition) API'si

Daha ince ayarlı (granular) bir kontrole ihtiyacınız varsa düşük seviyeli bileşim API'sini kullanabilirsiniz.

Yukarıdakiyle aynı sonucu elde etmek için istenen retriever sınıfını doğrudan içe aktarabilir ve oluşturabilirsiniz:

```python
from llama_index.core.retrievers import SummaryIndexLLMRetriever

retriever = SummaryIndexLLMRetriever(
    index=summary_index,
    choice_batch_size=5,
)
```

## Örnekler

Daha fazla örnek için [retriever kılavuzuna](/python/framework/module_guides/querying/retriever/retrievers) bakın.