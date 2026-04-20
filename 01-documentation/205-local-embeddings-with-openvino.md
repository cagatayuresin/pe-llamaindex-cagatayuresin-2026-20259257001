# OpenVINO ile Yerel Gömmeler (Local Embeddings)

[OpenVINO™](https://github.com/openvinotoolkit/openvino), yapay zeka çıkarımını (inference) optimize etmek ve dağıtmak için kullanılan açık kaynaklı bir araç setidir. OpenVINO™ Runtime, x86 ve ARM CPU'lar ile Intel GPU'lar dahil olmak üzere çeşitli donanım [aygıtlarını](https://github.com/openvinotoolkit/openvino?tab=readme-ov-file#supported-hardware-matrix) destekler. Bilgisayarlı Görü, Otomatik Konuşma Tanıma, Doğal Dil İşleme ve diğer yaygın görevlerde derin öğrenme performansını artırmaya yardımcı olabilir.

Hugging Face gömme (embedding) modeli OpenVINO tarafından `OpenVINOEmbedding` veya `OpenVINOGENAIEmbedding` sınıfı aracılığıyla desteklenebilir; OpenClip modeli ise `OpenVINOClipEmbedding` sınıfı aracılığıyla desteklenebilir.

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-embeddings-openvino
```

```python
!pip install llama-index
```

## Model Dışa Aktarıcı (Model Exporter)

`create_and_save_openvino_model` fonksiyonu ile modelinizi OpenVINO IR formatına dışa aktarmanız ve modeli yerel klasörden yüklemeniz mümkündür.

```python
from llama_index.embeddings.huggingface_openvino import OpenVINOEmbedding

OpenVINOEmbedding.create_and_save_openvino_model(
    "BAAI/bge-small-en-v1.5", "./bge_ov"
)
```

    /home2/ethan/intel/llama_index/llama_test/lib/python3.10/site-packages/openvino/runtime/__init__.py:10: DeprecationWarning: `openvino.runtime` modülü kullanımdan kaldırılmıştır ve 2026.0 sürümünde kaldırılacaktır. Lütfen `openvino.runtime` yerine `openvino` kullanın.
      warnings.warn(

    OpenVINO modeli ./bge_ov dizinine kaydedildi. Şununla kullanın: `embed_model = OpenVINOEmbedding(model_id_or_path='./bge_ov')`.

## Model Yükleme (Model Loading)

Eğer bir Intel GPU'nuz varsa, çıkarımı orada çalıştırmak için `device="gpu"` belirtebilirsiniz.

```python
ov_embed_model = OpenVINOEmbedding(model_id_or_path="./bge_ov", device="cpu")
```

```python
embeddings = ov_embed_model.get_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

    384
    [-0.0030246784444898367, -0.012189766392111778, 0.04163273051381111, -0.037758368998765945, 0.02439723163843155]

## OpenVINO GenAI ile Model Yükleme

Çalışma zamanında PyTorch bağımlılıklarından kaçınmak için yerel gömme modelinizi `OpenVINOGENAIEmbedding` sınıfı ile yükleyebilirsiniz.

```python
%pip install llama-index-embeddings-openvino-genai
```

```python
from llama_index.embeddings.openvino_genai import OpenVINOGENAIEmbedding

ov_embed_model = OpenVINOGENAIEmbedding(model_path="./bge_ov", device="CPU")
```

    /home2/ethan/intel/llama_index/llama_test/lib/python3.10/site-packages/openvino/runtime/__init__.py:10: DeprecationWarning: `openvino.runtime` modülü kullanımdan kaldırılmıştır ve 2026.0 sürümünde kaldırılacaktır. Lütfen `openvino.runtime` yerine `openvino` kullanın.
      warnings.warn(

```python
embeddings = ov_embed_model.get_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

    384
    [-0.0030246784444898367, -0.012189766392111778, 0.04163273051381111, -0.037758368998765945, 0.02439723163843155]

## OpenClip Model Dışa Aktarıcı

`OpenVINOClipEmbedding` sınıfı, OpenVINO çalışma zamanı ile open_clip modellerini dışa aktarmayı ve yüklemeyi destekleyebilir.

```python
%pip install open_clip_torch
```

```python
from llama_index.embeddings.huggingface_openvino import (
    OpenVINOClipEmbedding,
)

OpenVINOClipEmbedding.create_and_save_openvino_model(
    "laion/CLIP-ViT-B-32-laion2B-s34B-b79K",
    "ViT-B-32-ov",
)
```

## Çok Modlu (MultiModal) Model Yükleme

Eğer bir Intel GPU'nuz varsa, çıkarımı orada çalıştırmak için `device="GPU"` belirtebilirsiniz.

```python
ov_clip_model = OpenVINOClipEmbedding(
    model_id_or_path="./ViT-B-32-ov", device="CPU"
)
```

## OpenVINO ile görüntüleri ve sorguları gömme

```python
from PIL import Image
import requests
from numpy import dot
from numpy.linalg import norm

image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStMP8S3VbNCqOQd7QQQcbvC_FLa1HlftCiJw&s"
im = Image.open(requests.get(image_url, stream=True).raw)
print("Görüntü:")
display(im)

im.save("logo.jpg")
image_embeddings = ov_clip_model.get_image_embedding("logo.jpg")
print("Görüntü boyutu:", len(image_embeddings))
print("Görüntü gömmesi:", image_embeddings[:5])

text_embeddings = ov_clip_model.get_text_embedding(
    "Koyu arka plan üzerinde pembe mavi bir larkanın (llama) logosu"
)
print("Metin boyutu:", len(text_embeddings))
print("Metin gömmesi:", text_embeddings[:5])

cos_sim = dot(image_embeddings, text_embeddings) / (
    norm(image_embeddings) * norm(text_embeddings)
)
print("Kosinüs benzerliği:", cos_sim)
```

    Görüntü:

![png](output_19_1.png)

    Görüntü boyutu: 512
    Görüntü gömmesi: [-0.03019799292087555, -0.09727513045072556, -0.6659489274024963, -0.025658488273620605, 0.05379948765039444]
    Metin boyutu: 512
    Metin gömmesi: [-0.15816599130630493, -0.25564345717430115, 0.22376027703285217, -0.34983670711517334, 0.31968361139297485]
    Kosinüs benzerliği: 0.27307014923203976

Daha fazla bilgi için şuralara bakabilirsiniz:

* [OpenVINO LLM kılavuzu](https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide.html).

* [OpenVINO Dokümantasyonu](https://docs.openvino.ai/2024/home.html).

* [OpenVINO Başlangıç Kılavuzu](https://www.intel.com/content/www/us/en/content-details/819067/openvino-get-started-guide.html).

* [LlamaIndex ile RAG örneği](https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/llm-rag-llamaindex).
