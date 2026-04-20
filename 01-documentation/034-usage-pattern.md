# Kullanım Kalıbı

## LLM ve Embedding Token Sayılarını Tahmin Etme

LLM ve Embedding token sayılarını ölçmek için şunları yapmanız gerekir:

1. `MockLLM` ve `MockEmbedding` nesnelerini kurun

```python
from llama_index.core.llms import MockLLM
from llama_index.core import MockEmbedding

llm = MockLLM(max_tokens=256)
embed_model = MockEmbedding(embed_dim=1536)
```

2. `TokenCountingCallback` işleyicisini kurun

```python
import tiktoken
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler

token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)

callback_manager = CallbackManager([token_counter])
```

3. Bunları global `Settings` nesnesine ekleyin

```python
from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model
Settings.callback_manager = callback_manager
```

4. Bir İndeks oluşturun

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader(
    "./docs/examples/data/paul_graham"
).load_data()

index = VectorStoreIndex.from_documents(documents)
```

5. Sayıları ölçün!

```python
print(
    "Embedding Tokenleri: ",
    token_counter.total_embedding_token_count,
    "\n",
    "LLM Komut (Prompt) Tokenleri: ",
    token_counter.prompt_llm_token_count,
    "\n",
    "LLM Tamamlama (Completion) Tokenleri: ",
    token_counter.completion_llm_token_count,
    "\n",
    "Toplam LLM Token Sayısı: ",
    token_counter.total_llm_token_count,
    "\n",
)

# sayıları sıfırla
token_counter.reset_counts()
```

6. Bir sorgu çalıştırın ve tekrar ölçün

```python
query_engine = index.as_query_engine()

response = query_engine.query("sorgu")

print(
    "Embedding Tokenleri: ",
    token_counter.total_embedding_token_count,
    "\n",
    "LLM Komut (Prompt) Tokenleri: ",
    token_counter.prompt_llm_token_count,
    "\n",
    "LLM Tamamlama (Completion) Tokenleri: ",
    token_counter.completion_llm_token_count,
    "\n",
    "Toplam LLM Token Sayısı: ",
    token_counter.total_llm_token_count,
    "\n",
)
```