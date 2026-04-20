---
title: Qdrant Hibrit Arama
 | LlamaIndex OSS Belgeleri
---

# Qdrant Hibrit Arama

Qdrant, `seyrek` (sparse) ve `yoğun` (dense) vektörlerden gelen arama sonuçlarını birleştirerek hibrit aramayı destekler.

`Yoğun` (dense) vektörler muhtemelen halihazırda kullandığınız vektörlerdir; OpenAI, BGE, SentenceTransformers vb. gömme (embedding) modelleri genellikle `yoğun` gömme modelleridir. Bir metnin sayısal bir temsilini (representation) oluştururlar ve uzun bir sayı listesi olarak temsil edilirler. Bu `yoğun` vektörler, metnin tamamındaki zengin anlamsal özellikleri (semantics) yakalayabilir.

`Seyrek` (sparse) vektörler biraz daha farklıdır. Vektör oluşturmak için özelleştirilmiş bir yaklaşım veya model (TF-IDF, BM25, SPLADE vb.) kullanırlar. Bu vektörler temel olarak çoğunlukla sıfırlardan oluşur ve bu da onları `seyrek` vektörler yapar. Bu `seyrek` vektörler, belirli anahtar kelimeleri ve benzeri küçük ayrıntıları yakalamada harikadır.

Bu not defteri, Huggingface'ten `"prithvida/Splade_PP_en_v1"` varyantları ve Qdrant ile hibrit aramanın nasıl kurulacağını ve özelleştirileceğini adım adım gösterir.

## Kurulum

Öncelikle ortamımızı (env) kuruyor ve verilerimizi yüklüyoruz.

```bash
%pip install -U llama-index llama-index-vector-stores-qdrant fastembed
```

```python
import os


os.environ["OPENAI_API_KEY"] = "sk-..."
```

```bash
!mkdir -p 'data/'
!wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf"
```

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/").load_data()
```

## Verileri İndeksleme

Artık verilerimizi indeksleyebiliriz.

Qdrant ile hibrit aramanın başından itibaren etkinleştirilmiş olması gerekir; basitçe `enable_hybrid=True` ayarlayabiliriz.

Bu komut, OpenAI ile yoğun vektörler oluşturmaya ek olarak, fastembed kullanarak `"prithvida/Splade_PP_en_v1"` ile yerel olarak seyrek vektör oluşturma işlemini çalıştıracaktır.

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient


# diske kalıcı (persistant) bir indeks oluşturur
client = QdrantClient(host="localhost", port=6333)
aclient = AsyncQdrantClient(host="localhost", port=6333)


# vektör depomuzu hibrit indeksleme etkinleştirilmiş olarak oluşturun
# batch_size, tek seferde kaç düğümün seyrek vektörlerle kodlanacağını kontrol eder
vector_store = QdrantVectorStore(
    "llama2_paper",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    fastembed_sparse_model="Qdrant/bm25",
    batch_size=20,
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
Settings.chunk_size = 512


index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
```

## Hibrit Sorgular

Hibrit mod ile sorgulama yaparken, `similarity_top_k` ve `sparse_top_k` parametrelerini ayrı ayrı ayarlayabiliriz.

`sparse_top_k`, her bir yoğun ve seyrek sorgudan kaç düğümün (node) getirileceğini temsil eder. Örneğin, `sparse_top_k=5` ayarlandığında, bu, seyrek vektörleri kullanarak 5 düğüm ve yoğun vektörleri kullanarak 5 düğüm getireceğim anlamına gelir.

`similarity_top_k` ise nihai olarak döndürülecek düğüm sayısını kontrol eder. Yukarıdaki ayarda işlemimiz 10 düğüm (node) ile sonlanır. Farlı vektör alanlarından sıralamak (rank) ve düğümleri düzenlemek için bir birleştirme (fusion) algoritması uygulanır (bu durumda [göreceli skor füzyonu](https://weaviate.io/blog/hybrid-search-fusion-algorithms#relative-score-fusion) - relative score fusion kullanılmıştır). `similarity_top_k=2`, füzyondan sonraki en iyi iki düğümün döndürüldüğü anlamına gelir.

```python
query_engine = index.as_query_engine(
    similarity_top_k=2, sparse_top_k=12, vector_store_query_mode="hybrid"
)
```

```python
from IPython.display import display, Markdown


response = query_engine.query(
    "Llama2, Llama1'den özel olarak farklı şekilde nasıl eğitildi?"
)


display(Markdown(str(response)))
```

Llama 2, Llama 1'den özel olarak farklı bir şekilde eğitildi; örneğin verileri daha güçlüce temizlemek, veri harmanlarını (data mixes) güncellemek, %40 daha fazla toplam belirteç (token) üzerinde eğitim sağlamak, bağlam uzunluğunu (context length) iki katına çıkarmak ve daha büyük modeller için çıkarım ölçeklenebilirliğini geliştirmek üzere gruplandırılmış sorgu dikkati (GQA) kullanmak gibi değişiklikler yapıldı. Ek olarak, Llama 2 ön eğitim düzeninin (pretraining setting) ve model mimarisinin çoğunu Llama 1'den aldı ancak artırılmış bağlam uzunluğu ve gruplandırılmış sorgu dikkati gibi mimari geliştirmeleri de içerdi.

```python
print(len(response.source_nodes))
```

```bash
2
```

Şimdi hibrit aramayı hiç kullanmamakla kıyaslayalım!

```python
from IPython.display import display, Markdown


query_engine = index.as_query_engine(
    similarity_top_k=2,
    # sparse_top_k=10,
    # vector_store_query_mode="hybrid"
)


response = query_engine.query(
    "Llama2, Llama1'den özel olarak farklı şekilde nasıl eğitildi?"
)
display(Markdown(str(response)))
```

Llama 2, performansı artırmak adına değişiklikler yapılarak Llama 1'den özel olarak farklı şekilde eğitildi; daha sağlam (robust) veri temizliği, veri harmanlarını (mixes) güncelleme, %40 daha fazla toplam belirteç üzerinde eğitim, bağlam (context) uzunluğunun iki katına çıkarılması ve daha büyük modeller için çıkarım (inference) ölçeklenebilirliğini iyileştirmek için gruplandırılmış sorgu dikkati (GQA) kullanılması bu değişikliklere örnektir.

### Asenkron Destek (Async Support)

Ve tabii ki, asenkron sorgular da desteklenmektedir (bellek içi (in-memory) Qdrant verilerinin asenkron ve senkron istemciler arasında paylaşılmadığına dikkat edin!)

```python
import nest_asyncio


nest_asyncio.apply()
```

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore




# vektör depomuzu hibrit indeksleme etkinleştirilmiş olarak oluşturun
vector_store = QdrantVectorStore(
    collection_name="llama2_paper",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    fastembed_sparse_model="Qdrant/bm25",
    batch_size=20,
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
Settings.chunk_size = 512


index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    use_async=True,
)


query_engine = index.as_query_engine(similarity_top_k=2, sparse_top_k=10)


response = await query_engine.aquery(
    "Makalede hangi temel (baseline) modellere karşı ölçüm yapılıyor?"
)
```

## \[Gelişmiş] Qdrant ile Hibrit Aramayı Özelleştirme

Bu bölümde, hibrit arama deneyimini tamamen özelleştirmek için kullanılabilecek çeşitli ayarları adım adım inceleyeceğiz.

### Seyrek Vektör (Sparse Vector) Üretimini Özelleştirme

Seyrek vektör üretimi tek bir model kullanılarak veya bazen sorgular (queries) ve belgeler (documents) için ayrı ayrı farklı modeller kullanılarak yapılabilir. Burada iki model kullanıyoruz: `"naver/efficient-splade-VI-BT-large-doc"` ve `"naver/efficient-splade-VI-BT-large-query"`

Aşağıda, seyrek vektörleri oluşturmak için örnek kod ve kurucu metodda (constructor) işlevselliği nasıl ayarlayabileceğiniz yer almaktadır. Bunu kullanabilir ve ihtiyacınıza göre özelleştirebilirsiniz.

```python
from typing import Any, List, Tuple
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM


doc_tokenizer = AutoTokenizer.from_pretrained(
    "naver/efficient-splade-VI-BT-large-doc"
)
doc_model = AutoModelForMaskedLM.from_pretrained(
    "naver/efficient-splade-VI-BT-large-doc"
)


query_tokenizer = AutoTokenizer.from_pretrained(
    "naver/efficient-splade-VI-BT-large-query"
)
query_model = AutoModelForMaskedLM.from_pretrained(
    "naver/efficient-splade-VI-BT-large-query"
)




def sparse_doc_vectors(
    texts: List[str],
) -> Tuple[List[List[int]], List[List[float]]]:
    """
    ReLU, log ve max işlemlerini kullanarak logits ve attention mask'ten vektörleri hesaplar.
    """
    tokens = doc_tokenizer(
        texts, truncation=True, padding=True, return_tensors="pt"
    )
    if torch.cuda.is_available():
        tokens = tokens.to("cuda")


    output = doc_model(**tokens)
    logits, attention_mask = output.logits, tokens.attention_mask
    relu_log = torch.log(1 + torch.relu(logits))
    weighted_log = relu_log * attention_mask.unsqueeze(-1)
    tvecs, _ = torch.max(weighted_log, dim=1)


    # sıfır olmayan vektörleri ve indeks dizinlerini çıkartın
    indices = []
    vecs = []
    for batch in tvecs:
        indices.append(batch.nonzero(as_tuple=True)[0].tolist())
        vecs.append(batch[indices[-1]].tolist())


    return indices, vecs




def sparse_query_vectors(
    texts: List[str],
) -> Tuple[List[List[int]], List[List[float]]]:
    """
    ReLU, log ve max işlemlerini kullanarak logits ve attention mask'ten vektörleri hesaplar.
    """
    # YAPILACAKLAR (TODO): eğer maks (max) uzunluk aşılırsa, gruplar halinde seyrek vektörleri hesaplayın
    tokens = query_tokenizer(
        texts, truncation=True, padding=True, return_tensors="pt"
    )
    if torch.cuda.is_available():
        tokens = tokens.to("cuda")


    output = query_model(**tokens)
    logits, attention_mask = output.logits, tokens.attention_mask
    relu_log = torch.log(1 + torch.relu(logits))
    weighted_log = relu_log * attention_mask.unsqueeze(-1)
    tvecs, _ = torch.max(weighted_log, dim=1)


    # sıfır olmayan vektörleri ve indeks dizinlerini çıkartın
    indices = []
    vecs = []
    for batch in tvecs:
        indices.append(batch.nonzero(as_tuple=True)[0].tolist())
        vecs.append(batch[indices[-1]].tolist())


    return indices, vecs
```

```python
vector_store = QdrantVectorStore(
    "llama2_paper",
    client=client,
    enable_hybrid=True,
    sparse_doc_fn=sparse_doc_vectors,
    sparse_query_fn=sparse_query_vectors,
)
```

### `hybrid_fusion_fn()` Kullanımını Özelleştirme

Varsayılan olarak, Qdrant ile hibrit sorgular çalıştırılırken, hem seyrek (sparse) hem de yoğun (dense) sorgulardan alınan düğümleri birleştirmek için Göreceli Puan Birleştirme (Relative Score Fusion) kullanılır.

Bu işlevi istediğiniz başka bir yönteme (düz veri tekilleştirme, Resiprokal Sıralama Füzyonu veya RRF vb.) göre özelleştirebilirsiniz.

Aşağıda bizim göreceli skor füzyon yaklaşımımız için varsayılan kod ve bu işlevi kurucu metoda (constructor) nasıl aktarabileceğiniz yer almaktadır.

```python
from llama_index.core.vector_stores import VectorStoreQueryResult




def relative_score_fusion(
    dense_result: VectorStoreQueryResult,
    sparse_result: VectorStoreQueryResult,
    alpha: float = 0.5,  # sorgu motorundan (query engine) geçirilir
    top_k: int = 2,  # sorgu motorundan geçirilir yani similarity_top_k
) -> VectorStoreQueryResult:
    """
    Göreceli puan birleştirme (relative score fusion) kullanarak yoğun (dense) ve seyrek (sparse) sonuçları birleştirin.
    """
    # sağlık / tutarlılık kontrolü (sanity check)
    assert dense_result.nodes is not None
    assert dense_result.similarities is not None
    assert sparse_result.nodes is not None
    assert sparse_result.similarities is not None


    # sonuçların yapısını çözme (deconstruct)
    sparse_result_tuples = list(
        zip(sparse_result.similarities, sparse_result.nodes)
    )
    sparse_result_tuples.sort(key=lambda x: x[0], reverse=True)


    dense_result_tuples = list(
        zip(dense_result.similarities, dense_result.nodes)
    )
    dense_result_tuples.sort(key=lambda x: x[0], reverse=True)


    # her iki sonuçta yer alan düğümleri izleme
    all_nodes_dict = {x.node_id: x for x in dense_result.nodes}
    for node in sparse_result.nodes:
        if node.node_id not in all_nodes_dict:
            all_nodes_dict[node.node_id] = node


    # seyrek benzerlikleri (sparse similarities) 0'dan 1'e doğru normalleştir (normalize)
    sparse_similarities = [x[0] for x in sparse_result_tuples]
    max_sparse_sim = max(sparse_similarities)
    min_sparse_sim = min(sparse_similarities)
    sparse_similarities = [
        (x - min_sparse_sim) / (max_sparse_sim - min_sparse_sim)
        for x in sparse_similarities
    ]
    sparse_per_node = {
        sparse_result_tuples[i][1].node_id: x
        for i, x in enumerate(sparse_similarities)
    }


    # yoğun benzerlikleri (dense similarities) 0'dan 1'e doğru normalleştir
    dense_similarities = [x[0] for x in dense_result_tuples]
    max_dense_sim = max(dense_similarities)
    min_dense_sim = min(dense_similarities)
    dense_similarities = [
        (x - min_dense_sim) / (max_dense_sim - min_dense_sim)
        for x in dense_similarities
    ]
    dense_per_node = {
        dense_result_tuples[i][1].node_id: x
        for i, x in enumerate(dense_similarities)
    }


    # Puanları birleştir / bütünleştir
    fused_similarities = []
    for node_id in all_nodes_dict:
        sparse_sim = sparse_per_node.get(node_id, 0)
        dense_sim = dense_per_node.get(node_id, 0)
        fused_sim = alpha * (sparse_sim + dense_sim)
        fused_similarities.append((fused_sim, all_nodes_dict[node_id]))


    fused_similarities.sort(key=lambda x: x[0], reverse=True)
    fused_similarities = fused_similarities[:top_k]


    # son yanıt (response) nesnesini oluştur
    return VectorStoreQueryResult(
        nodes=[x[1] for x in fused_similarities],
        similarities=[x[0] for x in fused_similarities],
        ids=[x[1].node_id for x in fused_similarities],
    )
```

```python
vector_store = QdrantVectorStore(
    "llama2_paper",
    client=client,
    enable_hybrid=True,
    hybrid_fusion_fn=relative_score_fusion,
)
```

Yukarıdaki fonksiyonda alfa (alpha) parametresini fark etmişsinizdir. Bu değişken, doğrudan `as_query_engine()` çağrısında ayarlanabilir ve böylece bu onu vektör indeks erişicisine (vector index retriever) kuracaktır.

```python
index.as_query_engine(alpha=0.5, similarity_top_k=2)
```

### Hibrit Qdrant Koleksiyonlarını Özelleştirme

İşlemi llama-index'in gerçekleştirmesine izin vermek yerine, Qdrant hibrit koleksiyonlarınızı da önceden kendiniz yapılandırabilirsiniz.

**NOT:** Hibrit bir indeks oluşturuluyorsa vektör konfigürasyonlarının (vector configs) adları `text-dense` ve `text-sparse` olmalıdır.

```python
from qdrant_client import models


client.recreate_collection(
    collection_name="llama2_paper",
    vectors_config={
        "text-dense": models.VectorParams(
            size=1536,  # openai vektör boyutu
            distance=models.Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "text-sparse": models.SparseVectorParams(
            index=models.SparseIndexParams()
        )
    },
)


# Önceden seyrek koleksiyon oluşturduğumuzdan hibrit aramayı yeniden etkinleştir
vector_store = QdrantVectorStore(
    collection_name="llama2_paper", client=client, enable_hybrid=True
)
```
