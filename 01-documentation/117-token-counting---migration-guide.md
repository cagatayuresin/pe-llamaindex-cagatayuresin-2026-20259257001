# Token Sayımı - Migrasyon Kılavuzu (Token Counting - Migration Guide)

Mevcut token sayımı uygulaması **kullanımdan kaldırılmıştır (deprecated)**.

Token sayımının birçok kullanıcı için önemli olduğunu biliyoruz, bu nedenle bu kılavuz (umarız sancısız bir) geçiş sürecinde size yol göstermek için oluşturulmuştur.

Önceden, token sayımı doğrudan `llm_predictor` ve `embed_model` nesneleri üzerinden takip ediliyordu ve isteğe bağlı olarak konsola yazdırılıyordu. Bu uygulama, token sayımı için statik bir tokenizer (gpt-2) kullanıyordu ve `last_token_usage` ile `total_token_usage` nitelikleri her zaman doğru şekilde takip edilmiyordu.

Bundan böyle token sayımı bir geri arama (callback) yapısına taşınmıştır. `TokenCountingHandler` geri aramasını kullanarak artık tokenların nasıl sayılacağı, token sayımlarının ömrü ve hatta farklı indeksler için ayrı token sayaçları oluşturma konusunda daha fazla seçeneğe sahipsiniz.

İşte bir OpenAI modeli ile yeni `TokenCountingHandler` kullanımına dair asgari bir örnek:

```python
import tiktoken
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.core import Settings

# doğrudan bir tokenizer ayarlayabilir veya isteğe bağlı olarak varsayılan 
# bir tokenizer (daha önce token sayımı için kullanılanla aynı) kullanılmasına izin verebilirsiniz
# NOT: Tokenizer, metin alan ve tokenlardan oluşan bir liste döndüren bir fonksiyon olmalıdır
token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode,
    verbose=False,  # kullanımı konsolda görmek için True olarak ayarlayın
)

Settings.callback_manager = CallbackManager([token_counter])

document = SimpleDirectoryReader("./data").load_data()

# Eğer verbose açıksa, embedding token kullanımının yazdırıldığını göreceksiniz
index = VectorStoreIndex.from_documents(
    documents,
)

# Aksi takdirde, sayıma doğrudan erişebilirsiniz
print(token_counter.total_embedding_token_count)

# Sayımları tamamen kendi takdirinize bağlı olarak sıfırlayın!
token_counter.reset_counts()

# Embedding'lere ek olarak istem (prompt), tamamlama (completion) ve toplam LLM tokenlarını da takip edin
response = index.as_query_engine().query("Yazar büyürken ne yaptı?")
print(
    "Embedding Tokenları: ",
    token_counter.total_embedding_token_count,
    "\n",
    "LLM İstem Tokenları: ",
    token_counter.prompt_llm_token_count,
    "\n",
    "LLM Tamamlama Tokenları: ",
    token_counter.completion_llm_token_count,
    "\n",
    "Toplam LLM Token Sayısı: ",
    token_counter.total_llm_token_count,
)
```