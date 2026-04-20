# NVIDIA Triton

---
title: NVIDIA Triton
 | LlamaIndex OSS Documentation
---

[NVIDIA Triton Inference Server](https://github.com/triton-inference-server/server) provides a cloud and edge inferencing solution optimized for both CPUs and GPUs. This connector allows LlamaIndex to remotely interact with TensorRT-LLM models deployed with Triton.

## Launch Triton Inference Server

This connector requires a running instance of Triton Inference Server with A TensorRT-LLM model. For this example, we will use a [Triton Command Line Interface (Triton CLI)](https://github.com/triton-inference-server/triton_cli) to deploy a GPT2 model on Triton.

When using Triton and related tools on your host (outside of a Triton container image) there are a number of additional dependencies that may be required for various workflows. Most system dependency issues can be resolved by installing and running the CLI from within the latest corresponding `tritonserver` container image, which should have all necessary system dependencies installed.

For TRT-LLM, you can use `nvcr.io/nvidia/tritonserver:{YY.MM}-trtllm-python-py3` image, where `YY.MM` corresponds to the version of `tritonserver`, for example in this example we’re using 24.02 version of the container. To get the list of available versions, please refer to [Triton Inference Server NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tritonserver).

To start the container, run in your Linux terminal:

```
docker run -ti --gpus all --network=host --shm-size=1g --ulimit memlock=-1 nvcr.io/nvidia/tritonserver:24.02-trtllm-python-py3
```

Next, we’ll need to install dependencies with the following:

```
pip install \
  "psutil" \
  "pynvml>=11.5.0" \
  "torch==2.1.2" \
  "tensorrt_llm==0.8.0" --extra-index-url https://pypi.nvidia.com/
```

Finally, run the following to install Triton CLI.

```
pip install git+https://github.com/triton-inference-server/triton_cli.git
```

To generate the model repository for a GPT2 model and start an instance of Triton Server, run the following commands:

```
triton remove -m all
triton import -m gpt2 --backend tensorrtllm
triton start &
```

By default, Triton listens on `localhost:8000` (HTTP) and `localhost:8001` (gRPC). This example uses the gRPC port.

For more information, refer to the [Triton CLI GitHub repository](https://github.com/triton-inference-server/triton_cli).

## Install tritonclient

Since we are interacting with Triton Inference Server, you need to [install](https://github.com/triton-inference-server/client?tab=readme-ov-file#download-using-python-package-installer-pip) the `tritonclient` package.

```
pip install tritonclient[all]
```

Next, we’ll install llama index connector.

```
pip install llama-index-llms-nvidia-triton
```

## Basic Usage

#### Call `complete` with a prompt

```
from llama_index.llms.nvidia_triton import NvidiaTriton


# A Triton server instance must be running. Use the correct URL for your desired Triton server instance.
triton_url = "localhost:8001"
model_name = "gpt2"
resp = NvidiaTriton(server_url=triton_url, model_name=model_name, tokens=32).complete("The tallest mountain in North America is ")
print(resp)
```

You should expect the following response

```
the Great Pyramid of Giza, which is about 1,000 feet high. The Great Pyramid of Giza is the tallest mountain in North America.
```

#### Call `stream_complete` with a prompt

```
resp = NvidiaTriton(server_url=triton_url, model_name=model_name, tokens=32).stream_complete("The tallest mountain in North America is ")
for delta in resp:
    print(delta.delta, end=" ")
```

You should expect the following response as a stream

```
the Great Pyramid of Giza, which is about 1,000 feet high. The Great Pyramid of Giza is the tallest mountain in North America.
```

## Related

For more information on Triton Inference Server, refer to the following resources:

- [Quickstart guide](https://github.com/triton-inference-server/server/blob/main/docs/getting_started/quickstart.md#quickstart)
- [NVIDIA Developer Triton page](https://developer.nvidia.com/triton-inference-server)
- [GitHub issues](https://github.com/triton-inference-server/server/issues)
