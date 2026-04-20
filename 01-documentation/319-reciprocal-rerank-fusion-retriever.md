# Karşılıklı Sıralama Füzyon Erişicisi (Reciprocal Rerank Fusion Retriever)

---
title: Karşılıklı Sıralama Füzyon Erişicisi (Reciprocal Rerank Fusion Retriever)
 | LlamaIndex OSS Belgeleri
---

Bu örnekte, birden fazla sorgu ve birden fazla indeksten gelen erişim sonuçlarını nasıl birleştirebileceğinizi inceliyoruz.

Getirilen düğümler (nodes), bu [makalede](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) gösterilen `Karşılıklı Sıralama Füzyonu` (Reciprocal Rerank Fusion - RRF) algoritmasına göre yeniden sıralanacaktır. Bu algoritma, aşırı hesaplama yapmadan veya harici modellere güvenmeden erişim sonuçlarını yeniden sıralamak için verimli bir yöntem sunar.

Örnek uygulama için github'daki @Raduaschl'a [buradaki çalışmaları](https://github.com/Raudaschl/rag-fusion) için teşekkür ederiz.

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

```text
--2024-02-12 17:59:58--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8003::154, 2606:50c0:8001::154, 2606:50c0:8002::154, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8003::154|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 75042 (73K) [text/plain]
Saving to: ‘data/paul_graham/paul_graham_essay.txt’


data/paul_graham/pa 100%[===================>]  73.28K   327KB/s    in 0.2s


2024-02-12 17:59:59 (327 KB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042]
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


index = VectorStoreIndex.from_documents(documents, transformations=[splitter])
```

## Bir Hibrit Füzyon Erişicisi Oluşturma (Create a Hybrid Fusion Retriever)

Bu adımda, indeksimizi BM25 tabanlı bir erişici ile birleştiriyoruz (fuse). Bu, girdi sorgularımızdaki hem anlamsal ilişkileri hem de anahtar kelimeleri yakalamamıza olanak tanıyacaktır.

Bu erişicilerin her ikisi de bir puan hesapladığından, ek bir model kullanmadan veya aşırı hesaplama yapmadan düğümlerimizi yeniden sıralamak için karşılıklı sıralama (reciprocal rerank) algoritmasını kullanabiliriz.

Bu düzenek ayrıca 4 kez sorgulama yapacaktır: bir kez orijinal sorgunuzla ve 3 tane daha üretilen sorgu ile.

Varsayılan olarak, ek sorgular oluşturmak için aşağıdaki istemi (prompt) kullanır:

```python
QUERY_GEN_PROMPT = (
    "Sen, tek bir giriş sorgusuna dayanarak birden fazla arama sorgusu üreten yardımcı bir asistansın. "
    "Aşağıdaki giriş sorgusuyla ilgili, her satıra bir tane gelecek şekilde {num_queries} tane arama sorgusu oluştur:\n"
    "Sorgu (Query): {query}\n"
    "Sorgular (Queries):\n"
)
```

Önce erişicilerimizi oluşturuyoruz. Her biri en benzer 2 düğümü getirecek:

```python
from llama_index.retrievers.bm25 import BM25Retriever


vector_retriever = index.as_retriever(similarity_top_k=2)


bm25_retriever = BM25Retriever.from_defaults(
    docstore=index.docstore, similarity_top_k=2
)
```

Ardından, erişicilerden dönen 4 düğüm arasından en benzer 2 düğümü döndürecek olan füzyon erişicimizi (fusion retriever) oluşturabiliriz:

```python
from llama_index.core.retrievers import QueryFusionRetriever


retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    similarity_top_k=2,
    num_queries=4,  # sorgu oluşturmayı devre dışı bırakmak için bunu 1 yapın
    mode="reciprocal_rerank",
    use_async=True,
    verbose=True,
    # query_gen_prompt="...",  # burada sorgu oluşturma istemini geçersiz kılabiliriz
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

```text
Generated queries:
1. Interleafe ve Viaweb tarihindeki ana olaylar veya dönüm noktaları nelerdi?
2. Interleafe ve Viaweb'in temel gelişmeleri ve başarılarının bir zaman çizelgesini sunabilir misiniz?
3. Şirket olarak Interleafe ve Viaweb'in başarıları ve başarısızlıkları nelerdi?
```

```python
for node in nodes_with_scores:
    print(f"Puan (Score): {node.score:.2f} - {node.text}...\n-----\n")
```

```text
Puan (Score): 0.03 - Kullanıcı arayüzü (UI) korkunçtu, ancak herhangi bir istemci yazılımı olmadan veya sunucudaki komut satırına bir şey yazmadan tarayıcı üzerinden bütün bir mağaza oluşturabileceğinizi kanıtladı.


Şimdi gerçekten bir şeylerin üzerinde olduğumuzu hissettik. Yazılımın bu şekilde çalıştığı yepyeni bir nesil hayali kuruyordum. Versiyonlara, portlara veya bu tarz saçmalıklara ihtiyacınız olmayacaktı. Interleaf'te, yazılımı gerçekten yazan grup kadar büyük görünen Sürüm Mühendisliği (Release Engineering) adlı koca bir grup vardı. Artık yazılımı doğrudan sunucu üzerinde güncelleyebilirdiniz.


Viaweb adını verdiğimiz yeni bir şirket kurduk; ismini yazılımımızın web üzerinden çalışması gerçeğinden (via the web) almıştık ve Idelle'in kocası Julian'dan 10.000 dolarlık tohum sermayesi aldık. Karşılığında ve ilk yasal işleri yapması ve bize iş tavsiyeleri vermesi karşılığında ona şirketin %10'unu verdik. On yıl sonra bu anlaşma Y Combinator modeline dönüştü. Kurucuların böyle bir şeye ihtiyacı olduğunu biliyorduk çünkü buna kendimiz de ihtiyaç duymuştuk....
-----


Puan (Score): 0.03 - Şimdi gerçekten bir şeylerin üzerinde olduğumuzu hissettik. Yazılımın bu şekilde çalıştığı yepyeni bir nesil hayali kuruyordum. Versiyonlara, portlara veya bu tarz saçmalıklara ihtiyacınız olmayacaktı. Interleaf'te, yazılımı gerçekten yazan grup kadar büyük görünen Sürüm Mühendisliği (Release Engineering) adlı koca bir grup vardı. Artık yazılımı doğrudan sunucu üzerinde güncelleyebilirdiniz.


Viaweb adını verdiğimiz yeni bir şirket kurduk; ismini yazılımımızın web üzerinden çalışması gerçeğinden (via the web) almıştık ve Idelle'in kocası Julian'dan 10.000 dolarlık tohum sermayesi aldık. Karşılığında ve ilk yasal işleri yapması ve bize iş tavsiyeleri vermesi karşılığında ona şirketin %10'unu verdik. On yıl sonra bu anlaşma Y Combinator modeline dönüştü. Kurucuların böyle bir şeye ihtiyacı olduğunu biliyorduk çünkü buna kendimiz de ihtiyaç duymuştuk.


Bu aşamada net servetim negatifti çünkü bankadaki bin dolarım kadar para, devlete olan vergi borçlarım tarafından fazlasıyla dengeleniyordu. (Interleaf için yaptığım danışmanlıktan kazandığım paranın uygun oranını özenle bir kenara ayırmış mıydım?...
-----
```

Görüldüğü gibi, her iki dönen düğüm de Viaweb ve Interleaf'ten doğru bir şekilde bahsediyor!

## Bir Sorgu Motorunda Kullanın! (Use in a Query Engine!)

Şimdi, doğal dilde yanıtlar sentezlemek için erişicimizi bir sorgu motoruna bağlayabiliriz.

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine.from_args(retriever)
```

```python
response = query_engine.query("Interleafe ve Viaweb'de neler oldu?")
```

```text
Generated queries:
1. Interleafe ve Viaweb tarihindeki ana olaylar veya dönüm noktaları nelerdi?
2. Interleafe ve Viaweb'in temel gelişmeleri ve başarılarının bir zaman çizelgesini sunabilir misiniz?
3. Interleafe ve Viaweb'in faaliyet gösterdikleri ilgili endüstriler üzerindeki sonuçları veya etkileri nelerdi?
```

```python
from llama_index.core.response.notebook_utils import display_response


display_response(response)
```

**`Nihai Yanıt (Final Response):`** Interleaf'te, yazılımı gerçekten yazan grup kadar büyük bir Sürüm Mühendisliği (Release Engineering) grubu vardı. Bu durum, yazılımın versiyonlarını ve portlarını yönetmeye yönelik önemli bir odak noktası olduğunu göstermektedir. Ancak Viaweb'de kurucular, yazılımı doğrudan sunucu üzerinde güncelleyebileceklerini fark ederek versiyon ve port ihtiyacını ortadan kaldırdılar. Web üzerinden çalışan yazılımlar geliştiren Viaweb adında bir şirket kurdular. 10.000 dolarlık tohum sermayesi aldılar ve finansman ile iş tavsiyesi sağlayan Julian'a şirketin %10'unu verdiler. Bu anlaşma daha sonra Y Combinator'ın modeli haline geldi.
