# Çıktı Ayrıştırma Modülleri (Output Parsing Modules)

LlamaIndex, diğer çerçeveler tarafından sunulan çıktı ayrıştırma modülleriyle entegrasyonları destekler. Bu çıktı ayrıştırma modülleri aşağıdaki şekillerde kullanılabilir:

-   Herhangi bir istem / sorgu için formatlama talimatları sağlamak amacıyla (`output_parser.format` aracılığıyla).
-   LLM çıktıları için "ayrıştırma" (parsing) sağlamak amacıyla (`output_parser.parse` aracılığıyla).

### Guardrails

Guardrails; çıktı şemalarının belirlenmesi, doğrulanması ve düzeltilmesi için kullanılan açık kaynaklı bir Python paketidir. Aşağıdaki kod örneğine göz atın.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.output_parsers.guardrails import GuardrailsOutputParser
from llama_index.llms.openai import OpenAI


# belgeleri yükle, indeksi oluştur
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectorStoreIndex(documents, chunk_size=512)

# sorgu / çıktı özelliğini tanımla
rail_spec = """
<rail version="0.1">

<output>
    <list name="points" description="Yazarın hayatındaki olaylarla ilgili madde işaretleri.">
        <object>
            <string name="explanation" format="one-line" on-fail-one-line="noop" />
            <string name="explanation2" format="one-line" on-fail-one-line="noop" />
            <string name="explanation3" format="one-line" on-fail-one-line="noop" />
        </object>
    </list>
</output>

<prompt>

Sorgu dizesi buraya gelir.

@xml_prefix_prompt

{output_schema}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""

# çıktı ayrıştırıcıyı tanımla
output_parser = GuardrailsOutputParser.from_rail_string(
    rail_spec, llm=OpenAI()
)

# Çıktı ayrıştırıcıyı LLM'e bağla
llm = OpenAI(output_parser=output_parser)

# yapılandırılmış bir yanıt al
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query(
    "Yazarın büyürken yaptığı üç şey nedir?",
)
print(response)
```

Çıktı:

```
{'points': [{'explanation': 'Kısa hikayeler yazmak', 'explanation2': 'Bir IBM 1401 üzerinde programlama yapmak', 'explanation3': 'Mikrobilgisayarlar kullanmak'}]}
```

### Langchain

Langchain ayrıca LlamaIndex içerisinde kullanabileceğiniz çıktı ayrıştırma modülleri sunar.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.output_parsers import LangchainOutputParser
from llama_index.llms.openai import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


# belgeleri yükle, indeksi oluştur
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectorStoreIndex.from_documents(documents)

# çıktı şemasını tanımla
response_schemas = [
    ResponseSchema(
        name="Education",
        description="Yazarın eğitim deneyimini/geçmişini tanımlar.",
    ),
    ResponseSchema(
        name="Work",
        description="Yazarın iş deneyimini/geçmişini tanımlar.",
    ),
]

# çıktı ayrıştırıcıyı tanımla
lc_output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas
)
output_parser = LangchainOutputParser(lc_output_parser)

# Çıktı ayrıştırıcıyı LLM'e bağla
llm = OpenAI(output_parser=output_parser)

# yapılandırılmış bir yanıt al
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query(
    "Yazarın büyürken yaptığı birkaç şey nedir?",
)
print(str(response))
```

Çıktı:

```
{'Education': 'Üniversiteden önce yazar kısa hikayeler yazdı ve bir IBM 1401 üzerinde programlama deneyleri yaptı.', 'Work': 'Yazar okul dışında yazma ve programlama üzerine çalıştı.'}
```

### Kılavuzlar

Daha fazla örnek:

-   [Guardrails](/python/examples/output_parsing/guardrailsdemo)
-   [Langchain](/python/examples/output_parsing/langchainoutputparserdemo)
-   [Guidance Pydantic Programı](/python/examples/output_parsing/guidance_pydantic_program)
-   [Guidance Alt Sorusu (Sub-Question)](/python/examples/output_parsing/guidance_sub_question)
-   [OpenAI Pydantic Programı](/python/examples/output_parsing/openai_pydantic_program)