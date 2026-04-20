# Bir Ajan Oluşturmak

LlamaIndex'te bir ajan (agent), kendisine bir görev verilen ve bu görevi çözmek için bir dizi adımı yürüten, bir LLM tarafından desteklenen yarı otonom bir yazılım parçasıdır. Ajana, basit fonksiyonlardan tam teşekküllü LlamaIndex sorgu motorlarına kadar her şey olabilen bir dizi araç (tools) verilir ve ajan her adımı tamamlamak için mevcut en iyi aracı seçer. Her adım tamamlandığında ajan; görevin tamamlanıp tamamlanmadığına karar verir. Görev tamamlanmışsa kullanıcıya bir sonuç döndürür, aksi takdirde başka bir adım atması gerekiyorsa döngünün başına geri döner.

LlamaIndex'te, "İş Akışları Oluşturma" bölümünde ele alınan [kendi ajan iş akışlarınızı sıfırdan oluşturabilir](/python/llamaagents/workflows) veya `FunctionAgent` (basit bir fonksiyon/araç çağıran ajan) veya `AgentWorkflow` (birden fazla ajanı yönetebilen bir ajan) gibi önceden oluşturulmuş ajan iş akışlarımızı kullanabilirsiniz. Bu eğitim, `FunctionAgent` kullanarak bir fonksiyon çağıran ajan oluşturmayı kapsar.

Çoklu ajan sistemleri oluşturmanın çeşitli yollarını öğrenmek için ["Çoklu ajan sistemleri"](/python/framework/understanding/agent/multi_agent) sayfasını inceleyin.

![ajan akışı](./agent_flow.png)

## Başlarken

Tüm bu kodları [ajan eğitimi deposunda](https://github.com/run-llama/python-agents-tutorial) bulabilirsiniz.

Çakışmaları önlemek ve her şeyi temiz tutmak için yeni bir Python sanal ortamı (virtual environment) başlatacağız. Herhangi bir sanal ortam yöneticisi kullanabilirsiniz, ancak biz burada `poetry` kullanacağız:

```bash
poetry init
poetry shell
```

Ardından LlamaIndex kütüphanesini ve işimize yarayacak diğer bazı bağımlılıkları kuracağız:

```bash
pip install llama-index-core llama-index-llms-openai python-dotenv
```

Bunlardan herhangi birinde sorun yaşarsanız, daha ayrıntılı [kurulum kılavuzumuza](/python/framework/getting_started/installation) göz atın.

## OpenAI Anahtarı

Ajanımız OpenAI'ın `gpt-4o-mini` LLM'i tarafından desteklenecek, bu nedenle bir [API anahtarına](https://platform.openai.com/) ihtiyacınız olacak. Anahtarınızı aldıktan sonra, projenizin kök dizininde bir `.env` dosyasına yerleştirebilirsiniz:

```bash
OPENAI_API_KEY=sk-proj-xxxx
```

Eğer OpenAI kullanmak istemiyorsanız, yerel modeller dahil [diğer herhangi bir LLM'i](/python/framework/understanding/using_llms) kullanabilirsiniz. Ajanlar yetenekli modeller gerektirir, bu nedenle daha küçük modeller daha az güvenilir olabilir.

## Bağımlılıkları Dahil Etme

İhtiyacımız olan LlamaIndex bileşenlerini import ederek ve `.env` dosyamızdaki ortam değişkenlerini yükleyerek başlayacağız:

```python
from dotenv import load_dotenv

load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
```

## Temel Araçları Oluşturma

Bu basit örnek için iki araç oluşturacağız: biri sayıları çarpmayı bilen, diğeri ise onları toplamayı bilen araçlar.

```python
def multiply(a: float, b: float) -> float:
    """İki sayıyı çarpar ve sonucu (product) döndürür"""
    return a * b


def add(a: float, b: float) -> float:
    """İki sayıyı toplar ve toplamı (sum) döndürür"""
    return a + b
```

Gördüğünüz gibi, bunlar normal Python fonksiyonlarıdır. Hangi aracın kullanılacağına karar verirken ajanınız; aracın adını, parametrelerini ve docstring'ini (fonksiyon açıklamasını) kullanarak aracın ne yaptığını ve eldeki görev için uygun olup olmadığını belirleyecektir. Bu nedenle docstring'lerin açıklayıcı ve yardımcı olduğundan emin olmak önemlidir. Ajan ayrıca beklenen parametreleri ve dönüş tipini belirlemek için tip ipuçlarını (type hints) da kullanacaktır.

## LLM'i Başlatma

Bugün işi `gpt-4o-mini` yapacak:

```python
llm = OpenAI(model="gpt-4o-mini")
```

Ayrıca API üzerinden erişilebilen [Mistral](/python/examples/llm/mistralai), [Anthropic'ten Claude](/python/examples/llm/anthropic) veya [Google'dan Gemini](/python/examples/llm/google_genai) gibi diğer popüler modelleri de seçebilirsiniz.

## Ajanı Başlatma

Şimdi ajanımızı oluşturuyoruz. Bir araç dizisine, bir LLM'e ve ne tür bir ajan olacağını söyleyen bir sistem komutuna (system prompt) ihtiyacı var. Sistem komutunuz genellikle bundan daha detaylı olacaktır!

```python
workflow = FunctionAgent(
    tools=[multiply, add],
    llm=llm,
    system_prompt="Siz, araçları kullanarak temel matematiksel işlemleri gerçekleştirebilen bir ajansınız.",
)
```

GPT-4o-mini aslında bu kadar basit bir matematiği yapmak için araçlara ihtiyaç duymayacak kadar akıllıdır; bu yüzden komutta araçları kullanması gerektiğini belirttik.

`FunctionAgent` dışında LlamaIndex'te araçları yürütmek için farklı komut stratejileri kullanan [`ReActAgent`](/python/examples/agent/react_agent) ve [`CodeActAgent`](/python/examples/agent/code_act_agent) gibi başka ajanlar da mevcuttur.

## Bir Soru Sorun

Artık ajandan biraz matematik yapmasını isteyebiliriz:

```python
response = await workflow.run(user_msg="20+(2*4) nedir?")
print(response)
```

Bunun asenkron bir kod olduğunu unutmayın. Bir notebook ortamında çalışacaktır, ancak normal Python'da çalıştırmak isterseniz onu şu şekilde asenkron bir fonksiyon içine sarmanız gerekecektir:

```python
async def main():
    response = await workflow.run(user_msg="20+(2*4) nedir?")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

Bu size aşağıdakine benzer bir çıktı vermelidir:

```text
(20 + (2 çarpı 4)) işleminin sonucu 28'dir.
```

> **İpucu:** Bazı modeller akışlı (streaming) LLM çıktısını desteklemeyebilir. Akış özelliği varsayılan olarak etkindi olsa da, bir hatayla karşılaşırsanız akışı devre dışı bırakmak için her zaman `FunctionAgent(..., streaming=False)` ayarını yapabilirsiniz.

Kodun son halinin nasıl görünmesi gerektiğini görmek için [repoya](https://github.com/run-llama/python-agents-tutorial/blob/main/1_basic_agent.py) göz atın.

Tebrikler! En temel ajan türünü oluşturdunuz. Sırada [hazır araçları](/python/framework/understanding/agent/tools) nasıl kullanacağımızı öğrenelim.