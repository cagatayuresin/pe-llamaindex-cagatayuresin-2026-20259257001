# Dökümanları Tanımlama ve Özelleştirme

## Dökümanları Tanımlama

Dökümanlar (Documents), veri yükleyiciler aracılığıyla otomatik olarak oluşturulabilir veya manuel olarak inşa edilebilir.

Varsayılan olarak, tüm [veri yükleyicilerimiz](/python/framework/module_guides/loading/connector) (LlamaHub'dakiler dahil), `load_data` fonksiyonu aracılığıyla `Document` nesneleri döndürür.

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
```

Dökümanları manuel olarak oluşturmayı da seçebilirsiniz. LlamaIndex, `Document` yapısını dışa aktarır.

```python
from llama_index.core import Document

text_list = [text1, text2, ...]
documents = [Document(text=t) for t in text_list]
```

Prototiplemeyi ve geliştirmeyi hızlandırmak için varsayılan bir metin kullanarak hızlıca bir döküman da oluşturabilirsiniz:

```python
document = Document.example()
```

## Dökümanları Özelleştirme

Bu bölüm, `Document` nesnelerini özelleştirmenin çeşitli yollarını kapsar. `Document` nesnesi `TextNode` nesnemizin bir alt sınıfı olduğundan, tüm bu ayarlar ve detaylar `TextNode` nesne sınıfı için de geçerlidir.

### Meta Veri (Metadata)

Dökümanlar ayrıca yararlı meta veriler ekleme imkanı sunar. Her dökümandaki `metadata` sözlüğünü kullanarak, yanıtlara yardımcı olması ve sorgu yanıtları için kaynakları takip etmesi için ek bilgiler eklenebilir. Bu bilgiler dosya adları veya kategoriler gibi herhangi bir şey olabilir. Eğer bir vektör veritabanıyla entegrasyon yapıyorsanız, bazı vektör veritabanlarının anahtarların dize (string), değerlerin ise düz (flat) olmasını (`str`, `float` veya `int`) gerektirdiğini unutmayın.

Her dökümanın `metadata` sözlüğünde ayarlanan her türlü bilgi, dökümandan oluşturulan her kaynak node'un `metadata` kısmında görünecektir. Ek olarak, bu bilgiler node'lara dahil edilerek indeksin bunları sorgularda ve yanıtlarda kullanmasına olanak tanır. Varsayılan olarak meta veriler, hem embedding hem de LLM model çağrıları için metne enjekte edilir.

Bu sözlüğü kurmanın birkaç yolu vardır:

1. Döküman yapılandırıcısında (constructor):

```python
document = Document(
    text="metin",
    metadata={"filename": "<doc_file_name>", "category": "<category>"},
)
```

2. Döküman oluşturulduktan sonra:

```python
document.metadata = {"filename": "<doc_file_name>"}
```

3. `SimpleDirectoryReader` ve `file_metadata` kancasını (hook) kullanarak dosya adını otomatik olarak ayarlayın. Bu, `metadata` alanını ayarlamak için her dökümanda kancayı otomatik olarak çalıştıracaktır:

```python
from llama_index.core import SimpleDirectoryReader

filename_fn = lambda filename: {"file_name": filename}

# her dökümanın meta verisini filename_fn'ye göre otomatik olarak ayarlar
documents = SimpleDirectoryReader(
    "./data", file_metadata=filename_fn
).load_data()
```

### Kimliği (id) Özelleştirme

[Döküman Yönetimi](/python/framework/module_guides/indexing/document_management) bölümünde detaylandırıldığı gibi, `doc_id` indeksteki dökümanların verimli bir şekilde yenilenmesini sağlamak için kullanılır. `SimpleDirectoryReader` kullanırken, `doc_id` değerini otomatik olarak her dökümanın tam yolu (path) olacak şekilde ayarlayabilirsiniz:

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data", filename_as_id=True).load_data()
print([x.doc_id for x in documents])
```

Ayrıca herhangi bir `Document` nesnesinin `doc_id` değerini doğrudan ayarlayabilirsiniz!

```python
document.doc_id = "Yeni döküman kimliğim!"
```

Not: Kimlik ayrıca bir `Document` nesnesi üzerindeki `node_id` veya `id_` özelliği aracılığıyla da ayarlanabilir (bir `TextNode` nesnesine benzer şekilde).

### Gelişmiş - Meta Veri Özelleştirme

Yukarıda belirtilen önemli bir detay, varsayılan olarak ayarladığınız her türlü meta verinin embedding oluşturma ve LLM işlemlerine dahil edilmesidir.

#### LLM Meta Veri Metnini Özelleştirme

Genellikle, bir dökümanın birçok meta veri anahtarı olabilir ancak yanıt sentezi sırasında bunların hepsinin LLM tarafından görülmesini istemeyebilirsiniz. Yukarıdaki örneklerde, LLM'in dökümanımızın `file_name` değerini okumasını istemeyebiliriz. Ancak, `file_name` daha iyi embedding'ler oluşturmaya yardımcı olacak bilgiler içerebilir. Bunu yapmanın temel avantajı, LLM'in okuduğu şeyi değiştirmeden getirme (retrieval) için embedding'leri yönlendirmektir.

Şu şekilde hariç tutabiliriz:

```python
document.excluded_llm_metadata_keys = ["file_name"]
```

Ardından, LLM'in aslında ne okuyacağını `get_content()` fonksiyonunu kullanarak ve `MetadataMode.LLM` değerini belirterek test edebiliriz:

```python
from llama_index.core.schema import MetadataMode

print(document.get_content(metadata_mode=MetadataMode.LLM))
```

#### Embedding Meta Veri Metnini Özelleştirme

LLM'e görünen meta verileri özelleştirmeye benzer şekilde, embedding'lere görünen meta verileri de özelleştirebiliriz. Bu durumda, belirli bir metnin embedding'leri yönlendirmesini İSTEMEDİĞİNİZ durumlar için embedding modeline görünen meta verileri spesifik olarak hariç tutabilirsiniz.

```python
document.excluded_embed_metadata_keys = ["file_name"]
```

Ardından, embedding modelinin aslında ne okuyacağını `get_content()` fonksiyonunu kullanarak ve `MetadataMode.EMBED` değerini belirterek test edebiliriz:

```python
from llama_index.core.schema import MetadataMode

print(document.get_content(metadata_mode=MetadataMode.EMBED))
```

#### Meta Veri Formatını Özelleştirme

Artık bildiğiniz gibi, meta veriler LLM'e veya embedding modeline gönderilirken her dökümanın/node'un asıl metnine enjekte edilir. Varsayılan olarak bu meta verilerin formatı üç öznitelik tarafından kontrol edilir:

1. `Document.metadata_seperator` -> varsayılan = `"\n"`

Meta verilerinizin tüm anahtar/değer alanlarını birleştirirken, bu alan her anahtar/değer çifti arasındaki ayırıcıyı kontrol eder.

2. `Document.metadata_template` -> varsayılan = `"{key}: {value}"`

Bu öznitelik, meta verilerinizdeki her anahtar/değer çiftinin nasıl formatlanacağını kontrol eder. `key` ve `value` dize anahtarları zorunludur.

3. `Document.text_template` -> varsayılan = `{metadata_str}\n\n{content}`

Meta verileriniz `metadata_seperator` ve `metadata_template` kullanılarak bir dizeye dönüştürüldüğünde, bu şablonlar meta verilerin dökümanınızın/node'unuzun metin içeriğiyle birleştirildiğinde nasıl görüneceğini kontrol eder. `metadata_str` ve `content` dize anahtarları zorunludur.

### Özet

Tüm bunları bilerek, tüm bu gücü kullanan kısa bir örnek oluşturalım:

```python
from llama_index.core import Document
from llama_index.core.schema import MetadataMode

document = Document(
    text="Bu son derece özelleştirilmiş bir dökümandır",
    metadata={
        "file_name": "cok_gizli_dokuman.txt",
        "category": "finans",
        "author": "LlamaIndex",
    },
    excluded_llm_metadata_keys=["file_name"],
    metadata_seperator="::",
    metadata_template="{key}=>{value}",
    text_template="Meta Veri: {metadata_str}\n-----\nİçerik: {content}",
)

print(
    "LLM şunu görüyor: \n",
    document.get_content(metadata_mode=MetadataMode.LLM),
)
print(
    "Embedding modeli şunu görüyor: \n",
    document.get_content(metadata_mode=MetadataMode.EMBED),
)
```

### Gelişmiş - Otomatik Meta Veri Çıkarımı

Meta veri çıkarımı gerçekleştirmek için LLM'lerin kendilerini kullanmaya dair [ilk örneklerimiz](/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor) bulunmaktadır.