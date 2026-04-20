# Yanıt Modları (Response Modes)

Şu anda aşağıdaki seçenekleri destekliyoruz:

-   `refine`: Getirilen her metin parçasından (chunk) sırayla geçerek bir yanıt **_oluşturun ve rafine edin_**. Bu, her Düğüm (Node)/getirilen parça başına ayrı bir LLM çağrısı yapar.

    **Detaylar:** İlk parça, `text_qa_template` istemi kullanılarak bir sorguda kullanılır. Daha sonra yanıt ve bir sonraki parça (ve asıl soru), `refine_template` istemiyle başka bir sorguda kullanılır. Tüm parçalar ayrıştırılana kadar bu böyle devam eder.

    Eğer bir parça pencereye sığmayacak kadar büyükse (istem boyutu hesaba katılarak), bir `TokenTextSplitter` kullanılarak bölünür (parçalar arasında bir miktar metin çakışmasına izin verilir) ve (yeni) ek parçalar orijinal parça koleksiyonunun parçaları olarak kabul edilir (ve böylece `refine_template` ile sorgulanır).

    Daha ayrıntılı yanıtlar için iyidir.

-   `compact` (varsayılan): `refine` moduna benzer ancak parçaları önceden **_yoğunlaştırır_** (birleştirir), bu da daha az LLM çağrısı yapılmasını sağlar.

    **Detaylar:** Bağlam penceresine sığabilecek kadar çok metni (`text_qa_template` ve `refine_template` arasındaki maksimum istem boyutunu dikkate alarak getirilen parçalardan birleştirilmiş/paketlenmiş) doldurur. Metin tek bir isteme sığmayacak kadar uzunsa, ihtiyaç duyulduğu kadar çok parçaya bölünür (bir `TokenTextSplitter` kullanılarak ve böylece metin parçaları arasında bir miktar çakışmaya izin verilerek).

    Her metin parçası bir "parça" (chunk) olarak kabul edilir ve `refine` sentezleyicisine gönderilir.

    Kısacası, `refine` gibidir ancak daha az LLM çağrısı içerir.

-   `tree_summarize`: Birleştirilmiş tüm parçalar sorgulanana kadar `summary_template` istemini kullanarak LLM'i gerektiği kadar sorgular; bu da kendileri özyinelemeli (recursive) olarak bir `tree_summarize` LLM çağrısında parça olarak kullanılan yanıtlarla sonuçlanır ve tek bir parça kalana dek bu böyle devam eder, sonuçta tek bir nihai yanıt elde edilir.

    **Detaylar:** Parçaları, `summary_template` istemini kullanarak bağlam penceresine sığacak şekilde mümkün olduğunca birleştirir ve gerekirse böler (yine bir `TokenTextSplitter` ve bir miktar metin çakışması ile). Ardından, ortaya çıkan her parça/bölüm için `summary_template` üzerinden sorgu yapar (**_refine_** sorgusu yoktur!) ve her birinden yanıtlar alır.

    Sadece bir yanıt varsa (çünkü sadece bir parça vardı), o zaman bu nihai yanıttır.

    Birden fazla yanıt varsa, bunlar da parça olarak kabul edilir ve özyinelemeli olarak `tree_summarize` sürecine gönderilir (birleştirilir/sığacak şekilde bölünür/sorgulanır).

    Özetleme amaçları için iyidir.

-   `simple_summarize`: Tüm metin parçalarını tek bir LLM istemine sığacak şekilde keser (truncate). Hızlı özetleme amaçları için iyidir, ancak kesme nedeniyle detay kaybı yaşanabilir.
-   `no_text`: Sadece LLM'e gönderilecek olan node'ları getirmek için getiriciyi (retriever) çalıştırır, ancak bunları gerçekte göndermez. Daha sonra `response.source_nodes` kontrol edilerek incelenebilir.
-   `accumulate`: Bir metin parçası seti ve sorgu verildiğinde, yanıtları bir diziye (array) biriktirirken sorguyu her metin parçasına uygular. Tüm yanıtların birleştirilmiş bir dizesini döndürür. Aynı sorguyu her metin parçasına karşı ayrı ayrı çalıştırmanız gerektiğinde iyidir.
-   `compact_accumulate`: `accumulate` ile aynıdır, ancak her LLM istemini `compact` moduna benzer şekilde "yoğunlaştırır" ve her metin parçasına karşı aynı sorguyu çalıştırır.

Daha fazlasını öğrenmek için [Yanıt Sentezleyici (Response Synthesizer)](/python/framework/module_guides/querying/response_synthesizers) bölümüne bakın.