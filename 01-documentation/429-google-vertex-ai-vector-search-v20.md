# Google Vertex AI Vector Search v2.0

---
title: Google Vertex AI Vector Search v2.0
 | LlamaIndex OSS Documentation
---

Bu not defteri, **Vertex AI Vektör Araması (Vector Search) v2.0** sürümünün LlamaIndex ile nasıl kullanılacağını gösterir.
 
 > [Vertex AI Vektör Araması v2.0](https://cloud.google.com/vertex-ai/docs/vector-search/overview), ayrı indeks oluşturma ve uç nokta dağıtma ihtiyacını ortadan kaldıran basitleştirilmiş bir **koleksiyon tabanlı mimari** sunar.

## v2.0 ve v1.0 Karşılaştırması

| Özellik       | v1.0                              | v2.0              |
 | ------------- | --------------------------------- | ----------------- |
 | Mimari        | İndeks + Uç Nokta (Endpoint)      | Koleksiyon        |
 | Kurulum Adımları | İndeks Oluştur → Uç Noktaya Dağıt | Koleksiyon Oluştur |
 | GCS Bucket    | Toplu güncellemeler için gerekli  | Gerekli değil      |
 | Hibrit Arama | Desteklenmiyor                    | Destekleniyor     |
 
 **Not**: v1.0 kullanımı için [VertexAIVectorSearchDemo.ipynb](./VertexAIVectorSearchDemo.ipynb) dosyasına bakın.

## Bağımlılıkları Yükleme

v2 desteğiyle LlamaIndex'i kurun:
 
 > **Not**: V2 desteği, Vertex AI Vektör Araması v2.0 API'sini destekleyen bir `llama-index-vector-stores-vertexaivectorsearch` sürümü gerektirir.

```
# v2 desteği ile kurun ([v2] ek paketi google-cloud-vectorsearch'ü yükler)
 # !pip install 'llama-index-vector-stores-vertexaivectorsearch[v2]' llama-index-embeddings-vertex llama-index-llms-vertex
```

### Kimlik Doğrulama (Colab kullanılıyorsa):

```
# Colab authentication.
import sys


if "google.colab" in sys.modules:
    from google.colab import auth


    auth.authenticate_user()
    print("Authenticated")
```

## Yapılandırma

Google Cloud proje detaylarınızı ayarlayın:

```
# Google Cloud Configuration
PROJECT_ID = "your-project-id"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
COLLECTION_ID = "llamaindex-demo-collection"  # @param {type:"string"}


# Yerleştirme (Embedding) boyutları (text-embedding-004 için 768)
EMBEDDING_DIMENSION = 768
```

## Bir v2 Koleksiyonu Oluşturma

Bir indeks oluşturmayı ve bunu bir uç noktaya dağıtmayı gerektiren v1.0'ın aksine, v2.0 sadece bir koleksiyon oluşturmayı gerektirir.
 
 **Hibrit Arama için Önemli:** Aşağıdaki koleksiyon şeması, tüm hibrit arama özelliklerini destekleyecek şekilde yapılandırılmıştır:
 
 - **Metin Araması (Text Search)**: Dize alanları (`text`, `category`, `color`) anahtar kelimelerle aranabilir.
 - **Anlamsal Arama (Semantic Search)**: `vertex_embedding_config`, `SEMANTIC_HYBRID` modu için otomatik yerleştirmeleri etkinleştirir.
 - **Filtreleme (Filtering)**: Sayısal (`price`) ve dize alanları meta veri filtrelemeyi destekler.

```
from google.cloud import vectorsearch_v1beta


# Initialize the client
client = vectorsearch_v1beta.VectorSearchServiceClient()


# Check if collection already exists
parent = f"projects/{PROJECT_ID}/locations/{REGION}"
collection_name = f"{parent}/collections/{COLLECTION_ID}"


# Koleksiyon şeması aşağıdakileri destekler:
 # - Yoğun vektör araması (embedding alanı)
 # - text, category, color alanlarında metin araması (HYBRID modu için)
 # - Otomatik yerleştirmelerle anlamsal arama (SEMANTIC_HYBRID modu için)
 # - price, category, color alanlarında filtreleme
 collection_config = {
     "data_schema": {
         "type": "object",
         "properties": {
             "text": {"type": "string"},  # Ana metin içeriği (aranabilir)
             "ref_doc_id": {"type": "string"},  # Belge referansı
             "price": {"type": "number"},  # Filtrelenebilir sayısal alan
             "color": {"type": "string"},  # Filtrelenebilir/aranabilir dize
             "category": {"type": "string"},  # Filtrelenebilir/aranabilir dize
         },
     },
    "vector_schema": {
        "embedding": {
            "dense_vector": {
                "dimensions": EMBEDDING_DIMENSION,
                # Otomatik yerleştirme (auto-embedding) yapılandırması SEMANTIC_HYBRID modunu etkinleştirir
                 # Vertex AI, anlamsal arama için yerleştirmeleri otomatik olarak oluşturacaktır
                "vertex_embedding_config": {
                    "model_id": "text-embedding-004",
                    "text_template": "{text}",
                    "task_type": "RETRIEVAL_DOCUMENT",
                },
            }
        },
    },
}


try:
    request = vectorsearch_v1beta.GetCollectionRequest(name=collection_name)
    collection = client.get_collection(request=request)
    print(f"Koleksiyon zaten mevcut: {collection.name}")
    print(
        "Not: Hibrit arama özelliklerine ihtiyacınız varsa, yukarıdaki şema ile silip yeniden oluşturun."
    )
except Exception as e:
    if "404" in str(e) or "NotFound" in str(e):
        print(f"Koleksiyon oluşturuluyor: {COLLECTION_ID}")
        print(
            "Şema şunları içerir: metin arama alanları, anlamsal arama için otomatik yerleştirme yapılandırması"
        )


        request = vectorsearch_v1beta.CreateCollectionRequest(
            parent=parent,
            collection_id=COLLECTION_ID,
            collection=collection_config,
        )
        operation = client.create_collection(request=request)
        collection = operation.result()
        print(f"Collection created: {collection.name}")
    else:
        raise e
```

## LlamaIndex Bileşenlerini Ayarlama

```
# Imports
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator,
)
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex
from llama_index.vector_stores.vertexaivectorsearch import VertexAIVectorStore


# Yerleştirme kimlik bilgileri - varsayılan kimlik bilgilerini al
 import google.auth
 
 
 credentials, project = google.auth.default()
 print(f"Şu proje ile kimlik doğrulandı: {project}")
 ```
 
 ```
 # Yerleştirme modelini yapılandır
 embed_model = VertexTextEmbedding(
     model_name="text-embedding-004",
     project=PROJECT_ID,
     location=REGION,
     credentials=credentials,
 )
 
 
 # LLM'i yapılandır
 llm = Vertex(
     model="gemini-2.0-flash",
     project=PROJECT_ID,
     location=REGION,
     credentials=credentials,
 )
 
 
 # Varsayılan olarak ayarla
 Settings.embed_model = embed_model
 Settings.llm = llm
 
 
 print("Yerleştirme modeli ve LLM başarıyla yapılandırıldı!")
 ```
 
 ## v2 Vektör Deposu Oluşturma
 
 Bir v2 vektör deposu oluşturmak basittir - sadece `api_version="v2"` ve `collection_id` bilginizi belirtmeniz yeterlidir:
 
 ```
 # v2 vektör deposu oluştur
 vector_store = VertexAIVectorStore(
     api_version="v2",  # v2 API'sini kullan
     project_id=PROJECT_ID,
     region=REGION,
     collection_id=COLLECTION_ID,
     # index_id, endpoint_id veya gcs_bucket_name gerekmez!
 )
 
 
 print(f"Vektör deposu api_version={vector_store.api_version} ile oluşturuldu")
```

## Belgeler Ekleme
 
 ### Basit Metin Düğümleri (Text Nodes)
 
 ```
 # Bazı örnek metin düğümleri oluştur
 texts = [
     "LlamaIndex, LLM uygulamaları için bir veri çerçevesidir.",
     "Vertex AI Vektör Araması, ölçeklenebilir vektör benzerliği araması sağlar.",
     "RAG, daha iyi yapay zeka yanıtları için getirmeyi (retrieval) üretimle (generation) birleştirir.",
     "Yerleştirmeler (embeddings), benzerlik eşleştirmesi için metni sayısal vektörlere dönüştürür.",
 ]
 
 
 # Yerleştirmelere sahip düğümler oluştur
 nodes = [
     TextNode(text=text, embedding=embed_model.get_text_embedding(text))
     for text in texts
 ]
 
 
 # Vektör deposuna ekle
 ids = vector_store.add(nodes)
 print(f"Vektör deposuna {len(ids)} düğüm eklendi")
```

### Meta Verili Düğümler
 
 Filtreleme ve hibrit arama için meta verili düğümler ekleyin:
 
 ```
 # Meta verili örnek ürün verileri
 products = [
     {
         "text": "Rahat mavi pamuklu tişört, günlük kullanım için ideal",
         "color": "mavi",
         "category": "üst",
         "price": 29.99,
     },
     {
         "text": "Ofis toplantıları için profesyonel siyah kumaş pantolon",
         "color": "siyah",
         "category": "alt",
         "price": 79.99,
     },
     {
         "text": "Soğuk kış günleri için sıcak tutan yeşil yün kazak",
         "color": "yeşil",
         "category": "üst",
         "price": 59.99,
     },
     {
         "text": "Cepli, hafif mavi koşu şortu",
         "color": "mavi",
         "category": "alt",
         "price": 34.99,
     },
     {
         "text": "Resmi durumlar için zarif kırmızı ipek bluz",
         "color": "kırmızı",
         "category": "üst",
         "price": 89.99,
     },
 ]
 
 
 # Meta verili düğümler oluştur
 # Not: TEXT_SEARCH'ün metin alanında çalışması için meta verilere "text" alanını dahil edin
 product_nodes = [
     TextNode(
         text=p["text"],
         embedding=embed_model.get_text_embedding(p["text"]),
         metadata={
             "text": p["text"],
             "color": p["color"],
             "category": p["category"],
             "price": p["price"],
         },
     )
     for p in products
 ]
 
 
 # Vektör deposuna ekle
 product_ids = vector_store.add(product_nodes)
 print(f"Meta verili {len(product_ids)} ürün düğümü eklendi")
```

## Vektör Deposunu Sorgulama
 
 ### Basit Benzerlik Araması
 
 ```
 # Vektör deposundan indeks oluştur
 storage_context = StorageContext.from_defaults(vector_store=vector_store)
 index = VectorStoreIndex.from_vector_store(
     vector_store=vector_store, embed_model=embed_model
 )
 
 
 # Getirici (retriever) oluştur
 retriever = index.as_retriever(similarity_top_k=3)
 
 
 # Sorgula
 results = retriever.retrieve("günlük kullanım için rahat kıyafetler")
 
 
 print("Arama Sonuçları:")
 print("-" * 60)
 for result in results:
     print(f"Puan: {result.get_score():.3f}")
     print(f"Metin: {result.get_text()[:100]}...")
     print(f"Meta Veri: {result.metadata}")
     print("-" * 60)
```

### Meta Veri Filtreleri ile Arama
 
 ```
 # Renge göre filtrele
 filters = MetadataFilters(filters=[MetadataFilter(key="color", value="mavi")])
 
 
 retriever = index.as_retriever(filters=filters, similarity_top_k=3)
 results = retriever.retrieve("günlük kıyafet")
 
 
 print("Sadece mavi ürünler:")
 print("-" * 60)
 for result in results:
     print(
         f"Puan: {result.get_score():.3f} | Renk: {result.metadata.get('color')}"
     )
     print(f"Metin: {result.get_text()[:80]}...")
     print("-" * 60)
 ```
 
 ```
 # Fiyat aralığına göre filtrele
 filters = MetadataFilters(
     filters=[
         MetadataFilter(key="price", operator=FilterOperator.LT, value=50.0),
     ]
 )
 
 
 retriever = index.as_retriever(filters=filters, similarity_top_k=3)
 results = retriever.retrieve("kıyafet")
 
 
 print("50$ altındaki ürünler:")
 print("-" * 60)
 for result in results:
     print(
         f"Puan: {result.get_score():.3f} | Fiyat: ${result.metadata.get('price')}"
     )
     print(f"Metin: {result.get_text()[:80]}...")
     print("-" * 60)
```

## LLM ile RAG Sorgusu
 
 Getirme destekli üretim (retrieval-augmented generation) için vektör deposunu bir LLM ile kullanın:
 
 ```
 # Sorgu motoru (query engine) oluştur
 query_engine = index.as_query_engine(similarity_top_k=3)
 
 
 # Soru sor
 response = query_engine.query(
     "Hangi mavi kıyafetleriniz var ve fiyatları nelerdir?"
 )
 
 
 print(
     "Soru: Hangi mavi kıyafetleriniz var ve fiyatları nelerdir?"
 )
 print("-" * 60)
 print(f"Yanıt: {response.response}")
 print("-" * 60)
 print("Kaynaklar:")
 for node in response.source_nodes:
     print(f"  - {node.text[:60]}... (puan: {node.score:.3f})")
```

## Yalnızca v2 Özellikleri
 
 ### Belirli Düğümleri Silme
 
 ```
 # Kimliğe göre belirli düğümleri sil
 # vector_store.delete_nodes(node_ids=["node_id_1", "node_id_2"])
 print("delete_nodes() - Belirli düğümleri kimliklerine göre siler")
 ```
 
 ### Tüm Veriyi Temizle (sadece v2)
 
 v2, bir koleksiyondaki tüm verilerin temizlenmesini destekler - bu özellik v1'de mevcut DEĞİLDİR:
 
 ```
 # Koleksiyondaki tüm verileri temizle
 # UYARI: Bu, koleksiyondaki TÜM verileri siler!
 # vector_store.clear()
 print("clear() - Koleksiyondaki tüm verileri temizler (sadece v2!)")
```

## Hibrit Arama (sadece v2)

v2, gelişmiş getirme kalitesi için vektör benzerliğini metin tabanlı arama ile birleştiren **hibrit aramayı** destekler. Bu, hem anlamsal anlamadan (vektörler) hem de tam anahtar kelime eşleştirmeden (metin araması) yararlanmak istediğinizde özellikle yararlıdır.
 
 ### Desteklenen Sorgu Modları
 
 | Mod              | Açıklama                       | Kullanım Durumu                |
 | ----------------- | ------------------------------ | ------------------------------ |
 | `DEFAULT`         | Yoğun vektör benzerliği araması | Standart anlamsal arama        |
 | `TEXT_SEARCH`     | Tam metin anahtar kelime araması | Tam anahtar kelime eşleştirme |
 | `HYBRID`          | RRF füzyonu ile Vektör + Metin  | Her iki dünyanın en iyisi      |
 | `SEMANTIC_HYBRID` | Vektör + Anlamsal arama        | Otomatik yerleştirme anlamsal arama |
 
 ### Sıralayıcı (Ranker) Seçenekleri
 
 | Sıralayıcı      | Açıklama                                    |
 | --------------- | ------------------------------------------- |
 | `rrf` (varsayılan) | Alfa ağırlıklandırmalı Karşılıklı Sıra Füzyonu (Reciprocal Rank Fusion) |
 | `vertex`        | Vertex AI aracılığıyla yapay zeka destekli anlamsal sıralama |

### Hibrit Destekli Vektör Deposu Oluşturma

Hibrit aramayı etkinleştirmek için `enable_hybrid=True` ayarlayın ve metin araması için hangi alanların kullanılacağını belirtin:
 
 ```
 # Hibrit aramalı vektör deposu oluştur
 hybrid_vector_store = VertexAIVectorStore(
     api_version="v2",
     project_id=PROJECT_ID,
     region=REGION,
     collection_id=COLLECTION_ID,
     enable_hybrid=True,
     text_search_fields=["text", "category", "color"],  # Metin araması için alanlar
     default_hybrid_alpha=0.5,  # Vektör ve metin dengesi (0=sadece metin, 1=sadece vektör)
 )
 
 
 print(
     f"Hibrit vektör deposu enable_hybrid={hybrid_vector_store.enable_hybrid} ile oluşturuldu"
 )
```

### TEXT\_SEARCH Modu - Anahtar Kelime Araması
 
 Tam metin anahtar kelime eşleştirmesi için `TEXT_SEARCH` modunu kullanın. Bu, anlamsal benzerlikten ziyade tam anahtar kelime eşleşmeleri istediğinizde kullanışlıdır:
 
 ```
 from llama_index.core.vector_stores.types import (
     VectorStoreQuery,
     VectorStoreQueryMode,
 )
 
 
 # TEXT_SEARCH: Sadece tam metin anahtar kelime araması
 text_query = VectorStoreQuery(
     query_str="mavi pamuklu",  # Aranacak anahtar kelimeler
     mode=VectorStoreQueryMode.TEXT_SEARCH,
     similarity_top_k=3,
 )
 
 
 results = hybrid_vector_store.query(text_query)
 
 
 print("TEXT_SEARCH Sonuçları (anahtar kelime eşleştirme):")
 print("-" * 60)
 for i, node in enumerate(results.nodes):
     print(f"{i+1}. {node.text[:80]}...")
     print(f"   Meta Veri: {node.metadata}")
    print()
```

### HYBRID Modu - Vektör + Metin Araması
 
 Vektör benzerliğini metin aramasıyla birleştirmek için `HYBRID` modunu kullanın. `alpha` parametresi dengeyi kontrol eder:
 
 - `alpha=1.0` - Saf vektör araması
 - `alpha=0.5` - Dengeli
 - `alpha=0.0` - Saf metin araması
 
 ```
 # Farklı alfa değerlerini karşılaştır
 print("Alfa değerlerini karşılaştırma:")
 print("=" * 60)
 
 
 for alpha in [1.0, 0.5, 0.0]:
     query = VectorStoreQuery(
         query_embedding=embed_model.get_query_embedding(
             "sıcak kış kıyafetleri"
         ),
         query_str="yeşil kazak",  # Anahtar kelimeler yeşil kazaktan yana
         mode=VectorStoreQueryMode.HYBRID,
         alpha=alpha,
         similarity_top_k=2,
     )
     results = hybrid_vector_store.query(query)
 
 
     label = (
         "sadece vektör"
         if alpha == 1.0
         else "sadece metin"
         if alpha == 0.0
         else "dengeli"
     )
     print(f"\nalpha={alpha} ({label}):")
     for node in results.nodes:
         print(f"  - {node.text[:60]}... | renk={node.metadata.get('color')}")
```

### SEMANTIC\_HYBRID Modu
 
 `SEMANTIC_HYBRID`, yoğun vektör aramanızı Vertex AI'nın yerleşik anlamsal aramasıyla birleştirir. Bu, koleksiyonun otomatik yerleştirmeler (auto-embeddings) için `vertex_embedding_config` ile yapılandırılmış olmasını gerektirir.
 
 ```
 # SEMANTIC_HYBRID: Vektör + Vertex AI'nın anlamsal araması
 # Not: vertex_embedding_config yapılandırmasına sahip koleksiyon gerektirir
 
 
 semantic_query = VectorStoreQuery(
     query_embedding=embed_model.get_query_embedding(
         "profesyonel iş kıyafetleri"
     ),
     query_str="resmi ofis kıyafeti",  # Anlamsal arama metni
     mode=VectorStoreQueryMode.SEMANTIC_HYBRID,
     similarity_top_k=3,
 )
 
 
 try:
     results = hybrid_vector_store.query(semantic_query)
     print("SEMANTIC_HYBRID Sonuçları:")
     print("-" * 60)
     for i, node in enumerate(results.nodes):
         print(f"{i+1}. {node.text[:80]}...")
 except Exception as e:
     print(
         f"SEMANTIC_HYBRID, vertex_embedding_config şemasına sahip bir koleksiyon gerektirir: {e}"
     )
```

### VertexRanker Kullanımı
 
 RRF yerine, AI destekli sonuç sıralaması için Vertex AI'nın anlamsal sıralayıcısını (ranker) kullanabilirsiniz:
 
 ```
 # VertexRanker ile vektör deposu oluştur
 vertex_ranker_store = VertexAIVectorStore(
     api_version="v2",
     project_id=PROJECT_ID,
     region=REGION,
     collection_id=COLLECTION_ID,
     enable_hybrid=True,
     text_search_fields=["text", "category"],
     hybrid_ranker="vertex",  # Vertex AI'nın anlamsal sıralayıcısını kullan
     vertex_ranker_model="semantic-ranker-default@latest",
     vertex_ranker_title_field="category",  # Başlık olarak kullanılacak alan
     vertex_ranker_content_field="text",  # İçerik olarak kullanılacak alan
 )
 
 
 # VertexRanker ile sorgula
 query = VectorStoreQuery(
     query_embedding=embed_model.get_query_embedding("günlük giyim"),
     query_str="rahat tişört",
     mode=VectorStoreQueryMode.HYBRID,
     similarity_top_k=3,
 )
 
 
 results = vertex_ranker_store.query(query)
 
 
 print("VertexRanker ile HYBRID Sonuçlar:")
 print("-" * 60)
 for i, node in enumerate(results.nodes):
     print(f"{i+1}. {node.text[:80]}...")
     print(f"   Kategori: {node.metadata.get('category')}")
    print()
```

### Sorgu Motoru (Query Engine) ile Hibrit Arama (RAG)
 
 Hibrit aramayı RAG uygulamaları için standart LlamaIndex sorgu motoruyla da kullanabilirsiniz:
 
 ```
 # Hibrit destekli vektör deposu ile indeks oluştur
 hybrid_storage_context = StorageContext.from_defaults(
     vector_store=hybrid_vector_store
 )
 hybrid_index = VectorStoreIndex.from_vector_store(
     vector_store=hybrid_vector_store,
     embed_model=embed_model,
 )
 
 
 # Hibrit modda sorgu motoru oluştur
 hybrid_query_engine = hybrid_index.as_query_engine(
     vector_store_query_mode=VectorStoreQueryMode.HYBRID,
     similarity_top_k=3,
     alpha=0.7,  # Vektör aramasına biraz daha fazla ağırlık ver
 )
 
 
 # Hibrit getirme ile RAG kullanarak bir soru sorun
 response = hybrid_query_engine.query(
     "Hangi rahat mavi kıyafet seçenekleri mevcut?"
 )
 
 
 print("Soru: Hangi rahat mavi kıyafet seçenekleri mevcut?")
 print("-" * 60)
 print(f"Yanıt: {response.response}")
 print("-" * 60)
 print("Kaynaklar:")
 for node in response.source_nodes:
     print(f"  - {node.text[:60]}... (puan: {node.score:.3f})")
```

### Hibrit Arama Parametreleri Referansı
 
 | Parametre                     | Tip         | Varsayılan                         | Açıklama                              |
 | ----------------------------- | ----------- | ---------------------------------- | ------------------------------------- |
 | `enable_hybrid`               | `bool`      | `False`                            | Hibrit arama modlarını etkinleştirir  |
 | `text_search_fields`          | `List[str]` | `None`                             | Metin araması için veri alanları      |
 | `embedding_field`             | `str`       | `"embedding"`                      | Vektör alanı adı                      |
 | `default_hybrid_alpha`        | `float`     | `0.5`                              | Varsayılan RRF ağırlığı (0=metin, 1=vektör) |
 | `hybrid_ranker`               | `str`       | `"rrf"`                            | Sıralayıcı: “rrf” veya “vertex”        |
 | `semantic_task_type`          | `str`       | `"RETRIEVAL_QUERY"`                | SemanticSearch için görev tipi        |
 | `vertex_ranker_model`         | `str`       | `"semantic-ranker-default@latest"` | VertexRanker modeli                   |
 | `vertex_ranker_title_field`   | `str`       | `None`                             | VertexRanker için başlık alanı        |
 | `vertex_ranker_content_field` | `str`       | `None`                             | VertexRanker için içerik alanı        |

## Temizlik
 
 Ücret ödememek için işiniz bittiğinde koleksiyonu silin:
 
 ```
 CLEANUP = False  # Koleksiyonu silmek için True olarak ayarlayın
 
 
 if CLEANUP:
     from google.cloud import vectorsearch_v1beta
 
 
     client = vectorsearch_v1beta.VectorSearchServiceClient()
     collection_name = (
         f"projects/{PROJECT_ID}/locations/{REGION}/collections/{COLLECTION_ID}"
     )
 
 
     print(f"Koleksiyon siliniyor: {collection_name}")
     client.delete_collection(name=collection_name)
     print("Koleksiyon silindi.")
```

## Özet
 
 Bu not defteri şunları göstermiştir:
 
 1. **Basit Kurulum**: v2 sadece bir koleksiyon gerektirir - indeks/uç nokta dağıtımı gerekmez.
 
 2. **Kolay Entegrasyon**: Yeni API'yi kullanmak için sadece `api_version="v2"` eklemeniz yeterlidir.
 
 3. **Aynı Arayüz**: Tüm LlamaIndex işlemleri (ekleme, sorgulama, silme) aynı şekilde çalışır.
 
 4. **Yeni Özellikler**: v2, v1'de bulunmayan `clear()` metodunu ekler.
 
 5. **Hibrit Arama**: Daha iyi getirme için vektör ve metin aramasını birleştirin:
 
    - `TEXT_SEARCH` - Tam metin anahtar kelime araması.
    - `HYBRID` - RRF füzyonu ile Vektör + metin.
    - `SEMANTIC_HYBRID` - Vektör + anlamsal arama.
    - Yapay zeka destekli sıralama için VertexRanker.
 
 ### v1'den Geçiş
 
 ```
 # v1 (eski)
 vector_store = VertexAIVectorStore(
     project_id="...",
     region="...",
     index_id="projects/.../indexes/123",
     endpoint_id="projects/.../indexEndpoints/456",
     gcs_bucket_name="my-bucket"
 )
 
 
 # v2 (yeni)
 vector_store = VertexAIVectorStore(
     api_version="v2",
     project_id="...",
     region="...",
     collection_id="my-collection"
 )
 
 
 # hibrit arama ile v2
 vector_store = VertexAIVectorStore(
     api_version="v2",
     project_id="...",
     region="...",
     collection_id="my-collection",
     enable_hybrid=True,
     text_search_fields=["text", "unvan"],
 )
 ```
 
 Ayrıntılı geçiş talimatları için [V2\_MIGRATION.md](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/vector_stores/llama-index-vector-stores-vertexaivectorsearch/V2_MIGRATION.md) dosyasına bakın.
