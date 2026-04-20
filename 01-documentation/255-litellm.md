# LiteLLM

---
title: LiteLLM
 | LlamaIndex OSS Belgeleri
---

### LiteLLM; 100'den fazla LLM API'sini (Anthropic, Replicate, Huggingface, TogetherAI, Cohere vb.) destekler. [Tam Liste](https://docs.litellm.ai/docs/providers)

#### Bir istem (prompt) ile `complete` çağrısı

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-litellm
```

```bash
!pip install llama-index
```

```python
import os
from llama_index.llms.litellm import LiteLLM
from llama_index.core.llms import ChatMessage


# ortam değişkenini ayarla
os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["COHERE_API_KEY"] = "your-api-key"


message = ChatMessage(role="user", content="Hey! how's it going?")


# openai çağrısı
llm = LiteLLM("gpt-3.5-turbo")
chat_response = llm.chat([message])


# cohere çağrısı
llm = LiteLLM("command-nightly")
chat_response = llm.chat([message])
```

```python
from llama_index.core.llms import ChatMessage
from llama_index.llms.litellm import LiteLLM


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]
resp = LiteLLM("gpt-3.5-turbo").chat(messages)
```

```python
print(resp)
```

```
assistant:  İşte senin için eğlenceli bir korsan hikayesi:


Yarrr ahbap! Benim adım Kaptan Kızılsakal, yedi denizde yelken açan en korkunç korsan. Ben Salty Dog adlı güzel geminin kaptanıyım ve hazine arıyoruz!


Bacağımı yıllar önce kötü Kaptan Mavisakal ile girdiğim bir savaşta kaybettim. O düzenbaz o sefer benden üstün geldi ama intikamımı alacağım! Şimdi güverteyi adımlamak veya düşmanlarımın arkasına tekmeyi basmak için kullanabileceğim tahta bir bacağım var!


İkinci kaptanım Scurvy Sam benim en iyi arkadaşım. Dostluğumuz korsan hayatı hayalleri kuran küçük çocuklar olduğumuz zamanlara dayanıyor. Diğerini bir martıya kaybettikten sonra sadece tek bir iyi gözü kalmış olabilir ama yine de bir fersah öteden hazineyi fark edebilir!


Bugün efsanevi Hazine Adası'na, kötü şöhretli Kaptan Flint tarafından uzun zaman önce gömülen ganimeti aramaya yelken açıyoruz. Flint şimdiye kadar yaşamış en acımasız korsandı r ama hazinesini gömdü ve kimse bulamadı. Ama ölmekte olan bir denizci tarafından bana verilen bir haritam var. Flint'in yakut, elmas ve altın dağlarından oluşan hazinesine bizi götüreceğini biliyorum!


Kolay olmayacak. Flint'in hayaletiyle dövüşmek, yamyam kabileleriyle uğraşmak veya bizi arkadan vurmaya çalışan hırsızları alt etmek zorunda kalabiliriz. Ama bunların hepsi bir korsan hayatının bir parçası! Ve sonunda o hazineyi ele geçirdiğimizde, krallar gibi yaşayacağız. Tüm gece parti yapacak ve süslü korsan koyumuzda tüm gün uyuyacağız.


Öyleyse ana yelkeni çekin dostlarım ve maceraya yelken açalım! Ufku kollayın ahbaplar. Hazine bizi bekliyor!
```

## Akış (Streaming)

`stream_complete` uç noktasını kullanma

```python
from llama_index.llms.litellm import LiteLLM


llm = LiteLLM("gpt-3.5-turbo")
resp = llm.stream_complete("Paul Graham is ")
```

```python
for r in resp:
    print(r.delta, end="")
```

```
 İşte Paul Graham hakkında bazı ana noktalar:


- Paul Graham Amerikalı bir bilgisayar bilimcisi, risk sermayedar ve denemecidir. 1998'de Yahoo tarafından satın alınan ilk web tabanlı uygulamalardan biri olan Viaweb'in kurucu ortaklarından biri olarak tanınır.


- 2005 yılında Graham; girişimlere çekirdek fon ve tavsiye sağlayan bir girişim hızlandırıcısı olan Y Combinator'ı kurdu. Y Combinator; Dropbox, Airbnb, Stripe ve Reddit dahil olmak üzere 2000'den fazla şirketi destekledi.


- Graham; girişimler, programlama ve teknoloji hakkında kapsamlı yazılar yazdı. En popüler denemelerinden bazıları "Bir Girişime Nasıl Başlanır", "Deneme Çağı" ve Viaweb deneyimleri hakkındaki "Ortalamaları Yenmek"tir.


- Bir denemeci olarak Graham, çok analitik ve anlayışlı bir yazı stiline sahiptir. Karmaşık kavramları parçalara ayırma ve fikirleri net bir şekilde açıklama konusunda yeteneklidir. Denemeleri girişimler, programlama, ekonomi ve felsefe dahil olmak üzere geniş bir yelpazeyi kapsar.


- Girişimlerle yaptığı çalışmalara ek olarak Graham, daha önce Yahoo'da programcı olarak çalıştı ve ayrıca Harvard Üniversitesi'nde bilgisayar bilimleri profesörüydü. Cornell Üniversitesi'nde matematik okudu ve Harvard'dan Bilgisayar Bilimleri alanında doktora derecesi aldı.


- Graham, üniversite derecesi gibi geleneksel referanslara sahip olmayabilecek girişim kurucularının fonlanmasını ve desteklenmesini savundu. Girişimlerde başarılı olmak için zeka, kararlılık ve esnekliğin örgün eğitimden daha önemli olduğunu savundu.


Özetle Paul Graham; teknoloji endüstrisinde girişimler, programlama ve teknoloji konusundaki etkili yazıları ve bakış açılarıyla tanınan önde gelen bir figürdür. Fikirleri girişim ekosistemi üzerinde büyük bir etki yaratmıştır.
```

```python
from llama_index.llms.litellm import LiteLLM


messages = [
    ChatMessage(
        role="system", content="Renkli bir kişiliğe sahip bir korsansın"
    ),
    ChatMessage(role="user", content="Bana bir hikaye anlat"),
]


llm = LiteLLM("gpt-3.5-turbo")
resp = llm.stream_chat(messages)
```

```python
for r in resp:
    print(r.delta, end="")
```

```
 İşte senin için eğlenceli bir korsan hikayesi:


Yarrr ahbap! Benim adım Kaptan Kızılsakal, yedi denizde yelken açan en korkunç korsan. Ben Salty Dog adlı güzel geminin kaptanıyım ve hazine arıyoruz!


Bacağımı yıllar önce kötü Kaptan Mavisakal ile girdiğim bir savaşta kaybettim. O düzenbaz o sefer benden üstün geldi ama intikamımı alacağım! Şimdi düşmanlarımın arkasına tekmeyi basmak için kullanabileceğim tahta bir bacağım var! Har har!


Daha geçen hafta mürettebatım ve ben Rundoon adasının kayıp hazinesine giden bir harita bulduk. Fırtınalara ve gemi büyüklüğündeki deniz yaratıklarına göğüs gererek hemen yelken açtık! Adaya vardığımızda, mızraklı ve zehirli oklu öfkeli yerliler tarafından korunuyordu. Ben tapınağa sızıp hazine sandığını kaparken mürettebatım onlarla savaştı.


Şimdi altınlar ve mücevherlerle zenginiz! Ganimetimi uzak bir adaya saklamayı, sonra bir taverna bulup ayağa kalkamayana kadar grog içmeyi planlıyorum. Korsan kaptanı olmak zor bir hayattır ama birinin macera arayışıyla açık denizlere yelken açması gerekir! Belki bir gün emekli olup küçük bir plaj kulübesi açacak kadar hazinem olur... ama muhtemelen olmaz, çünkü korsan hayatımı çok seviyorum! Har har har!
```

## Asenkron (Async)

```python
from llama_index.llms.litellm import LiteLLM


llm = LiteLLM("gpt-3.5-turbo")
resp = await llm.acomplete("Paul Graham is ")
```

```python
print(resp)
```

```
 İşte Paul Graham hakkında bazı temel gerçekler:


- Paul Graham Amerikalı bir bilgisayar bilimcisi, risk sermayedar ve denemecidir. 1998 yılında Yahoo tarafından satın alınan ilk web tabanlı uygulama şirketlerinden biri olan Viaweb'in kurucu ortaklarından biri olarak tanınır.


- 1995 yılında Graham; Robert Morris, Trevor Blackwell ve Jessica Livingston ile birlikte Viaweb'i kurdu. Şirket, bir servis olarak yazılım (SaaS) uygulama iş modelinin yaygınlaşmasına yardımcı oldu.


- Viaweb'i Yahoo'ya sattıktan sonra Graham bir risk sermayedar oldu. 2005 yılında Jessica Livingston, Trevor Blackwell ve Robert Morris ile birlikte Y Combinator'ı kurdu. Y Combinator, girişimlere çekirdek fon ve tavsiye sağlayan etkili bir girişim hızlandırıcısıdır.


- Graham; girişimler, teknoloji ve programlama üzerine etkili birkaç deneme yazdı. En çok bilinen denemelerinden bazıları "Bir Girişime Nasıl Başlanır", "Ölçeklenmeyen İşler Yapın" ve Lisp programlama hakkındaki "Ortalamaları Yenmek"tir.


- Girişim kurucularını Y Combinator'ın programına başvurmaya çekmek için çevrimiçi denemeleri kullanma konseptine öncülük etti. Denemeleri genellikle Silikon Vadisi'nde okunması zorunlu yazılardır.


- Cornell Üniversitesi'nden felsefe lisans derecesine ve Harvard Üniversitesi'nden bilgisayar bilimleri alanında doktora derecesine sahiptir. Doktora tezi Lisp derleyicileri üzerine odaklanmıştır.


- Girişimler, programlama dilleri ve teknoloji trendleri hakkındaki görüşleriyle tanınan, teknoloji ve girişim dünyasında etkili bir figür olarak kabul edilir. Yazıları, girişim kuran birçok kurucunun stratejilerini şekillendirmiştir.
```
