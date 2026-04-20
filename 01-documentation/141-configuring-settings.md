# Ayarları Yapılandırma (Configuring Settings)

`Settings`, bir LlamaIndex iş akışı/uygulaması içindeki indeksleme ve sorgulama aşamasında kullanılan, yaygın olarak kullanılan kaynakların bir paketidir.

Global yapılandırmayı ayarlamak için bunu kullanabilirsiniz. Yerel yapılandırmalar (transformatörler, LLM'ler, embedding modelleri); bunları kullanan arayüzlere doğrudan geçirilebilir.

`Settings`, uygulamanız boyunca yaşayan basit bir singleton nesnesidir. Belirli bir bileşen sağlanmadığında, `Settings` nesnesi onu global bir varsayılan olarak sağlamak için kullanılır.

`Settings` nesnesi üzerinde aşağıdaki nitelikler yapılandırılabilir:

## LLM

LLM; istemlere ve sorgulara yanıt vermek için kullanılır ve doğal dilde yanıtlar yazmaktan sorumludur.

```python
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
```

## Embedding Modeli (Embed Model)

Embedding modeli metni sayısal temsillere dönüştürmek için kullanılır; benzerlik hesaplama ve top-k erişim (retrieval) işlemlerinde kullanılır.

```python
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small", embed_batch_size=100
)
```

## Node Ayrıştırıcı / Metin Bölücü (Node Parser / Text Splitter)

Node ayrıştırıcı / metin bölücü, dökümanları node adı verilen daha küçük parçalara ayırmak için kullanılır.

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

Settings.text_splitter = SentenceSplitter(chunk_size=1024)
```

Eğer varsayılan bölücüyü değiştirmeden sadece parça boyutunu (chunk size) veya parça örtüşmesini (chunk overlap) değiştirmek isterseniz, bu da mümkündür:

```python
Settings.chunk_size = 512
Settings.chunk_overlap = 20
```

## Dönüşümler (Transformations)

Dönüşümler (transformations), veri alımı (ingestion) sırasında `Document`'lara uygulanır. Varsayılan olarak `node_parser`/`text_splitter` kullanılır, ancak bu geçersiz kılınabilir ve daha fazla özelleştirilebilir.

```python
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

Settings.transformations = [SentenceSplitter(chunk_size=1024)]
```

## Belirteç Oluşturucu (Tokenizer)

Tokenizer, belirteçleri (tokens) saymak için kullanılır. Bu, kullandığınız LLM ile eşleşen bir şeye ayarlanmalıdır.

```python
from llama_index.core import Settings

# openai
import tiktoken

Settings.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo").encode

# açık kaynak (open-source)
from transformers import AutoTokenizer

Settings.tokenizer = AutoTokenizer.from_pretrained(
    "mistralai/Mixtral-8x7B-Instruct-v0.1"
)
```

## Geri Çağırmalar (Callbacks)

Tüm LlamaIndex kodu boyunca oluşturulan olayları gözlemlemek ve tüketmek için kullanılabilecek global bir geri çağırma yöneticisi (callback manager) ayarlayabilirsiniz.

```python
from llama_index.core.callbacks import TokenCountingHandler, CallbackManager
from llama_index.core import Settings

token_counter = TokenCountingHandler()
Settings.callback_manager = CallbackManager([token_counter])
```

## İstem Yardımcısı Değişkenleri (Prompt Helper Arguments)

Sorgulama sırasında, LLM'ye giriş istemlerinin belirli sayıda belirteç oluşturmak için yeterli alana sahip olmasını sağlamak amacıyla birkaç özel argüman/değer kullanılır.

Genellikle bunlar LLM'deki nitelikler kullanılarak otomatik olarak yapılandırılır, ancak özel durumlarda geçersiz kılınabilirler.

```python
from llama_index.core import Settings

# LLM'ye maksimum giriş boyutu
Settings.context_window = 4096

# metin üretimi için ayrılan belirteç sayısı.
Settings.num_output = 256
```

<Aside type="tip">
  Belirli modüllerin nasıl yapılandırılacağını öğrenin: -
  [LLM](/python/framework/module_guides/models/llms/usage_custom) - [Embedding
  Modeli](/python/framework/module_guides/models/embeddings) - [Node Ayrıştırıcı/Metin
  Bölücüler](/python/framework/module_guides/loading/node_parsers) -
  [Geri Çağırmalar (Callbacks)](/python/framework/module_guides/observability/callbacks)
</Aside>

## Yerel yapılandırmaları ayarlama (Setting local configurations)

Ayarların (settings) belirli kısımlarını kullanan arayüzler, yerel geçersiz kılmaları (local overrides) da kabul edebilir.

```python
index = VectorStoreIndex.from_documents(
    documents, embed_model=embed_model, transformations=transformations
)

query_engine = index.as_query_engine(llm=llm)
```