# RAG CLI

Yaygın kullanım durumlarından biri, bilgisayarınızda yerel olarak kayıtlı olan dosyalar hakkında bir LLM ile sohbet etmektir.

Bunu yapmanıza yardımcı olacak bir CLI (komut satırı) aracı yazdık! RAG CLI aracını yerel olarak kaydettiğiniz bir dizi dosyaya yönlendirebilirsiniz; araç bu dosyaları yerel bir vektör veritabanına aktaracak (ingest) ve ardından terminaliniz içinde bir Sohbet Soru-Cevap arayüzü (REPL) için kullanacaktır.

Varsayılan olarak bu araç, gömmeler (embeddings) ve LLM için OpenAI'ı, vektör veritabanı için ise yerel bir Chroma Vector DB örneğini kullanır. **Uyarı**: Bu, varsayılan olarak bu araçla aktardığınız yerel verilerin OpenAI'ın API'sine *gönderileceği* anlamına gelir.

Ancak, bu araçta kullanılan modelleri ve veritabanlarını özelleştirme yeteneğine sahipsiniz. Bu, tüm model yürütme işlemlerini yerel olarak çalıştırma olasılığını da içerir! Aşağıdaki **Özelleştirme** bölümüne bakın.

## Kurulum

CLI aracını kurmak için kütüphaneyi yüklediğinizden emin olun:

`$ pip install -U llama-index`

Ayrıca [Chroma](/python/examples/vector_stores/chromaindexdemo) veritabanını da kurmanız gerekecektir:

`$ pip install -U chromadb`

Bundan sonra aracı kullanmaya başlayabilirsiniz:

```shell
$ llamaindex-cli rag -h
usage: llamaindex-cli rag [-h] [-q QUESTION] [-f FILES [FILES ...]] [-c] [-v] [--clear] [--create-llama]

options:
  -h, --help            bu yardım mesajını gösterir ve çıkar
  -q QUESTION, --question QUESTION
                        Sormak istediğiniz soru.
  -f, --files FILES [FILES ...]
                        Hakkında soru sormak istediğiniz dosya(lar) veya dizinlerin adı,
                        örneğin "dosya.pdf". "*.py" gibi desenleri destekler.
  -c, --chat            Eğer bu bayrak varsa, bir sohbet REPL'i açar.
  -v, --verbose         Yürütme sırasında ayrıntılı bilgi yazdırılıp yazdırılmayacağı.
  --clear               Şu anda gömülü olan tüm verileri temizler.
  --create-llama        Seçilen dosyalara dayalı bir LlamaIndex uygulaması oluşturur.
```

## Kullanım

Başlamanıza yardımcı olacak bazı üst düzey adımlar:

1.  **`OPENAI_API_KEY` ortam değişkenini ayarlayın:** Varsayılan olarak bu araç OpenAI'ın API'sini kullanır. Bu nedenle, aracı her kullandığınızda OpenAI API Anahtarının `OPENAI_API_KEY` ortam değişkeni altında ayarlandığından emin olmanız gerekir.
    ```shell
    $ export OPENAI_API_KEY=<api_anahtari>
    ```
2.  **Bazı dosyaları aktarın (Ingest):** Şimdi, aracı yerel vektör veritabanına aktarabileceği bazı yerel dosyalara yönlendirmeniz gerekiyor. Bu örnek için LlamaIndex `README.md` dosyasını aktaracağız:
    ```shell
    $ llamaindex-cli rag --files "./README.md"
    ```
    Ayrıca aşağıdakine benzer bir dosya deseni de belirtebilirsiniz:
    ```shell
    $ llamaindex-cli rag --files "./docs/**/*.rst"
    ```
3.  **Bir Soru Sorun**: Artık önceki adımda aktardığınız belgelerden herhangi biri hakkında soru sormaya başlayabilirsiniz:
    ```shell
    $ llamaindex-cli rag --question "LlamaIndex nedir?"
    LlamaIndex, LLM tabanlı uygulamalar için özel veya alana özgü verileri aktarmaya, yapılandırmaya ve bunlara erişmeye yardımcı olan bir veri çerçevesidir (data framework). Çeşitli kaynaklardan veri aktarmak için veri bağlayıcıları (data connectors), verileri yapılandırmak için veri indeksleri ve verilere doğal dille erişim için motorlar (engines) gibi araçlar sağlar. LlamaIndex, veri kaynaklarından bilgi getirdiği, bunu bağlam olarak soruya eklediği ve ardından LLM'den zenginleştirilmiş komut istemine (prompt) dayanarak bir cevap oluşturmasını istediği bir RAG (Retrieval-Augmented Generation) yaklaşımını izler. Bu yaklaşım, LLM'leri ince ayar (fine-tuning) yapmanın sınırlamalarını aşar ve veri artırma için daha uygun maliyetli, güncel ve güvenilir bir çözüm sunar. LlamaIndex, hem yeni başlayanlar hem de ileri düzey kullanıcılar için tasarlanmıştır; kolay kullanım için üst düzey bir API ve özelleştirme ile genişletme için alt düzey API'ler sunar.
    ```
4.  **Bir Sohbet REPL'i Açın**: Terminalinizde bir sohbet arayüzü bile açabilirsiniz! Sadece `$ llamaindex-cli rag --chat` komutunu çalıştırın ve aktardığınız dosyalar hakkında soru sormaya başlayın.

### Bir LlamaIndex sohbet uygulaması oluşturun

Seçtiğiniz dosyalara dayanarak FastAPI backend ve NextJS frontend yapısına sahip bir full-stack sohbet uygulaması da oluşturabilirsiniz.

Uygulamayı başlatmak için makinenizde NodeJS ve npx kurulu olduğundan emin olun. Kurulu değilse, talimatlar için lütfen [LlamaIndex.TS](https://ts.llamaindex.ai/docs/llamaindex/getting_started) dökümantasyonuna bakın.

Her şeyi ayarladıktan sonra yeni bir uygulama oluşturmak kolaydır. Aşağıdaki komutu çalıştırmanız yeterlidir:

`$ llamaindex-cli rag --create-llama`

Bu komut `create-llama` aracımızı çağıracaktır, bu nedenle uygulamayı oluşturmak için birkaç bilgi vermeniz gerekecektir. `create-llama` hakkında daha fazla bilgiyi [npmjs - create-llama](https://www.npmjs.com/package/create-llama#example) sayfasında bulabilirsiniz.

```shell
❯ llamaindex-cli rag --create-llama

/tmp/rag-data/... adresindeki veriler kullanılarak create-llama çağrılıyor...

✔ Projenizin adı nedir? … my-app
✔ Hangi modeli kullanmak istersiniz? › gpt-3.5-turbo
✔ Lütfen OpenAI API anahtarınızı girin (atlamak için boş bırakın): …
? Nasıl devam etmek istersiniz? › - Ok tuşlarını kullanın. Göndermek için Enter'a basın.
   Sadece kod oluştur (~1 saniye)
   Kod oluştur ve bağımlılıkları kur (~2 dakika)
❯  Kod oluştur, bağımlılıkları kur ve uygulamayı çalıştır (~2 dakika)
...
```

Eğer `Kod oluştur, bağımlılıkları kur ve uygulamayı çalıştır (~2 dakika)` seçeneğini seçerseniz, tüm bağımlılıklar kurulacak ve uygulama otomatik olarak çalışacaktır. Uygulamaya şu adresten erişebilirsiniz: <http://localhost:3000>.

### Desteklenen Dosya Türleri

Dahili olarak, `rag` CLI aracı yerel dosya sisteminizdeki ham dosyaları dizelere dönüştürmek için [SimpleDirectoryReader](/python/framework/module_guides/loading/simpledirectoryreader) modülünü kullanır.

Bu modül, çok çeşitli dosya türleri için özel okuyuculara sahiptir. Bunlardan bazıları, belirli bir dosya türünü ayrıştırmak için gereken başka bir modülü `pip install` ile kurmanızı gerektirebilir.

Eğer `SimpleDirectoryReader`'ın özel bir okuyucusuna sahip olmadığı bir dosya uzantısıyla karşılaşılırsa, dosyayı sadece düz metin dosyası olarak okuyacaktır.

Kendi özel dosya okuyucularınızı nasıl ekleyeceğiniz ve CLI aracının diğer yönlerini nasıl özelleştireceğiniz hakkında bilgi için sonraki bölüme bakın!

## Özelleştirme

`rag` CLI aracı son derece özelleştirilebilirdir! Araç, [`RagCLI`](https://github.com/run-llama/llama_index/blob/main/llama-index-cli/llama_index/cli/rag/base.py) modülü içindeki [`IngestionPipeline`](/python/framework/module_guides/loading/ingestion_pipeline) modülünün birleştirilmesiyle güçlendirilmiştir.

Kendi özel RAG CLI aracınızı oluşturmak için, kendiniz yapılandırdığınız bir `IngestionPipeline` ile `RagCLI` sınıfını başlatan bir betik oluşturmanız yeterlidir. Buradan, kendi seçtiğiniz embedding modellerine, LLM'lere, vektör veritabanlarına vb. karşı aynı aktarım ve Soru-Cevap komutlarını çalıştırmak için betiğinizde `rag_cli_instance.cli()` komutunu çalıştırmanız yeterlidir.

İşte genel kurulumu gösteren bazı üst düzey kodlar:

```python
#!/path/to/your/virtualenv/bin/python
import os
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.cli.rag import RagCLI


# isteğe bağlı, betiğinizin ihtiyaç duyabileceği API anahtarlarını ayarlayın (belki bunun yerine python-dotenv kütüphanesini kullanabilirsiniz)
os.environ["OPENAI_API_KEY"] = "sk-xxx"

docstore = SimpleDocumentStore()

vec_store = ...  # vektör deposu örneğiniz
llm = ...  # LLM örneğiniz - isteğe bağlı, varsayılan olarak OpenAI gpt-3.5-turbo olacaktır

custom_ingestion_pipeline = IngestionPipeline(
    transformations=[...],
    vector_store=vec_store,
    docstore=docstore,
    cache=IngestionCache(),
)

# ek dosya türlerini desteklemek için opsiyonel olarak kendi özel okuyucularınızı belirtebilirsiniz.
file_extractor = {".html": ...}

rag_cli_instance = RagCLI(
    ingestion_pipeline=custom_ingestion_pipeline,
    llm=llm,  # isteğe bağlı
    file_extractor=file_extractor,  # isteğe bağlı
)

if __name__ == "__main__":
    rag_cli_instance.cli()
```

Buradan, özel CLI betiğinizi kullanabilmek için sadece birkaç adım kalmıştır:

1.  En üstteki Python yolunu, sanal ortamınızın kullandığı yol ile değiştirdiğinizden emin olun *(sanal ortamınız etkinken `$ which python` komutunu çalıştırın)*.
2.  Betiğinizi `/path/to/your/script/my_rag_cli.py` adresine kaydettiğinizi varsayalım. Buradan, kabuğunuzun yapılandırma dosyasını *(örneğin `.bashrc` veya `.zshrc`)* `$ export PATH="/path/to/your/script:$PATH"` benzeri bir satırla düzenleyebilirsiniz.
3.  Ardından, dosyaya yürütme izinleri vermek için `$ chmod +x my_rag_cli.py` komutunu çalıştırın.
4.  İşte bu kadar! Artık yeni bir terminal oturumu açıp `$ my_rag_cli.py -h` komutunu çalıştırabilirsiniz. Betiği aynı parametrelerle ancak kendi özel kod yapılandırmalarınızla çalıştırabilirsiniz!
    - Not: Komutu sadece `$ my_rag_cli --chat` şeklinde çalıştırmak isterseniz `my_rag_cli.py` dosyanızdan `.py` uzantısını kaldırabilirsiniz.