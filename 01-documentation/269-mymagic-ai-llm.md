# MyMagic AI LLM

---
title: MyMagic AI LLM
 | LlamaIndex OSS Belgeleri
---

## Giriş

Bu not defteri, bulut sepetlerinde (cloud buckets) depolanan devasa veriler üzerinde toplu çıkarım (batch inference) yapmak için MyMagicAI'nin nasıl kullanılacağını gösterir. Uygulanan tek uç noktalar, Tamamlama (Completion), Özetleme (Summarization) ve Çıkarma (Extraction) dahil olmak üzere birçok kullanım durumunda çalışabilen `complete` ve `acomplete` uç noktalarıdır. Bu not defterini kullanmak için MyMagicAI'den bir API anahtarına (Kişisel Erişim Belirteci) ve bulut sepetlerinde depolanan verilere ihtiyacınız vardır. API anahtarınızı almak için [MyMagicAI'nin web sitesindeki](https://mymagic.ai/) "Get Started" düğmesine tıklayarak kaydolun.

## Kurulum

Sepetinizi kurmak ve MyMagic API'sine bulut depolama alanınıza güvenli bir erişim yetkisi vermek için lütfen referans olarak [MyMagic belgelerini](https://docs.mymagic.ai/) ziyaret edin. Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-llms-mymagic
```

```bash
!pip install llama-index
```

```python
from llama_index.llms.mymagic import MyMagicAI
```

```python
llm = MyMagicAI(
    api_key="your-api-key",
    storage_provider="s3",  # s3, gcs
    bucket_name="your-bucket-name",
    session="your-session-name",  # toplu çıkarımın çalıştırılacağı dosyalar bu klasörde bulunmalıdır
    role_arn="your-role-arn",
    system_prompt="your-system-prompt",
    region="your-bucket-region",
    return_output=False,  # MyMagic API'nin çıktı json'unu döndürmesini isteyip istemediğiniz
    input_json_file=None,  # sepet üzerinde depolanan girdi dosyasının adı
    list_inputs=None,  # küçük toplu iş durumunda girdileri liste olarak sağlama seçeneği
    structured_output=None,  # çıktının json şeması
)
```

Not: Yukarıda `return_output` True olarak ayarlanmışsa, `max_tokens` değeri en az 100 olarak ayarlanmalıdır.

```python
resp = llm.complete(
    question="sorunuz",
    model="choose-model",  # şu anda mistral7b, llama7b, mixtral8x7b, codellama70b, llama70b desteklenmektedir...
    max_tokens=5,  # üretilecek belirteç sayısı, varsayılan 10'dur
)
```

```python
# Yanıt, nihai çıktının sepetinizde depolandığını gösterir veya iş başarısız olursa bir istisna fırlatır
print(resp)
```

## `acomplete` uç noktasını kullanarak asenkron istekler

Asenkron işlemler için aşağıdaki yaklaşımı kullanın.

```python
import asyncio
```

```python
async def main():
    response = await llm.acomplete(
        question="sorunuz",
        model="choose-model",  # desteklenen modeller sürekli güncellenmektedir ve docs.mymagic.ai adresinde listelenmektedir
        max_tokens=5,  # üretilecek belirteç sayısı, varsayılan 10'dur
    )


    print("Asenkron tamamlama yanıtı:", response)
```

```python
await main()
```
