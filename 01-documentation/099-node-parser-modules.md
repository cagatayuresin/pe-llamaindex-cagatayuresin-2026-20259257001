# Node Parser Modülleri

## Dosya Tabanlı Node Parser'lar

Ayrıştırılan içeriğin türüne (JSON, Markdown vb.) göre node'lar oluşturacak birkaç dosya tabanlı node parser bulunmaktadır.

En basit akış, her içerik türü için otomatik olarak en iyi node parser'ı kullanmak amacıyla `FlatFileReader` ile `SimpleFileNodeParser`'ı birleştirmektir. Daha sonra, metnin asıl uzunluğunu hesaba katmak için dosya tabanlı node parser'ı metin tabanlı bir node parser ile zincirlemek isteyebilirsiniz.

### SimpleFileNodeParser

```python
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path

md_docs = FlatReader().load_data(Path("./test.md"))

parser = SimpleFileNodeParser()
md_nodes = parser.get_nodes_from_documents(md_docs)
```

### HTMLNodeParser

Bu node parser, ham HTML'i ayrıştırmak için `beautifulsoup` kullanır.

Varsayılan olarak, HTML etiketlerinin seçili bir alt kümesini ayrıştıracaktır, ancak bunu geçersiz kılabilirsiniz.

Varsayılan etiketler: `["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "b", "i", "u", "section"]`

```python
from llama_index.core.node_parser import HTMLNodeParser

parser = HTMLNodeParser(tags=["p", "h1"])  # isteğe bağlı etiket listesi
nodes = parser.get_nodes_from_documents(html_docs)
```

### JSONNodeParser

`JSONNodeParser`, ham JSON verisini ayrıştırır.

```python
from llama_index.core.node_parser import JSONNodeParser

parser = JSONNodeParser()

nodes = parser.get_nodes_from_documents(json_docs)
```

### MarkdownNodeParser

`MarkdownNodeParser`, ham markdown metnini ayrıştırır.

```python
from llama_index.core.node_parser import MarkdownNodeParser

parser = MarkdownNodeParser()

nodes = parser.get_nodes_from_documents(markdown_docs)
```

## Metin Bölücüler (Text-Splitters)

### CodeSplitter

Ham kod metnini, yazıldığı dile göre böler.

Desteklenen dillerin tam listesini [buradan](https://github.com/grantjenks/py-tree-sitter-languages#license) kontrol edin.

```python
from llama_index.core.node_parser import CodeSplitter

splitter = CodeSplitter(
    language="python",
    chunk_lines=40,  # parça başına satır sayısı
    chunk_lines_overlap=15,  # parçalar arası çakışan satır sayısı
    max_chars=1500,  # parça başına maksimum karakter sayısı
)
nodes = splitter.get_nodes_from_documents(documents)
```

### LangchainNodeParser

Langchain'deki mevcut herhangi bir metin bölücüyü bir node parser ile sarmalayabilirsiniz.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import LangchainNodeParser

parser = LangchainNodeParser(RecursiveCharacterTextSplitter())
nodes = parser.get_nodes_from_documents(documents)
```

### Chunker

`Chunker`, [chonkie](https://docs.chonkie.ai/) bölücüleri etrafında yapılandırılmış çok amaçlı bir node parser'dır.
Desteklenen herhangi bir chonkie bölme stratejisi için bir takma ad (alias) kullanarak ayrıştırıcınızı başlatabilirsiniz; geçerli takma adların tam listesine `Chunker.valid_chunker_types` özniteliği aracılığıyla erişilebilir.

```python
from llama_index.node_parser.chonkie import Chunker

parser = Chunker("recursive", chunk_size=2048)
nodes = parser.get_nodes_from_documents(documents)
```

Ayrıca ayrıştırıcıyı başlatmak için doğrudan bir chonkie bölücü örneği (instance) de geçirebilirsiniz.

```python
from chonkie import RecursiveChunker
from llama_index.node_parser.chonkie import Chunker

chonkie_chunker = RecursiveChunker()
parser = Chunker(chonkie_chunker)
nodes = parser.get_nodes_from_documents(documents)
```

### SentenceSplitter

`SentenceSplitter`, cümle sınırlarını gözeterek metni bölmeye çalışır.

```python
from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,
)
nodes = splitter.get_nodes_from_documents(documents)
```

### SentenceWindowNodeParser

`SentenceWindowNodeParser`, diğer dökümanları tek tek cümlelere bölmesi dışında diğer node parser'lara benzer. Ortaya çıkan node'lar ayrıca meta verilerinde her bir node'un etrafındaki komşu cümle "penceresini" (window) içerir. Bu meta verilerin LLM veya embedding modeli tarafından görülmeyeceğini unutmayın.

Bu, en çok meta verileri çok spesifik bir kapsamı olan embedding'ler oluşturmak için yararlıdır. Ardından, bir `MetadataReplacementNodePostProcessor` ile birleştirilerek, node LLM'e gönderilmeden önce cümle etrafındaki bağlamla değiştirilebilir.

Aşağıda varsayılan ayarlarla ayrıştırıcının kurulumuna dair bir örnek bulunmaktadır. Pratikte, genellikle sadece cümlelerin pencere boyutunu (window size) ayarlamak istersiniz.

```python
from llama_index.core.node_parser import SentenceWindowNodeParser

node_parser = SentenceWindowNodeParser.from_defaults(
    # her iki taraftan kaç cümle yakalanacağı
    window_size=3,
    # çevreleyen cümlelerin penceresini tutan meta veri anahtarı
    window_metadata_key="window",
    # orijinal cümleyi tutan meta veri anahtarı
    original_text_metadata_key="original_sentence",
)
```

Tam bir örneğe [buradan `MetadataReplacementNodePostProcessor` ile birlikte](python/examples/node_postprocessor/metadatareplacementdemo) ulaşabilirsiniz.

### SemanticSplitterNodeParser

"Semantik bölme" (Semantic chunking), Greg Kamradt tarafından 5 seviyeli embedding bölme hakkındaki video eğitiminde önerilen yeni bir kavramdır: [https://youtu.be/8OJC21T2SL4?t=1933](https://youtu.be/8OJC21T2SL4?t=1933).

Metni **sabit** bir parça boyutuna göre bölmek yerine, semantik bölücü embedding benzerliğini kullanarak cümleler arasındaki kırılma noktasını uyarlanabilir şekilde seçer. Bu, bir "parçanın" birbirleriyle semantik olarak ilişkili cümleler içermesini sağlar.

Bunu bir LlamaIndex modülüne uyarladık.

Aşağıdaki notebook'umuza göz atın!

Dikkat edilecek noktalar:

-   Regex birincil olarak İngilizce cümleler için çalışır.
-   Kırılma noktası yüzdelik eşiğini (breakpoint percentile threshold) ayarlamanız gerekebilir.

```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()
splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)
```

Tam bir örneğe [`SemanticSplitterNodeParser` kullanımı kılavuzumuzdan](/python/examples/node_parsers/semantic_chunking) ulaşabilirsiniz.

### TokenTextSplitter

`TokenTextSplitter`, ham token sayılarına göre tutarlı bir parça boyutuyla bölme yapmaya çalışır.

```python
from llama_index.core.node_parser import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=1024,
    chunk_overlap=20,
    separator=" ",
)
nodes = splitter.get_nodes_from_documents(documents)
```

## İlişki Tabanlı Node Parser'lar

### HierarchicalNodeParser

Bu node parser, node'ları hiyerarşik node'lara bölecektir. Bu, tek bir girdinin birkaç parça boyutu hiyerarşisine bölüneceği ve her bir node'un kendi üst (parent) node'una bir referans içereceği anlamına gelir.

`AutoMergingRetriever` ile birleştirildiğinde bu, çocukların çoğunluğu getirildiğinde getirilen node'ları otomatik olarak ebeveynleriyle değiştirmemize olanak tanır. Bu süreç, LLM'e yanıt sentezi için daha eksiksiz bir bağlam sağlar.

```python
from llama_index.core.node_parser import HierarchicalNodeParser

node_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]
)
```

Tam bir örneğe [buradan `AutoMergingRetriever` ile birlikte](python/examples/retrievers/auto_merging_retriever) ulaşabilirsiniz.