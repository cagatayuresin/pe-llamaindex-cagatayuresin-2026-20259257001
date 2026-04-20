# Alt Düzey Yapılandırılmış Veri Çıkarımı

Eğer LLM'iniz araç çağırmayı (tool calling) destekliyorsa ve LlamaIndex'in verileri nasıl çıkardığı üzerinde daha doğrudan kontrole ihtiyacınız varsa, doğrudan bir LLM üzerinde `chat_with_tools` metodunu kullanabilirsiniz. Eğer LLM'iniz araç çağırmayı desteklemiyorsa, LLM'inizi doğrudan talimatlarla yönlendirebilir ve çıktıyı kendiniz ayrıştırabilirsiniz. Her ikisini de nasıl yapacağınızı göstereceğiz.

## Araçları Doğrudan Çağırma

```python
from llama_index.core.program.function_program import get_function_tool

tool = get_function_tool(Invoice)

resp = llm.chat_with_tools(
    [tool],
    # chat_history=chat_history,  # İsteğe bağlı olarak user_msg yerine sohbet geçmişini geçebilirsiniz
    user_msg="Aşağıdaki metinden bir fatura çıkarın: " + text,
    tool_required=True,  # İsteğe bağlı olarak araç çağrısını zorunlu kılabilirsiniz
)

tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_calls=False
)

outputs = []
for tool_call in tool_calls:
    if tool_call.tool_name == "Invoice":
        outputs.append(Invoice(**tool_call.tool_kwargs))

# çıktılarınızı kullanın
print(outputs[0])
```

Eğer LLM'in bir araç çağırma API'ı varsa, bu işlem `structured_predict` ile aynıdır. Ancak LLM destekliyorsa, isteğe bağlı olarak birden fazla araç çağrısına izin verebilirsiniz. Bu özellik, bu örnekte olduğu gibi aynı girdiden birden fazla nesne çıkarmanıza olanak tanır:

```python
from llama_index.core.program.function_program import get_function_tool

tool = get_function_tool(LineItem)

resp = llm.chat_with_tools(
    [tool],
    user_msg="Aşağıdaki metinden fatura kalemlerini (line items) çıkarın: " + text,
    allow_parallel_tool_calls=True,
)

tool_calls = llm.get_tool_calls_from_response(
    resp, error_on_no_tool_calls=False
)

outputs = []
for tool_call in tool_calls:
    if tool_call.tool_name == "LineItem":
        outputs.append(LineItem(**tool_call.tool_kwargs))

# çıktılarınızı kullanın
print(outputs)
```

Amacınız tek bir LLM çağrısından birden fazla Pydantic nesnesi çıkarmaksa, bunu bu şekilde yapabilirsiniz.

## Doğrudan Komut Verme (Direct Prompting)

Eğer herhangi bir sebeple LlamaIndex'in çıkarımı kolaylaştırma girişimleri sizin için işe yaramıyorsa, bunları bir kenara bırakıp LLM'e doğrudan komut verebilir ve çıktıyı kendiniz ayrıştırabilirsiniz:

```python
import json
from pprint import pprint

schema = Invoice.model_json_schema()
prompt = "İşte bir fatura için JSON şeması: " + json.dumps(
    schema, indent=2
)
prompt += (
    """
  Aşağıdaki metinden bir fatura çıkarın.
  Çıktınızı yukarıdaki şemaya göre bir JSON nesnesi olarak formatlayın.
  JSON nesnesinden başka hiçbir metin eklemeyin.
  Markdown formatlamasını atlayın. Herhangi bir giriş veya açıklama dahil etmeyin.
"""
    + text
)

response = llm.complete(prompt)

print(response)

invoice = Invoice.model_validate_json(response.text)

pprint(invoice)
```

Tebrikler! LlamaIndex'te yapılandırılmış veri çıkarımı hakkında bilinmesi gereken her şeyi öğrendiniz.

## Diğer Kılavuzlar

LlamaIndex ile yapılandırılmış veri çıkarımına daha derin bir bakış için aşağıdaki kılavuzları inceleyin:

-   [Yapılandırılmış Çıktılar (Structured Outputs)](/python/framework/module_guides/querying/structured_outputs)
-   [Pydantic Programları](/python/framework/module_guides/querying/structured_outputs/pydantic_program)
-   [Çıktı Ayrıştırma (Output Parsing)](/python/framework/module_guides/querying/structured_outputs/output_parser)

## Bonus Bölüm

Yapılandırılmış girdiler kullanarak LLM'inizin performansını nasıl artıracağınızı merak ediyorsanız, [bu kılavuza](/python/framework/understanding/extraction/structured_input) göz atın!