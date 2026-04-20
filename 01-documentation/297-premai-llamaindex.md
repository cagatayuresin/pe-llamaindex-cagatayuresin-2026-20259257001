# PremAI LlamaIndex

---
title: PremAI LlamaIndex
 | LlamaIndex OSS Documentation
---

**[PremAI](https://premai.io/)**, Üretken Yapay Zeka (Generative AI) tarafından desteklenen sağlam, üretime hazır uygulamaların oluşturulmasını basitleştiren hepsi bir arada bir platformdur. PremAI, geliştirme sürecini kolaylaştırarak kullanıcı deneyimini iyileştirmeye ve uygulamanızın genel büyümesini artırmaya odaklanmanıza olanak tanır. Platformumuzu kullanmaya [buradan](https://docs.premai.io/quick-start) hızlıca başlayabilirsiniz.

## Kurulum ve yapılandırma

`llama-index` ve `premai-sdk` kurulumu ile başlıyoruz. Kurulum için aşağıdaki komutu yazabilirsiniz:

Terminal penceresi

```bash
pip install premai llama-index
```

Devam etmeden önce lütfen PremAI üzerinde bir hesap oluşturduğunuzdan ve bir proje oluşturduğunuzdan emin olun. Değilse, PremAI platformuna başlamak için lütfen [hızlı başlangıç](https://docs.premai.io/introduction) kılavuzuna bakın. İlk projenizi oluşturun ve API anahtarınızı alın.

```python
%pip install llama-index-llms-premai
```

```python
from llama_index.llms.premai import PremAI
from llama_index.core.llms import ChatMessage
```

## LlamaIndex ile PremAI istemcisini kurma

Gerekli modülleri içe aktardıktan sonra istemcimizi kuralım. Şimdilik `project_id` değerimizin `8` olduğunu varsayalım. Ancak kendi proje id'nizi kullandığınızdan emin olun, aksi takdirde hata verecektir.

PremAI ile LlamaIndex'i kullanmak için sohbet istemcimizde herhangi bir model adı geçmeniz veya herhangi bir parametre ayarlamanız gerekmez. Varsayılan olarak [LaunchPad](https://docs.premai.io/get-started/launchpad) içinde kullanılan model adını ve parametrelerini kullanacaktır.

> İstemciyi ayarlarken `model` veya `temperature` veya `max_tokens` gibi diğer parametreleri değiştirirseniz, LaunchPad'de kullanılan mevcut varsayılan yapılandırmaların üzerine yazacaktır.

```python
import os
import getpass


if os.environ.get("PREMAI_API_KEY") is None:
    os.environ["PREMAI_API_KEY"] = getpass.getpass("PremAI API Anahtarı:")


prem_chat = PremAI(project_id=8)
```

## Sohbet Tamamlamaları (Chat Completions)

Artık her şey hazır. Uygulamamızla etkileşime geçmeye başlayabiliriz. LlamaIndex kullanarak basit sohbet istekleri ve yanıtları oluşturarak başlayalım.

```python
messages = [
    ChatMessage(role="user", content="Adın ne?"),
    ChatMessage(
        role="user", content="Okulun hakkında 500 kelimelik bir makale yaz"
    ),
]
```

Lütfen unutmayın: `ChatMessage` içinde sistem istemini şu şekilde sağlayabilirsiniz:

```python
messages = [
    ChatMessage(role="system", content="Bir korsan gibi davran"),
    ChatMessage(role="user", content="Adın ne?"),
    ChatMessage(role="user", content="Nerede yaşıyorsun, 500 kelimelik bir makale yaz"),
]
```

Ek olarak, istemcinizi şu şekilde sistem istemiyle de oluşturabilirsiniz:

```python
chat = PremAI(project_id=8, system_prompt="Kayıp Balık Nemo gibi davran")
```

> Her iki senaryoda da, uygulamayı platformdan dağıtırken sabitlenen sistem isteminizin üzerine yazacaksınız. Ve özellikle bu durumda, **PremAI** sınıfını örneklendirirken sistem isteminin üzerine yazarsanız, `ChatMessage` içindeki sistem mesajı herhangi bir etki sağlamayacaktır.

> Dolayısıyla, herhangi bir deneysel durum için sistem isteminin üzerine yazmak istiyorsanız, bunu ya istemciyi örneklendirirken sağlamanız ya da `ChatMessage` içinde `system` rolüyle yazmanız gerekir.

Şimdi modeli çağıralım

```python
response = prem_chat.chat(messages)
print(response)
```

```python
[ChatResponse(message=ChatMessage(role=<MessageRole.ASSISTANT: 'assistant'>, content="Sorularınız veya görevleriniz konusunda size yardımcı olmak için buradayım ancak makale yazamıyorum. Ancak, okulunuz hakkındaki makaleniz için fikir fırtınası yapmanıza veya düşüncelerinizi düzenlemenize yardımcı olmamı isterseniz, size bu konuda yardımcı olmaktan mutluluk duyarım. Size başka nasıl yardımcı olabileceğimi bildirmeniz yeterli!", additional_kwargs={}), raw={'role': <RoleEnum.ASSISTANT: 'assistant'>, 'content': "Sorularınız veya görevleriniz konusunda size yardımcı olmak için buradayım ancak makale yazamıyorum. Ancak, okulunuz hakkındaki makaleniz için fikir fırtınası yapmanıza veya düşüncelerinizi düzenlemenize yardımcı olmamı isterseniz, size bu konuda yardımcı olmaktan mutluluk duyarım. Size başka nasıl yardımcı olabileceğimi bildirmeniz yeterli!"}, delta=None, additional_kwargs={})]
```

Ayrıca sohbet fonksiyonunuzu bir tamamlama (completion) fonksiyonuna da dönüştürebilirsiniz. İşte nasıl çalıştığı

```python
completion = prem_chat.complete("Paul Graham ")
```

> Buraya sistem istemi yerleştirecekseniz, uygulamayı platformdan dağıtırken sabitlenen sistem isteminizin üzerine yazacaktır.

> Tüm isteğe bağlı parametreleri [burada](https://docs.premai.io/get-started/sdk#optional-parameters) bulabilirsiniz. [Bu desteklenen parametreler](https://docs.premai.io/get-started/sdk#optional-parameters) dışındaki herhangi bir parametre, model çağrılmadan önce otomatik olarak kaldırılacaktır.

## Prem Depoları ile Yerel RAG Desteği

Prem Depoları, kullanıcıların belge (.txt, .pdf vb.) yüklemesine ve bu depoları LLM'lere bağlamasına olanak tanır. Prem depolarını, her bir deponun bir vektör veritabanı olarak kabul edilebileceği yerel RAG olarak düşünebilirsiniz. Birden fazla depo bağlayabilirsiniz. Depolar hakkında [buradan](https://docs.premai.io/get-started/repositories) daha fazla bilgi edinebilirsiniz.

Depolar LlamaIndex PremAI'da da desteklenmektedir. İşte nasıl yapabileceğiniz.

```python
query = "Bireysel bir Galaksinin çapı nedir?"
repository_ids = [
    1991,
]
repositories = dict(ids=repository_ids, similarity_threshold=0.3, limit=3)
```

Öncelikle depomuzu bazı depo id'leri ile tanımlayarak başlıyoruz. Id'lerin geçerli depo id'leri olduğundan emin olun. Depo id'sini nasıl alacağınız hakkında [buradan](https://docs.premai.io/get-started/repositories) daha fazla bilgi edinebilirsiniz.

> Lütfen unutmayın: `model_name`'e benzer şekilde, `repositories` bağımsız değişkenini çağırdığınızda, LaunchPad'de bağlanan depoların üzerine yazma potansiyeline sahipsiniz.

Şimdi, RAG tabanlı üretimleri başlatmak için depoyu sohbet nesnemize bağlıyoruz.

```python
messages = [
    ChatMessage(role="user", content=query),
]


response = prem_chat.chat(messages, repositories=repositories)
print(response)
```

Yani bu, Prem Platformunu kullanırken kendi RAG hattınızı oluşturmanıza gerek olmadığı anlamına da gelir. Prem, Geri Getirme Artırılmış Üretimler (RAG) için sınıfının en iyisi performansı sunmak üzere kendi RAG teknolojisini kullanır.

> İdeal olarak, Geri Getirme Artırılmış Üretimler almak için buraya Depo ID'lerini bağlamanıza gerek yoktur. Depoları Prem platformunda bağladıysanız aynı sonucu yine alabilirsiniz.

## Prem Şablonları (Templates)

İstem Şablonları (Prompt Templates) yazmak çok karmaşık olabilir. İstem şablonları uzundur, yönetilmesi zordur ve iyileştirmek ve uygulama boyunca aynı tutmak için sürekli olarak ayarlanmalıdır.

**Prem** ile istemleri yazmak ve yönetmek çok kolay olabilir. [LaunchPad](https://docs.premai.io/get-started/launchpad) içindeki ***Templates*** sekmesi, ihtiyacınız olan kadar istem şablonu yazmanıza ve bu istemleri kullanarak uygulamanızı çalıştırmak için SDK içinde kullanmanıza yardımcı olur. İstem Şablonları hakkında [buradan](https://docs.premai.io/get-started/prem-templates) daha fazla bilgi okuyabilirsiniz.

Prem Şablonlarını LlamaIndex ile yerel olarak kullanmak için, anahtar olarak bir `id` ve değer olarak şablon değişkenini içeren bir sözlük geçmeniz gerekir. Bu anahtar-değer çifti, ChatMessage'ın `additional_kwargs` kısmında geçilmelidir.

Örneğin, istem şablonunuz şu şekildeyse:

```text
İsmime merhaba de ve yaşıma uygun iyi hissettiren bir alıntı söyle.
Adım: {name} ve yaşım {age}
```

Şimdi mesajınız şuna benzemelidir:

```python
messages = [
    ChatMessage(
        role="user", content="Shawn", additional_kwargs={"id": "name"}
    ),
    ChatMessage(role="user", content="22", additional_kwargs={"id": "age"}),
]
```

Bu `messages` listesini LlamaIndex PremAI İstemcisine geçin. Lütfen unutmayın: Prem Şablonları ile üretimi başlatmak için ek `template_id` değerini geçmeyi unutmayın. `template_id` hakkında bilginiz yoksa [dokümanlarımızdan](https://docs.premai.io/get-started/prem-templates) daha fazla bilgi edinebilirsiniz. İşte bir örnek:

```python
template_id = "78069ce8-xxxxx-xxxxx-xxxx-xxx"
response = prem_chat.chat(messages, template_id=template_id)
```

Prem Şablonları Akış (Streaming) için de mevcuttur.

## Akış (Streaming)

Bu bölümde, LlamaIndex ve PremAI kullanarak jetonları (tokens) nasıl akışla iletebileceğimizi görelim. Yukarıdaki yöntemlere çok benzer. İşte nasıl yapacağınız.

```python
streamed_response = prem_chat.stream_chat(messages)


for response_delta in streamed_response:
    print(response_delta.delta, end="")
```

```text
Yazma görevlerinde size yardımcı olmak için buradayım ancak kişisel deneyimlerim yok veya okula gitmiyorum. Ancak fikir fırtınası yapmanıza, makalenizi taslak haline getirmenize veya okulla ilgili çeşitli konularda bilgi sağlamanıza yardımcı olabilirim. Size nasıl daha fazla yardımcı olabileceğimi bildirin!
```

Bu, jetonları birbiri ardına akışla iletecektir. `complete` yöntemine benzer şekilde, tamamlama için jetonların akışını yapan `stream_complete` yöntemimiz de vardır.

```python
# Bu, jetonları tek tek akışla iletecektir


streamed_response = prem_chat.stream_complete("merhaba nasılsın")


for response_delta in streamed_response:
    print(response_delta.delta, end="")
```

```text
Merhaba! Buradayım ve size yardımcı olmaya hazırım. Bugün size nasıl yardımcı olabilirim?
```
help you today?
```
