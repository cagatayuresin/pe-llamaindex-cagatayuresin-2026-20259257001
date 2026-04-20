# Amazon SageMaker Uç Noktasında Dağıtılan LLM ile LlamaIndex Kullanarak Etkileşim Kurma

---
title: Amazon SageMaker Uç Noktasında Dağıtılan LLM ile LlamaIndex Kullanarak Etkileşim Kurma
 | LlamaIndex OSS Documentation
---

Amazon SageMaker uç noktası, yeni veriler üzerinde tahminler yapmak için makine öğrenimi modellerinin, özellikle de LLM (Büyük Dil Modelleri) modellerinin dağıtımını sağlayan tamamen yönetilen bir kaynaktır.

Bu not defteri, `SageMakerLLM` kullanarak LLM uç noktalarıyla nasıl etkileşim kurulacağını göstererek ek LlamaIndex özelliklerinin kilidini açar. Bu nedenle, bir LLM'nin bir SageMaker uç noktasında dağıtıldığı varsayılır.

## Kurulum

Bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex kurmanız gerekecektir 🦙.

```python
%pip install llama-index-llms-sagemaker-endpoint
```

```python
! pip install llama-index
```

Etkileşim kurmak için uç nokta adını belirtmeniz gerekir.

```python
ENDPOINT_NAME = "<-UC-NOKTA-ADINIZ->"
```

Uç noktaya bağlanmak için kimlik bilgileri sağlanmalıdır. Şunlardan birini yapabilirsiniz:

- `profile_name` parametresini belirterek bir AWS profili kullanın; belirtilmezse varsayılan kimlik bilgisi profili kullanılacaktır.
- Kimlik bilgilerini parametre olarak geçin (`aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`, `region_name`).

daha fazla ayrıntı için [bu bağlantıyı](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) kontrol edin.

**AWS profil adı**

```python
from llama_index.llms.sagemaker_endpoint import SageMakerLLM


AWS_ACCESS_KEY_ID = "<-AWS-ERISIM-ANAHTARI-KIMLIGINIZ->"
AWS_SECRET_ACCESS_KEY = "<-AWS-GIZLI-ERISIM-ANAHTARINIZ->"
AWS_SESSION_TOKEN = "<-AWS-OTURUM-JETONUNUZ->"
REGION_NAME = "<-UC-NOKTA-BOLGE-ADINIZ->"
```

```python
llm = SageMakerLLM(
    endpoint_name=ENDPOINT_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=REGION_NAME,
)
```

**Kimlik bilgileri ile**:

```python
from llama_index.llms.sagemaker_endpoint import SageMakerLLM


ENDPOINT_NAME = "<-UC-NOKTA-ADINIZ->"
PROFILE_NAME = "<-PROFIL-ADINIZ->"
llm = SageMakerLLM(
    endpoint_name=ENDPOINT_NAME, profile_name=PROFILE_NAME
)  # Varsayılan profili kullanmak için profil adını atlayın
```

## Temel Kullanım

### Bir istem (prompt) ile `complete` fonksiyonunu çağırın

```python
resp = llm.complete(
    "Paul Graham ", formatted=True
)  # sistem istemi eklenmesini önlemek için formatted=True
print(resp)
```

```text
66 yaşında (doğum tarihi: 4 Eylül 1951). Yapay zeka, makine öğrenimi ve bilgisayarlı görü alanlarındaki çalışmalarıyla tanınan İngiliz-Amerikalı bir bilgisayar bilimcisi, programcı ve girişimcidir. Stanford Üniversitesi'nde fahri profesör ve Stanford Yapay Zeka Laboratuvarı'nda (SAIL) araştırmacıdır.


Graham, bir veri kümesinde birlikte oluşan n öğelik diziler olan "n-gram" kavramının geliştirilmesi de dahil olmak üzere bilgisayar bilimi alanına önemli katkılarda bulunmuştur. Ayrıca makine öğrenimi algoritmalarının geliştirilmesi üzerinde çalışmış ve makine öğrenimi konusu üzerine kapsamlı yazılar yazmıştır.


Graham, çalışmaları için Bilgi İşlem Makineleri Birliği (ACM) A.M. Turing Ödülü, IEEE Sinir Ağları Öncü Ödülü ve IJCAI Ödülü dahil olmak üzere sayısız ödül almıştır.
```

### Bir mesaj listesi ile `chat` fonksiyonunu çağırın

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

```text
asistan: Arrrr, beni bir titreme aldı! *göz bandını düzeltir* Benim adım Kaptan Karagaga, yedi denizin en korkulan ve en rezil korsanı! *göz kırpar*


*öhöm* Ama benden bu kadar yeter evlat. Seni bu güzel sulara getiren nedir? Ganimet yağmalamak için mi buradasın, yoksa benim gibi eski bir deniz kurduyla bir kadeh rom paylaşmak için mi? *kıkırdar*
```

## Akış (Streaming)

#### `stream_complete` uç noktasını kullanma

```python
resp = llm.stream_complete("Paul Graham ", formatted=True)
```

```python
for r in resp:
    print(r.delta)
```

```text
bugün 64 yaşında. Yapay zeka, makine öğrenimi ve bilgisayar grafikleri alanlarındaki çalışmalarıyla tanınan bir bilgisayar bilimcisi, girişimci ve yazardır.
Graham, 1956 yılında Boston, Massachusetts'te doğdu. Lisans derecesini 1978 yılında Harvard Üniversitesi'nden Bilgisayar Bilimi alanında, doktorasını ise 1982 yılında Kaliforniya Üniversitesi, Berkeley'den Bilgisayar Bilimi alanında aldı.
Graham'ın ilk çalışmaları, foto-gerçekçi görüntüler üretebilen ilk bilgisayar grafik sistemlerinin geliştirilmesine odaklandı. 1980'lerde yapay zeka ve makine öğrenimi alanıyla ilgilenmeye başladı ve bu alanları keşfetmek için aralarında ilk ticari web barındırma hizmetlerinden biri olan Viaweb'in de bulunduğu bir dizi şirketin kurucu ortağı oldu.
Graham aynı zamanda üretken bir yazardır ve doğa gibi konular üzerine bir dizi etkili makale yayınlamıştır.
```

#### `stream_chat` uç noktasını kullanma

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

```text
  ARRGH! *göz bandını düzeltir* Can dostum? *göz kırpar* Benim adım Kaptan Karagaga, yedi denizde yelken açmış en korkulan ve en rezil korsan! *kıkırdar* Ya da en azından tayfam bana öyle söylüyor. *göz kırpar*


Ee, seni bu sulara getiren nedir dostum? Ganimet yağmalamak için mi buradasın yoksa engin denizlerle ilgili hikayelerimi dinlemek için mi? *sırıtır* Her iki durumda da hazinemi seninle paylaşmaya hazırım! *göz kırpar* Sadece gizli altın depolarımdan hiçbir kara faresiyle bahsetme, yoksa kendini tahtada yürürken bulabilirsin, anladın mı? *göz kırpar*
```

## Modeli Yapılandırma

`SageMakerLLM`, Amazon SageMaker'da dağıtılan farklı dil modelleriyle (LLM) etkileşim kurmak için bir soyutlamadır. Tüm varsayılan parametreler Llama 2 modeliyle uyumludur. Bu nedenle, farklı bir model kullanıyorsanız muhtemelen aşağıdaki parametreleri ayarlamanız gerekecektir:

- `messages_to_prompt`: Bir `ChatMessage` nesneleri listesini ve mesajda belirtilmemişse bir sistem istemini kabul eden çağrılabilir bir yapıdır. Mesajları uç nokta LLM uyumlu formatta içeren bir dize döndürmelidir.

- `completion_to_prompt`: Bir sistem istemiyle bir tamamlama dizesini kabul eden ve uç nokta LLM uyumlu formatta bir dize döndüren çağrılabilir bir yapıdır.

- `content_handler`: `llama_index.llms.sagemaker_llm_endpoint_utils.BaseIOHandler` sınıfından miras alan ve şu yöntemleri uygulayan bir sınıftır: `serialize_input`, `deserialize_output`, `deserialize_streaming_output` ve `remove_prefix`.
e_prefix`.
