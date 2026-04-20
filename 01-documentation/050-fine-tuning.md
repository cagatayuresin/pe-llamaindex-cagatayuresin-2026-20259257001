# İnce Ayar (Fine-tuning)

## Genel Bakış

Bir modele ince ayar yapmak, modeli çeşitli şekillerde iyileştirmek için bir veri kümesi üzerinde modelin kendisini güncellemek anlamına gelir. Bu; çıktıların kalitesini artırmayı, halüsinasyonları azaltmayı, daha fazla veriyi bütünsel olarak ezberlemeyi ve gecikme/maliyeti azaltmayı içerebilir.

Araç setimizin özü, modelleri çıkarım (inference) modunda kullanmayı ve modellerin kendilerini eğitmemeyi içeren bağlam içi öğrenme (in-context learning) / getirme zenginleştirmesi (retrieval augmentation) etrafında döner.

İnce ayar, bir modeli harici verilerle "zenginleştirmek" için de kullanılabilse de ince ayar, getirme zenginleştirmesini çeşitli şekillerde tamamlayabilir:

#### Embedding İnce Ayarının Faydaları

-   Embedding modeline ince ayar yapmak, verilerin eğitim dağılımı üzerinde daha anlamlı embedding temsillerine olanak tanır --> bu da daha iyi getirme (retrieval) performansı sağlar.

#### LLM İnce Ayarının Faydaları

-   Belirli bir veri kümesi üzerinde bir stil öğrenmesini sağlar.
-   Eğitim verilerinde daha az temsil edilen bir DSL (örneğin SQL) öğrenmesini sağlar.
-   İstem mühendisliği (prompt engineering) yoluyla düzeltilmesi zor olabilecek halüsinasyonları/hataları düzeltmesini sağlar.
-   Daha iyi bir modeli (örneğin GPT-4) daha basit/ucuz bir modele (örneğin gpt-3.5, Llama 2) damıtmasını (distill) sağlar.

## LlamaIndex ile Entegrasyonlar

Bu gelişen bir kılavuzdur ve şu anda LlamaIndex ile üç temel entegrasyon bulunmaktadır. Daha fazla detay için lütfen aşağıdaki bölümlere göz atın!

-   Daha iyi getirme performansı için embedding'lere ince ayar yapma.
-   Daha iyi metinden SQL'e (text-to-SQL) için Llama 2'ye ince ayar yapma.
-   gpt-4'ü damıtmak için gpt-3.5-turbo'ya ince ayar yapma.

## Embedding'lere İnce Ayar Yapma

Yapılandırılmamış bir metin külliyatı üzerinde modelin kendisine (`bge` gibi) veya herhangi bir kapalı kutu (black-box) embedding üzerinde bir adaptöre (adapter) nasıl ince ayar yapacağınızı gösteren kapsamlı kılavuzlar oluşturduk. Bu süreç aşağıdaki adımlardan oluşur:

1.  Herhangi bir yapılandırılmamış bağlam üzerinde LlamaIndex kullanarak sentetik bir soru/cevap veri kümesi oluşturma.
2.  Modele ince ayar yapma.
3.  Modeli değerlendirme.

İnce ayar, getirme değerlendirme metriklerinde size %5-10'luk bir artış sağlar. Daha sonra bu ince ayarlı modeli LlamaIndex ile RAG uygulamanıza dahil edebilirsiniz.

-   [Bir Adaptöre İnce Ayar Yapma](/python/examples/finetuning/embeddings/finetune_embedding_adapter)
-   [Embedding İnce Ayar Kılavuzu](/python/examples/finetuning/embeddings/finetune_embedding)
-   [Yönlendirici (Router) İnce Ayarı](/python/examples/finetuning/router/router_finetune)

**Eski**

-   [Embedding İnce Ayar Deposu (Repo)](https://github.com/run-llama/finetune-embedding)
-   [Embedding İnce Ayar Bloğu](https://medium.com/llamaindex-blog/fine-tuning-embeddings-for-rag-with-synthetic-data-e534409a3971)

## LLM'lere İnce Ayar Yapma

### GPT-4'ü Damıtmak için GPT-3.5'e İnce Ayar Yapma

RAG/ajanlar için GPT-4 yanıtları çıktı olarak verecek şekilde gpt-3.5-turbo'ya ince ayar yapmak üzere OpenAI'ın ince ayar uç noktalarını nasıl kullanacağınızı gösteren birden fazla kılavuzumuz var.

Herhangi bir yapılandırılmamış bağlamdan otomatik olarak sorular oluşturmak için GPT-4'ü kullanıyoruz ve "doğru" (ground-truth) yanıtlar oluşturmak için bir GPT-4 sorgu motoru akışı kullanıyoruz. `OpenAIFineTuningHandler` geri çağırma (callback) işlevimiz, soruları/cevapları otomatik olarak bir veri kümesine kaydeder.

Ardından bir ince ayar işi başlatıyoruz ve damıtılmış bir model elde ediyoruz. Bu modeli, temel bir GPT-3.5 akışına karşı kıyaslamak için [Ragas](https://github.com/explodinggradients/ragas) ile değerlendirebiliriz.

-   [GPT-3.5 İnce Ayar Notebook (Colab)](https://colab.research.google.com/drive/1NgyCJVyrC2xcZ5lxt2frTU862v6eJHlc?usp=sharing)
-   [GPT-3.5 İnce Ayar Notebook (Notebook bağlantısı)](/python/examples/finetuning/openai_fine_tuning)
-   [[Devam Ediyor] Fonksiyon Çağırma (Function Calling) İnce Ayarı](/python/examples/finetuning/openai_fine_tuning_functions)

**Eski**

-   [GPT-3.5 İnce Ayar Notebook (Colab)](https://colab.research.google.com/drive/1vWeJBXdFEObuihO7Z8ui2CAYkdHQORqo?usp=sharing)
-   [GPT-3.5 İnce Ayar Notebook (Repo içinde)](https://github.com/jerryjliu/llama_index/blob/main/experimental/openai_fine_tuning/openai_fine_tuning.ipynb)

### Daha İyi Yapılandırılmış Çıktılar İçin İnce Ayar

İnce ayar için başka bir kullanım durumu da, modeli yapılandırılmış veriler üretme konusunda daha iyi hale getirmektir. Bunu hem OpenAI hem de Llama 2 için yapabiliriz.

-   [OpenAI Fonksiyon Çağırma İnce Ayarı](/python/examples/finetuning/openai_fine_tuning_functions)

### Daha İyi Metinden SQL'e Geçiş İçin Llama 2 İnce Ayarı

Bu eğitimde, Llama 2'ye metinden SQL'e (text-to-SQL) veri kümesi üzerinde nasıl ince ayar yapabileceğinizi ve ardından bunu LlamaIndex soyutlamalarını kullanarak herhangi bir SQL veritabanına karşı yapılandırılmış analitik için nasıl kullanacağınızı gösteriyoruz.

Teknoloji yığını; eğitim veri kümesi olarak `sql-create-context`, temel model olarak OpenLLaMa, ince ayar için PEFT, bulut hesaplama için Modal ve çıkarım soyutlamaları için LlamaIndex'i içerir.

-   [Llama 2 Metinden SQL'e İnce Ayar (Modal ile, Repo)](https://github.com/run-llama/modal_finetune_sql)
-   [Llama 2 Metinden SQL'e İnce Ayar (Modal ile, Notebook)](https://github.com/run-llama/modal_finetune_sql/blob/main/tutorial.ipynb)

### Bir Değerlendiriciye (Evaluator) İnce Ayar Yapma

Bu eğitimlerde, bir GPT-4 yargıcını (veya değerlendiricisini) bir GPT-3.5 yargıcına damıtmayı amaçlıyoruz. Son zamanlarda GPT-4 yargıçlarının, insan değerlendiricilerle yüksek düzeyde uyum sağlayabildiği gözlemlenmiştir (örneğin, bkz. https://arxiv.org/pdf/2306.05685.pdf).

Bu nedenle, bir GPT-3.5 yargıcına ince ayar yaparak, daha düşük maliyetle GPT-4 seviyelerine (ve dolaylı olarak insanlarla uyuma) ulaşabiliriz.

-   [LLM Doğruluk Yargıcına İnce Ayar Yapma](/python/examples/finetuning/llm_judge/correctness/finetune_llm_judge_single_grading_correctness)
-   [LLM Yargıcına İnce Ayar Yapma](/python/examples/finetuning/llm_judge/pairwise/finetune_llm_judge)

## Yeniden Sıralama (Re-Ranking) İçin Cross-Encoder'lara İnce Ayar Yapma

Bir Cross-Encoder'a ince ayar yaparak, kendi özel verilerimiz üzerindeki yeniden sıralama performansını artırmayı deneyebiliriz.

Yeniden sıralama gelişim getirme (advanced retrieval) sürecinde kilit bir adımdır; burada birçok kaynaktan getirilen node'lar ayrı bir model kullanılarak yeniden sıralanır, böylece en alakalı olanlar en başta yer alır.

Bu örnekte, `QASPER` veri kümesine dayalı olarak oluşturulan bir veri kümesini kullanarak bir Cross-Encoder modeline ince ayar yapmaya yardımcı olması için `sentence-transformers` paketini kullanıyoruz.

-   [Cross-Encoder İnce Ayarı](/python/examples/finetuning/cross_encoder_finetuning/cross_encoder_finetuning)
-   [Metinden SQL'e İçin Llama 2 İnce Ayarı](https://medium.com/llamaindex-blog/easily-finetune-llama-2-for-your-text-to-sql-applications-ecd53640e10d)
-   [GPT-4'ü Damıtmak İçin GPT-3.5 İnce Ayarı](https://colab.research.google.com/drive/1vWeJBXdFEObuihO7Z8ui2CAYkdHQORqo?usp=sharing)

## Cohere Özel Yeniden Sıralayıcı (Custom Reranker)

CohereAI ile özel bir yeniden sıralayıcı eğiterek, kendi özel verilerimiz üzerindeki yeniden sıralama performansını artırmayı deneyebiliriz.

Yeniden sıralama, gelişmiş getirme süreçlerinde çok önemli bir adımdır. Bu adım, ilk getirme aşamasından elde edilen node'ları yeniden düzenlemek için ayrı bir model kullanılmasını içerir. Amaç, en alakalı node'ların önceliklendirilmesini ve ilk sırada görünmesini sağlamaktır.

Bu örnekte, getirme performansını artırmak için alanınıza veya özel veri kümenize ait bir yeniden sıralayıcı oluşturmak üzere `cohere` özel yeniden sıralayıcı eğitim modülünü kullanıyoruz.

-   [Cohere Özel Yeniden Sıralayıcı](/python/examples/finetuning/rerankers/cohere_custom_reranker)