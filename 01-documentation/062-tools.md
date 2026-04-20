# Araçlar (Tools)

## Kavram

Uygun araç soyutlamalarına sahip olmak, [LlamaIndex'te ajanlı sistemler oluşturmanın](/python/framework/module_guides/deploying/agents) merkezinde yer alır. Bir dizi Araç (Tool) tanımlamak, herhangi bir API arayüzü tanımlamaya benzer; tek fark, bu Araçların insan kullanımı için değil, ajan kullanımı için tasarlanmış olmasıdır. Kullanıcıların hem bir **Araç (Tool)** hem de perde arkasında bir dizi fonksiyon içeren bir **Araç Şeması (ToolSpec)** tanımlamasına olanak tanıyoruz.

Fonksiyon çağırma özelliğine sahip bir ajan veya LLM kullanırken, seçilen araç (ve o araç için yazılan argümanlar), aracın amacını ve argümanlarını açıklayan **araç adına** ve **açıklamasına** güçlü bir şekilde dayanır. Bu parametreleri ayarlamak için zaman harcamak, LLM'in bu araçları nasıl çağırdığı konusunda büyük değişikliklere yol açabilir.

Bir Araç, çok genel bir arayüz uygular - sadece `__call__` metodunu tanımlamanız ve ayrıca bazı temel meta verileri (ad, açıklama, fonksiyon şeması) döndürmeniz yeterlidir.

Birkaç farklı Araç türü sunuyoruz:

-   `FunctionTool`: Bir fonksiyon aracı, kullanıcıların kullanıcı tanımlı herhangi bir fonksiyonu kolayca bir Araca dönüştürmesine olanak tanır. Ayrıca fonksiyon şemasını otomatik olarak çıkarabilir veya çeşitli yönlerini özelleştirmenize izin verebilir.
-   `QueryEngineTool`: Mevcut bir [sorgu motorunu (query engine)](/python/framework/module_guides/deploying/query_engine) sarmalayan bir araç. Not: Ajan soyutlamalarımız `BaseQueryEngine`'den miras aldığı için bu araçlar diğer ajanları da sarmalayabilir.
-   Topluluk tarafından katkıda bulunulan ve tek bir hizmet (Gmail gibi) etrafında bir veya daha fazla araç tanımlayan `ToolSpecs`.
-   Bir araçtan büyük miktarda veri döndürmeyi yönetmek için diğer araçları sarmalayan yardımcı (utility) araçlar.

## FunctionTool

Bir fonksiyon aracı, mevcut herhangi bir fonksiyonun basit bir sarmalayıcısıdır (hem senkron hem de asenkron desteklenir!).

```python
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.tools import FunctionTool


def get_weather(location: str) -> str:
    """Belirli bir konum için hava durumunu almak için kullanışlıdır."""
    ...


tool = FunctionTool.from_defaults(
    get_weather,
    # async_fn=aget_weather,  # isteğe bağlı!
)

agent = ReActAgent(llm=llm, tools=tools)
```

Daha iyi bir fonksiyon tanımı için, argüman açıklamalarını belirtmek üzere `Annotated` tipinden de yararlanabilirsiniz.

```python
from typing import Annotated


def get_weather(
    location: Annotated[
        str, "Bir şehir adı ve eyalet, '<isim>, <eyalet>' şeklinde formatlanmış"
    ],
) -> str:
    """Belirli bir konum için hava durumunu almak için kullanışlıdır."""
    ...


tool = FunctionTool.from_defaults(get_weather)
```

Varsayılan olarak araç adı fonksiyon adı olacak ve dökümantasyon dizisi (docstring) de araç açıklaması olacaktır. Ancak bunu geçersiz kılabilirsiniz.

```python
tool = FunctionTool.from_defaults(get_weather, name="...", description="...")
```

## QueryEngineTool

Herhangi bir sorgu motoru, `QueryEngineTool` kullanılarak bir araca dönüştürülebilir:

```python
from llama_index.core.tools import QueryEngineTool

tool = QueryEngineTool.from_defaults(
    query_engine, name="...", description="..."
)
```

## Araç Şemaları (Tool Specs)

Ayrıca [LlamaHub](https://llamahub.ai/) 🦙 aracılığıyla zengin bir Araç ve Araç Şeması seti sunuyoruz.

Araç şemalarını, birlikte kullanılması amaçlanan araç paketleri gibi düşünebilirsiniz. Genellikle bunlar Gmail gibi tek bir arayüz/hizmet genelindeki yararlı araçları kapsar.

Bir ajanda kullanmak için ilgili araç şeması entegrasyonunu yükleyebilirsiniz:

```bash
pip install llama-index-tools-google
```

Ve sonra onu kullanın:

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.tools.google import GmailToolSpec

tool_spec = GmailToolSpec()
agent = FunctionAgent(llm=llm, tools=tool_spec.to_tool_list())
```

Topluluk tarafından katkıda bulunulan araç şemalarının tam listesi için [LlamaHub](https://llamahub.ai) adresini ziyaret edin.

## Yardımcı Araçlar (Utility Tools)

Çoğu zaman, bir API'yi doğrudan sorgulamak muazzam miktarda veri döndürebilir ve bu da tek başına LLM'in bağlam penceresini taşırabilir (veya en azından kullandığınız token sayısını gereksiz yere artırabilir).

Bununla başa çıkmak için LlamaHub Araçları'nda ilk bir dizi "yardımcı araç" sağladık. Yardımcı araçlar kavramsal olarak belirli bir hizmete (örneğin Gmail, Notion) bağlı değildir, bunun yerine mevcut Araçların yeteneklerini artırabilirler. Bu özel durumda yardımcı araçlar, herhangi bir API isteğinden dönen verileri önbelleğe alma/indeksleme ve sorgulama ihtiyacı olan yaygın kalıpları soyutlamaya yardımcı olur.

Aşağıdaki iki ana yardımcı aracımızı inceleyelim.

### OnDemandLoaderTool

Bu araç, mevcut herhangi bir LlamaIndex veri yükleyicisini (`BaseReader` sınıfı), bir ajanın kullanabileceği bir araca dönüştürür. Araç, veri yükleyiciden `load_data` işlemini tetiklemek için gereken tüm parametrelerle ve doğal dilde bir sorgu dizesiyle çağrılabilir. Yürütme sırasında önce veri yükleyiciden verileri yükleriz, bunları indeksleriz (örneğin bir vektör deposu ile) ve ardından "isteğe bağlı" (on-demand) olarak sorgularız. Bu üç adımın tamamı tek bir araç çağrısında gerçekleşir.

Çoğu zaman bu, API verilerini nasıl yükleyeceğinizi ve indeksleyeceğinizi kendiniz çözmekten daha tercih edilebilir olabilir. Bu veri yeniden kullanılabilirliğine izin verse de çoğu zaman kullanıcılar herhangi bir API çağrısı için istem penceresi sınırlamalarını soyutlamak için sadece anlık bir indekse ihtiyaç duyarlar.

Kullanım örneği aşağıda verilmiştir:

```bash
pip install llama-index-readers-wikipedia
```

```python
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.tools.ondemand_loader_tool import OnDemandLoaderTool

tool = OnDemandLoaderTool.from_defaults(
    reader,
    name="Wikipedia Tool",
    description="Wikipedia'dan veri yüklemek ve makaleleri sorgulamak için bir araç",
)
```

### LoadAndSearchToolSpec

`LoadAndSearchToolSpec`, girdi olarak mevcut herhangi bir Aracı alır. Bir araç şeması olarak `to_tool_list` metodunu uygular ve bu fonksiyon çağrıldığında iki araç döndürülür: bir `load` (yükle) aracı ve ardından bir `search` (ara) aracı.

`load` Aracının yürütülmesi temel Aracı çağırır ve çıktıyı indeksler (varsayılan olarak bir vektör indeksi ile). `search` Aracının yürütülmesi girdi olarak bir sorgu dizesi alır ve temel indeksi çağırır.

Bu, varsayılan olarak büyük hacimli veriler döndürecek olan herhangi bir API uç noktası için yararlıdır - örneğin `WikipediaToolSpec` varsayılan olarak tüm Wikipedia sayfalarını döndürür, bu da çoğu LLM bağlam penceresini kolayca taşıracaktır.

Örnek kullanım aşağıda gösterilmiştir:

```bash
pip install llama-index-tools-wikipedia
```

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools.tool_spec.load_and_search import (
    LoadAndSearchToolSpec,
)
from llama_index.tools.wikipedia import WikipediaToolSpec


wiki_spec = WikipediaToolSpec()
# Wikipedia'da arama yapma aracını al
tool = wiki_spec.to_tool_list()[1]

# Yükle/ara araçlarıyla Ajanı oluştur
agent = FunctionAgent(
    llm=llm, tools=LoadAndSearchToolSpec.from_defaults(tool).to_tool_list()
)
```

### Doğrudan Dönüş (Return Direct)

Araç sınıfı yapılandırıcısında `return_direct` seçeneğini göreceksiniz. Bu `True` olarak ayarlanırsa, ajandan gelen yanıt ajan tarafından yorumlanıp yeniden yazılmadan doğrudan döndürülür. Bu, çalışma süresini azaltmak için veya ajan akıl yürütme döngüsünü sonlandıracak araçlar tasarlamak/belirtmek için yararlı olabilir.

Örneğin, bir araç belirttiğinizi varsayalım:

```python
tool = QueryEngineTool.from_defaults(
    query_engine,
    name="<isim>",
    description="<açıklama>",
    return_direct=True,
)

agent = FunctionAgent(llm=llm, tools=[tool])

response = await agent.run("<aracı çağıran soru>")
```

Yukarıdaki örnekte, sorgu motoru aracı çağrılır ve bu araçtan gelen yanıt doğrudan yanıt olarak döndürülür ve yürütme döngüsü sona erer.

Eğer `return_direct=False` kullanılsaydı, ajan sohbet geçmişinin bağlamını kullanarak yanıtı yeniden yazardı veya hatta başka bir araç çağrısı yapardı.

Ayrıca `return_direct` kullanımına dair bir [örnek notebook](/python/examples/agent/return_direct_agent) sağladık.

## Araçlarda Hata Ayıklama (Debugging Tools)

Çoğu zaman, API'lere gönderilen araç tanımının tam olarak ne olduğunu ayıklamak yararlı olabilir.

OpenAI ve Anthropic gibi API'lerde kullanılan mevcut araç şemasını almak için temel fonksiyonu kullanarak buna bir göz atabilirsiniz.

```python
schema = tool.metadata.get_parameters_dict()
print(schema)
```