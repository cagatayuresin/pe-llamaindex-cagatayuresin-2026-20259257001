# Kurulum ve Yapılandırma

LlamaIndex ekosistemi, ad alanlı (namespaced) Python paketlerinden oluşan bir koleksiyon kullanılarak yapılandırılmıştır.

Bunun kullanıcılar için anlamı şudur: `pip install llama-index` komutu, temel bir paket setiyle birlikte gelir ve ihtiyaç duyuldukça ek entegrasyonlar kurulabilir.

Paketlerin ve kullanılabilir entegrasyonların tam listesine [LlamaHub](https://llamahub.ai/) üzerinden ulaşılabilir.

## Pip ile Hızlı Başlangıç Kurulumu

Hızlıca başlamak için şu komutla kurulum yapabilirsiniz:

```bash
pip install llama-index
```

Bu, aşağıdaki paketleri içeren başlangıç paket setidir:

- `llama-index-core`
- `llama-index-llms-openai`
- `llama-index-embeddings-openai`
- `llama-index-readers-file`

**NOT:** `llama-index-core`, çalışma zamanında indirmeleri ve ağ çağrılarını önlemek için önceden paketlenmiş NLTK ve tiktoken dosyalarıyla birlikte gelir.

### Önemli: OpenAI Ortam Yapılandırması

Varsayılan olarak, metin üretimi için OpenAI `gpt-3.5-turbo` modelini, geri getirme (retrieval) ve gömmeler (embeddings) için ise `text-embedding-ada-002` modelini kullanıyoruz. Bunu kullanabilmek için bir ortam değişkeni olarak `OPENAI_API_KEY` tanımlanmış olmalıdır.
OpenAI hesabınıza giriş yaparak ve [yeni bir API anahtarı oluşturarak](https://platform.openai.com/account/api-keys) bir API anahtarı edinebilirsiniz.

> **İpucu:**
> Ayrıca [mevcut diğer birçok LLM'den birini de kullanabilirsiniz](/python/framework/module_guides/models/llms/usage_custom). LLM sağlayıcısına bağlı olarak ek ortam anahtarları ve belirteç (token) kurulumu yapmanız gerekebilir.

[OpenAI Başlangıç Örneğimize Göz Atın](/python/framework/getting_started/starter_example)

## Pip ile Özel Kurulum

OpenAI kullanmıyorsanız veya daha seçici bir kurulum istiyorsanız, bireysel paketleri ihtiyaca göre kurabilirsiniz.

Örneğin, Ollama ve HuggingFace gömmeleri ile yerel bir kurulum için kurulum şu şekilde görünebilir:

```bash
pip install llama-index-core llama-index-readers-file llama-index-llms-ollama llama-index-embeddings-huggingface
```

[Yerel Modellerle Başlangıç Örneğimize Göz Atın](/python/framework/getting_started/starter_example_local)

LLM'leri kullanma ve yapılandırma hakkındaki tam rehbere [buradan](/python/framework/module_guides/models/llms) ulaşabilirsiniz.

Gömme modellerini kullanma ve yapılandırma hakkındaki tam rehbere [buradan](/python/framework/module_guides/models/embeddings) ulaşabilirsiniz.

## Kaynaktan Kurulum

Bu depoyu klonlayın: `git clone https://github.com/run-llama/llama_index.git`. Ardından aşağıdakileri yapın:

- [Poetry'yi kurun](https://python-poetry.org/docs/#installation) - bu, paket bağımlılıklarını yönetmenize yardımcı olacaktır.
- Poetry kullanarak kabuk (shell) komutları çalıştırmanız gerekiyorsa ancak kabuk eklentisi kurulu değilse, şu komutu çalıştırarak eklentiyi ekleyin:
  ```bash
  poetry self add poetry-plugin-shell
  ```
- `poetry shell` - bu komut, kurulan paketlerin bu projeye özel kalmasını sağlayan sanal bir ortam oluşturur.
- `pip install -e llama-index-core` - bu, temel paketi kuracaktır.
- (İsteğe bağlı) `poetry install --with dev,docs` - bu, çoğu yerel geliştirme için gereken tüm bağımlılıkları kuracaktır.

Buradan itibaren, ihtiyaç duyduğunuz entegrasyonları `pip` ile kurabilirsiniz. Örneğin:

```bash
pip install -e llama-index-integrations/readers/llama-index-readers-file
pip install -e llama-index-integrations/llms/llama-index-llms-ollama
```