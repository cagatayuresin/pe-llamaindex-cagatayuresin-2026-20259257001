# TruLens ile Değerlendirme ve İzleme

Bu sayfa, LlamaIndex üzerinde inşa edilen LLM uygulamalarını değerlendirmek ve izlemek için [TruLens](https://trulens.org)'in nasıl kullanılacağını kapsar.

## TruLens Nedir?

TruLens, büyük dil modeli (LLM) tabanlı uygulamalar için araçlandırma ve değerlendirme araçları sağlayan [açık kaynaklı](https://github.com/truera/trulens) bir pakettir. Bu; uygunluk, duygu ve daha fazlasına dair geri bildirim fonksiyonu değerlendirmelerinin yanı sıra maliyet ve gecikme süresini içeren derinlemesine izlemeyi (tracing) içerir.

![TruLens Mimarisi](https://www.trulens.org/Assets/image/TruLens_Architecture.png)

LLM uygulamanızın yeni sürümleri üzerinde yineleme yaptıkça, kurduğunuz tüm farklı kalite metrikleri genelinde performanslarını karşılaştırabilirsiniz. Ayrıca değerlendirmeleri kayıt bazında görüntüleyebilir ve her kayıt için uygulama meta verilerini inceleyebilirsiniz.

### Kurulum ve Kurulum (Installation and Setup)

TruLens eklemek basittir, sadece pypi'den yükleyin!

```bash
pip install trulens-eval
```

```python
from trulens_eval import TruLlama
```

## Deneyin!

[llama_index_quickstart.ipynb](https://github.com/truera/trulens/blob/trulens-eval-0.20.3/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb)

[![Colab'da Aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/truera/trulens/blob/main/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb)

## Daha fazlasını oku

-   [LlamaIndex ve TruLens ile LLM Uygulamaları Oluşturun ve Değerlendirin](https://medium.com/llamaindex-blog/build-and-evaluate-llm-apps-with-llamaindex-and-trulens-6749e030d83c)
-   [Daha fazla örnek](https://github.com/truera/trulens/tree/main/trulens_eval/examples/expositional/frameworks/llama_index)
-   [trulens.org](https://www.trulens.org/)