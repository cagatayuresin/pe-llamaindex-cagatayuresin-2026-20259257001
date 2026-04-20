# PaLM

---
title: PaLM 
 | LlamaIndex OSS Documentation
---

Bu kısa not defterinde, Google'ın PaLM LLM'sinin LlamaIndex içerisinde nasıl kullanılacağını gösteriyoruz: <https://ai.google/discover/palm2/>.

Varsayılan olarak `text-bison-001` modelini kullanıyoruz.

### Kurulum

Bu Not Defterini colab ortamında açıyorsanız, muhtemelen LlamaIndex'i yüklemeniz gerekecektir 🦙.

```python
%pip install llama-index-llms-palm
```

```python
!pip install llama-index
```

```python
!pip install -q google-generativeai
```

```
[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip available: [0m[31;49m22.3.1[0m[39;49m -> [0m[32;49m23.1.2[0m
[1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
```

```
import pprint
import google.generativeai as palm
```

```
palm_api_key = ""
```

```
palm.configure(api_key=palm_api_key)
```

### Modeli Tanımlayın

```python
models = [
    m
    for m in palm.list_models()
    if "generateText" in m.supported_generation_methods
]
model = models[0].name
print(model)
```

```python
models/text-bison-001
```

### `PaLM` LLM soyutlamamızı kullanmaya başlayın!

```python
from llama_index.llms.palm import PaLM


model = PaLM(api_key=palm_api_key)
```

```python
model.complete(prompt)
```

```python
CompletionResponse(text='1 evde 3 kedi * kedi başına 4 eldiven = 12 eldiven vardır.\n3 evde ev başına 12 eldiven * 3 ev = 36 eldiven vardır.\n1 şapka için 4m iplik gerekir. 36 şapka için şapka başına 4m * 36 şapka = 144m iplik gerekir.\n1 eldiven için 7m iplik gerekir. 36 eldiven için eldiven başına 7m * 36 eldiven = 252m iplik gerekir.\nToplamda şapkalar için 144m ve eldivenler için 252m iplik gerekmiştir, yani 144m + 252m = 396m iplik gerekmiştir.\n\nCevap: 396', additional_kwargs={}, raw={'output': '1 evde 3 kedi * kedi başına 4 eldiven = 12 eldiven vardır.\n3 evde ev başına 12 eldiven * 3 ev = 36 eldiven vardır.\n1 şapka için 4m iplik gerekir. 36 şapka için şapka başına 4m * 36 şapka = 144m iplik gerekir.\n1 eldiven için 7m iplik gerekir. 36 eldiven için eldiven başına 7m * 36 eldiven = 252m iplik gerekir.\nToplamda şapkalar için 144m ve eldivenler için 252m iplik gerekmiştir, yani 144m + 252m = 396m iplik gerekmiştir.\n\nCevap: 396', 'safety_ratings': [{'category': <HarmCategory.HARM_CATEGORY_DEROGATORY: 1>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_TOXICITY: 2>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_VIOLENCE: 3>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_SEXUAL: 4>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_MEDICAL: 5>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}, {'category': <HarmCategory.HARM_CATEGORY_DANGEROUS: 6>, 'probability': <HarmProbability.NEGLIGIBLE: 1>}]}, delta=None)
```
