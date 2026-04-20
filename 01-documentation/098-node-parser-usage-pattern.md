# Node Parser Kullanım Kalıbı

Node parser'lar (düğüm ayrıştırıcıları), bir döküman listesini alan ve bunları her bir node ana dökümanın belirli bir parçası olacak şekilde `Node` nesnelerine bölen basit bir soyutlamadır. Bir döküman node'lara bölündüğünde, tüm öznitelikleri alt node'lara miras kalır (yani `metadata`, metin ve meta veri şablonları vb.). `Node` ve `Document` özellikleri hakkında daha fazlasını [buradan](/python/framework/module_guides/loading/documents_and_nodes) okuyabilirsiniz.

## Başlarken

### Bağımsız Kullanım

Node parser'lar kendi başlarına kullanılabilirler:

```python
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

nodes = node_parser.get_nodes_from_documents(
    [Document(text="uzun metin")], show_progress=False
)
```

### Dönüşüm (Transformation) Olarak Kullanım

Node parser'lar, bir veri alma boru hattı (ingestion pipeline) içindeki herhangi bir dönüşüm kümesine dahil edilebilir.

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

documents = SimpleDirectoryReader("./data").load_data()

pipeline = IngestionPipeline(transformations=[TokenTextSplitter(), ...])

nodes = pipeline.run(documents=documents)
```

### İndeks İçinde Kullanım

Ya da `.from_documents()` kullanılarak bir indeks oluşturulduğunda otomatik olarak kullanılmak üzere `transformations` veya küresel (global) ayarlar içine yerleştirilebilir:

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

documents = SimpleDirectoryReader("./data").load_data()

# küresel (global)
from llama_index.core import Settings

Settings.text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

# indeks başına
index = VectorStoreIndex.from_documents(
    documents,
    transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)],
)
```

## Modüller

Tam [modül kılavuzuna](/python/framework/module_guides/loading/node_parsers/modules) bakın.