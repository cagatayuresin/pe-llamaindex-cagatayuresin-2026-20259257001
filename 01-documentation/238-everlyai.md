# EverlyAI

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-everlyai
```

```python
!pip install llama-index
```

```python
from llama_index.llms.everlyai import EverlyAI
from llama_index.core.llms import ChatMessage
```

## ChatMessage Listesi ile `chat` Çağrısı Yapın
`EVERLYAI_API_KEY` ortam değişkenini ayarlamanız veya sınıf yapıcısında (constructor) api_key'i belirtmeniz gerekir.

```python
# import os
# os.environ['EVERLYAI_API_KEY'] = '<api-anahtarınız>'

llm = EverlyAI(api_key="api-anahtarınız")
```

```python
message = ChatMessage(role="user", content="Bana bir şaka anlat")
resp = llm.chat([message])
print(resp)
```

    assistant:  Tabii! İşte klasik bir tane:
    
    Bilim insanları neden atomlara güvenmezler?
    
    Çünkü her şeyi onlar uyduruyorlar! (Because they make up everything!)
    
    Umarım bu yüzünde bir gülümseme oluşturmuştur!

### Akış (Streaming)

```python
message = ChatMessage(role="user", content="Bana 250 kelimelik bir hikaye anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

     Tabii, işte 250 kelimelik bir hikaye:
    
    Güneş ufukta batarken, Lily adında genç bir kız kumsalda oturmuş, dalgaların kıyıya vuruşunu izliyordu. Okyanusu her zaman sevmişti ve bugün de farklı değildi. Su derin bir mavi, neredeyse mordu ve dalgalar nazik ve yatıştırıcıydı. Lily gözlerini kapattı ve dalgaların sesinin kendisini sarmasına izin verdi, günlük hayatın stresinin eriyip gittiğini hissetti.
    Aniden, yakına bir martı kondu, ötüyor ve kanat çırpıyordu. Lily gözlerini açtı ve kuşun gagasında bir şey tuttuğunu gördü. Merakla öne eğildi ve kuşun küçük, parıldayan bir kabuk taşıdığını gördü. Kuş kabuğu Lily'nin ayaklarının dibine bıraktı ve Lily onu eline aldı, pürüzsüz yüzeyini hissetti ve güzelliğine hayran kaldı.
    Kabuğu tutarken, Lily garip bir hissin kendisini sardığını hissetti. Okyanusa ve kuşa bağlı olduğunu hissetti ve bu anın özel olduğunu biliyordu. Suya doğru baktı ve uzakta yüzen bir balık sürüsü gördü, pulları güneşin altında parlıyordu.

## İstemle (Prompt) `complete` Çağrısı Yapın

```python
resp = llm.complete("Bana bir şaka anlat")
print(resp)
```

     Tabii, işte klasik bir tane:
    
    Bilim insanları neden atomlara güvenmezler?
    
    Çünkü her şeyi onlar uyduruyorlar! (Because they make up everything!)
    
    Umarım bu yüzünde bir gülümseme oluşturmuştur!

```python
resp = llm.stream_complete("Bana 250 kelimelik bir hikaye anlat")
for r in resp:
    print(r.delta, end="")
```

     Tabii, işte 250 kelimelik bir hikaye:
    
    Güneş ufukta batarken, Maria adında genç bir kız kumsalda oturmuş, dalgaların kıyıya vuruşunu izliyordu. Okyanusu her zaman sevmişti ve bugün de farklı değildi. Su derin bir mavi, neredeyse mordu ve dalgalar nazik ve yatıştırıcıydı.
    Maria gözlerini kapattı ve dalgaların sesinin kendisini sarmasına izin verdi. Ayaklarının altındaki kumun sıcaklığını ve yumuşaklığını hissedebiliyordu. Kendinden daha büyük bir şeyin parçasıymış gibi huzurlu hissediyordu.
    Aniden, yakına bir martı kondu, ötüyor ve kanat çırpıyordu. Maria gözlerini açtı ve kuşu gördü, yüzünde bir gülümsemenin yayıldığını hissetti. Martıların sesini ve tam olarak ne zaman ortaya çıkacaklarını biliyor gibi görünmelerini seviyordu.
    Güneş gökyüzünde daha da alçalırken, Maria ayağa kalktı ve suya yaklaştı. Serin suyun ayaklarının üzerinden geçişini hissetti ve memnuniyet dolu bir iç çekti. Burası onun mutlu olduğu yerdi; günlük hayatın stresinden kaçabildiği ve sadece olduğu yer.
    Maria bir süre orada kaldı.
