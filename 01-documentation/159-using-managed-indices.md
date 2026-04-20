# Yönetilen İndeksleri (Managed Indices) Kullanma

LlamaIndex, Yönetilen İndekslerle (Managed Indices) birden fazla entegrasyon noktası sunar. Yönetilen bir indeks; LlamaIndex'in bir parçası olarak yerel olarak yönetilmeyen, bunun yerine [Vectara](https://vectara.com) gibi bir API aracılığıyla yönetilen özel bir indeks türüdür.

## Yönetilen Bir İndeks Kullanma

LlamaIndex içindeki diğer herhangi bir indeks (ağaç, anahtar kelime tablosu, liste) gibi, herhangi bir `ManagedIndex` de bir döküman koleksiyonuyla oluşturulabilir. Oluşturulduktan sonra, indeks sorgulama için kullanılabilir.

Eğer İndeks daha önce dökümanlarla doldurulmuşsa - doğrudan sorgulama için de kullanılabilir.

## Google Üretken Dil Semantik Erişicisi (Google Generative Language Semantic Retriever)

Google'ın Semantik Erişicisi (Semantic Retrieve) hem sorgulama hem de erişim (retrieval) yetenekleri sağlar. Yönetilen bir indeks oluşturun, dökümanları ekleyin ve LlamaIndex'in herhangi bir yerinde bir sorgu motoru veya erişici kullanın!

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.indices.managed.google import GoogleIndex

# Bir korpus (corpus) oluşturun
index = GoogleIndex.create_corpus(display_name="İlk korpusum!")
print(f"Yeni oluşturulan korpus ID'si: {index.corpus_id}.")

# Veri alımı (Ingestion)
documents = SimpleDirectoryReader("data").load_data()
index.insert_documents(documents)

# Sorgulama
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken ne yaptı?")

# Erişim (Retrieving)
retriever = index.as_retriever()
source_nodes = retriever.retrieve("Yazar büyürken ne yaptı?")
```

Tüm detaylar için [not defteri kılavuzuna](/python/examples/managed/googledemo) bakın.

## Vectara

İlk olarak, [kaydolun](https://vectara.com/integrations/llama_index) ve bir korpus (yani İndeks) oluşturmak için Vectara Konsolunu kullanın ve erişim için bir API anahtarı ekleyin.
API anahtarınızı aldıktan sonra, onu bir çevre değişkeni olarak dışa aktarın:

```python
import os

os.environ["VECTARA_API_KEY"] = "<VECTARA_API_ANAHTARINIZ>"
os.environ["VECTARA_CORPUS_KEY"] = "<VECTARA_CORPUS_ANAHTARINIZ>"
```

Ardından Vectara İndeksini oluşturun ve şu şekilde sorgulayın:

```python
from llama_index.core import ManagedIndex, SimpleDirectoryReader
from llama_index.indices.managed.vectara import VectaraIndex

# Dökümanları yükle ve indeksi oluştur
vectara_corpus_key = os.environ.get("VECTARA_CORPUS_KEY")
vectara_api_key = os.environ.get("VECTARA_API_KEY")

documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectaraIndex.from_documents(
    documents,
    vectara_corpus_key=vectara_corpus_key,
    vectara_api_key=vectara_api_key,
)
```

Notlar:

-   `VECTARA_CORPUS_KEY` ve `VECTARA_API_KEY` çevre değişkenleri zaten ortamda varsa, bunları çağrınızda açıkça belirtmeniz gerekmez ve VectaraIndex sınıfı bunları ortamdan okuyacaktır.
-   Birden fazla Vectara korpusuna bağlanmak için `VECTARA_CORPUS_KEY` değişkenini virgülle ayrılmış bir liste olarak ayarlayabilirsiniz; örneğin: `12,51` hem korpus `12`'ye hem de korpus `51`'e bağlanacaktır.

Korpusunuzda zaten dökümanlarınız varsa, `VectaraIndex`'i aşağıdaki gibi oluşturarak verilere doğrudan erişebilirsiniz:

```python
index = VectaraIndex()
```

VectaraIndex, yeni döküman yüklemeden mevcut korpusa bağlanacaktır.

İndeksi sorgulamak için aşağıdaki gibi bir sorgu motoru oluşturmanız yeterlidir:

```python
query_engine = index.as_query_engine(summary_enabled=True)
print(query_engine.query("Yazar büyürken ne yaptı?"))
```

Veya sohbet (chat) özelliğini kullanabilirsiniz:

```python
chat_engine = index.as_chat_engine()
print(chat_engine.chat("Yazar büyürken ne yaptı?").response)
```

Sohbet, beklediğiniz gibi çalışır ve sonraki `chat` çağrıları bir konuşma geçmişini korur. Tüm bunlar Vectara platformunda yapıldığından ek bir mantık eklemeniz gerekmez.

Daha fazla örnek için lütfen aşağıdakilere bakın:

-   [Vectara Demosu](/python/examples/managed/vectarademo)
-   [Vectara AutoRetriever](/python/examples/retrievers/vectara_auto_retriever)

## Vertex AI RAG (Vertex AI üzerinde LlamaIndex)

[RAG için Vertex AI üzerinde LlamaIndex](https://cloud.google.com/vertex-ai/generative-ai/docs/llamaindex-on-vertexai), Google Cloud Vertex AI üzerinde yönetilen bir RAG indeksidir.

İlk olarak, bir [Google Cloud projesi oluşturun ve Vertex AI API'sini etkinleştirin](https://cloud.google.com/vertex-ai/docs/start/cloud-environment). Ardından yönetilen bir indeks oluşturmak için aşağıdaki kodu çalıştırın.

```python
from llama_index.indices.managed.vertexai import VertexAIIndex

# TODO(geliştirici): Bu değerleri proje bilgilerinizle değiştirin
project_id = "PROJE_ID_NIZ"
location = "us-central1"

# İsteğe bağlı: Mevcut bir korpus kullanılıyorsa
corpus_id = "KORPUS_ID_NIZ"

# İsteğe bağlı: Yeni bir korpus oluşturuluyorsa
corpus_display_name = "korpus-adım"
corpus_description = "LlamaIndex için Vertex AI Korpusu"

# Bir korpus oluşturun veya mevcut bir korpus ID'si sağlayın
index = VertexAIIndex(
    project_id,
    location,
    corpus_display_name=corpus_display_name,
    corpus_description=corpus_description,
)
print(f"Yeni oluşturulan korpus adı: {index.corpus_name}.")

# Google Cloud Storage veya Google Drive'dan dosya aktarın
index.import_files(
    uris=["https://drive.google.com/file/123", "gs://kovam/dosya_dizinim"],
    chunk_size=512,  # İsteğe bağlı
    chunk_overlap=100,  # İsteğe bağlı
)

# Yerel dosya yükle
index.insert_file(
    file_path="dosyam.txt",
    metadata={"display_name": "dosyam.txt", "description": "Dosyam"},
)

# Sorgulama
query_engine = index.as_query_engine()
response = query_engine.query("RAG nedir ve neden yararlıdır?")

# Erişim (Retrieving)
retriever = index.as_retriever()
nodes = retriever.retrieve("RAG nedir ve neden yararlıdır?")
```

Tüm detaylar için [not defteri kılavuzuna](/python/examples/managed/vertexaidemo) bakın.