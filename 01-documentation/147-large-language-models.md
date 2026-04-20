# Büyük Dil Modelleri (Large Language Models)

##### SSS (FAQ)

1. [Özel bir LLM nasıl tanımlanır?](#1-özel-bir-llm-nasıl-tanımlanır)
2. [Farklı bir OpenAI modeli nasıl kullanılır?](#2-farklı-bir-openai-modeli-nasıl-kullanılır)
3. [İstemimi (prompt) nasıl özelleştirebilirim?](#3-istemimi-prompt-nasıl-özelleştirebilirim)
4. [Modelimi ince ayar (fine-tune) yapmam gerekli mi?](#4-modelimi-ince-ayar-fine-tune-yapmam-gerekli-mi)
5. [LLM'nin Çince/İtalyanca/Fransızca cevap vermesini istiyorum ama sadece İngilizce cevap veriyor, ne yapmalıyım?](#5-llmnin-çinceitalyancafransızca-cevap-vermesini-istiyorum-ama-sadece-ingilizce-cevap-veriyor-ne-yapmalıyım)
6. [LlamaIndex GPU hızlandırmalı mı?](#6-llamaindex-gpu-hızlandırmalı-mı)

---

##### 1. Özel bir LLM nasıl tanımlanır?

Özel bir LLM tanımlamak için [Kullanım Özelleştirme (Usage Custom)](/python/framework/module_guides/models/llms/usage_custom#example-using-a-custom-llm-model---advanced) kılavuzuna erişebilirsiniz.

---

##### 2. Farklı bir OpenAI modeli nasıl kullanılır?

Farklı bir OpenAI modeli kullanmak için kendi özel modelinizi ayarlamak üzere [Model Yapılandırma](/python/examples/llm/openai) kılavuzuna erişebilirsiniz.

---

##### 3. İstemimi (prompt) nasıl özelleştirebilirim?

İstemlerinizi nasıl özelleştireceğinizi öğrenmek için [İstemler (Prompts)](/python/framework/module_guides/models/prompts) kılavuzuna erişebilirsiniz.

---

##### 4. Modelimi ince ayar (fine-tune) yapmam gerekli mi?

Hayır. Daha iyi sonuçlar sağlayabilecek izole modüller vardır ancak modelinizi ince ayar yapmanız zorunlu değildir; LlamaIndex'i modelinizi ince ayar yapmaya gerek duymadan kullanabilirsiniz.

---

##### 5. LLM'nin Çince/İtalyanca/Fransızca cevap vermesini istiyorum ama sadece İngilizce cevap veriyor, ne yapmalıyım?

LLM'nin başka bir dilde daha doğru yanıt vermesi için çıktı dilini daha fazla zorlamak amacıyla istemleri güncelleyebilirsiniz.

```python
response = query_engine.query("Sorgunuzun geri kalanı... \nİtalyanca yanıtla")
```

Alternatif olarak:

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

llm = OpenAI(system_prompt="Her zaman İtalyanca yanıtla.")

# global bir llm ayarla
Settings.llm = llm

query_engine = load_index_from_storage(
    storage_context,
).as_query_engine()
```

---

##### 6. LlamaIndex GPU hızlandırmalı mı?

Evet, yerel olarak çalıştırırken bir dil modelini (LLM) GPU üzerinde çalıştırabilirsiniz. [llama2 kurulumu](/python/examples/vector_stores/simpleindexdemollama-local) dökümantasyonunda GPU destekli LLM'lerin ayarlanmasına dair bir örnek bulabilirsiniz.

---