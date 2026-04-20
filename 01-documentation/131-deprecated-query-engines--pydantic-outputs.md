# (Kullanımdan Kaldırıldı) Sorgu Motorları + Pydantic Çıktıları ((Deprecated) Query Engines + Pydantic Outputs)

<Aside type="tip">
  Bu kılavuz, bir RAG iş akışında yapılandırılmış çıktıları çıkarmanın (extracting) kullanımdan kaldırılmış bir yöntemine atıfta bulunmaktadır. Daha fazla ayrıntı için [yapılandırılmış çıktı başlangıç kılavuzumuza](/python/examples/structured_outputs/structured_outputs) göz atın.
</Aside>

`index.as_query_engine()` ve onun temelindeki `RetrieverQueryEngine` kullanarak, ek LLM çağrılarına gerek duymadan (tipik bir çıktı ayrıştırıcısının aksine) yapılandırılmış Pydantic çıktılarını destekleyebiliriz.

Her sorgu motoru, `RetrieverQueryEngine` içindeki aşağıdaki `response_mode` değerlerini kullanarak entegre yapılandırılmış yanıtları destekler:

-   `refine`
-   `compact`
-   `tree_summarize`
-   `accumulate` (beta, nesnelere dönüştürmek için ekstra ayrıştırma gerektirir)
-   `compact_accumulate` (beta, nesnelere dönüştürmek için ekstra ayrıştırma gerektirir)

Arka planda bu, kurduğunuz LLM'e bağlı olarak `OpenAIPydanticProgram` veya `LLMTextCompletionProgram` kullanır. Ara LLM yanıtları varsa (yani birden fazla LLM çağrısı içeren `refine` veya `tree_summarize` sırasında), Pydantic nesnesi bir sonraki LLM istemine (prompt) bir JSON nesnesi olarak eklenir.

## Kullanım Kalıbı (Usage Pattern)

Öncelikle, çıkarmak istediğiniz nesneyi tanımlamanız gerekir.

```python
from typing import List
from pydantic import BaseModel


class Biyografi(BaseModel):
    """Bir biyografi için veri modeli."""

    ad: str
    en_iyi_bilinen_ozellikleri: List[str]
    ek_bilgi: str
```

Ardından, sorgu motorunuzu oluşturursunuz.

```python
query_engine = index.as_query_engine(
    response_mode="tree_summarize", output_cls=Biyografi
)
```

Son olarak, bir yanıt alabilir ve çıktıyı inceleyebilirsiniz.

```python
response = query_engine.query("Paul Graham kimdir?")

print(response.ad)
# > 'Paul Graham'
print(response.en_iyi_bilinen_ozellikleri)
# > ['Bel üzerine çalışmak', 'Viaweb'in kurucu ortaklığı', 'Arc programlama dilini oluşturmak']
print(response.ek_bilgi)
# > "Paul Graham bir bilgisayar bilimcisi, girişimci ve yazardır. En çok ... ile tanınır."
```

## Modüller

Ayrıntılı kullanım aşağıdaki not defterlerinde mevcuttur:

-   [Sorgu Motoru ile Yapılandırılmış Çıktılar](/python/examples/query_engine/pydantic_query_engine)
-   [Tree Summarize ile Yapılandırılmış Çıktılar](/python/examples/response_synthesizers/pydantic_tree_summarize)