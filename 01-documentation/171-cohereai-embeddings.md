# CohereAI Embedding'leri

Cohere Embed; float, int8, binary ve ubinary embedding'lerini yerel olarak destekleyen ilk embedding modelidir.

1. v3 modelleri tüm embedding türlerini desteklerken, v2 modelleri yalnızca `float` embedding türünü destekler.
2. `LlamaIndex` ile varsayılan `embedding_type` (embedding türü) `float`'tur. v3 modelleri için `embedding_type` parametresini kullanarak bunu özelleştirebilirsiniz.

Bu not defterinde, farklı `models`, `input_types` ve `embedding_types` ile `Cohere Embeddings` kullanımını göstereceğiz.

Cohere int8 ve binary Embedding'leri hakkında daha fazla ayrıntı için [ana blog yazılarına](https://txt.cohere.com/int8-binary-embeddings/) bakın.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
%pip install llama-index-llms-cohere
%pip install llama-index-embeddings-cohere
```

```python
!pip install llama-index
```

```python
# API anahtarınızla başlatın
import os

cohere_api_key = "COHERE API ANAHTARINIZ"
os.environ["COHERE_API_KEY"] = cohere_api_key
```

#### En yeni `embed-english-v3.0` embedding'leri ile.

-   input_type="search_document": Bunu vektör veritabanınızda saklamak istediğiniz metinler (dökümanlar) için kullanın.
-   input_type="search_query": Bunu vektör veritabanınızdaki en alakalı dökümanları bulmak amacıyla kullanılan arama sorguları için kullanın.

Varsayılan `embedding_type` `float`'tur.

```python
from llama_index.embeddings.cohere import CohereEmbedding

# input_type='search_query' ile
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
)

embeddings = embed_model.get_text_embedding("Merhaba CohereAI!")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [-0.041931152, -0.022384644, -0.07067871, -0.011886597, -0.019210815]

```python
# input_type = 'search_document' ile
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_document",
)

embeddings = embed_model.get_text_embedding("Merhaba CohereAI!")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [-0.03074646, -0.0029201508, -0.058044434, -0.015457153, -0.02331543]

##### `int8` embedding_type ile kontrol edelim

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    embedding_type="int8",
)

embeddings = embed_model.get_text_embedding("Merhaba CohereAI!")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [-54, -29, -90, -16, -25]

##### `binary` embedding_type ile

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    embedding_type="binary",
)

embeddings = embed_model.get_text_embedding("Merhaba CohereAI!")

print(len(embeddings))
print(embeddings[:5])
```

    128
    [-127, -38, 66, 83, 89]

#### Eski `embed-english-v2.0` embedding'leri ile.

v2 modelleri varsayılan olarak `float` embedding_type'ını destekler.

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key, model_name="embed-english-v2.0"
)

embeddings = embed_model.get_text_embedding("Merhaba CohereAI!")

print(len(embeddings))
print(embeddings[:5])
```

    4096
    [0.65771484, 0.7998047, 2.3769531, -2.3105469, -1.6044922]

#### Şimdi en yeni `embed-english-v3.0` embedding'leri ile,

Şunları kullanalım:
1. İndeks oluşturmak için input_type=`search_document`
2. İlgili bağlamı getirmek için input_type=`search_query`

`int8` embedding_type'ı ile deneme yapacağız.

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from llama_index.llms.cohere import Cohere
from llama_index.core.response.notebook_utils import display_source_node

from IPython.display import Markdown, display
```

#### Veriyi İndir

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Veriyi Yükle

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

### `int8` embedding_type ile

#### input_type = 'search_document' ile indeks oluşturma

```python
llm = Cohere(model="command-nightly", api_key=cohere_api_key)
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_document",
    embedding_type="int8",
)

index = VectorStoreIndex.from_documents(
    documents=documents, embed_model=embed_model
)
```

#### input_type = 'search_query' ile erişici (retriever) oluşturma

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    embedding_type="int8",
)

search_query_retriever = index.as_retriever()

search_query_retrieved_nodes = search_query_retriever.retrieve(
    "1995 yazında ne oldu?"
)
```

```python
for n in search_query_retrieved_nodes:
    display_source_node(n, source_length=2000)
```

**Düğüm (Node) ID:** 0f821a16-5242-4284-86ba-23b16069e071<br>**Benzerlik:** 0.30740912992211505<br>**Metin:** Cambridge'de sahip olduğum binayı merkezimiz olarak kullanacaktık. Haftada bir kez — Salı günleri, çünkü Perşembe akşamı yemek yiyenler için zaten Perşembe günleri yemek pişiriyordum — orada hep birlikte akşam yemeği yiyecektik ve yemekten sonra konuşma yapmaları için girişim uzmanları getirecektik.

Üniversite öğrencilerinin o zamanlar yaz işleri hakkında karar verdiklerini biliyorduk, bu yüzden birkaç gün içinde Summer Founders Program adını verdiğimiz bir şey hazırladık ve sitemde öğrencileri başvurmaya davet eden bir duyuru yayınladım. Makale yazmanın, yatırımcıların deyimiyle "anlaşma akışı" (deal flow) elde etmenin bir yolu olacağını hiç hayal etmemiştim ama mükemmel bir kaynak olduğu ortaya çıktı. [15] Summer Founders Program için 225 başvuru aldık ve birçoğunun zaten mezun olmuş veya o bahar mezun olmak üzere olan kişilerden geldiğini görünce şaşırdık. Zaten bu SFP işi niyetlediğimizden daha ciddi bir hal almaya başlamıştı.

225 gruptan yaklaşık 20'sini şahsen görüşmeye davet ettik ve bunlar arasından fon sağlamak için 8'ini seçtik. Etkileyici bir gruptular. O ilk grupta reddit, daha sonra Twitch'i kuracak olan Justin Kan ve Emmett Shear, RSS özelliğinin yazılmasına çoktan yardım etmiş olan ve birkaç yıl sonra açık erişim için bir şehit haline gelecek olan Aaron Swartz ve daha sonra YC'nin ikinci başkanı olacak olan Sam Altman vardı. İlk grubun bu kadar iyi olmasının tamamen şans olduğunu düşünmüyorum. Microsoft veya Goldman Sachs gibi meşru bir yerdeki yaz işi yerine Summer Founders Program gibi tuhaf bir şeye kaydolmak için oldukça cesur olmanız gerekiyordu.

Girişimler için yapılan anlaşma, Julian ile yaptığımız anlaşmanın bir kombinasyonuna ($10 bin karşılığında %10) ve Robert'ın MIT yüksek lisans öğrencilerinin yaz için ne aldığını söylediği miktara ($6 bin) dayanıyordu. Kurucu başına $6 bin yatırım yaptık, bu da tipik bir iki kuruculu vaka için %6 karşılığında $12 bin demekti. Bu adil olmalıydı çünkü kendi aldığımız anlaşmadan iki kat daha iyiydi. Ayrıca o gerçekten sıcak geçen ilk yaz boyunca Jessica kuruculara ücretsiz klimalar getirdi. [16]

Oldukça hızlı bir şekilde fark ettim ki...<br>

**Düğüm (Node) ID:** 15e1050d-38f1-4c7c-a169-ef9fe4ab1249<br>**Benzerlik:** 0.3000104724138056<br>**Metin:** Sadece bir avuç dolusu çalışanı olan bir şirket amatörce görünürdü. Bu yüzden, 1998 yazında Yahoo bizi satın alana kadar başa baş noktasına (breakeven) ulaşamadık. Bu da şirketin tüm ömrü boyunca yatırımcıların insafına kaldığımız anlamına geliyordu. Hem biz hem de yatırımcılarımız girişimler konusunda acemi olduğumuz için, sonuç girişim standartlarına göre bile bir karmaşaydı.

Yahoo bizi satın aldığında büyük bir rahatlama oldu. Prensipte Viaweb hisselerimiz değerliydi. Kârlı ve hızla büyüyen bir işletmedeki hisselerdi. Ama bana pek değerli gelmiyordu; bir işletmeye nasıl değer biçileceği hakkında hiçbir fikrim yoktu ama birkaç ayda bir yaşadığımız ölüme yakın deneyimlerin fazlasıyla farkındaydım. Başladığımızdan beri yüksek lisans öğrencisi yaşam tarzımı da önemli ölçüde değiştirmemiştim. Bu yüzden Yahoo bizi satın aldığında kendimi fakirlikten zenginliğe geçmiş gibi hissettim. Kaliforniya'ya gideceğimiz için bir araba satın aldım, sarı bir 1998 VW GTI. Sadece deri koltuklarının bile o zamana kadar sahip olduğum en lüks şey olduğunu düşündüğümü hatırlıyorum.

Ertesi yıl, 1998 yazından 1999 yazına kadar olan süre, hayatımın muhtemelen en verimsiz dönemiydi. O zaman fark etmemiştim ama Viaweb'i yönetmenin çabasından ve stresinden tükenmiştim. Kaliforniya'ya gittikten bir süre sonra, sabaha karşı 3'e kadar programlama yapma şeklindeki olağan çalışma tarzımı sürdürmeye çalıştım ama yorgunluk, Yahoo'nun erkenden yaşlanmış kültürü ve Santa Clara'daki kasvetli ofis bölmeleriyle (cube farm) birleşince yavaş yavaş beni aşağı çekti. Birkaç ay sonra kendimi huzursuz edici bir şekilde Interleaf'te çalışıyormuş gibi hissettim.

Yahoo bizi satın aldığında bize çok sayıda opsiyon vermişti. O zamanlar Yahoo'nun o kadar aşırı değerli olduğunu düşünüyordum ki asla bir değeri olmayacaktı ama hayretle gördüm ki hisse senetli takip eden yıl içinde 5 kat arttı. Opsiyonların ilk kısmı hak edilene (vest) kadar bekledim, sonra 1999 yazında ayrıldım. Bir şeyler boyamayalı o kadar uzun zaman olmuştu ki bunu neden yaptığımı yarı yarıya unutmuştum. Beynim 4 yıl boyunca tamamen yazılım ve erkek gömlekleriyle doluydu. Ama bunu zengin olmak için yapmıştım bu yüzden...<br>

### `float` embedding_type ile

#### input_type = 'search_document' ile indeks oluşturma

```python
llm = Cohere(model="command-nightly", api_key=cohere_api_key)
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_document",
    embedding_type="float",
)

index = VectorStoreIndex.from_documents(
    documents=documents, embed_model=embed_model
)
```

#### input_type = 'search_query' ile erişici (retriever) oluşturma

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    embedding_type="float",
)

search_query_retriever = index.as_retriever()

search_query_retrieved_nodes = search_query_retriever.retrieve(
    "1995 yazında ne oldu?"
)
```

```python
for n in search_query_retrieved_nodes:
    display_source_node(n, source_length=2000)
```

**Düğüm (Node) ID:** cff8a942-2e1a-4921-ac08-8355b49fde85<br>**Benzerlik:** 0.3051793987443398<br>**Metin:** Cambridge'de sahip olduğum binayı merkezimiz olarak kullanacaktık. Haftada bir kez — Salı günleri, çünkü Perşembe akşamı yemek yiyenler için zaten Perşembe günleri yemek pişiriyordum — orada hep birlikte akşam yemeği yiyecektik ve yemekten sonra konuşma yapmaları için girişim uzmanları getirecektik.

... (yukarıdaki metinle aynı) ...

**Düğüm (Node) ID:** 1810afad-3817-447c-a194-859601437923<br>**Benzerlik:** 0.2959499578848539<br>**Metin:** Sadece bir avuç dolusu çalışanı olan bir şirket amatörce görünürdü. Bu yüzden, 1998 yazında Yahoo bizi satın alana kadar başa baş noktasına ulaşamadık.

... (yukarıdaki metinle aynı) ...

### `binary` embedding_type ile.

#### input_type = 'search_document' ile indeks oluşturma

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_document",
    embedding_type="binary",
)

index = VectorStoreIndex.from_documents(
    documents=documents, embed_model=embed_model
)
```

#### input_type = 'search_query' ile erişici (retriever) oluşturma

```python
embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    embedding_type="binary",
)

search_query_retriever = index.as_retriever()

search_query_retrieved_nodes = search_query_retriever.retrieve(
    "1995 yazında ne oldu?"
)
```

```python
for n in search_query_retrieved_nodes:
    display_source_node(n, source_length=2000)
```

**Düğüm (Node) ID:** fd8e185d-7c9e-40de-8d3e-09a76ae85e18<br>**Benzerlik:** 0.3498979255746315<br>**Metin:** Zamanında editör, en iyi genel amaçlı site oluşturuculardan biriydi. Kodun bütünlüğünü korudum ve Robert ile Trevor'ınkiler dışındaki hiçbir yazılımla entegre etmek zorunda kalmadım, bu yüzden üzerinde çalışmak oldukça eğlenceliydi. Tek yapmam gereken bu yazılım üzerinde çalışmak olsaydı, sonraki 3 yıl hayatımın en kolay yılları olurdu. Ne yazık ki çok daha fazlasını yapmak zorundaydım, bunların hepsi programlamadan daha kötü olduğum şeylerdi ve sonraki 3 yıl bunun yerine en stresli yıllarım oldu.

90'ların ikinci yarısında e-ticaret yazılımı yapan bir sürü girişim vardı. Biz Interleaf değil, Microsoft Word olmaya kararlıydık. Bu da kullanımı kolay ve ucuz olmak anlamına geliyordu. Fakir olmamız bizim için bir şanstı çünkü bu Viaweb'i fark ettiğimizden bile daha ucuz yapmamıza neden oldu. Küçük bir mağaza için ayda $100, büyük bir mağaza içinse ayda $300 ücret alıyorduk. Bu düşük fiyat büyük bir ilgi odağıydı ve rakiplerin ayaklarına takılan sürekli bir dikendi, ancak fiyatı düşük belirlememiz akıllıca bir içgörü sayesinde olmamıştı. İşletmelerin bir şeyler için ne ödediği hakkında hiçbir fikrimiz yoktu. Ayda $300 bize çok para gibi görünüyordu.

Bunun gibi pek çok şeyi yanlışlıkla doğru yaptık. Örneğin, şimdi "ölçeklenmeyen şeyleri yapmak" (doing things that don't scale) olarak adlandırılan şeyi yaptık, ancak o zamanlar bunu "kullanıcı edinmek için en çaresiz önlemlere sürüklenecek kadar ezik olmak" olarak tanımlardık. Bunların en yaygını onlar için mağazalar inşa etmekti. Bu özellikle aşağılayıcı görünüyordu çünkü yazılımımızın tüm varlık nedeni insanların onu kendi mağazalarını yapmak için kullanabilmesiydi. Ama kullanıcı edinmek için her şeyi yapardık.

Perakende hakkında bilmek istediğimizden çok daha fazlasını öğrendik. Örneğin, bir erkek gömleğinin yalnızca küçük bir görüntüsüne sahip olabiliyorsanız (ve o zamanlar tüm görüntüler bugünkü standartlara göre küçüktü), tüm gömleğin resmindense yakanın yakın çekimine sahip olmanın daha iyi olduğunu öğrendik. Bunu öğrendiğimi hatırlamamın sebebi, erkek gömleklerine ait yaklaşık 30 resmi yeniden taramam gerektiği anlamına gelmesiydi. İlk tarama setim de çok güzeldi.

...<br>

**Düğüm (Node) ID:** b013216a-1c23-46b6-ba78-aaeed21b2fe2<br>**Benzerlik:** 0.3376224194936838<br>**Metin:** Ancak yazın yaklaşık yarısında bir şirket yönetmeyi gerçekten istemediğimi fark ettim — özellikle de bunun olması gerektiği gibi görünen büyük bir şirket. Viaweb'e sadece paraya ihtiyacım olduğu için başlamıştım. Artık paraya ihtiyacım olmadığına göre bunu neden yapıyordum? Eğer bu vizyonun bir şirket olarak gerçekleştirilmesi gerekiyorsa, o vizyon batsın (screw the vision). Açık kaynaklı bir proje olarak yapılabilecek bir alt küme inşa ederdim.

Şaşırtıcı bir şekilde, bu şeyler üzerinde harcadığım zaman boşa gitmemişti. Y Combinator'a başladıktan sonra, bu yeni mimarinin bölümleri üzerinde çalışan girişimlerle sık sık karşılaşırdım ve bunun üzerinde bu kadar çok zaman düşünmüş olmak ve hatta bir kısmını yazmaya çalışmış olmak çok yararlıydı.

Açık kaynaklı bir proje olarak inşa edeceğim alt küme, parantezlerini artık saklamak zorunda bile kalmayacağım yeni Lisp'ti. Pek çok Lisp uzmanı yeni bir Lisp inşa etmeyi hayal eder, kısmen dilin ayırt edici özelliklerinden biri lehçelerinin olmasıdır ve kısmen de, sanırım, zihnimizde mevcut tüm lehçelerin gerisinde kaldığı Platonik bir Lisp formuna sahip olmamızdır. Bende kesinlikle vardı. Bu yüzden yazın sonunda Dan ve ben, Cambridge'de satın aldığım bir evde Arc adını verdiğim bu yeni Lisp lehçesi üzerinde çalışmaya başladık.

Ertesi bahar, şans yüzüme güldü. Bir Lisp konferansında bir konuşma yapmaya davet edildim, bu yüzden Lisp'i Viaweb'de nasıl kullandığımız hakkında bir konuşma yaptım. Daha sonra bu konuşmanın bir postscript dosyasını paulgraham.com'a koydum; orayı yıllar önce Viaweb kullanarak oluşturmuştum ama hiçbir şey için kullanmamıştım. Bir günde 30.000 sayfa görüntüleme aldı. Dünyada ne olmuştu? Yönlendiren URL'ler birinin onu Slashdot'ta paylaştığını gösteriyordu. [10]

Vay canına, diye düşündüm bir kitle var. Eğer bir şey yazar ve web'e koyarsam, herkes okuyabilir. Bu şimdi bariz görünebilir ama o zaman şaşırtıcıydı. Basılı yayın döneminde okuyuculara ulaşan dar bir kanal vardı ve bu kanal editörler olarak bilinen hırçın canavarlar tarafından korunuyordu. Yazdığınız herhangi bir şey için kitle edinmenin tek yolu...<br>

##### `binary` embedding türü ile getirilen parçalar, `float` ve `int8` ile karşılaştırıldığında kesinlikle farklıdır. RAG boru hattınızda `float`/`int8`/`binary`/`ubinary` embedding kullanımı için [erişim değerlendirmesi](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/usage_pattern_retrieval/) yapmak ilginç olacaktır.

### Metin-Görüntü (Text-Image) Embedding'leri

[Cohere artık hem metnin hem de görüntünün aynı embedding alanında bulunduğu çok modlu (multi-modal) embedding modelini destekliyor.](https://cohere.com/blog/multimodal-embed-3)

```python
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open("../data/images/prometheus_paper_card.png")
plt.imshow(img)
```

    <matplotlib.image.AxesImage at 0x2c7323af0>

![png](output_41_1.png)

```python
from llama_index.embeddings.cohere import CohereEmbedding

embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
)
```

##### Görüntü Embedding'leri

```python
embeddings = embed_model.get_image_embedding(
    "../data/images/prometheus_paper_card.png"
)

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.01171875, -0.014503479, 0.014205933, -0.022949219, -0.040374756]

##### Metin Embedding'leri

```python
embeddings = embed_model.get_text_embedding("prometheus evaluation model")

print(len(embeddings))
print(embeddings[:5])
```

    1024
    [0.0044403076, 0.01737976, -0.023345947, 0.028182983, -0.036499023]