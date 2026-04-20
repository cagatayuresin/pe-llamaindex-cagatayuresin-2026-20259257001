# Optimum-Intel kullanarak Optimize Edilmiş Gömme Modeli

LlamaIndex, [Optimum-Intel kütüphanesini](https://huggingface.co/docs/optimum/main/en/intel/index) kullanarak Intel için kuantize edilmiş (quantized) gömme modellerini yükleme desteğine sahiptir.

Optimize edilmiş modeller, minimum doğruluk kaybıyla daha küçük ve daha hızlıdır; [dokümantasyona](https://huggingface.co/docs/optimum/main/en/intel/optimization_inc) ve IntelLabs/fastRAG kütüphanesini kullanan [optimizasyon kılavuzuna](https://huggingface.co/docs/optimum/main/en/intel/optimization_inc) bakabilirsiniz.

Optimizasyon, Xeon® 4. nesil veya daha yeni işlemcilerdeki matematik komutlarına (math instructions) dayanmaktadır.

Kuantize edilmiş modelleri yükleyebilmek ve kullanabilmek için gerekli bağımlılığı kurun: `pip install optimum[exporters] optimum-intel neural-compressor intel_extension_for_pytorch`.

Yükleme, `IntelEmbedding` sınıfı kullanılarak yapılır; kullanımı herhangi bir HuggingFace yerel gömme modeline benzer. Örneğe bakın:

```python
%pip install llama-index-embeddings-huggingface-optimum-intel
```

```python
from llama_index.embeddings.huggingface_optimum_intel import IntelEmbedding

embed_model = IntelEmbedding("Intel/bge-small-en-v1.5-rag-int8-static")
```

```python
embeddings = embed_model.get_text_embedding("Merhaba Dünya!")
print(len(embeddings))
print(embeddings[:5])
```

    384
    [-0.0032782123889774084, -0.013396517373621464, 0.037944991141557693, -0.04642259329557419, 0.027709005400538445]
