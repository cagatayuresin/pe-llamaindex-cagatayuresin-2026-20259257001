# Aleph Alpha

Aleph Alpha, insan benzeri metinler üretebilen güçlü bir dil modelidir. Aleph Alpha, birden fazla dilde ve stilde metin üretme yeteneğine sahiptir ve belirli alanlarda metin üretmek üzere ince ayar (fine-tune) yapılabilir.

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-alephalpha
```

```python
!pip install llama-index
```

#### Aleph Alpha jetonunuzu (token) ayarlayın

```python
import os

os.environ["AA_TOKEN"] = "jetonunuz_buraya"
```

#### Bir istem (prompt) ile `complete` çağrısı

```python
from llama_index.llms.alephalpha import AlephAlpha

# Jetonunuzu özelleştirmek için bunu yapın,
# aksi takdirde ortam değişkeninizden AA_TOKEN aranacaktır
# llm = AlephAlpha(token="<aa_token>")
llm = AlephAlpha(model="luminous-base-control")

resp = llm.complete("Paul Graham ")
```

```python
print(resp)
```

     tanınmış bir bilgisayar bilimcisi ve girişimcidir. PayPal'ın kurucu ortağı ve Y Combinator girişim hızlandırıcısının kurucu ortağıdır. Ayrıca "Programming the Web" kitabının ortak yazarıdır. Paul Graham ayrıca bilgisayar bilimi, girişimcilik ve startuplar ile ilgili konularda sık sık konuşmacı ve yazar olarak yer almaktadır. "Girişimler Neden Başarısız Olur" konusu üzerine birkaç blog yazısı yazmıştır. Bu yazıda, Paul Graham'ın girişimlerin neden başarısız olduğu hakkındaki blog yazısından bazı önemli noktaları özetleyeceğim.
    
    1. Net bir vizyon eksikliği: Girişimler genellikle ne olduklarına dair net bir vizyondan yoksundur...

#### Ek Yanıt Ayrıntıları

Log olasılıkları (log probabilities) gibi ayrıntılı yanıt bilgilerine erişmek için, AlephAlpha örneğinizin `log_probs` parametresiyle başlatıldığından emin olun. `CompletionResponse` nesnesinin `logprobs` özniteliği bu verileri içerecektir. Model sürümü ve ham tamamlama metni gibi diğer ayrıntılara, eğer yanıtın bir parçasıysa doğrudan veya `additional_kwargs` üzerinden erişilebilir.

```python
from llama_index.llms.alephalpha import AlephAlpha

llm = AlephAlpha(model="luminous-base-control", log_probs=0)

resp = llm.complete("Paul Graham ")

if resp.logprobs is not None:
    print("\nLog Olasılıkları (Log Probabilities):")
    for lp_list in resp.logprobs:
        for lp in lp_list:
            print(f"Belirteç (Token): {lp.token}, LogProb: {lp.logprob}")

if "model_version" in resp.additional_kwargs:
    print("\nModel Sürümü:")
    print(resp.additional_kwargs["model_version"])

if "raw_completion" in resp.additional_kwargs:
    print("\nHam Tamamlama (Raw Completion):")
    print(resp.additional_kwargs["raw_completion"])
```

    Log Olasılıkları (Log Probabilities):
    Token:  a, LogProb: -0.95955
    Token:  well, LogProb: -1.9219251
    Token: -, LogProb: -0.1312752
    Token: known, LogProb: -0.022855662
    Token:  computer, LogProb: -0.9569155
    Token:  scientist, LogProb: -0.06721641
    Token:  and, LogProb: -0.56296504
    Token:  entrepreneur, LogProb: -0.65574974
    Token: ., LogProb: -0.5926046
    Token:  He, LogProb: -0.1885516
    Token:  is, LogProb: -0.3927348
    Token:  the, LogProb: -0.46820825
    Token:  co, LogProb: -0.465878
    Token: -, LogProb: -0.024082167
    Token: founder, LogProb: -0.009869587
    Token:  of, LogProb: -0.31641242
    Token:  PayPal, LogProb: -1.0825713
    Token:  and, LogProb: -0.39408743
    Token:  a, LogProb: -1.45493
    Token:  co, LogProb: -1.0837904
    Token: -, LogProb: -0.0011430404
    Token: founder, LogProb: -0.074010715
    Token:  of, LogProb: -0.038962167
    Token:  the, LogProb: -1.7761776
    Token:  Y, LogProb: -0.41853565
    Token:  Combin, LogProb: -0.17868777
    Token: ator, LogProb: -2.0265374e-05
    Token:  startup, LogProb: -0.24595682
    Token:  acceler, LogProb: -0.5855012
    Token: ator, LogProb: -6.675698e-06
    Token: ., LogProb: -0.022597663
    Token:  He, LogProb: -0.8310143
    Token:  has, LogProb: -1.5842702
    Token:  also, LogProb: -0.5774656
    Token:  been, LogProb: -1.3938092
    Token:  a, LogProb: -0.67207164
    Token:  professor, LogProb: -1.0511048
    Token:  at, LogProb: -0.13273911
    Token:  the, LogProb: -0.7993539
    Token:  MIT, LogProb: -1.2281163
    Token:  Media, LogProb: -0.7707413
    Token:  Lab, LogProb: -0.06716257
    Token: ., LogProb: -0.9140582
    Token:  Paul, LogProb: -0.8244309
    Token:  Graham, LogProb: -0.15202633
    Token:  has, LogProb: -1.3735206
    Token:  written, LogProb: -0.77148163
    Token:  several, LogProb: -0.7167357
    Token:  books, LogProb: -0.24542983
    Token:  on, LogProb: -0.77700675
    Token:  computer, LogProb: -0.8485363
    Token:  science, LogProb: -0.026196867
    Token:  and, LogProb: -0.4796574
    Token:  entrepreneurs, LogProb: -0.48952234
    Token: hip, LogProb: -1.0847986e-05
    Token: ,, LogProb: -0.1426171
    Token:  including, LogProb: -0.10799221
    Token:  ", LogProb: -0.4733107
    Token: Program, LogProb: -0.9295699
    Token: ming, LogProb: -0.00090034
    Token:  the, LogProb: -1.5219054
    Token:  Universe, LogProb: -1.2475122
    Token: ", LogProb: -0.8377396
    Token:  and, LogProb: -0.014596111
    Token:  ", LogProb: -0.0034322182
    Token: The, LogProb: -0.97810173
    Token:  Art, LogProb: -1.4708842
    Token:  of, LogProb: -0.0017665509
    Token:  Computer, LogProb: -0.027323013
    Token:  Programming, LogProb: -0.09090222
    Token: "., LogProb: -0.2312944
    Token:  He, LogProb: -0.9431941
    Token:  is, LogProb: -0.52350885
    Token:  also, LogProb: -0.8409716
    Token:  the, LogProb: -1.2813272
    Token:  founder, LogProb: -0.8080497
    Token:  of, LogProb: -0.12735468
    Token:  the, LogProb: -0.26858208
    Token:  startup, LogProb: -1.7183943
    Token:  incub, LogProb: -0.71643037
    Token: ator, LogProb: -0.00013922676
    Token: ,, LogProb: -1.6374074
    Token:  Y, LogProb: -1.3464186
    Token:  Combin, LogProb: -0.043204635
    Token: ator, LogProb: -1.490105e-05
    Token: ., LogProb: -0.48073012
    Token: <|endoftext|>, LogProb: -0.30235213

    Model Sürümü:
    20240215

    Ham Tamamlama (Raw Completion):
     a well-known computer scientist and entrepreneur. He is the co-founder of PayPal and a co-founder of the Y Combinator startup accelerator. He has also been a professor at the MIT Media Lab. Paul Graham has written several books on computer science and entrepreneurship, including "Programming the Universe" and "The Art of Computer Programming". He is also the founder of the startup incubator, Y Combinator.

## Asenkron (Async)

```python
from llama_index.llms.alephalpha import AlephAlpha

llm = AlephAlpha(model="luminous-base-control")
resp = await llm.acomplete("Paul Graham ")
```

```python
print(resp)
```

     yapay zeka ve bilgisayar bilimi alanındaki çalışmalarıyla tanınan bir bilgisayar bilimcisi ve girişimcidir. Girişimlerin fon ve kaynak bulmasına yardımcı olan bir girişim hızlandırıcısı olan Y Combinator şirketinin kurucu ortağıdır. Paul Graham ayrıca "Programming: Principles and Practice" ve "The Art of Computer Programming" gibi bilgisayar bilimi ve girişimcilik üzerine birkaç kitap yazmıştır. Bilgisayar bilimi topluluğunda tanınmış bir figürdür ve alana önemli katkılarda bulunmuştur.
