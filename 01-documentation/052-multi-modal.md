# Çok Modlu (Multi-modal)

LlamaIndex, yalnızca dil tabanlı uygulamalar değil, aynı zamanda dil ve görüntüleri birleştiren **çok modlu (multi-modal)** uygulamalar oluşturma yetenekleri sunar.

## Çok Modlu Kullanım Durumu Türleri

Bu alan şu anda aktif olarak keşfedilmektedir, ancak bazı büyüleyici kullanım durumları ortaya çıkmaktadır.

### RAG (Vektör Getirme ile Zenginleştirilmiş Oluşturma)

Tüm temel RAG kavramları (indeksleme, getirme ve sentezleme), görüntü ortamına genişletilebilir.

-   Girdi, metin veya görüntü olabilir.
-   Saklanan bilgi tabanı metin veya görüntülerden oluşabilir.
-   Yanıt oluşturma girdileri metin veya görüntü olabilir.
-   Nihai yanıt metin veya görüntü olabilir.

Aşağıdaki kılavuzlarımıza göz atın:

-   [GPT-4V Çok Modlu](/python/examples/multi_modal/gpt4v_multi_modal_retrieval)
-   [CLIP ile Çok Modlu Getirme](/python/examples/multi_modal/multi_modal_retrieval)
-   [Görüntüden Görüntüye Getirme](/python/examples/multi_modal/image_to_image_retrieval)
-   [Yapılandırılmış Görüntü Getirme](/python/examples/multi_modal/structured_image_retrieval)
-   [Chroma Çok Modlu](/python/examples/multi_modal/chromamultimodaldemo)
-   [Gemini Çok Modlu](/python/examples/multi_modal/gemini)

### Yapılandırılmış Çıktılar

LlamaIndex aracılığıyla yeni OpenAI GPT-4V ile `yapılandırılmış` bir çıktı oluşturabilirsiniz. Kullanıcının çıktı yapısını tanımlamak için bir Pydantic nesnesi belirtmesi yeterlidir.

Aşağıdaki kılavuza göz atın:

-   [Çok Modlu Pydantic Programı](/python/examples/multi_modal/multi_modal_pydantic)

### Getirme ile Zenginleştirilmiş Görüntü Altyazısı (Image Captioning)

Çoğu zaman bir görüntüyü anlamak, bir bilgi tabanından bilgi aramayı gerektirir. Buradaki bir akış, getirme ile zenginleştirilmiş görüntü altyazısıdır; önce görüntüyü çok modlu bir modelle altyazılandırın, ardından altyazıyı bir metin külliyatından getirerek rafine edin.

Aşağıdaki kılavuzlarımıza göz atın:

-   [Llava + Tesla 10Q](/python/examples/multi_modal/llava_multi_modal_tesla_10q)

### Ajanlar (Agents)

İşte GPT-4V ile ajan yeteneklerini gösteren bazı ilk çalışmalar.

-   [Çok Modlu Ajanlar](/python/framework/module_guides/deploying/agents#multi-modal-agents)
-   [GPT-4V Deneyleri](/python/examples/multi_modal/gpt4v_experiments_cot)

## Değerlendirmeler ve Karşılaştırmalar

Bu bölümler, farklı kullanım durumları için farklı çok modlu modeller arasındaki karşılaştırmaları gösterir.

### Görüntü Akıl Yürütme İçin LLaVa-13, Fuyu-8B ve MiniGPT-4 Çok Modlu LLM Modellerinin Karşılaştırılması

Bu notebook'lar, görüntü anlama/akıl yürütme için farklı Çok Modlu LLM modellerinin nasıl kullanılacağını gösterir. Çeşitli model çıkarımları Replicate veya OpenAI GPT-4V API tarafından desteklenmektedir. Birkaç popüler Çok Modlu LLM'i karşılaştırdık:

-   GPT-4V (OpenAI API)
-   LLava-13B (Replicate)
-   Fuyu-8B (Replicate)
-   MiniGPT-4 (Replicate)
-   CogVLM (Replicate)

Aşağıdaki kılavuzlarımıza göz atın:

-   [Replicate Çok Modlu](/python/examples/multi_modal/replicate_multi_modal)
-   [GPT-4V](/python/examples/multi_modal/openai_multi_modal)

### Çok Modlu RAG'in Basit Değerlendirmesi

Bu notebook kılavuzunda, Çok Modlu bir RAG sisteminin nasıl değerlendirileceğini göstereceğiz. Sadece metin içeren durumda olduğu gibi, Retriever'ların (Getiriciler) ve Generator'ların (Oluşturucular) değerlendirmesini ayrı ayrı ele alacağız. Bu konudaki blog yazımızda belirttiğimiz gibi, buradaki yaklaşımımız hem Retriever'ı hem de Generator'ı (sadece metin içeren durumda kullanılan) değerlendirmek için kullanılan alışılagelmiş tekniklerin uyarlanmış versiyonlarının uygulanmasını içerir. Bu uyarlanmış versiyonlar llama-index kütüphanesinin (yani değerlendirme modülünün) bir parçasıdır ve bu notebook bunları kendi değerlendirme kullanım durumlarınıza nasıl uygulayabileceğiniz konusunda size rehberlik edecektir.

-   [Çok Modlu RAG Değerlendirmesi](/python/examples/evaluation/multi_modal/multi_modal_rag_evaluation)

## Model Kılavuzları

İşte farklı çok modlu model sağlayıcılarıyla nasıl etkileşim kuracağınızı gösteren notebook kılavuzları.

-   [OpenAI Çok Modlu](/python/examples/multi_modal/openai_multi_modal)
-   [Replicate Çok Modlu](/python/examples/multi_modal/replicate_multi_modal)