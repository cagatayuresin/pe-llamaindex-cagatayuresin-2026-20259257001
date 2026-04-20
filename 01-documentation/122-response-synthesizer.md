# Yanıt Sentezleyici (Response Synthesizer)

## Kavram

Bir `Response Synthesizer`, kullanıcı sorgusu ve verilen bir grup metin parçasını (chunks) kullanarak bir LLM'den yanıt oluşturan bileşendir. Bir yanıt sentezleyicinin çıktısı bir `Response` nesnesidir.

Bunu yapma yöntemi; metin parçaları üzerinde basitçe dönmekten, karmaşık bir ağaç yapısı oluşturmaya kadar birçok form alabilir. Buradaki temel fikir, verileriniz üzerinde bir LLM kullanarak yanıt oluşturma sürecini basitleştirmektir.

Bir sorgu motorunda (query engine) kullanıldığında; yanıt sentezleyici, bir retriever'dan node'lar getirildikten ve tüm node postprocessor'lar çalıştırıldıktan sonra kullanılır.

<Aside type="tip">
  Yanıt sentezleyicinin RAG iş akışında nereye oturduğu konusunda kafanız mı karıştı?
  [Üst düzey kavramlar](/python/getting_started/concepts) dökümanını okuyun.
</Aside>

## Kullanım Kalıbı (Usage Pattern)

Yanıt sentezleyiciyi tek başına kullanın:

```python
from llama_index.core.data_structs import Node
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core import get_response_synthesizer

response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT
)

response = response_synthesizer.synthesize(
    "sorgu metni", nodes=[Node(text="metin"), ...]
)
```

Veya bir indeks oluşturduktan sonra bir sorgu motoru içinde:

```python
query_engine = index.as_query_engine(response_synthesizer=response_synthesizer)
response = query_engine.query("sorgu_metni")
```

Mevcut tüm yanıt sentezleyiciler, modlar ve kendi sentezleyicinizi nasıl oluşturacağınız hakkında daha fazla detayı aşağıda bulabilirsiniz.

## Başlarken

`response_mode` kullanarak bir sorgu motoru için yanıt sentezleyicinin yapılandırılması:

```python
from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore
from llama_index.core import get_response_synthesizer

response_synthesizer = get_response_synthesizer(response_mode="compact")

response = response_synthesizer.synthesize(
    "sorgu metni", nodes=[NodeWithScore(node=Node(text="metin"), score=1.0), ...]
)
```

Veya daha yaygın olarak, bir indeks oluşturduktan sonra bir sorgu motoru içinde:

```python
query_engine = index.as_query_engine(response_synthesizer=response_synthesizer)
response = query_engine.query("sorgu_metni")
```

<Aside type="tip">
  İndeks oluşturmayı öğrenmek için [İndeksleme](/python/indexing) dökümanına bakın.
</Aside>

## Yanıt Modunu Yapılandırma

Yanıt sentezleyiciler tipik olarak bir `response_mode` (yanıt modu) argümanı aracılığıyla belirlenir.

LlamaIndex'te halihazırda birkaç yanıt sentezleyici uygulanmıştır:

-   `refine`: Getirilen her metin parçasından sırayla geçerek bir yanıt **_oluşturun ve iyileştirin (refine)_**. Bu, her bir Node/metin parçası için ayrı bir LLM çağrısı yapar.

    **Detaylar:** İlk parça, `text_qa_template` istemi kullanılarak bir sorguda kullanılır. Ardından yanıt ve sonraki parça (ve orijinal soru), `refine_template` istemi ile başka bir sorguda kullanılır. Tüm parçalar ayrıştırılana kadar bu şekilde devam eder.

    Eğer bir parça (istem boyutu da düşünülerek) pencereye sığmayacak kadar büyükse, bir `TokenTextSplitter` kullanılarak bölünür (parçalar arasında bir miktar metin örtüşmesine/overlap izin verilir) ve (yeni) ek parçalar, orijinal parça koleksiyonunun birer parçası olarak kabul edilir (ve böylece onlar için de `refine_template` ile sorgu yapılır).

    Daha ayrıntılı yanıtlar için uygundur.

-   `compact` (varsayılan): `refine` moduna benzer ancak daha az LLM çağrısı yapılması için parçaları önceden **_sıkıştırır (compact/concatenate)_**.

    **Detaylar:** Bağlam penceresine sığabilecek kadar çok metni (getirilen parçalardan birleştirilmiş/paketlenmiş) doldurur (`text_qa_template` ve `refine_template` arasındaki maksimum istem boyutu dikkate alınarak). Eğer metin tek bir istem içine sığmayacak kadar uzunsa, gerektiği kadar parçaya bölünür (bir `TokenTextSplitter` kullanılarak ve metin parçaları arasında bir miktar örtüşmeye izin verilerek).

    Her metin bölümü bir "parça" (chunk) olarak kabul edilir ve `refine` sentezleyicisine gönderilir.

    Kısacası, `refine` gibidir ama daha az LLM çağrısı yapar.

-   `tree_summarize`: Tüm birleştirilmiş parçalar sorgulanana kadar LLM'e `summary_template` istemiyle gerektiği kadar sorgu gönderir. Sonuçta elde edilen yanıtlar, kendi içlerinde bir `tree_summarize` LLM çağrısında özyinelemeli (recursively) olarak parça olarak kullanılır ve tek bir parça kalana kadar (yani tek bir nihai yanıt) bu süreç devam eder.

    **Detaylar:** Parçaları, `summary_template` istemini kullanarak bağlam penceresine sığacak şekilde mümkün olduğunca birleştirir ve gerekiyorsa böler (yine `TokenTextSplitter` ve metin örtüşmesiyle). Ardından, her bir sonuç parçasını/bölümünü `summary_template` ile sorgular (**_refine_** sorgusu yoktur!) ve yanıtları alır.

    Eğer sadece bir yanıt varsa (çünkü sadece bir parça vardı), o zaman bu nihai yanıttır.

    Birden fazla yanıt varsa, bunlar kendileri parça olarak kabul edilir ve özyinelemeli olarak `tree_summarize` sürecine gönderilir (birleştirilir/sığacak şekilde bölünür/sorgulanır).

    Özetleme amaçları için uygundur.

-   `simple_summarize`: Tüm metin parçalarını tek bir LLM istemine sığacak şekilde kırpar (truncate). Hızlı özetleme amaçları için iyidir ancak kırpma nedeniyle detay kaybı yaşanabilir.
-   `no_text`: Sadece LLM'e gönderilecek olan node'ları getirmek için retriever'ı çalıştırır, ancak bunları gerçekten göndermez. Daha sonra `response.source_nodes` kontrol edilerek incelenebilir.
-   `context_only`: Tüm metin parçalarının birleştirilmiş bir dizesini döndürür.
-   `accumulate`: Bir metin parçası kümesi ve sorgu verildiğinde; yanıtları bir dizide biriktirirken (accumulate) sorguyu her bir metin parçasına uygular. Tüm yanıtların birleştirilmiş bir dizesini döndürür. Aynı sorguyu her bir metin parçasına karşı ayrı ayrı çalıştırmanız gerektiğinde iyidir.
-   `compact_accumulate`: `accumulate` ile aynıdır, ancak `compact` moduna benzer şekilde her bir LLM istemini "sıkıştırır" ve her bir metin parçasına karşı aynı sorguyu çalıştırır.

## Özel Yanıt Sentezleyiciler (Custom Response Synthesizers)

Her yanıt sentezleyici `llama_index.response_synthesizers.base.BaseSynthesizer` sınıfından miras alır. Temel API son derece basittir, bu da kendi yanıt sentezleyicinizi oluşturmanızı kolaylaştırır.

Belki `tree_summarize` aşamasındaki her adımda hangi şablonun kullanılacağını özelleştirmek isteyebilirsiniz veya belki bir sorguya yanıt oluşturmanın yeni bir yolunu detaylandıran yeni bir makale yayınlanmıştır; kendi yanıt sentezleyicinizi oluşturabilir ve onu herhangi bir sorgu motoruna takabilir veya tek başına kullanabilirsiniz.

Aşağıda `__init__()` fonksiyonunu ve her yanıt sentezleyicinin uygulaması gereken iki soyut yöntemi gösteriyoruz. Temel gereksinimler; bir sorguyu ve metin parçalarını işlemek ve bir dize (veya dize üreteci/generator) yanıtı döndürmektir.

```python
from llama_index.core import Settings


class BaseSynthesizer(ABC):
    """Yanıt oluşturucu sınıfı."""

    def __init__(
        self,
        llm: Optional[LLM] = None,
        streaming: bool = False,
    ) -> None:
        """Başlatma parametreleri."""
        self._llm = llm or Settings.llm
        self._callback_manager = Settings.callback_manager
        self._streaming = streaming

    @abstractmethod
    def get_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        """Yanıt al."""
        ...

    @abstractmethod
    async def aget_response(
        self,
        query_str: str,
        text_chunks: Sequence[str],
        **response_kwargs: Any,
    ) -> RESPONSE_TEXT_TYPE:
        """Yanıt al (asenkron)."""
        ...
```

## Yapılandırılmış Yanıt Filtreleme (Structured Answer Filtering) Kullanımı

`"refine"` veya `"compact"` yanıt sentezi modüllerini kullanırken, `structured_answer_filtering` seçeneğini denemek faydalı olabilir.

```python
from llama_index.core import get_response_synthesizer

response_synthesizer = get_response_synthesizer(structured_answer_filtering=True)
```

`structured_answer_filtering` True olarak ayarlandığında, refine modülümüz sorulan soruyla ilgili olmayan tüm girdi node'larını filtreleyebilir. Bu, özellikle belirli bir kullanıcı sorgusu için harici vektör deposundan metin parçalarının getirilmesini içeren RAG tabanlı Soru-Cevap sistemleri için kullanışlıdır.

Bu seçenek, özellikle [fonksiyon çağırmayı (function calling) destekleyen bir OpenAI modeli](https://openai.com/blog/function-calling-and-other-api-updates) kullanıyorsanız yararlıdır. Yerel fonksiyon çağırma desteği olmayan diğer LLM sağlayıcıları veya modelleri, bu özelliğin dayandığı yapılandırılmış yanıtı üretmede daha az güvenilir olabilir.

## Özel İstem Şablonlarını (ek değişkenlerle) Kullanma

Yanıt sentezleyicimizde kullanılan istemleri özelleştirmek ve sorgu zamanında ek değişkenler eklemek isteyebilirsiniz.

Bu ek değişkenleri `get_response` için `**kwargs` içinde belirtebilirsiniz.

Örneğin:

```python
from llama_index.core import PromptTemplate
from llama_index.core.response_synthesizers import TreeSummarize

# NOT: buraya ekstra bir tone_name değişkeni ekliyoruz
qa_prompt_tmpl = (
    "Bağlam bilgisi aşağıdadır.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Bağlam bilgisini kullanarak ve önceden bildiklerinize dayanmadan, "
    "sorguyu yanıtlayın.\n"
    "Lütfen yanıtı {tone_name} tonunda yazın.\n"
    "Sorgu: {query_str}\n"
    "Yanıt: "
)
qa_prompt = PromptTemplate(qa_prompt_tmpl)

# yanıt sentezleyiciyi başlat
summarizer = TreeSummarize(verbose=True, summary_template=qa_prompt)

# yanıtı al
response = summarizer.get_response(
    "Paul Graham kimdir?", [text], tone_name="bir Shakespeare oyunu"
)
```

## Modüller

Daha fazla detay için [tam modül kılavuzuna](/python/framework/module_guides/querying/response_synthesizers/response_synthesizers) göz atın.