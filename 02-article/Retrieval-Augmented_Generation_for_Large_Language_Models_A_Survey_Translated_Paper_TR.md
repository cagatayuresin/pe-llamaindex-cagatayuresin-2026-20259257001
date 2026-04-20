# Large Language Models için Retrieval-Augmented Generation: Bir İnceleme

**Yunfan Gao<sup>a</sup>, Yun Xiong<sup>b</sup>, Xinyu Gao<sup>b</sup>, Kangxiang Jia<sup>b</sup>, Jinliu Pan<sup>b</sup>, Yuxi Bi<sup>c</sup>, Yi Dai<sup>a</sup>, Jiawei Sun<sup>a</sup>, Meng Wang<sup>c</sup>, ve Haofen Wang<sup>a,c</sup>**

<sup>a</sup>Shanghai Research Institute for Intelligent Autonomous Systems, Tongji University
<sup>b</sup>Shanghai Key Laboratory of Data Science, School of Computer Science, Fudan University
<sup>c</sup>College of Design and Innovation, Tongji University

---

## Özet

Large Language Models (LLMs), etkileyici yetenekler sergilemekle birlikte, hallucination (halüsinasyon), güncel olmayan bilgi ve şeffaf olmayan, izlenemeyen akıl yürütme süreçleri gibi zorluklarla karşılaşmaktadır. Retrieval-Augmented Generation (RAG), harici veritabanlarından gelen bilgileri entegre ederek bu sorunlara umut verici bir çözüm olarak ortaya çıkmıştır. Bu, özellikle bilgi yoğun görevler için oluşturulan içeriğin doğruluğunu ve güvenilirliğini artırırken, sürekli bilgi güncellemelerine ve alana özgü bilgilerin entegrasyonuna olanak tanır. RAG, LLM'lerin içsel bilgilerini harici veritabanlarının geniş ve dinamik depolarıyla sinerjik bir şekilde birleştirir. Bu kapsamlı inceleme makalesi; Naive RAG, Advanced RAG ve Modular RAG'ı kapsayan RAG paradigmalarının gelişimini detaylı bir inceleme ile sunmaktadır. Retrieval (getirme), generation (oluşturma) ve augmentation (zenginleştirme) tekniklerini içeren RAG çerçevelerinin üçlü temelini titizlikle analiz eder. Makale, bu kritik bileşenlerin her birinde yer alan en son teknolojileri vurgulayarak RAG sistemlerindeki ilerlemeler hakkında derinlemesine bir anlayış sağlar. Ayrıca, bu makale güncel değerlendirme çerçevesini ve benchmark (kıyaslama) çalışmalarını tanıtmaktadır. Son olarak, bu makale şu anda karşılaşılan zorlukları ana hatlarıyla belirtir ve araştırma ile geliştirme için gelecekteki olası yollara işaret eder.

> Kaynaklar şu adreste mevcuttur: [https://github.com/Tongji-KGLLM/RAG-Survey](https://github.com/Tongji-KGLLM/RAG-Survey)

**Dizin Terimleri** — Large language model, retrieval-augmented generation, natural language processing, information retrieval

---

## I. GİRİŞ

Large language models (LLMs) dikkate değer bir başarı elde etmiş olsa da, özellikle alana özgü veya bilgi yoğun görevlerde [1], özellikle eğitim verilerinin ötesindeki sorguları işlerken veya güncel bilgi gerektirirken "hallucinations" [2] üretme gibi önemli sınırlamalarla karşı karşıyadır. Bu zorlukların üstesinden gelmek için Retrieval-Augmented Generation (RAG), harici bir knowledge base üzerinden anlamsal benzerlik hesaplaması yoluyla ilgili doküman parçalarını getirerek LLM'leri güçlendirir. RAG, harici bilgilere atıfta bulunarak olgusal olarak yanlış içerik üretme sorununu etkili bir şekilde azaltır. LLM'lere entegrasyonu, RAG'ın chatbot'ları ilerletmede ve LLM'lerin gerçek dünya uygulamaları için uygunluğunu artırmada temel bir teknoloji olarak kabul edilmesini sağlamıştır ve yaygın bir şekilde benimsenmesine yol açmıştır.

RAG teknolojisi son yıllarda hızla gelişmiş ve ilgili araştırmaları özetleyen teknoloji ağacı Şekil 1'de gösterilmiştir.

![Şekil 1: RAG Teknoloji Ağacı](images/page2_img1.png)

Büyük modeller çağında RAG'ın gelişim yörüngesi birkaç farklı aşama özelliği sergilemektedir. Başlangıçta, RAG'ın doğuşu, Pre-Training Models (PTM) aracılığıyla ek bilgiler ekleyerek dil modellerini geliştirmeye odaklanan Transformer mimarisinin yükselişiyle çakışmıştır. Bu erken aşama, ön eğitim tekniklerini iyileştirmeyi amaçlayan temel çalışmalarla karakterize edilmiştir [3]–[5]. Sonrasında ChatGPT'nin [6] gelişi, LLM'nin güçlü in-context learning (ICL) yeteneklerini sergilemesiyle dönüm noktası oluşturmuştur. RAG araştırmaları, çıkarım (inference) aşamasında LLM'lere daha karmaşık ve bilgi yoğun görevleri yanıtlamaları için daha iyi bilgi sağlamaya doğru kaymış ve RAG çalışmalarında hızlı bir gelişmeye yol açmıştır. Araştırmalar ilerledikçe, RAG'ın geliştirilmesi artık çıkarım aşamasıyla sınırlı kalmamış, LLM fine-tuning teknikleriyle daha fazla bütünleşmeye başlamıştır.

Gelişmekte olan RAG alanı hızlı bir büyüme yaşamış olsa da, buna daha geniş gidişatını açıklığa kavuşturabilecek sistematik bir sentez eşlik etmemiştir. Bu inceleme, RAG sürecini haritalandırarak ve RAG'ın LLM'ler içindeki entegrasyonuna odaklanarak gelişimini ve beklenen gelecek yollarını çizerek bu boşluğu doldurmaya çalışmaktadır. Bu makale hem teknik paradigmaları hem de araştırma yöntemlerini dikkate alarak 100'den fazla RAG çalışmasından üç ana araştırma paradigmasını özetlemekte ve "Retrieval", "Generation" ve "Augmentation"ın temel aşamalarındaki kilit teknolojileri analiz etmektedir. Diğer taraftan, mevcut araştırmalar yöntemlere odaklanma eğilimindedir ve RAG'ın nasıl değerlendirileceğine dair analiz ve özetleme konusunda eksiklik yaşamaktadır. Bu makale RAG'a uygulanabilir aşağı akış görevlerini, veri kümelerini, benchmark'ları ve değerlendirme yöntemlerini kapsamlı bir şekilde incelemektedir. Genel olarak bu makale, LLM sonrası ortaya çıkan temel teknik kavramları, tarihsel gelişimi ve RAG metodolojileri ile uygulamaları yelpazesini titizlikle derlemeyi ve kategorize etmeyi amaçlamaktadır. Okuyucuları ve profesyonelleri hem büyük modeller hem de RAG hakkında ayrıntılı ve yapılandırılmış bir anlayışla donatmak için tasarlanmıştır. Retrieval augmentation tekniklerinin evrimini aydınlatmayı, ilgili bağlamlarda çeşitli yaklaşımların güçlü ve zayıf yönlerini değerlendirmeyi ve gelecek trendleri ve yenilikler hakkında spekülasyon yapmayı hedeflemektedir.

Katkılarımız şunlardır:

- Bu incelemede, en son RAG yöntemlerinin kapsamlı ve sistematik bir incelemesini sunuyor, gelişimini naive RAG, advanced RAG ve modular RAG gibi paradigmalar üzerinden ana hatlarıyla belirtiyoruz. Bu inceleme, RAG araştırmalarının kapsamını LLM'ler bağlamında kavramsallaştırmaktadır.
- RAG sürecinin ayrılmaz bir parçası olan merkezi teknolojileri, özellikle "Retrieval", "Generation" ve "Augmentation" yönlerine odaklanarak tanımlıyor ve tartışıyoruz. Bu bileşenlerin uyumlu ve etkili bir RAG çerçevesi oluşturmak için nasıl karmaşık bir şekilde iş birliği yaptığını açıklayarak sinerjilerini derinlemesine inceliyoruz.
- 26 görevi ve yaklaşık 50 veri kümesini kapsayan, değerlendirme amaçlarını ve metriklerini, ayrıca mevcut değerlendirme benchmark'larını ve araçlarını ana hatlarıyla belirten mevcut RAG değerlendirme yöntemlerini özetledik. Ek olarak, mevcut zorlukların üstesinden gelmek için potansiyel geliştirmeleri vurgulayarak RAG için gelecek yönelimlerini öngörüyoruz.

Makale şu şekilde ilerlemektedir: Bölüm II, RAG'ın ana konseptini ve mevcut paradigmalarını tanıtmaktadır. Takip eden üç bölüm çekirdek bileşenleri — sırasıyla "Retrieval", "Generation" ve "Augmentation"ı incelemektedir. Bölüm III; indeksleme, sorgu (query) ve embedding optimizasyonu dahil olmak üzere retrieval'daki optimizasyon yöntemlerine odaklanmaktadır. Bölüm IV, retrieval sonrası süreçlere ve generation'daki LLM fine-tuning'e yoğunlaşmaktadır. Bölüm V, üç augmentation sürecini analiz etmektedir. Bölüm VI, RAG'ın aşağı akış (downstream) görevlerine ve değerlendirme sistemine odaklanmaktadır. Bölüm VII, esas olarak RAG'ın şu anda karşılaştığı zorlukları ve gelecekteki gelişim yönlerini tartışmaktadır. Son olarak, makale Bölüm VIII'de sonuçlanmaktadır.

---

## II. RAG'E GENEL BAKIŞ

Tipik bir RAG uygulaması Şekil 2'de gösterilmektedir. Burada bir kullanıcı, ChatGPT'ye son zamanlarda geniş çapta tartışılan bir haber hakkında soru sorar.

![Şekil 2: Tipik bir RAG uygulaması](images/page3_img1.png)

ChatGPT'nin ön eğitim verilerine olan bağımlılığı göz önüne alındığında, başlangıçta son gelişmeler hakkında güncel bilgi sağlama kapasitesinden yoksundur. RAG, harici veritabanlarından bilgi sağlayarak ve entegre ederek bu bilgi boşluğunu kapatır. Bu durumda, kullanıcının sorgusuyla ilgili haber makalelerini toplar. Bu makaleler, orijinal soruyla birleştirilerek LLM'lerin iyi bilgilendirilmiş bir yanıt üretmesini sağlayan kapsamlı bir prompt (istemi) oluşturur.

RAG araştırma paradigması sürekli gelişmektedir ve biz bunu üç aşamaya ayırıyoruz: Şekil 3'te gösterildiği gibi Naive RAG, Advanced RAG ve Modular RAG.

![Şekil 3: RAG Paradigmaları](images/page4_img1.png)

RAG yöntemleri maliyet etkin olmasına ve yerel (native) LLM'lerin performansını aşmasına rağmen, bazı sınırlamalara da sahiptir. Advanced RAG ve Modular RAG'ın geliştirilmesi, Naive RAG'daki bu spesifik eksikliklere bir yanıttır.

### A. Naive RAG

Naive RAG araştırma paradigması, ChatGPT'nin yaygın olarak benimsenmesinden kısa bir süre sonra popülerlik kazanan en eski metodolojiyi temsil eder. Naive RAG; indeksleme (indexing), retrieval (getirme) ve generation (oluşturma) adımlarını içeren geleneksel süreci takip eder ve bu süreç aynı zamanda bir "Retrieve-Read" (Getir-Oku) çerçevesi olarak da adlandırılır [7].

**Indexing (İndeksleme)**; PDF, HTML, Word ve Markdown gibi çeşitli formatlardaki ham verilerin temizlenmesi ve çıkarılmasıyla başlar ve bunlar daha sonra tek tip bir düz metin formatına dönüştürülür. Dil modellerinin bağlam (context) sınırlamalarına uymak için metinler daha küçük, sindirilebilir chunk (parça)lara bölünür. Chunk'lar daha sonra bir embedding (gömme) modeli kullanılarak vektör temsillerine kodlanır ve bir vektör veritabanında depolanır. Bu adım, sonraki retrieval aşamasında verimli benzerlik aramalarını mümkün kılmak için kritik öneme sahiptir.

**Retrieval (Getirme).** Bir kullanıcı sorgusu alındığında, RAG sistemi sorguyu bir vektör temsiline dönüştürmek için indeksleme aşamasında kullanılan aynı kodlama modelini kullanır. Daha sonra sorgu vektörü ile indekslenmiş külliyat içindeki chunk'ların vektörleri arasındaki benzerlik skorlarını hesaplar. Sistem, sorguya en yüksek benzerliği gösteren ilk K (top K) chunk'a öncelik verir ve bunları getirir. Bu chunk'lar daha sonra prompt içindeki genişletilmiş context (bağlam) olarak kullanılır.

**Generation (Oluşturma).** Sorulan sorgu ve seçilen dokümanlar, bir büyük dil modelinin (LLM) bir yanıt formüle etmekle görevlendirildiği tutarlı bir prompt halinde sentezlenir. Modelin yanıtlama yaklaşımı göreve özgü kriterlere göre değişebilir; bu da onun ya kendi içsel parametrik bilgisinden yararlanmasına ya da yanıtlarını sağlanan dokümanlar içindeki bilgilerle sınırlandırmasına olanak tanır. Devam eden diyaloglar durumunda, mevcut konuşma geçmişi prompt'a entegre edilebilir ve modelin çok turlu diyalog etkileşimlerine etkili bir şekilde girmesini sağlar.

Ancak Naive RAG bazı önemli dezavantajlarla karşılaşmaktadır:

**Retrieval (Getirme) Zorlukları.** Getirme aşaması genellikle kesinlik (precision) ve geri çağırma (recall) konusunda zorluk çeker; bu da yanlış hizalanmış veya ilgisiz chunk'ların seçilmesine ve kritik bilgilerin kaçırılışına yol açar.

**Generation (Oluşturma) Zorlukları.** Yanıtların üretilmesinde model, getirilen context tarafından desteklenmeyen içerikler ürettiği hallucination (halüsinasyon) sorunuyla karşılaşabilir. Bu aşama ayrıca çıktılarda ilgisizlik, toksisite veya yanlılık (bias) sorunlarından muzdarip olabilir ve bu da yanıtların kalitesini ve güvenilirliğini düşürebilir.

**Augmentation (Zenginleştirme) Engelleri.** Getirilen bilgilerin farklı görevlerle entegre edilmesi zorlayıcı olabilir, bazen kopuk veya tutarsız çıktılara neden olabilir. Birden fazla kaynaktan benzer bilgiler getirildiğinde süreçte gereksizlik (redundancy) oluşabilir ve bu da tekrarlayan yanıtlara yol açabilir. Çeşitli pasajların önemini ve alakasını belirlemek, stilistik ve tonlama tutarlılığını sağlamak karmaşıklığı artırır. Karmaşık sorunlarla karşılaşıldığında, orijinal sorguya dayalı tek bir retrieval işlemi yeterli bağlam bilgisini elde etmek için yeterli olmayabilir. Ayrıca, generation modellerinin zenginleştirilmiş bilgilere aşırı güvenerek, içgörülü veya sentezlenmiş bilgi eklemeden sadece getirilen içeriği yankılayan çıktıları üretmesi endişesi vardır.

### B. Advanced RAG

Advanced RAG, Naive RAG'ın sınırlarını aşmak için belirli iyileştirmeler sunar. Retrieval kalitesini artırmaya odaklanarak, retrieval öncesi (pre-retrieval) ve retrieval sonrası (post-retrieval) stratejilerini kullanır. İndeksleme sorunlarını ele almak için Advanced RAG; kayan pencere (sliding window) yaklaşımı, ince taneli (fine-grained) bölümleme ve metadata (meta veri) ekleme yoluyla indeksleme tekniklerini iyileştirir. Ek olarak, retrieval sürecini kolaylaştırmak için çeşitli optimizasyon yöntemlerini entegre eder [8].

**Pre-retrieval (Getirme Öncesi) süreci.** Bu aşamada birincil odak noktası indeksleme yapısını ve orijinal sorguyu optimize etmektir. İndekslemeyi optimize etmenin amacı, indekslenen içeriğin kalitesini artırmaktır. Bu şu stratejileri içerir: veri tanecikliliğini (granularity) artırma, indeks yapılarını optimize etme, metadata ekleme, hizalama optimizasyonu ve karma (mixed) retrieval. Sorgu optimizasyonunun amacı ise kullanıcının orijinal sorusunu retrieval görevi için daha net ve uygun hale getirmektir. Yaygın yöntemler arasında sorgu yeniden yazımı (query rewriting), sorgu dönüştürme (query transformation), sorgu genişletme (query expansion) ve diğer teknikler bulunur [7], [9]–[11].

**Post-Retrieval (Getirme Sonrası) Süreci.** İlgili context getirildikten sonra, bunun sorgu ile etkili bir şekilde entegre edilmesi kritik öneme sahiptir. Retrieval sonrası süreçteki ana yöntemler arasında chunk'ları yeniden sıralama (rerank) ve context sıkıştırma (context compression) bulunur. En alakalı içeriği prompt'un kenarlarına taşımak için getirilen bilgileri yeniden sıralamak kilit bir stratejidir. Bu konsept LlamaIndex, LangChain ve HayStack gibi çerçevelerde uygulanmıştır [12]. Tüm ilgili dokümanları doğrudan LLM'lere beslemek, bilginin aşırı yüklenmesine (information overload) yol açarak kilit detaylara olan odağı ilgisiz içeriklerle dağıtabilir. Bunu hafifletmek için, retrieval sonrası çabalar temel bilgileri seçmeye, kritik bölümleri vurgulamaya ve işlenecek bağlamı kısaltmaya odaklanır.

### C. Modular RAG

Modular RAG mimarisi, önceki iki RAG paradigmasının ötesine geçerek daha gelişmiş uyarlanabilirlik ve çok yönlülük sunar. Benzerlik aramaları için bir arama modülü eklemek ve retriever'ı fine-tuning yoluyla geliştirmek gibi bileşenlerini iyileştirmek için çeşitli stratejiler içerir. Belirli sorunları ele almak için yeniden yapılandırılmış RAG modülleri [13] ve yeniden düzenlenmiş RAG boru hatları (pipelines) [14] gibi yenilikler tanıtılmıştır. Bileşenleri arasında hem ardışık işlemeyi hem de entegre uçtan uca eğitimi destekleyen modüler bir RAG yaklaşımına geçiş yaygınlaşmaktadır. Ayırt ediciliğine rağmen Modular RAG, Advanced ve Naive RAG'ın temel ilkeleri üzerine inşa edilerek RAG ailesi içindeki ilerlemeyi ve gelişimi gösterir.

#### 1) Yeni Modüller

Modular RAG çerçevesi, retrieval ve işleme yeteneklerini geliştirmek için ek uzmanlaşmış bileşenler sunar. **Arara (Search)** modülü, LLM tarafından üretilen kod ve sorgu dillerini kullanarak arama motorları, veritabanları ve bilgi grafları (knowledge graphs) gibi çeşitli veri kaynaklarında doğrudan aramalar yapılmasına olanak tanıyarak belirli senaryolara uyum sağlar [15]. **RAG-Fusion**, kullanıcı sorgularını çeşitli perspektiflere genişleten çoklu sorgu stratejisi kullanarak, hem açık hem de dönüştürücü bilgileri ortaya çıkarmak için paralel vektör aramaları ve akıllı yeniden sıralamadan yararlanarak geleneksel arama sınırlamalarını ele alır [16]. **Bellek (Memory)** modülü, retrieval'ı yönlendirmek için LLM'nin belleğinden yararlanır ve yinelemeli kendi kendine geliştirme (iterative self-enhancement) yoluyla metni veri dağılımıyla daha yakından hizalayan sınırsız bir bellek havuzu oluşturur [17], [18]. RAG sistemindeki **Yönlendirme (Routing)**, özetleme, belirli veritabanı aramaları veya farklı bilgi akışlarını birleştirme gibi işlemler için sorgu için en uygun yolu seçerek çeşitli veri kaynakları arasında gezinir [19]. **Tahmin (Predict)** modülü, context'i doğrudan LLM üzerinden üreterek gereksiz bilgileri ve gürültüyü azaltmayı, alaka ve doğruluğu sağlamayı amaçlar [13]. Son olarak, **Görev Adaptörü (Task Adapter)** modülü, RAG'ı çeşitli aşağı akış görevlerine göre uyarlar, zero-shot (sıfır atışlı) girişler için otomatik prompt getirme ve few-shot (az atışlı) sorgu üretimi yoluyla göreve özgü retriever'lar oluşturur [20], [21].

#### 2) Yeni Kalıplar (Patterns)

Modular RAG, belirli sorunları çözmek için modül ikamesine veya yeniden yapılandırılmasına izin vererek olağanüstü uyumluluk sunar. Bu, basit bir "Getir" ve "Oku" mekanizmasıyla karakterize edilen Naive ve Advanced RAG'ın sabit yapılarının ötesine geçer. Dahası Modular RAG, yeni modülleri entegre ederek veya mevcutlar arasındaki etkileşim akışını ayarlayarak bu esnekliği genişletir ve farklı görevlerde uygulanabilirliğini artırır.

**Rewrite-Retrieve-Read** [7] gibi yenilikler, retrieval sorgularını bir yeniden yazma modülü aracılığıyla iyileştirmek ve yeniden yazma modelini güncellemek için bir LM-feedback mekanizması kullanarak LLM'nin yeteneklerinden yararlanır ve görev performansını artırır. Benzer şekilde, **Generate-Read** [13] gibi yaklaşımlar geleneksel retrieval'ı LLM tarafından üretilen içerikle değiştirirken, **Recite-Read** [22] model ağırlıklarından retrieval yapmaya vurgu yaparak modelin bilgi yoğun görevleri işleme yeteneğini artırır. Hibrit retrieval stratejileri, çeşitli sorgulara hitap etmek için anahtar kelime, anlamsal ve vektör aramalarını birleştirir. Ek olarak, alt sorgular (sub-queries) ve hipotezsel doküman gömmeleri (HyDE) [11] kullanmak, üretilen yanıtlar ile gerçek dokümanlar arasındaki embedding benzerliklerine odaklanarak retrieval alakasını artırmayı hedefler.

Modül düzenlemesi ve etkileşimindeki ayarlamalar; **Demonstrate-Search-Predict (DSP)** [23] çerçevesi ve **ITER-RETGEN**'in [14] yinelemeli **Retrieve-Read-Retrieve-Read** akışı gibi örnekler, bir modülün işlevselliğini güçlendirmek için diğer modül çıktılarını dinamik kullanımını göstererek modül sinerjisinin geliştirilmesine dair sofistike bir anlayışı sergiler. Modular RAG akışının esnek düzenlemesi, **FLARE** [24] ve **Self-RAG** [25] gibi teknikler aracılığıyla adaptif retrieval'ın faydalarını gösterir. Bu yaklaşım, farklı senaryolara dayalı olarak retrieval gerekliliğini değerlendirerek sabit RAG retrieval sürecini aşar. Esnek bir mimarinin bir başka faydası da RAG sisteminin diğer teknolojilerle (fine-tuning veya pekiştirmeli öğrenme gibi) daha kolay entegre olabilmesidir [26].

### D. RAG vs Fine-tuning

LLM'lerin zenginleştirilmesi, artan yaygınlıkları nedeniyle büyük ilgi görmüştür. LLM'ler için optimizasyon yöntemleri arasında RAG, genellikle Fine-tuning (FT) ve prompt engineering (istemi mühendisliği) ile karşılaştırılır. Her yöntemin Şekil 4'te gösterildiği gibi farklı özellikleri vardır.

![Şekil 4: RAG vs Fine-Tuning](images/page7_img1.png)

Üç yöntem arasındaki farkları iki boyutta göstermek için bir kadran grafiği kullandık: harici bilgi gereksinimleri ve model uyarlama gereksinimleri. Prompt engineering, harici bilgi ve model uyarlama için minimum gereksinimle bir modelin içsel yeteneklerinden yararlanır. RAG, bir modele bilgi retrieval'ı için özel olarak hazırlanmış bir ders kitabı sağlamaya benzetilebilir; kesin bilgi retrieval görevleri için idealdir. Buna karşılık FT, bir öğrencinin zaman içinde bilgiyi içselleştirmesine benzer; belirli yapıların, stillerin veya formatların kopyalanmasını gerektiren senaryolar için uygundur.

RAG, gerçek zamanlı bilgi güncellemeleri sunarak ve harici bilgi kaynaklarını yüksek yorumlanabilirlikle etkili bir şekilde kullanarak dinamik ortamlarda üstündür. Ancak, veri getirme ile ilgili daha yüksek gecikme süresi ve etik hususlar ile birlikte gelir. Diğer yandan FT daha statiktir, güncellemeler için yeniden eğitim gerektirir ancak modelin davranışı ve stilinin derinlemesine özelleştirilmesine olanak tanır. Veri kümesi hazırlama ve eğitim için önemli hesaplama kaynakları talep eder ve halüsinasyonları azaltabilse de alışılmadık verilerle zorluklar yaşayabilir.

Çeşitli konulardaki çeşitli bilgi yoğun görevlerdeki performanslarının çoklu değerlendirmelerinde [28], denetimsiz (unsupervised) fine-tuning'in bazı iyileştirmeler gösterse de, RAG'ın hem eğitim sırasında karşılaşılan mevcut bilgiler hem de tamamen yeni bilgiler için tutarlı bir şekilde ondan daha iyi performans gösterdiği ortaya çıkarılmıştır. Ek olarak LLM'lerin denetimsiz fine-tuning yoluyla yeni olgusal bilgileri öğrenmekte zorlandığı bulunmuştur. RAG ve FT arasındaki seçim; uygulama bağlamındaki veri dinamikleri, özelleştirme ve hesaplama yeteneklerine yönelik spesifik ihtiyaçlara bağlıdır. RAG ve FT birbirini dışlayan yöntemler değildir ve birbirlerini tamamlayarak bir modelin yeteneklerini farklı seviyelerde artırabilirler. Bazı durumlarda bunların birleşik kullanımı optimal performansa yol açabilir. RAG ve FT'yi içeren optimizasyon süreci, tatmin edici sonuçlar elde etmek için birden fazla iterasyon gerektirebilir.

---

## III. RETRIEVAL (GETİRME)

RAG bağlamında, ilgili dokümanları veri kaynağından verimli bir şekilde getirmek kritik öneme sahiptir. Retrieval kaynağı, retrieval tanecikliliği, retrieval öncesi işleme ve ilgili embedding modelinin seçimi gibi temel konular söz konusudur.

### A. Retrieval Kaynağı (Retrieval Source)

RAG; LLM'leri geliştirmek için harici bilgilere dayanırken, getirme kaynağının türü ve getirme birimlerinin tanecikliliği nihai üretim sonuçlarını etkiler.

#### 1) Veri Yapısı

Başlangıçta metin, retrieval'ın ana akım kaynağıydı. Daha sonra getirme kaynağı, geliştirme için yarı yapılandırılmış verileri (PDF) ve yapılandırılmış verileri (Knowledge Graph, KG) içerecek şekilde genişledi. Orijinal harici kaynaklardan getirmeye ek olarak, son araştırmalarda getirme ve geliştirme amaçları için LLM'lerin kendileri tarafından üretilen içeriğin kullanılmasına yönelik büyüyen bir eğilim de vardır.

**Yapılandırılmamış Veri (Unstructured Data)**, külliyattan toplanan ve en yaygın kullanılan getirme kaynağı olan metin gibi verilerdir. Açık alan soru-cevap (ODQA) görevleri için birincil getirme kaynakları; HotpotQA (1 Ekim 2017), DPR (20 Aralık 2018) gibi mevcut ana versiyonları içeren Wikipedia dökümleridir. Ansiklopedik verilere ek olarak yaygın yapılandırılmamış veriler arasında diller arası metinler [19] ve alana özgü veriler (tıbbi [67] ve yasal alanlar [29] gibi) bulunur.

**Yarı yapılandırılmış veriler (Semi-structured data)** tipik olarak PDF gibi metin ve tablo bilgilerinin bir kombinasyonunu içeren verilere atıfta bulunur. Yarı yapılandırılmış verilerin işlenmesi, geleneksel RAG sistemleri için iki ana nedenden dolayı zorluk teşkil eder. İlk olarak, metin bölme süreçleri yanlışlıkla tabloları ayırabilir ve retrieval sırasında veri bozulmasına yol açabilir. İkinci olarak, tabloların veriye dahil edilmesi anlamsal benzerlik aramalarını karmaşıklaştırabilir. Yarı yapılandırılmış verilerle uğraşırken bir yaklaşım, TableGPT [85] gibi veritabanları içindeki tablolar üzerinde Text-2-SQL sorguları yürütmek için LLM'lerin kod yeteneklerinden yararlanmayı içerir. Alternatif olarak tablolar, metin tabanlı yöntemler kullanılarak daha fazla analiz için metin formatına dönüştürülebilir [75].

**Yapılandırılmış veriler (Structured data)**, bilgi grafları (KG'ler) [86] gibi tipik olarak doğrulanmış olan ve daha kesin bilgiler sağlayabilen verilerdir. KnowledGPT [15], bilgi bankası (KB) arama sorguları oluşturur ve bilgileri kişiselleştirilmiş bir tabanda saklayarak RAG modelinin bilgi zenginliğini artırır. G-Retriever [84]; Grafik Sinir Ağları (GNN'ler), LLM'ler ve RAG'ı entegre ederek LLM'nin yumuşak istemlemesi (soft prompting) yoluyla grafik anlama ve soru yanıtlama yeteneklerini geliştirir ve hedeflenen grafik retrieval için Prize-Collecting Steiner Tree (PCST) optimizasyon problemini kullanır.

**LLM Tarafından Üretilen İçerik.** RAG'daki harici yardımcı bilgilerin sınırlarını ele alan bazı araştırmalar, LLM'lerin içsel bilgisinden yararlanmaya odaklanmıştır. SKR [58], soruları bilinen veya bilinmeyen olarak sınıflandırarak getirme geliştirmesini seçici olarak uygular. GenRead [13], retriever'ı bir LLM jeneratörü ile değiştirerek, LLM tarafından üretilen context'lerin nedensel dil modellemesinin (causal language modeling) ön eğitim hedefleriyle daha iyi hizalanması nedeniyle genellikle daha doğru yanıtlar içerdiğini bulmuştur. Selfmem [17], retrieval ile güçlendirilmiş bir jeneratörle sınırsız bir bellek havuzu oluşturur ve orijinal soruya ikili problem olarak hizmet eden çıktıları seçmek için bir bellek seçicisi kullanarak üretken modeli kendi kendine geliştirir.

#### 2) Retrieval Tanecikliliği (Retrieval Granularity)

Retrieval kaynağının veri formatının yanındaki bir diğer önemli faktör, getirilen verilerin tanecikliliğidir. Kaba taneli (coarse-grained) retrieval birimleri teorik olarak sorun için daha alakalı bilgiler sağlayabilir ancak aynı zamanda retriever'ın ve aşağı akış görevlerindeki dil modellerinin dikkatini dağıtabilecek gereksiz içerikler de içerebilir [50], [87]. Diğer yandan ince taneli (fine-grained) retrieval birim tanecikliliği, getirme yükünü artırır ve anlamsal bütünlüğü ve gerekli bilgiyi karşılamayı garanti etmez. Çıkarım sırasında uygun retrieval tanecikliliğini seçmek, yoğun (dense) retriever'ların retrieval ve aşağı akış görevi performansını artırmak için basit ve etkili bir strateji olabilir.

Metinlerde retrieval tanecikliliği; Token, Phrase (İfade), Sentence (Cümle), Proposition (Önerme), Chunk, Document (Doküman) arasında inceden kabaya doğru sıralanır. Bunlar arasında DenseX [30], önermelerin getirme birimi olarak kullanılması konseptini önermiştir. Önermeler; metindeki her biri benzersiz bir olgusal segmente karşılık gelen atomik ifadeler olarak tanımlanır ve özlü, bağımsız bir doğal dil formatında sunulur. Bilgi Grafiği (KG) üzerinde retrieval tanecikliliği Entity (Varlık), Triplet (Üçlü) ve alt-Grafik'i (sub-Graph) içerir. Detaylı bilgiler Tablo I'de gösterilmiştir.

### B. İndeksleme Optimizasyonu (Indexing Optimization)

İndeksleme aşamasında dokümanlar işlenecek, bölümlenecek ve bir vektör veritabanında saklanmak üzere Embedding'lere dönüştürülecektir. İndeks yapısının kalitesi, retrieval aşamasında doğru bağlamın elde edilip edilemeyeceğini belirler.

#### 1) Chunking Stratejisi

En yaygın yöntem, dokümanı sabit bir token sayısına (örneğin 100, 256, 512) göre chunk'lara bölmektir [88]. Daha büyük chunk'lar daha fazla bağlam yakalayabilir ancak aynı zamanda daha fazla gürültü üretirler, bu da daha uzun işlem süresi ve daha yüksek maliyet gerektirir. Küçük chunk'lar gerekli bağlamı tam olarak aktaramasa da daha az gürültüye sahiptirler. Ancak chunk'lar cümleler içinde kesintilere yol açarak yinelemeli bölünmelerin (recursive splits) ve kayan pencere (sliding window) yöntemlerinin optimizasyonunu tetiklemiş, birden fazla getirme süreci boyunca küresel olarak ilgili bilgileri birleştirerek katmanlı retrieval'ı mümkün kılmıştır [89]. Yine de bu yaklaşımlar anlamsal tamlık ve bağlam uzunluğu arasında bir denge kuramamaktadır. Bu nedenle, cümlelerin (küçük) getirme birimi olarak kullanıldığı ve önceki ile sonraki cümlelerin (büyük) bağlam olarak LLM'lere sağlandığı Small2Big gibi yöntemler önerilmiştir [90].

#### 2) Metadata Eklentileri

Chunk'lar; sayfa numarası, dosya adı, yazar, kategori zaman damgası gibi metadata bilgileriyle zenginleştirilebilir. Daha sonra retrieval bu metadata'ya göre filtrelenebilir ve getirme kapsamı sınırlandırılabilir. Retrieval sırasında doküman zaman damgalarına farklı ağırlıklar atamak, zaman farkındalıklı (time-aware) RAG gerçekleştirebilir; bu da bilginin güncelliğini sağlar ve güncelliğini yitirmiş bilgilerden kaçınır.

Orijinal dokümanlardan metadata çıkarmanın yanı sıra, metadata yapay olarak da oluşturulabilir. Örneğin, paragraf özetleri eklemek ve hipotezsel sorular (hypothetical questions) tanıtmak gibi. Bu yöntem Reverse HyDE olarak da bilinir. Spesifik olarak, doküman tarafından yanıtlanabilecek sorular üretmek için LLM kullanılır; ardından soru ile yanıt arasındaki anlamsal boşluğu azaltmak için retrieval sırasında orijinal soru ile hipotezsel soru arasındaki benzerlik hesaplanır.

#### 3) Yapısal İndeks (Structural Index)

Bilgi retrieval'ı geliştirmenin etkili bir yolu dokümanlar için hiyerarşik bir yapı oluşturmaktır. Yapı inşa ederek RAG sistemi, ilgili verilerin getirilmesini ve işlenmesini hızlandırabilir.

**Hiyerarşik indeks yapısı.** Dosyalar, ebeveyn-çocuk ilişkileri içinde düzenlenir ve chunk'lar bunlara bağlanır. Her düğümde veri özetleri saklanır, bu da veriler arasında hızlı geçişe yardımcı olur ve RAG sisteminin hangi chunk'ların çıkarılacağını belirlemesine asistanlık eder.

**Bilgi Grafiği (Knowledge Graph) indeksi.** Dokümanların hiyerarşik yapısını oluştururken KG kullanmak tutarlılığın korunmasına katkıda bulunur. Farklı konseptler ve varlıklar arasındaki bağlantıları tanımlayarak yanılsama potansiyelini belirgin şekilde azaltır. KGP [91], KG kullanarak birden fazla doküman arasında bir indeks oluşturma yöntemi önermiştir. Bu KG; düğümler (dokümanlardaki paragrafları veya sayfalar ve tablolar gibi yapıları temsil eder) ve kenarlardan (paragraflar arasındaki anlamsal/sözcüksel benzerliği veya doküman yapısı içindeki ilişkileri gösterir) oluşur.

### C. Sorgu Optimizasyonu (Query Optimization)

Naive RAG ile ilgili temel zorluklardan biri, retrieval temeli olarak doğrudan kullanıcının orijinal sorgusuna dayanmasıdır. Kesin ve net bir soru formüle etmek zordur ve özensiz sorgular yetersiz getirme etkinliğiyle sonuçlanır.

#### 1) Sorgu Genişletme (Query Expansion)

Tek bir sorguyu birden fazla sorguya genişletmek sorgunun içeriğini zenginleştirir; herhangi bir spesifik nüans eksikliğini gidermek için ek bağlam sağlar ve böylece üretilen yanıtların optimal alakasını garanti eder.

**Multi-Query (Çoklu Sorgu).** LLM'ler aracılığıyla sorguları genişletmek için prompt engineering kullanarak bu sorgular paralel olarak yürütülebilir.

**Sub-Query (Alt Sorgu).** Alt soru planlama süreci, birleştirildiğinde orijinal soruyu bağlamsallaştırmak ve tam olarak yanıtlamak için gerekli alt soruların üretilmesini temsil eder. Karmaşık bir soru, "least-to-most prompting" yöntemi kullanılarak bir dizi daha basit alt soruya ayrıştırılabilir [92].

**Chain-of-Verification (CoVe - Doğrulama Zinciri).** Genişletilmiş sorgular, halüsinasyonları azaltma etkisine ulaşmak için LLM tarafından doğrulamadan geçer. Doğrulanmış genişletilmiş sorgular tipik olarak daha yüksek güvenilirlik sergiler [93].

#### 2) Sorgu Dönüştürme (Query Transformation)

Temel konsept, kullanıcının orijinal sorgusu yerine dönüştürülmüş bir sorguya dayalı olarak chunk'ları getirmektir.

**Sorgu Yeniden Yazımı (Query Rewrite).** Orijinal sorgular, özellikle gerçek dünya senaryolarında LLM retrieval için her zaman optimal değildir. Bu nedenle, LLM'yi sorguları yeniden yazması için istemleyebiliriz. Sorgu yeniden yazımı için LLM kullanmanın yanı sıra, RRR (Rewrite-retrieve-read) [7] gibi daha küçük özel dil modelleri de kullanılabilir. Taobao'da BEQUE [9] adıyla bilinen sorgu yeniden yazma yönteminin uygulanması, "long-tail" (uzun kuyruklu) sorgular için geri çağırma (recall) etkinliğini belirgin şekilde artırmayı başarmıştır.

**HyDE** [11], hipotezsel dokümanlar (orijinal sorguya verilen varsayılan yanıtlar) inşa eder. Sorun veya sorgu için embedding benzerliği aramak yerine, yanıttan yanıta embedding benzerliğine odaklanır.

**Step-back Prompting** [10], orijinal sorguyu yüksek seviyeli bir konsept sorusu (geriye dönük soru - step-back question) oluşturmak için soyutlaştırır. RAG sisteminde hem geriye dönük soru hem de orijinal sorgu retrieval için kullanılır.

#### 3) Sorgu Yönlendirme (Query Routing)

Değişen sorgulara bağlı olarak farklı RAG boru hatlarına yönlendirme yapmak, çeşitli senaryolara uyum sağlamak üzere tasarlanmış çok yönlü bir RAG sistemi için uygundur.

**Metadata Yönlendiricisi/Filtresi.** İlk adım sorgudan anahtar kelimelerin (varlık) çıkarılmasını, ardından arama kapsamını daraltmak için chunk'lar içindeki anahtar kelimelere ve metadata'ya göre filtreleme yapılmasını içerir.

**Semantik Yönlendirici (Semantic Router)**, sorgunun anlamsal bilgisinden yararlanmayı içeren bir diğer yönlendirme yöntemidir.

### D. Embedding (Gömme)

RAG'da retrieval, soru ile doküman chunk'larının embedding'leri arasındaki benzerliğin (örneğin kosinüs benzerliği) hesaplanmasıyla sağlanır; burada embedding modellerinin anlamsal temsil yeteneği kilit rol oynar. Bu modeller esas olarak seyreltik (sparse) bir kodlayıcı (BM25) ve yoğun (dense) bir retriever (BERT mimarili ön eğitimli dil modelleri) içerir. Son araştırmalar AngIE, Voyage, BGE gibi önde gelen embedding modellerini tanıtmıştır [94]–[96].

#### 1) Karma/Hibrit Retrieval (Mix/Hybrid Retrieval)

Seyreltik ve yoğun embedding yaklaşımları farklı alaka özelliklerini yakalar ve tamamlayıcı alaka bilgilerinden yararlanarak birbirlerinden fayda sağlayabilirler. Seyreltik getirme modelleri, yoğun getirme modellerinin zero-shot yeteneğini geliştirebilir ve yoğun retriever'ların nadir varlıklar içeren sorguları işlemesine yardımcı olarak sağlamlığı (robustness) artırabilir.

#### 2) Embedding Modelini Fine-tuning Yapmak

Bağlamın ön eğitim külliyatından önemli ölçüde saptığı durumlarda (özellikle sağlık hizmetleri, hukuk uygulamaları gibi yüksek derecede uzmanlaşmış disiplinlerde), embedding modelini kendi alan veri kümeniz üzerinde fine-tuning yapmak temel hale gelir. Fine-tuning'in bir diğer amacı da retriever ile generator'ı (jeneratörü) hizalamaktır. PROMPTAGATOR [21], göreve özgü retriever'lar oluşturmak için LLM'yi az atışlı (few-shot) bir sorgu jeneratörü olarak kullanır. LLM-Embedder [97], birden fazla aşağı akış görevi genelinde ödül sinyalleri üretmek için LLM'lerden faydalanır. REPLUG [72], getirilen dokümanların olasılık dağılımlarını hesaplamak için bir retriever ve bir LLM kullanır ve ardından KL ıraksamasını (divergence) hesaplayarak denetimli eğitim gerçekleştirir.

### E. Adaptör (Adapter)

Modelleri fine-tuning yapmak, işlevselliği bir API üzerinden entegre etmek veya sınırlı yerel hesaplama kaynaklarından kaynaklanan kısıtlamaları ele almak gibi zorluklar sunabilir. Sonuç olarak, bazı yaklaşımlar hizalamaya yardımcı olması için bir harici adaptör dahil etmeyi tercih eder.

UPRISE [20], önceden oluşturulmuş bir prompt havuzundan otomatik olarak istemleri getirebilen hafif bir prompt retriever eğitmiştir. AAR (Augmentation-Adapted Retriever) [47], birden fazla aşağı akış görevine uyum sağlamak için tasarlanmış evrensel bir adaptör sunar. PRCA [69], takılabilir ödül odaklı bir bağlamsal adaptör ekler. BGM [26], retriever ve LLM'yi sabit tutar ve aralarında bir köprü Seq2Seq modeli eğitir. PKG, direktif fine-tuning yoluyla bilgiyi "beyaz kutu" (white-box) modellere entegre etmek için yenilikçi bir yöntem tanıtmaktadır [75].

---

## IV. GENERATION (OLUŞTURMA)

Retrieval işleminden sonra, getirilen tüm bilgileri doğrudan yanıt vermesi için LLM'ye girdi olarak vermek iyi bir uygulama değildir. Aşağıda iki perspektiften yapılan ayarlamalar tanıtılacaktır: getirilen içeriği ayarlamak ve LLM'yi ayarlamak.

### A. İçerik Kürasyonu (Context Curation)

Gereksiz (redundant) bilgiler LLM'nin nihai üretim sürecine müdahale edebilir ve aşırı uzun bağlamlar LLM'yi "ortada kaybolma" (Lost in the middle) problemine sürükleyebilir [98]. İnsanlar gibi LLM de uzun metinlerin başına ve sonuna odaklanma eğilimindeyken orta kısmı unutmaya meyillidir.

#### 1) Yeniden Sıralama (Reranking)

Reranking, en alakalı sonuçları ilk sırada vurgulamak için doküman chunk'larını temelden yeniden düzenler; bu da genel doküman havuzunu etkili bir şekilde azaltarak bilgi retrieval'ında hem geliştirici hem de filtre görevi görerek ikili bir amaca hizmet eder. Reranking; Çeşitlilik (Diversity), Alaka (Relevance) ve MRR gibi önceden tanımlanmış metriklere dayanan kural tabanlı yöntemler kullanılarak veya BERT serisinden Encoder-Decoder modelleri (örneğin SpanBERT), Cohere rerank veya bge-reranker-large gibi uzmanlaşmış reranking modelleri ve GPT gibi genel büyük dil modelleri kullanılarak gerçekleştirilebilir [12], [99].

#### 2) Bağlam Seçimi/Sıkıştırma (Context Selection/Compression)

RAG sürecindeki yaygın bir yanlış anlama, mümkün olduğunca çok ilgili doküman getirip bunları uzun bir getirme prompt'u oluşturacak şekilde birleştirmenin faydalı olduğu inancıdır. Ancak aşırı bağlam daha fazla gürültü getirebilir ve LLM'nin temel bilgileri algılamasını azaltabilir.

(Long) LLMLingua [100], [101], önemsiz token'ları tespit etmek ve kaldırmak için GPT-2 Small veya LLaMA-7B gibi küçük dil modellerini (SLM'ler) kullanır; bunları insanlar için anlaşılması zor ancak LLM'ler tarafından iyi anlaşılan bir forma dönüştürür. PRCA, bir bilgi çıkarıcı (information extractor) eğiterek bu sorunu ele almıştır [69]. RECOMP, kontrastlı öğrenme (contrastive learning) kullanarak bir bilgi yoğunlaştırıcı (information condenser) eğiterek benzer bir yaklaşım benimser [71].

Ma ve arkadaşları [103], LLM'lerin ve SLM'lerin güçlü yönlerini birleştiren "Filter-Reranker" paradigmasını önermektedir. Bu paradigmada SLM'ler filtre görevi görürken, LLM'ler yeniden sıralama ajanları olarak işlev görür. Chatlaw'da [104], referans verilen yasal hükümlerin alakasını değerlendirmek için LLM'den kendi kendine öneride (self-suggestion) bulunması istenir.

### B. LLM Fine-tuning

LLM'ler üzerinde senaryo ve veri özelliklerine göre hedeflenen fine-tuning işlemleri daha iyi sonuçlar verebilir. LLM'ler belirli bir alandaki verilerden yoksun olduğunda, fine-tuning yoluyla LLM'ye ek bilgi sağlanabilir.

Fine-tuning'in bir başka faydası da modelin girdi ve çıktısını ayarlama yeteneğidir. Örneğin, LLM'nin belirli veri formatlarına uyum sağlamasını mümkün kılabilir. Yapılandırılmış verilerle etkileşime giren retrieval görevleri için SANTA çerçevesi [76] üçlü bir eğitim rejimi uygular.

Pekiştirmeli öğrenme (reinforcement learning) yoluyla LLM çıktılarını insan veya retriever tercihleriyle hizalamak potansiyel bir yaklaşımdır. RA-DIT [27] gibi tipik bir yaklaşım, KL ıraksamasını kullanarak Retriever ile Generator arasındaki puanlama fonksiyonlarını hizalar.

---

## V. RAG'DA ZENGİNLEŞTİRME SÜRECİ (AUGMENTATION PROCESS)

RAG alanında, standart uygulama genellikle tek bir getirme adımını takip eden üretimden oluşur; bu da verimsizliklere yol açabilir ve genellikle çok adımlı akıl yürütme gerektiren karmaşık sorunlar için yetersizdir [105]. Birçok çalışma bu soruna yanıt olarak getirme sürecini optimize etmiştir ve biz bunları Şekil 5'te özetledik.

![Şekil 5: RAG'da Zenginleştirme Süreci](images/page11_img1.png)


### A. Yinelemeli Getirme (Iterative Retrieval)

Yinelemeli getirme, bilgi tabanının başlangıç sorgusuna ve şimdiye kadar üretilen metne dayalı olarak tekrar tekrar arandığı, LLM'ler için daha kapsamlı bir bilgi tabanı sağlayan bir süreçtir. Bu yaklaşımın, çoklu getirme iterasyonları yoluyla ek bağlamsal referanslar sunarak sonraki yanıt üretiminin sağlamlığını artırdığı gösterilmiştir. Ancak anlamsal süreksizlikten ve ilgisiz bilgilerin birikmesinden etkilenebilir. ITER-RETGEN [14], belirli bilgilerin yeniden üretilmesini gerektiren görevler için "retrieval-enhanced generation" (getirme ile güçlendirilmiş üretim) ile birlikte "generation-enhanced retrieval" (üretim ile güçlendirilmiş getirme) yöntemlerini kullanan sinerjik bir yaklaşım benimser.

### B. Yinelemeli/Özyinelemeli Getirme (Recursive Retrieval)

Recursive (özyinelemeli) getirme, arama sonuçlarının derinliğini ve alakasını artırmak için bilgi retrieval'ı ve doğal dil işlemede (NLP) sıklıkla kullanılır. Süreç, önceki aramalardan elde edilen sonuçlara dayanarak arama sorgularının yinelemeli olarak iyileştirilmesini içerir. IRCoT [61], getirme sürecine rehberlik etmek için düşünce zincirini (chain-of-thought, CoT) kullanır ve elde edilen getirme sonuçlarıyla CoT'yi iyileştirir. ToC [57], sorgudaki belirsiz kısımları sistematik olarak optimize eden bir açıklama ağacı (clarification tree) oluşturur.

Belirli veri senaryolarını ele almak için recursive getirme ve multi-hop (çok adımlı) getirme teknikleri birlikte kullanılır. Recursive getirme; verileri hiyerarşik bir şekilde işlemek ve getirmek için yapılandırılmış bir indeks içerir. Buna karşılık multi-hop getirme, grafik yapılı veri kaynaklarının derinliklerine inerek birbiriyle bağlantılı bilgileri çıkarmak üzere tasarlanmıştır [106].

### C. Adaptif Getirme (Adaptive Retrieval)

Flare [24] ve Self-RAG [25] tarafından örneklendirilen adaptif getirme yöntemleri, LLM'lerin getirme için en uygun anları ve içeriği aktif olarak belirlemesine olanak tanıyarak RAG çerçevesini iyileştirir; böylece kaynaklanan bilginin verimliliğini ve alakasını artırır.

**WebGPT** [110], metin üretimi sırasında otonom olarak bir arama motoru kullanması için GPT-3 modelini eğitmek üzere bir pekiştirmeli öğrenme çerçevesini entegre eder. **Flare**, üretilen terimlerin olasılığı ile gösterilen üretim sürecinin güvenini izleyerek zamanlamalı getirmeyi otomatiğe bağlar [24]. Olasılık belirli bir eşiğin altına düştüğünde getirme sistemini etkinleştirir. **Self-RAG** [25], modelin çıktılarını iç gözlemle (introspection) değerlendirmesine olanak tanıyan "yansıma token'ları" (reflection tokens) tanıtır. Bu token'lar iki çeşittir: "retrieve" (getir) ve "critic" (eleştir). Model, getirmeyi ne zaman etkinleştireceğine otonom olarak karar verir veya alternatif olarak önceden tanımlanmış bir eşik süreci tetikleyebilir.

---

## VI. GÖREV VE DEĞERLENDİRME (TASK AND EVALUATION)

NLP alanında RAG'ın hızlı ilerlemesi ve artan şekilde benimsenmesi, RAG modellerinin değerlendirilmesini LLM topluluğundaki araştırmaların ön saflarına taşımıştır.

### A. Aşağı Akış Görevi (Downstream Task)

RAG'ın temel görevi, geleneksel tek adımlı (single-hop)/çok adımlı (multi-hop) QA, çoktan seçmeli, alana özgü QA ve RAG için uygun uzun formdaki senaryolar dahil olmak üzere Soru Cevaplama (Question Answering - QA) olmaya devam etmektedir. QA'ya ek olarak RAG; Bilgi Çıkarımı (Information Extraction - IE), diyalog üretimi, kod araması vb. gibi çoklu aşağı akış görevlerine sürekli olarak genişletilmektedir. RAG'ın ana aşağı akış görevleri ve bunlara karşılık gelen veri kümeleri Tablo II'de özetlenmiştir.

### B. Değerlendirme Hedefi (Evaluation Target)

Tarihsel olarak RAG modelleri değerlendirmeleri, belirli aşağı akış görevlerindeki yürütmelerine odaklanmıştır. Bu değerlendirmeler, eldeki görevlere uygun yerleşik metrikleri kullanır.

**Retrieval Kalitesi (Retrieval Quality).** Getirme kalitesini değerlendirmek, retriever bileşeni tarafından sağlanan bağlamın etkinliğini belirlemek için kritik öneme sahiptir. Hit Rate, MRR ve NDCG gibi metrikler yaygın olarak kullanılmaktadır [161], [162].

**Generation Kalitesi (Generation Quality).** Üretim kalitesinin değerlendirilmesi, jeneratörün getirilen bağlamdan tutarlı ve alakalı yanıtlar sentezleme kapasitesine odaklanır. Etiketlenmemiş (unlabeled) içerik için değerlendirme; üretilen yanıtların faithfulness (sadakat), alaka düzeyi ve zararsızlığını kapsar [161].

### C. Değerlendirme Yönleri (Evaluation Aspects)

RAG modellerinin modern değerlendirme uygulamaları üç ana kalite puanını ve dört temel yeteneği vurgular.

#### 1) Kalite Puanları (Quality Scores)

- **Bağlam Alakası (Context Relevance)**, getirilen bağlamın kesinliğini ve özgüllüğünü değerlendirerek alaka düzeyini sağlar ve gereksiz içerikle ilişkili işlem maliyetlerini minimize eder.
- **Yanıt Sadakati (Answer Faithfulness)**, üretilen yanıtların getirilen bağlama sadık kalmasını sağlar, tutarlılığı korur ve çelişkilerden kaçınır.
- **Yanıt Alakası (Answer Relevance)**, üretilen yanıtların sorulan sorularla doğrudan ilgili olmasını gerektirir.

#### 2) Gerekli Yetenekler (Required Abilities)

- **Gürültü Sağlamlığı (Noise Robustness)**, modelin soruyla ilgili olan ancak içerikli bilgi barındırmayan gürültülü dokümanları yönetme yeteneğini değerlendirir.
- **Olumsuz Reddetme (Negative Rejection)**, getirilen dokümanlar gerekli bilgiyi içermediğinde modelin yanıt vermekten kaçınma konusundaki ayırt etme yeteneğini değerlendirir.
- **Bilgi Entegrasyonu (Information Integration)**, modelin karmaşık soruları yanıtlamak için birden fazla dokümandan bilgiyi sentezleme konusundaki uzmanlığını değerlendirir.
- **Karşıolgusal Sağlamlık (Counterfactual Robustness)**, modelin dokümanlar içindeki bilinen yanlışlıkları tanıma ve göz ardı etme yeteneğini test eder.

### D. Değerlendirme Benchmark'ları ve Araçları

RAG'ın değerlendirilmesini kolaylaştırmak için bir dizi benchmark testi ve aracı önerilmiştir. RGB, RECALL ve CRUD [167]–[169] gibi öne çıkan benchmark'lar, RAG modellerinin temel yeteneklerini değerlendirmeye odaklanır. Aynı zamanda RAGAS [164], ARES [165] ve TruLens gibi en son teknoloji otomatik araçlar kalite puanlarını belirlemek için LLM'leri kullanır. Bu araçlar ve benchmark'lar, Tablo IV'te özetlendiği gibi RAG modellerinin sistematik değerlendirmesi için sağlam bir çerçeve oluşturur.

---

## VII. TARTIŞMA VE GELECEK PERSPEKTİFLERİ

RAG teknolojisindeki önemli ilerlemelere rağmen, derinlemesine araştırma gerektiren birkaç zorluk devam etmektedir.

### A. RAG vs Uzun Bağlam (Long Context)

İlgili araştırmaların derinleşmesiyle birlikte LLM'lerin bağlam penceresi sürekli genişlemektedir [170]–[172]. Günümüzde LLM'ler 200.000 token'ı aşan bağlamları zahmetsizce yönetebilmektedir. Bu yetenek, daha önce RAG'a bağımlı olan uzun doküman soru-cevaplamanın artık tüm dokümanı doğrudan prompt'a dahil edebileceği anlamına gelir. Nitekim RAG hala yeri doldurulamaz bir rol oynamaktadır. Bir yandan, LLM'lere tek seferde çok miktarda bağlam sağlamak çıkarım hızını önemli ölçüde etkileyecekken; chunk'larla getirme ve talep üzerine girdi sağlama operasyonel verimliliği önemli ölçüde artırabilir. Diğer yandan, RAG tabanlı üretim, kullanıcıların üretilen yanıtları doğrulamasına yardımcı olmak için LLM'ler için orijinal referansları hızla konumlandırabilir. Süper uzun bağlamlar bağlamında yeni RAG yöntemleri geliştirmek, gelecekteki araştırma trendlerinden biridir.

### B. RAG Sağlamlığı (Robustness)

Retrieval sırasında gürültü veya çelişkili bilgilerin varlığı, RAG'ın çıktı kalitesini olumsuz etkileyebilir. Bu durum mecazi olarak "Yanlış bilgi, hiç bilgi olmamasından daha kötü olabilir" şeklinde ifade edilir. RAG'ın bu tür düşmanca (adversarial) veya karşıolgusal girdilere karşı direncini artırmak araştırma ivmesi kazanmaktadır [48], [50], [82]. Cuconasu ve arkadaşları [54], hangi tür dokümanların getirilmesi gerektiğini analiz etmiş ve araştırma bulguları, ilgisiz dokümanların dahil edilmesinin, kalite düşüşü varsayımının aksine doğruluğu beklenmedik bir şekilde %30'dan fazla artırabileceğini ortaya koymuştur.

### C. Hibrit Yaklaşımlar

RAG'ı fine-tuning ile birleştirmek önde gelen bir strateji olarak ortaya çıkmaktadır. RAG ve fine-tuning'in optimal entegrasyonunu belirlemek — ardışık mı, dönüşümlü mü yoksa uçtan uca ortak eğitim yoluyla mı — ve hem parametreleştirilmiş hem de parametreleştirilmemiş avantajlardan nasıl yararlanılacağı keşfedilmeye değer alanlardır [27]. Bir başka eğilim de RAG'a belirli işlevlere sahip SLM'lerin (küçük dil modelleri) dahil edilmesidir. Örneğin CRAG [67], bir sorgu için getirilen dokümanların genel kalitesini değerlendirmek üzere hafif bir retrieval değerlendiricisi eğitir.

### D. RAG'ın Ölçekleme Yasaları (Scaling Laws)

Uçtan uca RAG modelleri ve RAG tabanlı ön eğitimli modeller hala güncel araştırmacıların odak noktalarından biridir [173]. LLM'ler için ölçekleme yasaları [174] belirlenmiş olsa da, bunların RAG'a uygulanabilirliği belirsizliğini korumaktadır. RETRO++ [44] gibi ilk çalışmalar bunu ele almaya başlamış olsa da, RAG modellerindeki parametre sayısı hala LLM'lerin gerisinde kalmaktadır. Daha küçük modellerin daha büyük olanlardan daha iyi performans gösterdiği bir Ters Ölçekleme Yasası (Inverse Scaling Law) olasılığı özellikle ilgi çekicidir.

### E. Üretime Hazır RAG (Production-Ready RAG)

RAG'ın pratikliği ve mühendislik gereksinimleriyle hizalanması, benimsenmesini kolaylaştırmıştır. Ancak retrieval verimliliğinin artırılması, büyük bilgi tabanlarında doküman geri çağırmanın (recall) iyileştirilmesi ve veri güvenliğinin sağlanması ele alınması gereken kritik mühendislik zorlukları olmaya devam etmektedir [175].

RAG ekosisteminin gelişimi, teknik yığınının (stack) ilerlemesinden büyük ölçüde etkilenmektedir. LangChain ve LlamaIndex gibi temel araçlar ChatGPT'nin ortaya çıkışıyla hızla popülerlik kazanmıştır. Gelişmekte olan teknoloji yığını; Flowise AI (düşük kodlu yaklaşım), HayStack, Meltano ve Cohere Coral gibi özel ürünleri içerir. Geleneksel yazılım ve bulut hizmet sağlayıcıları da tekliflerini RAG odaklı hizmetleri içerecek şekilde genişletmektedir.

### F. Çok Modüllü RAG (Multi-modal RAG)

RAG, başlangıçtaki metin tabanlı soru-cevaplama sınırlarını aşarak çeşitli modal veri dizilerini benimsemiştir. Bu genişleme, RAG konseptlerini çeşitli alanlarda entegre eden yenilikçi multimodal modellerin doğuşuna yol açmıştır:

**Görüntü (Image).** RA-CM3 [176], hem metin hem de görüntü getirme ve üretme konusunda öncü bir multimodal model olarak durmaktadır. BLIP-2 [177], verimli görsel dil ön eğitimi için LLM'lerle birlikte dondurulmuş (frozen) görüntü kodlayıcılarını kullanır.

**Ses ve Video.** GSS yöntemi, makine tarafından çevrilmiş verileri konuşma çevirisi verilerine dönüştürmek için ses kliplerini getirir ve birbirine ekler [179]. Vid2Seq, dil modellerini uzmanlaşmış zamansal işaretleyicilerle zenginleştirir [181].

**Kod.** RBPS [182], geliştiricilerin hedefleriyle uyumlu kod örneklerini getirerek küçük ölçekli öğrenme görevlerinde üstünlük sağlar. CoK yöntemi [106] önce bir bilgi grafiğinden girdi sorgusuyla ilgili olguları çıkarır.

---

## VIII. SONUÇ

Şekil 6'da betimlendiği gibi bu makalenin özeti, dil modellerinden elde edilen parametreleştirilmiş bilgiyi harici bilgi tabanlarından gelen kapsamlı parametreleştirilmemiş verilerle entegre ederek RAG'ın LLM yeteneklerini geliştirmedeki önemli ilerlemesini vurgulamaktadır.

![Şekil 6: RAG Özeti ve Ekosistemi](images/page16_img1.png)

İnceleme, RAG teknolojilerinin evrimini ve birçok farklı görevdeki uygulamasını sergilemektedir. Analiz, RAG çerçevesi içindeki üç gelişimsel paradigmanın ana hatlarını çizmektedir: Naive, Advanced ve Modular RAG; her biri selefine göre aşamalı bir iyileştirmeyi temsil eder. RAG'ın fine-tuning ve pekiştirmeli öğrenme gibi diğer AI metodolojileriyle teknik entegrasyonu, yeteneklerini daha da genişletmiştir. RAG teknolojisindeki ilerlemeye rağmen, sağlamlığını ve uzun bağlamları yönetme yeteneğini geliştirmek için araştırma fırsatları bulunmaktadır. RAG'ın uygulama kapsamı multimodal alanlara doğru genişlemekte, görüntü, video ve kod gibi çeşitli veri formlarını yorumlamak ve işlemek için prensiplerini uyarlamaktadır.

RAG'ın büyüyen ekosistemi, RAG odaklı AI uygulamalarındaki artış ve destekleyici araçların sürekli gelişimi ile kanıtlanmaktadır. RAG ekosisteminin gelişimi, teknik yığınının (stack) ilerlemesinden büyük ölçüde etkilenmektedir. LangChain ve LlamaIndex gibi temel araçlar ChatGPT'nin ortaya çıkışıyla hızla popülerlik kazanmıştır. Gelişmekte olan teknoloji yığını; Flowise AI (düşük kodlu yaklaşım), HayStack, Meltano ve Cohere Coral gibi özel ürünleri içerir. Geleneksel yazılım ve bulut hizmet sağlayıcıları da tekliflerini RAG odaklı hizmetleri içerecek şekilde genişletmektedir.

RAG'ın uygulama manzarası genişledikçe, evrimine ayak uydurmak için değerlendirme metodolojilerini iyileştirme ihtiyacı vardır. Doğru ve temsilci performans değerlendirmelerinin sağlanması, RAG'ın AI araştırma ve geliştirme topluluğuna katkılarını tam olarak yakalamak için çok önemlidir.

---

## KAYNAKÇA (REFERENCES)

[1] N. Kandpal, H. Deng, A. Roberts, E. Wallace, and C. Raffel, “Large language models struggle to learn long-tail knowledge,” in Interna- tional Conference on Machine Learning. PMLR, 2023, pp. 15 696– 15 707.
[2] Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen et al., “Siren’s song in the ai ocean: A survey on hal- lucination in large language models,” arXiv preprint arXiv:2309.01219, 2023.
[3] D. Arora, A. Kini, S. R. Chowdhury, N. Natarajan, G. Sinha, and A. Sharma, “Gar-meets-rag paradigm for zero-shot information re- trieval,” arXiv preprint arXiv:2310.20158, 2023.
[4] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. K¨uttler, M. Lewis, W.-t. Yih, T. Rockt¨aschel et al., “Retrieval- augmented generation for knowledge-intensive nlp tasks,” Advances in Neural Information Processing Systems, vol. 33, pp. 9459–9474, 2020.
[5] S. Borgeaud, A. Mensch, J. Hoffmann, T. Cai, E. Rutherford, K. Milli- can, G. B. Van Den Driessche, J.-B. Lespiau, B. Damoc, A. Clark et al., “Improving language models by retrieving from trillions of tokens,” in International conference on machine learning. PMLR, 2022, pp. 2206–2240.
[6] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray et al., “Training language models to follow instructions with human feedback,” Advances in neural information processing systems, vol. 35, pp. 27 730–27 744, 2022.
[7] X. Ma, Y. Gong, P. He, H. Zhao, and N. Duan, “Query rewrit- ing for retrieval-augmented large language models,” arXiv preprint arXiv:2305.14283, 2023.
[8] I. ILIN, “Advanced rag techniques: an il- lustrated overview,” https://pub.towardsai.net/ advanced-rag-techniques-an-illustrated-overview-04d193d8fec6, 2023.
[9] W. Peng, G. Li, Y. Jiang, Z. Wang, D. Ou, X. Zeng, E. Chen et al., “Large language model based long-tail query rewriting in taobao search,” arXiv preprint arXiv:2311.03758, 2023.
[10] H. S. Zheng, S. Mishra, X. Chen, H.-T. Cheng, E. H. Chi, Q. V. Le, and D. Zhou, “Take a step back: Evoking reasoning via abstraction in large language models,” arXiv preprint arXiv:2310.06117, 2023.
[11] L. Gao, X. Ma, J. Lin, and J. Callan, “Precise zero-shot dense retrieval without relevance labels,” arXiv preprint arXiv:2212.10496, 2022.
[12] V. Blagojevi, “Enhancing rag pipelines in haystack: Introducing diver- sityranker and lostinthemiddleranker,” https://towardsdatascience.com/ enhancing-rag-pipelines-in-haystack-45f14e2bc9f5, 2023.
[13] W. Yu, D. Iter, S. Wang, Y. Xu, M. Ju, S. Sanyal, C. Zhu, M. Zeng, and M. Jiang, “Generate rather than retrieve: Large language models are strong context generators,” arXiv preprint arXiv:2209.10063, 2022.
[14] Z. Shao, Y. Gong, Y. Shen, M. Huang, N. Duan, and W. Chen, “Enhancing retrieval-augmented large language models with iterative retrieval-generation synergy,” arXiv preprint arXiv:2305.15294, 2023.
[15] X. Wang, Q. Yang, Y. Qiu, J. Liang, Q. He, Z. Gu, Y. Xiao, and W. Wang, “Knowledgpt: Enhancing large language models with retrieval and storage access on knowledge bases,” arXiv preprint arXiv:2308.11761, 2023.
[16] A. H. Raudaschl, “Forget rag, the future is rag-fusion,” https://towardsdatascience.com/ forget-rag-the-future-is-rag-fusion-1147298d8ad1, 2023.
[17] X. Cheng, D. Luo, X. Chen, L. Liu, D. Zhao, and R. Yan, “Lift yourself up: Retrieval-augmented text generation with self memory,” arXiv preprint arXiv:2305.02437, 2023.
[18] S. Wang, Y. Xu, Y. Fang, Y. Liu, S. Sun, R. Xu, C. Zhu, and M. Zeng, “Training data is more valuable than you think: A simple and effective method by retrieving from training data,” arXiv preprint arXiv:2203.08773, 2022.
[19] X. Li, E. Nie, and S. Liang, “From classification to generation: Insights into crosslingual retrieval augmented icl,” arXiv preprint arXiv:2311.06595, 2023.
[20] D. Cheng, S. Huang, J. Bi, Y. Zhan, J. Liu, Y. Wang, H. Sun, F. Wei, D. Deng, and Q. Zhang, “Uprise: Universal prompt retrieval for improving zero-shot evaluation,” arXiv preprint arXiv:2303.08518, 2023.
[21] Z. Dai, V. Y. Zhao, J. Ma, Y. Luan, J. Ni, J. Lu, A. Bakalov, K. Guu, K. B. Hall, and M.-W. Chang, “Promptagator: Few-shot dense retrieval from 8 examples,” arXiv preprint arXiv:2209.11755, 2022.
[22] Z. Sun, X. Wang, Y. Tay, Y. Yang, and D. Zhou, “Recitation-augmented language models,” arXiv preprint arXiv:2210.01296, 2022.
[23] O. Khattab, K. Santhanam, X. L. Li, D. Hall, P. Liang, C. Potts, and M. Zaharia, “Demonstrate-search-predict: Composing retrieval and language models for knowledge-intensive nlp,” arXiv preprint arXiv:2212.14024, 2022.
[24] Z. Jiang, F. F. Xu, L. Gao, Z. Sun, Q. Liu, J. Dwivedi-Yu, Y. Yang, J. Callan, and G. Neubig, “Active retrieval augmented generation,” arXiv preprint arXiv:2305.06983, 2023.
[25] A. Asai, Z. Wu, Y. Wang, A. Sil, and H. Hajishirzi, “Self-rag: Learning to retrieve, generate, and critique through self-reflection,” arXiv preprint arXiv:2310.11511, 2023.
[26] Z. Ke, W. Kong, C. Li, M. Zhang, Q. Mei, and M. Bendersky, “Bridging the preference gap between retrievers and llms,” arXiv preprint arXiv:2401.06954, 2024.
[27] X. V. Lin, X. Chen, M. Chen, W. Shi, M. Lomeli, R. James, P. Ro- driguez, J. Kahn, G. Szilvasy, M. Lewis et al., “Ra-dit: Retrieval- augmented dual instruction tuning,” arXiv preprint arXiv:2310.01352, 2023.
[28] O. Ovadia, M. Brief, M. Mishaeli, and O. Elisha, “Fine-tuning or retrieval? comparing knowledge injection in llms,” arXiv preprint arXiv:2312.05934, 2023.
[29] T. Lan, D. Cai, Y. Wang, H. Huang, and X.-L. Mao, “Copy is all you need,” in The Eleventh International Conference on Learning Representations, 2022.
[30] T. Chen, H. Wang, S. Chen, W. Yu, K. Ma, X. Zhao, D. Yu, and H. Zhang, “Dense x retrieval: What retrieval granularity should we use?” arXiv preprint arXiv:2312.06648, 2023.
[31] F. Luo and M. Surdeanu, “Divide & conquer for entailment-aware multi-hop evidence retrieval,” arXiv preprint arXiv:2311.02616, 2023.
[32] Q. Gou, Z. Xia, B. Yu, H. Yu, F. Huang, Y. Li, and N. Cam-Tu, “Diversify question generation with retrieval-augmented style transfer,” arXiv preprint arXiv:2310.14503, 2023.
[33] Z. Guo, S. Cheng, Y. Wang, P. Li, and Y. Liu, “Prompt-guided re- trieval augmentation for non-knowledge-intensive tasks,” arXiv preprint arXiv:2305.17653, 2023.
[34] Z. Wang, J. Araki, Z. Jiang, M. R. Parvez, and G. Neubig, “Learning to filter context for retrieval-augmented generation,” arXiv preprint arXiv:2311.08377, 2023.
[35] M. Seo, J. Baek, J. Thorne, and S. J. Hwang, “Retrieval-augmented data augmentation for low-resource domain tasks,” arXiv preprint arXiv:2402.13482, 2024.
[36] Y. Ma, Y. Cao, Y. Hong, and A. Sun, “Large language model is not a good few-shot information extractor, but a good reranker for hard samples!” arXiv preprint arXiv:2303.08559, 2023.
[37] X. Du and H. Ji, “Retrieval-augmented generative question answering for event argument extraction,” arXiv preprint arXiv:2211.07067, 2022.
[38] L. Wang, N. Yang, and F. Wei, “Learning to retrieve in-context examples for large language models,” arXiv preprint arXiv:2307.07164, 2023.
[39] S. Rajput, N. Mehta, A. Singh, R. H. Keshavan, T. Vu, L. Heldt, L. Hong, Y. Tay, V. Q. Tran, J. Samost et al., “Recommender systems with generative retrieval,” arXiv preprint arXiv:2305.05065, 2023.
[40] B. Jin, H. Zeng, G. Wang, X. Chen, T. Wei, R. Li, Z. Wang, Z. Li, Y. Li, H. Lu et al., “Language models as semantic indexers,” arXiv preprint arXiv:2310.07815, 2023.
[41] R. Anantha, T. Bethi, D. Vodianik, and S. Chappidi, “Context tuning for retrieval augmented generation,” arXiv preprint arXiv:2312.05708, 2023.
[42] G. Izacard, P. Lewis, M. Lomeli, L. Hosseini, F. Petroni, T. Schick, J. Dwivedi-Yu, A. Joulin, S. Riedel, and E. Grave, “Few-shot learning with retrieval augmented language models,” arXiv preprint arXiv:2208.03299, 2022.
[43] J. Huang, W. Ping, P. Xu, M. Shoeybi, K. C.-C. Chang, and B. Catan- zaro, “Raven: In-context learning with retrieval augmented encoder- decoder language models,” arXiv preprint arXiv:2308.07922, 2023.
[44] B. Wang, W. Ping, P. Xu, L. McAfee, Z. Liu, M. Shoeybi, Y. Dong, O. Kuchaiev, B. Li, C. Xiao et al., “Shall we pretrain autoregressive language models with retrieval? a comprehensive study,” arXiv preprint arXiv:2304.06762, 2023.
[45] B. Wang, W. Ping, L. McAfee, P. Xu, B. Li, M. Shoeybi, and B. Catan- zaro, “Instructretro: Instruction tuning post retrieval-augmented pre- training,” arXiv preprint arXiv:2310.07713, 2023.
[46] S. Siriwardhana, R. Weerasekera, E. Wen, T. Kaluarachchi, R. Rana, and S. Nanayakkara, “Improving the domain adaptation of retrieval augmented generation (rag) models for open domain question answer- ing,” Transactions of the Association for Computational Linguistics, vol. 11, pp. 1–17, 2023.
[47] Z. Yu, C. Xiong, S. Yu, and Z. Liu, “Augmentation-adapted retriever improves generalization of language models as generic plug-in,” arXiv preprint arXiv:2305.17331, 2023.
[48] O. Yoran, T. Wolfson, O. Ram, and J. Berant, “Making retrieval- augmented language models robust to irrelevant context,” arXiv preprint arXiv:2310.01558, 2023.
[49] H.-T. Chen, F. Xu, S. A. Arora, and E. Choi, “Understanding re- trieval augmentation for long-form question answering,” arXiv preprint arXiv:2310.12150, 2023.
[50] W. Yu, H. Zhang, X. Pan, K. Ma, H. Wang, and D. Yu, “Chain-of-note: Enhancing robustness in retrieval-augmented language models,” arXiv preprint arXiv:2311.09210, 2023.
[51] S. Xu, L. Pang, H. Shen, X. Cheng, and T.-S. Chua, “Search-in-the- chain: Towards accurate, credible and traceable large language models for knowledgeintensive tasks,” CoRR, vol. abs/2304.14732, 2023.
[52] M. Berchansky, P. Izsak, A. Caciularu, I. Dagan, and M. Wasserblat, “Optimizing retrieval-augmented reader models via token elimination,” arXiv preprint arXiv:2310.13682, 2023.
[53] J. L´ala, O. O’Donoghue, A. Shtedritski, S. Cox, S. G. Rodriques, and A. D. White, “Paperqa: Retrieval-augmented generative agent for scientific research,” arXiv preprint arXiv:2312.07559, 2023.
[54] F. Cuconasu, G. Trappolini, F. Siciliano, S. Filice, C. Campagnano, Y. Maarek, N. Tonellotto, and F. Silvestri, “The power of noise: Redefining retrieval for rag systems,” arXiv preprint arXiv:2401.14887, 2024.
[55] Z. Zhang, X. Zhang, Y. Ren, S. Shi, M. Han, Y. Wu, R. Lai, and Z. Cao, “Iag: Induction-augmented generation framework for answer- ing reasoning questions,” in Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, 2023, pp. 1–14.
[56] N. Thakur, L. Bonifacio, X. Zhang, O. Ogundepo, E. Kamalloo, D. Alfonso-Hermelo, X. Li, Q. Liu, B. Chen, M. Rezagholizadeh et al., “Nomiracl: Knowing when you don’t know for robust multilingual retrieval-augmented generation,” arXiv preprint arXiv:2312.11361, 2023.
[57] G. Kim, S. Kim, B. Jeon, J. Park, and J. Kang, “Tree of clarifica- tions: Answering ambiguous questions with retrieval-augmented large language models,” arXiv preprint arXiv:2310.14696, 2023.
[58] Y. Wang, P. Li, M. Sun, and Y. Liu, “Self-knowledge guided retrieval augmentation for large language models,” arXiv preprint arXiv:2310.05002, 2023.
[59] Z. Feng, X. Feng, D. Zhao, M. Yang, and B. Qin, “Retrieval- generation synergy augmented large language models,” arXiv preprint arXiv:2310.05149, 2023.
[60] P. Xu, W. Ping, X. Wu, L. McAfee, C. Zhu, Z. Liu, S. Subramanian, E. Bakhturina, M. Shoeybi, and B. Catanzaro, “Retrieval meets long context large language models,” arXiv preprint arXiv:2310.03025, 2023.
[61] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal, “Interleav- ing retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions,” arXiv preprint arXiv:2212.10509, 2022.
[62] R. Ren, Y. Wang, Y. Qu, W. X. Zhao, J. Liu, H. Tian, H. Wu, J.- R. Wen, and H. Wang, “Investigating the factual knowledge boundary of large language models with retrieval augmentation,” arXiv preprint arXiv:2307.11019, 2023.
[63] P. Sarthi, S. Abdullah, A. Tuli, S. Khanna, A. Goldie, and C. D. Manning, “Raptor: Recursive abstractive processing for tree-organized retrieval,” arXiv preprint arXiv:2401.18059, 2024.
[64] O. Ram, Y. Levine, I. Dalmedigos, D. Muhlgay, A. Shashua, K. Leyton- Brown, and Y. Shoham, “In-context retrieval-augmented language models,” arXiv preprint arXiv:2302.00083, 2023.
[65] Y. Ren, Y. Cao, P. Guo, F. Fang, W. Ma, and Z. Lin, “Retrieve-and- sample: Document-level event argument extraction via hybrid retrieval augmentation,” in Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2023, pp. 293–306.
[66] Z. Wang, X. Pan, D. Yu, D. Yu, J. Chen, and H. Ji, “Zemi: Learning zero-shot semi-parametric language models from multiple tasks,” arXiv preprint arXiv:2210.00185, 2022.
[67] S.-Q. Yan, J.-C. Gu, Y. Zhu, and Z.-H. Ling, “Corrective retrieval augmented generation,” arXiv preprint arXiv:2401.15884, 2024.
[68] P. Jain, L. B. Soares, and T. Kwiatkowski, “1-pager: One pass answer generation and evidence retrieval,” arXiv preprint arXiv:2310.16568, 2023.
[69] H. Yang, Z. Li, Y. Zhang, J. Wang, N. Cheng, M. Li, and J. Xiao, “Prca: Fitting black-box large language models for retrieval question answer- ing via pluggable reward-driven contextual adapter,” arXiv preprint arXiv:2310.18347, 2023.
[70] S. Zhuang, B. Liu, B. Koopman, and G. Zuccon, “Open-source large language models are strong zero-shot query likelihood models for document ranking,” arXiv preprint arXiv:2310.13243, 2023.
[71] F. Xu, W. Shi, and E. Choi, “Recomp: Improving retrieval-augmented lms with compression and selective augmentation,” arXiv preprint arXiv:2310.04408, 2023.
[72] W. Shi, S. Min, M. Yasunaga, M. Seo, R. James, M. Lewis, L. Zettle- moyer, and W.-t. Yih, “Replug: Retrieval-augmented black-box lan- guage models,” arXiv preprint arXiv:2301.12652, 2023.
[73] E. Melz, “Enhancing llm intelligence with arm-rag: Auxiliary ra- tionale memory for retrieval augmented generation,” arXiv preprint arXiv:2311.04177, 2023.
[74] H. Wang, W. Huang, Y. Deng, R. Wang, Z. Wang, Y. Wang, F. Mi, J. Z. Pan, and K.-F. Wong, “Unims-rag: A unified multi-source retrieval-augmented generation for personalized dialogue systems,” arXiv preprint arXiv:2401.13256, 2024.
[75] Z. Luo, C. Xu, P. Zhao, X. Geng, C. Tao, J. Ma, Q. Lin, and D. Jiang, “Augmented large language models with parametric knowledge guid- ing,” arXiv preprint arXiv:2305.04757, 2023.
[76] X. Li, Z. Liu, C. Xiong, S. Yu, Y. Gu, Z. Liu, and G. Yu, “Structure- aware language model pretraining improves dense retrieval on struc- tured data,” arXiv preprint arXiv:2305.19912, 2023.
[77] M. Kang, J. M. Kwak, J. Baek, and S. J. Hwang, “Knowledge graph-augmented language models for knowledge-grounded dialogue generation,” arXiv preprint arXiv:2305.18846, 2023.
[78] W. Shen, Y. Gao, C. Huang, F. Wan, X. Quan, and W. Bi, “Retrieval- generation alignment for end-to-end task-oriented dialogue system,” arXiv preprint arXiv:2310.08877, 2023.
[79] T. Shi, L. Li, Z. Lin, T. Yang, X. Quan, and Q. Wang, “Dual-feedback knowledge retrieval for task-oriented dialogue systems,” arXiv preprint arXiv:2310.14528, 2023.
[80] P. Ranade and A. Joshi, “Fabula: Intelligence report generation using retrieval-augmented narrative construction,” arXiv preprint arXiv:2310.13848, 2023.
[81] X. Jiang, R. Zhang, Y. Xu, R. Qiu, Y. Fang, Z. Wang, J. Tang, H. Ding, X. Chu, J. Zhao et al., “Think and retrieval: A hypothesis knowledge graph enhanced medical large language models,” arXiv preprint arXiv:2312.15883, 2023.
[82] J. Baek, S. Jeong, M. Kang, J. C. Park, and S. J. Hwang, “Knowledge-augmented language model verification,” arXiv preprint arXiv:2310.12836, 2023.
[83] L. Luo, Y.-F. Li, G. Haffari, and S. Pan, “Reasoning on graphs: Faithful and interpretable large language model reasoning,” arXiv preprint arXiv:2310.01061, 2023.
[84] X. He, Y. Tian, Y. Sun, N. V. Chawla, T. Laurent, Y. LeCun, X. Bresson, and B. Hooi, “G-retriever: Retrieval-augmented generation for textual graph understanding and question answering,” arXiv preprint arXiv:2402.07630, 2024.
[85] L. Zha, J. Zhou, L. Li, R. Wang, Q. Huang, S. Yang, J. Yuan, C. Su, X. Li, A. Su et al., “Tablegpt: Towards unifying tables, nature language and commands into one gpt,” arXiv preprint arXiv:2307.08674, 2023.
[86] M. Gaur, K. Gunaratna, V. Srinivasan, and H. Jin, “Iseeq: Information seeking question generation using dynamic meta-information retrieval and knowledge graphs,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 36, no. 10, 2022, pp. 10 672–10 680.
[87] F. Shi, X. Chen, K. Misra, N. Scales, D. Dohan, E. H. Chi, N. Sch¨arli, and D. Zhou, “Large language models can be easily distracted by irrelevant context,” in International Conference on Machine Learning. PMLR, 2023, pp. 31 210–31 227.
[88] R. Teja, “Evaluating the ideal chunk size for a rag system using llamaindex,” https://www.llamaindex.ai/blog/ evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5, 2023.
[89] Langchain, “Recursively split by character,” https://python.langchain. com/docs/modules/data connection/document transformers/recursive text splitter, 2023.
[90] S. Yang, “Advanced rag 01: Small-to- big retrieval,” https://towardsdatascience.com/ advanced-rag-01-small-to-big-retrieval-172181b396d4, 2023.
[91] Y. Wang, N. Lipka, R. A. Rossi, A. Siu, R. Zhang, and T. Derr, “Knowledge graph prompting for multi-document question answering,” arXiv preprint arXiv:2308.11730, 2023.
[92] D. Zhou, N. Sch¨arli, L. Hou, J. Wei, N. Scales, X. Wang, D. Schu- urmans, C. Cui, O. Bousquet, Q. Le et al., “Least-to-most prompting enables complex reasoning in large language models,” arXiv preprint arXiv:2205.10625, 2022.
[93] S. Dhuliawala, M. Komeili, J. Xu, R. Raileanu, X. Li, A. Celikyilmaz, and J. Weston, “Chain-of-verification reduces hallucination in large language models,” arXiv preprint arXiv:2309.11495, 2023.
[94] X. Li and J. Li, “Angle-optimized text embeddings,” arXiv preprint arXiv:2309.12871, 2023.
[95] VoyageAI, “Voyage’s embedding models,” https://docs.voyageai.com/ embeddings/, 2023.
[96] BAAI, “Flagembedding,” https://github.com/FlagOpen/ FlagEmbedding, 2023.
[97] P. Zhang, S. Xiao, Z. Liu, Z. Dou, and J.-Y. Nie, “Retrieve anything to augment large language models,” arXiv preprint arXiv:2310.07554, 2023.
[98] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and P. Liang, “Lost in the middle: How language models use long contexts,” arXiv preprint arXiv:2307.03172, 2023.
[99] Y. Gao, T. Sheng, Y. Xiang, Y. Xiong, H. Wang, and J. Zhang, “Chat- rec: Towards interactive and explainable llms-augmented recommender system,” arXiv preprint arXiv:2303.14524, 2023.
[100] N. Anderson, C. Wilson, and S. D. Richardson, “Lingua: Addressing scenarios for live interpretation and automatic dubbing,” in Proceedings of the 15th Biennial Conference of the Association for Machine Translation in the Americas (Volume 2: Users and Providers Track and Government Track), J. Campbell, S. Larocca, J. Marciano, K. Savenkov, and A. Yanishevsky, Eds. Orlando, USA: Association for Machine Translation in the Americas, Sep. 2022, pp. 202–209. [Online]. Available: https://aclanthology.org/2022.amta-upg.14
[101] H. Jiang, Q. Wu, X. Luo, D. Li, C.-Y. Lin, Y. Yang, and L. Qiu, “Longllmlingua: Accelerating and enhancing llms in long context scenarios via prompt compression,” arXiv preprint arXiv:2310.06839, 2023.
[102] V. Karpukhin, B. O˘guz, S. Min, P. Lewis, L. Wu, S. Edunov, D. Chen, and W.-t. Yih, “Dense passage retrieval for open-domain question answering,” arXiv preprint arXiv:2004.04906, 2020.
[103] Y. Ma, Y. Cao, Y. Hong, and A. Sun, “Large language model is not a good few-shot information extractor, but a good reranker for hard samples!” ArXiv, vol. abs/2303.08559, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:257532405
[104] J. Cui, Z. Li, Y. Yan, B. Chen, and L. Yuan, “Chatlaw: Open-source legal large language model with integrated external knowledge bases,” arXiv preprint arXiv:2306.16092, 2023.
[105] O. Yoran, T. Wolfson, O. Ram, and J. Berant, “Making retrieval- augmented language models robust to irrelevant context,” arXiv preprint arXiv:2310.01558, 2023.
[106] X. Li, R. Zhao, Y. K. Chia, B. Ding, L. Bing, S. Joty, and S. Poria, “Chain of knowledge: A framework for grounding large language mod- els with structured knowledge bases,” arXiv preprint arXiv:2305.13269, 2023.
[107] H. Yang, S. Yue, and Y. He, “Auto-gpt for online decision making: Benchmarks and additional opinions,” arXiv preprint arXiv:2306.02224, 2023.
[108] T. Schick, J. Dwivedi-Yu, R. Dess`ı, R. Raileanu, M. Lomeli, L. Zettle- moyer, N. Cancedda, and T. Scialom, “Toolformer: Language models can teach themselves to use tools,” arXiv preprint arXiv:2302.04761, 2023.
[109] J. Zhang, “Graph-toolformer: To empower llms with graph rea- soning ability via prompt augmented by chatgpt,” arXiv preprint arXiv:2304.11116, 2023.
[110] R. Nakano, J. Hilton, S. Balaji, J. Wu, L. Ouyang, C. Kim, C. Hesse, S. Jain, V. Kosaraju, W. Saunders et al., “Webgpt: Browser- assisted question-answering with human feedback,” arXiv preprint arXiv:2112.09332, 2021.
[111] T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin, J. Devlin, K. Lee et al., “Natural questions: a benchmark for question answering research,” Transactions of the Association for Computational Linguistics, vol. 7, pp. 453–466, 2019.
[112] Y. Liu, S. Yavuz, R. Meng, M. Moorthy, S. Joty, C. Xiong, and Y. Zhou, “Exploring the integration strategies of retriever and large language models,” arXiv preprint arXiv:2308.12574, 2023.
[113] M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer, “Triviaqa: A large scale distantly supervised challenge dataset for reading comprehen- sion,” arXiv preprint arXiv:1705.03551, 2017.
[114] P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang, “Squad: 100,000+ questions for machine comprehension of text,” arXiv preprint arXiv:1606.05250, 2016.
[115] J. Berant, A. Chou, R. Frostig, and P. Liang, “Semantic parsing on freebase from question-answer pairs,” in Proceedings of the 2013 conference on empirical methods in natural language processing, 2013, pp. 1533–1544.
[116] A. Mallen, A. Asai, V. Zhong, R. Das, H. Hajishirzi, and D. Khashabi, “When not to trust language models: Investigating effectiveness and limitations of parametric and non-parametric memories,” arXiv preprint arXiv:2212.10511, 2022.
[117] T. Nguyen, M. Rosenberg, X. Song, J. Gao, S. Tiwary, R. Majumder, and L. Deng, “Ms marco: A human-generated machine reading com- prehension dataset,” 2016.
[118] Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. W. Cohen, R. Salakhutdi- nov, and C. D. Manning, “Hotpotqa: A dataset for diverse, explain- able multi-hop question answering,” arXiv preprint arXiv:1809.09600, 2018.
[119] X. Ho, A.-K. D. Nguyen, S. Sugawara, and A. Aizawa, “Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps,” arXiv preprint arXiv:2011.01060, 2020.
[120] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal, “Musique: Multihop questions via single-hop question composition,” Transactions of the Association for Computational Linguistics, vol. 10, pp. 539–554, 2022.
[121] A. Fan, Y. Jernite, E. Perez, D. Grangier, J. Weston, and M. Auli, “Eli5: Long form question answering,” arXiv preprint arXiv:1907.09190, 2019.
[122] T. Koˇcisk`y, J. Schwarz, P. Blunsom, C. Dyer, K. M. Hermann, G. Melis, and E. Grefenstette, “The narrativeqa reading comprehension chal- lenge,” Transactions of the Association for Computational Linguistics, vol. 6, pp. 317–328, 2018.
[123] K.-H. Lee, X. Chen, H. Furuta, J. Canny, and I. Fischer, “A human- inspired reading agent with gist memory of very long contexts,” arXiv preprint arXiv:2402.09727, 2024.
[124] I. Stelmakh, Y. Luan, B. Dhingra, and M.-W. Chang, “Asqa: Factoid questions meet long-form answers,” arXiv preprint arXiv:2204.06092, 2022.
[125] M. Zhong, D. Yin, T. Yu, A. Zaidi, M. Mutuma, R. Jha, A. H. Awadallah, A. Celikyilmaz, Y. Liu, X. Qiu et al., “Qmsum: A new benchmark for query-based multi-domain meeting summarization,” arXiv preprint arXiv:2104.05938, 2021.
[126] P. Dasigi, K. Lo, I. Beltagy, A. Cohan, N. A. Smith, and M. Gardner, “A dataset of information-seeking questions and answers anchored in research papers,” arXiv preprint arXiv:2105.03011, 2021.
[127] T. M¨oller, A. Reina, R. Jayakumar, and M. Pietsch, “Covid-qa: A question answering dataset for covid-19,” in ACL 2020 Workshop on Natural Language Processing for COVID-19 (NLP-COVID), 2020.
[128] X. Wang, G. H. Chen, D. Song, Z. Zhang, Z. Chen, Q. Xiao, F. Jiang, J. Li, X. Wan, B. Wang et al., “Cmb: A comprehensive medical benchmark in chinese,” arXiv preprint arXiv:2308.08833, 2023.
[129] H. Zeng, “Measuring massive multitask chinese understanding,” arXiv preprint arXiv:2304.12986, 2023.
[130] R. Y. Pang, A. Parrish, N. Joshi, N. Nangia, J. Phang, A. Chen, V. Pad- makumar, J. Ma, J. Thompson, H. He et al., “Quality: Question an- swering with long input texts, yes!” arXiv preprint arXiv:2112.08608, 2021.
[131] P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord, “Think you have solved question answering? try arc, the ai2 reasoning challenge,” arXiv preprint arXiv:1803.05457, 2018.
[132] A. Talmor, J. Herzig, N. Lourie, and J. Berant, “Commonsenseqa: A question answering challenge targeting commonsense knowledge,” arXiv preprint arXiv:1811.00937, 2018.
[133] E. Dinan, S. Roller, K. Shuster, A. Fan, M. Auli, and J. Weston, “Wizard of wikipedia: Knowledge-powered conversational agents,” arXiv preprint arXiv:1811.01241, 2018.
[134] H. Wang, M. Hu, Y. Deng, R. Wang, F. Mi, W. Wang, Y. Wang, W.- C. Kwan, I. King, and K.-F. Wong, “Large language models as source planner for personalized knowledge-grounded dialogue,” arXiv preprint arXiv:2310.08840, 2023.
[135] ——, “Large language models as source planner for personal- ized knowledge-grounded dialogue,” arXiv preprint arXiv:2310.08840, 2023.
[136] X. Xu, Z. Gou, W. Wu, Z.-Y. Niu, H. Wu, H. Wang, and S. Wang, “Long time no see! open-domain conversation with long-term persona memory,” arXiv preprint arXiv:2203.05797, 2022.
[137] T.-H. Wen, M. Gasic, N. Mrksic, L. M. Rojas-Barahona, P.-H. Su, S. Ultes, D. Vandyke, and S. Young, “Conditional generation and snapshot learning in neural dialogue systems,” arXiv preprint arXiv:1606.03352, 2016.
[138] R. He and J. McAuley, “Ups and downs: Modeling the visual evolution of fashion trends with one-class collaborative filtering,” in proceedings of the 25th international conference on world wide web, 2016, pp. 507–517.
[139] S. Li, H. Ji, and J. Han, “Document-level event argument extraction by conditional generation,” arXiv preprint arXiv:2104.05919, 2021.
[140] S. Ebner, P. Xia, R. Culkin, K. Rawlins, and B. Van Durme, “Multi- sentence argument linking,” arXiv preprint arXiv:1911.03766, 2019.
[141] H. Elsahar, P. Vougiouklis, A. Remaci, C. Gravier, J. Hare, F. Laforest, and E. Simperl, “T-rex: A large scale alignment of natural language with knowledge base triples,” in Proceedings of the Eleventh Inter- national Conference on Language Resources and Evaluation (LREC 2018), 2018.
[142] O. Levy, M. Seo, E. Choi, and L. Zettlemoyer, “Zero-shot relation ex- traction via reading comprehension,” arXiv preprint arXiv:1706.04115, 2017.
[143] R. Zellers, A. Holtzman, Y. Bisk, A. Farhadi, and Y. Choi, “Hel- laswag: Can a machine really finish your sentence?” arXiv preprint arXiv:1905.07830, 2019.
[144] S. Kim, S. J. Joo, D. Kim, J. Jang, S. Ye, J. Shin, and M. Seo, “The cot collection: Improving zero-shot and few-shot learning of language models via chain-of-thought fine-tuning,” arXiv preprint arXiv:2305.14045, 2023.
[145] A. Saha, V. Pahuja, M. Khapra, K. Sankaranarayanan, and S. Chandar, “Complex sequential question answering: Towards learning to converse over linked question answer pairs with a knowledge graph,” in Proceed- ings of the AAAI conference on artificial intelligence, vol. 32, no. 1, 2018.
[146] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt, “Measuring massive multitask language understanding,” arXiv preprint arXiv:2009.03300, 2020.
[147] S. Merity, C. Xiong, J. Bradbury, and R. Socher, “Pointer sentinel mixture models,” arXiv preprint arXiv:1609.07843, 2016.
[148] M. Geva, D. Khashabi, E. Segal, T. Khot, D. Roth, and J. Berant, “Did aristotle use a laptop? a question answering benchmark with implicit reasoning strategies,” Transactions of the Association for Computational Linguistics, vol. 9, pp. 346–361, 2021.
[149] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, “Fever: a large-scale dataset for fact extraction and verification,” arXiv preprint arXiv:1803.05355, 2018.
[150] N. Kotonya and F. Toni, “Explainable automated fact-checking for public health claims,” arXiv preprint arXiv:2010.09926, 2020.
[151] R. Lebret, D. Grangier, and M. Auli, “Neural text generation from structured data with application to the biography domain,” arXiv preprint arXiv:1603.07771, 2016.
[152] H. Hayashi, P. Budania, P. Wang, C. Ackerson, R. Neervannan, and G. Neubig, “Wikiasp: A dataset for multi-domain aspect-based summarization,” Transactions of the Association for Computational Linguistics, vol. 9, pp. 211–225, 2021.
[153] S. Narayan, S. B. Cohen, and M. Lapata, “Don’t give me the details, just the summary! topic-aware convolutional neural networks for ex- treme summarization,” arXiv preprint arXiv:1808.08745, 2018.
[154] S. Saha, J. A. Junaed, M. Saleki, A. S. Sharma, M. R. Rifat, M. Rahouti, S. I. Ahmed, N. Mohammed, and M. R. Amin, “Vio-lens: A novel dataset of annotated social network posts leading to different forms of communal violence and its evaluation,” in Proceedings of the First Workshop on Bangla Language Processing (BLP-2023), 2023, pp. 72– 84.
[155] X. Li and D. Roth, “Learning question classifiers,” in COLING 2002: The 19th International Conference on Computational Linguistics, 2002.
[156] R. Socher, A. Perelygin, J. Wu, J. Chuang, C. D. Manning, A. Y. Ng, and C. Potts, “Recursive deep models for semantic compositionality over a sentiment treebank,” in Proceedings of the 2013 conference on empirical methods in natural language processing, 2013, pp. 1631– 1642.
[157] H. Husain, H.-H. Wu, T. Gazit, M. Allamanis, and M. Brockschmidt, “Codesearchnet challenge: Evaluating the state of semantic code search,” arXiv preprint arXiv:1909.09436, 2019.
[158] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano et al., “Training verifiers to solve math word problems,” arXiv preprint arXiv:2110.14168, 2021.
[159] R. Steinberger, B. Pouliquen, A. Widiger, C. Ignat, T. Erjavec, D. Tufis, and D. Varga, “The jrc-acquis: A multilingual aligned parallel corpus with 20+ languages,” arXiv preprint cs/0609058, 2006.
[160] Y. Hoshi, D. Miyashita, Y. Ng, K. Tatsuno, Y. Morioka, O. Torii, and J. Deguchi, “Ralle: A framework for developing and eval- uating retrieval-augmented large language models,” arXiv preprint arXiv:2308.10633, 2023.
[161] J. Liu, “Building production-ready rag applications,” https://www.ai. engineer/summit/schedule/building-production-ready-rag-applications, 2023.
[162] I. Nguyen, “Evaluating rag part i: How to evaluate document retrieval,” https://www.deepset.ai/blog/rag-evaluation-retrieval, 2023.
[163] Q. Leng, K. Uhlenhuth, and A. Polyzotis, “Best practices for llm evaluation of rag applications,” https://www.databricks.com/blog/ LLM-auto-eval-best-practices-RAG, 2023.
[164] S. Es, J. James, L. Espinosa-Anke, and S. Schockaert, “Ragas: Au- tomated evaluation of retrieval augmented generation,” arXiv preprint arXiv:2309.15217, 2023.
[165] J. Saad-Falcon, O. Khattab, C. Potts, and M. Zaharia, “Ares: An automated evaluation framework for retrieval-augmented generation systems,” arXiv preprint arXiv:2311.09476, 2023.
[166] C. Jarvis and J. Allard, “A survey of techniques for maximizing llm performance,” https://community.openai. com/t/openai-dev-day-2023-breakout-sessions/505213# a-survey-of-techniques-for-maximizing-llm-performance-2, 2023.
[167] J. Chen, H. Lin, X. Han, and L. Sun, “Benchmarking large lan- guage models in retrieval-augmented generation,” arXiv preprint arXiv:2309.01431, 2023.
[168] Y. Liu, L. Huang, S. Li, S. Chen, H. Zhou, F. Meng, J. Zhou, and X. Sun, “Recall: A benchmark for llms robustness against external counterfactual knowledge,” arXiv preprint arXiv:2311.08147, 2023.
[169] Y. Lyu, Z. Li, S. Niu, F. Xiong, B. Tang, W. Wang, H. Wu, H. Liu, T. Xu, and E. Chen, “Crud-rag: A comprehensive chinese benchmark for retrieval-augmented generation of large language models,” arXiv preprint arXiv:2401.17043, 2024.
[170] P. Xu, W. Ping, X. Wu, L. McAfee, C. Zhu, Z. Liu, S. Subramanian, E. Bakhturina, M. Shoeybi, and B. Catanzaro, “Retrieval meets long context large language models,” arXiv preprint arXiv:2310.03025, 2023.
[171] C. Packer, V. Fang, S. G. Patil, K. Lin, S. Wooders, and J. E. Gon- zalez, “Memgpt: Towards llms as operating systems,” arXiv preprint arXiv:2310.08560, 2023.
[172] G. Xiao, Y. Tian, B. Chen, S. Han, and M. Lewis, “Efficient streaming language models with attention sinks,” arXiv preprint arXiv:2309.17453, 2023.
[173] T. Zhang, S. G. Patil, N. Jain, S. Shen, M. Zaharia, I. Stoica, and J. E. Gonzalez, “Raft: Adapting language model to domain specific rag,” arXiv preprint arXiv:2403.10131, 2024.
[174] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws for neural language models,” arXiv preprint arXiv:2001.08361, 2020.
[175] U. Alon, F. Xu, J. He, S. Sengupta, D. Roth, and G. Neubig, “Neuro- symbolic language modeling with automaton-augmented retrieval,” in International Conference on Machine Learning. PMLR, 2022, pp. 468–485.
[176] M. Yasunaga, A. Aghajanyan, W. Shi, R. James, J. Leskovec, P. Liang, M. Lewis, L. Zettlemoyer, and W.-t. Yih, “Retrieval-augmented multi- modal language modeling,” arXiv preprint arXiv:2211.12561, 2022.
[177] J. Li, D. Li, S. Savarese, and S. Hoi, “Blip-2: Bootstrapping language- image pre-training with frozen image encoders and large language models,” arXiv preprint arXiv:2301.12597, 2023.
[178] W. Zhu, A. Yan, Y. Lu, W. Xu, X. E. Wang, M. Eckstein, and W. Y. Wang, “Visualize before you write: Imagination-guided open-ended text generation,” arXiv preprint arXiv:2210.03765, 2022.
[179] J. Zhao, G. Haffar, and E. Shareghi, “Generating synthetic speech from spokenvocab for speech translation,” arXiv preprint arXiv:2210.08174, 2022.
[180] D. M. Chan, S. Ghosh, A. Rastrow, and B. Hoffmeister, “Using external off-policy speech-to-text mappings in contextual end-to-end automated speech recognition,” arXiv preprint arXiv:2301.02736, 2023.
[181] A. Yang, A. Nagrani, P. H. Seo, A. Miech, J. Pont-Tuset, I. Laptev, J. Sivic, and C. Schmid, “Vid2seq: Large-scale pretraining of a visual language model for dense video captioning,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023, pp. 10 714–10 726.
[182] N. Nashid, M. Sintaha, and A. Mesbah, “Retrieval-based prompt selection for code-related few-shot learning,” in 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE), 2023, pp. 2450–2462.
