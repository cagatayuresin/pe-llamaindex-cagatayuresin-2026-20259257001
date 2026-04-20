# Yapılandırılmış Veri Çıkarma (Structured Data Extraction)

LLM'ler büyük miktarda yapılandırılmamış veriyi özümseme ve bunları yapılandırılmış formatlarda döndürme yeteneğine sahiptir ve LlamaIndex bunu kolaylaştırmak için kurulmuştur.

LlamaIndex kullanarak, bir LLM'in doğal dili okumasını ve isimler, tarihler, adresler ve rakamlar gibi anlamsal olarak önemli ayrıntıları tanımlamasını ve kaynak formatı ne olursa olsun bunları tutarlı ve yapılandırılmış bir formatta döndürmesini sağlayabilirsiniz.

Bu, özellikle sohbet günlükleri ve konuşma dökümleri gibi yapılandırılmamış kaynak materyalleriniz olduğunda faydalı olabilir.

Yapılandırılmış verilere sahip olduğunuzda bunları bir veritabanına gönderebilir veya iş akışlarını otomatikleştirmek için kod içinde yapılandırılmış çıktıları ayrıştırabilirsiniz.

## Tam Eğitim

Öğrenme (Learn) bölümümüzde [yapılandırılmış veri çıkarma üzerine tam bir eğitim](/python/framework/understanding/extraction) bulunmaktadır. Oradan başlamanızı öneririz.

Ayrıca eğitimdeki bazı teknikleri gösteren bir [örnek notebook](/python/examples/structured_outputs/structured_outputs) da mevcuttur.

## Diğer Kılavuzlar

Düşük seviyeli modüller de dahil olmak üzere LlamaIndex ile yapılandırılmış veri çıkarmanın daha kapsamlı bir özeti için aşağıdaki kılavuzlara göz atın:

-   [Yapılandırılmış Çıktılar (Structured Outputs)](/python/framework/module_guides/querying/structured_outputs)
-   [Pydantic Programları](/python/framework/module_guides/querying/structured_outputs/pydantic_program)
-   [Çıktı Ayrıştırma (Output Parsing)](/python/framework/module_guides/querying/structured_outputs/output_parser)

Ayrıca çok modlu (multi-modal) yapılandırılmış veri çıkarma özelliğimiz de mevcuttur. [Göz atın](/python/framework/use_cases/multimodal#simple-evaluation-of-multi-modal-rag).

## Çeşitli Örnekler

Kullanım durumlarını vurgulayan bazı ek örnekler:

-   [Kişi açıklamalarından isimleri ve konumları çıkarma](/python/examples/output_parsing/df_program)
-   [Müzik incelemelerinden albüm verilerini çıkarma](/python/examples/llm/llama_api)
-   [E-postalardan bilgi çıkarma](/python/examples/usecases/email_data_extraction)