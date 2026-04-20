# Döngüde İnsan (Human in the Loop)

Döngüye bir insanı dahil eden araçlar da tanımlanabilir. Bu, bir araç çağrısını onaylamak veya geri bildirim sağlamak gibi insan girdisi gerektiren görevler için yararlıdır.

[İş Akışları (Workflows) eğitimimizde](/python/llamaagents/workflows) göreceğimiz gibi, İş Akışlarının AgentWorkflow'un arka planında çalışma şekli, hem olay (event) yayınlayan hem de olay alan adımları çalıştırmaktır. Aşağıda, bir AgentWorkflow'u oluşturan adımların (mavi renkte) ve aralarında veri aktaran olayların (yeşil renkte) bir diyagramı bulunmaktadır. Bu olayları tanıyacaksınız; bunlar daha önce çıktı akışında ele aldığımız olaylarla aynıdır.

![İş Akışları diyagramı](./agentworkflow.jpg)

Döngüye bir insanı dahil etmek için, aracımızın iş akışındaki diğer hiçbir adım tarafından alınmayan bir olay yayınlamasını sağlayacağız. Ardından aracımıza, belirli bir "yanıt" (reply) olayı alana kadar beklemesini söyleyeceğiz.

Bu amaçla kullanılmak üzere yerleşik `InputRequiredEvent` ve `HumanResponseEvent` olaylarımız mevcuttur. Farklı insan girdisi formlarını yakalamak istiyorsanız, bu olayları kendi tercihlerinize uyacak şekilde alt sınıflara (subclass) ayırabilirsiniz. Bunları import edelim:

```python
from llama_index.core.workflow import (
    InputRequiredEvent,
    HumanResponseEvent,
)
```

Ardından, varsayımsal bir tehlikeli görev gerçekleştiren bir araç oluşturacağız. Burada birkaç yeni şey oluyor:

- `wait_for_event`, bir `HumanResponseEvent` beklemek için kullanılır.
- `waiter_event`, çağıranın bir yanıt beklediğimizi bilmesini sağlamak için olay akışına yazılan olaydır.
- `waiter_id`, bu spesifik bekleme çağrısı için benzersiz bir tanımlayıcıdır. Her bir `waiter_id` için yalnızca bir `waiter_event` gönderilmesini sağlamaya yardımcı olur.
- `requirements` argümanı, belirli bir `user_name` değerine sahip bir `HumanResponseEvent` beklemek istediğimizi belirtmek için kullanılır.

```python
from llama_index.core.workflow import Context


async def dangerous_task(ctx: Context) -> str:
    """İnsan onayı gerektiren tehlikeli bir görev."""

    # bir bekleme olayı yayınla (burada InputRequiredEvent)
    # ve bir HumanResponseEvent görene kadar bekle
    question = "Devam etmek istediğinizden emin misiniz? "
    response = await ctx.wait_for_event(
        HumanResponseEvent,
        waiter_id=question,
        waiter_event=InputRequiredEvent(
            prefix=question,
            user_name="Laurie",
        ),
        requirements={"user_name": "Laurie"},
    )

    # olaydan gelen girdiye göre hareket et
    if response.response.strip().lower() == "evet":
        return "Tehlikeli görev başarıyla tamamlandı."
    else:
        return "Tehlikeli görev iptal edildi."
```

Ajanımızı her zamanki gibi oluşturuyoruz ve az önce tanımladığımız aracı ona geçiriyoruz:

```python
workflow = FunctionAgent(
    tools=[dangerous_task],
    llm=llm,
    system_prompt="Siz tehlikeli görevleri yerine getirebilen yardımcı bir asistansınız.",
)
```

Artık iş akışını çalıştırabilir, `InputRequiredEvent` olayını tıpkı diğer herhangi bir akış (streaming) olayı gibi ele alabilir ve `send_event` metodunu kullanarak geçirilen bir `HumanResponseEvent` ile yanıt verebiliriz:

```python
handler = workflow.run(user_msg="Tehlikeli göreve devam etmek istiyorum.")

async for event in handler.stream_events():
    if isinstance(event, InputRequiredEvent):
        # klavye girdisini yakala
        response = input(event.prefix)
        # yanıtımızı geri gönder
        handler.ctx.send_event(
            HumanResponseEvent(
                response=response,
                user_name=event.user_name,
            )
        )

response = await handler
print(str(response))
```

Her zamanki gibi, bu örneğin [tam kodunu](https://github.com/run-llama/python-agents-tutorial/blob/main/5_human_in_the_loop.py) görebilirsiniz.

Girdiyi yakalamak için istediğiniz her şeyi yapabilirsiniz; bir grafik arayüz (GUI), ses girişi kullanabilir ve hatta başka, ayrı bir ajanı sürece dahil edebilirsiniz. Girdiniz zaman alacaksa veya başka bir süreçte gerçekleşecekse, iş akışına daha sonra devam edebilmek için [bağlamı serileştirmek (serialize the context)](/python/framework/understanding/agent/state) ve bir veritabanına ya da dosyaya kaydetmek isteyebilirsiniz.

Diğer ajanları dahil etmekten bahsetmişken, bir sonraki bölümümüze geçiyoruz: [çoklu ajan sistemleri (multi-agent systems)](/python/framework/understanding/agent/multi_agent) oluşturmanın çeşitli yollarını detaylandırıyoruz.