# İndeksleme (Indexing)

Verileriniz yüklendikten sonra artık bir Document nesneleri listeniz (veya bir Node'lar listeniz) var. Şimdi, bu nesneleri sorgulamaya başlayabilmek için üzerlerinde bir `Index` (İndeks) oluşturma zamanı.

## İndeks (Index) Nedir?

LlamaIndex terimleriyle bir `Index`, bir LLM tarafından sorgulanmaya olanak tanımak üzere tasarlanmış, `Document` nesnelerinden oluşan bir veri yapısıdır. İndeksiniz, sorgulama stratejinizi tamamlayacak şekilde tasarlanmıştır.

LlamaIndex birkaç farklı indeks türü sunar. Burada en yaygın iki tanesini ele alacağız.

## Vektör Deposu İndeksi (Vector Store Index)

`VectorStoreIndex`, açık ara en sık karşılaşacağınız İndeks türüdür. Vektör Deposu İndeksi, Dökümanlarınızı alır ve onları Node'lara böler. Ardından, her bir node'un metni için bir LLM tarafından sorgulanmaya hazır `vektör gömmeleri` (vector embeddings) oluşturur.

### Embedding nedir?

`Vektör gömmeleri` (vector embeddings), LLM uygulamalarının işleyişinin merkezinde yer alır.

Genellikle sadece embedding olarak adlandırılan bir `vektör gömmesi`, **metninizin semantiğinin veya anlamının sayısal bir temsilidir**. Benzer anlamlara sahip iki metin parçası, asıl metinler oldukça farklı olsa bile matematiksel olarak benzer gömmelere sahip olacaktır.

Bu matematiksel ilişki, kullanıcının sorgu terimleri sağladığı ve LlamaIndex'in basit anahtar kelime eşleşmesi yerine **sorgu terimlerinin anlamıyla** ilgili metinleri bulabildiği **semantik aramayı** (semantic search) mümkün kılar. Bu, Veri Getirme ile Güçlendirilmiş Üretim'in (RAG) ve genel olarak LLM'lerin nasıl çalıştığının büyük bir parçasıdır.

[Birçok embedding türü](/python/framework/module_guides/models/embeddings) vardır ve bunlar verimlilik, etkinlik ve hesaplama maliyeti açısından farklılık gösterir. Varsayılan olarak LlamaIndex, OpenAI tarafından kullanılan varsayılan embedding olan `text-embedding-ada-002`'yi kullanır. Farklı LLM'ler kullanıyorsanız genellikle farklı embedding'ler kullanmak isteyeceksiniz.

### Vektör Deposu İndeksi dökümanlarınızı gömer (embeds)

Vektör Deposu İndeksi, LLM'inizden gelen bir API'yi kullanarak tüm metninizi embedding'lere dönüştürür; "metninizi gömer (embeds)" denildiğinde kastedilen budur. Çok fazla metniniz varsa, birçok gidiş-dönüş API çağrısı içerdiği için embedding oluşturmak uzun zaman alabilir.

Embedding'lerinizde arama yapmak istediğinizde, sorgunuzun kendisi bir vektör gömmesine dönüştürülür ve ardından sorgunuzla semantik olarak ne kadar benzer olduklarına göre tüm gömmeleri sıralamak için VectorStoreIndex tarafından matematiksel bir işlem gerçekleştirilir.

### Top K Getirme (Retrieval)

Sıralama tamamlandığında, VectorStoreIndex en benzer gömmeleri karşılık gelen metin parçaları olarak döndürür. Döndürdüğü gömme sayısı `k` olarak bilinir, bu nedenle kaç tane gömme döndürüleceğini kontrol eden parametre `top_k` olarak bilinir. Bu arama türünün tamamı bu nedenle genellikle "top-k semantik getirme" olarak adlandırılır.

Top-k getirme, bir vektör indeksini sorgulamanın en basit yoludur; [sorgulama](/python/framework/understanding/rag/querying) bölümünü okuduğunuzda daha karmaşık ve ince stratejiler hakkında bilgi edineceksiniz.

### Vektör Deposu İndeksini Kullanma

Vektör Deposu İndeksini kullanmak için, yükleme aşamasında oluşturduğunuz Document listesini ona geçirin:

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
```

> **İpucu:** `from_documents` metodu ayrıca isteğe bağlı bir `show_progress` argümanı alır. İndeks oluşturma sırasında bir ilerleme çubuğu görüntülemek için bunu `True` olarak ayarlayın.

Ayrıca doğrudan bir Node nesnesi listesi üzerinde bir indeks oluşturmayı da seçebilirsiniz:

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(nodes)
```

Metniniz indekslendiğine göre, teknik olarak artık [sorgulamaya](/python/framework/understanding/rag/querying) hazır! Ancak tüm metninizi gömmek zaman alıcı olabilir ve barındırılan bir LLM kullanıyorsanız pahalı da olabilir. Zaman ve paradan tasarruf etmek için önce [gömmelerinizi saklamak](/python/framework/understanding/rag/storing) isteyeceksiniz.

## Özet İndeksi (Summary Index)

Özet İndeksi, adından da anlaşılacağı gibi, Dökümanlarınızdaki metnin bir özetini oluşturmaya çalıştığınız sorgular için en uygun olan daha basit bir İndeks formudur. Tüm Dökümanları basitçe saklar ve hepsini sorgu motorunuza döndürür.

## Daha Fazla Okuma

Verileriniz birbirine bağlı kavramlardan oluşan bir küme (bilgisayar bilimleri terimiyle bir "graf") ise, [bilgi grafiği indeksimizle](/python/examples/index_structs/knowledge_graph/knowledgegraphdemo) (knowledge graph index) ilgilenebilirsiniz.