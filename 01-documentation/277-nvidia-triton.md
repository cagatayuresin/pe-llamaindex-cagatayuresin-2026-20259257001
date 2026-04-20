# NVIDIA Triton

---
title: NVIDIA Triton
 | LlamaIndex OSS Belgeleri
---

[NVIDIA Triton Çıkarım Sunucusu](https://github.com/triton-inference-server/server), hem CPU'lar hem de GPU'lar için optimize edilmiş bir bulut ve uç çıkarım çözümü sunar. Bu bağlayıcı, LlamaIndex'in Triton ile dağıtılmış TensorRT-LLM modelleriyle uzaktan etkileşim kurmasını sağlar.

## Triton Çıkarım Sunucusunu Başlatma

Bu bağlayıcı, TensorRT-LLM modeliyle çalışan bir Triton Çıkarım Sunucusu örneği gerektirir. Bu örnek için, Triton üzerinde bir GPT2 modeli dağıtmak üzere [Triton Komut Satırı Arayüzü'nü (Triton CLI)](https://github.com/triton-inference-server/triton_cli) kullanacağız.

Triton ve ilgili araçları ana makinenizde (bir Triton konteyner imajının dışında) kullanırken, çeşitli iş akışları için gerekli olabilecek bazı ek bağımlılıklar vardır. Çoğu sistem bağımlılığı sorunu, CLI'yı gerekli tüm sistem bağımlılıklarının kurulu olması gereken en son ilgili `tritonserver` konteyner imajı içinden kurarak ve çalıştırarak çözülebilir.

TRT-LLM için, `YY.MM`'nin `tritonserver` sürümüne karşılık geldiği `nvcr.io/nvidia/tritonserver:{YY.MM}-trtllm-python-py3` imajını kullanabilirsiniz; örneğin bu örnekte konteynerin 24.02 sürümünü kullanıyoruz. Mevcut sürümlerin listesini almak için lütfen [Triton Inference Server NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tritonserver) sayfasına bakın.

Konteyneri başlatmak için Linux terminalinizde çalıştırın:

```bash
docker run -ti --gpus all --network=host --shm-size=1g --ulimit memlock=-1 nvcr.io/nvidia/tritonserver:24.02-trtllm-python-py3
```

Ardından, bağımlılıkları aşağıdakilerle kurmamız gerekecek:

```bash
pip install \
  "psutil" \
  "pynvml>=11.5.0" \
  "torch==2.1.2" \
  "tensorrt_llm==0.8.0" --extra-index-url https://pypi.nvidia.com/
```

Son olarak, Triton CLI'yı kurmak için aşağıdakini çalıştırın.

```bash
pip install git+https://github.com/triton-inference-server/triton_cli.git
```

Bir GPT2 modeli için model deposunu oluşturmak ve bir Triton Sunucusu örneği başlatmak için aşağıdaki komutları çalıştırın:

```bash
triton remove -m all
triton import -m gpt2 --backend tensorrtllm
triton start &
```

Varsayılan olarak Triton, `localhost:8000` (HTTP) ve `localhost:8001` (gRPC) üzerinden dinler. Bu örnek gRPC portunu kullanır.

Daha fazla bilgi için [Triton CLI GitHub deposuna](https://github.com/triton-inference-server/triton_cli) bakın.

## tritonclient Kurulumu

Triton Çıkarım Sunucusu ile etkileşim kurduğumuz için `tritonclient` paketini [kurmanız](https://github.com/triton-inference-server/client?tab=readme-ov-file#download-using-python-package-installer-pip) gerekir.

```bash
pip install tritonclient[all]
```

Daha sonra LlamaIndex bağlayıcısını kuracağız.

```bash
pip install llama-index-llms-nvidia-triton
```

## Temel Kullanım

#### Bir istem (prompt) ile `complete` çağrısı

```python
from llama_index.llms.nvidia_triton import NvidiaTriton


# Bir Triton sunucu örneği çalışıyor olmalıdır. İstenen Triton sunucu örneği için doğru URL'yi kullanın.
triton_url = "localhost:8001"
model_name = "gpt2"
resp = NvidiaTriton(server_url=triton_url, model_name=model_name, tokens=32).complete("Kuzey Amerika'daki en yüksek dağ ")
print(resp)
```

Şu şekilde bir yanıt beklemelisiniz:

```
yaklaşık 1.000 fit yüksekliğindeki Giza'nın Büyük Piramidi'dir. Giza'nın Büyük Piramidi Kuzey Amerika'daki en yüksek dağdır. (Not: Bu model çıktıları halüsinasyon içerebilir.)
```

#### Bir istem ile `stream_complete` çağrısı

```python
resp = NvidiaTriton(server_url=triton_url, model_name=model_name, tokens=32).stream_complete("Kuzey Amerika'daki en yüksek dağ ")
for delta in resp:
    print(delta.delta, end=" ")
```

Yanıtın bir akış olarak gelmesini beklemelisiniz.

## İlgili Kaynaklar

Triton Çıkarım Sunucusu hakkında daha fazla bilgi için aşağıdaki kaynaklara bakın:

- [Hızlı başlangıç kılavuzu](https://github.com/triton-inference-server/server/blob/main/docs/getting_started/quickstart.md#quickstart)
- [NVIDIA Developer Triton sayfası](https://developer.nvidia.com/triton-inference-server)
- [GitHub sorunları (Issues)](https://github.com/triton-inference-server/server/issues)
