# CometAPI

CometAPI; GPT serisi, Claude serisi, Gemini serisi ve daha fazlasını içeren çeşitli son teknoloji LLM modellerine, OpenAI uyumlu birleşik bir arayüz üzerinden erişim sağlar. Daha fazla bilgiyi [ana sayfalarında](https://www.cometapi.com/) bulabilirsiniz.

Kaydolmak ve bir API anahtarı almak için https://api.cometapi.com/console/token adresini ziyaret edin.

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-cometapi
```

```python
%pip install llama-index
```

```python
from llama_index.llms.cometapi import CometAPI
```

## ChatMessage Listesi ile `chat` Çağrısı Yapın
`COMETAPI_API_KEY` ortam değişkenini ayarlamanız veya sınıf yapıcısında (constructor) api_key'i belirtmeniz gerekir.

```python
import os

os.environ["COMETAPI_KEY"] = "<cometapi-anahtarınız>"

api_key = os.getenv("COMETAPI_KEY")
llm = CometAPI(
    api_key=api_key,
    max_tokens=256,
    context_window=4096,
    model="gpt-5-chat-latest",
)
```

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="system", content="Yardımsever bir asistansın"),
    ChatMessage(role="user", content="Sadece 'Selam' de!"),
]
resp = llm.chat(messages)
print(resp)
```

    assistant: Selam

```python
resp = llm.complete("Kaiming He kimdir?")
```

```python
print(resp)
```

    Kaiming He, bilgisayar görüsü (computer vision) ve derin öğrenme alanındaki etkili katkılarıyla tanınan ünlü bir bilgisayar bilimcisi ve araştırma bilimcisidir. Özellikle, CVPR 2016'da En İyi Makale Ödülü'nü kazanan *"Deep Residual Learning for Image Recognition"* (2015) adlı makalede tanıtılan **ResNet** (Artık Ağlar - Residual Networks) mimarisinin ana yazarlarından biri olmasıyla tanınır. ResNet, artık bağlantıları (residual connections) kullanarak çok derin sinir ağlarının eğitimini önemli ölçüde iyileştirmiş ve birçok görüntü işleme görevi için temel bir mimari haline gelmiştir.
    
    ### Kaiming He Hakkında Önemli Bilgiler:
    
    - **Eğitim**:  
      Kaiming He, doktora derecesini Hong Kong Çince Üniversitesi'nden (CUHK) bilgisayar bilimleri alanında almıştır. Burada Prof. Jian Sun ile çalışmış ve Visual Computing Group ile iş birliği yapmıştır.
    
    - **Araştırma Kariyeri**:
      - Microsoft Research Asia (MSRA) bünyesinde çalışmıştır.
      - Daha sonra Facebook AI Research (FAIR) bünyesinde araştırma görevlisi olarak yer almıştır.
      - Son yıllarda, bilgisayar görüsü, derin öğrenme ve yapay zeka konularına odaklanarak FAIR (şimdi Meta AI'nın bir parçası) bünyesinde çalışmalarını sürdürmektedir.
    
    - **Başlıca Katkılar**:
      - **ResNet** (Deep Residual Networks, 2015) — derin ağlarda devrim yaratmıştır.

### Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
message = ChatMessage(role="user", content="ResNet'in ne olduğunu anlat")
resp = llm.stream_chat([message])
for r in resp:
    print(r.delta, end="")
```

    ResNet, **Residual Network** (Artık Ağ) ifadesinin kısaltmasıdır ve Microsoft Research tarafından 2015 yılında Kaiming He ve arkadaşları tarafından hazırlanan *"Deep Residual Learning for Image Recognition"* makalesinde tanıtılan bir derin sinir ağı mimarisi türüdür. **ImageNet Large Scale Visual Recognition Challenge ( al. It became famous after winning the **ImageNet Large Scale Visual Recognition Challenge (ILSVRC) 2015**. mimarisi, 2015 yılında düzenlenen **ImageNet Large Scale Visual Recognition Challenge (ILSVRC) 2015** yarışmasını kazandıktan sonra ünlenmiştir.
    
    ---
    
    ### **Temel fikir**
    ResNet'in en büyük yeniliği,ILSVRC) 2015**. **atlamalı bağlantılar** (veya kestirme bağlantılar - skip connections) kullanan **artık öğrenme** (residual learning) kavramıdır. Çok derin derin sinir ağlarında, **yok olan/patlayan gradyan sorunu** ve optimizasyon zorlukları nedeniyle performans düşebilir. ResNet, belirli katmanların ağ içinde özdeşlik eşlemeleri (identity mappings) aracılığıyla ileriye "atlamasına" izin vererek bu sorunu çözer.
    
    Bir *artık blok* (residual block) şuna benzer:
    
    ```
    Girdi → [Katman(lar): Conv, BatchNorm, ReLU] → Çıktı
       \_____________________________________/
                      (atlamalı bağlantı)
    ```
    
    Bağlantı aracılığıyla doğrudan bir \( H(x) \) eşlemesini öğrenmek yerine, artık blok \( F(x) = H(x) - x \) öğrenir, böylece:
    \[
    H(x) = F(x) + x
    \]
    Burada \( x \), bloğun çıktısına doğrudan eklenerek daha kolay gradyan akışı sağlar ve ağın eğitimine olanak tanır.

```python
resp = llm.stream_complete("Bana Büyük Dil Modellerinden (LLM) bahset")
```

```python
for r in resp:
    print(r.delta, end="")
```

    Tabii! **Büyük Dil Modelleri** (Büyük Dil Modelleri - LLMs), insan dilini anlamak, oluşturmak ve manipüle etmek için tasarlanmış bir tür **yapay zeka modeli**dir. Kitaplar, makaleler, web siteleri, kodlar ve daha fazlasından oluşan devasa miktardaki metin verileriyle eğitilirler; bu da bir isteme (prompt) dayalı olarak tutarlı metinler tahmin etmelerini ve üretmelerini sağlar.
    
    İşte ayrıntılı bir genel bakış:
    
    ---
    
    ## **1. Nedirler?**
    - LLM'ler, genellikle 2017 yılında *Vaswani ve arkadaşları* tarafından *"Attention Is All You Need"* makalesinde tanıtılan **transformer mimarisine** dayanan **derin öğrenme** modellerinin bir alt kümesidir.
    - Bunlara *"büyük"* denilmesinin sebebi, milyarlarca hatta trilyonlarca **parametreye** (eğitim sırasında öğrenilen ayarlanabilir ağırlıklar) sahip olmaları ve devasa veri kümeleri üzerinde eğitilmeleridir.
    
    ---
    
    ## **2. Nasıl Çalışırlar?**
    1. **Eğitim Verileri**  
       Kitaplar, Wikipedia, internet vb. kaynaklardan alınan devasa metin külliyatlarından (corpora) dil kalıplarını öğrenirler.
    2. **Tokenizasyon**  
       Metin, *token* adı verilen küçük parçalara (bunlar kelimelerin tamamı, alt kelimeler veya karakterler olabilir) bölünür.
    3. **Sinirsel Mimari**  
       Transformer'lar, farklı bölümler arasındaki ilişkileri kurmak için *öz-dikkat* (self-attention) mekanizmalarını kullanırlar.

### Farklı Modellerin Kullanımı

CometAPI; GPT, Claude ve Gemini serileri dahil olmak üzere çeşitli yapay zeka modellerini destekler.

```python
# Claude modelini kullanma
claude_llm = CometAPI(
    api_key=api_key, model="claude-3-7-sonnet-latest", max_tokens=200
)

resp = claude_llm.complete("Derin öğrenmeyi kısaca açıkla")
print(resp)
```

    # Derin Öğrenme: Kısa Bir Açıklama
    
    Derin öğrenme, verileri analiz etmek ve tahminlerde bulunmak için çok katmanlı (bu yüzden "derin") sinir ağlarını kullanan makine öğreniminin bir alt kümesidir.
    
    ## Temel Özellikler:
    
    - **Sinir Ağları**: İnsan beyninden esinlenen bu ağlar, katmanlar halinde organize edilmiş birbirine bağlı düğümlerden (nöronlar) oluşur.
    - **Otomatik Özellik Çıkarımı**: Geleneksel makine öğreniminin aksine, derin öğrenme, manuel mühendislik olmadan verilerdeki önemli özellikleri otomatik olarak keşfeder.
    - **Hiyerarşik Öğrenme**: Alt katmanlar basit kalıpları öğrenirken, daha derin katmanlar bunları birleştirerek karmaşık kavramları tanır.
    - **Büyük Veri Gereksinimi**: Genellikle iyi performans göstermek için önemli miktarda veriye ihtiyaç duyar.
    
    Derin öğrenme; görüntü tanıma, doğal dil işleme, konuşma tanıma ve öneri sistemleri dahil olmak üzere birçok modern teknolojinin temelini oluşturur. Etkinliği, verilerdeki son derece karmaşık ilişkileri modelleme yeteneğinden gelir, ancak bu genellikle önemli hesaplama kaynakları gerektirir.
