# Başlangıç Eğitimi (OpenAI Kullanarak)

Bu eğitim, LlamaIndex ile ajanlar (agents) oluşturmaya nasıl başlayacağınızı gösterecektir. Temel bir örnekle başlayacağız ve ardından RAG (Retrieval-Augmented Generation / Veri Getirme ile Güçlendirilmiş Üretim) yeteneklerini nasıl ekleyeceğinizi göstereceğiz.

> **İpucu:** Devam etmeden önce [kurulum](/python/framework/getting_started/installation) adımlarını tamamladığınızdan emin olun.

> **İpucu:** Yerel modelleri mi kullanmak istiyorsunuz? Eğer bu başlangıç eğitimini sadece yerel modeller kullanarak yapmak isterseniz, [bu eğitim dosyasına göz atın](/python/framework/getting_started/starter_example_local).

## OpenAI API Anahtarınızı Ayarlayın

LlamaIndex varsayılan olarak OpenAI'ın `gpt-3.5-turbo` modelini kullanır. API anahtarınızın kodunuz tarafından erişilebilir olması için anahtarı bir ortam değişkeni (environment variable) olarak ayarlayın:

```bash
# MacOS/Linux
export OPENAI_API_KEY=XXXXX

# Windows
set OPENAI_API_KEY=XXXXX
```

> **İpucu:** Eğer OpenAI uyumlu bir API kullanıyorsanız, `OpenAILike` LLM sınıfını kullanabilirsiniz. Daha fazla bilgiyi [OpenAILike LLM](https://docs.llamaindex.ai/en/stable/api_reference/llms/openai_like/) entegrasyonu ve [OpenAILike Embeddings](https://docs.llamaindex.ai/en/stable/api_reference/embeddings/openai_like/) entegrasyonu sayfalarında bulabilirsiniz.

## Temel Ajan Örneği

Bir araç (tool) çağırarak temel çarpma işlemi yapabilen basit bir ajan örneğiyle başlayalım. `starter.py` adında bir dosya oluşturun:

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
    system_prompt="Siz iki sayıyı çarpabilen yardımcı bir asistansınız.",
)


async def main():
    # Ajanı çalıştırın
    response = await agent.run("1234 * 4567 nedir?")
    print(str(response))


# Ajanı çalıştırın
if __name__ == "__main__":
    asyncio.run(main())
```

Bu kod şuna benzer bir çıktı verecektir: `1234 * 4567 işleminin sonucu 5,678,678'dir.`

Süreç şu şekilde işledi:

- Ajana bir soru soruldu: `1234 * 4567 nedir?`
- Arka planda bu soru, araçların şemasıyla (isim, docstring ve argümanlar) birlikte LLM'e iletildi.
- Ajan `multiply` aracını seçti ve aracın argümanlarını yazdı.
- Ajan araçtan sonucu aldı ve bunu nihai yanıta ekledi.

> **İpucu:** Gördüğünüz gibi `async` Python fonksiyonlarını kullanıyoruz. Birçok LLM ve model asenkron (async) çağrıları destekler; uygulamanızın performansını artırmak için asenkron kod kullanmanız önerilir. Asenkron kod ve Python hakkında daha fazla bilgi edinmek için [Python'da Asenkron Programlama](/python/framework/getting_started/async_python) bölümünü incelemenizi öneririz.

## Sohbet Geçmişi Ekleme

`AgentWorkflow` ayrıca önceki mesajları hatırlama yeteneğine sahiptir. Bu bilgi, `AgentWorkflow` içindeki `Context` nesnesinde tutulur.

Eğer `Context` ajana geçilirse, ajan bunu konuşmayı devam ettirmek için kullanacaktır.

```python
from llama_index.core.workflow import Context

# bağlam (context) oluşturun
ctx = Context(agent)

# ajanı bağlam ile çalıştırın
response = await agent.run("Benim adım Logan", ctx=ctx)
response = await agent.run("Benim adım ne?", ctx=ctx)
```

## RAG Yetenekleri Ekleme

Şimdi ajanımızı dökümanlar içinde arama yapma yeteneğiyle güçlendirelim. Öncelikle terminalimizi kullanarak bazı örnek veriler alalım:

```bash
mkdir data
wget https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt -O data/paul_graham_essay.txt
```

Dizin yapınız şu şekilde görünmelidir:

```text
├── starter.py
└── data
    └── paul_graham_essay.txt
```

Artık LlamaIndex kullanarak dökümanlarda arama yapacak bir araç oluşturabiliriz. Varsayılan olarak `VectorStoreIndex` yapımız, metni gömmek (embed) ve getirmek için OpenAI'dan `text-embedding-ada-002` embedding modelini kullanacaktır.

Güncellenmiş `starter.py` dosyanız şu şekilde görünmelidir:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
import asyncio
import os

# LlamaIndex kullanarak bir RAG aracı oluşturun
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()


def multiply(a: float, b: float) -> float:
    """İki sayıyı çarpmak için kullanışlıdır."""
    return a * b


async def search_documents(query: str) -> str:
    """Paul Graham tarafından yazılan kişisel bir makale hakkındaki doğal dil sorularını yanıtlamak için kullanışlıdır."""
    response = await query_engine.aquery(query)
    return str(response)


# Her iki araçla güçlendirilmiş bir iş akışı oluşturun
agent = FunctionAgent(
    tools=[multiply, search_documents],
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="""Siz, hesaplamalar yapabilen ve soruları yanıtlamak için 
    dökümanlar arasında arama yapabilen yardımcı bir asistansınız.""",
)


# Artık dökümanlar hakkında sorular sorabilir veya hesaplamalar yapabiliriz
async def main():
    response = await agent.run(
        "Yazar üniversitede ne yaptı? Ayrıca, 7 * 8 kaç eder?"
    )
    print(response)


# Ajanı çalıştırın
if __name__ == "__main__":
    asyncio.run(main())
```

Ajan artık soruları yanıtlamak için hesap makinesi kullanmak ile dökümanlar arasında arama yapmak arasında sorunsuz bir şekilde geçiş yapabilir.

## RAG İndeksini Saklama

Dökümanları her seferinde yeniden işlememek için indeksi diske kaydedebilirsiniz:

```python
# İndeksi kaydedin
index.storage_context.persist("storage")

# Daha sonra indeksi yükleyin
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
```

> **İpucu:** Eğer varsayılanın dışında bir [vektör deposu entegrasyonu](/python/framework/module_guides/storing/vector_stores) kullandıysanız, muhtemelen sadece vektör deposundan yeniden yükleyebilirsiniz:

```python
index = VectorStoreIndex.from_vector_store(vector_store)
```

## Sırada Ne Var?

Bu, LlamaIndex ajanlarıyla yapabileceklerinizin sadece başlangıcı! Şunları yapabilirsiniz:

- Ajanınıza daha fazla araç eklemek
- Farklı LLM'ler kullanmak
- Sistem komutlarını (system prompts) kullanarak ajanın davranışını özelleştirmek
- Akış (streaming) yetenekleri eklemek
- "Döngüde insan" (human-in-the-loop) iş akışlarını uygulamak
- Görevlerde iş birliği yapmak için birden fazla ajan kullanmak

İlgili bazı bağlantılar:

- [Ajan dökümantasyonumuzda](/python/framework/understanding/agent) daha gelişmiş ajan örneklerini görün
- [Üst düzey kavramlar](/python/framework/getting_started/concepts) hakkında daha fazla bilgi edinin
- [Nelerin özelleştirilebileceğini](/python/framework/getting_started/faq) keşfedin
- [Bileşen kılavuzlarını](/python/framework/module_guides) inceleyin