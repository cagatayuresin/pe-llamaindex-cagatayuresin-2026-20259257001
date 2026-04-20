# LlamaIndex'te Çoklu Ajan Tasarımları

Bir görevi çözmek için birden fazla uzmanın gerektiği durumlarda LlamaIndex'te; her biri esneklik karşılığında kolaylık sunan birkaç seçeneğiniz vardır. Bu sayfa en yaygın üç tasarım kalıbını (pattern), her birini ne zaman seçmeniz gerektiğini açıklar ve her yaklaşım için asgari bir kod taslağı sunar.

1.  **AgentWorkflow (yerleşik)** – Bir dizi ajan tanımlayın ve `AgentWorkflow`'un geçişleri yönetmesine izin verin. [Bölüm](#pattern-1--agentworkflow-yani-dogrusal-ogul-tasarimi) [Tam Notebook](/python/examples/agent/agent_workflow_multi)
2.  **Orchestrator tasarımı (yerleşik)** – Bir "orkestra şefi" (orchestrator) ajan, bir sonraki adımda hangi alt ajanı çağıracağını seçer; bu alt ajanlar ona **araçlar (tools)** olarak sunulur. [Bölüm](#pattern-2--orkestra-sefi-ajani-arac-olarak-alt-ajanlar) [Tam Notebook](/python/examples/agent/agents_as_tools)
3.  **Özel planlayıcı (DIY - Sıfırdan)** – Sekansı planlayan LLM komutunu (genellikle XML / JSON) kendiniz yazarsınız ve ajanları kod içinde zorunlu (imperatively) olarak çağırırsınız. [Bölüm](#pattern-3--ozel-planlayici-sıfırdan-komut-hazırlama-ve-ayrıstırma) [Tam Notebook](/python/examples/agent/custom_multi_agent)

---

<div id="pattern-1--agentworkflow-yani-dogrusal-ogul-tasarimi"></div>

## Tasarım 1 – AgentWorkflow (yani doğrusal "oğul/swarm" tasarımı)

**Ne zaman kullanmalı** – Neredeyse hiç ekstra kod yazmadan çoklu ajan davranışı istiyorsanız ve `AgentWorkflow` ile gelen varsayılan geçiş mekanizmalarından memnunsanız.

`AgentWorkflow`, ajanları, durumu ve araç çağırmayı anlayacak şekilde önceden yapılandırılmış bir [İş Akışıdır (Workflow)](/python/llamaagents/workflows). Bir veya daha fazla ajandan oluşan bir *dizi* verirsiniz, hangisinin başlayacağını söylersiniz ve o:

1.  *Kök* (root) ajana kullanıcı mesajını iletir.
2.  O ajanın seçtiği araçları yürütür.
3.  Ajan karar verdiğinde kontrolü başka bir ajana "devretmesine" (handoff) izin verir.
4.  Bir ajan nihai bir yanıt döndürene kadar süreci tekrarlar.

**NOT:** Herhangi bir noktada, mevcut aktif ajan kontrolü kullanıcıya geri döndürmeyi seçebilir.

Aşağıda, [çoklu ajan rapor oluşturma örneğinin](/python/examples/agent/agent_workflow_multi) sadeleştirilmiş versiyonu yer almaktadır. Üç ajan bir raporu araştırmak, yazmak ve incelemek için iş birliği yapar. (`…` ifadesi, kısa tutmak amacıyla atlanan kodları belirtir.)

```python
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent

# --- uzman ajanlarımızı oluşturun ------------------------------------------------
research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Web'de arama yapın ve notlar alın.",
    system_prompt="Siz bir araştırmacısınız… Hazır olduğunuzda WriteAgent'a devredin.",
    llm=llm,
    tools=[search_web, record_notes],
    can_handoff_to=["WriteAgent"],
)

write_agent = FunctionAgent(
    name="WriteAgent",
    description="Notlardan bir markdown raporu yazar.",
    system_prompt="Siz bir yazarsınız… İşiniz bittiğinde ReviewAgent'tan geri bildirim isteyin.",
    llm=llm,
    tools=[write_report],
    can_handoff_to=["ReviewAgent", "ResearchAgent"],
)

review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Bir raporu inceler ve geri bildirim verir.",
    system_prompt="Siz bir incelemecisiniz…",  # vb.
    llm=llm,
    tools=[review_report],
    can_handoff_to=["WriteAgent"],
)

# --- onları birbirine bağlayın ---------------------------------------------------
agent_workflow = AgentWorkflow(
    agents=[research_agent, write_agent, review_agent],
    root_agent=research_agent.name,
    initial_state={
        "research_notes": {},
        "report_content": "Henüz yazılmadı.",
        "review": "İnceleme bekleniyor.",
    },
)

resp = await agent_workflow.run(
    user_msg="Bana web'in tarihçesi üzerine bir rapor yaz …"
)
print(resp)
```

`AgentWorkflow` tüm orkestrasyonu yapar ve ilerledikçe olayları (streaming events) yayınlar, böylece kullanıcıları ilerleme hakkında bilgilendirebilirsiniz.

---

<div id="pattern-2--orkestra-sefi-ajani-arac-olarak-alt-ajanlar"></div>

## Tasarım 2 – Orkestra şefi ajanı (araç olarak alt ajanlar)

**Ne zaman kullanmalı** – *Her* adıma karar veren tek bir yer olmasını ve buraya kendi özel mantığınızı dahil etmek istiyor ancak yine de kendi planlayıcınızı yazmak yerine dekleratif *araç olarak ajan* deneyimini tercih ediyorsanız.

Bu tasarımda yine uzman ajanlar (`ResearchAgent`, `WriteAgent`, `ReviewAgent`) oluşturursunuz, **ancak** birbirlerine devretmelerini **istemezsiniz**. Bunun yerine her ajanın `run` metodunu bir araç olarak sunarsınız ve bu araçları yeni bir üst düzey ajana – *Orchestrator* (Orkestra Şefi) – verirsiniz.

Tam örneği [agents_as_tools notebook](/python/examples/agent/agents_as_tools) dosyasında görebilirsiniz.

```python
import re
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context

# research_agent / write_agent / review_agent'ın yukarıdaki gibi tanımlandığını varsayalım
# ek olarak en azından `search_web` aracına ihtiyacımız var


async def call_research_agent(ctx: Context, prompt: str) -> str:
    """Belirli bir komuta dayanarak araştırma notları kaydetmek için kullanışlıdır."""
    result = await research_agent.run(
        user_msg=f"Aşağıdakiler hakkında notlar yaz: {prompt}"
    )

    async with ctx.store.edit_state() as ctx_state:
        ctx_state["state"]["research_notes"].append(str(result))

    return str(result)


async def call_write_agent(ctx: Context) -> str:
    """Araştırma notlarına dayanarak bir rapor yazmak veya geri bildirime dayanarak raporu revize etmek için kullanışlıdır."""
    async with ctx.store.edit_state() as ctx_state:
        notes = ctx_state["state"].get("research_notes", None)
        if not notes:
            return "Yazılacak araştırma notu yok."

        user_msg = f"Aşağıdaki notlardan bir markdown raporu yazın. Raporu mutlaka şu formatta çıktı olarak verin: <report>...</report>:\n\n"

        # Eğer varsa geri bildirimi kullanıcı mesajına ekleyin
        feedback = ctx_state["state"].get("review", None)
        if feedback:
            user_msg += f"<feedback>{feedback}</feedback>\n\n"

        # Araştırma notlarını kullanıcı mesajına ekleyin
        notes = "\n\n".join(notes)
        user_msg += f"<research_notes>{notes}</research_notes>\n\n"

        # Yazma ajanını çalıştırın
        result = await write_agent.run(user_msg=user_msg)
        report = re.search(
            r"<report>(.*)</report>", str(result), re.DOTALL
        ).group(1)
        ctx_state["state"]["report_content"] = str(report)

    return str(report)


async def call_review_agent(ctx: Context) -> str:
    """Raporu incelemek ve geri bildirim sağlamak için kullanışlıdır."""
    async with ctx.store.edit_state() as ctx_state:
        report = ctx_state["state"].get("report_content", None)
        if not report:
            return "İncelenecek rapor içeriği yok."

        result = await review_agent.run(
            user_msg=f"Aşağıdaki raporu incele: {report}"
        )
        ctx_state["state"]["review"] = result

    return result


orchestrator = FunctionAgent(
    system_prompt=(
        "Siz rapor yazma alanında bir uzmansınız. "
        "Size bir kullanıcı isteği ve isteğe yardımcı olabilecek araçların bir listesi veriliyor. "
        "Verilen konu hakkında bir raporu araştırmak, yazmak ve incelemek için araçları koordine etmelisiniz. "
        "İnceleme olumlu olduğunda kullanıcıya raporun erişime hazır olduğunu bildirmelisiniz."
    ),
    llm=orchestrator_llm,
    tools=[
        call_research_agent,
        call_write_agent,
        call_review_agent,
    ],
    initial_state={
        "research_notes": [],
        "report_content": None,
        "review": None,
    },
)

response = await orchestrator.run(
    user_msg="Bana web'in tarihçesi üzerine bir rapor yaz …"
)
print(response)
```

Orkestra şefi de sadece başka bir `FunctionAgent` olduğu için akış (streaming), araç çağırma ve durum yönetimini bedavaya alırsınız; buna rağmen ajanların nasıl çağrıldığı ve genel kontrol akışı üzerinde tam kontrole sahip olursunuz (araçlar her zaman orkestra şefine geri döner).

---

<div id="pattern-3--ozel-planlayici-sıfırdan-komut-hazırlama-ve-ayrıstırma"></div>

## Tasarım 3 – Özel planlayıcı (DIY - komut hazırlama + ayrıştırma)

**Ne zaman kullanmalı** – Nihai esneklik gereken durumlarda. Çok özel bir plan formatı dayatmanız, harici zamanlayıcılarla entegre olmanız veya önceki tasarımların hazır sunamadığı ek metadataları toplamanız gerekiyorsa.

Buradaki fikir, LLM'e yapılandırılmış bir plan (XML / JSON / YAML) çıktılamasını talimat veren bir komut yazmanızdır. Kendi Python kodunuz bu planı ayrıştırır ve zorunlu olarak yürütür. Alt ajanlar herhangi bir şey olabilir – `FunctionAgent`lar, RAG hatları veya diğer servisler.

Aşağıda, plan yapabilen, planı yürütebilen ve daha fazla adıma gerek olup olmadığını görebilen bir iş akışının *asgari* taslağı yer almaktadır. Tam örneği [custom_multi_agent notebook](/python/examples/agent/custom_multi_agent) dosyasında görebilirsiniz.

```python
import re
import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field
from typing import Any, Optional

from llama_index.core.llms import ChatMessage
from llama_index.core.workflow import (
    Context,
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)

# Ajanları çağırmak için yardımcı fonksiyonlar oluşturduğumuzu varsayalım

PLANNER_PROMPT = """Siz bir planlayıcı sohbet robotusunuz.

Bir kullanıcı isteği ve mevcut durum verildiğinde, çözümü sıralı <step> bloklarına bölün. Her adım, çağrılacak ajanı ve gönderilecek mesajı belirtmelidir, örn:
<plan>
  <step agent=\"ResearchAgent\">şunu ara: …</step>
  <step agent=\"WriteAgent\">bir rapor taslağı hazırla: …</step>
  ...
</plan>

<state>
{state}
</state>

<available_agents>
{available_agents}
</available_agents>

Genel akış şu şekilde olmalıdır:
- Araştırma notlarını kaydet
- Bir rapor yaz
- Raporu incele
- İnceleme yeterince olumlu değilse raporu tekrar yaz

Kullanıcı isteği herhangi bir adım gerektirmiyorsa <plan> bloğunu atlayabilir ve doğrudan yanıt verebilirsiniz.
"""


class InputEvent(StartEvent):
    user_msg: Optional[str] = Field(default=None)
    chat_history: list[ChatMessage]
    state: Optional[dict[str, Any]] = Field(default=None)


class OutputEvent(StopEvent):
    response: str
    chat_history: list[ChatMessage]
    state: dict[str, Any]


class StreamEvent(Event):
    delta: str


class PlanEvent(Event):
    step_info: str


# Planın modellenmesi
class PlanStep(BaseModel):
    agent_name: str
    agent_input: str


class Plan(BaseModel):
    steps: list[PlanStep]


class ExecuteEvent(Event):
    plan: Plan
    chat_history: list[ChatMessage]


class PlannerWorkflow(Workflow):
    llm: OpenAI = OpenAI(
        model="o3-mini",
        api_key="sk-proj-...",
    )
    agents: dict[str, FunctionAgent] = {
        "ResearchAgent": research_agent,
        "WriteAgent": write_agent,
        "ReviewAgent": review_agent,
    }

    @step
    async def plan(
        self, ctx: Context, ev: InputEvent
    ) -> ExecuteEvent | OutputEvent:
        # Varsa başlangıç durumunu ayarla
        if ev.state:
            await ctx.store.set("state", ev.state)

        chat_history = ev.chat_history

        if ev.user_msg:
            user_msg = ChatMessage(
                role="user",
                content=ev.user_msg,
            )
            chat_history.append(user_msg)

        # Durum ve mevcut ajanlarla birlikte sistem komutunu enjekte et
        state = await ctx.store.get("state")
        available_agents_str = "\n".join(
            [
                f'<agent name="{agent.name}">{agent.description}</agent>'
                for agent in self.agents.values()
            ]
        )
        system_prompt = ChatMessage(
            role="system",
            content=PLANNER_PROMPT.format(
                state=str(state),
                available_agents=available_agents_str,
            ),
        )

        # LLM'den yanıt akışı al
        response = await self.llm.astream_chat(
            messages=[system_prompt] + chat_history,
        )
        full_response = ""
        async for chunk in response:
            full_response += chunk.delta or ""
            if chunk.delta:
                ctx.write_event_to_stream(
                    StreamEvent(delta=chunk.delta),
                )

        # Yanıtı bir plana ayrıştırın ve yürütmeye mi yoksa çıktı vermeye mi karar verin
        xml_match = re.search(r"(<plan>.*</plan>)", full_response, re.DOTALL)

        if not xml_match:
            chat_history.append(
                ChatMessage(
                    role="assistant",
                    content=full_response,
                )
            )
            return OutputEvent(
                response=full_response,
                chat_history=chat_history,
                state=state,
            )
        else:
            xml_str = xml_match.group(1)
            root = ET.fromstring(xml_str)
            plan = Plan(steps=[])
            for step in root.findall("step"):
                plan.steps.append(
                    PlanStep(
                        agent_name=step.attrib["agent"],
                        agent_input=step.text.strip() if step.text else "",
                    )
                )

            return ExecuteEvent(plan=plan, chat_history=chat_history)

    @step
    async def execute(self, ctx: Context, ev: ExecuteEvent) -> InputEvent:
        chat_history = ev.chat_history
        plan = ev.plan

        for step in plan.steps:
            agent = self.agents[step.agent_name]
            agent_input = step.agent_input
            ctx.write_event_to_stream(
                PlanEvent(
                    step_info=f'<step agent="{step.agent_name}">{step.agent_input}</step>'
                ),
            )

            if step.agent_name == "ResearchAgent":
                await call_research_agent(ctx, agent_input)
            elif step.agent_name == "WriteAgent":
                # Not: Plandan gelen girdiyi geçmiyoruz çünkü
                # yazma ajanını yönlendirmek için durumu (state) kullanıyoruz
                await call_write_agent(ctx)
            elif step.agent_name == "ReviewAgent":
                await call_review_agent(ctx)

        state = await ctx.store.get("state")
        chat_history.append(
            ChatMessage(
                role="user",
                content=f"Önceki adımları tamamladım, işte güncellenmiş durum:\n\n<state>\n{state}\n</state>\n\nDevam edip daha fazla adım planlamanız gerekiyor mu? Gerekiyorsa planlayın, gerekmiyorsa nihai bir yanıt yazın.",
            )
        )

        return InputEvent(
            chat_history=chat_history,
        )
```

Bu yaklaşım, orkestrasyon döngüsünün *size* ait olduğu anlamına gelir; böylece ihtiyacınız olan her türlü özel mantığı, önbelleğe almayı veya döngüde insan kontrollerini ekleyebilirsiniz.

---

## Bir Tasarım Kalıbı Seçmek

| Tasarım Kalıbı     | Kod Satırı Sayısı | Esneklik | Yerleşik Akış / Olaylar                       |
| ------------------ | ----------------- | -------- | --------------------------------------------- |
| AgentWorkflow      | ⭐ – en az        | ★★       | Evet                                          |
| Orchestrator ajan  | ⭐⭐              | ★★★      | Evet (orkestra şefi aracılığıyla)             |
| Özel planlayıcı    | ⭐⭐⭐            | ★★★★★    | Evet (alt ajanlar üzerinden). Üst düzey size ait. |

Eğer hızlıca prototip oluşturuyorsanız `AgentWorkflow` ile başlayın. Sekans üzerinde daha fazla kontrole ihtiyacınız olduğunda *Orchestrator ajanına* geçin. Sadece ilk iki tasarım kalıbı ihtiyacınız olan akışı ifade edemediğinde *Özel planlayıcıya* başvurun.

Sıkardaki bölümde, [tekli ve çoklu ajan iş akışlarında yapılandırılmış çıktı (structured output)](/python/framework/understanding/agent/structured_output) kullanımını öğreneceksiniz.