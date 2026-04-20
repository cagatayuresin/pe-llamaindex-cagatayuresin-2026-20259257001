# Sorgulama (Querying)

Artık verilerinizi yüklediniz, bir indeks oluşturdunuz ve bu indeksi daha sonra kullanmak üzere sakladınız; bir LLM uygulamasının en önemli kısmına gelmeye hazırsınız: sorgulama.

En basit haliyle sorgulama, bir LLM'e yapılan bir komut (prompt) çağrısıdır: Bir soru sorup yanıt almak, bir özetleme isteği veya çok daha karmaşık bir talimat olabilir.

Daha karmaşık sorgulama; tekrarlanan/zincirlenmiş komut + LLM çağrılarını ve hatta birden çok bileşen arasında bir akıl yürütme (reasoning) döngüsünü içerebilir.

## Başlarken

Tüm sorgulamanın temeli `QueryEngine`'dir (Sorgu Motoru). Bir QueryEngine almanın en basit yolu, indeksi sizin için bir tane oluşturmaya zorlamaktır:

```python
query_engine = index.as_query_engine()
response = query_engine.query(
    "Kullanıcının geçmiş bilgilerini göz önünde bulundurarak ona bir e-posta yaz."
)
print(response)
```

## Sorgulamanın Aşamaları

Ancak sorgulama, ilk bakışta göründüğünden daha fazlasını içerir. Sorgulama üç ayrı aşamadan oluşur:

-   **Getirme (Retrieval)**: `Index`'inizden sorgunuz için en alakalı dökümanları bulup getirdiğiniz aşamadır. [İndeksleme](/python/framework/module_guides/indexing) bölümünde daha önce tartışıldığı gibi, en yaygın getirme türü "top-k" semantik getirmedir, ancak başka birçok getirme stratejisi de mevcuttur.
-   **Son İşleme (Postprocessing)**: Getirilen `Node`'ların isteğe bağlı olarak yeniden sıralandığı (reranked), dönüştürüldüğü veya filtrelendiği aşamadır. Örneğin, belirli anahtar kelimeler gibi spesifik metadatalara sahip olmalarını şart koşabilirsiniz.
-   **Yanıt Sentezleme (Response synthesis)**: Sorgunuzun, en alakalı verilerinizin ve komutunuzun birleştirilip bir yanıt döndürmesi için LLM'inize gönderildiği aşamadır.

> **İpucu:** [Dökümanlara](/python/framework/module_guides/loading/documents_and_nodes/usage_documents) ve [Node'lara](/python/framework/module_guides/loading/documents_and_nodes/usage_nodes) nasıl metadata ekleneceği hakkında bilgi edinebilirsiniz.

## Sorgulama Aşamalarını Özelleştirme

LlamaIndex, sorgulamanız üzerinde ayrıntılı kontrol sağlayan düşük seviyeli bir birleştirme (composition) API'ına sahiptir.

Bu örnekte, getiricimizi (retriever) `top_k` için farklı bir sayı kullanacak şekilde özelleştiriyoruz ve getirilen node'ların dahil edilmesi için minimum bir benzerlik puanına ulaşmasını gerektiren bir son işleme adımı ekliyoruz. Bu, alakalı sonuçlarınız olduğunda size çok fazla veri verecektir; ancak alakalı hiçbir şeyiniz yoksa potansiyel olarak hiç veri vermeyecektir.

```python
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

# indeks oluştur
index = VectorStoreIndex.from_documents(documents)

# getiriciyi (retriever) yapılandır
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

# yanıt sentezleyiciyi yapılandır
response_synthesizer = get_response_synthesizer()

# sorgu motorunu birleştir
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

# sorgula
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

Ayrıca ilgili arayüzleri uygulayarak kendi getirme, yanıt sentezleme ve genel sorgu mantığınızı da ekleyebilirsiniz.

Uygulanan bileşenlerin tam listesi ve desteklenen yapılandırmalar için [referans dökümanlarımıza](/python/framework/api_reference) göz atın.

Her adımı özelleştirme hakkında daha fazla detaya girelim:

### Getiriciyi (Retriever) Yapılandırma

```python
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)
```

[Getiriciler üzerine modül kılavuzumuzda](/python/framework/module_guides/querying/retriever) bilgi edinebileceğiniz çok çeşitli getirici türleri vardır.

### Node Son İşleyicileri Yapılandırma

Getirilen `Node` nesnelerinin alaka düzeyini daha da artırabilen gelişmiş `Node` filtreleme ve zenginleştirme özelliklerini destekliyoruz.
Bu, süreyi/LLM çağrısı sayısını/maliyeti azaltmaya veya yanıt kalitesini artırmaya yardımcı olabilir.

Örneğin:

-   `KeywordNodePostprocessor`: Node'ları `required_keywords` (gerekli anahtar kelimeler) ve `exclude_keywords` (hariç tutulan anahtar kelimeler) parametrelerine göre filtreler.
-   `SimilarityPostprocessor`: Benzerlik puanı üzerine bir eşik belirleyerek node'ları filtreler (bu nedenle yalnızca embedding tabanlı getiriciler tarafından desteklenir).
-   `PrevNextNodePostprocessor`: Getirilen `Node` nesnelerini, `Node` ilişkilerine dayalı olarak ek ilgili bağlamlarla zenginleştirir.

Node son işleyicilerin tam listesi [Node Postprocessor Referansında](/python/framework/api_reference/postprocessor) dökümante edilmiştir.

İstenen node son işleyicileri yapılandırmak için:

```python
node_postprocessors = [
    KeywordNodePostprocessor(
        required_keywords=["Combinator"], exclude_keywords=["Italy"]
    )
]
query_engine = RetrieverQueryEngine.from_args(
    retriever, node_postprocessors=node_postprocessors
)
response = query_engine.query("Yazar büyürken ne yaptı?")
```

### Yanıt Sentezlemeyi Yapılandırma

Bir getirici ilgili node'ları getirdikten sonra, bir `BaseSynthesizer` bilgileri birleştirerek nihai yanıtı sentezler.

Şu şekilde yapılandırabilirsiniz:

```python
query_engine = RetrieverQueryEngine.from_args(
    retriever, response_mode=response_mode
)
```

Şu anda aşağıdaki seçenekleri destekliyoruz:

-   `default`: Getirilen her bir `Node` üzerinden sıralı olarak giderek bir cevap "oluşturur ve rafine eder" (create and refine). Bu, Node başına ayrı bir LLM çağrısı yapar. Daha ayrıntılı cevaplar için iyidir.
-   `compact`: Maksimum komut boyutuna sığabilecek kadar çok `Node` metin parçasını doldurarak her LLM çağrısı sırasında komutu "sıkıştırır" (compact). Bir komuta sığdırılamayacak kadar çok parça varsa, birden fazla komut üzerinden giderek bir cevap "oluşturur ve rafine eder".
-   `tree_summarize`: Verilen bir dizi `Node` nesnesi ve sorgu ile özyinelemeli (recursive) bir ağaç oluşturur ve yanıt olarak kök düğümü döndürür. Özetleme amaçları için iyidir.
-   `no_text`: LLM'e gönderilecek olan node'ları dökümanlardan getirir ancak onları LLM'e göndermeden işlemi bitirir. Daha sonra `response.source_nodes` kontrol edilerek incelenebilir. Yanıt nesnesi Bölüm 5'te daha detaylı ele alınmıştır.
-   `accumulate`: Verilen bir dizi `Node` nesnesi ve sorgu ile, yanıtları bir dizide biriktirirken sorguyu her bir `Node` metin parçasına uygular. Tüm yanıtların birleştirilmiş bir dizesini döndürür. Aynı sorguyu her metin parçasına karşı ayrı ayrı çalıştırmanız gerektiğinde iyidir.

## Yapılandırılmış Çıktılar (Structured Outputs)

Çıktınızın yapılandırılmış olduğundan emin olmak isteyebilirsiniz. Bir sorgu motoru sınıfından bir Pydantic nesnesinin nasıl çıkarılacağını görmek için [Sorgu Motorları + Pydantic Çıktıları](/python/framework/module_guides/querying/structured_outputs/query_engine) bölümümüze bakın.

Ayrıca [Yapılandırılmış Çıktılar](/python/framework/module_guides/querying/structured_outputs) kılavuzumuzun tamamına göz attığınızdan emin olun.

## Kendi Sorgu İş Akışınızı Oluşturma

Karmaşık sorgu akışları tasarlamak istiyorsanız; komutlar/LLM'ler/çıktı ayrıştırıcılardan getiricilere, yanıt sentezleyicilere ve kendi özel bileşenlerinize kadar birçok farklı modül arasında kendi sorgu iş akışınızı oluşturabilirsiniz.

Daha fazla ayrıntı için [İş Akışı Kılavuzumuza](/python/framework/module_guides/workflow) göz atın.