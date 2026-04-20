---
title: Tam Metin Araması (Full-Text Search) ile Milvus Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Tam Metin Araması (Full-Text Search) ile Milvus Vektör Deposu

**Tam metin araması (Full-text search)**, kesin kelime eşleşmesini kullanır ve belgeleri alaka düzeyine göre sıralamak için genellikle BM25 gibi algoritmalar kullanır. **Erişim Destekli Nesil (Retrieval-Augmented Generation - RAG)** sistemlerinde bu yöntem, yapay zeka tarafından oluşturulan yanıtları geliştirmek için ilgili metinleri getirir.

Diğer yandan, **semantik arama**, daha geniş sonuçlar sağlamak için bağlamsal anlamı yorumlar. Her iki yaklaşımı birleştirmek, özellikle tek bir yöntemin yetersiz kaldığı durumlarda bilgi erişimini iyileştiren bir **hibrit arama** oluşturur.

[Milvus 2.5](https://milvus.io/blog/introduce-milvus-2-5-full-text-search-powerful-metadata-filtering-and-more.md)'in Seyrek-BM25 (Sparse-BM25) yaklaşımıyla, ham metin otomatik olarak seyrek vektörlere dönüştürülür. Bu, manuel seyrek gömme (sparse embedding) oluşturma ihtiyacını ortadan kaldırır ve semantik anlama ile anahtar kelime alakasını dengeleyen hibrit bir arama stratejisi sağlar.

Bu eğitimde, tam metin araması ve hibrit arama kullanan bir RAG sistemi oluşturmak için LlamaIndex ve Milvus'u nasıl kullanacağınızı öğreneceksiniz. Önce yalnızca tam metin aramasını uygulayarak başlayacağız ve ardından daha kapsamlı sonuçlar için semantik aramayı entegre ederek sistemi geliştireceğiz.

> Bu eğitime devam etmeden önce, [tam metin araması](https://milvus.io/docs/full-text-search.md#Full-Text-Search) ve [LlamaIndex'te Milvus kullanmanın temelleri](https://milvus.io/docs/integrate_with_llamaindex.md) hakkında bilgi sahibi olduğunuzdan emin olun.

## Ön Koşullar

**Bağımlılıkları kurun**

Başlamadan önce aşağıdaki bağımlılıkların kurulu olduğundan emin olun:

```bash
%pip install llama-index-vector-stores-milvus
%pip install llama-index-embeddings-openai
%pip install llama-index-llms-openai
```

> Google Colab kullanıyorsanız, **çalışma zamanını yeniden başlatmanız** gerekebilir (Arayüzün üst kısmındaki "Runtime" menüsüne gidin ve açılır menüden "Restart session" seçeneğini seçin.)

**Hesapları ayarlayın**

bu eğitim; metin gömmeleri ve cevap oluşturma için OpenAI kullanır. [OpenAI API anahtarını](https://platform.openai.com/api-keys) hazırlamanız gerekir.

```python
import openai


openai.api_key = "sk-"
```

Milvus vektör deposunu kullanmak için Milvus sunucu `URI` (ve isteğe bağlı olarak `TOKEN`) bilginizi belirtin. Bir Milvus sunucusu başlatmak için [Milvus kurulum kılavuzunu](https://milvus.io/docs/install-overview.md) takip ederek bir Milvus sunucusu kurabilir veya ücretsiz olarak [Zilliz Cloud](https://docs.zilliz.com/docs/register-with-zilliz-cloud)'u deneyebilirsiniz.

> Tam metin araması şu anda Milvus Standalone, Milvus Distributed ve Zilliz Cloud'da desteklenmektedir, ancak henüz Milvus Lite'da desteklenmemektedir (gelecekteki uygulama için planlanmıştır). Daha fazla bilgi için <support@zilliz.com> ile iletişime geçin.

```python
URI = "http://localhost:19530"
# TOKEN = ""
```

**Örnek veriyi indir**

Örnek belgeleri "data/paul_graham" dizinine indirmek için aşağıdaki komutları çalıştırın:

```bash
%mkdir -p 'data/paul_graham/'
%wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

## Tam Metin Araması ile RAG

Tam metin aramasını bir RAG sistemine entegre etmek, semantik aramayı hassas ve öngörülebilir anahtar kelime tabanlı erişimle dengeler. Daha iyi arama sonuçları için tam metin aramasını semantik arama ile birleştirmeniz önerilse de, yalnızca tam metin araması kullanmayı da tercih edebilirsiniz. Burada gösterim amacıyla hem tek başına tam metin aramasını hem de hibrit aramayı göstereceğiz.

Başlamak için, Paul Graham'ın "What I Worked On" (Neler Üzerine Çalıştım) makalesini yüklemek için `SimpleDirectoryReader` kullanın:

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


# İlk belgeye göz atalım
print("Örnek belge:\n", documents[0])
```

### BM25 ile Tam Metin Araması

LlamaIndex'in `MilvusVectorStore` bileşeni, verimli anahtar kelime tabanlı erişim sağlayarak tam metin aramasını destekler. `sparse_embedding_function` olarak yerleşik bir işlev kullanarak, arama sonuçlarını sıralamak için BM25 puanlaması uygular.

Bu bölümde, tam metin araması için BM25 kullanan bir RAG sisteminin nasıl uygulanacağını göstereceğiz.

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BM25BuiltInFunction
from llama_index.core import Settings


# Yoğun gömme (dense embedding) modelini atla
Settings.embed_model = None


# Yeni bir koleksiyon oluşturarak Milvus vektör deposunu oluşturun
vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    enable_dense=False,
    enable_sparse=True,  # Tam metin aramasını göstermek için yalnızca seyrek (sparse) olanı etkinleştir
    sparse_embedding_function=BM25BuiltInFunction(),
    overwrite=True,
)


# Belgeleri Milvus'ta saklayın
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Yukarıdaki kod, örnek belgeleri Milvus'a ekler ve tam metin araması için BM25 sıralamasını etkinleştirmek üzere bir indeks oluşturur. Yoğun gömmeyi devre dışı bırakır ve varsayılan parametrelerle `BM25BuiltInFunction` kullanır.

`BM25BuiltInFunction` parametrelerinde giriş ve çıkış alanlarını belirtebilirsiniz:

- `input_field_names (str)`: Giriş metni alanı (varsayılan: "text"). BM25 algoritmasının hangi metin alanına uygulanacağını belirtir. Farklı bir metin alanı adı olan kendi koleksiyonunuzu kullanıyorsanız bunu değiştirin.
- `output_field_names (str)`: Bu BM25 işlevinin çıktılarının saklandığı alan (varsayılan: "sparse_embedding").

Vektör deposu ayarlandıktan sonra, "sparse" veya "text_search" sorgu moduyla Milvus'u kullanarak tam metin araması sorguları gerçekleştirebilirsiniz:

```python
import textwrap


query_engine = index.as_query_engine(
    vector_store_query_mode="sparse", similarity_top_k=5
)
answer = query_engine.query("Yazar Viaweb'de ne öğrendi?")
print(textwrap.fill(str(answer), 100))
```

**"Yazar Viaweb'de birkaç önemli ders öğrendi. Bir girişimin nihai testi olarak büyüme oranının önemini, perakende ve yazılım kullanılabilirliğini anlamak için kullanıcılar adına mağazalar oluşturmanın değerini ve bir pazarda 'giriş seviyesi' seçeneği olmanın önemini öğrendiler. Ayrıca, Viaweb'i ucuz hale getirmenin tesadüfi başarısını, çok fazla insanı işe almanın zorluklarını ve şirket Yahoo tarafından satın alındığında hissedilen rahatlamayı keşfettiler."**

#### Metin analizörünü özelleştirme

Analizörler (analyzers), cümleleri belirteçlere (tokens) ayırarak ve gövdeleme (stemming) ile durdurma kelimelerinin (stop-words) temizlenmesi gibi sözcüksel işlemler gerçekleştirerek tam metin aramasında hayati bir rol oynar. Genellikle dile özeldirler. Daha fazla bilgi için [Milvus Analizör Kılavuzu](https://milvus.io/docs/analyzer-overview.md#Analyzer-Overview)'na bakın.

Milvus iki tür analizörü destekler: **Yerleşik Analizörler (Built-in Analyzers)** ve **Özel Analizörler (Custom Analyzers)**. Varsayılan olarak, `BM25BuiltInFunction`, metni noktalama işaretlerine göre belirteçlere ayıran standart yerleşik analizörü kullanır.

Farklı bir analizör kullanmak veya mevcut olanı özelleştirmek için `analyzer_params` argümanına değer iletebilirsiniz:

```python
bm25_function = BM25BuiltInFunction(
    analyzer_params={
        "tokenizer": "standard",
        "filter": [
            "lowercase",  # Yerleşik filtre
            {"type": "length", "max": 40},  # Tek bir belirtecin özel sınır boyutu
            {"type": "stop", "stop_words": ["of", "to"]},  # Özel durdurma kelimeleri
        ],
    },
    enable_match=True,
)
```

### Yeniden Sıralayıcı (Reranker) ile Hibrit Arama

Hibrit bir arama sistemi, bir RAG sisteminde erişim performansını optimize ederek semantik arama ve tam metin aramasını birleştirir.

Aşağıdaki örnek, semantik arama için OpenAI gömmesini ve tam metin araması için BM25'i kullanır:

```python
# Belgeler üzerinde indeks oluşturun
vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    # enable_dense=True,  # enable_dense varsayılan olarak True'dur
    dim=1536,
    enable_sparse=True,
    sparse_embedding_function=BM25BuiltInFunction(),
    overwrite=True,
    # hybrid_ranker="RRFRanker",  # hybrid_ranker varsayılan olarak "RRFRanker"dır
    # hybrid_ranker_params={},  # hybrid_ranker_params varsayılan olarak {}'dır
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model="default",  # "default" OpenAI gömmesini kullanacaktır
)
```

**Nasıl çalışır?**

Bu yaklaşım, belgeleri her iki vektör alanıyla birlikte bir Milvus koleksiyonunda saklar:

- `embedding`: Semantik arama için OpenAI gömme modeli tarafından oluşturulan yoğun gömmeler.
- `sparse_embedding`: Tam metin araması için BM25BuiltInFunction kullanılarak hesaplanan seyrek gömmeler.

Ek olarak, varsayılan parametreleriyle "RRFRanker" kullanan bir yeniden sıralama (reranking) stratejisi uyguladık. Yeniden sıralayıcıyı özelleştirmek için [Milvus Yeniden Sıralama Kılavuzu](https://milvus.io/docs/reranking.md)'nu takip ederek `hybrid_ranker` ve `hybrid_ranker_params` yapılandırmasını yapabilirsiniz.

Şimdi, RAG sistemini örnek bir sorgu ile test edelim:

```python
# Sorgu
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=5
)
answer = query_engine.query("Yazar Viaweb'de ne öğrendi?")
print(textwrap.fill(str(answer), 100))
```

**"Yazar Viaweb'de birkaç önemli ders öğrendi. Bunlar arasında, bir girişimin nihai testi olarak büyüme oranını anlamanın önemi, çok fazla insanı işe almanın etkisi, yatırımcıların insafına kalmanın zorlukları ve Yahoo şirketi satın aldığında yaşanan rahatlama yer alıyordu. Ayrıca yazar, kullanıcı geri bildirimlerinin önemini, kullanıcılar için mağazalar oluşturmanın değerini ve büyüme oranının bir girişimin uzun vadeli başarısı için çok önemli olduğu gerçeğini öğrendi."**

bu hibrit yaklaşım, hem semantik hem de anahtar kelime tabanlı erişimden yararlanarak bir RAG sisteminde daha doğru ve bağlam odaklı yanıtlar sağlar.
