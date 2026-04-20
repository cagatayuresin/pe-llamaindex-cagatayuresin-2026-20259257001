# Soru-Cevap (RAG)

LLM'ler için en yaygın kullanım durumlarından biri, bir veri kümesi üzerinde soruları yanıtlamaktır. Bu veriler genellikle yapılandırılmamış dökümanlar (örneğin PDF'ler, HTML) biçimindedir, ancak yarı yapılandırılmış veya yapılandırılmış da olabilir.

LLM'ler ile soru-cevap yapmayı sağlayan baskın çerçeve Getirme Zenginleştirmeli Oluşturma'dır (Retrieval Augmented Generation - RAG). LlamaIndex; farklı hacim ve türdeki veriler üzerinde basitten karmaşığa soruları çözmek için basitten gelişim aşamasına kadar RAG teknikleri sunar. İster önceden oluşturulmuş RAG soyutlamalarımızı (örneğin [sorgu motorları](/python/framework/module_guides/deploying/query_engine)) kullanabilir, isterseniz de özel RAG [iş akışları](/python/framework/module_guides/workflow) oluşturabilirsiniz (örnek [kılavuz](/python/examples/workflow/rag)).

## Yapılandırılmamış Dökümanlar Üzerinde RAG

LlamaIndex; yapılandırılmamış metin, PDF, Notion ve Slack dökümanlarını ve daha fazlasını çekebilir ve içlerindeki verileri indeksleyebilir.

En basit sorgular ya anlamsal aramayı ya da özetlemeyi içerir.

-   **Anlamsal arama (Semantic search)**: Bir dökümandaki, sorgu terimleri ve/veya anlamsal niyetle eşleşen belirli bir bilgi hakkındaki sorgu. Bu genellikle basit vektör getirme (top-k) ile yürütülür. [Anlamsal arama örneği](/python/framework/understanding/putting_it_all_together/q_and_a#semantic-search)
-   **Özetleme (Summarization)**: Büyük miktardaki veriyi mevcut sorunuzla ilgili kısa bir özete sıkıştırmak. [Özetleme örneği](/python/framework/understanding/putting_it_all_together/q_and_a#summarization)

## Yapılandırılmış Veriler Üzerinde Soru-Cevap

Verileriniz halihazırda bir SQL veritabanında, CSV dosyasında veya başka bir yapılandırılmış formatta bulunuyorsa LlamaIndex bu kaynaklardaki verileri sorgulayabilir. Bu, **metinden SQL'e** (text-to-SQL, doğal dilden SQL işlemlerine) ve ayrıca **metinden Pandas'a** (text-to-Pandas, doğal dilden Pandas işlemlerine) geçişi içerir.

-   [Metinden SQL'e Kılavuzu](/python/examples/index_structs/struct_indices/sqlindexdemo)
-   [Metinden Pandas'a Kılavuzu](/python/examples/query_engine/pandas_query_engine)

## Gelişmiş Soru-Cevap Konuları

Daha karmaşık sorulara / daha fazla veriye ölçeklendikçe, LlamaIndex'te daha iyi sorgu anlama, getirme ve veri kaynaklarının entegrasyonu konusunda size yardımcı olacak birçok teknik mevcuttur.

-   **Karmaşık Dökümanları Sorgulama**: Çoğu zaman döküman temsiliniz karmaşıktır - PDF'iniz metin, tablolar, grafikler, görüntüler, üstbilgiler/altbilgiler ve daha fazlasını içerebilir. LlamaIndex, tescilli döküman ayrıştırıcımız olan LlamaParse ile entegre gelişmiş indeksleme/getirme sağlar. [Tam tarifler (cookbooks) burada](https://github.com/run-llama/llama_parse/tree/main/examples).
-   **Birden Çok Kaynağı Birleştirme**: Verilerinizin bir kısmı Slack'te, bir kısmı PDF'lerde, bir kısmı yapılandırılmamış metinlerde mi? LlamaIndex, istediğiniz sayıda kaynak genelindeki sorguları birleştirebilir ve sonuçları sentezleyebilir.
    -   [Birden çok kaynağı birleştirme örneği](/python/framework/understanding/putting_it_all_together/q_and_a#multi-document-queries)
-   **Birden Çok Kaynak Arasında Yönlendirme**: Birden çok veri kaynağı verildiğinde, uygulamanız önce en iyi kaynağı seçebilir ve ardından soruyu o kaynağa "yönlendirebilir".
    -   [Birden çok kaynak arasında yönlendirme örneği](/python/framework/understanding/putting_it_all_together/q_and_a#routing-over-heterogeneous-data)
-   **Çoklu Döküman Sorguları**: Bazı soruların, birleştirilmeden önce ayrı ayrı sorgulanması gereken birden çok veri kaynağında kısmi cevapları vardır.
    -   [Çoklu döküman sorguları örneği](/python/framework/understanding/putting_it_all_together/q_and_a#multi-document-queries)
    -   [LlamaIndex dökümanları üzerinde çoklu döküman ajanı oluşturma](/python/examples/agent/multi_document_agents-v1) - [Metinden SQL'e](/python/examples/index_structs/struct_indices/sqlindexdemo)

## Kaynaklar

LlamaIndex'in Soru-Cevap / RAG etrafında birçok kaynağı vardır. İşte başvurulacak bazı temel kaynak kılavuzları:

**RAG'e yeni başlayan biriyim ve temelleri öğrenmek istiyorum**: ["Öğrenme" (Learn) serisi kılavuzlarımıza](/python/framework/understanding) göz atın.

**RAG sistemini kurdum ve şimdi optimize etmek istiyorum**: ["Gelişmiş Konular" Kılavuzlarımıza](/python/framework/optimizing/production_rag) göz atın.

**Daha ileri seviyedeyim ve özel bir RAG iş akışı oluşturmak istiyorum**: Bu [Düzeltici RAG (Corrective RAG)](/python/examples/workflow/corrective_rag_pack) iş akışı gibi gelişmiş, ajanlı RAG boru hatları (pipelines) oluşturmak için LlamaIndex [iş akışlarını (workflows)](/python/framework/module_guides/workflow) kullanın.

**Belirli bir modül hakkında her şeyi öğrenmek istiyorum**: Basitten gelişim aşamasına kadar Soru-Cevap/RAG sistemleri oluşturmaya yardımcı olacak temel modül kılavuzları şunlardır:

-   [Sorgu Motorları (Query Engines)](/python/framework/module_guides/deploying/query_engine)
-   [Sohbet Motorları (Chat Engines)](/python/framework/module_guides/deploying/chat_engines)
-   [Ajanlar (Agents)](/python/framework/module_guides/deploying/agents)

## Daha Fazla Örnek

Soru-Cevap kullanım durumlarının daha fazla örneği için ["Hepsini Bir Araya Getirme" bölümündeki Soru-Cevap kısmına](/python/framework/understanding/putting_it_all_together/q_and_a) bakın.