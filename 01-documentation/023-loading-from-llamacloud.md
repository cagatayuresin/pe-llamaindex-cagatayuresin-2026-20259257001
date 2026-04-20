# LlamaCloud'dan Yükleme

Kurumsal hizmetimiz olan [LlamaCloud](https://cloud.llamaindex.ai/), verilerinizi tamamen yönetilen, ölçeklenebilir ve güvenli bir ortamda saklamanıza ve sorgulamanıza olanak tanır. LlamaCloud'un nasıl kullanılacağına dair tam bir açıklama için [LlamaCloud dökümantasyonuna](https://docs.cloud.llamaindex.ai/) ve özellikle [framework entegrasyon kılavuzuna](https://docs.cloud.llamaindex.ai/llamacloud/guides/framework_integration) göz atın.

## LlamaIndex'ten LlamaCloud Kullanımı

Veri depolarınıza bağlanmak ve onları otomatik olarak indekslemek için LlamaCloud'u kullanabilirsiniz. Bir indeks oluşturulduktan sonra, onu sadece birkaç satır kodla kullanabilirsiniz:

```python
import os
from llama_cloud_services import LlamaCloudIndex

os.environ["LLAMA_CLOUD_API_KEY"] = "llx-..."

index = LlamaCloudIndex("ilk_indeksim", project_name="Default")
query_engine = index.as_query_engine()
answer = query_engine.query("Örnek sorgu")
```

Dökümanları programlı olarak bir LlamaCloud indeksine yüklemek de mümkündür; daha fazla ayrıntı için [dökümantasyonu](https://docs.cloud.llamaindex.ai/llamacloud/guides/framework_integration) kontrol edin.