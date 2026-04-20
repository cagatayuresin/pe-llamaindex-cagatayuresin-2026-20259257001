# Konko

---
title: Konko
 | LlamaIndex OSS Belgeleri
---

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

> [Konko](https://www.konko.ai/) API, uygulama geliştiricilerine aşağıdakilerde yardımcı olmak için tasarlanmış tam yönetimli bir Web API'sidir:

Konko API, uygulama geliştiricilerine yardımcı olmak için tasarlanmış tam yönetimli bir API'dir:

1. Uygulamaları için doğru LLM'yi (veya LLM'leri) seçin
2. Çeşitli açık kaynaklı ve tescilli (proprietary) LLM'lerle prototip oluşturun
3. Endüstri lideri performansı maliyetinin küçük bir kısmına elde etmek için açık kaynaklı LLM'ler için İnce Ayar (Fine Tuning) imkanına erişin
4. Konko AI'nın SOC 2 uyumlu, çoklu bulut altyapısını kullanarak altyapı kurulumu veya yönetimi olmadan güvenlik, gizlilik, üretim miktarı ve gecikme SLA'larına uygun düşük maliyetli üretim API'leri kurun

### Modellere Erişim Adımları

1.  **Mevcut Modelleri Keşfedin:** Konko üzerindeki [mevcut modellere](https://docs.konko.ai/docs/list-of-models) göz atarak başlayın. Her model farklı kullanım durumlarına ve yeteneklere hitap eder.

2.  **Uygun Uç Noktaları (Endpoints) Belirleyin:** Seçtiğiniz modelin hangi [uç noktasını](https://docs.konko.ai/docs/list-of-models#list-of-available-models) (ChatCompletion veya Completion) desteklediğini belirleyin.

3.  **Model Seçimi:** Metadatalarına ve kullanım durumunuza ne kadar uygun olduğuna bağlı olarak bir [model seçin](https://docs.konko.ai/docs/list-of-models#list-of-available-models).

4.  **İstem (Prompting) Kılavuzları:** Bir model seçildikten sonra, onunla etkili bir şekilde iletişim kurmak için [istem kılavuzlarına](https://docs.konko.ai/docs/prompting) başvurun.

5.  **API'yi Kullanma:** Son olarak, modeli çağırmak ve yanıtları almak için uygun Konko [API uç noktasını](https://docs.konko.ai/docs/quickstart-for-completion-and-chat-completion-endpoint) kullanın.

Bu not defterini çalıştırmak için Konko API anahtarına ihtiyacınız olacak. [Konko](https://www.konko.ai/) üzerinden kaydolarak bir tane oluşturabilirsiniz.

Bu örnek, `Konko` ChatCompletion [modelleri](https://docs.konko.ai/docs/list-of-models#konko-hosted-models-for-chatcompletion) ve Completion [modelleri](https://docs.konko.ai/docs/list-of-models#konko-hosted-models-for-completion) ile etkileşim kurmak için LlamaIndex'in nasıl kullanılacağını gösterir.

```
%pip install llama-index-llms-konko
```

```
!pip install llama-index
```

## ChatMessage Listesi ile `chat` Çağrısı

`KONKO_API_KEY` ortam değişkenini (env var) ayarlamanız gerekir.

```python
import os


os.environ["KONKO_API_KEY"] = "<your-api-key>"
```

```python
from llama_index.llms.konko import Konko
from llama_index.core.llms import ChatMessage
```

```python
llm = Konko(model="meta-llama/llama-2-13b-chat")
messages = ChatMessage(role="user", content="Explain Big Bang Theory briefly")


resp = llm.chat([messages])
print(resp)
```

```
assistant:   The Big Bang Theory is the leading explanation for the origin and evolution of the universe, based on a vast body of observational and experimental evidence. Here's a brief summary of the theory:


1. The universe began as a single point: According to the Big Bang Theory, the universe began as an infinitely hot and dense point called a singularity around 13.8 billion years ago.
2. Expansion and cooling: The singularity expanded rapidly, and as it did, it cooled and particles began to form. This process is known as the "cosmic microwave background radiation" (CMB).
3. Formation of subatomic particles: As the universe expanded and cooled, protons, neutrons, and electrons began to form from the CMB. These particles eventually coalesced into the first atoms, primarily hydrogen and helium.
4. Nucleosynthesis: As the universe continued to expand and cool, more complex nuclei were formed through a process called nucleosynthesis. This process created heavier elements such as deuterium, helium-3, helium-4, and lithium.
5. The first stars and galaxies: As
```

## OpenAI Modelleri ile `chat` Çağrısı

`OPENAI_API_KEY` ortam değişkenini ayarlamanız gerekir.

```python
import os


os.environ["OPENAI_API_KEY"] = "<your-api-key>"


llm = Konko(model="gpt-3.5-turbo")
```

```python
message = ChatMessage(role="user", content="Explain Big Bang Theory briefly")
resp = llm.chat([message])
print(resp)
```

```
assistant: The Big Bang Theory is a scientific explanation for the origin and evolution of the universe. According to this theory, the universe began as a singularity, an extremely hot and dense point, approximately 13.8 billion years ago. It then rapidly expanded and continues to expand to this day. As the universe expanded, it cooled down, allowing matter and energy to form. Over time, galaxies, stars, and planets formed through gravitational attraction. The Big Bang Theory is supported by various pieces of evidence, such as the observed redshift of distant galaxies and the cosmic microwave background radiation.
```

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Tell me a story in 250 words")
resp = llm.stream_chat([message], max_tokens=1000)
for r in resp:
    print(r.delta, end="")
```

```
Once upon a time in a small village, there lived a young girl named Lily. She was known for her kind heart and love for animals. Every day, she would visit the nearby forest to feed the birds and rabbits.


One sunny morning, as Lily was walking through the forest, she stumbled upon a wounded bird with a broken wing. She carefully picked it up and decided to take it home. Lily named the bird Ruby and made a cozy nest for her in a small cage.


Days turned into weeks, and Ruby's wing slowly healed. Lily knew it was time to set her free. With a heavy heart, she opened the cage door, and Ruby hesitantly flew away. Lily watched as Ruby soared high into the sky, feeling a sense of joy and fulfillment.


As the years passed, Lily's love for animals grew stronger. She started rescuing and rehabilitating injured animals, creating a sanctuary in the heart of the village. People from far and wide would bring her injured creatures, knowing that Lily would care for them with love and compassion.


Word of Lily's sanctuary spread, and soon, volunteers came forward to help her. Together, they built enclosures, planted trees, and created a safe haven for all creatures big and small. Lily's sanctuary became a place of hope and healing, where animals found solace and humans learned the importance of coexistence.


Lily's dedication and selflessness inspired others to follow in her footsteps. The village transformed into a community that valued and protected its wildlife. Lily's dream of a harmonious world, where humans and animals lived in harmony, became a reality.


And so, the story of Lily and her sanctuary became a legend, passed down through generations. It taught people the power of compassion and the impact one person can have on the world. Lily's legacy lived on, reminding everyone that even the smallest act of kindness can create a ripple effect of change.
```

## İstem (Prompt) ile `complete` Çağrısı

```python
llm = Konko(model="numbersstation/nsql-llama-2-7b", max_tokens=100)
text = """CREATE TABLE stadium (
    stadium_id number,
    location text,
    name text,
    capacity number,
    highest number,
    lowest number,
    average number
)


CREATE TABLE singer (
    singer_id number,
    name text,
    country text,
    song_name text,
    song_release_year text,
    age number,
    is_male others
)


CREATE TABLE concert (
    concert_id number,
    concert_name text,
    theme text,
    stadium_id text,
    year text
)


CREATE TABLE singer_in_concert (
    concert_id number,
    singer_id text
)


-- Using valid SQLite, answer the following questions for the tables provided above.


-- What is the maximum capacity of stadiums ?


SELECT"""
response = llm.complete(text)
print(response)
```

```
 MAX(capacity) FROM stadiumm</s>
```

```python
llm = Konko(model="phind/phind-codellama-34b-v2", max_tokens=100)
text = """### System Prompt
You are an intelligent programming assistant.


### User Message
Implement a linked list in C++


### Assistant
..."""


resp = llm.stream_complete(text, max_tokens=1000)
for r in resp:
    print(r.delta, end="")
```

````cpp
```cpp
#include<iostream>
using namespace std;


// Node yapısı
struct Node {
    int data;
    Node* next;
};


// LinkedList sınıfı
class LinkedList {
    private:
        Node* head;
    public:
        LinkedList() : head(NULL) {}


        void addNode(int n) {
            Node* newNode = new Node;
            newNode->data = n;
            newNode->next = head;
            head = newNode;
        }


        void printList() {
            Node* cur = head;
            while(cur != NULL) {
                cout << cur->data << " -> ";
                cur = cur->next;
            }
            cout << "NULL" << endl;
        }
};


int main() {
    LinkedList list;
    list.addNode(1);
    list.addNode(2);
    list.addNode(3);
    list.printList();


    return 0;
}
```


Bu program, bir `Node` yapısı ve bir `LinkedList` sınıfı ile basit bir bağlı liste (linked list) oluşturur. `addNode` fonksiyonu listeye düğüm eklemek için, `printList` fonksiyonu ise listeyi yazdırmak için kullanılır. Main fonksiyonu bir `LinkedList` nesnesi oluşturur, bazı düğümler ekler ve ardından listeyi yazdırır.</s>
````

## Model Yapılandırması

```python
llm = Konko(model="meta-llama/llama-2-13b-chat")
```

```python
resp = llm.stream_complete(
    "Show me the c++ code to send requests to HTTP Server", max_tokens=1000
)
for r in resp:
    print(r.delta, end="")
```

````
  Elbette, bir HTTP sunucusuna C++ kullanarak nasıl istek gönderebileceğinize dair bir örnek:


Öncelikle, `iostream` ve `string` başlıklarını (headers) eklemeniz gerekecek:
```cpp
#include <iostream>
#include <string>
```
Ardından, HTTP isteğini içeren bir dize (string) oluşturmak için `std::string` sınıfını kullanmanız gerekecektir. Örneğin, sunucuya bir GET isteği göndermek için aşağıdaki kodu kullanabilirsiniz:
```cpp
std::string request = "GET /path/to/resource HTTP/1.1\r\n";
request += "Host: www.example.com\r\n";
request += "User-Agent: My C++ HTTP Client\r\n";
request += "Accept: */*\r\n";
request += "Connection: close\r\n\r\n";
```
Bu kod; istek yöntemini, URL'yi ve HTTP başlıklarını içeren GET isteğini barındıran bir dize oluşturur.


Ardından, `socket` fonksiyonunu kullanarak bir soket oluşturmanız gerekecektir:
```cpp
int sock = socket(AF_INET, SOCK_STREAM, 0);
```
Bu fonksiyon, ağ üzerinden veri göndermek ve almak için kullanılabilecek bir soket oluşturur.


Soketiniz olduğunda, sunucuya `send` fonksiyonunu kullanarak isteği gönderebilirsiniz:
```cpp
send(sock, request.c_str(), request.size(), 0);
```
Bu fonksiyon, soket üzerinden sunucuya isteği gönderir. `c_str` yöntemi, dizenin verilerine bir işaretçi döndürür ve bu işaretçi `send` fonksiyonuna iletilir. `size` yöntemi dizenin uzunluğunu döndürür ve bu da `send` fonksiyonuna iletilir.


Son olarak, sunucudan gelen yanıtı `recv` fonksiyonunu kullanarak okumanız gerekecektir:
```cpp
char buffer[1024];
int bytes_received = recv(sock, buffer, 1024, 0);
```
Bu fonksiyon sunucudan gelen verileri okur ve `buffer` dizisinde saklar. `bytes_received` değişkeni, alınan bayt sayısına ayarlanır.


İşte tamamlanmış kod:
```cpp
#include <iostream>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


int main() {
  // Bir soket oluştur
  int sock = socket(AF_INET, SOCK_STREAM, 0);


  // HTTP isteğini içeren bir dize oluştur
  std::string request = "GET /path/to/resource HTTP/1.1\r\n";
  request += "Host: www.example.com\r\n";
  request += "User-Agent: My C++ HTTP Client\r\n";
  request += "Accept: */*\r\n";
  request += "Connection: close\r\n\r\n";


  // İsteği sunucuya gönder
  send(sock, request.c_str(), request.size(), 0);


  // Sunucudan gelen yanıtı oku
  char buffer[1024];
  int bytes_received = recv(sock, buffer, 1024, 0);


  // Yanıtı yazdır
  std::cout << "Response: " << buffer << std::endl;


  // Soketi kapat
  close(sock);


  return 0;
}
```
Bu kod, sunucuya bir GET isteği gönderir, yanıtı okur ve konsola yazdırır. Bunun sadece basit bir örnek olduğunu ve gerçek dünya uygulamasında muhtemelen hataları ele almak ve soketi daha sağlam bir şekilde yönetmek isteyeceğinizi unutmayın.
````
