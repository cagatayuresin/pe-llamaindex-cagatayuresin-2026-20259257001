# Maliyet Analizi

## Konsept

Bir LLM'e yapılan her çağrı belirli bir miktar paraya mal olacaktır; örneğin, OpenAI'ın gpt-3.5-turbo modeli 1000 token başına 0.002 dolar maliyete sahiptir. Bir indeksi oluşturma ve sorgulama maliyeti şunlara bağlıdır:

-   Kullanılan LLM türü
-   Kullanılan veri yapısı türü
-   Oluşturma sırasında kullanılan parametreler
-   Sorgulama sırasında kullanılan parametreler

Her bir indeksi oluşturma ve sorgulama maliyeti referans dökümantasyonunda henüz tamamlanmamıştır (TODO). Bu sırada aşağıdaki bilgileri sağlıyoruz:

1.  İndekslerin maliyet yapısına genel bir bakış.
2.  Doğrudan LlamaIndex içinde kullanabileceğiniz bir token tahmincisi!

### Maliyet Yapısına Genel Bakış

#### LLM çağrısı gerektirmeyen indeksler

Aşağıdaki indeksler oluşturma sırasında hiçbir LLM çağrısı gerektirmez (0 maliyet):

-   `SummaryIndex`
-   `SimpleKeywordTableIndex`: Her dökümandan anahtar kelimeleri çıkarmak için bir regex anahtar kelime çıkarıcı kullanır.
-   `RAKEKeywordTableIndex`: Her dökümandan anahtar kelimeleri çıkarmak için bir RAKE anahtar kelime çıkarıcı kullanır.

#### LLM çağrısı gerektiren indeksler

Aşağıdaki indeksler oluşturma sırasında LLM çağrısı gerektirir:

-   `TreeIndex`: Ağacı oluşturmak için metni hiyerarşik olarak özetlemek üzere LLM kullanır.
-   `KeywordTableIndex`: Her dökümandan anahtar kelimeleri çıkarmak için LLM kullanır.

### Sorgu Süresi

Nihai cevabı sentezlemek için sorgu süresi boyunca her zaman >= 1 LLM çağrısı yapılacaktır.
Bazı indeksler, indeks oluşturma ve sorgulama arasında maliyet dengeleri (tradeoffs) içerir. Örneğin `SummaryIndex`, oluşturulması ücretsizdir; ancak bir özet indeksi üzerinde (filtreleme veya embedding araması olmadan) bir sorgu çalıştırmak, LLM'i $N$ kez çağıracaktır.

İşte her bir indeksle ilgili bazı notlar:

-   `SummaryIndex`: Varsayılan olarak, N node sayısı olmak üzere $N$ adet LLM çağrısı gerektirir.
-   `TreeIndex`: Varsayılan olarak, N yaprak node (leaf node) sayısı olmak üzere $\log (N)$ adet LLM çağrısı gerektirir.
    -   `child_branch_factor=2` olarak ayarlanması, varsayılan `child_branch_factor=1` değerinden daha pahalı olacaktır (polinomiyal mi logaritmik mi?), çünkü her ebeveyn node için sadece 1 yerine 2 çocuk node üzerinden geçeriz.
-   `KeywordTableIndex`: Varsayılan olarak, sorgu anahtar kelimelerini çıkarmak için bir LLM çağrısı gerektirir.
    -   Sorgu metniniz üzerinde regex/RAKE anahtar kelime çıkarıcılarını da kullanmak için `index.as_retriever(retriever_mode="simple")` veya `index.as_retriever(retriever_mode="rake")` yapabilirsiniz.
-   `VectorStoreIndex`: Varsayılan olarak, sorgu başına bir LLM çağrısı gerektirir. Eğer `similarity_top_k` veya `chunk_size` değerlerini artırırsanız veya `response_mode`'u değiştirirseniz, bu sayı artacaktır.

## Kullanım Kalıbı

LlamaIndex, LLM ve embedding çağrılarının token kullanımını tahmin etmek için token **tahmincileri** (predictors) sunar.
bu, 1) indeks oluşturma ve 2) indeks sorgulama sırasında, herhangi bir LLM çağrısı yapılmadan önce maliyetlerinizi tahmin etmenize olanak tanır.

Tokenler `TokenCountingHandler` geri çağırma yöneticisi kullanılarak sayılır. Kurulumla ilgili detaylar için [örnek notebook'u](/python/examples/observability/tokencountinghandler) inceleyin.

### MockLLM Kullanımı

LLM çağrılarının token kullanımını tahmin etmek için MockLLM'i aşağıda gösterildiği gibi içe aktarın ve örneklendirin. `max_tokens` parametresi, her LLM yanıtının tam olarak o sayıda token içereceği "en kötü durum" tahmini olarak kullanılır. Eğer `max_tokens` belirtilmezse, sadece komutu geri tahmin edecektir.

```python
from llama_index.core.llms import MockLLM
from llama_index.core import Settings

# global olarak bir mock llm kullanın
Settings.llm = MockLLM(max_tokens=256)
```

Daha sonra bu tahminciyi hem indeks oluşturma hem de sorgulama sırasında kullanabilirsiniz.

### MockEmbedding Kullanımı

Ayrıca `MockEmbedding` ile embedding çağrılarının token kullanımını da tahmin edebilirsiniz.

```python
from llama_index.core import MockEmbedding
from llama_index.core import Settings

# global olarak bir mock embedding kullanın
Settings.embed_model = MockEmbedding(embed_dim=1536)
```

## Kullanım Kalıbı

Daha fazla detay için [tam kullanım kalıbını](/python/framework/understanding/evaluating/cost_analysis/usage_pattern) okuyun!