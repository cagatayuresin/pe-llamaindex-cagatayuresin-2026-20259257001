# İzleme (Tracing) ve Hata Ayıklama (Debugging)

Uygulamanızın işleyişini izlemek ve hataları ayıklamak, onu anlamak ve optimize etmek için kilit öneme sahiptir. LlamaIndex bunu yapmak için çeşitli yollar sunar.

## Temel Loglama (Basic Logging)

Uygulamanızın ne yaptığını incelemenin mümkün olan en basit yolu, hata ayıklama (debug) loglamasını açmaktır. Bu, uygulamanızın herhangi bir yerinde şu şekilde yapılabilir:

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

## Geri Çağırma Yöneticisi (Callback Handler)

LlamaIndex; kütüphanenin iç işleyişini ayıklamaya, izlemeye ve takip etmeye yardımcı olmak için geri çağırmalar (callbacks) sağlar. Geri çağırma yöneticisini kullanarak, ihtiyaç duyulan sayıda geri çağırma eklenebilir.

Olaylarla (events) ilgili verileri loglamanın yanı sıra, her bir olayın süresini ve oluşma sayısını da takip edebilirsiniz.

Ayrıca, olayların bir iz haritası (trace map) da kaydedilir ve geri çağırmalar bu verileri istedikleri şekilde kullanabilir. Örneğin, `LlamaDebugHandler` varsayılan olarak çoğu işlemden sonra olayların izini (trace) yazdıracaktır.

Basit bir geri çağırma yöneticisini şu şekilde alabilirsiniz:

```python
import llama_index.core

llama_index.core.set_global_handler("simple")
```

Ayrıca [kendi özel geri çağırma yöneticinizi nasıl oluşturacağınızı](/python/framework/module_guides/observability/callbacks) da öğrenebilirsiniz.

## Gözlemlenebilirlik (Observability)

LlamaIndex, üretim ortamında ilkeli LLM uygulamaları oluşturmanıza olanak sağlamak için **tek tıkla gözlemlenebilirlik** sağlar.

Bu özellik, LlamaIndex kütüphanesini ortaklarımız tarafından sunulan güçlü gözlemlenebilirlik/değerlendirme araçlarıyla sorunsuz bir şekilde entegre etmenize olanak tanır. Bir değişkeni bir kez yapılandırdığınızda, aşağıdakiler gibi işlemleri yapabileceksiniz:

-   LLM/komut girdi ve çıktılarını görüntüleme
-   Herhangi bir bileşenin (LLM'ler, embedding'ler) çıktılarının beklendiği gibi performans gösterdiğinden emin olma
-   Hem indeksleme hem de sorgulama için çağrı izlerini (call traces) görüntüleme

Daha fazlasını öğrenmek için [gözlemlenebilirlik dökümanlarımıza](/python/framework/module_guides/observability) göz atın.