# Graphsignal ile İzleme (Tracing)

[Graphsignal](https://graphsignal.com/), AI ajanları ve LLM destekli uygulamalar için gözlemlenebilirlik sağlar. Geliştiricilerin AI uygulamalarının beklendiği gibi çalıştığından ve kullanıcıların en iyi deneyimi yaşadığından emin olmalarına yardımcı olur.

Graphsignal, LlamaIndex'i **otomatik olarak** izler ve denetler. İzler (traces) ve metrikler; sorgulama, erişim ve indeksleme işlemleri için yürütme ayrıntıları sağlar. Bu içgörüler; **istemleri (prompts)**, **tamamlamaları (completions)**, **embedding istatistiklerini**, **erişilen node'ları**, **parametreleri**, **gecikme süresini (latency)** ve **istisnaları (exceptions)** içerir.

OpenAI API'leri kullanıldığında Graphsignal; dağıtım, model veya herhangi bir bağlam başına **belirteç sayıları (token counts)** ve **maliyetler** gibi ek içgörüler sağlar.

### Kurulum ve Kurulum (Installation and Setup)

[Graphsignal izleyicisini (tracer)](https://github.com/graphsignal/graphsignal-python) eklemek basittir; sadece kurun ve yapılandırın:

```sh
pip install graphsignal
```

```python
import graphsignal

# Doğrudan veya GRAPHSIGNAL_API_KEY çevre değişkeni aracılığıyla bir API anahtarı sağlayın
graphsignal.configure(
    api_key="my-api-key", deployment="my-llama-index-app-prod"
)
```

API anahtarını [buradan](https://app.graphsignal.com/) alabilirsiniz.

Daha fazla bilgi için [Hızlı Başlangıç kılavuzuna](https://graphsignal.com/docs/guides/quick-start/), [Entegrasyon kılavuzuna](https://graphsignal.com/docs/integrations/llama-index/) ve [örnek bir uygulamaya](https://github.com/graphsignal/examples/blob/main/llama-index-app/main.py) bakın.

### Diğer Fonksiyonları İzleme

Herhangi bir fonksiyonu veya kodu ek olarak izlemek için bir dekoratör (decorator) veya bir bağlam yöneticisi (context manager) kullanabilirsiniz:

```python
with graphsignal.start_trace("harici-veri-yukle"):
    reader.load_data()
```

Eksiksiz talimatlar için [Python API Referansına](https://graphsignal.com/docs/reference/python-api/) bakın.

### Yararlı Bağlantılar

-   [LlamaIndex Uygulamalarını İzleme ve Denetleme](https://graphsignal.com/blog/tracing-and-monitoring-llama-index-applications/)
-   [OpenAI API Gecikmesini, Belirteçlerini, Hız Limitlerini ve Daha Fazlasını Denetleme](https://graphsignal.com/blog/monitor-open-ai-api-latency-tokens-rate-limits-and-more/)
-   [OpenAI API Maliyet Takibi: Modele, Dağıtıma ve Bağlama Göre Harcamaları Analiz Etme](https://graphsignal.com/blog/open-ai-api-cost-tracking-analyzing-expenses-by-model-deployment-and-context/)