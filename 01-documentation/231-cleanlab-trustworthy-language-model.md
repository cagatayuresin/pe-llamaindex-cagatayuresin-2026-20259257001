# Cleanlab Güvenilir Dil Modeli (Trustworthy Language Model - TLM)

Cleanlab’in [Güvenilir Dil Modeli (Trustworthy Language Model - TLM)](https://help.cleanlab.ai/tlm/), LLM'ler için en gelişmiş belirsizlik tahminlerini kullanarak her LLM yanıtının güvenilirliğini gerçek zamanlı olarak puanlar. Güven puanlaması, kontrol edilmeyen halüsinasyonların ve diğer LLM hatalarının engelleyici olduğu uygulamalar için kritik öneme sahiptir.

Bu sayfa, hem yanıtlar oluşturmak hem de bunların güvenilirliğini puanlamak için kendi LLM'nizin yerine TLM'yi nasıl kullanacağınızı gösterir. Ancak TLM'yi kullanmanın **tek** yolu bu değildir.
Mevcut, değiştirilmemiş RAG uygulamanıza güven puanlaması eklemek için bunun yerine [bu Güvenilir RAG öğreticisine](https://docs.llamaindex.ai/en/stable/examples/evaluation/cleanlab/) bakabilirsiniz.
RAG uygulamalarının ötesinde, `TLM.get_trustworthiness_score()` aracılığıyla herhangi bir LLM'den halihazırda oluşturulmuş yanıtların güvenilirliğini puanlayabilirsiniz.

Cleanlab [dokümantasyonunda](https://help.cleanlab.ai/tlm/) daha fazla bilgi edinebilirsiniz.

## Kurulum

Eğer bu Not Defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-cleanlab
```

```python
%pip install llama-index
```

```python
from llama_index.llms.cleanlab import CleanlabTLM
```

```python
# API anahtarını ortam değişkenlerinde veya llm içinde ayarlayın
# Ücretsiz API anahtarını şuradan alabilirsiniz: https://cleanlab.ai/
# import os
# os.environ["CLEANLAB_API_KEY"] = "api-anahtarınız"

llm = CleanlabTLM(api_key="api_anahtarınız")
```

```python
resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

    Paul Graham, Amerikalı bir bilgisayar bilimcisi, girişimci ve risk sermayedaridir. En çok, Dropbox, Airbnb ve Reddit gibi çok sayıda başarılı şirketin kurulmasına yardımcı olan girişim hızlandırıcısı Y Combinator'ın kurucu ortaklarından biri olarak tanınır. Graham aynı zamanda, startup'lar ve girişimcilikten teknoloji ve topluma kadar uzanan konulardaki içgörülü ve düşünmeye sevk eden denemeleriyle tanınan üretken bir yazar ve deneme yazarıdır. Teknoloji endüstrisinde etkili olmuş, uzmanlığı ve girişimcilik ekosistemine katkıları nedeniyle büyük saygı görmektedir.

Ayrıca yukarıdaki yanıtın güvenilirlik puanını `additional_kwargs` içinde alırsınız. TLM, tüm <istem, yanıt> çiftleri için bu puanı otomatik olarak hesaplar.

```python
print(resp.additional_kwargs)
```

    {'trustworthiness_score': 0.8659043183923533}

Yüksek bir puan, LLM'nin yanıtına güvenilebileceğini gösterir. Şimdi başka bir örnek ele alalım.

```python
resp = llm.complete(
    "Amerika Birleşik Devletleri'nde ticari bir kamyonda kullanılan ilk otomobil motorunun beygir gücü neydi?"
)
```

```python
print(resp)
```

    Amerika Birleşik Devletleri'nde ticari bir kamyonda kullanılan ilk otomobil motoru, 20 beygir gücünde 2 silindirli bir motora sahip olan 1899 Winton Motor Carriage Company Model 10'du.

```python
print(resp.additional_kwargs)
```

    {'trustworthiness_score': 0.5820799504369166}

Düşük bir puan, LLM'nin yanıtına güvenilmemesi gerektiğini gösterir.

Bu 2 basit örnekten, LLM'nin en yüksek puanlı yanıtlarının doğrudan, doğru ve uygun şekilde ayrıntılı olduğunu gözlemleyebiliriz.<br />
Öte yandan, düşük güvenilirlik puanına sahip LLM yanıtları, bazen halüsinasyon olarak adlandırılan yardımcı olmayan veya gerçekte yanlış yanıtlar iletir.

### Akış (Streaming)

Cleanlab’in TLM'si hem yanıtı hem de güvenilirlik puanını akış şeklinde (streaming) yerel olarak desteklemez. Ancak, uygulamanız için kullanılabilecek düşük gecikmeli, akışlı yanıtlar elde etmek için alternatif bir yaklaşım mevcuttur.<br>
Yaklaşımla ilgili ayrıntılı bilgi ve örnek kod [burada](https://help.cleanlab.ai/tlm/use-cases/tlm_rag/#alternate-low-latencystreaming-approach-use-tlm-to-assess-responses-from-an-existing-rag-system) mevcuttur.

## TLM'nin İleri Düzey Kullanımı

TLM aşağıdaki seçeneklerle yapılandırılabilir:
- **model**: kullanılacak temel LLM
- **max_tokens**: yanıtta oluşturulacak maksimum token sayısı
- **num_candidate_responses**: TLM tarafından dahili olarak oluşturulan alternatif aday yanıtların sayısı
- **num_consistency_samples**: LLM yanıt tutarlılığını değerlendirmek için dahili örnekleme miktarı
- **use_self_reflection**: LLM'nin oluşturduğu yanıt üzerine öz-yansıtma (self-reflect) yapmasının ve bu yanıtı öz-değerlendirmesinin (self-evaluate) istenip istenmeyeceği
- **log**: döndürülecek ek meta verileri belirtir. bir yanıtın neden düşük güvenirlikle puanlandığına dair açıklamalar almak için buraya "explanation" ekleyin.

Bu yapılandırmalar, başlatma sırasında bir sözlük olarak `CleanlabTLM` nesnesine iletilir. <br />
Bu seçenekler hakkında daha fazla ayrıntı [Cleanlab'in API dokümantasyonundan](https://help.cleanlab.ai/tlm/api/python/tlm/#class-tlmoptions) incelenebilir ve bu seçeneklerin birkaç kullanım durumu [bu not defterinde](https://help.cleanlab.ai/tlm/tutorials/tlm_advanced/) araştırılmıştır.

Uygulamanın `128` çıktı token'ına sahip `gpt-4` modeli gerektirdiği bir örneği düşünelim.

```python
options = {
    "model": "gpt-4",
    "max_tokens": 128,
}
llm = CleanlabTLM(api_key="api_anahtarınız", options=options)
```

```python
resp = llm.complete("Paul Graham kimdir?")
```

```python
print(resp)
```

    Paul Graham, İngiliz asıllı Amerikalı bir bilgisayar bilimcisi, girişimci, risk sermayedarı, yazar ve deneme yazarıdır. 1998 yılında 49 milyon doların üzerinde bir bedelle Yahoo'ya satılan ve Yahoo Store haline gelen Viaweb'in kurucu ortaklarından biri olarak tanınır. Ayrıca, Dropbox, Airbnb, Stripe ve Reddit dahil olmak üzere 2.000'den fazla şirketin kurulmasına yardımcı olan etkili girişim hızlandırıcısı ve tohum sermayesi firması Y Combinator'ın kurucu ortaklarındandır. Graham ayrıca startup şirketleri ve programlama dilleri üzerine yazdığı denemeleriyle de tanınır.

TLM'nin önceki beygir gücüyle ilgili soru için neden düşük güvenirlik tahmin ettiğini anlamak için TLM'yi başlatırken `"explanation"` bayrağını belirtin.

```python
options = {
    "log": ["explanation"],
}
llm = CleanlabTLM(api_key="api_anahtarınız", options=options)

resp = llm.complete(
    "Amerika Birleşik Devletleri'nde ticari bir kamyonda kullanılan ilk otomobil motorunun beygir gücü neydi?"
)
```

```python
print(resp)
```

    Amerika Birleşik Devletleri'ndeki ticari bir kamyonda kullanılan ilk otomobil motoru, Amerikan şirketi "GMC Truck Company" tarafından üretilen 1899 "Motor Truck"taydı. Bu ilk kamyon 2 beygir gücündeki bir motorla donatılmıştı. Ancak, ticari kamyonların gelişiminin hızla evrildiğini ve sonraki modellerin önemli ölçüde daha güçlü motorlara sahip olduğunu belirtmek önemlidir.

```python
print(resp.additional_kwargs["explanation"])
```

    Önerilen yanıt, Amerika Birleşik Devletleri'ndeki ilk ticari kamyonu yanlış bir şekilde GMC Truck Company'ye atfediyor ve 1899'da 2 beygir gücündeki bir motorla üretildiğini belirtiyor. Gerçekte, ilk ticari kamyon genellikle Amerikan şirketi "GMC Truck Company" tarafından üretilen "Motor Truck" olarak kabul edilir, ancak aslında daha sonra kurulan "GMC" markası tarafından üretilmiştir. İlk ticari kamyon genellikle "Benz Velo" veya farklı beygir gücü değerlerine sahip benzer erken modellere atfedilir. Erken kamyonların genellikle daha güçlü motorlara sahip olması nedeniyle, 2 beygir gücündeki motorla ilgili spesifik iddia da yanıltıcıdır. Bu nedenle yanıt, hem üretici hem de motorun özellikleri açısından yanlışlıklar içermektedir. 
    Bu yanıt, modelden gelen olası yanıtlar arasındaki tutarlılık eksikliği nedeniyle güvenilmezdir. İşte modelin dikkate aldığı tutarsız bir alternatif yanıt (bu da doğru olmayabilir): 
    Amerika Birleşik Devletleri'nde ticari bir kamyonda kullanılan ilk otomobil motorunun beygir gücü 6 beygir gücüydü.
