# Gözlemlenebilirlik (Observability)

LlamaIndex, üretim ortamında ilkeli (principled) LLM uygulamaları oluşturmanıza olanak tanımak için **tek tıkla gözlemlenebilirlik** 🔭 sağlar.

Verileriniz üzerinde geliştirilen LLM uygulamalarının (RAG sistemleri, ajanlar) ilkeli bir şekilde geliştirilmesi için temel gereksinim; hem sistemin tamamını hem de her bir bileşeni gözlemleyebilmek, hata ayıklayabilmek ve değerlendirebilmektir.

Bu özellik, LlamaIndex kütüphanesini ortaklarımızın sunduğu güçlü gözlemlenebilirlik/değerlendirme araçlarıyla sorunsuz bir şekilde entegre etmenize olanak tanır. Bir değişkeni bir kez yapılandırdığınızda, aşağıdakiler gibi işlemleri yapabileceksiniz:

-   LLM/istem (prompt) girişlerini/çıkışlarını görüntüleme
-   Herhangi bir bileşenin (LLM'ler, embedding'ler) çıktılarını beklenen şekilde performans gösterdiğinden emin olma
-   Hem indeksleme hem de sorgulama için çağrı izlerini (call traces) görüntüleme

Her sağlayıcının benzerlikleri ve farklılıkları vardır. Her biri için tam kılavuz setine aşağıdan göz atın!

**NOT:**

Gözlemlenebilirlik artık [`instrumentation` modülü](/python/framework/module_guides/observability/instrumentation) (v0.10.20 ve sonrası sürümlerde mevcuttur) aracılığıyla yönetilmektedir.

Bu sayfada bahsedilen araçların ve entegrasyonların çoğu eski `CallbackManager` yapımızı kullanır veya `set_global_handler` kullanmaz. Bu entegrasyonları buna göre işaretledik!

## Kullanım Kalıbı (Usage Pattern)

Etkinleştirmek için genellikle sadece aşağıdakini yapmanız yeterlidir:

```python
from llama_index.core import set_global_handler

# genel kullanım
set_global_handler("<handler_adi>", **kwargs)
```

`set_global_handler` fonksiyonuna verilen tüm `kwargs` argümanlarının altta yatan geri arama işleyicisine (callback handler) aktarıldığını unutmayın.

İşte bu kadar! Çalıştırma işlemleri sorunsuz bir şekilde ilgili hizmete aktarılacak ve uygulamanızın çalıştırma izlerini görüntüleme gibi özelliklere erişebileceksiniz.

## Entegrasyonlar

### OpenTelemetry

[OpenTelemetry](https://opentelemetry.io), çok sayıda arka uç entegrasyonuna (Jaeger, Zipkin veya Prometheus gibi) sahip, izleme (tracing) ve gözlemlenebilirlik için yaygın olarak kullanılan bir açık kaynak hizmettir.

OpenTelemetry entegrasyonumuz; LLM'ler, Ajanlar, RAG boru hattı bileşenleri ve çok daha fazlası dahil olmak üzere LlamaIndex kodu tarafından üretilen tüm olayları izler: LlamaIndex yerel enstrümantasyonuyla elde edebileceğiniz her şeyi OpenTelemetry formatında dışa aktarabilirsiniz!

Kütüphaneyi şu komutla yükleyebilirsiniz:

```bash
pip install llama-index-observability-otel
```

Ve bir RAG boru hattı içeren bu örnekte olduğu gibi, varsayılan ayarlarla kodunuzda kullanabilirsiniz:

```python
from llama_index.observability.otel import LlamaIndexOpenTelemetry
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# enstrümantasyon nesnesini başlat
instrumentor = LlamaIndexOpenTelemetry()

if __name__ == "__main__":
    embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
    llm = OpenAI(model="gpt-4o-mini")

    # dinlemeye başla!
    instrumentor.start_registering()

    # olayları kaydet
    documents = SimpleDirectoryReader(
        input_dir="./data/paul_graham/"
    ).load_data()

    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    query_engine = index.as_query_engine(llm=llm)

    query_result_one = query_engine.query("Paul kimdir?")
    query_result_two = query_engine.query("Paul ne yaptı?")
```

Veya aşağıdaki örnekte olduğu gibi daha karmaşık ve özelleştirilmiş bir kurulum kullanabilirsiniz:

```python
import json
from pydantic import BaseModel, Field
from typing import List

from llama_index.observability.otel import LlamaIndexOpenTelemetry
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)

# özel bir span (iz parçası) dışa aktarıcı tanımla
span_exporter = OTLPSpanExporter("http://0.0.0.0:4318/v1/traces")

# enstrümantasyon nesnesini başlat
instrumentor = LlamaIndexOpenTelemetry(
    service_name_or_resource="benim.test.servisim.1",
    span_exporter=span_exporter,
    debug=True,
)


if __name__ == "__main__":
    instrumentor.start_registering()
    # ... kodunuz buraya
```

Ayrıca agentic iş akışlarının nasıl izleneceğini ve kayıtlı izlerin bir Postgres veritabanına nasıl aktarılacağını gösterdiğimiz bir [demo depomuz](https://github.com/run-llama/agents-observability-demo) da bulunmaktadır.

### LlamaTrace (Barındırılan Arize Phoenix)

Arize ile, LlamaIndex açık kaynak kullanıcılarıyla yerel olarak çalışan ve LlamaCloud ile entegrasyonları olan barındırılan bir izleme, gözlemlenebilirlik ve değerlendirme platformu olan [LlamaTrace](https://llamatrace.com/) üzerinde ortaklık kurduk.

Bu, açık kaynaklı Arize [Phoenix](https://github.com/Arize-ai/phoenix) projesi üzerine inşa edilmiştir. Phoenix, modellerinizi ve LLM uygulamalarınızı izlemek için "önce not defteri" (notebook-first) bir deneyim sunar:

-   **LLM İzleri (Traces)**: LLM uygulamanızın dahili işleyişini anlamak; getirme (retrieval) ve araç çalıştırma gibi konulardaki sorunları gidermek için uygulamanızın yürütülmesini izleyin.
-   **LLM Değerlendirmeleri (Evals)**: Üretken modelinizin veya uygulamanızın uygunluğunu, toksisitesini ve daha fazlasını değerlendirmek için büyük dil modellerinin gücünden yararlanın.

#### Kullanım Kalıbı

Entegrasyon paketini yüklemek için `pip install -U llama-index-callbacks-arize-phoenix` komutunu kullanın.

Ardından LlamaTrace üzerinde bir hesap oluşturun: https://llamatrace.com/login. Bir API anahtarı oluşturun ve bunu aşağıdaki `PHOENIX_API_KEY` değişkenine yerleştirin.

Ardından aşağıdaki kodu çalıştırın:

```python
# Phoenix, LlamaIndex uygulamanızdan otomatik olarak toplanan izleri 
# gerçek zamanlı olarak görüntüleyebilir.
# Tüm LlamaIndex uygulamalarınızı her zamanki gibi çalıştırın; izler 
# toplanacak ve Phoenix'te görüntülenecektir.

# günlükleme/gözlemlenebilirlik için Arize Phoenix'i kurun
import llama_index.core
import os

PHOENIX_API_KEY = "<PHOENIX_API_KEY>"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
llama_index.core.set_global_handler(
    "arize_phoenix", endpoint="https://llamatrace.com/v1/traces"
)

...
```

#### Kılavuzlar

-   [LlamaTrace ile LlamaCloud Ajanı](https://github.com/run-llama/llamacloud-demo/blob/main/examples/tracing/llamacloud_tracing_phoenix.ipynb)

![](./../../_static/integrations/arize_phoenix.png)

### SigNoz

[SigNoz](https://signoz.io/), açık kaynaklı bir gözlemlenebilirlik çerçevesidir. Yerel olarak OpenTelemetry üzerinden inşa edilmiştir; izleri, günlükleri ve metrikleri tek bir panelde sunar; hem kendi kendine barındırma (self-hosted) hem de bulut dağıtım seçeneklerine sahiptir. LlamaIndex ile SigNoz kullanarak, tüm RAG ve Ajan iş akışlarının ayrıntılı izlerini görüntüleyebilir; token kullanımı, gecikme, hata oranları, LLM model dağılımı ve çok daha fazlası gibi önemli metrikleri takip edebilirsiniz.

#### Kullanım Kalıbı

Aşağıdaki bağımlılıkları yükleyin:

```bash
pip install \
  opentelemetry-distro \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-httpx \
  opentelemetry-instrumentation-system-metrics \
  llama-index \
  openinference-instrumentation-llama-index
```

Ardından, otomatik enstrümantasyonu ekleyin:

```bash
opentelemetry-bootstrap --action=install
```

Sonrasında, LlamaIndex uygulamanızı otomatik enstrümantasyon ile çalıştırın:

```bash
OTEL_RESOURCE_ATTRIBUTES="service.name=<servis_adi>" \
OTEL_EXPORTER_OTLP_ENDPOINT="https://ingest.<bolge>.signoz.cloud:443" \
OTEL_EXPORTER_OTLP_HEADERS="signoz-ingestion-key=<ingestion_anahtariniz>" \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
OTEL_TRACES_EXPORTER=otlp \
OTEL_METRICS_EXPORTER=otlp \
OTEL_LOGS_EXPORTER=otlp \
OTEL_PYTHON_LOG_CORRELATION=true \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
opentelemetry-instrument <calistirma_komutunuz>
```

-   `<servis_adi>` servisinizin adıdır.
-   `<bolge>` kısmını SigNoz Cloud [bölgenizle](https://signoz.io/docs/ingestion/signoz-cloud/overview/#endpoint) eşleşecek şekilde ayarlayın.
-   `<ingestion_anahtariniz>` kısmını SigNoz [ingestion anahtarınızla](https://signoz.io/docs/ingestion/signoz-cloud/keys/) değiştirin.
-   `<calistirma_komutunuz>` kısmını uygulamanızı çalıştırmak için kullanacağınız gerçek komutla değiştirin. Örneğin: `python main.py`

> 📌 Not: Kendi kendine barındırılan (self-hosted) SigNoz mu kullanıyorsunuz? Çoğu adım özdeştir. Bu kılavuzu uyarlamak için, [Bulut → Kendi Kendine Barındırma](https://signoz.io/docs/ingestion/cloud-vs-self-hosted/#cloud-to-self-hosted) kısmında gösterildiği gibi uç noktayı güncelleyin ve ingestion anahtarı başlığını kaldırın.

Artık LlamaIndex uygulamanız tarafından otomatik veya manuel olarak dışa aktarılan tüm izleri, günlükleri ve metrikleri görebileceksiniz.

![SigNoz Ayrıntılı İz Görünümü](https://signoz.io/img/docs/llm/llamaindex/llamaindex-detailed-trace-view.webp)

#### Örnek Kılavuzlar

-   [SigNoz LlamaIndex Entegrasyon Dökümanları](https://signoz.io/docs/llamaindex-observability/)
-   [SigNoz LlamaIndex Soru-Cevap RAG Demosu](https://github.com/SigNoz/llamaindex-rag-opentelemetry-demo)

### Weights and Biases (W&B) Weave

[W&B Weave](https://weave-docs.wandb.ai/), LLM uygulamalarını izlemek, denemek, değerlendirmek, yayına almak ve iyileştirmek için kullanılan bir çerçevedir. Ölçeklenebilirlik ve esneklik için tasarlanan Weave, uygulama geliştirme iş akışınızın her aşamasını destekler.

#### Kullanım Kalıbı

Entegrasyon, span'ları/olayları Weave çağrıları olarak kaydetmek için LlamaIndex'in [`instrumentation` modülünü](/python/framework/module_guides/observability/instrumentation) kullanır. Varsayılan olarak Weave, [yaygın LLM kütüphanelerine ve çerçevelerine](https://weave-docs.wandb.ai/guides/integrations/) yapılan çağrıları otomatik olarak yamalar (patch) ve izler.

`weave` kütüphanesini yükleyin:

```bash
pip install weave
```

Bir W&B API Anahtarı edinin:

Henüz bir W&B hesabınız yoksa, [https://wandb.ai](https://wandb.ai) adresini ziyaret ederek bir tane oluşturun ve API anahtarınızı [https://wandb.ai/authorize](https://wandb.ai/authorize) adresinden kopyalayın. Kimlik doğrulaması istendiğinde API anahtarını girin.

```python
import weave
from llama_index.llms.openai import OpenAI

# Proje adınızla Weave'i başlatın
weave.init("llamaindex-demo")

# Tüm LlamaIndex işlemleri artık otomatik olarak izleniyor
llm = OpenAI(model="gpt-4o-mini")
response = llm.complete("William Shakespeare şöyledir: ")
print(response)
```

![weave başlangıç](./../../_static/integrations/weave/weave_quickstart.png)

İzler; yürütme süresini, token kullanımını, maliyeti, girişleri/çıkışları, hataları, iç içe geçmiş işlemleri ve akış verilerini içerir. Weave izleme konusunda yeniyseniz, nasıl gezinileceği hakkında daha fazlasını [buradan](https://weave-docs.wandb.ai/guides/tracking/trace-tree) öğrenebilirsiniz.

İzlenmeyen özel bir fonksiyonunuz varsa, onu [`@weave.op()`](https://weave-docs.wandb.ai/guides/tracking/ops) ile dekore edin.

`weave.init` içindeki `autopatch_settings` argümanını kullanarak yama davranışını da kontrol edebilirsiniz. Örneğin bir kütüphaneyi/çerçeveyi izlemek istemiyorsanız şu şekilde kapatabilirsiniz:

```python
weave.init(..., autopatch_settings={"openai": {"enabled": False}})
```

Herhangi bir ek LlamaIndex yapılandırması gerekmez; izleme `weave.init()` çağrıldığı anda başlar.

#### Kılavuzlar

LlamaIndex ile entegrasyon, LlamaIndex'in neredeyse her bileşenini (akış/asenkron, tamamlamalar, sohbet, araç çağırma, ajanlar, iş akışları ve RAG desteği) destekler. Resmi [W&B Weave × LlamaIndex](https://weave-docs.wandb.ai/guides/integrations/llamaindex) dökümantasyonunda daha fazlasını öğrenebilirsiniz.

### MLflow

[MLflow](https://mlflow.org/docs/latest/llms/tracing/index.html), makine öğrenimi projeleri için her aşamanın yönetilebilir, izlenebilir ve yeniden üretilebilir olmasını sağlayan, tam yaşam döngüsüne odaklanan açık kaynaklı bir MLOps/LLMOps platformudur.
**MLflow Tracing**, OpenTelemetry tabanlı bir izleme özelliğidir ve LlamaIndex uygulamaları için tek tıkla enstrümantasyonu destekler.

#### Kullanım Kalıbı

MLflow açık kaynaklı olduğu için, herhangi bir hesap oluşturmadan veya API anahtarı kurulumu yapmadan kullanmaya başlayabilirsiniz. MLflow paketini yükledikten sonra doğrudan koda geçin!

```python
import mlflow

mlflow.llama_index.autolog()  # MLflow izlemeyi etkinleştir
```

![](./../../_static/integrations/mlflow/mlflow.gif)

#### Kılavuzlar

MLflow LlamaIndex entegrasyonu ayrıca deney takibi, değerlendirme, bağımlılık yönetimi ve daha fazlasını sunar. Daha fazla detay için [MLflow dökümantasyonuna](https://mlflow.org/docs/latest/llms/llama-index/index.html) göz atın.

#### Destek Tablosu

MLflow Tracing, LlamaIndex özelliklerinin tamamını destekler. [AgentWorkflow](https://www.llamaindex.ai/blog/introducing-agentworkflow-a-powerful-system-for-building-ai-agent-systems) gibi bazı yeni özellikler MLflow >= 2.18.0 gerektirir.

| Akış (Streaming) | Asenkron (Async) | Motor (Engine) | Ajanlar | İş Akışı (Workflow) | AgentWorkflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | ✅ | ✅ | ✅ | ✅ (>= 2.18) | ✅ (>= 2.18) |

### OpenLLMetry

[OpenLLMetry](https://github.com/traceloop/openllmetry), LLM uygulamalarını izlemek için OpenTelemetry tabanlı açık kaynaklı bir objedir. [Tüm büyük gözlemlenebilirlik platformlarına](https://www.traceloop.com/docs/openllmetry/integrations/introduction) bağlanır ve dakikalar içinde kurulur.

#### Kullanım Kalıbı

```python
from traceloop.sdk import Traceloop

Traceloop.init()
```

#### Kılavuzlar

-   [OpenLLMetry](/python/examples/observability/openllmetry)

![](./../../_static/integrations/openllmetry.png)

### Arize Phoenix (yerel)

Açık kaynaklı proje aracılığıyla Phoenix'in **yerel** bir örneğini kullanmayı da seçebilirsiniz.

Bu durumda LlamaTrace'te bir hesap oluşturmanıza veya Phoenix için bir API anahtarı ayarlamanıza gerek yoktur. Phoenix sunucusu yerel olarak başlatılacaktır.

#### Kullanım Kalıbı

Entegrasyon paketini yüklemek için `pip install -U llama-index-callbacks-arize-phoenix` komutunu çalıştırın.

Ardından aşağıdaki kodu çalıştırın:

```python
# Phoenix, LlamaIndex uygulamanızdan otomatik olarak toplanan izleri 
# gerçek zamanlı olarak görüntüleyebilir.
# Tüm LlamaIndex uygulamalarınızı her zamanki gibi çalıştırın; izler 
# toplanacak ve Phoenix'te görüntülenecektir.

import phoenix as px

# Uygulamayı tarayıcıda açmak için çıktıdaki URL'ye bakın.
px.launch_app()
# Uygulama başlangıçta boştur, ancak aşağıdaki adımlarla devam ettikçe, 
# LlamaIndex uygulamanız çalıştıkça izler otomatik olarak görünecektir.

import llama_index.core

llama_index.core.set_global_handler("arize_phoenix")
...
```

#### Örnek Kılavuzlar

-   [Pinecone ve Arize Phoenix ile Otomatik Getirme (Auto-Retrieval) Kılavuzu](https://docs.llamaindex.ai/en/latest/examples/vector_stores/pinecone_auto_retriever/?h=phoenix)
-   [Arize Phoenix İzleme Eğitimi](https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/tracing/llama_index_tracing_tutorial.ipynb)

### Langfuse 🪢

[Langfuse](https://langfuse.com/docs), ekiplerin LLM uygulamaları üzerinde iş birliği içinde hata ayıklamasına, analiz etmesine ve yineleme yapmasına yardımcı olan açık kaynaklı bir LLM mühendislik platformudur. Langfuse entegrasyonu ile LlamaIndex uygulamanızın performansını, izlerini ve metriklerini takip edebilir ve izleyebilirsiniz. Bağlam zenginleştirme (context augmentation) ve LLM sorgulama süreçlerinin ayrıntılı [izleri](https://langfuse.com/docs/tracing) yakalanır ve doğrudan Langfuse kullanıcı arayüzünde incelenebilir.

#### Kullanım Kalıbı

Hem `llama-index` hem de `langfuse` paketlerinin yüklü olduğundan emin olun.

```bash
pip install llama-index langfuse openinference-instrumentation-llama-index
```

Ardından, Langfuse API anahtarlarınızı ayarlayın. Bu anahtarları ücretsiz bir [Langfuse Bulut](https://cloud.langfuse.com/) hesabı oluşturarak veya [kendiniz barındırarak (self-hosting)](https://langfuse.com/self-hosting) alabilirsiniz. Bu ortam değişkenleri, Langfuse istemcisinin kimlik doğrulaması yapması ve Langfuse projenize veri göndermesi için gereklidir.

```python
import os

# Projeniz için anahtarları proje ayarları sayfasından alın: https://cloud.langfuse.com

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # 🇪🇺 AB bölgesi
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 ABD bölgesi
```

Ortam değişkenleri ayarlandıktan sonra Langfuse istemcisini başlatabiliriz. `get_client()`, ortam değişkenlerinde sağlanan kimlik bilgilerini kullanarak Langfuse istemcisini başlatır.

```python
from langfuse import get_client

langfuse = get_client()

# Bağlantıyı doğrula
if langfuse.auth_check():
    print("Langfuse istemcesi doğrulandı ve hazır!")
else:
    print("Kimlik doğrulaması başarısız oldu. Lütfen bilgilerinizi ve host adresini kontrol edin.")
```

Şimdi, [OpenInference LlamaIndex enstrümantasyonunu](https://docs.arize.com/phoenix/tracing/integrations-tracing/llamaindex) başlatıyoruz. Bu üçüncü taraf enstrümantasyon, LlamaIndex işlemlerini otomatik olarak yakalar ve OpenTelemetry (OTel) span'larını Langfuse'a aktarır.

```python
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

# LlamaIndex enstrümantasyonunu başlat
LlamaIndexInstrumentor().instrument()
```

Artık LlamaIndex uygulamanızın günlüklerini Langfuse'da görebilirsiniz:

[LlamaIndex örnek iz](https://langfuse.com/images/cookbook/integration-llamaindex-workflows/llamaindex-trace.gif)

#### Örnek Kılavuzlar

-   [Langfuse Dökümantasyonu](https://langfuse.com/docs/integrations/llama-index/get-started)
-   [LlamaIndex Ajanlarını İzleme](https://langfuse.com/docs/integrations/llama-index/workflows)

### Literal AI

[Literal AI](https://literalai.com/), mühendislik ve ürün ekiplerinin LLM uygulamalarını güvenilir, daha hızlı ve ölçeklenebilir şekilde sunmalarını sağlayan bir LLM değerlendirme ve gözlemlenebilirlik çözümüdür. Bu, istem mühendisliği, LLM gözlemlenebilirliği, LLM değerlendirmesi ve LLM izlemeyi içeren iş birlikçi bir geliştirme döngüsü ile mümkündür. Konuşma Akışları (Threads) ve Ajan Çalıştırmaları Literal AI üzerinde otomatik olarak günlüklenebilir.

Literal AI'yı denemenin en kolay yolu [bulut örneğimize](https://cloud.getliteral.ai/) kaydolmaktır. Ardından **Ayarlar**'a gidip API anahtarınızı alabilir ve günlüklemeye başlayabilirsiniz!

#### Kullanım Kalıbı

-   `pip install literalai` ile Literal AI Python SDK'sını yükleyin.
-   Literal AI projenizde **Ayarlar**'a gidin ve API anahtarınızı alın.
-   Kendi kendine barındırılan bir Literal AI örneği kullanıyorsanız, temel URL'sini de not edin.

Ardından uygulama kodunuza aşağıdaki satırları ekleyin:

```python
from llama_index.core import set_global_handler

# Literal AI API anahtarınızı ve temel URL'nizi aşağıdaki ortam değişkenlerini kullanarak sağlamalısınız:
# LITERAL_API_KEY, LITERAL_API_URL
set_global_handler("literalai")
```

#### Örnek Kılavuzlar

-   [Literal AI ile Llama Index Entegrasyonu](https://docs.getliteral.ai/integrations/llama-index)
-   [LlamaIndex ile bir Soru-Cevap uygulaması oluşturun ve bunu Literal AI ile izleyin](https://github.com/Chainlit/literal-cookbook/blob/main/python/llamaindex-integration)

### Comet Opik

[Opik](https://www.comet.com/docs/opik/?utm_source=llama-index&utm_medium=docs&utm_campaign=opik&utm_content=home_page), Comet tarafından geliştirilen açık kaynaklı uçtan uca bir LLM Değerlendirme Platformudur.

Başlamak için sadece [Comet](https://www.comet.com/signup?from=llm&utm_medium=github&utm_source=llama-index&utm_campaign=opik) üzerinde bir hesap oluşturun ve API anahtarınızı alın.

#### Kullanım Kalıbı

-   `pip install opik` ile Opik Python SDK'sını yükleyin.
-   Opik'te kullanıcı menüsünden API anahtarınızı alın.
-   Kendi kendine barındırılan bir Opik örneği kullanıyorsanız, temel URL'sini de not edin.

[Kendi kendine barındırılan bir örnek](https://www.comet.com/docs/opik/self-host/self_hosting_opik) kullanıyorsanız `OPIK_API_KEY`, `OPIK_WORKSPACE` ve `OPIK_URL_OVERRIDE` ortam değişkenlerini kullanarak Opik'i yapılandırabilirsiniz:

```bash
export OPIK_API_KEY="<OPIK_API_KEY>"
export OPIK_WORKSPACE="<OPIK_WORKSPACE - Genellikle API anahtarınızla aynıdır>"

# İsteğe bağlı
#export OPIK_URL_OVERRIDE="<OPIK_URL_OVERRIDE>"
```

Artık küresel işleyiciyi ayarlayarak Opik entegrasyonunu LlamaIndex ile kullanabilirsiniz:

```python
from llama_index.core import Document, VectorStoreIndex, set_global_handler

# OPIK API anahtarınızı ve Çalışma Alanınızı (Workspace) aşağıdaki ortam değişkenleri ile sağlamalısınız:
# OPIK_API_KEY, OPIK_WORKSPACE
set_global_handler(
    "opik",
)

# Bu örnek varsayılan olarak OpenAI kullanır, bu yüzden bir OPENAI_API_KEY ayarlamayı unutmayın
index = VectorStoreIndex.from_documents([Document.example()])
query_engine = index.as_query_engine()

questions = [
    "Bana LLM'lerden bahset",
    "Bir sinir ağı nasıl ince ayar (fine-tune) yapılır?",
    "RAG nedir?",
]

for question in questions:
    print(f"> \033[92m{question}\033[0m")
    response = query_engine.query(question)
    print(response)
```

Opik'te şu izleri göreceksiniz:

![Opik LlamaIndex Entegrasyonu](./../../_static/integrations/opik.png)

#### Örnek Kılavuzlar

-   [Llama-index + Opik dökümantasyon sayfası](https://www.comet.com/docs/opik/tracing/integrations/llama_index?utm_source=llamaindex&utm_medium=docs&utm_campaign=opik)
-   [Llama-index entegrasyon tarif kitabı (cookbook)](https://www.comet.com/docs/opik/cookbook/llama-index?utm_source=llama-index&utm_medium=docs&utm_campaign=opik)

### Argilla

[Argilla](https://github.com/argilla-io/argilla), projeleri için yüksek kaliteli veri kümeleri oluşturması gereken AI mühendisleri ve alan uzmanları için bir iş birliği aracıdır.

Başlamak için Argilla sunucusunu kurmanız gerekir. Henüz yapmadıysanız, bu [kılavuzu](https://docs.argilla.io/latest/getting_started/quickstart/) izleyerek kolayca kurabilirsiniz.

#### Kullanım Kalıbı

-   `pip install argilla-llama-index` ile Argilla LlamaIndex entegrasyon paketini yükleyin.
-   ArgillaHandler'ı başlatın. `<api_key>` Argilla Alanınızın `My Settings` sayfasındadır, ancak Alanı oluşturmak için kullandığınız `owner` hesabıyla giriş yaptığınızdan emin olun. `<api_url>` tarayıcınızda gösterilen URL'dir.
-   ArgillaHandler'ı dispatcher'a ekleyin.

```python
from llama_index.core.instrumentation import get_dispatcher
from argilla_llama_index import ArgillaHandler

argilla_handler = ArgillaHandler(
    dataset_name="query_llama_index",
    api_url="http://localhost:6900",
    api_key="argilla.apikey",
    number_of_retrievals=2,
)
root_dispatcher = get_dispatcher()
root_dispatcher.add_span_handler(argilla_handler)
root_dispatcher.add_event_handler(argilla_handler)
```

#### Örnek Kılavuzlar

-   [Argilla LlamaIndex Entegrasyonuna Başlarken](https://github.com/argilla-io/argilla-llama-index/blob/main/docs/tutorials/getting_started.ipynb)
-   [Diğer örnek eğitimler](https://github.com/argilla-io/argilla-llama-index/tree/main/docs/tutorials)

![Argilla LlamaIndex Entegrasyonu](./../../_static/integrations/argilla.png)

### Agenta

[Agenta](https://agenta.ai), geliştiricilerin ve ürün ekiplerinin LLM'ler tarafından desteklenen sağlam AI uygulamaları oluşturmasına yardımcı olan **açık kaynaklı** bir LLMOps platformudur. **Gözlemlenebilirlik**, **istem yönetimi ve mühendisliği** ile **LLM değerlendirmesi** için tüm araçları sunar.

#### Kullanım Kalıbı

Entegrasyon için gerekli bağımlılıkları yükleyin:

```bash
pip install agenta llama-index openinference-instrumentation-llama-index
```

API kimlik bilgilerinizi ayarlayın ve Agenta'yı başlatın:

```python
import os
import agenta as ag
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

# Agenta kimlik bilgilerinizi ayarlayın
os.environ["AGENTA_API_KEY"] = "agenta_api_anahtariniz"
os.environ["AGENTA_HOST"] = "https://cloud.agenta.ai"  # Varsa kendi barındırdığınız URL'yi kullanın

# Agenta SDK'yı başlat
ag.init()

# LlamaIndex enstrümantasyonunu etkinleştir
LlamaIndexInstrumentor().instrument()
```

Enstrümante edilmiş uygulamanızı oluşturun:

```python
@ag.instrument()
def document_search_app(user_query: str):
    """
    LlamaIndex kullanan döküman arama uygulaması.
    Dökümanları yükler, aranabilir bir indeks oluşturur ve kullanıcı sorgularını yanıtlar.
    """
    # Yerel dizinden dökümanları yükle
    docs = SimpleDirectoryReader("data").load_data()

    # Vektör arama indeksi oluştur
    search_index = VectorStoreIndex.from_documents(docs)

    # Sorgu işlemciyi başlat
    query_processor = search_index.as_query_engine()

    # Kullanıcı sorgusunu işle
    answer = query_processor.query(user_query)

    return answer
```

Bu kurulum yapıldıktan sonra Agenta tüm yürütme adımlarını otomatik olarak yakalayacaktır. Ardından uygulamanızda hata ayıklamak, bunları belirli yapılandırmalara ve istemlere bağlamak, performanslarını değerlendirmek, verileri sorgulamak ve temel metrikleri izlemek için Agenta'daki izleri görüntüleyebilirsiniz.

![Agenta LlamaIndex Entegrasyonu](./../../_static/integrations/agenta.png)

#### Örnek Kılavuzlar

-   [Agenta ile LlamaIndex için Gözlemlenebilirlik Dökümantasyonu](https://docs.agenta.ai/observability/integrations/llamaindex)
-   [Agenta ile LlamaIndex için Notebook Gözlemlenebilirliği](https://github.com/agenta-ai/agenta/blob/main/examples/jupyter/integrations/observability-openinference-llamaindex.ipynb)

### Deepeval

[DeepEval (Confident AI tarafından)](https://github.com/confident-ai/deepeval), LLM uygulamaları için açık kaynaklı bir değerlendirme çerçevesidir. LLM uygulamanızı DeepEval'in sunduğu 14'ten fazla varsayılan metrik (özetleme, halüsinasyon, yanıt uygunluğu, sadakat, RAGAS vb.) kullanarak "birim testine" tabi tutarken, LlamaIndex ile bu izleme entegrasyonu aracılığıyla başarısız test durumlarında hata ayıklayabilir veya DeepEval'in üretimde referanssız değerlendirmeler yapan barındırılan değerlendirme platformu [Confident AI](https://documentation.confident-ai.com/docs) aracılığıyla **üretimdeki** yetersiz değerlendirmeleri inceleyebilirsiniz.

#### Kullanım Kalıbı

```bash
pip install -U deepeval llama-index
```

```python
import deepeval
from deepeval.integrations.llama_index import instrument_llama_index

import llama_index.core.instrumentation as instrument

# Giriş yap
deepeval.login("<confident-api-anahtariniz>")

# DeepEval'in izleri toplamasını sağla
instrument_llama_index(instrument.get_dispatcher())
```

![tracing](https://confident-bucket.s3.us-east-1.amazonaws.com/llama-index%3Atrace.gif)

#### Kılavuzlar

-   [Llama Index Ajanlarını Değerlendirme](https://deepeval.com/integrations/frameworks/langchain)
-   [Llama Index Ajanlarını İzleme](https://documentation.confident-ai.com/docs/llm-tracing/integrations/llamaindex)

### Maxim AI

[Maxim AI](https://www.getmaxim.ai/), geliştiricilerin LLM uygulamalarını oluşturmalarına, izlemelerine ve iyileştirmelerine yardımcı olan bir Ajan Simülasyonu, Değerlendirme ve Gözlemlenebilirlik platformudur. Maxim'in LlamaIndex ile entegrasyonu; RAG sistemleriniz, ajanlarınız ve diğer LLM iş akışlarınız için kapsamlı izleme, takip ve değerlendirme yetenekleri sağlar.

#### Kullanım Kalıbı

Gerekli paketleri yükleyin:

```bash
pip install maxim-py
```

Ortam değişkenlerinizi ayarlayın:

```python
import os
from dotenv import load_dotenv

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

# Ortam değişkenlerini al
MAXIM_API_KEY = os.getenv("MAXIM_API_KEY")
MAXIM_LOG_REPO_ID = os.getenv("MAXIM_LOG_REPO_ID")

# Gerekli değişkenlerin ayarlandığını doğrula
if not MAXIM_API_KEY:
    raise ValueError("MAXIM_API_KEY ortam değişkeni gereklidir")
if not MAXIM_LOG_REPO_ID:
    raise ValueError("MAXIM_LOG_REPO_ID ortam değişkeni gereklidir")
```

Maxim'i başlatın ve LlamaIndex'i enstrümante edin:

```python
from maxim import Config, Maxim
from maxim.logger import LoggerConfig
from maxim.logger.llamaindex import instrument_llamaindex

# Maxim logger'ı başlat
maxim = Maxim(Config(api_key=os.getenv("MAXIM_API_KEY")))
logger = maxim.logger(LoggerConfig(id=os.getenv("MAXIM_LOG_REPO_ID")))

# LlamaIndex'i Maxim gözlemlenebilirliği ile enstrümante et
# Geliştirme sırasında ayrıntılı günlükleri görmek için debug=True yapın
instrument_llamaindex(logger, debug=True)

print("✅ Maxim enstrümantasyonu LlamaIndex için etkinleştirildi")
```

Artık LlamaIndex uygulamalarınız Maxim'e otomatik olarak iz gönderecektir:

```python
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI


# Araçları tanımla ve ajan oluştur
def add_numbers(a: float, b: float) -> float:
    """İki sayıyı topla."""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add_numbers)
llm = OpenAI(model="gpt-4o-mini", temperature=0)

agent = FunctionAgent(
    tools=[add_tool],
    llm=llm,
    verbose=True,
    system_prompt="Siz yardımcı bir hesap makinesi asistanısınız.",
)

# Bu işlem Maxim enstrümantasyonu tarafından otomatik olarak günlüklenecektir
import asyncio

response = await agent.run("15 + 25 kaçtır?")
print(f"Yanıt: {response}")
```

#### Kılavuzlar

-   [Maxim Enstrümantasyon Tarif Kitabı](/python/examples/observability/maxim-instrumentation)
-   [Maxim AI Dökümantasyonu](https://www.getmaxim.ai/docs/sdk/python/integrations/llamaindex/llamaindex)

![tracing](https://cdn.getmaxim.ai/public/images/llamaindex.gif)

## Diğer İş Ortağı `Tek Tıkla` Entegrasyonları (Eski Modüller)

Bu iş ortağı entegrasyonları eski `CallbackManager` yapımızı veya üçüncü taraf çağrılarını kullanır.

### Langfuse

Bu entegrasyon kullanımdan kaldırılmıştır (deprecated). Langfuse ile [burada](https://langfuse.com/docs/integrations/llama-index/get-started) açıklandığı gibi enstrümantasyon tabanlı yeni entegrasyonu kullanmanızı öneririz.

#### Kullanım Kalıbı

```python
from llama_index.core import set_global_handler

# 'llama-index-callbacks-langfuse' entegrasyon paketini yüklediğinizden emin olun.

# NOT: 'LANGFUSE_SECRET_KEY', 'LANGFUSE_PUBLIC_KEY' ve 'LANGFUSE_HOST' ortam 
# değişkenlerinizi langfuse.com proje ayarlarınızda gösterildiği gibi ayarlayın.

set_global_handler("langfuse")
```

#### Kılavuzlar

-   [Langfuse Callback İşleyicisi](/python/examples/observability/langfusecallbackhandler)
-   [PostHog ile Langfuse İzleme](/python/examples/observability/langfusemistralposthog)

![langfuse-tracing](https://static.langfuse.com/llamaindex-langfuse-docs.gif)

### OpenInference

[OpenInference](https://github.com/Arize-ai/open-inference-spec), AI model çıkarımlarını yakalamak ve depolamak için açık bir standarttır. [Phoenix](https://github.com/Arize-ai/phoenix) gibi LLM gözlemlenebilirlik çözümlerini kullanarak LLM uygulamalarının denenmesini, görselleştirilmesini ve değerlendirilmesini sağlar.

#### Kullanım Kalıbı

```python
import llama_index.core

llama_index.core.set_global_handler("openinference")

# NOT: Aşağıdakileri yapmanıza gerek yoktur
from llama_index.callbacks.openinference import OpenInferenceCallbackHandler
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings

# callback_handler = OpenInferenceCallbackHandler()
# Settings.callback_manager = CallbackManager([callback_handler])

# LlamaIndex uygulamanızı burada çalıştırın...
for query in queries:
    query_engine.query(query)

# LLM uygulama verilerinizi OpenInference formatında bir dataframe olarak görüntüleyin.
from llama_index.core.callbacks.open_inference_callback import as_dataframe

query_data_buffer = llama_index.core.global_handler.flush_query_data_buffer()
query_dataframe = as_dataframe(query_data_buffer)
```

**NOT**: Phoenix yeteneklerini açmak için, sorgu/bağlam dataframe'lerini beslemek üzere ek adımlar tanımlamanız gerekecektir. Aşağıya bakın!

#### Kılavuzlar

-   [OpenInference Callback İşleyicisi](/python/examples/observability/openinferencecallback)
-   [Arize Phoenix ile Arama ve Getirme İşlemini Değerlendirme](https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/llama_index_search_and_retrieval_tutorial.ipynb)

### TruEra TruLens

TruLens; geri bildirim fonksiyonları ve izleme gibi özellikler aracılığıyla kullanıcıların LlamaIndex uygulamalarını enstrümante etmelerine/değerlendirmelerine olanak tanır.

#### Kullanım Kalıbı + Kılavuzlar

```python
# trulens kullan
from trulens_eval import TruLlama

tru_query_engine = TruLlama(query_engine)

# sorgula
tru_query_engine.query("Yazar büyürken ne yaptı?")
```

![](./../../_static/integrations/trulens.png)

#### Kılavuzlar

-   [Trulens Kılavuzu](/python/framework/community/integrations/trulens)
-   [LlamaIndex + TruLens ile Hızlı Başlangıç Kılavuzu](https://github.com/truera/trulens/blob/trulens-eval-0.20.3/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb)

### HoneyHive

HoneyHive, kullanıcıların herhangi bir LLM iş akışının yürütme akışını izlemesine olanak tanır. Kullanıcılar daha sonra izlerinde hata ayıklayabilir ve analiz edebilir veya üretimden değerlendirme/ince ayar veri kümeleri oluşturmak için belirli iz olaylarındaki geri bildirimleri özelleştirebilirler.

#### Kullanım Kalıbı

```python
from llama_index.core import set_global_handler

set_global_handler(
    "honeyhive",
    project="Benim HoneyHive Projem",
    name="LLM İş Akışı Adım",
    api_key="HONEYHIVE API ANAHTARIM",
)

# NOT: Aşağıdakileri yapmanıza gerek yoktur
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings

# hh_tracer = HoneyHiveLlamaIndexTracer(
#     project="Benim HoneyHive Projem",
#     name="LLM İş Akışı Adım",
#     api_key="HONEYHIVE API ANAHTARIM",
# )
# Settings.callback_manager = CallbackManager([hh_tracer])
```

![](./../../_static/integrations/honeyhive.png)
![](./../../_static/integrations/perfetto.png)
_HoneyHive izlerinizi hata ayıklamak ve analiz etmek için Perfetto'yu kullanın_

#### Kılavuzlar

-   [HoneyHive Callback İşleyicisi](/python/examples/observability/honeyhivellamaindextracer)

### PromptLayer

PromptLayer; LLM çağrıları, etiketleme, çeşitli kullanım durumları için istemleri analiz etme ve değerlendirme genelinde analitikleri izlemenize olanak tanır. RAG istemlerinizin performansını ve daha fazlasını izlemek için LlamaIndex ile birlikte kullanın.

#### Kullanım Kalıbı

```python
import os

os.environ["PROMPTLAYER_API_KEY"] = "api_anahtariniz"

from llama_index.core import set_global_handler

# pl_tags opsiyoneldir, istemlerinizi ve uygulamalarınızı düzenlemenize yardımcı olur
set_global_handler("promptlayer", pl_tags=["paul graham", "essay"])
```

#### Kılavuzlar

-   [PromptLayer](/python/examples/observability/promptlayerhandler)

### Langtrace

[Langtrace](https://github.com/Scale3-Labs/langtrace), OpenTelemetry'yi destekleyen ve LLM uygulamalarını sorunsuz bir şekilde izlemek, değerlendirmek ve yönetmek için tasarlanmış sağlam bir açık kaynaklı araçtır. Langtrace, LlamaIndex ile doğrudan entegre olur; doğruluk, değerlendirmeler ve gecikme gibi performans metrikleri hakkında ayrıntılı, gerçek zamanlı içgörüler sunar.

#### Yükleme

```shell
pip install langtrace-python-sdk
```

#### Kullanım Kalıbı

```python
from langtrace_python_sdk import (
    langtrace,
)  # Herhangi bir llm modülü içe aktarmasından önce gelmelidir

langtrace.init(api_key="<LANGTRACE_API_KEY>")
```

#### Kılavuzlar

-   [Langtrace](https://docs.langtrace.ai/supported-integrations/llm-frameworks/llamaindex)

### OpenLIT

[OpenLIT](https://github.com/openlit/openlit), OpenTelemetry yerel bir Üretken Yapay Zeka (GenAI) ve LLM Uygulama Gözlemlenebilirlik aracıdır. Gözlemlenebilirliğin GenAI projelerine entegrasyon sürecini tek bir satır kodla gerçekleştirmek için tasarlanmıştır. OpenLIT; çeşitli LLM'ler, Vektör Veritabanları ve LlamaIndex gibi Çerçeveler için OpenTelemetry otomatik enstrümantasyonu sağlar. OpenLIT; LLM uygulamalarınızın performansı, isteklerin izlenmesi, maliyetler, tokenlar gibi kullanım metriklerine dair içgörüler ve çok daha fazlasını sunar.

#### Yükleme

```shell
pip install openlit
```

#### Kullanım Kalıbı

```python
import openlit

openlit.init()
```

#### Kılavuzlar

-   [OpenLIT Resmi Dökümantasyonu](https://docs.openlit.io/latest/integrations/llama-index)

### AgentOps

[AgentOps](https://github.com/AgentOps-AI/agentops), geliştiricilerin AI ajanları oluşturmasına, değerlendirmesine ve izlemesine yardımcı olur. AgentOps; prototipten üretime ajanlar oluşturmaya yardımcı olur, ajan izleme, LLM maliyet takibi, kıyaslama (benchmarking) ve daha fazlasını sağlar.

#### Yükleme

```shell
pip install llama-index-instrumentation-agentops
```

#### Kullanım Kalıbı

```python
from llama_index.core import set_global_handler

# NOT: AgentOps ortam değişkenlerinizi (örneğin 'AGENTOPS_API_KEY') AgentOps 
# dökümantasyonunda belirtildiği gibi ayarlayabilir veya set_global_handler 
# içindeki **eval_params olarak geçebilirsiniz.

set_global_handler("agentops")
```

### Basit (Simple - LLM Girişleri/Çıkışları)

Bu basit gözlemlenebilirlik aracı, her LLM giriş/çıkış çiftini terminale yazdırır. En çok LLM uygulamanızda hızlıca hata ayıklama (debug) günlüklerini etkinleştirmeniz gerektiğinde yararlıdır.

#### Kullanım Kalıbı

```python
import llama_index.core

llama_index.core.set_global_handler("simple")
```

#### Kılavuzlar

-   [MLflow](https://mlflow.org/docs/latest/llms/llama-index/index.html)

## Daha fazla gözlemlenebilirlik

-   [Geri Aramalar (Callbacks) Kılavuzu](/python/framework/module_guides/observability/callbacks)