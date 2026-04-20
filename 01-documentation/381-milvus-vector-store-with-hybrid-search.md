---
title: Hibrit Arama (Hybrid Search) ile Milvus Vektör Deposu
 | LlamaIndex OSS Belgeleri
---

# Hibrit Arama (Hybrid Search) ile Milvus Vektör Deposu

Hibrit arama, daha doğru ve bağlamsal olarak ilgili sonuçlar sunmak için hem semantik erişimin hem de anahtar kelime eşleştirmenin güçlü yanlarından yararlanır. Semantik arama ve anahtar kelime eşleştirmenin avantajlarını birleştiren hibrit arama, özellikle karmaşık bilgi erişim görevlerinde etkilidir.

Bu not defteri, LlamaIndex RAG boru hatlarında (pipelines) hibrit arama için Milvus'un nasıl kullanılacağını göstermektedir. Önerilen varsayılan hibrit arama (semantik + BM25) ile başlayacağız ve ardından diğer alternatif seyrek gömme (sparse embedding) yöntemlerini ve hibrit yeniden sıralayıcının (reranker) özelleştirilmesini keşfedeceğiz.

## Ön Koşullar

**Bağımlılıkları kurun**

Başlamadan önce aşağıdaki bağımlılıkların kurulu olduğundan emin olun:

```bash
! pip install llama-index-vector-stores-milvus
! pip install llama-index-embeddings-openai
! pip install llama-index-llms-openai
```

> Google Colab kullanıyorsanız, **çalışma zamanını yeniden başlatmanız** gerekebilir (Ekranın üst kısmındaki "Runtime" menüsüne gidin ve açılır menüden "Restart session" seçeneğini seçin.)

**Hesapları ayarlayın**

Bu eğitim; metin gömmeleri ve cevap oluşturma için OpenAI kullanır. [OpenAI API anahtarını](https://platform.openai.com/api-keys) hazırlamanız gerekir.

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

**Örnek veriyi yükle**

Örnek belgeleri "data/paul_graham" dizinine indirmek için aşağıdaki komutları çalıştırın:

```bash
! mkdir -p 'data/paul_graham/'
! wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

Ardından, Paul Graham'ın "What I Worked On" (Neler Üzerine Çalıştım) makalesini yüklemek için `SimpleDirectoryReader` kullanın:

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham/").load_data()


# İlk belgeye göz atalım
print("Örnek belge:\n", documents[0])
```

## BM25 ile Hibrit Arama

Bu bölüm, BM25 kullanarak hibrit bir aramanın nasıl gerçekleştirileceğini gösterir. Başlamak için `MilvusVectorStore`'u başlatacağız ve örnek belgeler için bir indeks oluşturacağız. Varsayılan yapılandırma şunları kullanır:

- Varsayılan gömme modelinden gelen yoğun gömmeler (OpenAI'nin `text-embedding-ada-002` modeli)
- `enable_sparse` True ise tam metin araması için BM25
- Hibrit arama etkinleştirilmişse sonuçları birleştirmek için k=60 ile `RRFRanker`

```python
# Belgeler üzerinde bir indeks oluşturun
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext, VectorStoreIndex


vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    dim=1536,  # vektör boyutu gömme modeline bağlıdır
    enable_sparse=True,  # BM25 kullanarak varsayılan tam metin aramasını etkinleştir
    overwrite=True,  # koleksiyon zaten varsa sil ve yeniden oluştur
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

İşte `MilvusVectorStore` içindeki yoğun (dense) ve seyrek (sparse) alanları yapılandırmak için argümanlar hakkında daha fazla bilgi:

**Yoğun (dense) alan**

- `enable_dense (bool)`: Yoğun gömmeyi etkinleştirmek veya devre dışı bırakmak için bir bayrak. Varsayılan olarak True'dur.
- `dim (int, isteğe bağlı)`: Koleksiyon için gömme vektörlerinin boyutu.
- `embedding_field (str, isteğe bağlı)`: Koleksiyon için yoğun gömme alanının adı, varsayılan olarak DEFAULT_EMBEDDING_KEY.
- `index_config (dict, isteğe bağlı)`: Yoğun gömme indeksini oluşturmak için kullanılan yapılandırma. Varsayılan olarak None'dır.
- `search_config (dict, isteğe bağlı)`: Milvus yoğun indeksinde arama yapmak için kullanılan yapılandırma. Bunun `index_config` tarafından belirtilen indeks tipiyle uyumlu olması gerektiğini unutmayın. Varsayılan olarak None'dır.
- `similarity_metric (str, isteğe bağlı)`: Yoğun gömme için kullanılacak benzerlik metriği; şu anda IP, COSINE ve L2 desteklenmektedir.

**Seyrek (sparse) alan**

- `enable_sparse (bool)`: Seyrek gömmeyi etkinleştirmek veya devre dışı bırakmak için bir bayrak. Varsayılan olarak False'dur.
- `sparse_embedding_field (str)`: Seyrek gömme alanının adı, varsayılan olarak DEFAULT_SPARSE_EMBEDDING_KEY.
- `sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], isteğe bağlı)`: Eğer `enable_sparse` True ise, metni seyrek gömmeye dönüştürmek için bu nesne sağlanmalıdır. None ise, varsayılan seyrek gömme işlevi (BM25BuiltInFunction) kullanılır veya yerleşik işlevleri olmayan mevcut koleksiyon için BGEM3SparseEmbedding kullanılır.
- `sparse_index_config (dict, isteğe bağlı)`: Seyrek gömme indeksini oluşturmak için kullanılan yapılandırma. Varsayılan olarak None'dır.

Sorgulama aşamasında hibrit aramayı etkinleştirmek için `vector_store_query_mode` parametresini "hybrid" olarak ayarlayın. Bu, hem semantik arama hem de tam metin aramasından gelen arama sonuçlarını birleştirecek ve yeniden sıralayacaktır. Örnek bir sorguyla test edelim: "Yazar Viaweb'de ne öğrendi?":

```python
import textwrap


query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=5
)
response = query_engine.query("Yazar Viaweb'de ne öğrendi?")
print(textwrap.fill(str(response), 100))
```

**"Yazar Viaweb'de perakendeciliği, kullanıcı geri bildirimlerinin önemini ve bir girişimin nihai testi olarak büyüme oranının önemini öğrendi."**

### Metin analizörünü özelleştirme

Analizörler (analyzers), cümleleri belirteçlere (tokens) ayırarak ve gövdeleme (stemming) ile durdurma kelimelerinin (stop-word) temizlenmesi gibi sözcüksel işlemler gerçekleştirerek tam metin aramasında hayati bir rol oynar. Genellikle dile özeldirler. Daha fazla bilgi için [Milvus Analizör Kılavuzu](https://milvus.io/docs/analyzer-overview.md#Analyzer-Overview)'na bakın.

Milvus iki tür analizörü destekler: **Yerleşik Analizörler (Built-in Analyzers)** ve **Özel Analizörler (Custom Analyzers)**. Varsayılan olarak, `enable_sparse` True olarak ayarlanmışsa, `MilvusVectorStore`, metni noktalama işaretlerine göre belirteçlere ayıran standart yerleşik analizörü kullanan varsayılan yapılandırmalı `BM25BuiltInFunction`'ı kullanır.

Farklı bir analizör kullanmak veya mevcut olanı özelleştirmek için `BM25BuiltInFunction` oluştururken `analyzer_params` argümanına değerler sağlayabilirsiniz. Ardından, bu işlevi `MilvusVectorStore` içinde `sparse_embedding_function` olarak ayarlayın.

```python
from llama_index.vector_stores.milvus.utils import BM25BuiltInFunction


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


vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    dim=1536,
    enable_sparse=True,
    sparse_embedding_function=bm25_function,  # Özel analizörlü BM25
    overwrite=True,
)
```

## Diğer Seyrek Gömmeler (Sparse Embeddings) ile Hibrit Arama

Semantik aramayı BM25 ile birleştirmenin yanı sıra Milvus, [BGE-M3](https://arxiv.org/abs/2402.03216) gibi bir seyrek gömme işlevi kullanarak hibrit aramayı da destekler. Aşağıdaki örnek, seyrek gömmeler oluşturmak için yerleşik `BGEM3SparseEmbeddingFunction`'ı kullanır.

İlk olarak `FlagEmbedding` paketini kurmamız gerekiyor:

```bash
! pip install -q FlagEmbedding
```

Ardından, yoğun gömme için varsayılan OpenAI modelini ve seyrek gömme için yerleşik BGE-M3'ü kullanarak vektör deposunu ve indeksi oluşturalım:

```python
from llama_index.vector_stores.milvus.utils import BGEM3SparseEmbeddingFunction


vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    dim=1536,
    enable_sparse=True,
    sparse_embedding_function=BGEM3SparseEmbeddingFunction(),
    overwrite=True,
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
```

Şimdi örnek bir soruyla hibrit arama sorgusu gerçekleştirelim:

```python
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=5
)
response = query_engine.query("Yazar Viaweb'de ne öğrendi??")
print(textwrap.fill(str(response), 100))
```

**"Yazar; perakendeciliği, kullanıcı geri bildirimlerinin önemini, bir girişimde büyüme oranının değerini, fiyatlandırma stratejisinin önemini, saygın olmayan işler üzerinde çalışmanın faydalarını ve bir girişimi yönetmenin zorluklarını ve ödüllerini öğrendi."**

### Seyrek Gömme İşlevini Özelleştirme

Seyrek gömme işlevini, aşağıdaki yöntemleri içeren `BaseSparseEmbeddingFunction` sınıfından miras aldığı sürece özelleştirebilirsiniz:

- `encode_queries`: Bu yöntem, metinleri sorgular için seyrek gömme listesine dönüştürür.
- `encode_documents`: Bu yöntem, metinleri belgeler için seyrek gömme listesine dönüştürür.

Her yöntemin çıktısı, sözlüklerden oluşan bir liste olan seyrek gömme formatını takip etmelidir. Her sözlük, boyutu temsil eden bir anahtara (tam sayı) ve o boyuttaki gömmenin büyüklüğünü temsil eden karşılık gelen bir değere (kayan noktalı sayı) sahip olmalıdır (örneğin, {1: 0.5, 2: 0.3}).

Örneğin, işte BGE-M3 kullanan özel bir seyrek gömme işlevi uygulaması:

```python
from FlagEmbedding import BGEM3FlagModel
from typing import List
from llama_index.vector_stores.milvus.utils import BaseSparseEmbeddingFunction




class ÖrnekGömmeİşlevi(BaseSparseEmbeddingFunction):
    def __init__(self):
        self.model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False)


    def encode_queries(self, queries: List[str]):
        outputs = self.model.encode(
            queries,
            return_dense=False,
            return_sparse=True,
            return_colbert_vecs=False,
        )["lexical_weights"]
        return [self._to_standard_dict(output) for output in outputs]


    def encode_documents(self, documents: List[str]):
        outputs = self.model.encode(
            documents,
            return_dense=False,
            return_sparse=True,
            return_colbert_vecs=False,
        )["lexical_weights"]
        return [self._to_standard_dict(output) for output in outputs]


    def _to_standard_dict(self, raw_output):
        result = {}
        for k in raw_output:
            result[int(k)] = raw_output[k]
        return result
```

## Hibrit Yeniden Sıralayıcıyı (Reranker) Özelleştirme

Milvus iki tür [yeniden sıralama stratejisini](https://milvus.io/docs/reranking.md) destekler: Resiprokal Sıralama Füzyonu (Reciprocal Rank Fusion - RRF) ve Ağırlıklı Puanlama (Weighted Scoring). `MilvusVectorStore` hibrit aramasındaki varsayılan sıralayıcı, k=60 ile RRF'dir. Hibrit sıralayıcıyı özelleştirmek için aşağıdaki parametreleri değiştirin:

- `hybrid_ranker (str)`: Hibrit arama sorgularında kullanılan sıralayıcı tipini belirtir. Şu anda yalnızca ["RRFRanker", "WeightedRanker"] desteklenmektedir. Varsayılan olarak "RRFRanker"dır.

- `hybrid_ranker_params (dict, isteğe bağlı)`: Hibrit sıralayıcı için yapılandırma parametreleri. Bu sözlüğün yapısı, kullanılan belirli sıralayıcıya bağlıdır:

  - "RRFRanker" için şunları içermelidir:
    - "k" (int): Resiprokal Sıralama Füzyonu'nda (RRF) kullanılan bir parametre. Bu değer, arama alaka düzeyini artırmak için birden fazla sıralama stratejisini tek bir puanda birleştiren RRF algoritmasının bir parçası olarak sıralama puanlarını hesaplamak için kullanılır. Belirtilmezse varsayılan değer 60'tır.

  - "WeightedRanker" için şunları bekler:

    - "weights" (kayan noktalı sayı listesi): Tam olarak iki ağırlıktan oluşan bir liste:

      1. Yoğun gömme bileşeni için ağırlık.
      2. Seyrek gömme bileşeni için ağırlık. Bu ağırlıklar, hibrit erişim sürecinde gömmelerin yoğun ve seyrek bileşenlerinin önemini dengelemek için kullanılır. Belirtilmezse varsayılan ağırlıklar [1.0, 1.0]'dır.

```python
vector_store = MilvusVectorStore(
    uri=URI,
    # token=TOKEN,
    dim=1536,
    overwrite=False,  # Önceki örnekte oluşturulan mevcut koleksiyonu kullan
    enable_sparse=True,
    hybrid_ranker="WeightedRanker",
    hybrid_ranker_params={"weights": [1.0, 0.5]},
)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine(
    vector_store_query_mode="hybrid", similarity_top_k=5
)
response = query_engine.query("Yazar Viaweb'de ne öğrendi?")
print(textwrap.fill(str(response), 100))
```

**"Yazar, Viaweb'de bir girişimin nihai testi olarak büyüme oranını anlamanın önemi, yazılımın şekillenmesinde kullanıcı geri bildirimlerinin önemi ve web uygulamalarının yazılım geliştirmenin geleceği olduğu gerçeği dahil olmak üzere birkaç değerli ders öğrendi. Ayrıca, Viaweb deneyimi yazara bir girişimi yönetmenin zorlukları ve ödülleri, yazılım tasarımında sadeliğin değeri ve fiyatlandırma stratejilerinin müşteri çekme üzerindeki etkisi hakkında eğitim verdi."**
