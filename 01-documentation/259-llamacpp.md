# LlamaCPP

---
title: LlamaCPP 
 | LlamaIndex OSS Belgeleri
---

Bu kısa not defterinde, LlamaIndex ile [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) kütüphanesinin nasıl kullanılacağını gösteriyoruz.

Bu not defterinde, uygun istem formatlamasıyla birlikte [`Qwen/Qwen2.5-7B-Instruct-GGUF`](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF) modelini kullanıyoruz.

Varsayılan olarak, `model_path` ve `model_url` boş bırakılırsa, `LlamaCPP` modülü llama2-chat-13B modelini yükleyecektir.

## Kurulum

`LlamaCPP`'den en iyi performansı almak için, paketi GPU desteğiyle derlenecek şekilde kurmanız önerilir. Bu şekilde kurulum için tam bir kılavuz [buradadır](https://github.com/abetlen/llama-cpp-python#installation-with-openblas--cublas--clblast--metal).

Tam MACOS talimatları da [buradadır](https://llama-cpp-python.readthedocs.io/en/latest/install/macos/).

Genel olarak:

- CUDA ve bir NVidia GPU'nuz varsa `CuBLAS` kullanın
- M1/M2/M3 işlemcili bir MacBook kullanıyorsanız `METAL` kullanın
- AMD/Intel GPU kullanıyorsanız `CLBLAST` kullanın

Benim için, bir MAC üzerinde `metal` backend'ini kurmam gerekiyor.

Terminal penceresi:

```bash
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python
```

Ardından gerekli llama-index paketlerini kurabilirsiniz:

```bash
%pip install llama-index-embeddings-huggingface
%pip install llama-index-llms-llama-cpp
```

## LLM Kurulumu

LlamaCPP LLM oldukça yapılandırılabilirdir. Kullanılan modele bağlı olarak, model girişlerini formatlamaya yardımcı olması için `messages_to_prompt` ve `completion_to_prompt` fonksiyonlarını iletmek isteyeceksiniz.

Başlatma sırasında iletilmesi gereken tüm anahtar kelime argümanlarını (kwargs) `model_kwargs` içinde ayarlayın. Mevcut model kwargs listesinin tamamına [LlamaCPP belgelerinden](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.llama.Llama.__init__) ulaşılabilir.

Çıkarım (inference) sırasında iletilmesi gereken tüm kwargs'ları `generate_kwargs` içinde ayarlayabilirsiniz. [Buradaki generate kwargs](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.llama.Llama.__call__) listesinin tamamına bakın.

Genel olarak, varsayılanlar harika bir başlangıç noktasıdır. Aşağıdaki örnek, tümü varsayılan olan yapılandırmayı gösterir.

Bu Not Defterini (Notebook) Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
model_url = "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q3_k_m.gguf"
```

```python
from llama_index.llms.llama_cpp import LlamaCPP
from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")




def messages_to_prompt(messages):
    messages = [{"role": m.role.value, "content": m.content} for m in messages]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return prompt




def completion_to_prompt(completion):
    messages = [{"role": "user", "content": completion}]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return prompt




llm = LlamaCPP(
    # Otomatik olarak indirmek için bir GGML modelinin URL'sini verebilirsiniz
    model_url=model_url,
    # isteğe bağlı olarak, model_url yerine önceden indirilmiş bir modelin yolunu ayarlayabilirsiniz
    model_path=None,
    temperature=0.1,
    max_new_tokens=256,
    # llama2'nin 4096 tokentlik bir bağlam penceresi vardır, ancak biz biraz boşluk bırakmak için daha düşük ayarlıyoruz
    context_window=16384,
    # __call__()'a iletilecek kwargs'lar
    generate_kwargs={},
    # __init__()'e iletilecek kwargs'lar
    # GPU kullanmak için en az 1 yapın
    model_kwargs={"n_gpu_layers": -1},
    # girişleri Llama2 formatına dönüştür
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)
```

```
llama_model_load_from_file: using device Metal (Apple M2 Max) - 16584 MiB free
... (günlük çıktıları)
offloaded 29/29 layers to GPU
```

Günlüklerden modelin `metal` ve GPU'muzu kullandığını anlayabiliriz!

## `LlamaCPP` LLM soyutlamamızı kullanmaya başlayın!

Verilen bir isteme (prompt) karşılık tamamlamalar üretmek için `LlamaCPP` LLM soyutlamamızın `complete` yöntemini kullanabiliriz.

```python
response = llm.complete("Merhaba! Bana kediler ve köpekler hakkında bir şiir anlatır mısın?")
print(response.text)
```

```
Kesinlikle! İşte kedilerin ve köpeklerin özelliklerini ve etkileşimlerini harmanlayan kısa bir şiir:

Akşamın sessizliğinde,
Gölgelerin ve ışığın oynaştığı yerde,
İki canlı, her biri bir köşede,
Dünyanın, güçlerini bulurlar içlerinde.

Kedi, zarafet ve gizlilikle,
Karanlıkta atılır ileriye,
Köpek ise sadık dişleriyle,
Korur ve asla düşmez yanılgıya.

Birinin tüyü ipek kadar yumuşak,
Diğerininki keten gibi parlak,
Yine de kalplerinde bir bağ kurulur,
Asla eksilmeyecek bir dostluk doğurur.

Yolları ayrı görünse de,
Kalplerinde bulurlar bir çare,
Barış ve huzur içinde bir arada,
Uyumun ritmiyle, bu masalda.

Bu şiir, hem kedilerin hem de köpeklerin özünü yakalar; onların benzersiz özelliklerini ve aralarındaki dostluk potansiyelini vurgular.
```

Tüm yanıtın oluşturulmasını beklemek yerine, yanıt oluşturulurken akışını sağlamak için `stream_complete` uç noktasını kullanabiliriz.

```python
response_iter = llm.stream_complete("Hızlı arabalar hakkında bana bir şiir yazar mısın?")
for response in response_iter:
    print(response.delta, end="", flush=True)
```

## LlamaCPP ile Sorgu Motoru Kurulumu

`LlamaCPP` LLM soyutlamasını her zamanki gibi `LlamaIndex` sorgu motoruna doğrudan iletebiliriz.

Ancak önce, küresel belirteçleyiciyi (tokenizer) LLM'imizle eşleşecek şekilde değiştirelim.

```python
from llama_index.core import set_global_tokenizer
from transformers import AutoTokenizer


set_global_tokenizer(
    AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct").encode
)
```

```python
# Huggingface gömmelerini (embeddings) kullan
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

```python
from llama_index.core import SimpleDirectoryReader


# belgeleri yükle
documents = SimpleDirectoryReader("../data/paul_graham/").load_data()
```

```python
from llama_index.core import VectorStoreIndex


# vektör deposu dizini oluştur
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
```

```python
# sorgu motorunu kur
query_engine = index.as_query_engine(llm=llm)
```

```python
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

```
Yazar büyürken yazarlık ve programlama üzerine yoğunlaştı. Özellikle üniversiteden önce, başlangıç seviyesinde bir yazar olarak kısa öyküler yazdı; bunların olay örgüsü bakımından zayıf ancak karakter duyguları açısından zengin olduğunu fark etti. Ayrıca okul bölgesinin bodrum katındaki bir IBM 1401 bilgisayarında, Fortran'ın erken bir sürümünü kullanarak programlama yaparak vakit geçirdi. Programları delikli kartlara girmek ve gürültülü bir yazıcıda çalıştırmak zorundaydı. Bu deneyim sınırlıydı ve pek verimli değildi, çünkü girdi verisi olmadan veya daha karmaşık hesaplamalar yapma yeteneği olmadan makineyle yapacak pek bir şey bulamıyordu. Yazar daha sonra mikro bilgisayarlara yöneldi; bu da daha etkileşimli programlama ve yazma imkanı sundu ve tekrar denemeler yazmaya başladı. Daha sonra, Mart 2015'te, bir programlama dili olarak benzersiz özellikleri ve gücü ilginisini çektiği için tekrar Lisp üzerinde çalışmaya başladı.
```
