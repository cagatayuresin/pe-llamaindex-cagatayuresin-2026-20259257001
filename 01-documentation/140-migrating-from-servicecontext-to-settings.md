# ServiceContext'ten Settings'e Geçiş (Migrating from ServiceContext to Settings)

v0.10.0 sürümüyle birlikte tanıtılan yeni global `Settings` nesnesi, eski `ServiceContext` yapılandırmasının yerini almayı amaçlamaktadır.

Yeni `Settings` nesnesi, parametrelerin tembelce (lazily) başlatıldığı bir global ayarlar nesnesidir. LLM veya embedding modeli gibi nitelikler, sadece temel bir modül tarafından gerçekten ihtiyaç duyulduklarında yüklenirler.

Önceden `service_context` ile çeşitli modüller genellikle bunu kullanmıyordu ve ayrıca çalışma zamanında her bileşenin (o bileşenler kullanılmasa bile) belleğe yüklenmesini zorunlu kılıyordu.

Global ayarları yapılandırmak, LlamaIndex'teki HER modül için varsayılanı değiştirdiğiniz anlamına gelir. Bu, eğer OpenAI kullanmıyorsanız, örnek bir yapılandırmanın şu şekilde görünebileceği anlamına gelir:

```python
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.llm = Ollama(model="llama2", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

Şimdi bu ayarlarla, OpenAI'nin framework içinde asla kullanılmayacağından emin olabilirsiniz.

`Settings` nesnesi, eski `ServiceContext` ile hemen hemen aynı nitelikleri destekler. Tam bir listeyi [dökümanlar sayfasında](/python/framework/module_guides/supporting_modules/settings) bulabilirsiniz.

### Tam Geçiş (Complete Migration)

Aşağıda `ServiceContext`'ten `Settings`'e tamamen geçiş yapmaya dair bir örnek bulunmaktadır:

**Önce**

```python
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import ServiceContext, set_global_service_context

service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-3.5-turbo"),
    embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
    node_parser=SentenceSplitter(chunk_size=512, chunk_overlap=20),
    num_output=512,
    context_window=3900,
)
set_global_service_context(service_context)
```

**Sonra**

```python
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900
```

## Yerel Yapılandırma (Local Config)

Yukarıdakiler global yapılandırmayı kapsar. Ayarları modül bazında yapılandırmak için, tüm modül arayüzleri kullanılan nesneler için `kwargs` (keyword arguments) kabul edecek şekilde güncellenmiştir.

Eğer bir IDE kullanıyorsanız, `kwargs` otomatik olarak intellisense ile dolmalıdır; işte aşağıda bazı örnekler:

```python
# bir vektör deposu indeksi sadece bir embed modeline ihtiyaç duyar
index = VectorStoreIndex.from_documents(
    documents, embed_model=embed_model, transformations=transformations
)

# ... bir sorgu motoru (query engine) oluşturana kadar
query_engine = index.as_query_engine(llm=llm)
```

```python
# bir döküman özetleme indeksi (document summary index),
# kurucu metot için hem bir llm hem de bir embed modeline ihtiyaç duyar
index = DocumentSummaryIndex.from_documents(
    documents, embed_model=embed_model, llm=llm
)
```