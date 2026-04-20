# Soru-Cevap (Q&A) Kalıpları

## Anlamsal Arama (Semantic Search)

LlamaIndex'in en temel kullanım örneği anlamsal aramadır. Başlamanız için size basit bir bellek içi (in-memory) vektör deposu sağlıyoruz ancak [vektör deposu entegrasyonlarımızdan](/python/framework/community/integrations/vector_stores) herhangi birini de kullanmayı seçebilirsiniz:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Yazar büyürken ne yaptı?")
print(response)
```

**Eğitimler**

-   [Başlangıç Eğitimi](/python/framework/getting_started/starter_example)
-   [Temel Kullanım Kalıbı](/python/framework/module_guides/querying)

**Kılavuzlar**

-   [Örnek Notebook](/python/examples/vector_stores/simpleindexdemo)

## Özetleme (Summarization)

Bir özetleme sorgusu, bir cevabı sentezlemek için LLM'in dökümanların çoğunu, hatta tamamını gözden geçirmesini gerektirir. Örneğin, bir özetleme sorgusu şunlardan birine benzeyebilir:

-   "Bu metin koleksiyonunun özeti nedir?"
-   "X kişisinin şirketle olan deneyiminin bir özetini verin."

Genel olarak, bir özet indeksi (summary index) bu kullanım durumu için uygun olacaktır. Bir özet indeksi varsayılan olarak tüm verileri gözden geçirir.

Deneysel olarak, `response_mode="tree_summarize"` ayarını yapmak da daha iyi özetleme sonuçlarına yol açar.

```python
index = SummaryIndex.from_documents(documents)

query_engine = index.as_query_engine(response_mode="tree_summarize")
response = query_engine.query("<özetleme_sorgusu>")
```

## Yapılandırılmış Veriler Üzerinde Sorgulama

LlamaIndex; ister bir Pandas DataFrame ister bir SQL veritabanı olsun, yapılandırılmış veriler üzerinde sorgulamayı destekler.

İşte bazı ilgili kaynaklar:

**Eğitimler**

-   [Metinden SQL'e Geçiş Kılavuzu](/python/framework/understanding/putting_it_all_together/structured_data)

**Kılavuzlar**

-   [SQL Kılavuzu (Temel)](/python/examples/index_structs/struct_indices/sqlindexdemo) ([Notebook](https://github.com/jerryjliu/llama_index/blob/main/docs../../examples/index_structs/struct_indices/SQLIndexDemo.ipynb))
-   [Pandas Demosu](/python/examples/query_engine/pandas_query_engine) ([Notebook](https://github.com/jerryjliu/llama_index/blob/main/docs../../examples/query_engine/pandas_query_engine.ipynb))

## Heterojen Veriler Üzerinde Yönlendirme (Routing)

LlamaIndex, `RouterQueryEngine` ile heterojen veri kaynakları üzerinde yönlendirmeyi de destekler - örneğin bir sorguyu temel bir dökümana veya bir alt indekse "yönlendirmek" isterseniz.

Bunu yapmak için önce farklı veri kaynakları üzerinde alt indeksler oluşturun. Ardından ilgili sorgu motorlarını oluşturun ve bir `QueryEngineTool` elde etmek için her sorgu motoruna bir açıklama verin.

```python
from llama_index.core import TreeIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool

...

# alt indeksleri tanımla
index1 = VectorStoreIndex.from_documents(notion_docs)
index2 = VectorStoreIndex.from_documents(slack_docs)

# sorgu motorlarını ve araçlarını tanımla
tool1 = QueryEngineTool.from_defaults(
    query_engine=index1.as_query_engine(),
    description="Bu sorgu motorunu ... yapmak için kullanın",
)
tool2 = QueryEngineTool.from_defaults(
    query_engine=index2.as_query_engine(),
    description="Bu sorgu motorunu başka bir şey için kullanın...",
)
```

Ardından, üzerlerinde bir `RouterQueryEngine` tanımlıyoruz. Varsayılan olarak bu, yönlendirici olarak bir `LLMSingleSelector` kullanır; bu, verilen açıklamaları dikkate alarak sorguyu en iyi alt indekse yönlendirmek için LLM'i kullanır.

```python
from llama_index.core.query_engine import RouterQueryEngine

query_engine = RouterQueryEngine.from_defaults(
    query_engine_tools=[tool1, tool2]
)

response = query_engine.query(
    "Notion'da, ürün yol haritasının (product roadmap) bir özetini verin."
)
```

**Kılavuzlar**

-   [Yönlendirici Sorgu Motoru Kılavuzu](/python/examples/query_engine/retrieverrouterqueryengine)

## Karşılaştırma/Karşıtlaştırma Sorguları

Bir `ComposableGraph` içindeki bir **sorgu dönüştürme (query transformation)** modülü ile açıkça karşılaştırma/karşıtlaştırma sorguları gerçekleştirebilirsiniz.

```python
from llama_index.core.query.query_transform.base import DecomposeQueryTransform

decompose_transform = DecomposeQueryTransform(
    service_context.llm, verbose=True
)
```

Bu modül, karmaşık bir sorguyu mevcut indeks yapınız üzerinde daha basit bir sorguya dönüştürmenize yardımcı olacaktır.

**Kılavuzlar**

-   [Sorgu Dönüştürmeleri](/python/framework/optimizing/advanced_retrieval/query_transformations)

Ayrıca karşılaştırma/karşıtlaştırma sorgularının yapılıp yapılmayacağını *çıkarması (infer)* için LLM'e de güvenebilirsiniz (aşağıdaki Çoklu Döküman Sorguları bölümüne bakın).

## Çoklu Döküman Sorguları

Yukarıda açıklanan açık sentezleme/yönlendirme akışlarının yanı sıra, LlamaIndex genel çoklu döküman sorgularını da destekleyebilir. Bunu `SubQuestionQueryEngine` sınıfımız aracılığıyla yapabilir. Bir sorgu verildiğinde; bu sorgu motoru, nihai cevabı sentezlemeden önce alt dökümanlara yönelik alt sorguları içeren bir "sorgu planı" oluşturacaktır.

Bunu yapmak için önce her döküman/veri kaynağı için bir indeks tanımlayın ve onu bir `QueryEngineTool` ile sarmalayın (yukarıdakine benzer şekilde):

```python
from llama_index.core.tools import QueryEngineTool

query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=sept_engine,
        name="sept_22",
        description="Eylül 2022'de sona eren Uber çeyrek mali durumları hakkında bilgi sağlar",
    ),
    QueryEngineTool.from_defaults(
        query_engine=june_engine,
        name="june_22",
        description="Haziran 2022'de sona eren Uber çeyrek mali durumları hakkında bilgi sağlar",
    ),
    QueryEngineTool.from_defaults(
        query_engine=march_engine,
        name="march_22",
        description="Mart 2022'de sona eren Uber çeyrek mali durumları hakkında bilgi sağlar",
    ),
]
```

Ardından, bu araçlar üzerinde bir `SubQuestionQueryEngine` tanımlıyoruz:

```python
from llama_index.core.query_engine import SubQuestionQueryEngine

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools
)
```

Bu sorgu motoru, nihai yanıtı sentezlemeden önce herhangi bir sorgu motoru aracı alt kümesine karşı istediği sayıda alt sorgu yürütebilir. Bu, onu belirli bir dökümanla ilgili sorguların yanı sıra dökümanlar arası karşılaştırma/karşıtlaştırma sorguları için özellikle uygun hale getirir.

**Kılavuzlar**

-   [Alt Soru Sorgu Motoru (Giriş)](/python/examples/query_engine/sub_question_query_engine)
-   [10Q Analizi (Uber)](/python/examples/usecases/10k_sub_question)
-   [10K Analizi (Uber ve Lyft)](/python/examples/usecases/10k_sub_question)

## Çok Adımlı Sorgular

LlamaIndex ayrıca yinelemeli çok adımlı sorguları da destekleyebilir. Karmaşık bir sorgu verildiğinde, onu ilk alt sorulara ayırın ve nihai yanıt dönene kadar dönen yanıtlara dayalı olarak sırayla alt sorular oluşturun.

Örneğin, "Yazarın başlattığı hızlandırıcı programının (accelerator program) ilk döneminde kimler vardı?" sorusu verildiğinde; modül önce sorguyu "Yazarın başlattığı hızlandırıcı programı neydi?" şeklinde daha basit bir başlangıç sorusuna dönüştürecek, indeksi sorgulayacak ve ardından takip soruları soracaktır.

**Kılavuzlar**

-   [Sorgu Dönüştürmeleri](/python/framework/optimizing/advanced_retrieval/query_transformations)
-   [Çok Adımlı Sorgu Ayrıştırma](/python/examples/query_transformations/hydequerytransformdemo)

## Zaman Karakterli (Temporal) Sorgular

LlamaIndex zamanın anlaşılmasını gerektiren sorguları destekleyebilir. Bunu iki şekilde yapabilir:

-   Soruyu yanıtlamak için ek bağlam getirmek üzere node'lar arasındaki zamansal ilişkilerin (önceki/sonraki ilişkileri) kullanılması gerekip gerekmediğine karar vermek.
-   Giderek eskiye göre (recency) sıralama ve güncelliğini yitirmiş bağlamı filtreleme.

**Kılavuzlar**

-   [İşlem Sonrası (Postprocessing) Kılavuzu](/python/framework/module_guides/querying/node_postprocessors/node_postprocessors)
-   [Önceki/Sonraki (Prev/Next) İşleme](/python/examples/node_postprocessor/prevnextpostprocessordemo)
-   [Yenilik (Recency) İşleme](/python/examples/node_postprocessor/recencypostprocessordemo)

## Ek Kaynaklar

-   [Terim ve Tanımları Çıkarma Kılavuzu](/python/framework/understanding/putting_it_all_together/q_and_a/terms_definitions_tutorial)
-   [SEC 10k Analizi](https://medium.com/@jerryjliu98/how-unstructured-and-llamaindex-can-help-bring-the-power-of-llms-to-your-own-data-3657d063e30d)