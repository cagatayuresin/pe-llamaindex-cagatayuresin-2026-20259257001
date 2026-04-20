# Ajanlar (Agents)

LlamaIndex'te bir "ajanı"; dış kullanıcılardan gelen girdileri işlemek için LLM, bellek ve araçlar kullanan belirli bir sistem olarak tanımlıyoruz. Bunu, genel olarak süreçte LLM karar verme mekanizmasına sahip olan herhangi bir sistemi ifade eden "ajanlı" (agentic) terimiyle karşılaştırın.

LlamaIndex'te bir ajan oluşturmak sadece birkaç satır kod alır:

```python
import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI


# Basit bir hesap makinesi aracı tanımlayın
def multiply(a: float, b: float) -> float:
    """İki sayıyı çarpmak için kullanışlıdır."""
    return a * b


# Hesap makinesi aracımızla bir ajan iş akışı oluşturun
agent = FunctionAgent(
    tools=[multiply],
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="Siz, iki sayıyı çarpabilen yardımcı bir asistansınız.",
)


async def main():
    # Ajanı çalıştırın
    response = await agent.run("1234 * 4567 nedir?")
    print(str(response))


# Ajanı çalıştırın
if __name__ == "__main__":
    asyncio.run(main())
```

Bu ajanı çağırmak, belirli bir eylem döngüsünü başlatır:

-   Ajan en son mesajı + sohbet geçmişini alır.
-   Araç şemaları ve sohbet geçmişi API üzerinden gönderilir.
-   Ajan ya doğrudan bir yanıtla ya da bir araç çağrıları listesiyle yanıt verir.
    -   Her araç çağrısı yürütülür.
    -   Araç çağrısı sonuçları sohbet geçmişine eklenir.
    -   Ajan güncellenmiş geçmişle tekrar çağrılır ve ya doğrudan yanıt verir ya da daha fazla çağrı seçer.

`FunctionAgent`, araçları yürütmek için bir LLM sağlayıcısının fonksiyon/araç çağırma yeteneklerini kullanan bir ajan türüdür. [`ReActAgent`](/python/examples/agent/react_agent) ve [`CodeActAgent`](/python/examples/agent/code_act_agent) gibi diğer ajan türleri, araçları yürütmek için farklı istem verme stratejileri kullanır.

Ajanlar ve yetenekleri hakkında daha fazla bilgi edinmek için [ajanlar kılavuzunu](/python/framework/understanding/agent) ziyaret edebilirsiniz.

> **İpucu:** Bazı modeller akışlı (streaming) LLM çıktısını desteklemeyebilir. Akış varsayılan olarak etkin olsa da, bir hatayla karşılaşırsanız akışı devre dışı bırakmak için her zaman `FunctionAgent(..., streaming=False)` ayarını yapabilirsiniz.

## Araçlar (Tools)

Araçlar basitçe Python fonksiyonları olarak tanımlanabilir veya `FunctionTool` ve `QueryEngineTool` gibi sınıflar kullanılarak daha da özelleştirilebilir. LlamaIndex ayrıca `Tool Specs` adı verilen bir yapı kullanarak yaygın API'ler için önceden tanımlanmış araç setleri sağlar.

Araçları yapılandırma hakkında daha fazla bilgiyi [araçlar kılavuzunda](/python/framework/module_guides/deploying/agents/tools) okuyabilirsiniz.

## Bellek (Memory)

Bellek, ajanlar oluştururken temel bir bileşendir. Varsayılan olarak tüm LlamaIndex ajanları bellek için `ChatMemoryBuffer` kullanır.

Bunu özelleştirmek için ajanın dışında tanımlayabilir ve içeri aktarabilirsiniz:

```python
from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=40000)

response = await agent.run(..., memory=memory)
```

Belleği yapılandırma hakkında daha fazla bilgiyi [bellek kılavuzunda](/python/framework/module_guides/deploying/agents/memory) okuyabilirsiniz.

## Çok Modlu (Multi-Modal) Ajanlar

Bazı LLM'ler görüntüler ve metin gibi birden fazla modaliteyi destekleyecektir. İçerik bloklarına sahip sohbet mesajlarını kullanarak, akıl yürütme için bir ajana görüntüler geçebiliriz.

Örneğin, [bu sunumdaki slaydın](https://docs.google.com/presentation/d/1wy3nuO9ezGS4R99mzP3Q3yvrjAkZ26OGI2NjfqtwAaE/edit?usp=sharing) bir ekran görüntüsüne sahip olduğunuzu varsayalım.

Bu görüntüyü akıl yürütme için bir ajana iletebilir ve görüntüyü okuyup buna göre hareket ettiğini görebilirsiniz.

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llms import ChatMessage, ImageBlock, TextBlock
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini", api_key="sk-...")


def add(a: int, b: int) -> int:
    """İki sayıyı toplamak için kullanışlıdır."""
    return a + b


workflow = FunctionAgent(
    tools=[add],
    llm=llm,
)

msg = ChatMessage(
    role="user",
    blocks=[
        TextBlock(text="Görüntünün söylediklerini takip et."),
        ImageBlock(path="./screenshot.png"),
    ],
)

response = await workflow.run(msg)
print(str(response))
```

## Çok Ajanlı Sistemler (Multi-Agent Systems)

Ajanları, görevleri tamamlarken her ajanın koordine olmak için kontrolü başka bir ajana devredebildiği çok ajanlı bir sistemde birleştirebilirsiniz.

```python
from llama_index.core.agent.workflow import AgentWorkflow

multi_agent = AgentWorkflow(agents=[FunctionAgent(...), FunctionAgent(...)])

resp = await agent.run("sorgu")
```

Bu, çok ajanlı sistemler kurmanın yollarından sadece biridir. [Çok ajanlı sistemler](/python/framework/understanding/agent/multi_agent) hakkında daha fazla bilgi edinmek için okumaya devam edin.

## Manuel Ajanlar

`FunctionAgent`, `ReActAgent`, `CodeActAgent` ve `AgentWorkflow` gibi ajan sınıfları birçok ayrıntıyı soyutlasa da, bazen kendi düşük seviyeli ajanlarınızı oluşturmak isteyebilirsiniz.

`LLM` nesnelerini doğrudan kullanarak, araç çağırma ve hata işleme süreçlerini tam olarak kontrol ederken hızlı bir şekilde temel bir ajan döngüsü uygulayabilirsiniz.

```python
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI


def select_song(song_name: str) -> str:
    """Bir şarkı seçmek için kullanışlıdır."""
    return f"Şarkı seçildi: {song_name}"


tools = [FunctionTool.from_defaults(select_song)]
tools_by_name = {t.metadata.name: t for t in [tool]}

# llm'i başlangıç araçları + sohbet geçmişi ile çağırın
chat_history = [ChatMessage(role="user", content="Benim için rastgele bir şarkı seç")]
resp = llm.chat_with_tools([tool], chat_history=chat_history)

# yanıttan araç çağrılarını ayrıştırın
tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_call=False
)

# çağrılacak daha fazla araç olduğu sürece döngüye girin
while tool_calls:
    # LLM'in yanıtını sohbet geçmişine ekleyin
    chat_history.append(resp.message)

    # her aracı çağırın ve sonucunu chat_history'e ekleyin
    for tool_call in tool_calls:
        tool_name = tool_call.tool_name
        tool_kwargs = tool_call.tool_kwargs

        print(f"{tool_name}, {tool_kwargs} ile çağrılıyor")
        tool_output = tool(**tool_kwargs)
        chat_history.append(
            ChatMessage(
                role="tool",
                content=str(tool_output),
                # OpenAI gibi çoğu LLM'in araç çağrı kimliğini (tool call id) bilmesi gerekir
                additional_kwargs={"tool_call_id": tool_call.tool_id},
            )
        )

        # LLM'in nihai bir yanıt yazıp yazamadığını veya daha fazla araç çağırıp çağırmadığını kontrol edin
        resp = llm.chat_with_tools([tool], chat_history=chat_history)
        tool_calls = llm.get_tool_calls_from_response(
            resp, error_on_no_tool_call=False
)

# nihai yanıtı yazdırın
print(resp.message.content)
```

## Örnekler / Modül Kılavuzları

Erişilebilen örneklerin ve modül kılavuzlarının daha eksiksiz bir listesini [modül kılavuzları sayfasında](/python/framework/module_guides/deploying/agents/modules) bulabilirsiniz.