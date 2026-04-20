# LLM'leri Kullanma (Using LLMs)

## Kavram

Uygun Büyük Dil Modelini (LLM) seçmek, verileriniz üzerinde herhangi bir LLM uygulaması oluştururken dikkate almanız gereken ilk adımlardan biridir.

LLM'ler, LlamaIndex'in temel bileşenlerinden biridir. Bağımsız modüller olarak kullanılabilecekleri gibi, diğer temel LlamaIndex modüllerine (indeksler, retriever'lar, sorgu motorları) de eklenebilirler. Her zaman yanıt sentezi (response synthesis) adımında (örneğin getirme/retrieval işleminden sonra) kullanılırlar. Kullanılan indeks türüne bağlı olarak, LLM'ler indeks oluşturma, ekleme ve sorgu tarama sırasında da kullanılabilir.

LlamaIndex; OpenAI, Hugging Face veya LangChain'den olsun, LLM arayüzünü kendiniz tanımlama zahmetine girmemeniz için LLM modüllerini tanımlamak üzere birleşik bir arayüz sağlar. Bu arayüz şunlardan oluşur (detaylar aşağıda):

-   **Metin tamamlama (text completion)** ve **sohbet (chat)** uç noktaları desteği.
-   **Akışlı (streaming)** ve **akışsız (non-streaming)** uç noktalar desteği.
-   **Senkron (synchronous)** ve **asenkron (asynchronous)** uç noktalar desteği.

## Kullanım Kalıbı (Usage Pattern)

Aşağıdaki kod parçası, LLM'leri kullanmaya nasıl başlayabileceğinizi gösterir.

Eğer henüz yüklü değilse, LLM paketini yükleyin:

```bash
pip install llama-index-llms-openai
```

Ardından:

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

# küresel varsayılanı değiştirme
Settings.llm = OpenAI()

# yerel kullanım
resp = OpenAI().complete("Paul Graham şöyledir: ")
print(resp)

# sorgu/sohbet motoru başına
query_engine = index.as_query_engine(..., llm=llm)
chat_engine = index.as_chat_engine(..., llm=llm)
```

[Bağımsız kullanım](/python/framework/module_guides/models/llms/usage_standalone) veya [özel kullanım](/python/framework/module_guides/models/llms/usage_custom) hakkında daha fazla detay bulabilirsiniz.

## Tokenleştirme (Tokenization) Üzerine Bir Not

LlamaIndex varsayılan olarak tüm token sayımları için küresel bir tokenizer (tokenleştirici) kullanır. Bu, varsayılan LLM olan `gpt-3.5-turbo` ile eşleşen tiktoken'dan `cl100k` dizesine varsayılan olarak ayarlanmıştır.

LLM'i değiştirirseniz, doğru token sayımı, parçalama (chunking) ve istemleme (prompting) sağlamak için bu tokenizer'ı güncellemeniz gerekebilir.

Bir tokenizer için tek gereksinim; bir dize alan ve bir liste döndüren, çağrılabilir (callable) bir fonksiyon olmasıdır.

Küresel bir tokenizer'ı şu şekilde ayarlayabilirsiniz:

```python
from llama_index.core import Settings

# tiktoken
import tiktoken

Settings.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo").encode

# huggingface
from transformers import AutoTokenizer

Settings.tokenizer = AutoTokenizer.from_pretrained(
    "HuggingFaceH4/zephyr-7b-beta"
)
```

## Modüller

OpenAI, HuggingFace, Anthropic ve daha fazlasıyla entegrasyonları destekliyoruz.

[Modüllerin tam listesine](/python/framework/module_guides/models/llms/modules) göz atın.

## Daha Fazla Okuma

-   [Embedding'ler](/python/framework/module_guides/models/embeddings)
-   [İstemler (Prompts)](/python/framework/module_guides/models/prompts)
-   [Yerel LLM'ler](/python/framework/module_guides/models/llms/local)
-   [Llama2'yi Yerel Olarak Çalıştırma](https://replicate.com/blog/run-llama-locally)