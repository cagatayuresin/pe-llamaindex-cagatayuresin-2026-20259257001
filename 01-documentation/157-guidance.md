# Guidance

[Guidance](https://github.com/microsoft/guidance), Microsoft tarafından geliştirilen, büyük dil modellerini kontrol etmek için kullanılan bir yönlendirme dilidir.

Guidance programları; üretimi (generation), istemleri (prompting) ve mantıksal kontrolü, dil modelinin metni aslında nasıl işlediğiyle eşleşen tek bir kesintisiz akışta birleştirmenize olanak tanır.

## Yapılandırılmış Çıktı (Structured Output)

Guidance'ın özellikle heyecan verici bir yönü, yapılandırılmış nesneler (belirli bir şemayı takip eden JSON veya bir Pydantic nesnesi gibi) üretme yeteneğidir. İstenen çıktı yapısını LLM'ye sadece "önermek" yerine, Guidance aslında LLM çıktısını istenen şemayı takip etmeye "zorlayabilir". Bu, LLM'nin sözdizimi (syntax) yerine içeriğe odaklanmasını sağlar ve çıktı ayrıştırma (parsing) sorunları olasılığını tamamen ortadan kaldırır.

Bu, parametre sayısı daha az olan ve güvenilir bir şekilde iyi biçimlendirilmiş, hiyerarşik yapılandırılmış çıktı üretebilmek için yeterli kaynak kod verisiyle eğitilmemiş daha zayıf LLM'ler için özellikle güçlüdür.

### Pydantic nesneleri oluşturmak için bir Guidance programı oluşturma

LlamaIndex'te, yapılandırılmış çıktı (daha spesifik olarak Pydantic nesneleri) oluşturmayı süper kolay hale getirmek için Guidance ile ilk entegrasyonu sağlıyoruz.

Örneğin, aşağıdaki şemaya sahip bir şarkı albümü oluşturmak istiyorsak:

```python
class Song(BaseModel):
    title: str
    length_seconds: int


class Album(BaseModel):
    name: str
    artist: str
    songs: List[Song]
```

Bu, istenen Pydantic sınıfımız olan `Album`'ü belirterek bir `GuidancePydanticProgram` oluşturmak ve uygun bir istem şablonu sağlamak kadar basittir.

> Not: Guidance, değişken değiştirme için çift süslü parantez ve tam (literal) süslü parantezler için tek süslü parantez kullanan handlebars tarzı şablonlar kullanır. Bu, Python format dizelerinin tam tersi bir kuraldır.

`from llama_index.core.prompts.guidance_utils import convert_to_handlebars` modülü, Python format dizesi tarzındaki şablonları Guidance handlebars tarzındaki şablonlara dönüştürebilir.

```python
program = GuidancePydanticProgram(
    output_cls=Album,
    prompt_template_str="Bir örnek albüm oluşturun, bir sanatçı ve bir şarkı listesi olsun. İlham kaynağı olarak {{movie_name}} filmini kullanın",
    guidance_llm=OpenAI("text-davinci-003"),
    verbose=True,
)
```

Şimdi programı ek kullanıcı girdisiyle çağırarak çalıştırabiliriz.
Burada biraz ürkütücü bir şey seçelim ve "The Shining" filminden esinlenen bir albüm oluşturalım.

```python
output = program(movie_name="The Shining")
```

Pydantic nesnemiz elimizde:

```python
Album(
    name="The Shining",
    artist="Jack Torrance",
    songs=[
        Song(title="All Work and No Play", length_seconds=180),
        Song(title="The Overlook Hotel", length_seconds=240),
        Song(title="The Shining", length_seconds=210),
    ],
)
```

Daha fazla detay için [bu not defteriyle](/python/examples/output_parsing/guidance_pydantic_program) oynayabilirsiniz.

### Alt-soru sorgu motorumuzun (sub-question query engine) sağlamlığını artırmak için Guidance kullanma

LlamaIndex, farklı kullanım durumlarını ele almak için gelişmiş sorgu motorlarından oluşan bir araç seti sunar.
Bunların birkaçı, ara adımlarda yapılandırılmış çıktıya dayanır.
Ara yanıtın beklenen yapıya sahip olduğundan emin olarak (böylece yapılandırılmış bir nesneye doğru şekilde ayrıştırılabilirler) bu sorgu motorlarının sağlamlığını artırmak için Guidance'ı kullanabiliriz.

Örnek olarak, varsayılan ayarı kullanmaktan daha sağlam hale getirmek için bir `SubQuestionQueryEngine`'e takılabilen bir `GuidanceQuestionGenerator` uyguluyoruz.

```python
from llama_index.question_gen.guidance import GuidanceQuestionGenerator
from guidance.llms import OpenAI as GuidanceOpenAI

# Guidance tabanlı soru oluşturucuyu tanımla
question_gen = GuidanceQuestionGenerator.from_defaults(
    guidance_llm=GuidanceOpenAI("text-davinci-003"), verbose=False
)

# sorgu motoru araçlarını tanımla
query_engine_tools = ...

# alt-soru sorgu motorunu oluştur
s_engine = SubQuestionQueryEngine.from_defaults(
    question_gen=question_gen,  # yukarıda tanımlanan guidance tabanlı question_gen'i kullan
    query_engine_tools=query_engine_tools,
)
```

Daha fazla detay için [bu not defterine](/python/examples/output_parsing/guidance_sub_question) bakın.