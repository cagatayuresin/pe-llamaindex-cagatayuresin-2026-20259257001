# Sohbet Depoları (Chat Stores)

Bir sohbet deposu (chat store), sohbet geçmişinizi saklamak için merkezi bir arayüz görevi görür. Sohbet geçmişi, diğer saklama formatlarına kıyasla benzersizdir; çünkü mesajların sırası genel bir konuşmayı sürdürmek için önemlidir.

Sohbet depoları, mesaj dizilerini anahtarlara (`user_id`'ler veya diğer benzersiz tanımlayıcı dizeler gibi) göre düzenleyebilir ve `delete` (sil), `insert` (ekle) ve `get` (getir) işlemlerini gerçekleştirebilir.

## SimpleChatStore

En temel sohbet deposu, mesajları bellekte saklayan ve diskten kaydedip yükleyebilen veya serileştirilip başka bir yerde saklanabilen `SimpleChatStore`'dur.

Tipik olarak, bir sohbet deposunu başlatır ve onu bir bellek (memory) modülüne verirsiniz. Sohbet deposu kullanan bellek modülleri, eğer bir depo sağlanmazsa varsayılan olarak `SimpleChatStore` kullanacaktır.

```python
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer

chat_store = SimpleChatStore()

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
```

Belleği oluşturduktan sonra, onu bir ajana (agent) veya sohbet motoruna dahil edebilirsiniz:

```python
agent = FunctionAgent(tools=tools, llm=llm)
await agent.run("...", memory=memory)
# VEYA
chat_engine = index.as_chat_engine(memory=memory)
```

Sohbet deposunu daha sonra kullanmak üzere kaydedebilir veya diskten yükleyebilirsiniz:

```python
chat_store.persist(persist_path="chat_store.json")
loaded_chat_store = SimpleChatStore.from_persist_path(
    persist_path="chat_store.json"
)
```

Veya bir dizeye (string) dönüştürüp, bu dizeyi başka bir yere kaydedebilirsiniz:

```python
chat_store_string = chat_store.json()
loaded_chat_store = SimpleChatStore.parse_raw(chat_store_string)
```

## UpstashChatStore

`UpstashChatStore` kullanarak, sohbet geçmişinizi sunucusuz (serverless) bir Redis çözümü olan Upstash Redis kullanarak uzaktan saklayabilirsiniz. Bu, ölçeklenebilir ve verimli sohbet saklama gerektiren uygulamalar için idealdir. Bu sohbet deposu hem senkron hem de asenkron işlemleri destekler.

### Kurulum

```bash
pip install llama-index-storage-chat-store-upstash
```

### Kullanım

```python
from llama_index.storage.chat_store.upstash import UpstashChatStore
from llama_index.core.memory import ChatMemoryBuffer

chat_store = UpstashChatStore(
    redis_url="UPSTASH_REDIS_URL_ADRESINIZ",
    redis_token="UPSTASH_REDIS_TOKEN_BILGINIZ",
    ttl=300,  # İsteğe bağlı: Saniye cinsinden yaşam süresi (time to live)
)

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
```

UpstashChatStore hem senkron hem de asenkron işlemleri destekler. İşte asenkron yöntemleri kullanmaya dair bir örnek:

```python
import asyncio
from llama_index.core.llms import ChatMessage


async def main():
    # Mesaj ekle
    messages = [
        ChatMessage(content="Merhaba", role="user"),
        ChatMessage(content="Selam!", role="assistant"),
    ]
    await chat_store.async_set_messages("konusma1", messages)

    # Mesajları getir
    retrieved_messages = await chat_store.async_get_messages("konusma1")
    print(retrieved_messages)

    # Son mesajı sil
    deleted_message = await chat_store.async_delete_last_message(
        "konusma1"
    )
    print(f"Silinen mesaj: {deleted_message}")


asyncio.run(main())
```

## RedisChatStore

`RedisChatStore` kullanarak sohbet geçmişinizi uzakta saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

```python
from llama_index.storage.chat_store.redis import RedisChatStore
from llama_index.core.memory import ChatMemoryBuffer

chat_store = RedisChatStore(redis_url="redis://localhost:6379", ttl=300)

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
```

## AzureChatStore

`AzureChatStore` kullanarak sohbet geçmişinizi Azure Table Storage veya CosmosDB'de uzaktan saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

```bash
pip install llama-index
pip install llama-index-llms-azure-openai
pip install llama-index-storage-chat-store-azure
```

```python
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.azure import AzureChatStore

chat_store = AzureChatStore.from_account_and_key(
    account_name="",
    account_key="",
    chat_table_name="ChatUser",
)

memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="conversation1",
)

chat_engine = SimpleChatEngine(
    memory=memory, llm=Settings.llm, prefix_messages=[]
)

response = chat_engine.chat("Merhaba.")
```

## DynamoDBChatStore

`DynamoDBChatStore` kullanarak sohbet geçmişinizi AWS DynamoDB'de saklayabilirsiniz.

### Kurulum

```bash
pip install llama-index-storage-chat-store-dynamodb
```

### Kullanım

Uygun şema ile oluşturulmuş bir DynamoDB tablonuz olduğundan emin olun. Varsayılan olarak işte bir örnek:

```python
import boto3

# Hizmet kaynağını al
dynamodb = boto3.resource("dynamodb")

# DynamoDB tablosunu oluştur
table = dynamodb.create_table(
    TableName="ORNEK_TABLO",
    KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],
    AttributeDefinitions=[
        {"AttributeName": "SessionId", "AttributeType": "S"}
    ],
    BillingMode="PAY_PER_REQUEST",
)
```

Ardından, sohbet geçmişlerini kalıcı hale getirmek ve getirmek için `DynamoDBChatStore` sınıfını kullanabilirsiniz:

```python
import os
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.storage.chat_store.dynamodb.base import DynamoDBChatStore

# DynamoDB sohbet deposunu başlat
chat_store = DynamoDBChatStore(
    table_name="ORNEK_TABLO", profile_name=os.getenv("AWS_PROFILE")
)

# Henüz mevcut olmayan bir sohbet geçmişi boş bir dizi döndürür.
print(chat_store.get_messages("123"))
# >>> []

# "SessionID = 123" anahtarı ile bir sohbet geçmişi başlatma
messages = [
    ChatMessage(role=MessageRole.USER, content="Sen kimsin?"),
    ChatMessage(
        role=MessageRole.ASSISTANT, content="Ben senin yardımcı AI asistanınım."
    ),
]
chat_store.set_messages(key="123", messages=messages)
print(chat_store.get_messages("123"))
# >>> [ChatMessage(role=<MessageRole.USER: 'user'>, content='Sen kimsin?', additional_kwargs={}),
#      ChatMessage(role=<MessageRole.ASSISTANT: 'assistant'>, content='Ben senin yardımcı AI asistanınım.', additional_kwargs={})]]

# Mevcut bir sohbet geçmişine mesaj ekleme
message = ChatMessage(role=MessageRole.USER, content="Neler yapabilirsin?")
chat_store.add_message(key="123", message=message)
print(chat_store.get_messages("123"))
# >>> [ChatMessage(role=<MessageRole.USER: 'user'>, content='Sen kimsin?', additional_kwargs={}),
#      ChatMessage(role=<MessageRole.ASSISTANT: 'assistant'>, content='Ben senin yardımcı AI asistanınım.', additional_kwargs={})],
#      ChatMessage(role=<MessageRole.USER: 'user'>, content='Neler yapabilirsin?', additional_kwargs={})]
```

## PostgresChatStore

`PostgresChatStore` kullanarak sohbet geçmişinizi uzakta saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

```python
from llama_index.storage.chat_store.postgres import PostgresChatStore
from llama_index.core.memory import ChatMemoryBuffer

chat_store = PostgresChatStore.from_uri(
    uri="postgresql+asyncpg://postgres:parola@127.0.0.1:5432/veritabani",
)

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
```

## TablestoreChatStore

`TablestoreChatStore` kullanarak sohbet geçmişinizi uzakta saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

#### Kurulum

```bash
pip install llama-index-storage-chat-store-tablestore
```

#### Kullanım

```python
from llama_index.storage.chat_store.tablestore import TablestoreChatStore
from llama_index.core.memory import ChatMemoryBuffer

# 1. tablestore vektör deposu oluştur
chat_store = TablestoreChatStore(
    endpoint="<uc_nokta>",
    instance_name="<ornek_adi>",
    access_key_id="<erisim_anahtari_id>",
    access_key_secret="<erisim_anahtari_sirri>",
)
# İlk kullanım için bir tablo oluşturmanız gerekir
chat_store.create_table_if_not_exist()

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
```

## Google AlloyDB Sohbet Deposu (ChatStore)

`AlloyDBChatStore` kullanarak sohbet geçmişinizi AlloyDB'de saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

Bu kılavuz senkron arayüzü göstermektedir. Tüm senkron yöntemlerin ilgili asenkron yöntemleri mevcuttur.

#### Kurulum

```bash
pip install llama-index
pip install llama-index-alloydb-pg
pip install llama-index-llms-vertex
```

#### Kullanım

```python
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index_alloydb_pg import AlloyDBChatStore, AlloyDBEngine
from llama_index.llms.vertex import Vertex
import asyncio

# Kendi AlloyDB bilgilerinizle değiştirin
engine = AlloyDBEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    cluster=CLUSTER,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)

engine.init_chat_store_table(table_name=TABLE_NAME)

chat_store = AlloyDBChatStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)

memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)

llm = Vertex(model="gemini-1.5-flash-002", project=PROJECT_ID)

chat_engine = SimpleChatEngine(memory=memory, llm=llm, prefix_messages=[])

response = chat_engine.chat("Merhaba.")

print(response)
```

## Google Cloud SQL for PostgreSQL Sohbet Deposu (ChatStore)

`PostgresChatStore` kullanarak sohbet geçmişinizi Cloud SQL for Postgres'te saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

Bu kılavuz senkron arayüzü göstermektedir. Tüm senkron yöntemlerin ilgili asenkron yöntemleri mevcuttur.

#### Kurulum

```bash
pip install llama-index
pip install llama-index-cloud-sql-pg
pip install llama-index-llms-vertex
```

#### Kullanım

```python
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index_cloud_sql_pg import PostgresChatStore, PostgresEngine
from llama_index.llms.vertex import Vertex
import asyncio

# Kendi Cloud SQL bilgilerinizle değiştirin
engine = PostgresEngine.from_instance(
    project_id=PROJECT_ID,
    region=REGION,
    instance=INSTANCE,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
)

engine.init_chat_store_table(table_name=TABLE_NAME)

chat_store = PostgresChatStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
)

memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)

llm = Vertex(model="gemini-1.5-flash-002", project=PROJECT_ID)

chat_engine = SimpleChatEngine(memory=memory, llm=llm, prefix_messages=[])

response = chat_engine.chat("Merhaba.")

print(response)
```

## YugabyteDBChatStore

`YugabyteDBChatStore` kullanarak sohbet geçmişinizi uzakta saklayabilir; sohbet geçmişini manuel olarak kaydetme ve yükleme konusunda endişelenmenize gerek kalmaz.

### Ön Koşullar

Bu entegrasyonu kullanmadan önce, çalışan bir YugabyteDB örneğine ihtiyacınız olacaktır. [YugaByteDB Hızlı Başlangıç Kılavuzu](https://docs.yugabyte.com/preview/quick-start/macos/)'nu takip ederek yerel bir YugabyteDB örneği kurabilirsiniz.

### Kurulum

```shell
pip install llama-index-storage-chat-store-yugabytedb
```

### Kullanım

```python
from llama_index.storage.chat_store.yugabytedb import YugabyteDBChatStore
from llama_index.core.memory import ChatMemoryBuffer

chat_store = YugabyteDBChatStore.from_uri(
    uri="yugabytedb+psycopg2://yugabyte:parola@127.0.0.1:5433/yugabyte?load_balance=true",
)

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
```

#### Bağlantı Dizesi Parametreleri

`YugabyteDBChatStore.from_uri()` fonksiyonuna geçirilen bağlantı dizesi, YugabyteDB kümenize olan bağlantıyı yapılandırmak için kullanılabilecek çeşitli parametreleri destekler.
Desteklenen parametrelerin tam listesini [YugabyteDB psycopg2 Driver Dökümantasyonu](https://docs.yugabyte.com/preview/drivers-orms/python/yugabyte-psycopg2/#step-2-set-up-the-database-connection) içerisinde bulabilirsiniz.

YugabyteDB'ye özel parametreler şunları içerir:

-   `load_balance`: Yük dengelemeyi etkinleştir/devre dışı bırak (varsayılan: false)
-   `topology_keys`: Bağlantı yönlendirmesi için tercih edilen node'ları belirtin
-   `yb_servers_refresh_interval`: Kullanılabilir sunucu listesini yenileme aralığı (saniye cinsinden)
-   `fallback_to_topology_keys_only`: Sadece topology_keys içinde belirtilen node'lara bağlanılıp bağlanılmayacağı
-   `failed_host_ttl_seconds`: Başarısız olan node'lara bağlanmayı tekrar denemeden önce bekleme süresi (saniye cinsinden)