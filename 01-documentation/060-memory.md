# Bellek (Memory)

## Kavram

Bellek, ajanlı sistemlerin temel bir bileşenidir. Geçmişten gelen bilgileri saklamanıza ve geri getirmenize (retrieve) olanak tanır.

LlamaIndex'te bellek genellikle mevcut bir `BaseMemory` sınıfı kullanılarak veya özel bir tane oluşturularak özelleştirilebilir.

Ajan çalıştıkça, bilgi saklamak için `memory.put()` ve bilgi getirmek için `memory.get()` çağrıları yapacaktır.

**NOT:** `ChatMemoryBuffer` artık kullanılmamaktadır (deprecated). Gelecek bir sürümde varsayılanın yerini, daha esnek olan ve daha karmaşık bellek yapılandırmalarına izin veren `Memory` sınıfı alacaktır. Bu bölümdeki örneklerde `Memory` sınıfı kullanılacaktır. Varsayılan olarak çerçeve genelinde, ajana bir token sınırına sığan son X mesajı veren temel bir sohbet geçmişi arabelleği (buffer) oluşturmak için `ChatMemoryBuffer` kullanılır. `Memory` sınıfı da benzer şekilde çalışır ancak daha esnektir ve daha karmaşık bellek yapılandırmalarına olanak tanır.

## Kullanım

`Memory` sınıfını kullanarak, hem kısa süreli belleğe (yani mesajların FIFO -ilk giren ilk çıkar- kuyruğu) hem de isteğe bağlı olarak uzun süreli belleğe (yani zamanla bilgi çıkarma) sahip bir bellek oluşturabilirsiniz.

### Bir Ajan İçin Belleği Yapılandırma

Bir ajanın belleğini `run()` metoduna geçirerek ayarlayabilirsiniz:

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.memory import Memory

memory = Memory.from_defaults(session_id="oturum_kimligim", token_limit=40000)

agent = FunctionAgent(llm=llm, tools=tools)

response = await agent.run("<aracı çağıran soru>", memory=memory)
```

### Belleği Manuel Olarak Yönetme

Sohbet geçmişini içeri aktararak ve doğrudan `memory.put_messages()` ve `memory.get()` yöntemlerini çağırarak da belleği manuel olarak yönetebilirsiniz.

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import Memory


memory = Memory.from_defaults(session_id="oturum_kimligim", token_limit=40000)
memory.put_messages(
    [
        ChatMessage(role="user", content="Merhaba dünya!"),
        ChatMessage(role="assistant", content="Sana da merhaba dünya!"),
    ]
)
chat_history = memory.get()

agent = FunctionAgent(llm=llm, tools=tools)

# sohbet geçmişini içeri aktarmak, mevcut tüm bellekleri geçersiz kılar
response = await agent.run(
    "<aracı çağıran soru>", chat_history=chat_history
)
```

### Bir Ajandan En Son Belleği Getirme

Ajan bağlamından (context) çekerek bir ajandaki en son belleği alabilirsiniz:

```python
from llama_index.core.workflow import Context

ctx = Context(agent)

response = await ctx.run("<aracı çağıran soru>", ctx=ctx)

# belleği al
memory = await ctx.store.get("memory")
chat_history = memory.get()
```

## Belleği Özelleştirme

### Kısa Süreli Bellek (Short-Term Memory)

Varsayılan olarak `Memory` sınıfı, bir token sınırına sığan son X mesajı saklayacaktır. Bunu `token_limit` ve `chat_history_token_ratio` argümanlarını `Memory` sınıfına geçirerek özelleştirebilirsiniz.

-   `token_limit` (varsayılan: 30000): Saklanacak maksimum kısa süreli ve uzun süreli token sayısı.
-   `chat_history_token_ratio` (varsayılan: 0.7): Toplam token sınırına oranla kısa süreli sohbet geçmişindeki tokenlerin oranı. Sohbet geçmişi bu oranı aşarsa, en eski mesajlar uzun süreli belleğe aktarılır (uzun süreli bellek etkinse).
-   `token_flush_size` (varsayılan: 3000): Sohbet geçmişi token sınırını aştığında uzun süreli belleğe aktarılacak token sayısı.

```python
memory = Memory.from_defaults(
    session_id="oturum_kimligim",
    token_limit=40000,
    chat_history_token_ratio=0.7,
    token_flush_size=3000,
)
```

### Uzun Süreli Bellek (Long-Term Memory)

Uzun süreli bellek, `Memory Block` (Bellek Bloğu) nesneleri olarak temsil edilir. Bu nesneler, kısa süreli bellekten boşaltılan (flushed) mesajları alır ve isteğe bağlı olarak bilgi çıkarmak için bunları işler. Ardından bellek geri getirildiğinde, kısa süreli ve uzun süreli bellekler bir araya getirilir.

Şu anda önceden tanımlanmış üç bellek bloğu bulunmaktadır:

-   `StaticMemoryBlock`: Statik bir bilgi parçasını saklayan bir bellek bloğu.
-   `FactExtractionMemoryBlock`: Sohbet geçmişinden olguları (facts) çıkaran bir bellek bloğu.
-   `VectorMemoryBlock`: Bir vektör veritabanından sohbet mesajı partilerini (batches) saklayan ve getiren bir bellek bloğu.

Varsayılan olarak `insert_method` argümanına bağlı olarak bellek blokları sistem mesajına veya en son kullanıcı mesajına eklenecektir.

Bu kulağa biraz karmaşık gelebilir, ancak aslında oldukça basittir. Bir örneğe bakalım:

```python
from llama_index.core.memory import (
    StaticMemoryBlock,
    FactExtractionMemoryBlock,
    VectorMemoryBlock,
)

blocks = [
    StaticMemoryBlock(
        name="temel_bilgi",
        static_content="Benim adım Logan ve Saskatoon'da yaşıyorum. LlamaIndex'te çalışıyorum.",
        priority=0,
    ),
    FactExtractionMemoryBlock(
        name="cıkarılan_bilgi",
        llm=llm,
        max_facts=50,
        priority=1,
    ),
    VectorMemoryBlock(
        name="vektor_bellegi",
        # gerekli: qdrant, chroma, weaviate, milvus vb. gibi bir vektör deposu geçirin
        vector_store=vector_store,
        priority=2,
        embed_model=embed_model,
        # Getirilecek en iyi k mesaj partisi
        # similarity_top_k=2,
        # isteğe bağlı: Getirme sorgusuna kaç tane önceki mesajın dahil edileceği
        # retrieval_context_window=5
        # isteğe bağlı: Benzerlik eşiği vb. gibi şeyler için isteğe bağlı node son işleyicileri geçirin
        # node_postprocessors=[...],
    ),
]
```

Burada üç bellek bloğu kurduk:

-   `core_info`: Kullanıcı hakkında bazı temel bilgileri saklayan statik bir bellek bloğu. Statik içerik bir dize veya `TextBlock`, `ImageBlock` vb. gibi `ContentBlock` nesnelerinin bir listesi olabilir. Bu bilgi her zaman belleğe eklenecektir.
-   `extracted_info`: Sohbet geçmişinden bilgi çıkaracak bir bellek bloğu. Burada, boşaltılan sohbet geçmişinden olguları çıkarmak için kullanılacak `llm`'i geçtik ve `max_facts` değerini 50 olarak ayarladık. Çıkarılan olgu sayısı bu sınırı aşarsa, yeni bilgilere yer açmak için `max_facts` otomatik olarak özetlenecek ve azaltılacaktır.
-   `vector_memory`: Bir vektör veritabanından sohbet mesajı partilerini saklayacak ve getirecek bir vektör bellek bloğu. Her parti, boşaltılan sohbet mesajlarının bir listesidir. Burada, sohbet mesajlarını saklamak ve getirmek için kullanılacak `vector_store` ve `embed_model`'i geçtik.

Ayrıca her blok için bir `priority` (öncelik) ayarladığımızı fark edeceksiniz. Bu, bellek bloklarının içeriği (yani uzun süreli bellek) + kısa süreli bellek, `Memory` nesnesindeki token sınırını aştığında yapılacak işlemi belirlemek için kullanılır.

Bellek blokları çok uzadığında otomatik olarak "kesilir" (truncated). Varsayılan olarak bu, tekrar yer açılana kadar bellekten çıkarıldıkları anlamına gelir. Bu, kendi kesme mantığını uygulayan bellek bloğu alt sınıflarıyla özelleştirilebilir.

-   `priority=0`: Bu blok her zaman bellekte tutulacaktır.
-   `priority=1, 2, 3, vb.`: Toplam kısa süreli bellek + uzun süreli bellek içeriğinin `token_limit` değerine eşit veya ondan daha az olmasına yardımcı olmak için, bellek token sınırını aştığında bellek bloklarının kesilme sırasını belirler.

Şimdi bu blokları `Memory` sınıfına geçirelim:

```python
memory = Memory.from_defaults(
    session_id="oturum_kimligim",
    token_limit=40000,
    memory_blocks=blocks,
    insert_method="system",
)
```

Bellek kullanıldıkça kısa süreli bellek dolacaktır. Kısa süreli bellek `chat_history_token_ratio` oranını aştığında, `token_flush_size` boyutuna sığan en eski mesajlar boşaltılacak ve işlenmek üzere her bir bellek bloğuna gönderilecektir.

Bellek geri getirildiğinde, kısa süreli ve uzun süreli bellekler bir araya getirilir. `Memory` nesnesi, kısa süreli bellek + uzun süreli bellek içeriğinin `token_limit` değerine eşit veya ondan daha az olmasını sağlayacaktır. Eğer daha uzunsa, kesme sırasını belirlemek için `priority` kullanılarak bellek bloklarında `.truncate()` metodu çağrılacaktır.

> **İpucu:** Varsayılan olarak tokenler tiktoken kullanılarak sayılır. Bunu özelleştirmek için, bir dize verildiğinde bir liste döndüren özel bir çağrılabilir (callable) olan `tokenizer_fn` argümanını ayarlayabilirsiniz. Listenin uzunluğu daha sonra token sayısını belirlemek için kullanılır.

Bellek yeterli bilgi topladığında, bellekten şuna benzer bir şey görebiliriz:

```python
# isteğe bağlı olarak, bellek bloklarına iletilecek olan alınacak mesajların bir listesini geçirin
chat_history = memory.get(messages=[...])

print(chat_history[0].content)
```

Bu, şuna benzer bir şey yazdıracaktır:

```
<memory>
<static_memory>
Benim adım Logan ve Saskatoon'da yaşıyorum. LlamaIndex'te çalışıyorum.
</static_memory>
<fact_extraction_memory>
<fact>Olgu 1</fact>
<fact>Olgu 2</fact>
<fact>Olgu 3</fact>
</fact_extraction_memory>
<retrieval_based_memory>
<message role='user'>Mesaj 1</message>
<message role='assistant'>Mesaj 2</message>
<message role='user'>Mesaj 3</message>
</retrieval_based_memory>
</memory>
```

Burada bellek, her bellek bloğu için özel bölümlerle birlikte sistem mesajına eklenmiştir.

## Bellek Bloklarını Özelleştirme

Önceden tanımlanmış bellek blokları mevcut olsa da, kendi özel bellek bloklarınızı da oluşturabilirsiniz.

```python
from typing import Optional, List, Any
from llama_index.core.llms import ChatMessage
from llama_index.core.memory.memory import BaseMemoryBlock


# bellek bloğunun çıktı türünü tanımlamak için jenerikleri (generics) kullanın
# str veya List[ContentBlock] olabilir
class MentionCounter(BaseMemoryBlock[str]):
    """
    Kullanıcının belirli bir ismi kaç kez zikrettiğini (mention) sayan bir bellek bloğu.
    """

    mention_name: str = "Logan"
    mention_count: int = 0

    async def _aget(
        self, messages: Optional[List[ChatMessage]] = None, **block_kwargs: Any
    ) -> str:
        return f"Logan'dan {self.mention_count} kez bahsedildi."

    async def _aput(self, messages: List[ChatMessage]) -> None:
        for message in messages:
            if self.mention_name in message.content:
                self.mention_count += 1

    async def atruncate(
        self, content: str, tokens_to_truncate: int
    ) -> Optional[str]:
        return ""
```

Burada, kullanıcının belirli bir ismi kaç kez zikrettiğini sayan bir bellek bloğu tanımladık. Kesme metodu temeldir, sadece boş bir dize döndürür.

### Uzak Bellek (Remote Memory)

Varsayılan olarak `Memory` sınıfı, bellek içi (in-memory) bir SQLite veritabanı kullanmaktadır. Veritabanı URI'sini değiştirerek herhangi bir uzak veritabanını sisteme dahil edebilirsiniz.

Tablo adını özelleştirebilir ve isteğe bağlı olarak doğrudan asenkron bir motor (engine) geçirebilirsiniz. Bu, kendi bağlantı havuzunuzu yönetmek için kullanışlıdır.

```python
from llama_index.core.memory import Memory

memory = Memory.from_defaults(
    session_id="oturum_kimligim",
    token_limit=40000,
    async_database_uri="postgresql+asyncpg://postgres:password@localhost:5432/postgres",
    # İsteğe bağlı: bir tablo adı belirtin
    # table_name="bellek_tablosu",
    # İsteğe bağlı: doğrudan asenkron bir motor geçirin
    # bu, kendi bağlantı havuzunuzu yönetmek için kullanışlıdır
    # async_engine=engine,
)
```

## Bellek vs. İş Akışı Bağlamı (Memory vs. Workflow Context)

Dökümantasyonun bu noktasında, bir İş Akışı (Workflow) kullandığınız ve belirli bir iş akışı durumunu kaydetmek ve devam ettirmek için bir `Context` nesnesini serileştirdiğiniz durumlarla karşılaşmış olabilirsiniz. İş akışı `Context`'i, iş akışı hakkındaki çalışma zamanı bilgilerini ve iş akışı adımları arasında paylaşılan anahtar/değer çiftlerini tutan karmaşık bir nesnedir.

Buna karşılık `Memory` nesnesi daha basit bir nesnedir; sadece `ChatMessage` nesnelerini ve isteğe bağlı olarak uzun süreli bellek için bir `MemoryBlock` nesnesi listesini tutar.

Çoğu pratik durumda her ikisini de kullanacaksınız. Belleği özelleştirmiyorsanız, `Context` nesnesini serileştirmek yeterli olacaktır.

```python
from llama_index.core.workflow import Context

ctx = Context(workflow)

# bağlamı serileştir
ctx_dict = ctx.to_dict()

# bağlamı geri yükle (deserialize)
ctx = Context.from_dict(workflow, ctx_dict)
```

`FunctionAgent`, `AgentWorkflow` veya `ReActAgent` kullanırken olduğu gibi belleği özelleştirdiğiniz diğer durumlarda, bunu ayrı bir çalışma zamanı argümanı olarak sağlamak isteyeceksiniz (özellikle varsayılanın ötesinde, `Memory` nesnesi serileştirilebilir olmadığı için).

```python
response = await agent.run("Merhaba!", memory=memory)
```

Son olarak, hem `Context`'i (iş akışını devam ettirmek için) hem de `Memory`'yi (sohbet geçmişini saklamak için) sağlamanız gereken durumlar ([süreçte insan (human-in-the-loop) gibi](/python/framework/understanding/agent/human_in_the_loop)) vardır.

```python
response = await agent.run("Merhaba!", ctx=ctx, memory=memory)
```

## (Eski/Kullanımdan Kaldırılan) Bellek Türleri

`llama_index.core.memory` altında birkaç farklı bellek türü sunuyoruz:

-   `ChatMemoryBuffer`: Bir token sınırına sığan son X mesajı saklayan temel bir bellek arabelleği.
-   `ChatSummaryMemoryBuffer`: Token sınırına sığan son X mesajı saklayan ve aynı zamanda sohbet çok uzadığında periyodik olarak özetleyen bir bellek arabelleği.
-   `VectorMemory`: Sohbet mesajlarını bir vektör veritabanından saklayan ve getiren bir bellek. Mesajların sırası hakkında garanti vermez ve en son kullanıcı mesajına en benzer mesajları döndürür.
-   `SimpleComposableMemory`: Birden fazla belleği bir araya getiren bir bellek. Genellikle `VectorMemory`'yi `ChatMemoryBuffer` veya `ChatSummaryMemoryBuffer` ile birleştirmek için kullanılır.

## Örnekler

Belleğin işleyişine dair birkaç örneği aşağıda bulabilirsiniz:

-   [Bellek (Memory)](/python/examples/memory/memory)
-   [Çalışma Zamanında Belleği Yönetme](/python/examples/memory/custom_memory)
-   [Özel Bellek ile Çok Turlu Karışıklığı Sınırlandırma](/python/examples/memory/custom_multi_turn_memory)

**NOT:** Eski örnekler:

-   [Chat Memory Buffer](/python/examples/agent/memory/chat_memory_buffer)
-   [Chat Summary Memory Buffer](/python/examples/agent/memory/summary_memory_buffer)
-   [Composable Memory](/python/examples/agent/memory/composable_memory)
-   [Vector Memory](/python/examples/agent/memory/vector_memory)
-   [Mem0 Belleği](/python/examples/memory/mem0memory)