# VoyageAI Gömmeleri (Embeddings)

Yeni VoyageAI Gömme modelleri yerel olarak float, int8, binary ve ubinary gömmelerini destekler. Daha fazla ayrıntı için lütfen [buradaki](https://docs.voyageai.com/docs/embeddings) `output_dtype` açıklamasına bakın.

Bu not defterinde, `VoyageAI Embeddings`i farklı `modeller`, `giriş tipleri` (input_types) ve `gömme tipleri` (embedding_types) ile kullanmayı göstereceğiz.

Eğer bu not defterini colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-openai
%pip install llama-index-embeddings-voyageai
```

```python
!pip install llama-index
```

#### En son `voyage-3` gömmeleri ile.

Varsayılan `embedding_type` `float` şeklindedir.

```python
from llama_index.embeddings.voyageai import VoyageEmbedding

# input_typ='search_query' ile
embed_model = VoyageEmbedding(
    voyage_api_key="<VOYAGE_API_ANAHTARINIZ>",
    model_name="voyage-3",
)

embeddings = embed_model.get_text_embedding("Merhaba VoyageAI!")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [-0.010165567509829998, -0.0588739775121212, 0.007418953347951174, 0.004723705351352692, 0.0029206324834376574]

##### `voyage-3-large` modeli ile `int8` gömme tipiini (embedding_type) kontrol edelim

```python
embed_model = VoyageEmbedding(
    voyage_api_key="<VOYAGE_API_ANAHTARINIZ>",
    model_name="voyage-3-large",
    output_dtype="int8",
    truncation=False,
)

embeddings = embed_model.get_text_embedding("Merhaba VoyageAI!")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [-37, 41, 5, -1, 10]

#### `voyage-3-large` gömmelerini derinlemesine inceleyelim

`int8` gömme tipi (embedding_type) ile deneme yapacağız.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from llama_index.llms.openai import OpenAI
from llama_index.core.response.notebook_utils import display_source_node

from IPython.display import Markdown, display
```

#### Veriyi İndir

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

    --2024-12-21 19:28:14--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
    raw.githubusercontent.com (raw.githubusercontent.com) çözülüyor... 2606:50c0:8003::154, 2606:50c0:8000::154, 2606:50c0:8001::154, ...
    bağlanıldı. raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8003::154|:443... 
    200 OK yanıtı alındı... 
    Uzunluk: 75042 (73K) [text/plain]
    Kaydediliyor: ‘data/paul_graham/paul_graham_essay.txt’
    
    data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    0.02s içinde   
    
    2024-12-21 19:28:14 (3.55 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ kaydedildi [75042/75042]

#### Veriyi Yükle

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

### `int8` Gömme Tipi (embedding_type) ile

#### İndeks Oluşturma

```python
llm = OpenAI(
    model="command-nightly",
    api_key="<OPENAI_API_ANAHTARINIZ>",
)
embed_model = VoyageEmbedding(
    voyage_api_key="<VOYAGE_API_ANAHTARINIZ>",
    model_name="voyage-3-large",
    embedding_type="int8",
)

index = VectorStoreIndex.from_documents(
    documents=documents, embed_model=embed_model
)
```

#### Geri Çağırıcı (Retriever) Oluşturma

```python
search_query_retriever = index.as_retriever()

search_query_retrieved_nodes = search_query_retriever.retrieve(
    "1995 yazında ne oldu?"
)
```

```python
for n in search_query_retrieved_nodes:
    display_source_node(n, source_length=2000)
```

**Düğüm (Node) ID:** 1c052573-9fef-4f1b-9882-e69db8b7d62a<br>**Benzerlik:** 0.23402080114051563<br>**Metin:** Kullanıcıların bir tarayıcıdan fazlasına ihtiyacı olmayacaktı.
 
Web uygulaması olarak bilinen bu tür yazılımlar artık yaygın, ancak o zamanlar bunun mümkün olup olmadığı bile belli değildi. Bunu öğrenmek için, tarayıcı üzerinden kontrol edebileceğiniz mağaza oluşturucumuzun bir versiyonunu yapmayı denemeye karar verdik. Birkaç gün sonra, 12 Ağustos'ta çalışan bir tanesine sahiptik. Kullanıcı arayüzü berbattı, ancak herhangi bir istemci yazılımı olmadan veya sunucudaki komut satırına bir şey yazmadan tarayıcı üzerinden bütün bir mağaza oluşturabileceğinizi kanıtladı.
 
Şimdi gerçekten bir şeyler yakalamış gibi hissediyorduk. Bu şekilde çalışan yepyeni bir yazılım nesli hayal ediyordum. Sürümlere, portlara veya bu tür saçmalıklara ihtiyacınız olmayacaktı. Interleaf'te, Release Engineering adında, yazılımı asıl yazan grup kadar büyük görünen bir grup vardı. Artık yazılımı doğrudan sunucu üzerinde güncelleyebilirdiniz.
 
Yazılımımızın web üzerinden çalışması nedeniyle Viaweb adını verdiğimiz yeni bir şirket kurduk ve Idelle'in kocası Julian'dan 10.000 dolarlık tohum yatırımı aldık. Bunun karşılığında ve ilk yasal işleri yapması ve bize iş tavsiyesi vermesi karşılığında ona şirketin %10'unu verdik. On yıl sonra bu anlaşma Y Combinator'ın modeli oldu. Kurucuların böyle bir şeye ihtiyacı olduğunu biliyorduk, çünkü buna kendimiz ihtiyaç duymuştuk.
 
Bu aşamada net değerim negatifti, çünkü bankadaki bin dolarım veya o civardaki param, devlete olan vergi borcumla fazlasıyla dengeleniyordu. (Interleaf için yaptığım danışmanlıktan kazandığım paranın uygun bir kısmını özenle bir kenara ayırmış mıydım? Hayır, ayırmamıştım.) रॉबर्ट'ın lisansüstü öğrenci maaşı olmasına rağmen, benim yaşamak için o tohum yatırımına ihtiyacım vardı.
 
Başlangıçta Eylül ayında yayına girmeyi umuyorduk ama yazılım üzerinde çalıştıkça daha hırslı hale geldik. Sonunda, sayfaları oluştururken daha sonra oluşturulacak statik sayfalar gibi göründükleri anlamında bir WYSIWYG site oluşturucu yapmayı başardık, ancak şu farkla...<br>

**Düğüm (Node) ID:** 43747196-8c04-4b9a-86dc-94f15e310988<br>**Benzerlik:** 0.22620195227632825<br>**Metin:** Hızlı değil, ama test etmek için yeterince hızlı.
 
Bu sürenin çoğunda kendime deneme yazmayı yasaklamak zorunda kaldım, yoksa asla bitiremezdim. 2015'in sonlarında 3 ayımı deneme yazarak geçirdim ve Bel üzerinde çalışmaya geri döndüğümde kodu zar zor anlayabiliyordum. Kötü yazıldığı için değil, problemin çok karmaşık olmasından dolayı. Kendi içinde yazılmış bir yorumlayıcı (interpreter) üzerinde çalışırken, hangi seviyede ne olduğunu takip etmek zordur ve hatalar size ulaştığında pratik olarak şifrelenmiş olabilir.
 
Bu yüzden Bel bitene kadar artık deneme yazmayacağımı söyledim. Ancak üzerinde çalışırken Bel'den az kişiye bahsettim. Bu yüzden yıllarca hiçbir şey yapmıyormuşum gibi görünmüş olmalı, oysa aslında şimdiye kadar herhangi bir şey üzerinde çalıştığımdan daha sıkı çalışıyordum. Bazen saatlerce korkunç bir bug ile boğuştuktan sonra Twitter'a veya HN'ye bakar ve birinin "Paul Graham hala kod yazıyor mu?" diye sorduğunu görürdüm.
 
Bel üzerinde çalışmak zordu ama tatmin ediciydi. O kadar yoğun çalıştım ki, herhangi bir zamanda kodun önemli bir kısmını kafamda tutabiliyor ve orada daha fazlasını yazabiliyordum. 2015'te güneşli bir günde çocukları sahile götürdüğümü ve onlar gelgit havuzlarında oynarken devamlılıkları (continuations) içeren bir sorunu nasıl çözeceğimi bulduğumu hatırlıyorum. Hayatı doğru yaşıyormuşum gibi hissettiriyordu. Bunu hatırlıyorum çünkü ne kadar yeni hissettirdiği beni biraz dehşete düşürmüştü. İyi haber şu ki, sonraki birkaç yıl içinde bu tür anlarım daha fazla oldu.
 
2016 yazında İngiltere'ye taşındık. Çocuklarımızın başka bir ülkede yaşamanın nasıl bir şey olduğunu görmelerini istedik ve doğumdan itibaren İngiliz vatandaşı olduğum için bu bariz bir seçim gibi göründü. Sadece bir yıl kalmayı planlıyorduk ama o kadar çok sevdik ki hala orada yaşıyoruz. Yani Bel'in çoğu İngiltere'de yazıldı.
 
2019 sonbaharında Bel nihayet bitti. McCarthy’nin orijinal Lisp'i gibi, bu bir uygulamadan ziyade bir şartnamedir (spec), ancak McCarthy'nin Lisp'i gibi kod olarak ifade edilmiş bir şartnamedir.
 
Artık tekrar deneme yazabildiğim için, biriktirdiğim konular hakkında bir sürü yazı yazdım. ...<br>

### Metin-Görüntü Gömmeleri (Text-Image Embeddings)

[VoyageAI artık metin ve görüntünün aynı gömme uzayında olduğu çok modlu (multi-modal) gömme modelini destekliyor](https://docs.voyageai.com/docs/multimodal-embeddings).

```python
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open("./data/images/prometheus_paper_card.png")
plt.imshow(img)
```

![png](output_22_1.png)

```python
embed_model = VoyageEmbedding(
    voyage_api_key="<VOYAGE_API_ANAHTARINIZ>",
    model_name="voyage-multimodal-3",
    truncation=False,
)
```

##### Görüntü Gömmeleri

```python
embeddings = embed_model.get_image_embedding(
    "./data/images/prometheus_paper_card.png"
)

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.06298828125, -0.0206298828125, 0.01055908203125, 0.0072021484375, 0.0269775390625]

##### Metin Gömmeleri

```python
embeddings = embed_model.get_text_embedding("prometheus değerlendirme modeli")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.12255859375, -0.0277099609375, 0.028076171875, 0.035888671875, 0.0262451171875]
