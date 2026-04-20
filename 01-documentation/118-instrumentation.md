# Enstrümantasyon (Instrumentation)

**NOT**: `instrumentation` modülü (llama-index v0.10.20 ve sonrası sürümlerde mevcuttur), eski `callbacks` modülünün yerini alması için tasarlanmıştır. Kullanımdan kaldırma (deprecation) süresi boyunca llama-index kütüphanesi, LLM uygulamanızı enstrümante etmeniz için her iki modülü de desteklemektedir. Ancak, mevcut tüm entegrasyonlar yeni `instrumentation` modülüne taşındıktan sonra bir noktada `callbacks` modülünü artık desteklemeyeceğiz.

Yeni `instrumentation` modülü, `llama-index` uygulamalarının enstrümante edilmesine olanak tanır. Özellikle; hem özel mantıkla hem de modülde sunulanlarla olayları işleyebilir ve zaman aralıklarını (span) takip edebilirsiniz. Kullanıcılar ayrıca kendi olaylarını tanımlayabilir ve bu olayların kod mantığında nerede ve ne zaman yayınlanması gerektiğini belirtebilirler. `instrumentation` modülünün temel sınıfları ve kısa açıklamaları aşağıda listelenmiştir:

-   `Event`: Uygulama kodunun yürütülmesi sırasında belirli bir olayın meydana geldiği tek bir anı temsil eder.
-   `EventHandler`: `Event` (Olay) oluşumlarını dinler ve bu anlarda kod mantığını yürütür.
-   `Span`: Uygulama kodunun belirli bir bölümünün yürütme akışını temsil eder ve bu nedenle `Event`'leri içerir.
-   `SpanHandler`: `Span`'ların (Zaman Aralığı) girişi, çıkışı ve düşürülmesinden (yani hata nedeniyle erken çıkış) sorumludur.
-   `Dispatcher`: `Event`'leri yayınlamanın yanı sıra uygun işleyicilere bir `Span`'a girme/çıkma/düşürme sinyalleri gönderir.

## Gözlemlenebilirlik için Enstrümantasyon Modülünü Kullanma

Enstrümantasyonun temel kullanım durumlarından biri gözlemlenebilirliktir. Üçüncü taraf ortaklarla olan yerel enstrümantasyon entegrasyonlarımız, tüm çağrı yığını (call stack) boyunca ayrıntılı izler (traces) almanızı sağlar.

Desteklenen ortaklar hakkında daha fazla ayrıntı için [gözlemlenebilirlik kılavuzumuza](/python/framework/module_guides/observability) göz atın.

## Kullanım

Yeni `instrumentation` modülünü kullanmak 3 üst düzey adımı içerir:

1. Bir `dispatcher` (dağıtıcı) tanımlayın.
2. (İsteğe bağlı) `EventHandler`'larınızı (Olay İşleyicileri) tanımlayın ve `dispatcher`'a bağlayın.
3. (İsteğe bağlı) `SpanHandler`'ınızı (Zaman Aralığı İşleyicisi) tanımlayın ve `dispatcher`'a bağlayın.

Bunu yapmak, `llama-index` kütüphanesi ve uzantı paketleri boyunca iletilen olayları işleme ve zaman aralıklarını (span) elde etme yeteneği ile sonuçlanır.

Örneğin, kütüphanede yapılan her LLM çağrısını takip etmek isteseydim:

```python
from typing import Dict, List

from llama_index.core.instrumentation.events.llm import (
    LLMChatEndEvent,
    LLMChatStartEvent,
    LLMChatInProgressEvent,
)


class ExampleEventHandler(BaseEventHandler):
    events: List[BaseEvent] = []

    @classmethod
    def class_name(cls) -> str:
        """Sınıf adı."""
        return "ExampleEventHandler"

    def handle(self, event: BaseEvent) -> None:
        """Olayı işleme mantığı."""
        print("-----------------------")
        # tüm olaylar bu niteliklere sahiptir
        print(event.id_)
        print(event.timestamp)
        print(event.span_id)

        # olaya özel nitelikler
        if isinstance(event, LLMChatStartEvent):
            # başlangıç
            print(event.messages)
            print(event.additional_kwargs)
            print(event.model_dict)
        elif isinstance(event, LLMChatInProgressEvent):
            # akış (streaming)
            print(event.response.delta)
        elif isinstance(event, LLMChatEndEvent):
            # nihai yanıt
            print(event.response)

        self.events.append(event)
        print("-----------------------")
```

LlamaIndex'te günlüğe kaydedilen tüm olaylar hakkında [tam kılavuza](/python/examples/instrumentation/instrumentation_observability_rundown) bakın veya daha fazla ayrıntı için [API referansını](/python/framework-api-reference/instrumentation) ziyaret edin.

### Özel bir `EventHandler` Tanımlama

Kullanıcılar, `BaseEventHandler` sınıfını alt sınıfa ayırarak ve soyut `handle()` yöntemine mantık sağlayarak kendi özel işleyicilerini oluşturabilirler.

```python
from llama_index.core.instrumentation.event_handlers.base import (
    BaseEventHandler,
)


class MyEventHandler(BaseEventHandler):
    """Benim özel EventHandler'ım."""

    @classmethod
    def class_name(cls) -> str:
        """Sınıf adı."""
        return "MyEventHandler"

    def handle(self, event: BaseEvent, **kwargs) -> Any:
        """Olayı işleme mantığı."""
        print(event.class_name())


my_event_handler = MyEventHandler()
```

İşleyicinizi tanımladıktan sonra istediğiniz dağıtıcıya (dispatcher) bağlayabilirsiniz:

```python
import llama_index.core.instrumentation as instrument

dispatcher = instrument.get_dispatcher(__name__)
dispatcher.add_event_handler(my_event_handler)
```

### Özel bir `Event` Tanımlama

Kullanıcılar, `BaseEvent` sınıfını alt sınıfa ayırarak kendi özel olaylarını oluşturabilirler. `BaseEvent` sınıfı bir `timestamp` ve bir `id_` alanı ile birlikte gelir. Bu olay yüküne (payload) daha fazla öğe eklemek için, bunları yeni `Fields` (alanlar) olarak eklemeniz yeterlidir (çünkü bunlar `pydantic.BaseModel`'in alt sınıflarıdır).

```python
from llama_index.core.instrumentation.event.base import BaseEvent


class MyEvent(BaseEvent):
    """Benim özel Olayım (Event)."""

    yeni_alan_1 = Field(...)
    yeni_alan_2 = Field(...)
```

Özel olayınız tanımlandıktan sonra, uygulamanızın kodu boyunca istenen durumlarda olayı ateşlemek için bir dağıtıcı (dispatcher) kullanırsınız.

```python
import llama_index.core.instrumentation as instrument

dispatcher = instrument.get_dispatcher(__name__)
dispatcher.event(MyEvent(yeni_alan_1=..., yeni_alan_2=...))
```

### Özel bir `Span` Tanımlama

`Span`'lar, her ikisinin de yapılandırılmış veri sınıfları olması bakımından `Event`'lere benzer. Ancak `Event`'lerin aksine, `Span`'lar adından da anlaşılacağı gibi, programın yürütme akışı içinde bir zaman süresini kapsar. İstediğiniz bilgileri depolamak için özel bir `Span` tanımlayabilirsiniz.

```python
from typing import Any
from llama_index.core.bridge.pydantic import Field


class MyCustomSpan(BaseSpan):
    ozel_alan_1: Any = Field(...)
    ozel_alan_2: Any = Field(...)
```

Yeni Span türünüzü işlemek için ayrıca `BaseSpanHandler` sınıfını alt sınıfa ayırarak kendi özel `SpanHandler` sınıfınızı tanımlamanız gerekir. Bu temel sınıfı alt sınıfa ayırırken üç soyut yöntemin tanımlanması gerekir: `new_span()`, `prepare_to_exit_span()` ve `prepare_to_drop_span()`.

```python
import inspect
from typing import Any, Dict, Optional
from llama_index.core.instrumentation.span.base import BaseSpan
from llama_index.core.instrumentation.span_handlers import BaseSpanHandler


class MyCustomSpanHandler(BaseSpanHandler[MyCustomSpan]):
    @classmethod
    def class_name(cls) -> str:
        """Sınıf adı."""
        return "MyCustomSpanHandler"

    def new_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[MyCustomSpan]:
        """Yeni bir span oluştur."""
        # yeni bir MyCustomSpan oluşturma mantığı
        pass

    def prepare_to_exit_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        result: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """Bir span'dan çıkmaya hazırlanma mantığı."""
        pass

    def prepare_to_drop_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        err: Optional[BaseException] = None,
        **kwargs: Any,
    ) -> Any:
        """Bir span'ı düşürmeye (drop) hazırlanma mantığı."""
        pass
```

Yeni SpanHandler'ınızı (ve ilişkili Span türünü) kullanmak için, onu istediğiniz dağıtıcıya (dispatcher) eklemeniz yeterlidir.

```python
import llama_index.core.instrumentation as instrument
from llama_index.core.instrumentation.span_handler import SimpleSpanHandler

dispatcher = (
    instrument.get_dispatcher()
)  # ad argümanı verilmezse varsayılan olarak kök (root) olur

my_span_handler = MyCustomSpanHandler()
dispatcher.add_span_handler(my_span_handler)
```

### Bir `Span`'a Giriş/Çıkış Yapma

`SpanHandler`'lara bir `Span`'a girme/çıkma sinyali göndermek için sırasıyla `span_enter()` ve `span_exit()` yöntemlerini kullanırız. Ayrıca, kapsanan kodun yürütülmesi sırasındaki hatalar nedeniyle `Span`'ların normalden daha kısa kesildiği durumları yönetmek için kullanılabilecek `span_drop()` yöntemi de vardır.

```python
import llama_index.core.instrumentation as instrument

dispatcher = instrument.get_dispatcher(__name__)


def func():
    dispatcher.span_enter(...)
    try:
        val = ...
    except:
        ...
        dispatcher.span_drop(...)
    else:
        dispatcher.span_exit(...)
        return val


# veya dekoratörler aracılığıyla sözdizimsel şeker (syntactic sugar)


@dispatcher.span
def func():
    ...
```

### `dispatcher` Hiyerarşisinden Faydalanma

Standart Python `logging` kütüphanesinde ve onun `Logger` sınıfında görülene benzer bir hiyerarşi `dispatcher` için de mevcuttur. Özellikle; kök (root) `dispatcher` dışındaki tüm `dispatcher`'ların bir üst (parent) öğesi vardır ve olayları veya zaman aralıklarını (span) işlerken bunları üst öğesine de yayabilir (bu varsayılan davranıştır). Olayları ve zaman aralıklarını işlemenin bu hiyerarşik yöntemi, "küresel" olay işleyicilerinin yanı sıra "yerel" olanların da tanımlanmasına olanak tanır.

Aşağıda tanımlanan proje yapısını düşünün. 3 adet `dispatcher` vardır: biri `project`'in üst seviyesinde ve diğer ikisi `llama1` ve `llama2` alt modüllerindedir. Bu kurulumla; proje kökünün `dispatcher`'ına bağlı herhangi bir `EventHandler`, `llama1` ve `llama2` kodunun yürütülmesinde meydana gelen tüm `Event`'lere abone olacaktır. Diğer yandan, ilgili `llama<x>` alt modüllerinde tanımlanan `EventHandler`'lar sadece kendi alt modül yürütmeleri içinde meydana gelen `Event`'lere abone olacaktır.

```sh
proje
├── __init__.py  # dispatcher=instrument.get_dispatcher(__name__) içerir
├── llama1
│   ├── __init__.py  # dispatcher=instrument.get_dispatcher(__name__) içerir
│   └── app_query_engine.py
└── llama2
    ├── __init__.py  # dispatcher=instrument.get_dispatcher(__name__) içerir
    └── app_query_engine.py
```

## Not Defteri Kılavuzları:

-   [Temel Kullanım](/python/examples/instrumentation/basic_usage)
-   [Model Çağrılarını Gözlemleme](/python/examples/instrumentation/observe_api_calls)
-   [Tüm Olayları Gözlemleme](/python/examples/instrumentation/instrumentation_observability_rundown)

## API Referansı

-   [Enstrümantasyon API Referansı](/python/framework-api-reference/instrumentation)