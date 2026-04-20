# LlamaIndex'i Keşfedin Video Serisi

Eğer videolardan öğrenmeyi seviyorsanız, "Discover LlamaIndex" (LlamaIndex'i Keşfedin) serimize göz atmak için harika bir zaman. Eğer sevmiyorsanız, doğrudan [LlamaIndex'i Anlama](/python/framework/understanding) eğitimimize geçmenizi öneririz.

## Aşağıdan Yukarıya Geliştirme (Llama Docs Bot)

Bu, LlamaIndex'i Keşfedin serisi içinde yer alan ve sıfırdan bir döküman sohbet robotu (chatbot) oluşturmayı gösteren bir alt seridir.

Bunu "aşağıdan yukarıya" (bottoms-up) bir yaklaşımla nasıl yapacağınızı gösteriyoruz; LLM'leri ve veri nesnelerini bağımsız modüller olarak kullanarak başlayın. Ardından, indeksleme ve gelişmiş getiriciler (retrievers)/yeniden sıralayıcılar (rerankers) gibi üst düzey soyutlamaları kademeli olarak ekleyin.

- [Tüm Depo (Repo)](https://github.com/run-llama/llama_docs_bot)
- [[Bölüm 1] LLM'ler ve Komutlar (Prompts)](https://www.youtube.com/watch?v=p0jcvGiBKSA)
- [[Bölüm 2] Dökümanlar ve Metadatalar](https://www.youtube.com/watch?v=nGNoacku0YY)
- [[Bölüm 3] Değerlendirme (Evaluation)](https://www.youtube.com/watch?v=LQy8iHOJE2A)
- [[Bölüm 4] Gömmeler (Embeddings)](https://www.youtube.com/watch?v=2c64G-iDJKQ)
- [[Bölüm 5] Getiriciler (Retrievers) ve Son İşleyiciler (Postprocessors)](https://www.youtube.com/watch?v=mIyZ_9gqakE)

## SubQuestionQueryEngine + 10K Analizi

Bu video, `SubQuestionQueryEngine` konusunu ve karmaşık sorguları birden fazla alt soruya ayırarak finansal dökümanlara nasıl uygulanabileceğini kapsar.

- [Youtube](https://www.youtube.com/watch?v=GT_Lsj3xj1o)
- [Notebook](/python/examples/usecases/10k_sub_question)

## Discord Döküman Yönetimi

Bu video, sürekli güncellenen bir kaynaktan (örneğin Discord) gelen dökümanların yönetilmesini, döküman yinelemesinden nasıl kaçınılacağını ve embedding token'larından nasıl tasarruf edileceğini kapsar.

- [Youtube](https://www.youtube.com/watch?v=j6dJcODLd_c)
- [Notebook ve Ek Materyaller](https://github.com/jerryjliu/llama_index/tree/main/docs/examples/discover_llamaindex/document_management/)
- [Referans Dökümanları](/python/framework/module_guides/indexing/document_management)

## Ortak Metinden SQL'e ve Semantik Arama

Bu video, SQL ve semantik aramayı tek bir birleşik sorgu arayüzünde birleştirmek için LlamaIndex'te yerleşik olarak bulunan araçları kapsar.

- [Youtube](https://www.youtube.com/watch?v=ZIvcVJGtCrY)
- [Notebook](/python/examples/query_engine/sqlautovectorqueryengine)