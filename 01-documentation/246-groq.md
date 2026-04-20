# Groq

Groq'a hoş geldiniz! 🚀 Groq'ta, dünyanın ilk Dil İşleme Ünitesi™'ni (Language Processing Unit™) veya kısaca LPU'yu geliştirdik. Groq LPU, herhangi bir iş yükü için öngörülebilir ve tekrarlanabilir performansla GenAI çıkarım hızı standardını belirleyen, deterministik, tek çekirdekli bir akış mimarisine sahiptir.

Mimarinin ötesinde yazılımımız, yenilikçi ve güçlü AI uygulamaları oluşturmanız için ihtiyacınız olan araçlarla sizin gibi geliştiricileri güçlendirmek üzere tasarlanmıştır. Motorunuz olarak Groq ile şunları yapabilirsiniz:

* Gerçek zamanlı AI ve HPC çıkarımları için tavizsiz düşük gecikme ve performans elde edin 🔥
* Herhangi bir iş yükü için tam performansı ve hesaplama süresini bilin 🔮
* Rekabetin önünde kalmak için en son teknolojimizden yararlanın 💪

Daha fazla Groq ister misiniz? Daha fazla kaynak için [web sitemize](https://groq.com) göz atın ve geliştiricilerimizle bağlantı kurmak için [Discord topluluğumuza](https://discord.gg/JvNsBDKeCG) katılın!

## Kurulum

Eğer bu Notebook'u Colab üzerinde açıyorsanız, muhtemelen LlamaIndex 🦙 kurmanız gerekecektir.

```python
% pip install llama-index-llms-groq
```

```python
!pip install llama-index
```

```python
from llama_index.llms.groq import Groq
```

    PyTorch, TensorFlow >= 2.0 veya Flax bulunamadı. Modeller mevcut olmayacak ve sadece tokenizer'lar, yapılandırma ve dosya/veri yardımcı programları kullanılabilecektir.

[Groq konsolu](https://console.groq.com/keys) üzerinden bir API anahtarı oluşturun, ardından bunu `GROQ_API_KEY` ortam değişkenine atayın.

```bash
export GROQ_API_KEY=<api anahtarınız>
```

Alternatif olarak, başlatırken API anahtarınızı LLM'e iletebilirsiniz:

```python
llm = Groq(model="llama3-70b-8192", api_key="api_anahtarınız")
```

Mevcut LLM modellerinin listesini [burada](https://console.groq.com/docs/models) bulabilirsiniz.

```python
response = llm.complete("Düşük gecikmeli LLM'lerin önemini açıkla")
```

```python
print(response)
```

    Düşük gecikmeli Büyük Dil Modelleri (LLM'ler), girdileri hızlı bir şekilde işleme ve yanıtlama yetenekleri nedeniyle belirli uygulamalarda önemlidir. Gecikme (latency), bir kullanıcının isteği ile sistemin yanıtı arasındaki zaman gecikmesini ifade eder. Bazı gerçek zamanlı veya zamana duyarlı uygulamalarda, sorunsuz bir kullanıcı deneyimi sağlamak ve gecikmeleri veya takılmaları önlemek için düşük gecikme kritiktir.
    
    Örneğin, diyaloğa dayalı ajanlarda veya chatbot'larda, kullanıcılar hızlı ve duyarlı etkileşimler bekler. Sistem kullanıcı girdilerini işlemek ve yanıtlamak için çok uzun sürerse, bu durum kullanıcı deneyimini olumsuz etkileyebilir ve hüsrana yol açabilir. Benzer şekilde, gerçek zamanlı dil çevirisi veya konuşma tanıma gibi uygulamalarda, kullanıcıya doğru ve zamanında geri bildirim sağlamak için düşük gecikme esastır.
    
    Dahası, düşük gecikmeli LLM'ler, dil girdilerinin gerçek zamanlı veya gerçek zamanlıya yakın işlenmesini gerektiren yeni kullanım durumları ve uygulamalar sağlayabilir. Örneğin, otonom araçlar alanında, düşük gecikmeli LLM'ler gerçek zamanlı konuşma tanıma ve doğal dil anlama için kullanılabilir; bu da sürücülerin ellerini direksiyonda, gözlerini yolda tutmalarına izin veren sesle kontrol edilen arayüzleri mümkün kılar.
    
    Özetle, düşük gecikmeli LLM'ler sorunsuz ve duyarlı bir kullanıcı deneyimi sağlamak, dil girdilerinin gerçek zamanlı veya gerçek zamanlıya yakın işlenmesini mümkün kılmak ve gerçek zamanlı veya gerçek zamanlıya yakın işleme gerektiren yeni kullanım durumlarının ve uygulamaların kapısını açmak için önemlidir.

#### Bir mesaj listesiyle `chat` fonksiyonunu çağırın

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

    assistant: Arr, ben Kaptan Kızılsakal olarak bilinirim, yedi denizin en korkunç korsanı! Ama bana kısaca Kaptan diyebilirsin. Hazineye ve maceraya aşık korkunç bir korsanım ve her zaman iyi vakit geçirmeye hazırım! İster güverteyi paspaslıyor olayım, ister grog yudumluyor, her zaman biraz eğlenceye varım. Hadi, Jolly Roger'ı çekin ve maceraya yelken açalım, ahbaplarım!

### Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
response = llm.stream_complete("Düşük gecikmeli LLM'lerin önemini açıkla")
```

```python
for r in response:
    print(r.delta, end="")
```

    Düşük gecikmeli Büyük Dil Modelleri (LLM'ler), yapay zeka ve doğal dil işleme (NLP) alanında birkaç nedenden dolayı önemlidir:
    
    1. Gerçek zamanlı uygulamalar: Düşük gecikmeli LLM'ler; chatbot'lar, sesli asistanlar ve gerçek zamanlı çeviri hizmetleri gibi gerçek zamanlı uygulamalar için esastır. Bu uygulamalar anında yanıt gerektirir ve yüksek gecikme kötü bir kullanıcı deneyimine neden olabilir.
    2. Gelişmiş kullanıcı deneyimi: Düşük gecikmeli LLM'ler daha sorunsuz ve duyarlı bir kullanıcı deneyimi sağlayabilir. Kullanıcıların, hızlı ve doğru yanıtlar veren bir hizmeti kullanmaya devam etme olasılığı daha yüksektir; bu da daha yüksek kullanıcı bağlılığı ve memnuniyeti sağlar.
    3. Daha iyi karar verme: Finansal ticaret veya otonom araçlar gibi bazı uygulamalarda, düşük gecikmeli LLM'ler gerçek zamanlı olarak kritik bilgiler sağlayabilir; bu da daha iyi karar vermeyi mümkün kılar ve kaza riskini azaltır.
    4. Ölçeklenebilirlik: Düşük gecikmeli LLM'ler daha yüksek hacimli istekleri işleyebilir, bu da onları daha ölçeklenebilir ve büyük ölçekli uygulamalar için uygun hale getirir.
    5. Rekabet avantajı: Düşük gecikmeli LLM'ler, gerçek zamanlı karar vermenin ve duyarlılığın kritik olduğu sektörlerde rekabet avantajı sağlayabilir. Örneğin, çevrimiçi oyunlarda veya e-ticarette düşük gecikmeli LLM'ler daha sürükleyici ve ilgi çekici bir kullanıcı deneyimi sunarak daha yüksek müşteri sadakati ve geliri sağlayabilir.
    
    Özetle, düşük gecikmeli LLM'ler gerçek zamanlı uygulamalar için esastır, daha iyi bir kullanıcı deneyimi sağlar, daha iyi karar vermeyi mümkün kılar, ölçeklenebilirliği artırır ve rekabet avantajı sağlar. LLM'ler çeşitli sektörlerde giderek daha önemli bir rol oynamaya devam ettikçe, düşük gecikme onların başarısı için daha da kritik hale gelecektir.

`stream_chat` uç noktasını kullanma

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Adın ne?"),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

    Arr, ben Kaptan ŞekerSakal olarak bilinirim! Benden daha renkli ve gözü pek bir korsan daha asla bulamazsın!