# `LabelledRagDataset` ile Katkıda Bulunma

Daha sağlam bir RAG sistemi oluşturmak, çeşitlendirilmiş bir değerlendirme paketine ihtiyaç duyar. Bu nedenle [LlamaHub](https://llamahub.ai) üzerinde `LlamaDatasets`'i başlattık. Bu sayfada, LlamaHub'da kullanıma sunulan ilk `LlamaDataset` türü olan `LabelledRagDataset` ile nasıl katkıda bulunabileceğinizi ele alıyoruz.

Bir `LabelledRagDataset` ile katkıda bulunmak iki üst düzey adım içerir. Genel olarak konuşursak, `LabelledRagDataset`'i oluşturmalı, bir JSON dosyası olarak kaydetmeli ve hem bu JSON dosyasını hem de kaynak metin dosyalarını [llama-datasets depomuza (repository)](https://github.com/run-llama/llama_datasets) göndermelisiniz. Ek olarak, veri kümesinin gerekli meta verilerini [llama-hub depomuza](https://github.com/run-llama/llama-hub) yüklemek için bir çekme isteği (pull request) oluşturmanız gerekecektir.

Gönderim sürecini daha sorunsuz hale getirmeye yardımcı olmak için, sıfırdan bir `LabelledRagDataset` oluşturmak (veya benzer yapıdaki bir soru-cevap veri kümesini buna dönüştürmek) ve gönderiminizi yapmak için gereken diğer adımları gerçekleştirmek üzere takip edebileceğiniz bir şablon notebook hazırladık. Lütfen aşağıda bağlantısı verilen "LlamaDataset Gönderim Şablonu Notebook'una" bakın.

## Diğer llama-dataset'ler ile Katkıda Bulunma

`LabelledEvaluatorDataset` gibi diğer llama-dataset'lerimizden herhangi biri ile katkıda bulunmaya yönelik genel süreç, daha önce açıklanan `LabelledRagDataset` süreciyle aynıdır. Bu diğer veri kümeleri için gönderim şablonları yakında eklenecek!

## Gönderim Örneği

Tam [gönderim örneği Notebook'unu](/python/examples/llama_dataset/ragdataset_submission_template) okuyun.