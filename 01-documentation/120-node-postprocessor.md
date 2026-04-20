# Node Postprocessor

## Kavram

Node postprocessor'lar, bir grup node'u alan ve bunları döndürmeden önce bir tür dönüşüm veya filtreleme uygulayan modüllerdir.

LlamaIndex'te node postprocessor'lar en yaygın olarak bir sorgu motoru (query engine) içinde; node getirme (retrieval) adımından sonra ve yanıt sentezi (synthesis) adımından önce uygulanır.

LlamaIndex, doğrudan kullanım için birkaç node postprocessor sunarken, aynı zamanda kendi özel postprocessor'larınızı eklemeniz için basit bir API sağlar.

<Aside type="tip">
  Node postprocessor'ın RAG iş akışında nereye oturduğu konusunda kafanız mı karıştı?
  [Üst düzey kavramlar](/python/getting_started/concepts) hakkında bilgi edinin.
</Aside>

## Kullanım Kalıbı (Usage Pattern)

Bir node postprocessor kullanımına dair örnek aşağıdadır:

```python
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore

nodes = [
    NodeWithScore(node=Node(text="metin1"), score=0.7),
    NodeWithScore(node=Node(text="metin2"), score=0.8),
]

# similarity postprocessor: 0.75 benzerlik puanının altındaki node'ları filtrele
processor = SimilarityPostprocessor(similarity_cutoff=0.75)
filtered_nodes = processor.postprocess_nodes(nodes)

# cohere rerank: eğitilmiş model kullanarak verilen sorguya göre node'ları yeniden sırala (rerank)
reranker = CohereRerank(api_key="<COHERE_API_KEY>", top_n=2)
reranker.postprocess_nodes(nodes, query_str="<kullanici_sorgusu>")
```

`postprocess_nodes` fonksiyonunun hem `query_str` hem de `query_bundle` (`QueryBundle`) alabildiğini, ancak her ikisini birden alamayacağını unutmayın.

## Kullanım Kalıbı

En yaygın olarak node postprocessor'lar; bir retriever'dan döndürülen node'lara uygulandıkları ve yanıt sentezi adımından önce çalıştırıldıkları bir sorgu motorunda kullanılırlar.

## Bir Sorgu Motoruyla Kullanma

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.postprocessor import TimeWeightedPostprocessor

documents = SimpleDirectoryReader("./data").load_data()

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(
    node_postprocessors=[
        TimeWeightedPostprocessor(
            time_decay=0.5, time_access_refresh=False, top_k=1
        )
    ]
)

# tüm node postprocessor'lar her sorgu sırasında uygulanacaktır
response = query_engine.query("sorgu metni")
```

## Getirilen Node'larla Kullanma

Veya getirilen node'ları filtrelemek için bağımsız bir nesne olarak kullanılır:

```python
from llama_index.core.postprocessor import SimilarityPostprocessor

nodes = index.as_retriever().retrieve("test sorgu metni")

# 0.75 benzerlik puanının altındaki node'ları filtrele
processor = SimilarityPostprocessor(similarity_cutoff=0.75)
filtered_nodes = processor.postprocess_nodes(nodes)
```

## Kendi Node'larınızla Kullanma

Fark etmiş olabileceğiniz gibi, postprocessor'lar girdi olarak `NodeWithScore` nesnelerini alır; bu, bir `Node` ve bir `puan` (score) değerini içeren basit bir sarmalayıcı (wrapper) sınıftır.

```python
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.data_structs import Node
from llama_index.core.schema import NodeWithScore

nodes = [
    NodeWithScore(node=Node(text="metin"), score=0.7),
    NodeWithScore(node=Node(text="metin"), score=0.8),
]

# 0.75 benzerlik puanının altındaki node'ları filtrele
processor = SimilarityPostprocessor(similarity_cutoff=0.75)
filtered_nodes = processor.postprocess_nodes(nodes)
```

## Özel Node PostProcessor (Custom Node PostProcessor)

Temel sınıf `BaseNodePostprocessor`'dır ve API arayüzü oldukça basittir:

```python
class BaseNodePostprocessor:
    """Node postprocessor."""

    @abstractmethod
    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle]
    ) -> List[NodeWithScore]:
        """Node'ları sonradan işle (postprocess)."""
```

Basit bir node postprocessor sadece birkaç satır kodla uygulanabilir:

```python
from llama_index.core import QueryBundle
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore


class TaslakNodePostprocessor(BaseNodePostprocessor):
    def _postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle]
    ) -> List[NodeWithScore]:
        # puandan 1 çıkarır
        for n in nodes:
            n.score -= 1

        return nodes
```

## Modüller

Daha fazla detay için tam [modül listesine](/python/framework/module_guides/querying/node_postprocessors/node_postprocessors) göz atın.