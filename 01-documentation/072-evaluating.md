# Değerlendirme (Evaluating)

## Kavram

Değerlendirme (evaluation) ve kıyaslama (benchmarking), LLM geliştirmede kritik kavramlardır. Bir LLM uygulamasının (RAG, ajanlar) performansını artırmak için onu ölçmenin bir yoluna sahip olmalısınız.

LlamaIndex, oluşturulan sonuçların kalitesini ölçmek için temel modüller sunar. Ayrıca getirme (retrieval) kalitesini ölçmek için de temel modüller sağlıyoruz.

-   **Yanıt Değerlendirmesi (Response Evaluation)**: Yanıt, getirilen bağlamla eşleşiyor mu? Ayrıca sorguyla eşleşiyor mu? Referans cevapla veya kılavuzlarla eşleşiyor mu?
-   **Getirme Değerlendirmesi (Retrieval Evaluation)**: Getirilen kaynaklar sorguyla ilgili mi?

Bu bölüm, LlamaIndex içindeki değerlendirme bileşenlerinin nasıl çalıştığını açıklamaktadır.

### Yanıt Değerlendirmesi

Oluşturulan sonuçların değerlendirilmesi zor olabilir; çünkü geleneksel makine öğreniminin aksine, tahmin edilen sonuç tek bir sayı değildir ve bu sorun için nicel metrikler tanımlamak zor olabilir.

LlamaIndex, sonuçların kalitesini ölçmek için **LLM tabanlı** değerlendirme modülleri sunar. Bu, tahmin edilen cevabın çeşitli şekillerde doğru olup olmadığına karar vermek için bir "altın" (gold) LLM (örneğin GPT-4) kullanır.

Mevcut bu değerlendirme modüllerinin birçoğunun temel gerçeklik (ground-truth) etiketlerine ihtiyaç _duymadığını_ unutmayın. Değerlendirme; sorgu, bağlam, yanıtın bazı kombinasyonları ile yapılabilir ve bunlar LLM çağrılarıyla birleştirilebilir.

Bu değerlendirme modülleri aşağıdaki formlardadır:

-   **Doğruluk (Correctness)**: Oluşturulan cevabın, sorgu verildiğinde referans cevapla eşleşip eşleşmediği (etiket gerektirir).
-   **Anlamsal Benzerlik (Semantic Similarity)**: Tahmin edilen cevabın referans cevapla anlamsal olarak benzer olup olmadığı (etiket gerektirir).
-   **Sadakat (Faithfulness)**: Cevabın getirilen bağlamlara sadık olup olmadığını değerlendirir (başka bir deyişle, halüsinasyon olup olmadığını kontrol eder).
-   **Bağlam İlgililiği (Context Relevancy)**: Getirilen bağlamın sorguyla ilgili olup olmadığı.
-   **Cevap İlgililiği (Answer Relevancy)**: Oluşturulan cevabın sorguyla ilgili olup olmadığı.
-   **Kılavuza Uyumluluk (Guideline Adherence)**: Tahmin edilen cevabın belirli kılavuzlara uyup uymadığı.

#### Soru Oluşturma (Question Generation)

Sorguları değerlendirmeye ek olarak LlamaIndex, üzerinde değerlendirme yapmak üzere sorular oluşturmak için verilerinizi de kullanabilir. Bu, otomatik olarak sorular oluşturabileceğiniz ve ardından LLM'in verilerinizi kullanarak soruları gerçekten doğru bir şekilde yanıtlayıp yanıtlayamadığını test etmek için bir değerlendirme akışı çalıştırabileceğiniz anlamına gelir.

### Getirme Değerlendirmesi (Retrieval Evaluation)

Getirmeyi bağımsız olarak değerlendirmeye yardımcı olacak modüller de sağlıyoruz.

Getirme değerlendirmesi kavramı yeni değildir; bir soru seti ve temel gerçeklik sıralamaları (ground-truth rankings) verildiğinde, getiricileri (retrievers); karşılıklı sıralama ortalaması (MRR), isabet oranı (hit-rate), kesinlik (precision) ve daha fazlası gibi sıralama metriklerini kullanarak değerlendirebiliriz.

Temel getirme değerlendirmesi adımları şunlar etrafında döner:

-   **Veri Kümesi Oluşturma (Dataset generation)**: Yapılandırılmamış bir metin külliyatı (corpus) verildiğinde, sentetik olarak (soru, bağlam) çiftleri oluşturulur.
-   **Getirme Değerlendirmesi**: Bir getirici ve bir dizi soru verildiğinde, getirilen sonuçlar sıralama metrikleri kullanılarak değerlendirilir.

## Entegrasyonlar

Ayrıca topluluk değerlendirme araçlarıyla da entegre oluyoruz.

-   [UpTrain](https://github.com/uptrain-ai/uptrain)
-   [Tonic Validate](/python/framework/community/integrations/tonicvalidate) (Sonuçları görselleştirmek için Web arayüzü içerir)
-   [DeepEval](https://github.com/confident-ai/deepeval)
-   [Ragas](https://github.com/explodinggradients/ragas/blob/main/docs/howtos/integrations/llamaindex.ipynb)
-   [RAGChecker](https://github.com/amazon-science/RAGChecker)
-   [Cleanlab](/python/examples/evaluation/cleanlab)

## Kullanım Kalıbı (Usage Pattern)

Tam kullanım ayrıntıları için aşağıdaki kullanım kalıplarına bakın.

-   [Sorgu Değerlendirme Kullanım Kalıbı](/python/framework/module_guides/evaluating/usage_pattern)
-   [Getirme Değerlendirme Kullanım Kalıbı](/python/framework/module_guides/evaluating/usage_pattern_retrieval)

## Modüller

Bu bileşenlerin kullanımını içeren notebook'lar [modül kılavuzlarında](/python/framework/module_guides/evaluating/modules) bulunabilir.

## `LabelledRagDataset`'ler ile Değerlendirme

`LabelledRagDataset` olarak adlandırılan çeşitli değerlendirme veri kümeleriyle bir RAG sisteminin değerlendirmesinin nasıl gerçekleştirileceğine dair ayrıntılar için aşağıya bakın:

-   [Değerlendirme](/python/framework/module_guides/evaluating/evaluating_with_llamadatasets)
-   [Katkıda Bulunma](/python/framework/module_guides/evaluating/contributing_llamadatasets)