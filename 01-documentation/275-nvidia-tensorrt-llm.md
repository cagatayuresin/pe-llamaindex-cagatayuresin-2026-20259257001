# NVIDIA TensorRT-LLM

---
title: NVIDIA TensorRT-LLM
 | LlamaIndex OSS Belgeleri
---

TensorRT-LLM, büyük dil modellerini (LLM'ler) tanımlamak ve NVIDIA GPU'larda çıkarımı (inference) verimli bir şekilde gerçekleştirmek için en son optimizasyonları içeren TensorRT motorları oluşturmak için kullanımı kolay bir Python API'si sağlar.

Daha fazla bilgi için [TensorRT-LLM GitHub deposuna](https://github.com/NVIDIA/TensorRT-LLM) bakın.

## TensorRT-LLM ortam kurulumu

TensorRT-LLM, yerel modellerle işlem içinde etkileşim kurmak için bir SDK olduğundan, TensorRT-LLM'in kullanılabilmesini sağlamak için izlenmesi gereken birkaç ortam adımı vardır. TensorRT-LLM'i çalıştırmak için NVIDIA CUDA 12.2 veya üzeri gereklidir.

Bu öğreticide, bağlayıcının GPT2 modeliyle nasıl kullanılacağını göstereceğiz. En iyi deneyim için resmi [TensorRT-LLM Github](https://github.com/NVIDIA/TensorRT-LLM) sayfasındaki [Kurulum](https://github.com/NVIDIA/TensorRT-LLM/tree/v0.8.0?tab=readme-ov-file#installation) sürecini takip etmenizi öneririz.

Aşağıdaki adımlar, x86\_64 kullanıcıları için TensorRT-LLM v0.8.0 ile modelinizi nasıl kuracağınızı göstermektedir.

1. Temel docker imaj ortamını edinin ve başlatın.

```bash
docker run --rm --runtime=nvidia --gpus all --entrypoint /bin/bash -it nvidia/cuda:12.1.0-devel-ubuntu22.04
```

2. Bağımlılıkları kurun, TensorRT-LLM Python 3.10 gerektirir.

```bash
apt-get update && apt-get -y install python3.10 python3-pip openmpi-bin libopenmpi-dev git git-lfs wget
```

3. TensorRT-LLM'in en son kararlı sürümünü (yayın dalına karşılık gelen) kurun. Biz 0.8.0 sürümünü kullanıyoruz, ancak en güncel yayın için lütfen [resmi yayın sayfasına](https://github.com/NVIDIA/TensorRT-LLM/releases) bakın.

```bash
pip3 install tensorrt_llm==0.8.0 -U --extra-index-url https://pypi.nvidia.com
```

4. Kurulumu kontrol edin.

```bash
python3 -c "import tensorrt_llm"
```

Yukarıdaki komut herhangi bir hata üretmemelidir.

5. Bu örnek için GPT2 kullanacağız. GPT2 model dosyalarının, [buradaki](https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/gpt#usage) talimatları izleyerek betikler aracılığıyla oluşturulması gerekir.

   - İlk olarak, 1. aşamada başlattığımız konteynerin içinde TensorRT-LLM deposunu klonlayın:

   ```bash
   git clone --branch v0.8.0 https://github.com/NVIDIA/TensorRT-LLM.git
   ```

   - GPT2 modeli için gereksinimleri şu komutla kurun:

   ```bash
   cd TensorRT-LLM/examples/gpt/ && pip install -r requirements.txt
   ```

   - HuggingFace GPT2 modelini indirin:

   ```bash
   rm -rf gpt2 && git clone https://huggingface.co/gpt2-medium gpt2
   cd gpt2
   rm pytorch_model.bin model.safetensors
   wget -q https://huggingface.co/gpt2-medium/resolve/main/pytorch_model.bin
   cd ..
   ```

   - Ağırlıkları HF Transformers formatından TensorRT-LLM formatına dönüştürün:

   ```bash
   python3 hf_gpt_convert.py -i gpt2 -o ./c-model/gpt2 --tensor-parallelism 1 --storage-type float16
   ```

   - TensorRT motorunu oluşturun (Build):

   ```bash
   python3 build.py --model_dir=./c-model/gpt2/1-gpu --use_gpt_attention_plugin --remove_input_padding
   ```

6. `llama-index-llms-nvidia-tensorrt` paketini kurun.

```bash
pip install llama-index-llms-nvidia-tensorrt
```

## Temel kullanım

### Bir istem (prompt) ile `complete` çağrısı

```python
from llama_index.llms.nvidia_tensorrt import LocalTensorRTLLM


llm = LocalTensorRTLLM(
    model_path="./engine_outputs",
    engine_name="gpt_float16_tp1_rank0.engine",
    tokenizer_dir="gpt2",
    max_new_tokens=40,
)


resp = llm.complete("Harry Potter kimdir?")
print(str(resp))
```

Beklenen yanıt şuna benzemelidir:

```
Harry Potter, J.K. Rowling tarafından ilk romanı Harry Potter ve Felsefe Taşı'nda yaratılan kurgusal bir karakterdir. Karakter, kurgusal bir kasabada yaşayan bir büyücüdür#
```
