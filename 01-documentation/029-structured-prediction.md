# Yapılandırılmış Tahmin (Structured Prediction)

Yapılandırılmış Tahmin (Structured Prediction), uygulamanızın LLM'i nasıl çağıracağı ve Pydantic'i nasıl kullanacağı üzerinde size daha ayrıntılı kontrol sağlar. Önceki örnekte yaptığımız gibi aynı `Invoice` sınıfını kullanacağız, PDF'i yükleyeceğiz ve yine OpenAI kullanacağız. Ancak yapılandırılmış bir LLM oluşturmak yerine, LLM sınıfının kendisinin bir metodu olan `structured_predict` metodunu çağıracağız.

`structured_predict`, argüman olarak bir Pydantic sınıfı ve bir Komut Şablonu (Prompt Template) ile birlikte, komut şablonundaki herhangi bir değişkenin anahtar kelime argümanlarını (keyword arguments) alır.

```python
from llama_index.core.prompts import PromptTemplate

prompt = PromptTemplate(
    "Aşağıdaki metinden bir fatura çıkarın. Eğer bir fatura ID'si bulamazsanız, fatura ID'si olarak faturasını kestiğiniz '{company_name}' şirket adını ve tarihi kullanın: {text}"
)

response = llm.structured_predict(
    Invoice, prompt, text=text, company_name="Uber"
)
```

Gördüğünüz gibi bu yöntem, Pydantic'in verileri doğru şekilde ayrıştırmak için tek başına yeterli olmadığı durumlarda LLM'in ne yapması gerektiğine dair ek komut yönlendirmeleri dahil etmemize olanak tanır. Bu durumda yanıt nesnesi Pydantic nesnesinin kendisidir. İstersek çıktıyı JSON olarak alabiliriz:

```python
import json
json_output = response.model_dump_json()
print(json.dumps(json.loads(json_output), indent=2))
```

```json
{
    "invoice_id": "Uber-2024-10-10",
    "date": "2024-10-10T19:49:00",
    "line_items": [
        {"item_name": "Trip fare", "price": 12.18},
        {"item_name": "Access for All Fee", "price": 0.1},
        "..."
    ]
}
```

`structured_predict` metodunun asenkron (`astructured_predict`) ve akışlı (`stream_structured_predict`, `astream_structured_predict`) dahil olmak üzere farklı kullanım durumları için birkaç varyantı mevcuttur.

## Arka Planda Neler Oluyor?

Hangi LLM'i kullandığınıza bağlı olarak, `structured_predict` metodu LLM'i çağırmak ve çıktıyı ayrıştırmak için iki farklı sınıftan birini kullanır.

### FunctionCallingProgram

Kullandığınız LLM eğer bir fonksiyon çağırma (function calling) API'ına sahipse, `FunctionCallingProgram` şunları yapar:

-   Pydantic nesnesini bir araca (tool) dönüştürür.
-   LLM'i bu aracı kullanmaya zorlayarak komutu iletir.
-   Oluşturulan Pydantic nesnesini döndürür.

Bu genellikle daha güvenilir bir yöntemdir ve eğer mevcutsa tercih edilerek kullanılır. Ancak bazı LLM'ler yalnızca metin tabanlıdır ve diğer yöntemi kullanırlar.

### LLMTextCompletionProgram

Eğer LLM yalnızca metin tabanlıysa, `LLMTextCompletionProgram` şunları yapar:

-   Pydantic şemasını JSON olarak çıktı verir.
-   Şemayı ve verileri, şemaya uygun bir formda yanıt vermesi için komut talimatlarıyla birlikte LLM'e gönderir.
-   LLM'den dönen ham metni geçirerek Pydantic nesnesi üzerinde `model_validate_json()` metodunu çağırır.

Bu yöntem belirgin şekilde daha az güvenilirdir ancak tüm metin tabanlı LLM'ler tarafından desteklenir.

## Tahmin (Prediction) Sınıflarını Doğrudan Çağırma

Uygulamada `structured_predict` her türlü LLM için iyi çalışmalıdır; ancak daha alt düzey kontrole ihtiyacınız varsa `FunctionCallingProgram` ve `LLMTextCompletionProgram` sınıflarını doğrudan çağırabilir ve süreci daha da özelleştirebilirsiniz:

```python
from llama_index.core.program import LLMTextCompletionProgram

textCompletion = LLMTextCompletionProgram.from_defaults(
    output_cls=Invoice,
    llm=llm,
    prompt=PromptTemplate(
        "Aşağıdaki metinden bir fatura çıkarın. Eğer bir fatura ID'si bulamazsanız, fatura ID'si olarak faturasını kestiğiniz '{company_name}' şirket adını ve tarihi kullanın: {text}"
    ),
)

output = textCompletion(company_name="Uber", text=text)
```

Yukarıdaki işlem, fonksiyon çağırma API'ları olmayan bir LLM üzerinde `structured_predict` çağırmakla aynıdır ve tıpkı `structured_predict` gibi bir Pydantic nesnesi döndürür. Ancak `PydanticOutputParser` sınıfını alt sınıflara ayırarak (subclassing) çıktının nasıl ayrıştırılacağını özelleştirebilirsiniz:

```python
from llama_index.core.output_parsers import PydanticOutputParser


class MyOutputParser(PydanticOutputParser):
    def get_pydantic_object(self, text: str):
        # Burada mevcut olandan daha akıllıca bir işlem yapın
        return self.output_parser.model_validate_json(text)


textCompletion = LLMTextCompletionProgram.from_defaults(
    llm=llm,
    prompt=PromptTemplate(
        "Aşağıdaki metinden bir fatura çıkarın. Eğer bir fatura ID'si bulamazsanız, fatura ID'si olarak faturasını kestiğiniz '{company_name}' şirket adını ve tarihi kullanın: {text}"
    ),
    output_parser=MyOutputParser(output_cls=Invoice),
)
```

Bu yöntem, ayrıştırma konusunda yardıma ihtiyaç duyan düşük performanslı bir LLM kullanıyorsanız kullanışlıdır.

Son bölümde, aynı çağrıda birden fazla yapıyı çıkarmak da dahil olmak üzere [yapılandırılmış verileri çıkarmak için daha alt düzey çağrılara](/python/framework/understanding/extraction/lower_level) göz atacağız.