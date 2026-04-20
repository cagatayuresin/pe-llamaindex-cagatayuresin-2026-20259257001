# Yapılandırılmış Veri Çıkarımına Giriş

LLM'ler veri anlama konusunda mükemmeldir; bu da onları en önemli kullanım durumlarından birine yönlendirir: normal insan dilini (biz buna **yapılandırılmamış veri** diyoruz) bilgisayar programları tarafından tüketilmek üzere belirli, düzenli ve beklenen formatlara dönüştürme yeteneği. Bu sürecin çıktısına **yapılandırılmış veri** diyoruz. Dönüştürme sürecinde çok fazla gereksiz veri genellikle göz ardı edildiğinden, buna **çıkarım** (extraction) diyoruz.

LlamaIndex'te yapılandırılmış veri çıkarımının işleyişinin temelinde [Pydantic](https://docs.pydantic.dev/latest/) sınıfları yatar: Pydantic'te bir veri yapısı tanımlarsınız ve LlamaIndex, LLM'den gelen çıktıyı bu yapıya zorlamak (coerce) için Pydantic ile birlikte çalışır.

## Pydantic Nedir?

Pydantic, yaygın olarak kullanılan bir veri doğrulama ve dönüştürme kütüphanesidir. Büyük ölçüde Python tip bildirimlerine dayanır. Projenin kendi dökümantasyonunda [kapsamlı bir Pydantic kılavuzu](https://docs.pydantic.dev/latest/concepts/models/) vardır, ancak biz burada çok temel konuları ele alacağız.

Bir Pydantic sınıfı oluşturmak için Pydantic'in `BaseModel` sınıfından miras alın:

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "Jane Doe"
```

Bu örnekte, `id` ve `name` adında iki alanı olan bir `User` sınıfı oluşturdunuz. `id` alanını bir tamsayı (integer), `name` alanını ise varsayılan değeri `Jane Doe` olan bir dize (string) olarak tanımladınız.

Bu modelleri iç içe yerleştirerek daha karmaşık yapılar oluşturabilirsiniz:

```python
from typing import List, Optional
from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = "x"
    banana: str = "y"


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]
```

Artık `Spam` sınıfının bir `foo` alanı ve bir `bars` listesi var. `Foo` sınıfının bir `count` değeri ve isteğe bağlı bir `size` değeri vardır; `bars` ise her biri `apple` ve `banana` özelliklerine sahip bir nesne listesidir.

## Pydantic Nesnelerini JSON Şemalarına Dönüştürme

Pydantic, Pydantic sınıflarının [popüler standartlara](https://docs.pydantic.dev/latest/concepts/json_schema/) uygun JSON serileştirilmiş şema nesnelerine dönüştürülmesini destekler. Örneğin, yukarıdaki `User` sınıfı şuna serileştirilir:

```json
{
  "properties": {
    "id": {
      "title": "Id",
      "type": "integer"
    },
    "name": {
      "default": "Jane Doe",
      "title": "Name",
      "type": "string"
    }
  },
  "required": ["id"],
  "title": "User",
  "type": "object"
}
```

Bu özellik kritiktir: Bu JSON formatındaki şemalar genellikle LLM'lere iletilir ve LLM'ler de bunları verilerin nasıl döndürüleceğine dair talimatlar olarak kullanır.

## Açıklamaları (Annotations) Kullanma

Belirtildiği gibi LLM'ler, Pydantic'ten gelen JSON şemalarını verilerin nasıl döndürüleceğine dair talimatlar olarak kullanır. Onlara yardımcı olmak ve döndürülen verilerinizin doğruluğunu artırmak için, nesnelerin ve alanların ne işe yaradığına dair doğal dilde açıklamalar eklemek faydalıdır. Pydantic, bu konuda [docstring'ler](https://www.geeksforgeeks.org/python-docstrings/) ve [Field'lar](https://docs.pydantic.dev/latest/concepts/fields/) ile destek sağlar.

Bundan sonraki tüm örneklerimizde aşağıdaki örnek Pydantic sınıflarını kullanacağız:

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

Bu, çok daha karmaşık bir JSON şemasına genişler:

```json
{
  "$defs": {
    "LineItem": {
      "description": "Bir faturadaki kalem (satır öğesi).",
      "properties": {
        "item_name": {
          "description": "Bu öğenin adı",
          "title": "Item Name",
          "type": "string"
        },
        "price": {
          "description": "Bu öğenin fiyatı",
          "title": "Price",
          "type": "number"
        }
      },
      "required": ["item_name", "price"],
      "title": "LineItem",
      "type": "object"
    }
  },
  "description": "Bir faturadaki bilgilerin temsili.",
  "properties": {
    "invoice_id": {
      "description": "Bu fatura için benzersiz bir tanımlayıcı, genellikle bir numara",
      "title": "Invoice Id",
      "type": "string"
    },
    "date": {
      "description": "Bu faturanın oluşturulduğu tarih",
      "format": "date-time",
      "title": "Date",
      "type": "string"
    },
    "line_items": {
      "description": "Bu faturadaki tüm kalemlerin listesi",
      "items": {
        "$ref": "#/$defs/LineItem"
      },
      "title": "Line Items",
      "type": "array"
    }
  },
  "required": ["invoice_id", "date", "line_items"],
  "title": "Invoice",
  "type": "object"
}
```

Pydantic ve ürettiği şemalar hakkında temel bir anlayışa sahip olduğunuza göre, LlamaIndex'te yapılandırılmış veri çıkarımı için Pydantic sınıflarını kullanmaya geçebilirsiniz; [Yapılandırılmış LLM'ler (Structured LLMs)](/python/framework/understanding/extraction/structured_llms) ile başlıyoruz.