# Anyscale

Eğer bu Not Defterini colab üzerinden açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-anyscale
```

```python
!pip install llama-index
```

```python
from llama_index.llms.anyscale import Anyscale
from llama_index.core.llms import ChatMessage
```

## ChatMessage Listesi ile `chat` Çağrısı
`ANYSCALE_API_KEY` ortam değişkenini ayarlamanız veya sınıf yapıcıda (constructor) api_key değerini belirtmeniz gerekir.

```python
# import os
# os.environ['ANYSCALE_API_KEY'] = '<api-anahtarınız>'

llm = Anyscale(api_key="<api-anahtarınız>")
```

```python
message = ChatMessage(role="user", content="Bana bir fıkra anlat")
resp = llm.chat([message])
print(resp)
```

    assistant: Tabii, işte bir fıkra:
    
    Bisiklet neden kendi başına ayakta duramazmış?
    
    Çünkü çok *yorgunmuş* (iki tekerlekli/tired)!
    
    Umarım yüzünüze bir gülümseme getirebilmişimdir! Size yardımcı olabileceğim başka bir konu var mı?

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Bana 250 kelimelik bir hikaye anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

    Bir zamanlar, gür yeşil ormanlarla çevrili küçük bir köyde yaşayan Maria adında genç bir kız vardı. Maria, köydeki herkes tarafından sevilen, nazik ve kibar bir ruhtu. Günlerinin çoğunu ormanları keşfederek, yeni bitki ve hayvan türleri keşfederek ve köylülere günlük işlerinde yardım ederek geçirirdi.
    
    Bir gün Maria yürüyüşe çıkmışken, daha önce hiç görmediği gizli bir yola rastladı. Yol yabani otlar ve asmalarla kaplıydı ama içinden bir ses onu oraya çağırdı. Takip etmeye karar verdi ve yol onu ormanın derinliklerine, gittikçe daha derinlerine götürdü.
    
    Yürüdükçe ağaçlar uzadı ve hava soğudu. Maria bir huzursuzluk hissetmeye başladı ama yolun nereye vardığını görmeye kararlıydı. Sonunda bir açıklığa geldi ve merkezinde gövdesi bir ev kadar geniş, devasa bir ağaç duruyordu.
    
    Maria ağaca yaklaştı ve ağacın garip sembollerle kaplı olduğunu gördü. Sembollerden birine dokunmak için elini uzattı ve aniden ağaç parlamaya başladı. Parlaklık gittikçe güçlendi, ta ki Maria...

## İstem (Prompt) ile `complete` Çağrısı

```python
resp = llm.complete("Bana bir fıkra anlat")
print(resp)
```

    Tabii, işte bir fıkra:
    
    Bisiklet neden kendi başına ayakta duramazmış?
    
    Çünkü çok *yorgunmuş* (iki tekerlekli/tired)!
    
    Umarım yüzünüze bir gülümseme getirebilmiştir!

```python
resp = llm.stream_complete("Bana 250 kelimelik bir hikaye anlat")
for r in resp:
    print(r.delta, end="")
```

    Bir zamanlar Maria adında genç bir kız vardı. Gür yeşil ormanlar ve pırıl pırıl nehirlerle çevrili küçük bir köyde yaşıyordu. Maria, köydeki herkes tarafından sevilen, nazik ve kibar bir ruhtu. Günlerini ailesine çiftlik işlerinde yardım ederek ve çevredeki doğayı keşfederek geçirirdi.
    
    Bir gün ormanda dolaşırken Maria, daha önce hiç görmediği gizli bir yola rastladı. Takip etmeye karar verdi ve yol onu yabani çiçeklerle dolu güzel bir çayıra götürdü. Çayırın ortasında küçük bir gölet buldu; orada sudaki kendi yansımasını gördü.
    
    Gölete bakarken Maria, kendisine doğru bir figürün yaklaştığını gördü. Bu, kendisini çayırın koruyucusu olarak tanıtan bilge, yaşlı bir kadındı. Yaşlı kadın Maria'ya, kendisine büyük bir neşe ve mutluluk getirecek özel bir hediye alması için seçildiğini söyledi.
    
    Yaşlı kadın daha sonra Maria'ya küçük, narin bir çiçek sundu. Bu çiçeğin hem fiziksel hem de duygusal her türlü yarayı iyileştirme gücüne sahip olduğunu söyledi. Maria hayran kaldı ve minnettar oldu; çiçeği akıllıca kullanacağına söz verdi.

## Model Yapılandırması

```python
llm = Anyscale(model="codellama/CodeLlama-34b-Instruct-hf")
```

```python
resp = llm.complete("Bana bir HTTP Sunucusuna istek göndermek için gereken C++ kodunu göster")
print(resp)
```

    C++'da bir HTTP sunucusuna istek göndermek için `curl` kütüphanesini kullanabilirsiniz. İşte bunun nasıl kullanılacağına dair bir örnek:
    ```cpp
    #include <curl/curl.h>
    
    int main() {
        CURL *curl;
        CURLcode res;
        curl = curl_easy_init();
        if (curl) {
            curl_easy_setopt(curl, CURLOPT_URL, "http://example.com");
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=John&age=25");
            res = curl_easy_perform(curl);
            if (res != CURLE_OK) {
                fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            }
            curl_easy_cleanup(curl);
        }
        return 0;
    }
    ```
    Bu kod `curl` kütüphanesini başlatır, URL ve POST alanlarını ayarlar, isteği gerçekleştirir ve kaynakları temizler.
    
    Ayrıca `libcurl` kütüphanesini de kullanabilirsiniz.
