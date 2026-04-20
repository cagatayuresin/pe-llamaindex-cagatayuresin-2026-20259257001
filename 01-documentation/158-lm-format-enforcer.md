# LM Format Enforcer

[LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer), bir dil modelinin çıktı formatını (JSON Şeması, Regex vb.) zorunlu kılan bir kütüphanedir. İstenen çıktı yapısını LLM'ye sadece "önermek" yerine, LM Format Enforcer aslında LLM çıktısını istenen şemayı takip etmeye "zorlayabilir".

![resim](https://raw.githubusercontent.com/noamgat/lm-format-enforcer/main/docs/Intro.webp)

LM Format Enforcer yerel LLM'lerle çalışır (şu anda `LlamaCPP` ve `HuggingfaceLLM` arka uçlarını destekler) ve sadece LLM'nin çıktı logitlerini işleyerek çalışır. Bu, üretim döngüsünün kendisini değiştiren diğer çözümlerin aksine, beam search ve batching gibi gelişmiş üretim yöntemlerini desteklemesini sağlar. Daha fazla detay için [LM Format Enforcer sayfasındaki](https://github.com/noamgat/lm-format-enforcer) karşılaştırma tablosuna bakın.

## JSON Şeması Çıktısı (JSON Schema Output)

LlamaIndex'te, yapılandırılmış çıktı (daha spesifik olarak Pydantic nesneleri) oluşturmayı süper kolay hale getirmek için LM Format Enforcer ile ilk entegrasyonu sağlıyoruz.

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

Bu, istenen Pydantic sınıfımız olan `Album`'ü belirterek bir `LMFormatEnforcerPydanticProgram` oluşturmak ve uygun bir istem şablonu sağlamak kadar basittir.

> Not: `LMFormatEnforcerPydanticProgram`, istem şablonundaki isteğe bağlı `{json_schema}` parametresine Pydantic sınıfının JSON şemasını otomatik olarak doldurur. Bu, LLM'nin doğal olarak doğru JSON'u oluşturmasına yardımcı olabilir ve format denetleyicisinin müdahale saldırganlığını azaltarak çıktı kalitesini artırabilir.

```python
program = LMFormatEnforcerPydanticProgram(
    output_cls=Album,
    prompt_template_str="Bir örnek albüm oluşturun, bir sanatçı ve bir şarkı listesi olsun. İlham kaynağı olarak {movie_name} filmini kullanın. Şu şemaya göre cevap vermelisiniz: \n{json_schema}\n",
    llm=LlamaCPP(),
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
    name="The Shining: Overlook Oteli'nin Perili Salonlarında Müzikal Bir Yolculuk",
    artist="The Shining Korosu (The Shining Choir)",
    songs=[
        Song(title="Redrum", length_seconds=300),
        Song(
            title="All Work and No Play Makes Jack a Dull Boy",
            length_seconds=240,
        ),
        Song(title="Heeeeere's Johnny!", length_seconds=180),
    ],
)
```

Daha fazla detay için [bu not defteriyle](/python/examples/output_parsing/lmformatenforcer_pydantic_program) oynayabilirsiniz.

## Düzenli İfade Çıktısı (Regular Expression Output)

LM Format Enforcer ayrıca regex çıktısını da destekler. LlamaIndex'te düzenli ifadeler için mevcut bir soyutlama bulunmadığından, içine LM Format Generator enjekte ettikten sonra doğrudan LLM'yi kullanacağız.

```python
regex = r'"Merhaba, benim adım (?P<name>[a-zA-Z]*)\. Şurada doğdum: (?P<hometown>[a-zA-Z]*). Tanıştığımıza memnun oldum!"'
prompt = "Eğer adım John olsaydı ve Boston'da doğmuş olsaydım, kendimi şu şekilde tanıtırdım: "

llm = LlamaCPP()
regex_parser = lmformatenforcer.RegexParser(regex)
lm_format_enforcer_fn = build_lm_format_enforcer_function(llm, regex_parser)
with activate_lm_format_enforcer(llm, lm_format_enforcer_fn):
    output = llm.complete(prompt)
```

Bu, LLM'nin belirttiğimiz düzenli ifade biçiminde çıktı üretmesine neden olacaktır. Çıktıyı adlandırılmış grupları almak için de ayrıştırabiliriz:

```python
print(output)
# "Merhaba, benim adım John. Şurada doğdum: Boston. Tanıştığımıza memnun oldum!"
print(re.match(regex, output.text).groupdict())
# {'name': 'John', 'hometown': 'Boston'}
```

Daha fazla detay için [bu not defterine](/python/examples/output_parsing/lmformatenforcer_regular_expressions) bakın.