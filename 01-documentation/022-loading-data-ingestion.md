# Veri Yükleme (Aktarma/Ingestion)

Seçtiğiniz LLM verileriniz üzerinde işlem yapabilmeden önce, verileri işlemeniz ve yüklemeniz gerekir. Bunun ML dünyasındaki veri temizleme/özellik mühendisliği (feature engineering) hatlarıyla veya geleneksel veri bağlamındaki ETL hatlarıyla paralellikleri vardır.

Bu aktarma hattı genellikle üç ana aşamadan oluşur:

1. Veriyi yükle
2. Veriyi dönüştür
3. Veriyi indeksle ve sakla

İndeksleme/saklama konularını [gelecek](/python/framework/understanding/rag/indexing) [bölümlerde](/python/framework/understanding/rag/storing) ele alacağız. Bu kılavuzda çoğunlukla yükleyiciler (loaders) ve dönüşümlerden (transformations) bahsedeceğiz.

## Yükleyiciler (Loaders)

Seçtiğiniz LLM verileriniz üzerinde işlem yapabilmeden önce onları yüklemeniz gerekir. LlamaIndex bunu `Reader` (Okuyucu) olarak da adlandırılan veri bağlayıcıları (data connectors) aracılığıyla yapar. Veri bağlayıcıları, farklı veri kaynaklarından verileri aktarır ve verileri `Document` nesneleri şeklinde formatlar. Bir `Document`, bir veri koleksiyonu (şu anda metin ve gelecekte resim ile ses) ve bu veri hakkındaki metadatalardır.

### SimpleDirectoryReader kullanarak yükleme

Kullanımı en kolay okuyucu, verilen bir dizindeki her dosyadan dökümanlar oluşturan SimpleDirectoryReader'dır. LlamaIndex'e yerleşiktir ve Markdown, PDF'ler, Word dökümanları, PowerPoint sunumları, resimler, ses ve video dahil olmak üzere çeşitli formatları okuyabilir.

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
```

### LlamaHub Okuyucularını Kullanma

Veri alınabilecek çok fazla yer olduğu için her şey yerleşik değildir. Bunun yerine, onları veri bağlayıcıları kayıt defterimiz olan [LlamaHub](/python/framework/understanding/rag/loading/llamahub) üzerinden indirirsiniz.

Bu örnekte LlamaIndex, bir SQL veritabanına sorgu gönderen ve sonuçların her satırını bir `Document` olarak döndüren [DatabaseReader](https://llamahub.ai/l/readers/llama-index-readers-database) adlı bağlayıcıyı indirir ve kurar:

```python
from llama_index.core import download_loader
from llama_index.readers.database import DatabaseReader
import os

reader = DatabaseReader(
    scheme=os.getenv("DB_SCHEME"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dbname=os.getenv("DB_NAME"),
)

query = "SELECT * FROM users"
documents = reader.load_data(query=query)
```

[LlamaHub](https://llamahub.ai) adresinde kullanılacak yüzlerce bağlayıcı mevcuttur!

### Doğrudan Document Oluşturma

Bir yükleyici kullanmak yerine, doğrudan bir Document da kullanabilirsiniz.

```python
from llama_index.core import Document

doc = Document(text="örnek metin")
```

## Dönüşümler (Transformations)

Veriler yüklendikten sonra, onları bir depolama sistemine yerleştirmeden önce işlemeniz ve dönüştürmeniz gerekir. Bu dönüşümler arasında parçalara ayırma (chunking), metadata çıkarma ve her parçayı gömme (embedding) yer alır. Bu; verilerin getirilebilmesini ve LLM tarafından en iyi şekilde kullanılabilmesini sağlamak için gereklidir.

Dönüşüm girdi/çıktıları `Node` nesneleridir (bir `Document`, bir `Node` alt sınıfıdır). Dönüşümler üst üste eklenebilir ve yeniden sıralanabilir.

Dökümanları dönüştürmek için hem üst düzey hem de alt düzey API'larımız mevcuttur.

### Üst Düzey Dönüşüm API'ı

İndekslerin, bir Document nesnesi dizisi kabul eden ve onları doğru bir şekilde ayrıştırıp parçalara ayıracak olan `.from_documents()` metodu vardır. Ancak bazen dökümanlarınızın nasıl bölüneceği konusunda daha fazla kontrol sahibi olmak istersiniz.

```python
from llama_index.core import VectorStoreIndex

vector_index = VectorStoreIndex.from_documents(documents)
vector_index.as_query_engine()
```

Arka planda bu işlem, Dökümanınızı Dökümanlara benzer (metin ve metadata içerirler) ancak ana Dökümanlarıyla bir ilişkisi olan Node nesnelerine böler.

Bu soyutlama üzerinden metin bölücü (text splitter) gibi temel bileşenleri özelleştirmek isterseniz, özel bir `transformations` listesi geçebilir veya bunu global `Settings` nesnesine uygulayabilirsiniz:

```python
from llama_index.core.node_parser import SentenceSplitter

text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

# global ayar
from llama_index.core import Settings
Settings.text_splitter = text_splitter

# indeks bazlı ayar
index = VectorStoreIndex.from_documents(
    documents, transformations=[text_splitter]
)
```

### Alt Düzey Dönüşüm API'ı

Bu adımları açıkça da tanımlayabilirsiniz.

Bunu, dönüşüm modüllerimizi (metin bölücüler, metadata çıkarıcılar vb.) bağımsız bileşenler olarak kullanarak veya dekleratif [Aktarma Hattı arayüzümüzde](/python/framework/module_guides/loading/ingestion_pipeline) birleştirerek yapabilirsiniz.

Aşağıdaki adımları inceleyelim:

#### Dökümanlarınızı Node'lara Bölme

Dökümanlarınızı işlemenin temel adımlarından biri, onları "parçalara" (chunks)/Node nesnelerine bölmektir. Temel fikir, verilerinizi getirilebilecek ve LLM'e beslenebilecek küçük parçalar haline getirmektir.

LlamaIndex; paragraf/cümle/token tabanlı bölücülerden HTML, JSON gibi dosya tabanlı bölücülere kadar geniş bir yelpazede [metin bölücüleri](/python/framework/module_guides/loading/node_parsers/modules) destekler.

Bunlar [tek başlarına veya bir aktarma hattının parçası olarak kullanılabilirler](/python/framework/module_guides/loading/node_parsers).

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

documents = SimpleDirectoryReader("./data").load_data()

pipeline = IngestionPipeline(transformations=[TokenTextSplitter(), ...])

nodes = pipeline.run(documents=documents)
```

### Metadata Ekleme

Ayrıca dökümanlarınıza ve node'larınıza metadata eklemeyi de seçebilirsiniz. Bu manuel olarak veya [otomatik metadata çıkarıcılar](/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor) ile yapılabilir.

Burada şunlara dair kılavuzlar mevcuttur: 1) [Document'ları nasıl özelleştireceğiniz](/python/framework/module_guides/loading/documents_and_nodes/usage_documents) ve 2) [Node'ları nasıl özelleştireceğiniz](/python/framework/module_guides/loading/documents_and_nodes/usage_nodes).

```python
document = Document(
    text="örnek metin",
    metadata={"filename": "<dosya_adı>", "category": "<kategori>"},
)
```

### Embedding Ekleme

Bir node'u bir vektör indeksine eklemek için bir embedding'e sahip olması gerekir. Daha fazla ayrıntı için [aktarma hattı](/python/framework/module_guides/loading/ingestion_pipeline) veya [embedding kılavuzumuza](/python/framework/module_guides/models/embeddings) bakın.

### Doğrudan Node Oluşturma ve Geçme

İsterseniz doğrudan node'lar oluşturabilir ve bir Node listesini doğrudan bir indeksleyiciye geçebilirsiniz:

```python
from llama_index.core.schema import TextNode

node1 = TextNode(text="<metin_parçası>", id_="<node_id>")
node2 = TextNode(text="<metin_parçası>", id_="<node_id>")

index = VectorStoreIndex([node1, node2])
```