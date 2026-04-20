# DeepSeek

# LlamaIndex LLM Entegrasyonu: DeepSeek

Bu, LlamaIndex için DeepSeek entegrasyonudur. Bir API anahtarının nasıl alınacağı ve hangi modellerin desteklendiği hakkında bilgi için [DeepSeek](https://api-docs.deepseek.com/) adresini ziyaret edin.

Bu yazının yazıldığı sırada şunları kullanabilirsiniz:
- `deepseek-chat`
- `deepseek-reasoner`

## Kurulum

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-deepseek
```

```python
from llama_index.llms.deepseek import DeepSeek

# Ayrıca ortam değişkenlerinizde DEEPSEEK_API_KEY'i ayarlayabilirsiniz
llm = DeepSeek(model="deepseek-reasoner", api_key="api_anahtarınız")

# Ayrıca deepseek'i varsayılan llm'niz olarak ayarlamak isteyebilirsiniz
# from llama_index.core import Settings
# Settings.llm = llm
```

```python
response = llm.complete("9.9 mu yoksa 9.11 mi daha büyük?")
```

```python
print(response)
```

    9.9'un mu yoksa 9.11'in mi daha büyük olduğunu belirlemek için basamaklarını hizalayarak karşılaştıralım:
    
    1. **Her iki sayıyı da aynı sayıda ondalık basamakla yazın**:  
       - \(9.9\), \(9.90\) olur.  
       - \(9.11\), olduğu gibi \(9.11\) kalır.  
    
    2. **Basamak basamak karşılaştırın**:  
       - **Birler basamağı**: Her ikisinde de \(9\) var (eşit).  
       - **Onda birler basamağı**: \(9.90\)'daki \(9\) ile \(9.11\)'deki \(1\). \(9 > 1\) olduğu için, \(9.90 > 9.11\).  
    
    **Sonuç**:  
    \(9.9\) (veya \(9.90\)), \(9.11\)'den büyüktür.  
    
    \(\boxed{9.9}\)

#### Bir mesaj listesiyle `chat` çağrısı yapın

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(
        role="user", content="'strawberry' kelimesinde kaç tane 'r' harfi var?"
    ),
]
resp = llm.chat(messages)
```

```python
print(resp)
```

    assistant: Arrrr, ahbap! O sinsi 'r'leri bulmak için "strawberry" kelimesini yağmalayalım! İşte dökümü:  
    
    **S - T - R - A - W - B - E - R - R - Y**  
    
    Vay canına! Bu harflerin arasında pusuda bekleyen **3 tane 'r'** var! Evet, bir tanesi "straw" kısmında ve iki tanesi "berry" kısmında; tıpkı üç sandığa gömülmüş hazine gibi! 🏴‍☠️🍓

### Akış (Streaming)

`stream_complete` bitiş noktasını (endpoint) kullanma

```python
response = llm.stream_complete("9.9 mu yoksa 9.11 mi daha büyük?")
```

```python
for r in response:
    print(r.delta, end="")
```

    9.9'un mu yoksa 9.11'in mi daha büyük olduğunu belirlemek için, her iki sayıyı da aynı sayıda ondalık basamağa sahip olacak şekilde dönüştürerek karşılaştırabiliriz. 
    
    - 9.9, 9.90 olarak yazılabilir (iki ondalık basamak yapmak için bir sıfır ekleyerek).
    - 9.11 zaten iki ondalık basamaklıdır.
    
    Ardından, onda birler basamağını karşılaştırırız:
    - 9.90'ın onda birler basamağında 9 vardır.
    - 9.11'in onda birler basamağında 1 vardır.
    
    9, 1'den büyük olduğu için 9.90, 9.11'den daha büyüktür. 
    
    Doğrulamak için çıkarma yapabiliriz:
    \[ 9.90 - 9.11 = 0.79 \]
    Pozitif sonuç, 9.90'ın 9.11'den büyük olduğunu gösterir.
    
    Başka bir yöntem de kesirlere dönüştürmektir:
    - 9.9, \( \frac{99}{10} \)'dur ve bu da \( \frac{990}{100} \)'e eşittir.
    - 9.11, \( \frac{911}{100} \)'dür.
    
    \( \frac{990}{100} \) ile \( \frac{911}{100} \)'ü karşılaştırdığımızda, 990'ın 911'den büyük olduğunu görürüz.
    
    Böylece, büyük olan sayı \boxed{9.9}'dur.

`stream_chat` bitiş noktasını kullanma

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(
        role="user", content="'strawberry' kelimesinde kaç tane 'r' harfi var?"
    ),
]
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

    Arrrr, ahbap! O sinsi 'r'leri saymak için "strawberry" harflerini yağmalayalım! 🏴‍☠️
    
    **S-T-R-A-W-B-E-R-R-Y**  
    Yarrr, işte dökümü:  
    
    1. **S** 🚫  
    2. **T** 🚫  
    3. **R** ✅ (1. 'r')  
    4. **A** 🚫  
    5. **W** 🚫  
    6. **B** 🚫  
    7. **E** 🚫  
    8. **R** ✅ (2. 'r')  
    9. **R** ✅ (3. 'r')  
    10. **Y** 🚫  
    
    **Toplam 'r' sayısı: 3**  
    Vay canına! "strawberry" içinde tam üç 'r' pusuda bekliyormuş! 🍓⚔️
