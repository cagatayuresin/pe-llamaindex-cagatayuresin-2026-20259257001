# Yapılandırılmış LLM'leri (Structured LLMs) Kullanma

LlamaIndex'te yapılandırılmış veri çıkarmanın en üst düzey yolu, bir "Structured LLM" (Yapılandırılmış LLM) oluşturmaktır. Önce, Pydantic sınıfımızı daha önce olduğu gibi tanımlayalım:

```python
from datetime import datetime
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    """Bir faturadaki kalem (satır öğesi)."""

    item_name: str = Field(description="Bu öğenin adı")
    price: float = Field(description="Bu öğenin fiyatı")


class Invoice(BaseModel):
    """Bir faturadaki bilgilerin temsili."""

    invoice_id: str = Field(
        description="Bu fatura için benzersiz bir tanımlayıcı, genellikle bir numara"
    )
    date: datetime = Field(description="Bu faturanın oluşturulduğu tarih")
    line_items: list[LineItem] = Field(
        description="Bu faturadaki tüm kalemlerin listesi"
    )
```

Eğer LlamaIndex'i ilk kez kullanıyorsanız, bağımlılıklarımızı alalım:

-   LLM'i almak için `pip install llama-index-core llama-index-llms-openai` (Basitlik için OpenAI kullanacağız, ancak her zaman başka birini de kullanabilirsiniz)
-   Bir OpenAI API anahtarı alın ve bunu `OPENAI_API_KEY` adında bir ortam değişkeni olarak ayarlayın.
-   PDFReader'ı almak için `pip install llama-index-readers-file`
    -   Not: PDF'lerin daha iyi ayrıştırılması için [LlamaParse](https://docs.cloud.llamaindex.ai/llamaparse/getting_started) kullanmanızı öneririz.

Şimdi gerçek bir faturanın metnini yükleyelim:

```python
from llama_index.readers.file import PDFReader
from pathlib import Path

pdf_reader = PDFReader()
documents = pdf_reader.load_data(file=Path("./uber_receipt.pdf"))
text = documents[0].text
```

Şimdi bir LLM oluşturalım, ona Pydantic sınıfımızı verelim ve ardından faturanın düz metnini kullanarak `complete` (tamamla) metodunu çağıralım:

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o")
sllm = llm.as_structured_llm(Invoice)

response = sllm.complete(text)
```

`response` nesnesi, iki özelliğe sahip bir LlamaIndex `CompletionResponse` nesnesidir: `text` ve `raw`. `text` özelliği, Pydantic tarafından işlenen yanıtın JSON serileştirilmiş halini içerir:

```python
import json
json_response = json.loads(response.text)
print(json.dumps(json_response, indent=2))
```

```json
{
    "invoice_id": "Visa \u2022\u2022\u2022\u20224469",
    "date": "2024-10-10T19:49:00",
    "line_items": [
        {"item_name": "Trip fare", "price": 12.18},
        {"item_name": "Access for All Fee", "price": 0.1},
        {"item_name": "CA Driver Benefits", "price": 0.32},
        {"item_name": "Booking Fee", "price": 2.0},
        {"item_name": "San Francisco City Tax", "price": 0.21}
    ]
}
```

Bu faturanın bir ID'si olmadığını, bu yüzden LLM'in elinden geleni yapıp kredi kartı numarasını kullandığını fark edin. Pydantic doğrulaması her zaman garanti değildir!

Yanıtın `raw` özelliği (biraz kafa karıştırıcı olsa da) Pydantic nesnesinin kendisini içerir:

```python
from pprint import pprint

pprint(response.raw)
```

```python
Invoice(
    invoice_id="Visa ••••4469",
    date=datetime.datetime(2024, 10, 10, 19, 49),
    line_items=[
        LineItem(item_name="Trip fare", price=12.18),
        LineItem(item_name="Access for All Fee", price=0.1),
        LineItem(item_name="CA Driver Benefits", price=0.32),
        LineItem(item_name="Booking Fee", price=2.0),
        LineItem(item_name="San Francisco City Tax", price=0.21),
    ],
)
```

Pydantic'in sadece bir dizeyi (string) çevirmekle kalmayıp, tam bir `datetime` nesnesi oluşturduğuna dikkat edin.

Yapılandırılmış bir LLM (Structured LLM), tıpkı normal bir LLM sınıfı gibi çalışır: `chat`, `stream`, `achat`, `astream` vb. metodları çağırabilirsiniz ve her durumda Pydantic nesneleriyle yanıt verecektir. Ayrıca, Yapılandırılmış LLM'inizi `VectorStoreIndex.as_query_engine(llm=sllm)` metoduna bir parametre olarak geçebilirsiniz; böylece RAG sorgularınıza otomatik olarak yapılandırılmış nesnelerle yanıt verecektir.

Yapılandırılmış LLM, tüm komut (prompt) işlemlerini sizin yerinize halleder. Komut üzerinde daha fazla kontrole sahip olmak istiyorsanız, [Yapılandırılmış Tahmin (Structured Prediction)](/python/framework/understanding/extraction/structured_prediction) bölümüne geçin.