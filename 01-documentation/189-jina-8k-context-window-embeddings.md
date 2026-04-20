# Jina 8K Bağlam Penceresi (Context Window) Embedding'leri

Burada, 8k bağlam uzunluğunu destekleyen ve `text-embedding-ada-002` ile eşdeğer performansa sahip olan `jina-embeddings-v2` modelinin nasıl kullanılacağını gösteriyoruz.

<a href="https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/embeddings/jina_embeddings.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab'da Aç"/></a>

```python
%pip install llama-index-embeddings-huggingface
%pip install llama-index-embeddings-huggingface-api
%pip install llama-index-embeddings-openai
```

```python
import nest_asyncio

nest_asyncio.apply()
```

## Embedding Modelini Kurma

```python
from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding,
)
from llama_index.embeddings.huggingface_api import (
    HuggingFaceInferenceAPIEmbedding,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
```

```python
# temel model
# model_name = "jinaai/jina-embeddings-v2-base-en"
# küçük model
model_name = "jinaai/jina-embeddings-v2-small-en"
```

```python
# modeli yerel olarak indir
# not: bunu çalıştırmak için yeterli RAM+işlem gücüne ihtiyacınız var
embed_model = HuggingFaceEmbedding(
    model_name=model_name, trust_remote_code=True
)


# Hugging Face üzerindeki çıkarım (inference) API'sini kullan (ancak hız sınırı sorunlarıyla karşılaşabilirsiniz)
# embed_model = HuggingFaceInferenceAPIEmbedding(
#     model_name="jinaai/jina-embeddings-v2-base-en",
# )
```

```python
# şimdilik parça boyutunu (chunk size) 1024 olarak ayarlıyoruz, açıkçası çok daha büyük ayarlayabilirsiniz
Settings.embed_model = embed_model
Settings.chunk_size = 1024
```

### Karşılaştırma için OpenAI ada embedding'lerini kurun

```python
embed_model_base = OpenAIEmbedding()
```

## Test etmek için İndeksi Kurun

Standart Paul Graham örneğimizi kullanacağız.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
```

```python
reader = SimpleDirectoryReader("../data/paul_graham")
docs = reader.load_data()
```

```python
index_jina = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
```

```python
index_base = VectorStoreIndex.from_documents(
    docs, embed_model=embed_model_base
)
```

## Sonuçları Görüntüle

Jina-8k ve OpenAI (base) ile getirilen sonuçlara bakalım.

```python
from llama_index.core.response.notebook_utils import display_source_node

retriever_jina = index_jina.as_retriever(similarity_top_k=1)
retriever_base = index_base.as_retriever(similarity_top_k=1)
```

```python
retrieved_nodes = retriever_jina.retrieve(
    "Yazar sanat okulunda ne yaptı?"
)
```

```python
for n in retrieved_nodes:
    display_source_node(n, source_length=2000)
```

**Düğüm (Node) ID:** 921cc179-312f-4ee2-a760-3cccd27470d9<br>**Benzerlik:** 0.7612087686435924<br>**Metin:** Sanatçıların her zaman kendine özgü bir stili olmasının nedeni bu değildir ama alıcıların bu tür işlere çok para ödemesinin nedeni genellikle budur. [6]

Epey hevesli öğrenci de vardı: lisede "çizebilen" çocuklar ve şimdi daha da iyi çizmeyi öğrenmek için ülkedeki en iyi sanat okulu olması gereken yere gelmişlerdi. RISD'de buldukları şeylerden dolayı kafaları karışmış ve moralleri bozulmuş olma eğilimindeydiler ama devam ettiler çünkü resim yapmak onların yaptığı şeydi. Ben lisede çizebilen çocuklardan biri değildim ama RISD'de kesinlikle kendime özgü stil arayanların kabilesinden ziyade onların kabilesine daha yakındım.

RISD'de aldığım renk dersinde çok şey öğrendim ama onun dışında temelde kendime resim yapmayı öğretiyordum ve bunu bedavaya yapabilirdim. Bu yüzden 1993'te okulu bıraktım. Bir süre Providence çevresinde takıldım ve sonra üniversite arkadaşım Nancy Parmet bana büyük bir iyilik yaptı. New York'ta annesinin sahibi olduğu bir binada kirası kontrollü bir daire boşalıyordu. İster miydim? Mevcut yerimden çok daha pahalı değildi ve New York sanatçıların olduğu yer olmalıydı. Yani evet, istedim! [7]

Asterix çizgi romanları, Romalılar tarafından kontrol edilmediği ortaya çıkan Galya'nın küçük bir köşesine yakınlaşarak başlar. New York City haritasında da benzer bir şey yapabilirsiniz: Upper East Side'a yakınlaşırsanız, zengin olmayan ya da en azından 1993'te zengin olmayan küçük bir köşe vardır. Adı Yorkville ve orası benim yeni evimdi. Artık bir New York sanatçısıydım — kelimenin tam anlamıyla resim yapan ve New York'ta yaşayan teknik anlamda.

Para konusunda gergindim çünkü Interleaf'in düşüşe geçtiğini hissedebiliyordum. Serbest zamanlı Lisp programlama işi çok nadirdi ve başka bir dilde program yazmak istemiyordum; o günlerde şanslıysam bu C++ demekti. Bu yüzden finansal fırsatlara olan sarsılmaz burnumla Lisp üzerine başka bir kitap yazmaya karar verdim. Bu popüler bir kitap olacaktı, ders kitabı olarak kullanılabilecek türden bir kitap. Kendimi telif haklarıyla mütevazı bir şekilde yaşarken ve tüm zamanımı...<br>

```python
retrieved_nodes = retriever_base.retrieve("Yazar okulda ne yaptı?")
```

```python
for n in retrieved_nodes:
    display_source_node(n, source_length=2000)
```

**Düğüm (Node) ID:** 0abf44f2-94bd-421f-9ebd-5b50f4de37f0<br>**Benzerlik:** 0.8352482505756655<br>**Metin:** Neler Üzerinde Çalıştım

Şubat 2021

Üniversiteden önce, okul dışında üzerinde çalıştığım iki ana şey yazmak ve programlamaktı. Makale yazmazdım. O zamanlar başlangıç seviyesindeki yazarların yazması gereken şeyi yazardım ve muhtemelen hala öyledir: kısa hikayeler. Hikayelerim berbattı. Neredeyse hiç olay örgüsü yoktu, sadece derin olduklarını hayal ettiğim güçlü duygulara sahip karakterler vardı.

Yazmaya çalıştığım ilk programlar, okul bölgemizin o zamanlar "veri işleme" olarak adlandırılan şey için kullandığı IBM 1401 üzerindeydi. Bu 9. sınıftaydı, yani 13 veya 14 yaşındaydım. Okul bölgesinin 1401'i tesadüfen ortaokulumuzun bodrumundaydı ve arkadaşım Rich Draves ile ben onu kullanmak için izin aldık. Orası, parlak floresan ışıkları altında yükseltilmiş bir zeminde duran CPU, disk sürücüleri, yazıcı, kart okuyucu gibi tüm bu uzaylı görünümlü makinelerle, minyatür bir Bond kötü adamının inine benziyordu.

Kullandığımız dil, Fortran'ın erken bir versiyonuydu. Programları delikli kartlara yazmanız, ardından bunları kart okuyucuya istiflemeniz ve programı belleğe yükleyip çalıştırmak için bir düğmeye basmanız gerekiyordu. Sonuç genellikle muazzam gürültülü yazıcıda bir şeyler yazdırmak olurdu.

1401 kafamı karıştırmıştı. Onunla ne yapacağımı bulamamıştım. Ve geriye dönüp baktığımda onunla yapabileceğim pek bir şey yoktu. Programlara tek girdi biçimi delikli kartlarda saklanan verilerdi ve benim delikli kartlarda saklanan hiçbir verim yoktu. Diğer tek seçenek, pi sayısının yaklaşık değerlerini hesaplamak gibi herhangi bir girdiye dayanmayan şeyler yapmaktı, ancak bu tür ilginç bir şey yapacak kadar matematik bilmiyordum. Bu yüzden yazdığım hiçbir programı hatırlayamadığıma şaşırmıyorum, çünkü pek bir şey yapmış olamazlar. En net anım, programların sonlanmamasının mümkün olduğunu öğrendiğim andı; benimkilerden biri sonlanmadığında. Zaman paylaşımı olmayan bir makinede bu, veri merkezi müdürünün ifadesinden de anlaşıldığı üzere teknik bir hata olduğu kadar sosyal bir hataydı da.

Mikrobilgisayarlarla her şey değişti. Artık...<br>