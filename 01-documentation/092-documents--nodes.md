# Dökümanlar (Documents) / Node'lar

## Kavram

Döküman (Document) ve Node nesneleri, LlamaIndex içindeki temel soyutlamalardır.

Bir **Döküman (Document)**, herhangi bir veri kaynağı için genel bir kapsayıcıdır; örneğin bir PDF, bir API çıktısı veya bir veritabanından getirilen veriler. Manuel olarak oluşturulabilecekleri gibi, veri yükleyicilerimiz aracılığıyla otomatik olarak da oluşturulabilirler. Varsayılan olarak bir Döküman, bazı diğer özniteliklerle birlikte metni saklar. Bunlardan bazıları şunlardır:

-   `metadata` - metne eklenebilen ek açıklamaların bulunduğu bir sözlük.
-   `relationships` - diğer Dökümanlara/Node'lara olan ilişkileri içeren bir sözlük.

_Not_: Dökümanların görsel saklamasına yönelik beta desteğimiz bulunmaktadır ve çok modlu (multimodal) yeteneklerini geliştirmek için aktif olarak çalışıyoruz.

Bir **Node**, bir kaynak Dökümanın bir "parçasını" (chunk) temsil eder; bu bir metin parçası, bir görsel veya başka bir şey olabilir. Dökümanlara benzer şekilde, diğer node'larla olan meta veri ve ilişki bilgilerini içerirler.

Node'lar LlamaIndex'te birinci sınıf vatandaştır. Node'ları ve tüm özniteliklerini doğrudan tanımlamayı seçebilirsiniz. Ayrıca, kaynak Dökümanları `NodeParser` sınıflarımız aracılığıyla Node'lara "ayrıştırmayı" da seçebilirsiniz. Varsayılan olarak, bir Dökümandan türetilen her Node, o Dökümanla aynı meta verileri miras alacaktır (örneğin, Dökümandaki bir "file_name" alanı her Node'a aktarılır).

## Kullanım Kalıbı (Usage Pattern)

İşte Dökümanlar ve Node'larla başlamak için bazı basit kod parçaları.

#### Dökümanlar (Documents)

```python
from llama_index.core import Document, VectorStoreIndex

text_list = [text1, text2, ...]
documents = [Document(text=t) for t in text_list]

# indeks oluştur
index = VectorStoreIndex.from_documents(documents)
```

#### Node'lar

```python
from llama_index.core.node_parser import SentenceSplitter

# dökümanları yükle
...

# node'ları ayrıştır
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

# indeks oluştur
index = VectorStoreIndex(nodes)
```

### Döküman/Node Kullanımı

Dökümanların/Node'ların nasıl kullanılacağına dair daha fazla ayrıntı için derinlemesine kılavuzlarımıza göz atın.

-   [Döküman Kullanımı](/python/framework/module_guides/loading/documents_and_nodes/usage_documents)
-   [Node Kullanımı](/python/framework/module_guides/loading/documents_and_nodes/usage_nodes)
-   [Veri Alma Boru Hattı (Ingestion Pipeline)](/python/framework/module_guides/loading/ingestion_pipeline)