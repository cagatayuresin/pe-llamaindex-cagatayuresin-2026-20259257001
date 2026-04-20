# Bir LLM Uygulaması Oluşturmak

"LlamaIndex'i Anlama" bölümüne hoş geldiniz. Bu bölüm, daha gelişmiş ve ince stratejilere dalmadan önce LlamaIndex'i nasıl kullanacağınızı öğrenmeniz için bir "ajanik" (agentic) LLM uygulaması oluşturmanın her aşamasını kapsayan kısa ve öz eğitimlerden oluşan bir seridir. Eğer LlamaIndex'e yeni olan deneyimli bir programcıysanız, başlamak için doğru yer burasıdır.

## Bir Ajanik LLM Uygulaması Oluşturmanın Temel Adımları

> **İpucu:** Bu terimler size yabancı geliyorsa [üst düzey kavramlar](/python/framework/getting_started/concepts) bölümümüzü okumak isteyebilirsiniz.

Bu eğitim üç ana bölümden oluşur: **Bir RAG hattı (pipeline) oluşturmak**, **Bir ajan oluşturmak** ve **İş Akışları (Workflows) oluşturmak**. İşte sizi bekleyenler:

- **[LLM'leri Kullanma](/python/framework/understanding/using_llms)**: LLM'lerle çalışmaya hemen başlayın. İster uzak API çağrıları yoluyla ister makinenizde yerel olarak çalıştırarak, [desteklenen düzinelerce LLM'imizden](/python/framework/module_guides/models/llms/modules) herhangi birini nasıl kullanacağınızı göstereceğiz.

- **[Ajanlar Oluşturma](/python/framework/understanding/agent)**: Ajanlar, bir dizi araç aracılığıyla dünyayla etkileşime girebilen LLM destekli bilgi işçileridir. Bu araçlar bilgi getirebilir (aşağıda göreceğiniz RAG gibi) veya eyleme geçebilir. Bu eğitim şunları içerir:

  - **[Tek Bir Ajan Oluşturma](/python/framework/understanding/agent)**: Bir dizi araç aracılığıyla dünyayla etkileşime girebilen basit bir ajanı nasıl oluşturacağınızı gösteriyoruz.
  - **[Mevcut Araçları Kullanma](/python/framework/understanding/agent/tools)**: LlamaIndex, [LlamaHub](https://llamahub.ai/) adresinde ajanlarınıza dahil edebileceğiniz önceden oluşturulmuş bir araç kaydı sunar.
  - **[Durumu (State) Koruma](/python/framework/understanding/agent/state)**: Ajanlar durumu koruyabilir, bu da daha karmaşık uygulamalar oluşturmak için önemlidir.
  - **[Çıktı ve Olay Akışı (Streaming)](/python/framework/understanding/agent/streaming)**: Kullanıcıya görünürlük ve geri bildirim sağlamak önemlidir; akış (streaming) bunu yapmanıza olanak tanır.
  - **[Döngüde İnsan (Human-in-the-loop)](/python/framework/understanding/agent/human_in_the_loop)**: Ajanınız için insan geri bildirimi almak kritik olabilir.
  - **[AgentWorkflow ile Çoklu Ajan Sistemleri](/python/framework/understanding/agent/multi_agent)**: Birden fazla ajanı iş birliği yapacak şekilde birleştirmek, daha karmaşık sistemler oluşturmak için güçlü bir tekniktir; bu bölüm bunu nasıl yapacağınızı gösterir.

- **[İş Akışları (Workflows)](/python/llamaagents/workflows)**: İş Akışları, ajan uygulamaları oluşturmak için daha alt düzey, olay odaklı bir soyutlamadır. Her türlü gelişmiş ajan uygulamasını oluşturmak için kullanmanız gereken temel katmandır. Yukarıda öğrendiğiniz önceden oluşturulmuş soyutlamaları kullanabilir veya tamamen sıfırdan ajanlar oluşturabilirsiniz. Bu eğitim şunları kapsar:

  - **[Basit Bir İş Akışı Oluşturma](/python/llamaagents/workflows)**: Temel bir ajan uygulaması oluşturmak için `Workflow` sınıfını nasıl kullanacağınızı gösteren basit bir iş akışı.
  - **[Döngü Oluşturma ve Dallanma](/python/llamaagents/workflows/branches_and_loops)**: Bu temel kontrol akışı kalıpları, daha karmaşık iş akışlarının yapı taşlarıdır.
  - **[Eşzamanlı Yürütme](/python/llamaagents/workflows/concurrent_execution)**: İşi verimli bir şekilde bölmek için adımları paralel olarak çalıştırabilirsiniz.
  - **[Olay Akışı (Streaming Events)](/python/llamaagents/workflows/stream)**: Ajanlarınız, yukarıda oluşturduğunuz ajanlar gibi kullanıcıya yönelik olaylar yayınlayabilir.
  - **[Durumlu (Stateful) İş Akışları](/python/llamaagents/workflows/managing_state)**: İş akışları durumu koruyabilir, bu da daha karmaşık uygulamalar oluşturmak için önemlidir.
  - **[Gözlemlenebilirlik (Observability)](/python/llamaagents/workflows/observability)**: İş akışları Arize Phoenix, OpenTelemetry ve daha fazlası gibi çeşitli entegrasyonlar kullanılarak izlenebilir ve hataları ayıklanabilir.

- **[Ajanlarınıza RAG Ekleme](/python/framework/understanding/rag)**: Veri Getirme ile Güçlendirilmiş Üretim (RAG), verilerinizi bir LLM'e iletmek için temel bir tekniktir ve daha sofistike ajan sistemlerinin bir bileşenidir. Ajanlarınızı, verileriniz hakkındaki soruları yanıtlayabilen tam özellikli bir RAG hattıyla nasıl geliştireceğinizi göstereceğiz. Bu şunları içerir:

  - **[Yükleme ve Aktarma (Loading & Ingestion)](/python/framework/understanding/rag/loading)**: Yapılandırılmamış metin, PDF'ler, veritabanları veya diğer uygulamalara ait API'ler olsun, verilerinizi yaşadığı her yerden almak. LlamaIndex, [LlamaHub](https://llamahub.ai/) üzerinde her veri kaynağına bağlanan yüzlerce bağlayıcıya sahiptir.
  - **[İndeksleme ve Embedding](/python/framework/understanding/rag/indexing)**: Verilerinizi aldıktan sonra, uygulamanızın her zaman en alakalı verilerle çalışmasını sağlamak için bu verilere erişimi yapılandırmanın sonsuz yolu vardır. LlamaIndex birçok yerleşik stratejiye sahiptir ve en iyilerini seçmenize yardımcı olabilir.
  - **[Saklama (Storing)](/python/framework/understanding/rag/storing)**: Verilerinizi indekslenmiş formda veya bir LLM tarafından sağlanan önceden işlenmiş özetler halinde saklamayı, genellikle `Vector Store` (Vektör Deposu) olarak bilinen özel bir veritabanında saklamayı daha verimli bulacaksınız. Ayrıca indekslerinizi, metadatalarınızı ve daha fazlasını da saklayabilirsiniz.
  - **[Sorgulama (Querying)](/python/framework/understanding/rag/querying)**: Her indeksleme stratejisinin karşılık gelen bir sorgulama stratejisi vardır. Getirdiğiniz verilerin alakasını, hızını ve doğruluğunu; ayrıca LLM'in bunu size döndürmeden önce ne yapacağını iyileştirmenin (verileri bir API gibi yapılandırılmış yanıtlara dönüştürmek dahil) birçok yolu vardır.

- **[Hepsini Bir Araya Getirmek](/python/framework/understanding/putting_it_all_together)**: İster Soru-Cevap sistemi, ister sohbet robotu, ister bir API veya otonom bir ajan oluşturuyor olun, uygulamanızı üretim (production) aşamasına nasıl getireceğinizi gösteriyoruz.

- **[İzleme ve Hata Ayıklama (Tracing and Debugging)](/python/framework/understanding/tracing_and_debugging/tracing_and_debugging)**: **Gözlemlenebilirlik** olarak da adlandırılır; LLM uygulamalarında, sorunları ayıklamanıza ve iyileştirme yapılabilecek yerleri tespit etmenize yardımcı olmak için işlerin iç yüzüne bakabilmek özellikle önemlidir.

- **[Değerlendirme (Evaluating)](/python/framework/understanding/evaluating/evaluating)**: Her stratejinin artıları ve eksileri vardır. Uygulamanızı oluşturmanın, yayınlamanın ve geliştirmenin anahtar bir parçası; yaptığınız değişikliğin doğruluk, performans, netlik, maliyet ve daha fazlası açısından uygulamanızı iyileştirip iyileştirmediğini değerlendirmektir. Değişikliklerinizi güvenilir bir şekilde değerlendirmek, LLM uygulama geliştirmenin kritik bir parçasıdır.

## Haydi Başlayalım!

Dalmaya hazır mısınız? [LLM'leri Kullanma](/python/framework/understanding/using_llms) bölümüne geçin.