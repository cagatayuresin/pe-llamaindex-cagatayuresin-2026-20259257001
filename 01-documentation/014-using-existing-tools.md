# Mevcut Araçları Kullanma

Artık yetenekli bir ajan oluşturduğunuza göre, onun yapabilecekleri konusunda heyecanlı olduğunuzu umuyoruz. Ajan yeteneklerini genişletmenin temelinde mevcut araçlar yatar ve size iyi bir haberimiz var: LlamaIndex'in [LlamaHub](https://llamahub.ai) platformu, hemen kullanabileceğiniz [onlarca mevcut ajan aracı](https://llamahub.ai/?tab=tools) dahil olmak üzere yüzlerce entegrasyona sahiptir. Size mevcut araçlardan birini nasıl kullanacağınızı ve ayrıca kendi araçlarınızı nasıl oluşturup katkıda bulunacağınızı göstereceğiz.

## LlamaHub'dan Mevcut Bir Aracı Kullanma

Örneğimiz için LlamaHub'daki [Yahoo Finance aracını](https://llamahub.ai/l/tools/llama-index-tools-yahoo-finance?from=tools) kullanacağız. Bu araç, hisse senedi sembolleri (tickers) hakkında çeşitli bilgileri arayan altı adet ajan aracından oluşan bir set sunar.

Öncelikle aracı kurmamız gerekiyor:

```bash
pip install llama-index-tools-yahoo-finance
```

Bağımlılıklarımız önceki örneğimizle aynıdır, sadece Yahoo Finance araçlarını eklememiz gerekiyor:

```python
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
```

Özel araçları LlamaHub araçlarıyla nasıl birleştirebileceğinizi göstermek için, burada ihtiyacımız olmasa bile `add` ve `multiply` fonksiyonlarını yerinde bırakacağız. Araçlarımızı dahil ediyoruz:

```python
finance_tools = YahooFinanceToolSpec().to_tool_list()
```

Bir araç listesi aslında bir dizidir, bu nedenle kendi araçlarımızı karışıma eklemek için Python'ın `extend` metodunu kullanabiliriz:

```python
finance_tools.extend([multiply, add])
```

Ve bu sefer yeni araçların kullanılmasını gerektiren farklı bir soru soracağız:

```python
workflow = FunctionAgent(
    name="Agent",
    description="Finansal işlemleri gerçekleştirmek için kullanışlıdır.",
    llm=OpenAI(model="gpt-4o-mini"),
    tools=finance_tools,
    system_prompt="Siz yardımcı bir asistansınız.",
)


async def main():
    response = await workflow.run(
        user_msg="NVIDIA'nın şu anki hisse senedi fiyatı nedir?"
    )
    print(response)
```

Şu yanıtı alıyoruz:

```text
NVIDIA Corporation'ın (NVDA) şu anki hisse senedi fiyatı 128,41$'dır.
```

(Bu biraz hile sayılır, çünkü modelimiz NVIDIA'nın hisse senedi sembolünü zaten biliyordu. Eğer daha az tanınan bir şirket olsaydı, sembolü bulmak için [Tavily](https://llamahub.ai/l/tools/llama-index-tools-tavily-research) gibi bir arama aracı eklemeniz gerekirdi.)

İşte bu kadar! Artık LlamaHub'daki araçlardan herhangi birini ajanlarınızda kullanabilirsiniz.

Her zaman olduğu gibi, bu kodun tamamını bir arada görmek için [repoya](https://github.com/run-llama/python-agents-tutorial/blob/main/2_tools.py) göz atabilirsiniz.

## Kendi Araçlarınızı Oluşturma ve Katkıda Bulunma

Yeni araçların açık kaynaklı katkılarını çok seviyoruz! Yahoo finance aracının [kodunun nasıl göründüğüne dair bir örneği](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-yahoo-finance/llama_index/tools/yahoo_finance/base.py) inceleyebilirsiniz:

- `BaseToolSpec` sınıfını genişleten bir sınıf
- Bir dizi bağımsız Python fonksiyonu
- Fonksiyonları aracın API'sine eşleyen bir `spec_functions` listesi

Bir aracı çalıştırdıktan sonra, metadataları doğru şekilde ayarlamak ve bir pull request göndermek için talimatlar içeren [katkı kılavuzumuzu (contributing guide)](https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md#2--contribute-a-pack-reader-tool-or-dataset-formerly-from-llama-hub) takip edin.

Sırada, ajanlarınızda [durumu (state) nasıl koruyacağınıza](/python/framework/understanding/agent/state) bakacağız.