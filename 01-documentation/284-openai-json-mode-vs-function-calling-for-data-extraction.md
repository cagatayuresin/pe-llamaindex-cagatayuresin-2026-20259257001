# Veri Çıkarma için OpenAI JSON Modu vs. Fonksiyon Çağırma

---
title: Veri Çıkarma için OpenAI JSON Modu vs. Fonksiyon Çağırma
 | LlamaIndex OSS Documentation
---

OpenAI kısa süre önce [JSON Modu](https://platform.openai.com/docs/guides/text-generation/json-mode)'nu yayınladı: Bu yeni yapılandırma, LLM'yi yalnızca geçerli JSON'a ayrıştırılan (ancak herhangi bir şemaya karşı doğrulama garantisi olmayan) dizeler oluşturmaya zorlar.

Bundan önce, metinden yapılandırılmış veri çıkarmanın en iyi yolu [fonksiyon çağırma](https://platform.openai.com/docs/guides/function-calling) yöntemiydi.

Bu not defterinde, yapılandırılmış çıktı ve veri çıkarma için en son [JSON Modu](https://platform.openai.com/docs/guides/text-generation/json-mode) ile fonksiyon çağırma özelliği arasındaki dengeyi/takasları inceliyoruz.

*Güncelleme*: OpenAI, fonksiyon çağırma için JSON modunun her zaman etkinleştirildiğini, normal mesajlar için ise isteğe bağlı olduğunu açıklamıştır (<https://community.openai.com/t/json-mode-vs-function-calling/476994/4>)

### Sentetik veri oluşturma

Veri çıkarma görevimiz için bazı sentetik veriler oluşturarak başlayacağız. LLM'mizden varsayımsal bir satış görüşmesi transkripti isteyelim.

```python
%pip install llama-index-llms-openai
%pip install llama-index-program-openai
```

```python
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo-1106")
response = llm.complete(
    "Bir satış araması transkripti oluşturun, gerçek isimler kullanın, bir ürün hakkında konuşun, bazı eylem maddelerini tartışın"
)
```

```python
transcript = response.text
print(transcript)
```

```python
[Telefon çalıyor]


John: Merhaba, ben John.


Sarah: Merhaba John, ben XYZ Şirketi'nden Sarah. Yeni ürünümüz olan XYZ Widget'ı tartışmak ve işletmeniz için uygun olup olmayacağını görmek için arıyorum.


John: Merhaba Sarah, ulaştığın için teşekkürler. XYZ Widget hakkında daha fazla bilgi edinmekle kesinlikle ilgileniyorum. Ne yaptığına dair bana hızlı bir genel bakış verebilir misin?


Sarah: Elbette! XYZ Widget, işletmelerin iş akışlarını kolaylaştırmalarına ve üretkenliği artırmalarına yardımcı olan son teknoloji bir araçtır. Tekrarlanan görevleri otomatikleştirmek ve bilinçli kararlar vermenize yardımcı olmak için gerçek zamanlı veri analitiği sağlamak üzere tasarlanmıştır.


John: Kulağa gerçekten ilginç geliyor. Bunun ekibimize nasıl fayda sağlayabileceğini görebiliyorum. XYZ Widget'ı kullanan diğer şirketlerden herhangi bir vaka çalışmanız veya başarı hikayeniz var mı?


Sarah: Kesinlikle, sizinle paylaşabileceğim birkaç vaka çalışmamız var. Bunları ürünle ilgili bazı ek bilgilerle birlikte göndereceğim. Ayrıca XYZ Widget'ı iş başında görmeniz için size ve ekibinize bir demo planlamayı çok isterim.


John: Bu harika olur. Vaka çalışmalarını incelediğimden emin olacağım ve ardından demo için bir zaman ayarlayabiliriz. Bu arada, yapmamız gereken belirli eylem maddeleri veya sonraki adımlar var mı?


Sarah: Evet, bilgileri göndereceğim ve ardından demoyu planlamak için sizi takip edeceğim. Bu arada, herhangi bir sorunuz olursa veya daha fazla bilgiye ihtiyaç duyarsanız ulaşmaktan çekinmeyin.


John: Kulağa hoş geliyor, yardımın için teşekkürler Sarah. XYZ Widget hakkında daha fazla bilgi edinmeyi ve işletmemize nasıl fayda sağlayabileceğini görmeyi dört gözle bekliyorum.


Sarah: Teşekkürler John. Yakında iletişime geçeceğim. İyi günler!


John: Size de, hoşça kalın.
```

### İstediğimiz şemayı kurma

İstediğimiz çıktı "biçimini" bir Pydantic Modeli olarak belirtelim.

```python
from pydantic import BaseModel, Field
from typing import List




class CallSummary(BaseModel):
    """Bir çağrı özeti için veri modeli."""


    summary: str = Field(
        description="Çağrı transkriptinin üst düzey özeti. 3 cümleyi geçmemelidir."
    )
    products: List[str] = Field(
        description="Görüşmede tartışılan ürünlerin listesi"
    )
    rep_name: str = Field(description="Satış temsilcisinin adı")
    prospect_name: str = Field(description="Potansiyel müşterinin adı")
    action_items: List[str] = Field(description="Eylem maddelerinin listesi")
```

### Fonksiyon çağırma ile veri çıkarma

LlamaIndex'teki `OpenAIPydanticProgram` modülünü kullanarak işleri çok kolaylaştırabiliriz; sadece bir istem şablonu tanımlayın ve tanımladığımız LLM'yi ve pydantic modelini iletin.

```python
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage
```

```python
prompt = ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role="system",
            content=(
                "Satış araması transkriptlerini özetleme ve bunlardan içgörü çıkarma konusunda uzman bir asistansınız."
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                "İşte transkript: \n"
                "------\n"
                "{transcript}\n"
                "------"
            ),
        ),
    ]
)
program = OpenAIPydanticProgram.from_defaults(
    output_cls=CallSummary,
    llm=llm,
    prompt=prompt,
    verbose=True,
)
```

```python
output = program(transcript=transcript)
```

```python
Fonksiyon çağrısı: CallSummary şu argümanlarla: {"summary":"XYZ Şirketi'nden Sarah, John'un ilgisini çeken yeni ürün XYZ Widget'ı tartışmak üzere aradı. Sarah vaka çalışmalarını paylaşmayı ve bir demo planlamayı teklif etti. Vaka çalışmalarını incelemek ve demo için bir zaman ayarlamak konusunda anlaştılar. Sonraki adımlar arasında Sarah'nın bilgi göndermesi ve demoyu planlamak için takip etmesi yer alıyor.","products":["XYZ Widget"],"rep_name":"Sarah","prospect_name":"John","action_items":["Vaka çalışmalarını incele","Demo planla"]}
```

Şu anda bir Pydantic Modeli olarak istediğimiz yapılandırılmış veriye sahibiz. Hızlı bir inceleme, sonuçların beklediğimiz gibi olduğunu göstermektedir.

```python
output.dict()
```

```python
{'summary': 'XYZ Şirketi\'nden Sarah, John\'un ilgisini çeken yeni ürün XYZ Widget\'ı tartışmak üzere aradı. Sarah vaka çalışmalarını paylaşmayı ve bir demo planlamayı teklif etti. Vaka çalışmalarını incelemek ve demo için bir zaman ayarlamak konusunda anlaştılar. Sonraki adımlar arasında Sarah\'nın bilgi göndermesi ve demoyu planlamak için takip etmesi yer alıyor.',
 'products': ['XYZ Widget'],
 'rep_name': 'Sarah',
 'prospect_name': 'John',
 'action_items': ['Vaka çalışmalarını incele', 'Demo planla']}
```

### JSON modu ile veri çıkarma

Aynı şeyi fonksiyon çağırma yerine JSON modu ile yapmaya çalışalım.

```python
prompt = ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role="system",
            content=(
                "Satış araması transkriptlerini özetleme ve bunlardan içgörü çıkarma konusunda uzman bir asistansınız.\n"
                "Aşağıdaki şemayı takip eden geçerli bir JSON oluşturun:\n"
                "{json_schema}"
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                "İşte transkript: \n"
                "------\n"
                "{transcript}\n"
                "------"
            ),
        ),
    ]
)
```

```python
messages = prompt.format_messages(
    json_schema=CallSummary.schema_json(), transcript=transcript
)
```

```python
output = llm.chat(
    messages, response_format={"type": "json_object"}
).message.content
```

Geçerli bir JSON alıyoruz ancak bu sadece belirttiğimiz şemayı tekrarlıyor ve aslında çıkarma işlemini gerçekleştirmiyor.

```python
print(output)
```

```json
{
  "title": "CallSummary",
  "description": "Data model for a call summary.",
  "type": "object",
  "properties": {
    "summary": {
      "title": "Summary",
      "description": "High-level summary of the call transcript. Should not exceed 3 sentences.",
      "type": "string"
    },
    "products": {
      "title": "Products",
      "description": "List of products discussed in the call",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "rep_name": {
      "title": "Rep Name",
      "description": "Name of the sales rep",
      "type": "string"
    },
    "prospect_name": {
      "title": "Prospect Name",
      "description": "Name of the prospect",
      "type": "string"
    },
    "action_items": {
      "title": "Action Items",
      "description": "List of action items",
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["summary", "products", "rep_name", "prospect_name", "action_items"]
}
```

Şemayı belirtmek yerine sadece istediğimiz JSON formatını göstererek tekrar deneyelim.

```python
import json


prompt = ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role="system",
            content=(
                "Satış araması transkriptlerini özetleme ve bunlardan içgörü çıkarma konusunda uzman bir asistansınız.\n"
                "Aşağıdaki formatta geçerli bir JSON oluşturun:\n"
                "{json_example}"
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                "İşte transkript: \n"
                "------\n"
                "{transcript}\n"
                "------"
            ),
        ),
    ]
)


dict_example = {
    "summary": "Çağrı transkriptinin üst düzey özeti. 3 cümleyi geçmemelidir.",
    "products": ["ürün 1", "ürün 2"],
    "rep_name": "Satış temsilcisinin adı",
    "prospect_name": "Potansiyel müşterinin adı",
    "action_items": ["eylem maddesi 1", "eylem maddesi 2"],
}


json_example = json.dumps(dict_example)
```

```python
messages = prompt.format_messages(
    json_example=json_example, transcript=transcript
)
```

```python
output = llm.chat(
    messages, response_format={"type": "json_object"}
).message.content
```

Artık beklediğimiz gibi çıkarılmış yapılandırılmış verileri alabiliyoruz.

```python
print(output)
```

```json
{
  "summary": "XYZ Şirketi'nden Sarah, iş akışını kolaylaştırmak ve üretkenliği artırmak için tasarlanan yeni ürün XYZ Widget'ı tartışmak üzere John'u aradı. Vaka çalışmalarını ve John ve ekibi için bir demo planlamayı tartıştılar. Sonraki adımlar arasında Sarah'nın bilgi göndermesi ve demoyu planlamak için takip etmesi yer alıyor.",
  "products": ["XYZ Widget"],
  "rep_name": "Sarah",
  "prospect_name": "John",
  "action_items": ["Vaka çalışmalarını incele", "Demo planla"]
}
```

### Önemli Çıkarımlar

- Fonksiyon çağırma, yapılandırılmış veri çıkarma için kullanımı daha kolay olmaya devam ediyor (özellikle şemanızı önceden bir pydantic modeli olarak belirttiyseniz).
- JSON modu çıktının formatını zorunlu kılsa da, belirtilen bir şemaya karşı doğrulamaya yardımcı olmaz. Bir şemayı doğrudan iletmek beklenen JSON'u oluşturmayabilir ve ek dikkatli formatlama ve istemleme (prompting) gerektirebilir.
