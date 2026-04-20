# İstemler (Prompts)

## Kavram

İstemleme (prompting), LLM'lere ifade güçlerini veren temel girdidir. LlamaIndex; indeks oluşturmak, veri eklemek, sorgulama sırasında tarama yapmak ve nihai yanıtı sentezlemek için istemleri kullanır.

Agentic (ajan tabanlı) iş akışları oluştururken, istemleri kurgulamak ve yönetmek geliştirme sürecinin kilit bir parçasıdır. LlamaIndex, istemleri yönetmek ve bunları çeşitli şekillerde kullanmak için esnek ve güçlü bir yol sunar.

-   `RichPromptTemplate`: Değişkenler ve mantık içeren jinja tarzı istemler oluşturmak için en yeni stil.
-   `PromptTemplate`: Tek bir f-string ile istemler oluşturmak için kullanılan eski stil basit şablonlama.
-   `ChatPromptTemplate`: Mesajlar ve f-string'ler ile sohbet istemleri oluşturmak için kullanılan eski stil basit şablonlama.

LlamaIndex, kutudan çıktığı haliyle iyi çalışan bir dizi [varsayılan istem şablonu](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py) kullanır.

Buna ek olarak, `gpt-3.5-turbo` gibi sohbet modelleri için özel olarak yazılmış ve kullanılan bazı istemleri [burada](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/chat_prompts.py) bulabilirsiniz.

Kullanıcılar, çerçevenin (framework) davranışını daha fazla özelleştirmek için kendi istem şablonlarını da sağlayabilirler. Özelleştirme için en iyi yöntem, yukarıdaki bağlantıdan varsayılan istemi kopyalamak ve bunu herhangi bir değişiklik için temel olarak kullanmaktır.

## Kullanım Kalıbı (Usage Pattern)

İstemleri kullanmak basittir. Aşağıda, jinja tarzı bir istem şablonu oluşturmak için `RichPromptTemplate` kullanımına dair bir örnek verilmiştir:

```python
from llama_index.core.prompts import RichPromptTemplate

template_str = """Aşağıda bağlam bilgisi sağlanmıştır.
---------------------
{{ context_str }}
---------------------
Bu bilgileri göz önünde bulundurarak lütfen soruyu yanıtlayın: {{ query_str }}
"""
qa_template = RichPromptTemplate(template_str)

# Metin istemi oluşturabilirsiniz (tamamlama API'si için)
prompt = qa_template.format(context_str=..., query_str=...)

# Veya kolayca mesaj istemlerine dönüştürebilirsiniz (sohbet API'si için)
messages = qa_template.format_messages(context_str=..., query_str=...)
```

`RichPromptTemplate`'den tam olarak yararlanma ve diğer istem şablonları hakkındaki detaylar için [Kullanım Kalıbı Kılavuzumuza](/python/framework/module_guides/models/prompts/usage_pattern) göz atın.

## Örnek Kılavuzlar

İstem Mühendisliği (Prompt Engineering) Kılavuzları

-   [Gelişmiş İstemler (Advanced Prompts)](/python/examples/prompts/advanced_prompts)
-   [RichPromptTemplate Özellikleri](/python/examples/prompts/rich_prompt_template_features)

Basit Özelleştirme Örnekleri

-   [Tamamlama (Completion) istemleri](/python/examples/customization/prompts/completion_prompts)
-   [Sohbet (Chat) istemleri](/python/examples/customization/prompts/chat_prompts)
-   [Prompt Mixin](/python/examples/prompts/prompt_mixin)

Deneysel

-   [Duygusal İstemleme (Emotion Prompting)](/python/examples/prompts/emotion_prompt)