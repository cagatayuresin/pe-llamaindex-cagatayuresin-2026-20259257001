# Node'ları Tanımlama ve Özelleştirme

Node'lar, kaynak Dökümanların (Documents) "parçalarını" (chunks) temsil eder; bu bir metin parçası, bir görsel veya daha fazlası olabilir. Ayrıca meta verileri ve diğer node'lar ile indeks yapılarıyla olan ilişki bilgilerini de içerirler.

Node'lar LlamaIndex'te birinci sınıf vatandaştır. Node'ları ve tüm özniteliklerini doğrudan tanımlamayı seçebilirsiniz. Ayrıca, kaynak Dökümanları `NodeParser` sınıflarımız aracılığıyla Node'lara "ayrıştırmayı" (parse) da seçebilirsiniz.

Örneğin, şunları yapabilirsiniz:

```python
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter()

nodes = parser.get_nodes_from_documents(documents)
```

Node nesnelerini manuel olarak oluşturmayı ve ilk bölümü atlamayı da seçebilirsiniz. Örneğin:

```python
from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo

node1 = TextNode(text="<metin_parçası>", id_="<node_id>")
node2 = TextNode(text="<metin_parçası>", id_="<node_id>")

# ilişkileri ayarla
node1.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(
    node_id=node2.node_id
)
node2.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(
    node_id=node1.node_id
)
nodes = [node1, node2]
```

`RelatedNodeInfo` sınıfı, gerekirse ek `metadata` (meta veri) da saklayabilir:

```python
node2.relationships[NodeRelationship.PARENT] = RelatedNodeInfo(
    node_id=node1.node_id, metadata={"key": "val"}
)
```

### Kimliği (ID) Özelleştirme

Her node, manuel olarak belirtilmezse otomatik olarak oluşturulan bir `node_id` özelliğine sahiptir. Bu kimlik çeşitli amaçlar için kullanılabilir; bunlar arasında depolamadaki node'ları güncelleyebilmek, node'lar arasında (`IndexNode` aracılığıyla) ilişkiler tanımlayabilmek ve daha fazlası yer alır.

Herhangi bir `TextNode` nesnesinin `node_id` değerini doğrudan alabilir ve ayarlayabilirsiniz.

```python
print(node.node_id)
node.node_id = "Yeni node_id değerim!"
```