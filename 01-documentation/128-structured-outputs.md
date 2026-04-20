# Yapılandırılmış Çıktılar (Structured Outputs)

LLM'lerin yapılandırılmış çıktılar üretebilme yeteneği, çıktı değerlerinin güvenilir bir şekilde ayrıştırılmasına dayanan alt akış uygulamaları (downstream applications) için önemlidir.
LlamaIndex'in kendisi de aşağıdaki şekillerde yapılandırılmış çıktıya güvenir:

-   **Döküman getirme (retrieval)**: LlamaIndex içindeki birçok veri yapısı, döküman getirme için belirli bir şemaya sahip LLM çağrılarına dayanır. Örneğin; ağaç indeksi (tree index), LLM çağrılarının "YANIT: (sayı)" formatında olmasını bekler.
-   **Yanıt sentezi**: Kullanıcılar, nihai yanıtın bir dereceye kadar yapı içermesini bekleyebilir (örneğin; bir JSON çıktısı, formatlanmış bir SQL sorgusu vb.).

LlamaIndex, LLM'lerin yapılandırılmış formatta çıktılar üretmesini sağlayan çeşitli modüller sunar. Varsayılan olarak yapılandırılmış çıktı, LLM sınıflarımız içinde sunulmaktadır. Ayrıca daha düşük seviyeli modüller de sağlıyoruz:

-   **Pydantic Programları**: Bunlar, bir girdi istemini (prompt), bir Pydantic nesnesiyle temsil edilen yapılandırılmış bir çıktıya eşleyen genel modüllerdir. Fonksiyon çağırma (function calling) API'lerini veya metin tamamlama API'lerini + çıktı ayrıştırıcılarını kullanabilirler. Bunlar sorgu motorlarıyla da entegre edilebilir.
-   **Önceden Tanımlanmış Pydantic Programları**: Girdileri (dataframe'ler gibi) belirli çıktı türlerine eşleyen önceden tanımlanmış Pydantic programlarımız vardır.
-   **Çıktı Ayrıştırıcıları (Output Parsers)**: Bunlar, bir LLM metin tamamlama uç noktasının öncesinde ve sonrasında çalışan modüllerdir. LLM fonksiyon çağırma uç noktalarıyla birlikte kullanılmazlar (çünkü bunlar zaten kutudan çıktığı haliyle yapılandırılmış çıktılar içerir).

Çıktı ayrıştırıcıları ve Pydantic programlarına genel bir bakış için aşağıdaki bölümlere bakın.

## 🔬 Yapılandırılmış Çıktı Fonksiyonunun Anatomisi

Burada, LLM destekli bir yapılandırılmış çıktı fonksiyonunun farklı bileşenlerini açıklıyoruz. İşlem hattı (pipeline), dökümanlarda **genel bir LLM metin tamamlama API'si** mi yoksa bir **LLM fonksiyon çağırma API'si** mi kullandığınıza bağlıdır.

![](./../../../_static/structured_output/diagram1.png)

Genel tamamlama API'lerinde girdiler ve çıktılar metin istemleri (prompts) ile yönetilir. Çıktı ayrıştırıcısı (output parser), yapılandırılmış çıktıları sağlamak için LLM çağrısından önce ve sonra bir rol oynar. LLM çağrısından önce çıktı ayrıştırıcısı, isteme format talimatları ekleyebilir. LLM çağrısından sonra ise çıktı ayrıştırıcısı, çıktıyı belirtilen talimatlara göre ayrıştırabilir.

Fonksiyon çağırma API'lerinde çıktı doğal olarak yapılandırılmış bir formattadır ve girdi istenen nesnenin imzasını (signature) alabilir. Yapılandırılmış çıktının sadece doğru nesne formatına (örneğin Pydantic) dönüştürülmesi gerekir.

## Başlangıç Kılavuzları

-   [Yapılandırılmış veri çıkarma eğitimi](/python/understanding/extraction)
-   [Yapılandırılmış Çıktı Örnekleri](/python/examples/structured_outputs/structured_outputs)

## Diğer Kaynaklar

-   [Pydantic Programları](/python/framework/module_guides/querying/structured_outputs/pydantic_program)
-   [Yapılandırılmış Çıktılar + Sorgu Motorları](/python/framework/module_guides/querying/structured_outputs/query_engine)
-   [Çıktı Ayrıştırıcıları](/python/framework/module_guides/querying/structured_outputs/output_parser)