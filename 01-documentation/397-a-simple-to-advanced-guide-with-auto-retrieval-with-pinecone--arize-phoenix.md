---
title: Pinecone + Arize Phoenix ile Otomatik Erişim (Auto-Retrieval) için Basitten Gelişmişe Rehber
 | LlamaIndex OSS Belgeleri
---

# Pinecone + Arize Phoenix ile Otomatik Erişim (Auto-Retrieval) için Basitten Gelişmişe Rehber

Bu not defterinde, standart top-k semantik aramanın ötesinde çok çeşitli yarı yapılandırılmış sorguları yürütmenize olanak tanıyan Pinecone üzerinde **otomatik erişimi (auto-retrieval)** nasıl gerçekleştireceğinizi gösteriyoruz.

Hem temel otomatik erişimin nasıl kurulacağını hem de nasıl genişletileceğini (istemi özelleştirerek ve dinamik meta veri erişimi yoluyla) gösteriyoruz.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```bash
%pip install llama-index-vector-stores-pinecone
```

```bash
# !pip install llama-index>=0.9.31 scikit-learn==1.2.2 arize-phoenix==2.4.1 pinecone-client>=3.0.0
```

## Bölüm 1: Otomatik Erişimi Kurma

Otomatik erişimi kurmak için aşağıdakileri yapın:

1. Bazı kurulumlar yapacağız, verileri yükleyeceğiz ve bir Pinecone vektör indeksi oluşturacağız.
2. Otomatik erişicimizi (autoretriever) tanımlayacağız ve bazı örnek sorgular çalıştıracağız.
3. Her izlemeyi (trace) gözlemlemek ve istem (prompt) girdi/çıktılarını görselleştirmek için Phoenix'i kullanacağız.
4. Otomatik erişim istemini nasıl özelleştireceğinizi göstereceğiz.

### 1.a Pinecone/Phoenix Kurulumu, Veri Yükleme ve Vektör İndeksi Oluşturma

Bu bölümde Pinecone'u kuruyoruz ve kitaplar/filmler hakkında bazı küçük verileri (metin verileri ve meta verilerle birlikte) içeri aktarıyoruz.

Ayrıca Phoenix'i, alt akış (downstream) izlerini yakalayacak şekilde kuruyoruz.

```python
# Phoenix kurulumu
import phoenix as px
import llama_index.core


px.launch_app()
llama_index.core.set_global_handler("arize_phoenix")
```

```bash
🌍 Phoenix uygulamasını tarayıcınızda görüntülemek için http://127.0.0.1:6006/ adresini ziyaret edin.
📺 Phoenix uygulamasını bir not defterinde görüntülemek için `px.active_session().view()` komutunu çalıştırın.
📖 Phoenix'in nasıl kullanılacağı hakkında daha fazla bilgi için https://docs.arize.com/phoenix adresine göz atın.
```

```python
import os


os.environ[
    "PINECONE_API_KEY"
] = "<Pinecone API anahtarınız, app.pinecone.io adresinden alınır>"
# os.environ["OPENAI_API_KEY"] = "sk-..."
```

```python
from pinecone import Pinecone
from pinecone import ServerlessSpec


api_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=api_key)
```

```python
# gerekirse silin
# pc.delete_index("quickstart-index")
```

```python
# Boyutlar text-embedding-ada-002 içindir
try:
    pc.create_index(
        "quickstart-index",
        dimension=1536,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-west-2"),
    )
except Exception as e:
    # Büyük olasılıkla indeks zaten mevcut
    print(e)
    pass
```

```python
pinecone_index = pc.Index("quickstart-index")
```

#### Belgeleri yükleyin, PineconeVectorStore ve VectorStoreIndex'i oluşturun

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
```

```python
from llama_index.core.schema import TextNode


nodes = [
    TextNode(
        text="The Shawshank Redemption",
        metadata={
            "author": "Stephen King",
            "theme": "Friendship",
            "year": 1994,
        },
    ),
    TextNode(
        text="The Godfather",
        metadata={
            "director": "Francis Ford Coppola",
            "theme": "Mafia",
            "year": 1972,
        },
    ),
    TextNode(
        text="Inception",
        metadata={
            "director": "Christopher Nolan",
            "theme": "Fiction",
            "year": 2010,
        },
    ),
    TextNode(
        text="To Kill a Mockingbird",
        metadata={
            "author": "Harper Lee",
            "theme": "Fiction",
            "year": 1960,
        },
    ),
    TextNode(
        text="1984",
        metadata={
            "author": "George Orwell",
            "theme": "Totalitarianism",
            "year": 1949,
        },
    ),
    TextNode(
        text="The Great Gatsby",
        metadata={
            "author": "F. Scott Fitzgerald",
            "theme": "The American Dream",
            "year": 1925,
        },
    ),
    TextNode(
        text="Harry Potter and the Sorcerer's Stone",
        metadata={
            "author": "J.K. Rowling",
            "theme": "Fiction",
            "year": 1997,
        },
    ),
]
```

```python
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
    namespace="test",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```

```python
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

### 1.b Otomatik Erişimciyi Tanımlama, Bazı Örnek Sorgular Çalıştırma

#### `VectorIndexAutoRetriever` Kurulumu

Girdilerden biri, vektör deposu koleksiyonunun hangi içeriği barındırdığını açıklayan bir `şemadır (schema)`. Bu, bir SQL veritabanındaki bir tabloyu tanımlayan tablo şemasına benzer. Bu şema bilgisi daha sonra isteme (prompt) enjekte edilir ve LLM'ye geçirilerek, meta veri filtreleri de dahil olmak üzere tam sorgunun ne olması gerektiği çıkarılır.

```python
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo


vector_store_info = VectorStoreInfo(
    content_info="ünlü kitaplar ve filmler",
    metadata_info=[
        MetadataInfo(
            name="director",
            type="str",
            description=("Yönetmenin adı"),
        ),
        MetadataInfo(
            name="theme",
            type="str",
            description=("Kitabın/filmin teması"),
        ),
        MetadataInfo(
            name="year",
            type="int",
            description=("Kitabın/filmin yılı"),
        ),
    ],
)
retriever = VectorIndexAutoRetriever(
    index,
    vector_store_info=vector_store_info,
    empty_query_top_k=10,
    # bu, pinecone'da boş sorgulara izin vermek için bir hack'tir
    default_empty_query_vector=[0] * 1536,
    verbose=True,
)
```

#### Haydi bazı sorgular çalıştıralım

Yapılandırılmış bilgileri kullanan bazı örnek sorgular çalıştıralım.

```python
nodes = retriever.retrieve(
    "2000 yılından sonraki bazı kitaplar/filmler hakkında bilgi ver"
)
```

```bash
Kullanılan sorgu dizisi (query str):
Kullanılan filtreler: [('year', '>', 2000)]
```

```python
for node in nodes:
    print(node.text)
    print(node.metadata)
```

**Inception**
**{'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}**

```python
nodes = retriever.retrieve("Bana Kurgu (Fiction) olan bazı kitaplardan bahset")
```

```bash
Kullanılan sorgu dizisi: Fiction
Kullanılan filtreler: [('theme', '==', 'Fiction')]
```

```python
for node in nodes:
    print(node.text)
    print(node.metadata)
```

**Inception**
**{'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010}**
**To Kill a Mockingbird**
**{'author': 'Harper Lee', 'theme': 'Fiction', 'year': 1960}**

#### Ek Meta Veri Filtreleri Geçirme

Otomatik olarak çıkarılmayan, manuel olarak geçirmek istediğiniz ek meta veri filtreleriniz varsa aşağıdakileri yapın.

```python
from llama_index.core.vector_stores import MetadataFilters


filter_dicts = [{"key": "year", "operator": "==", "value": 1997}]
filters = MetadataFilters.from_dicts(filter_dicts)
retriever2 = VectorIndexAutoRetriever(
    index,
    vector_store_info=vector_store_info,
    empty_query_top_k=10,
    # bu, pinecone'da boş sorgulara izin vermek için bir hack'tir
    default_empty_query_vector=[0] * 1536,
    extra_filters=filters,
)
```

```python
nodes = retriever2.retrieve("Bana Kurgu (Fiction) olan bazı kitaplardan bahset")
for node in nodes:
    print(node.text)
    print(node.metadata)
```

**Harry Potter and the Sorcerer's Stone**
**{'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997}**

#### Başarısız Bir Sorgu Örneği

Hiçbir sonucun getirilmediğine dikkat edin! Bunu daha sonra düzelteceğiz.

```python
nodes = retriever.retrieve("Bana mafya temalı bazı kitaplardan bahset")
```

```bash
Kullanılan sorgu dizisi: books
Kullanılan filtreler: [('theme', '==', 'mafia')]
```

```python
for node in nodes:
    print(node.text)
    print(node.metadata)
```

### İzlemeleri (Traces) Görselleştirme

İzlemelere göz atmak için Phoenix'i açalım!

![](https://drive.google.com/uc?export=view&id=1PCEwIdv7GcInk3i6ebd2WWjTp9ducG5F)

Otomatik erişim istemine bir göz atalım. Otomatik erişim isteminin iki adet birkaç adımlı (few-shot) örnek kullandığını görüyoruz.

## Bölüm 2: Otomatik Erişimi Genişletme (Dinamik Meta Veri Erişimi ile)

Şimdi istemi özelleştirerek otomatik erişimi genişletiyoruz. İlk bölümde, açıkça bazı kurallar ekliyoruz.

İkinci bölümde, vektör veritabanından ilgili meta verileri getiren bir ilk aşama erişim adımı gerçekleştiren ve bunu otomatik erişim istemine birkaç adımlı örnekler olarak ekleyen **dinamik meta veri erişimini (dynamic metadata retrieval)** uyguluyoruz. (Elbette, ikinci aşama erişim adımı asıl öğeleri vektör veritabanından getirir).

### 2.a Otomatik Erişim İstemi'ni İyileştirme

Otomatik erişim istemimiz çalışıyor, ancak çeşitli şekillerde iyileştirilebilir. Bazı örnekler arasında, 2 adet sabit kodlanmış birkaç adımlı örnek içermesi (kendi örneklerinizi nasıl ekleyebilirsiniz?) ve ayrıca otomatik erişimin "her zaman" doğru meta veri filtrelerini çıkarmaması yer alır.

Örneğin, tüm `theme` alanları büyük harfle başlar. LLM'ye bunu nasıl söyleriz ki yanlışlıkla küçük harfli bir "tema" çıkarmasın?

İstemi değiştirmeyi deneyelim!

```python
from llama_index.core.prompts import display_prompt_dict
from llama_index.core import PromptTemplate
```

```python
prompts_dict = retriever.get_prompts()
```

```python
display_prompt_dict(prompts_dict)
```

```python
# gerekli şablon değişkenlerine bakın.
prompts_dict["prompt"].template_vars
```

```python
['schema_str', 'info_str', 'query_str']
```

#### İstemi Özelleştirme

İstemi biraz özelleştirelim. Şunları yapıyoruz:

- Belirteçten (token) tasarruf etmek için ilk birkaç adımlı örneği çıkarın.
- Eğer "theme" çıkarımı yapılıyorsa bir harfi her zaman büyük yapması için bir mesaj ekleyin.

İstem şablonunun `schema_str`, `info_str` ve `query_str` değişkenlerinin tanımlanmış olmasını beklediğini unutmayın.

```python
# istem şablonunu yazın ve değiştirin.


prompt_tmpl_str = """\
Hedefiniz, kullanıcının sorgusunu aşağıda sağlanan istek şemasıyla eşleşecek şekilde yapılandırmaktır.


<< Yapılandırılmış İstek Şeması >>
Yanıt verirken, aşağıdaki şemada biçimlendirilmiş bir JSON nesnesi içeren bir markdown kod parçacığı kullanın:


{schema_str}


Sorgu dizisi (query string), yalnızca belgelerin içeriğiyle eşleşmesi beklenen metni içermelidir. Filtredeki hiçbir koşul sorguda da belirtilmemelidir.


Filtrelerin yalnızca veri kaynağında bulunan özniteliklere atıfta bulunduğundan emin olun.
Filtrelerin özniteliklerin açıklamalarını dikkate aldığından emin olun.
Filtrelerin yalnızca gerektiğinde kullanıldığından emin olun. Uygulanması gereken bir filtre yoksa, filtre değeri için [] döndürün.
Kullanıcının sorgusu açıkça getirilecek belge sayısını belirtiyorsa, top_k değerini o sayıya ayarlayın, aksi takdirde top_k değerini ayarlamayın.
Bir filtre için ASLA null değeri çıkarmayın. Bu, alt akış programını bozacaktır. Bunun yerine filtreyi dahil etmeyin.


<< Örnek 1. >>
Veri Kaynağı:
```json
{{
    "metadata_info": [
        {{
            "name": "author",
            "type": "str",
            "description": "Yazar adı"
        }},
        {{
            "name": "book_title",
            "type": "str",
            "description": "Kitap başlığı"
        }},
        {{
            "name": "year",
            "type": "int",
            "description": "Yayın Yılı"
        }},
        {{
            "name": "pages",
            "type": "int",
            "description": "Sayfa sayısı"
        }},
        {{
            "name": "summary",
            "type": "str",
            "description": "Kitabın kısa bir özeti"
        }}
    ],
    "content_info": "Klasik edebiyat"
}}
```


Kullanıcı Sorgusu: Jane Austen'ın 1813'ten sonra yayımlanan ve toplumsal statü için evlilik temasını inceleyen bazı kitapları nelerdir?


Ek Talimatlar: Yok


Yapılandırılmış İstek:


```
{{"query": "Toplumsal statü için evlilik temasıyla ilgili kitaplar", "filters": [{{"key": "year", "value": "1813", "operator": ">"}}, {{"key": "author", "value": "Jane Austen", "operator": "=="}}], "top_k": null}}
```


<< Örnek 2. >> Veri Kaynağı:


```
{info_str}
```


Kullanıcı Sorgusu: {query_str}


Ek Talimatlar: {additional_instructions}


Yapılandırılmış İstek: """


prompt_tmpl = PromptTemplate(prompt_tmpl_str)
```

Bir `additional_instructions` (ek talimatlar) şablon değişkeni eklediğimizi fark edeceksiniz. Bu, vektör koleksiyonuna özel talimatlar eklememize olanak tanır.

Talimatı eklemek için `partial_format` kullanacağız.

```python
add_instrs = """\
Filtrelerden biri 'theme' (tema) ise, çıkarılan değerin ilk harfinin büyük olduğundan emin olun. 'theme' için yalnızca büyük harfle başlayan kelimeler geçerli değerlerdir. \
"""
prompt_tmpl = prompt_tmpl.partial_format(additional_instructions=add_instrs)
```

```python
retriever.update_prompts({"prompt": prompt_tmpl})
```

#### Sorguları Yeniden Çalıştırma

Şimdi bazı sorguları yeniden çalıştırmayı deneyelim ve değerin otomatik olarak çıkarıldığını göreceğiz.

```python
nodes = retriever.retrieve(
    "Bana arkadaşlık temalı bazı kitaplardan bahset"
)
```

```python
for node in nodes:
    print(node.text)
    print(node.metadata)
```

**The Shawshank Redemption**
**{'author': 'Stephen King', 'theme': 'Friendship', 'year': 1994}**

### 2.b Dinamik Meta Veri Erişimini Uygulama

İsteme kuralları sabit kodlamak yerine bir seçenek de, LLM'nin doğru meta veri filtrelerini daha iyi çıkarmasına yardımcı olmak için **meta verilerin ilgili birkaç adımlı örneklerini** getirmektir.

Bu, LLM'nin "where" yan tümcelerini çıkarırken, özellikle değerin yazımı / doğru biçimlendirilmesi gibi konularda hata yapmasını daha iyi önleyecektir.

Bunu vektör erişimi yoluyla yapabiliriz. Mevcut vektör veritabanı koleksiyonu ham metni + meta verileri saklar; doğrudan bu koleksiyonu sorgulayabiliriz veya ayrı olarak yalnızca meta verileri indeksleyip oradan getirebiliriz. Bu bölümde ilkini yapmayı seçiyoruz ancak pratikte ikincisini yapmak isteyebilirsiniz.

```python
# en iyi 2 örneği getiren erişiciyi tanımlayın.
metadata_retriever = index.as_retriever(similarity_top_k=2)
```

Önceki bölümde tanımlanan aynı `prompt_tmpl_str` değerini kullanıyoruz.

```python
from typing import List, Any


def format_additional_instrs(**kwargs: Any) -> str:
    """Örnekleri bir dizeye dönüştürün."""


    nodes = metadata_retriever.retrieve(kwargs["query_str"])
    context_str = (
        "İşte veritabanı koleksiyonundan ilgili girişlerin meta verileri. "
        "Bu, doğru filtreleri çıkarmanıza yardımcı olmalıdır: \n"
    )
    for node in nodes:
        context_str += str(node.node.metadata) + "\n"
    return context_str


ext_prompt_tmpl = PromptTemplate(
    prompt_tmpl_str,
    function_mappings={"additional_instructions": format_additional_instrs},
)
```

```python
retriever.update_prompts({"prompt": ext_prompt_tmpl})
```

#### Sorguları Yeniden Çalıştırma

Şimdi bazı sorguları yeniden çalıştırmayı deneyelim ve değerin otomatik olarak çıkarıldığını göreceğiz.

```python
nodes = retriever.retrieve("Bana mafya temalı bazı kitaplardan bahset")
for node in nodes:
    print(node.text)
    print(node.metadata)
```

```bash
Kullanılan sorgu dizisi: books
Kullanılan filtreler: [('theme', '==', 'Mafia')]
The Godfather
{'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972}
```

```python
nodes = retriever.retrieve("Bana HARPER LEE tarafından yazılmış bazı kitapları söyle")
for node in nodes:
    print(node.text)
    print(node.metadata)
```

```bash
Kullanılan sorgu dizisi: Books authored by Harper Lee
Kullanılan filtreler: [('author', '==', 'Harper Lee')]
To Kill a Mockingbird
{'author': 'Harper Lee', 'theme': 'Fiction', 'year': 1960}
```
