# LlamaIndex Soyutlamaları Dahilinde LLM'leri Özelleştirme

Bu LLM soyutlamalarını LlamaIndex'teki diğer modüllerimizle (indeksler, retriever'lar, sorgu motorları, ajanlar) birlikte kullanarak verileriniz üzerinde gelişmiş iş akışları oluşturabilirsiniz.

Varsayılan olarak OpenAI'ın `gpt-3.5-turbo` modelini kullanıyoruz. Ancak kullanılan temeldeki LLM'i özelleştirmeyi seçebilirsiniz.

## Örnek: Temeldeki LLM'i Değiştirme

Kullanılan LLM'in özelleştirilmesine dair bir örnek kod parçası aşağıda gösterilmiştir.

Bu örnekte, `gpt-3.5-turbo` yerine `gpt-4o-mini` kullanıyoruz. Mevcut modeller arasında `gpt-4o-mini`, `gpt-4o`, `o3-mini` ve daha fazlası bulunmaktadır.

```python
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

# LLM'i tanımla
llm = OpenAI(temperature=0.1, model="gpt-4o-mini")

# küresel varsayılan LLM'i değiştir
Settings.llm = llm

documents = SimpleDirectoryReader("data").load_data()

# indeksi oluştur
index = VectorStoreIndex.from_documents(documents)

# LLM'i yerel olarak geçersiz kıl (override)
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query(
    "Yazar, Y Combinator'daki zamanından sonra ne yaptı?"
)
```

## Örnek: Özel Bir LLM Modeli Kullanma - Gelişmiş

Özel bir LLM modeli kullanmak için sadece `LLM` sınıfını (veya daha basit bir arayüz için `CustomLLM` sınıfını) uygulamanız yeterlidir. Metni modele iletmekten ve yeni oluşturulan token'ları döndürmekten siz sorumlu olacaksınız.

Bu uygulama yerel bir model olabileceği gibi kendi API'nız etrafında bir sarmalayıcı (wrapper) da olabilir.

Tamamen gizli bir deneyim için ayrıca bir [yerel embedding modeli](/python/framework/module_guides/models/embeddings) de kurmanız gerektiğini unutmayın.

İşte küçük bir şablon (boilerplate) örneği:

```python
from typing import Optional, List, Mapping, Any

from llama_index.core import SimpleDirectoryReader, SummaryIndex
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings


class BizimLLM(CustomLLM):
    context_window: int = 3900
    num_output: int = 256
    model_name: str = "ozel"
    dummy_response: str = "Benim yanıtım"

    @property
    def metadata(self) -> LLMMetadata:
        """LLM meta verilerini al."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        return CompletionResponse(text=self.dummy_response)

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseGen:
        response = ""
        for token in self.dummy_response:
            response += token
            yield CompletionResponse(text=response, delta=token)


# LLM'imizi tanımlayalım
Settings.llm = BizimLLM()

# embedding modelini tanımlayalım
Settings.embed_model = "local:BAAI/bge-base-en-v1.5"


# Verilerinizi yükleyin
documents = SimpleDirectoryReader("./data").load_data()
index = SummaryIndex.from_documents(documents)

# Sorgula ve yanıtı yazdır
query_engine = index.as_query_engine()
response = query_engine.query("<sorgu_metni>")
print(response)
```

Bu yöntemi kullanarak herhangi bir LLM'i kullanabilirsiniz. Belki yerel olarak çalışan veya kendi sunucunuzda çalışan bir modeliniz vardır. Sınıf uygulandığı ve oluşturulan token'lar döndürüldüğü sürece çalışması gerekir. Her modelin bağlam uzunluğu biraz farklı olduğundan, istem boyutlarını özelleştirmek için istem yardımcısını (prompt helper) kullanmamız gerektiğini unutmayın.

Dekoratör (decorator) isteğe bağlıdır ancak LLM çağrıları üzerindeki geri aramalar (callbacks) aracılığıyla gözlemlenebilirlik sağlar.

İyi bir performans elde etmek için dahili istemleri ayarlamanız gerekebileceğini unutmayın. Öyle olsa bile, LlamaIndex'in dahili olarak kullandığı karmaşık sorguları işleyebildiğinden emin olmak için yeterince büyük bir LLM kullanmalısınız, sonuçlar buna göre değişiklik gösterebilir.

Tüm varsayılan dahili istemlerin bir listesi [burada](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py) ve sohbete özel istemler de [burada](https://github.com/run-llama/llama_index/blob/main/llama_index/prompts/chat_prompts.py) listelenmiştir. Ayrıca [kendi özel istemlerinizi](/python/framework/module_guides/models/prompts) de uygulayabilirsiniz.