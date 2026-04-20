# İstem (Prompt) Kullanım Kalıbı

## `RichPromptTemplate` ve Jinja Sözdizimini Kullanma

Jinja sözdiziminden yararlanarak; değişkenler, mantıksal ifadeler, ayrıştırma nesneleri ve daha fazlasını içeren istem şablonları oluşturabilirsiniz.

Bazı örneklere göz atalım:

```python
from llama_index.core.prompts import RichPromptTemplate

template = RichPromptTemplate(
    """Aşağıda bağlam bilgisi sağlanmıştır.
---------------------
{{ context_str }}
---------------------
Bu bilgileri göz önünde bulundurarak lütfen soruyu yanıtlayın: {{ query_str }}
"""
)

# dize olarak biçimlendir
prompt_str = template.format(context_str=..., query_str=...)

# sohbet mesajları listesi olarak biçimlendir
messages = template.format_messages(context_str=..., query_str=...)
```

Jinja istemleri ile f-string'ler arasındaki temel fark, değişkenlerin artık tekli süslü parantez `{ }` yerine çiftli süslü parantez `{{ }}` ile kullanılmasıdır.

Çok modlu (multi-modal) bir istem oluşturmak için döngüleri kullanan daha karmaşık bir örneğe bakalım.

```python
from llama_index.core.prompts import RichPromptTemplate

template = RichPromptTemplate(
    """
{% chat role="system" %}
Görsellerin bir listesi ve her bir görselden alınan metinler verildiğinde, lütfen soruyu elinizden gelen en iyi şekilde yanıtlayın.
{% endchat %}

{% chat role="user" %}
{% for image_path, text in images_and_texts %}
İşte bir metin: {{ text }}
Ve işte bir görsel:
{{ image_path | image }}
{% endfor %}
{% endchat %}
"""
)

messages = template.format_messages(
    images_and_texts=[
        ("sayfa_1.png", "Bu, dökümanın ilk sayfasıdır"),
        ("sayfa_2.png", "Bu, dökümanın ikinci sayfasıdır"),
    ]
)
```

Bu örnekte birkaç özellik görebilirsiniz:

-   `{% chat %}` bloğu, mesajı bir sohbet mesajı olarak biçimlendirmek ve rolü ayarlamak için kullanılır.
-   `{% for %}` döngüsü, iletilen `images_and_texts` listesi üzerinde dönmek için kullanılır.
-   `{{ image_path | image }}` sözdizimi, görsel yolunu bir görsel içerik bloğu olarak biçimlendirmek için kullanılır. Burada `|`, değişkeni bir görsel olarak tanımlamaya yardımcı olacak bir "filtre" uygulamak için kullanılır.

Bir retriever'dan gelen node'ları kullanarak bir şablon oluşturmaya dair başka bir örneğe bakalım:

```python
from llama_index.core.prompts import RichPromptTemplate

template = RichPromptTemplate(
    """
{% chat role="system" %}
Sağlanan bağlam hakkındaki soruları yanıtlayabilen yardımcı bir asistansınız.
{% endchat %}

{% chat role="user" %}
{% for node in nodes %}
{{ node.text }}
{% endfor %}
{% endchat %}
"""
)

nodes = retriever.retrieve("Ay'ın başkenti neresidir?")

messages = template.format_messages(nodes=nodes)
```

## `f-string` İstem Şablonlarını Kullanma

Bu dökümanın yazıldığı sırada birçok eski bileşen ve örnek `f-string` istemlerini kullanmaktadır.

Özel bir istem tanımlamak, bir biçimlendirme dizesi oluşturmak kadar basittir:

```python
from llama_index.core import PromptTemplate

template = (
    "Aşağıda bağlam bilgisi sağlanmıştır. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Bu bilgileri göz önünde bulundurarak lütfen soruyu yanıtlayın: {query_str}\n"
)
qa_template = PromptTemplate(template)

# Metin istemi oluşturabilirsiniz (tamamlama API'si için)
prompt = qa_template.format(context_str=..., query_str=...)

# Veya kolayca mesaj istemlerine dönüştürebilirsiniz (sohbet API'si için)
messages = qa_template.format_messages(context_str=..., query_str=...)
```

Sohbet mesajlarından da bir şablon tanımlayabilirsiniz:

```python
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

message_templates = [
    ChatMessage(content="Siz bir uzman sistemisiniz.", role=MessageRole.SYSTEM),
    ChatMessage(
        content="{topic} hakkında kısa bir hikaye oluşturun",
        role=MessageRole.USER,
    ),
]
chat_template = ChatPromptTemplate(message_templates=message_templates)

# Mesaj istemleri oluşturabilirsiniz (sohbet API'si için)
messages = chat_template.format_messages(topic=...)

# Veya kolayca metin istemine dönüştürebilirsiniz (tamamlama API'si için)
prompt = chat_template.format(topic=...)
```

## Özel İstemleri Alma ve Ayarlama

LlamaIndex çok aşamalı bir boru hattı (pipeline) olduğundan, değiştirmek istediğiniz işlemi tanımlamak ve özel istemi doğru yere iletmek önemlidir.

Örneğin; istemler yanıt sentezleyicide (response synthesizer), retriever'larda, indeks oluşturmada vb. kullanılır; bu modüllerin bazıları diğer modüllerin içine yerleştirilmiştir (sentezleyici, sorgu motorunun içindedir).

İstemlere erişme ve onları özelleştirme hakkındaki tüm detaylar için [bu kılavuza](/python/examples/prompts/prompt_mixin) bakın.

### Yaygın Olarak Kullanılan İstemler

En yaygın kullanılan istemler `text_qa_template` ve `refine_template` olacaktır.

-   `text_qa_template`: Getirilen node'ları kullanarak bir sorguya başlangıç yanıtı almak için kullanılır.
-   `refine_template`: Getirilen metin, `response_mode="compact"` (varsayılan) ile tek bir LLM çağrısına sığmadığında veya `response_mode="refine"` kullanılarak birden fazla node getirildiğinde kullanılır. İlk sorgudan gelen yanıt bir `existing_answer` (mevcut yanıt) olarak eklenir ve LLM'in yeni bağlama göre mevcut yanıtı güncellemesi veya tekrarlaması gerekir.

### İstemlere Erişme

Modül ve iç içe geçmiş alt modüller içinde kullanılan istemlerin düz bir listesini almak için LlamaIndex'teki birçok modülde `get_prompts` fonksiyonunu çağırabilirsiniz.

Örneğin, aşağıdaki kod parçasına bir göz atın.

```python
query_engine = index.as_query_engine(response_mode="compact")
prompts_dict = query_engine.get_prompts()
print(list(prompts_dict.keys()))
```

Geriye şu anahtarlar dönebilir:

```
['response_synthesizer:text_qa_template', 'response_synthesizer:refine_template']
```

İstemlerin, "ad alanları" (namespaces) olarak alt modülleriyle ön ek aldığını unutmayın.

### İstemleri Güncelleme

`get_prompts` uygulayan herhangi bir modüldeki istemleri `update_prompts` fonksiyonu ile özelleştirebilirsiniz. `get_prompts` aracılığıyla elde ettiğiniz istem sözlüğündeki anahtarlara eşit olan argüman değerlerini iletmeniz yeterlidir.

Örn. yukarıdaki örnekle ilgili olarak şunları yapabiliriz:

```python
# shakespeare tarzı!
qa_prompt_tmpl_str = (
    "Bağlam bilgisi aşağıdadır.\n"
    "---------------------\n"
    "{{ context_str }}\n"
    "---------------------\n"
    "Bağlam bilgisini kullanarak ve önceden bildiklerinize dayanmadan, "
    "sorguyu bir Shakespeare oyunu tarzında yanıtlayın.\n"
    "Sorgu: {{ query_str }}\n"
    "Yanıt: "
)
qa_prompt_tmpl = RichPromptTemplate(qa_prompt_tmpl_str)

query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
)
```

### Sorgu Motorunda Kullanılan İstemleri Değiştirme

Sorgu motorları için, sorgu zamanında (yani bir indekse karşı bir sorgu yürütürken ve nihai yanıtı sentezlerken) doğrudan özel istemler de iletebilirsiniz.

Ayrıca istemleri geçersiz kılmanın iki eşdeğer yolu vardır:

1. Üst düzey (high-level) API aracılığıyla:

```python
query_engine = index.as_query_engine(
    text_qa_template=custom_qa_prompt, refine_template=custom_refine_prompt
)
```

2. Alt düzey (low-level) bileşim API'si aracılığıyla:

```python
retriever = index.as_retriever()
synth = get_response_synthesizer(
    text_qa_template=custom_qa_prompt, refine_template=custom_refine_prompt
)
query_engine = RetrieverQueryEngine(retriever, response_synthesizer)
```

Yukarıdaki iki yaklaşım eşdeğerdir; burada 1. seçenek aslında 2. seçenek için bir "sözdizimsel şekerdir" (syntactic sugar) ve temeldeki karmaşıklığı gizler. Bazı yaygın parametreleri hızlıca değiştirmek için 1'i, daha ince ayarlı (granular) kontrole sahip olmak için ise 2'yi kullanmak isteyebilirsiniz.

Hangi sınıfların hangi istemleri kullandığı hakkında daha fazla detay için lütfen [Sorgu sınıfı referanslarını](/python/framework-api-reference/response_synthesizers) ziyaret edin.

Tüm istemlerin tam seti ve yöntemleri/parametreleri için [referans dökümantasyonunu](/python/framework-api-reference/prompts) kontrol edin.

## [Gelişmiş] Gelişmiş İstem Yetenekleri

Bu bölümde LlamaIndex'teki bazı gelişmiş istem yeteneklerini gösteriyoruz.

İlgili Kılavuzlar:

-   [Gelişmiş İstemler (Advanced Prompts)](/python/examples/prompts/advanced_prompts)
-   [RichPromptTemplate Özellikleri](/python/examples/prompts/rich_prompt_template_features)

### Fonksiyon Eşlemeleri (Function Mappings)

Şablon değişkenleri olarak sabit değerler yerine fonksiyonlar iletin.

Bu oldukça gelişmiş ve güçlüdür; dinamik az-örnekli (few-shot) istemleme vb. yapmanıza olanak tanır.

İşte `context_str`'yi yeniden biçimlendirmeye dair bir örnek:

```python
from llama_index.core.prompts import RichPromptTemplate


def format_context_fn(**kwargs):
    # bağlamı madde işaretleriyle (bullet points) biçimlendir
    context_list = kwargs["context_str"].split("\n\n")
    fmtted_context = "\n\n".join([f"- {c}" for c in context_list])
    return fmtted_context


prompt_tmpl = RichPromptTemplate(
    "{{ context_str }}", function_mappings={"context_str": format_context_fn}
)

prompt_str = prompt_tmpl.format(context_str="baglam", query_str="sorgu")
```

### Kısmi Biçimlendirme (Partial Formatting)

Bazı değişkenleri doldurup diğerlerini daha sonra doldurulmak üzere bırakarak bir istemi kısmi olarak biçimlendirin.

```python
from llama_index.core.prompts import RichPromptTemplate

template = RichPromptTemplate(
    """
{{ foo }} {{ bar }}
"""
)

partial_prompt_tmpl = template.partial_format(foo="abc")

fmt_str = partial_prompt_tmpl.format(bar="def")
```

### Şablon Değişken Eşlemeleri (Template Variable Mappings)

LlamaIndex istem soyutlamaları genellikle belirli anahtarlar bekler. Örneğin `text_qa_prompt` istemimiz, bağlam için `context_str` ve kullanıcı sorgusu için `query_str` bekler.

Ancak bir dize şablonunu LlamaIndex ile kullanmak için uyarlamaya çalışıyorsanız, şablon değişkenlerini değiştirmek sinir bozucu olabilir.

Bunun yerine `template_var_mappings` tanımlayın:

```python
from llama_index.core.prompts import RichPromptTemplate

template_var_mappings = {"context_str": "benim_baglamim", "query_str": "benim_sorgum"}

prompt_tmpl = RichPromptTemplate(
    "İşte bazı bağlamlar: {{ context_str }} ve işte bir sorgu: {{ query_str }}",
    template_var_mappings=template_var_mappings,
)

prompt_str = prompt_tmpl.format(benim_baglamim="baglam", benim_sorgum="sorgu")
```