# Llama Packs 🦙📦

## Kavram

Llama Pack'ler (Llama Paketleri), LLM uygulamanızı başlatmak için kullanabileceğiniz **önceden paketlenmiş modüller/şablonlardan** oluşan topluluk odaklı bir merkezdir.

Bu, LLM uygulamaları oluşturmadaki büyük bir sorunu doğrudan ele alır; her kullanım durumu, özel bileşenlerin bir araya getirilmesini ve çok fazla ince ayar/geliştirme süresi gerektirir. Amacımız, topluluk liderliğindeki bir çabayla bunu hızlandırmaktır.

İki şekilde kullanılabilirler:

-   Bir yandan, parametrelerle başlatılabilen ve belirli bir kullanım durumuna (tam bir RAG akışı, uygulama şablonu veya daha fazlası) ulaşmak için kutudan çıktığı gibi çalıştırılabilen **önceden paketlenmiş modüllerdir**. Ayrıca doğrudan kullanmak için alt modülleri (örneğin LLM'ler, sorgu motorları) içe aktarabilirsiniz.
-   Öte yandan LlamaPack'ler, inceleyebileceğiniz, değiştirebileceğiniz ve kullanabileceğiniz **şablonlardır**.

**Tüm paketler [LlamaHub](https://llamahub.ai/) üzerinde bulunur.** Açılır menüye gidin ve paketlere göre filtrelemek için "LlamaPacks"i seçin.

**Nasıl kullanılacağına dair ayrıntılar için lütfen her paketin README dosyasına bakın.** [Örnek paket burada](https://llamahub.ai/l/llama_packs-voyage_query_engine).

Daha fazla ayrıntı için [lansman blog yazımıza](https://blog.llamaindex.ai/introducing-llama-packs-e14f453b913a) bakın.

## Kullanım Kalıbı

Llama Pack'leri CLI veya Python aracılığıyla kullanabilirsiniz.

CLI:

```bash
llamaindex-cli download-llamapack <pack_name> --download-dir <pack_directory>
```

Python:

```python
from llama_index.core.llama_pack import download_llama_pack

# bağımlılıkları indir ve kur
pack_cls = download_llama_pack("<paket_adi>", "<paket_dizini>")
```

Paketi, modülleri incelemek, uçtan uca (e2e) çalıştırmak veya şablonları özelleştirmek için farklı şekillerde kullanabilirsiniz.

```python
# her paket farklı argümanlarla başlatılır
pack = pack_cls(*args, **kwargs)

# modülleri al
modules = pack.get_modules()
display(modules)

# çalıştır (her paketin farklı argümanları olacaktır)
output = pack.run(*args, **kwargs)
```

Önemli olan, kaynak dosyaları incelemek/özelleştirmek için `pack_directory` (paket dizini) içine de gidebilmeniz/gitmeniz gerektiğidir. İşin püf noktası zaten budur!

## Modül Kılavuzları

Bazı örnek modül kılavuzları aşağıda verilmiştir. Unutmayın, paketlerin tam listesine erişmek için [LlamaHub](https://llamahub.ai) adresine gidin.

-   [LlamaPacks Örneği](/python/examples/llama_hub/llama_packs_example)
-   [Özgeçmiş (Resume) LlamaPack](/python/examples/llama_hub/llama_pack_resume)
-   [Ollama LlamaPack](/python/examples/llama_hub/llama_pack_ollama)