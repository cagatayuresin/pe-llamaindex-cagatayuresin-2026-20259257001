# Çıkış ve Olay Akışı (Streaming)

Gerçek dünyadaki kullanımda, ajanların çalışması uzun zaman alabilir. Ajanın ilerleyişi hakkında kullanıcıya geri bildirim sağlamak kritiktir ve akış (streaming) bunu yapmanıza olanak tanır.

`AgentWorkflow`, kullanıcıya çıktı akışı sağlamak için kullanabileceğiniz bir dizi önceden oluşturulmuş olay sunar. Bunun nasıl yapıldığına bir göz atalım.

> **İpucu:** Bazı modeller akışlı LLM çıktısını desteklemeyebilir. Akış özelliği varsayılan olarak etkin olsa da, bir hatayla karşılaşırsanız akışı devre dışı bırakmak için her zaman `FunctionAgent(..., streaming=False)` ayarını yapabilirsiniz.

İlk olarak, yürütülmesi biraz zaman alan yeni bir araç tanıtacağız. Bu durumda, LlamaHub'da bulunan [Tavily](https://llamahub.ai/l/tools/llama-index-tools-tavily-research) adlı bir web arama aracını kullanacağız.

```bash
pip install llama-index-tools-tavily-research
```

Bu araç bir API anahtarı gerektirir; anahtarı `.env` dosyamıza `TAVILY_API_KEY` olarak ayarlayacağız ve `os.getenv` metodunu kullanarak geri alacağız. Importlarımızı yapalım:

```python
from llama_index.tools.tavily_research import TavilyToolSpec
import os
```

Ve aracı başlatalım:

```python
tavily_tool = TavilyToolSpec(api_key=os.getenv("TAVILY_API_KEY"))
```

Şimdi bu aracı ve daha önce yaptığımız gibi başlattığımız bir LLM'i kullanan bir ajan oluşturacağız.

```python
workflow = FunctionAgent(
    tools=tavily_tool.to_tool_list(),
    llm=llm,
    system_prompt="Siz bilgi için web'de arama yapabilen yardımcı bir asistansınız.",
)
```

Önceki örneklerde, ajandan nihai yanıtı almak için `workflow.run` metodu üzerinde `await` kullandık. Ancak, yanıtı beklemezsek (await etmezsek), olaylar geldikçe üzerinde döngü kurabileceğimiz asenkron bir iteratör (iterator) alırız. Bu iteratör her türlü olayı döndürecektir. Çıktı geldikçe çıktıdaki "delta"yı (en son değişikliği) içeren bir `AgentStream` olayıyla başlayacağız. Bu olay tipini import etmemiz gerekiyor:

```python
from llama_index.core.agent.workflow import AgentStream
```

Ve şimdi iş akışını çalıştırabilir ve çıktı üretmek için bu tipteki olayları arayabiliriz:

```python
handler = workflow.run(user_msg="San Francisco'da hava nasıl?")

async for event in handler.stream_events():
    if isinstance(event, AgentStream):
        print(event.delta, end="", flush=True)
```

Bunu kendiniz çalıştırırsanız, ajan çalışırken çıktının parçalar halinde geldiğini göreceksiniz ve şuna benzer bir sonuç dönecektir:

```text
San Francisco'daki mevcut hava durumu şu şekildedir:

- **Sıcaklık**: 17,2°C (63°F)
- **Durum**: Güneşli
- **Rüzgar**: Kuzey-Kuzeybatı'dan 6,3 mil/saat (10,1 km/saat)
- **Nem**: %54
- **Basınç**: 1021 mb (30,16 in)
- **Görünürlük**: 16 km (9 mil)

Daha fazla ayrıntı için tam raporu [buradan](https://www.weatherapi.com/) kontrol edebilirsiniz.
```

`AgentStream`, `AgentWorkflow` çalışırken yayınladığı birçok olaydan sadece biridir. Diğerleri şunlardır:

- `AgentInput`: Ajanın yürütülmesini başlatan tam mesaj nesnesi
- `AgentOutput`: Ajandan gelen yanıt
- `ToolCall`: Hangi araçların hangi argümanlarla çağrıldığı
- `ToolCallResult`: Bir araç çağrısının sonucu

Bu olaylardan daha fazlasını nasıl filtrelediğimizi [bu örneğin tam kodunda](https://github.com/run-llama/python-agents-tutorial/blob/main/4_streaming.py) görebilirsiniz.

Sırada, ajanlarınıza geri bildirim sağlamak için [döngüde bir insan (human-in-the-loop)](/python/framework/understanding/agent/human_in_the_loop) nasıl dahil edilir öğreneceksiniz.