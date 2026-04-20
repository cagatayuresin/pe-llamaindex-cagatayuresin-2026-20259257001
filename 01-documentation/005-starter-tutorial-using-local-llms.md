# Başlangıç Eğitimi (Yerel LLM'ler Kullanarak)

Bu eğitim, LlamaIndex ile ajanlar (agents) oluşturmaya nasıl başlayacağınızı gösterecektir. Temel bir örnekle başlayacağız ve ardından RAG (Retrieval-Augmented Generation / Veri Getirme ile Güçlendirilmiş Üretim) yeteneklerini nasıl ekleyeceğinizi göstereceğiz.

Embedding modelimiz olarak [`BAAI/bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5) kullanacağız ve LLM olarak `Ollama` üzerinden sunulan `llama3.1 8B` modelini kullanacağız.

> **İpucu:** Devam etmeden önce [kurulum](/python/framework/getting_started/installation) adımlarını tamamladığınızdan emin olun.

## Kurulum

Ollama, LLM'leri minimum kurulumla yerel olarak çalıştırmanıza yardımcı olan bir araçtır.

Nasıl kurulacağını öğrenmek için [README](https://github.com/jmorganca/ollama) sayfasını takip edin.

Llama3 modelini indirmek için `ollama pull llama3.1` komutunu çalıştırmanız yeterlidir.

**NOT**: En az yaklaşık 32GB RAM'e sahip bir makineye ihtiyacınız olacaktır.

[Kurulum kılavuzumuzda](/python/framework/getting_started/installation) açıklandığı gibi, `llama-index` aslında bir paket koleksiyonudur. Ollama ve Huggingface'i çalıştırmak için şu entegrasyonları kurmamız gerekecek:

```bash
pip install llama-index-llms-ollama llama-index-embeddings-huggingface
```

Paket isimleri import yollarını doğrudan belirtir, bu da onları nasıl import edeceğinizi veya kuracağınızı hatırlamanıza yardımcı olur!

```python
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
```

Daha fazla entegrasyon için [https://llamahub.ai](https://llamahub.ai) adresine göz atabilirsiniz.

## Temel Ajan Örneği

Bir araç (tool) çağırarak temel çarpma işlemi yapabilen basit bir ajan örneğiyle başlayalım. `starter.py` adında bir dosya oluşturun:

```python
import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama


# Basit bir hesap makinesi aracı tanımlayın
def multiply(a: float, b: float) -> float:
    """İki sayıyı çarpmak için kullanışlıdır."""
    return a * b


# Hesap makinesi aracımızla bir ajan iş akışı oluşturun
agent = FunctionAgent(
    tools=[multiply],
    llm=Ollama(
        model="llama3.1",
        request_timeout=360.0,
        # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
        context_window=8000,
    ),
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

Bu kod şuna benzer bir çıktı verecektir: `1234 * 4567 işleminin cevabı 5635678'dir.`

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

Artık LlamaIndex kullanarak dökümanlarda arama yapacak bir araç oluşturabiliriz. Varsayılan olarak `VectorStoreIndex` yapımız, metni gömmek (embed) ve getirmek için OpenAI'dan `text-embedding-ada-002` embedding modelini kullanacaktır. Ancak biz burada yerel modellerimizi kullanacağız.

Güncellenmiş `starter.py` dosyanız şu şekilde görünmelidir:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import asyncio
import os

# Ayarlar (Settings) global varsayılanları kontrol eder
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(
    model="llama3.1",
    request_timeout=360.0,
    # Bellek kullanımını sınırlamak için bağlam penceresini manuel olarak ayarlayın
    context_window=8000,
)

# LlamaIndex kullanarak bir RAG aracı oluşturun
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    # burada opsiyonel olarak embed_model'i geçersiz kılabiliriz
    # embed_model=Settings.embed_model,
)
query_engine = index.as_query_engine(
    # burada opsiyonel olarak llm'i geçersiz kılabiliriz
    # llm=Settings.llm,
)


def multiply(a: float, b: float) -> float:
    """İki sayıyı çarpmak için kullanışlıdır."""
    return a * b


async def search_documents(query: str) -> str:
    """Paul Graham tarafından yazılan kişisel bir makale hakkındaki doğal dil sorularını yanıtlamak için kullanışlıdır."""
    response = await query_engine.aquery(query)
    return str(response)


# Her iki araçla güçlendirilmiş bir iş akışı oluşturun
agent = AgentWorkflow.from_tools_or_functions(
    [multiply, search_documents],
    llm=Settings.llm,
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
index = load_index_from_storage(
    storage_context,
    # burada opsiyonel olarak embed_model'i geçersiz kılabiliriz
    # indeksi oluştururken kullanılan aynı embed_model'i kullanmak önemlidir
    # embed_model=Settings.embed_model,
)
query_engine = index.as_query_engine(
    # burada opsiyonel olarak llm'i geçersiz kılabiliriz
    # llm=Settings.llm,
)
```

> **İpucu:** Eğer varsayılanın dışında bir [vektör deposu entegrasyonu](/python/framework/module_guides/storing/vector_stores) kullandıysanız, muhtemelen sadece vektör deposundan yeniden yükleyebilirsiniz:

```python
index = VectorStoreIndex.from_vector_store(
    vector_store,
    # indeksi oluştururken kullanılan aynı embed_model'i kullanmak önemlidir
    # embed_model=Settings.embed_model,
)
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