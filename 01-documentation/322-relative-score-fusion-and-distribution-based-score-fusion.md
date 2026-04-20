# Göreceli Puan Füzyonu ve Dağılım Tabanlı Puan Füzyonu (Relative Score Fusion and Distribution-Based Score Fusion)

---
title: Göreceli Puan Füzyonu ve Dağılım Tabanlı Puan Füzyonu (Relative Score Fusion and Distribution-Based Score Fusion)
 | LlamaIndex OSS Belgeleri
---

Bu örnekte, Karşılıklı Sıralama Füzyonunu (Reciprocal Rank Fusion) iyileştirmeyi amaçlayan iki yöntemle `QueryFusionRetriever` kullanımını gösteriyoruz:

1. Göreceli Puan Füzyonu (Relative Score Fusion - [Weaviate](https://weaviate.io/blog/hybrid-search-fusion-algorithms))
2. Dağılım Tabanlı Puan Füzyonu (Distribution-Based Score Fusion - [Mazzeschi: blog yazısı](https://medium.com/plain-simple-software/distribution-based-score-fusion-dbsf-a-new-approach-to-vector-search-ranking-f87c37488b18))

```bash
%pip install llama-index-llms-openai
%pip install llama-index-retrievers-bm25
```

```python
import os
import openai


os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = os.environ["OPENAI_API_KEY"]
```

## Kurulum (Setup)

Eğer bu Not Defterini Colab üzerinde açıyorsanız, muhtemelen LlamaIndex'i kurmanız gerekecektir 🦙.

Veriyi İndir (Download Data)

```bash
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

```python
from llama_index.core import SimpleDirectoryReader


documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

Ardından, dokümantasyon üzerinde bir vektör indeksi kuracağız.

```python
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter


splitter = SentenceSplitter(chunk_size=256)


index = VectorStoreIndex.from_documents(
    documents, transformations=[splitter], show_progress=True
)
```

```text
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00,  7.55it/s]
Generating embeddings: 100%|██████████| 504/504 [00:03<00:00, 128.32it/s]
```

## Göreceli Puan Füzyonu Kullanarak bir Hibrit Füzyon Erişicisi Oluşturma (Create a Hybrid Fusion Retriever using Relative Score Fusion)

Bu adımda, indeksimizi BM25 tabanlı bir erişici ile birleştiriyoruz (fuse). Bu, girdi sorgularımızdaki hem anlamsal ilişkileri hem de anahtar kelimeleri yakalamamıza olanak tanıyacaktır.

Bu erişicilerin her ikisi de bir puan hesapladığından, ek bir model kullanmadan veya aşırı hesaplama yapmadan düğümlerimizi yeniden sıralamak için `QueryFusionRetriever`ı kullanabiliriz.

Aşağıdaki örnek, Weaviate'in her bir sonuç kümesine bir MinMax ölçekleyici uygulayan ve ardından ağırlıklı bir toplam oluşturan [Göreceli Puan Füzyonu](https://weaviate.io/blog/hybrid-search-fusion-algorithms) (Relative Score Fusion) algoritmasını kullanır. Burada, vektör erişicisine BM25'ten biraz daha fazla ağırlık vereceğiz (0.4'e karşı 0.6).

Önce erişicilerimizi oluşturuyoruz. Her biri en benzer 10 düğümü getirecek.

```python
from llama_index.retrievers.bm25 import BM25Retriever


vector_retriever = index.as_retriever(similarity_top_k=5)


bm25_retriever = BM25Retriever.from_defaults(
    docstore=index.docstore, similarity_top_k=10
)
```

Ardından, erişicilerden dönen 20 düğüm arasından en benzer 10 düğümü döndürecek olan füzyon erişicimizi oluşturabiliriz.

Vektör ve BM25 erişicilerinin tamamen aynı düğümleri yalnızca farklı sıralarda döndürmüş olabileceğini unutmayın; bu durumda, basitçe bir yeniden sıralayıcı (re-ranker) görevi görür.

```python
from llama_index.core.retrievers import QueryFusionRetriever


retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    retriever_weights=[0.6, 0.4],
    similarity_top_k=10,
    num_queries=1,  # sorgu oluşturmayı devre dışı bırakmak için bunu 1 yapın
    mode="relative_score",
    use_async=True,
    verbose=True,
)
```

```python
# bir not defterinde çalıştırmak için iç içe geçmiş asenkron yapıyı uygula
import nest_asyncio


nest_asyncio.apply()
```

```python
nodes_with_scores = retriever.retrieve(
    "Interleafe ve Viaweb'de neler oldu?"
)
```

```python
for node in nodes_with_scores:
    print(f"Puan (Score): {node.score:.2f} - {node.text[:100]}...\n-----")
```

```text
Puan (Score): 0.60 - Versiyonlara, portlara veya bu tarz saçmalıklara ihtiyacınız olmayacaktı. Interleaf'te koca bir grup vardı...
-----
Puan (Score): 0.59 - Kullanıcı arayüzü korkunçtu, ancak herhangi bir istemci yazılımı olmadan tarayıcı üzerinden bütün bir mağaza inşa edebileceğinizi kanıtladı...
-----
Puan (Score): 0.40 - Interleaf değil, Microsoft Word olmaya kararlıydık. Bu da kullanımı kolay ve uygun fiyatlı olmak anlamına geliyordu...
-----
Puan (Score): 0.36 - Kendi zamanında, bu editör en iyi genel amaçlı site oluşturuculardan biriydi. Kodları sıkı tuttum ve...
-----
Puan (Score): 0.25 - Kodları sıkı tuttum ve Robert ile Trevor'ın kodları dışında başka hiçbir yazılımla entegre olmam gerekmedi...
-----
Puan (Score): 0.25 - Tek yapmam gereken bu yazılım üzerinde çalışmak olsaydı, sonraki 3 yıl hayatımın en kolay yılları olurdu...
-----
Puan (Score): 0.21 - Öğrenmek için, mağaza oluşturucumuzun kontrol edebileceğiniz bir versiyonunu yapmaya karar verdik...
-----
Puan (Score): 0.11 - Ancak hem Viaweb hem de Y Combinator'da öğrendiğim ve kullandığım en önemli şey şuydu...
-----
Puan (Score): 0.11 - Ertesi yıl, 1998 yazından 1999 yazına kadar olan süre, en az üretken olduğum yıl olmalıydı...
-----
Puan (Score): 0.07 - Mesele şu ki gerçekten ucuzdu, piyasa fiyatının yarısından daha azdı.


[8] Çoğu yazılımı başlattığınızda...
-----
```

### Dağılım Tabanlı Puan Füzyonu (Distribution-Based Score Fusion)

Göreceli Puan Füzyonunun bir çeşidi olan [Dağılım Tabanlı Puan Füzyonu](https://medium.com/plain-simple-software/distribution-based-score-fusion-dbsf-a-new-approach-to-vector-search-ranking-f87c37488b18) (DBSF), puanları her sonuç kümesi için puanların ortalamasına ve standart sapmasına göre biraz daha farklı ölçeklendirir.

```python
from llama_index.core.retrievers import QueryFusionRetriever


retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    retriever_weights=[0.6, 0.4],
    similarity_top_k=10,
    num_queries=1,  # sorgu oluşturmayı devre dışı bırakmak için bunu 1 yapın
    mode="dist_based_score",
    use_async=True,
    verbose=True,
)


nodes_with_scores = retriever.retrieve(
    "Interleafe ve Viaweb'de neler oldu?"
)


for node in nodes_with_scores:
    print(f"Puan (Score): {node.score:.2f} - {node.text[:100]}...\n-----")
```

```text
Puan (Score): 0.42 - Versiyonlara, portlara veya bu tarz saçmalıklara ihtiyacınız olmayacaktı. Interleaf'te koca bir grup vardı...
-----
Puan (Score): 0.41 - Kullanıcı arayüzü korkunçtu, ancak herhangi bir istemci yazılımı olmadan tarayıcı üzerinden bütün bir mağaza inşa edebileceğinizi kanıtladı...
-----
Puan (Score): 0.32 - Interleaf değil, Microsoft Word olmaya kararlıydık. Bu da kullanımı kolay ve uygun fiyatlı olmak anlamına geliyordu...
-----
Puan (Score): 0.30 - Kendi zamanında, bu editör en iyi genel amaçlı site oluşturuculardan biriydi. Kodları sıkı tuttum ve...
-----
Puan (Score): 0.27 - Öğrenmek için, mağaza oluşturucumuzun kontrol edebileceğiniz bir versiyonunu yapmaya karar verdik...
-----
Puan (Score): 0.24 - Kodları sıkı tuttum ve Robert ile Trevor'ın kodları dışında başka hiçbir yazılımla entegre olmam gerekmedi...
-----
Puan (Score): 0.24 - Tek yapmam gereken bu yazılım üzerinde çalışmak olsaydı, sonraki 3 yıl hayatımın en kolay yılları olurdu...
-----
Puan (Score): 0.20 - Şimdi gerçekten bir şeylerin üzerinde olduğumuzu hissettik. Yazılımın bu şekilde çalıştığı yepyeni bir nesil...
-----
Puan (Score): 0.20 - Kullanıcıların bir tarayıcıdan fazlasına ihtiyacı olmayacaktı.


Web uygulaması olarak bilinen bu tür yazılımlar genellikle...
-----
Puan (Score): 0.18 - Ancak hem Viaweb hem de Y Combinator'da öğrendiğim ve kullandığım en önemli şey şuydu...
-----
```

## Bir Sorgu Motorunda Kullanın! (Use in a Query Engine!)

Şimdi, doğal dilde yanıtlar sentezlemek için erişicimizi bir sorgu motoruna bağlayabiliriz.

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine.from_args(retriever)
```

```python
response = query_engine.query("Interleafe ve Viaweb'de neler oldu?")
```

```python
from llama_index.core.response.notebook_utils import display_response


display_response(response)
```

**`Nihai Yanıt (Final Response):`** Interleaf'te, yazılımı yazan grup kadar büyük bir Sürüm Mühendisliği (Release Engineering) grubu vardı. Versiyonlar, portlar ve diğer karmaşıklıklarla uğraşmak zorundaydılar. Buna karşılık Viaweb'de yazılım doğrudan sunucu üzerinde güncellenebiliyordu, bu da süreci basitleştiriyordu. Viaweb 10.000 dolarlık tohum sermayesi ile kuruldu ve yazılım, tarayıcı üzerinden istemci yazılımına veya sunucuda komut satırı girişlerine gerek kalmadan bütün bir mağaza inşa etmeye olanak tanıdı. Şirket, hizmetleri için düşük aylık fiyatlar sunarak kullanımı kolay ve ucuz olmayı hedefledi.
