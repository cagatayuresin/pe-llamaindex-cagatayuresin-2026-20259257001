# Ajanlar (Agents)

Bir "ajan", otomatik bir akıl yürütme ve karar verme motorudur. Kullanıcı girişini/sorgusunu alır ve doğru sonucu döndürmek için bu sorguyu yürütmeye yönelik dahili kararlar verebilir. Temel ajan bileşenleri şunları içerebilir ancak bunlarla sınırlı değildir:

-   Karmaşık bir soruyu daha küçük sorulara bölmek
-   Kullanılacak harici bir Araç (Tool) seçmek + Aracı çağırmak için parametreler oluşturmak
-   Bir dizi görevi planlamak
-   Önceden tamamlanmış görevleri bir bellek (memory) modülünde saklamak

LlamaIndex, değişen karmaşıklık derecelerine sahip ajanlı sistemler oluşturmak için kapsamlı bir çerçeve sunar:

-   **Ajanları hızlıca oluşturmak istiyorsanız**: Ajanlı sistemleri hızla kurmak için önceden oluşturulmuş [ajan (agent)](/python/framework/module_guides/deploying/agents) ve [araç (tool)](/python/framework/module_guides/deploying/agents/tools) mimarilerimizi kullanın.
-   **Ajanlı sisteminiz üzerinde tam kontrol istiyorsanız**: [İş Akışlarımızı (Workflows)](/python/framework/module_guides/workflow) kullanarak sıfırdan özel ajanlı iş akışları oluşturun ve dağıtın.

## Kullanım Durumları

Ajanlar için olası kullanım durumlarının kapsamı geniştir ve sürekli genişlemektedir. Bununla birlikte, anında değer katabilecek bazı pratik kullanım durumları şunlardır:

-   **Ajanlı RAG**: Verileriniz üzerinde sadece basit soruları değil, karmaşık araştırma görevlerini de yanıtlayan, bağlamla zenginleştirilmiş bir araştırma asistanı oluşturun. [Başlangıç kılavuzumuz](/python/framework/getting_started/starter_example) başlamak için harika bir yerdir.

-   **Rapor Oluşturma**: Çok ajanlı bir araştırmacı + yazar iş akışı + LlamaParse kullanarak çok modlu (multimodal) bir rapor oluşturun. [Notebook](https://github.com/run-llama/llama_cloud_services/examples/parse/multimodal/multimodal_report_generation_agent.ipynb).

-   **Müşteri Desteği**: [İş akışlarıyla çok ajanlı bir mihmandar (concierge)](https://github.com/run-llama/multi-agent-concierge/) oluşturmak için başlangıç şablonuna göz atın.

Diğerleri:

-   **Verimlilik Asistanı**: E-posta, takvim gibi yaygın iş akışı araçları üzerinde çalışabilen bir ajan oluşturun. [GSuite ajan eğitimimize](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-google/examples/advanced_tools_usage.ipynb) göz atın.

-   **Kod Asistanı**: Kod üzerinde çalışabilen bir ajan oluşturun. [Kod yorumlayıcı (code interpreter) eğitimimize](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/tools/llama-index-tools-code-interpreter/examples/code_interpreter.ipynb) göz atın.

## Kaynaklar

**Önceden Oluşturulmuş Ajanlar ve Araçlar**

Aşağıdaki bileşen kılavuzları, ajanlarla geliştirmeye başlamak için merkezi merkezlerdir:

-   [Ajanlar (Agents)](/python/framework/module_guides/deploying/agents)
-   [Araçlar (Tools)](/python/framework/module_guides/deploying/agents/tools)

**Özel Ajanlı İş Akışları**

LlamaIndex İş Akışları (Workflows), temel bir olay güdümlü (event-driven) orkestrasyon temeli aracılığıyla çok özel, ajanlı iş akışları oluşturmanıza olanak tanır.

-   [İş Akışları Dökümantasyonu](/python/llamaagents/workflows)
-   [Bir ReAct ajan iş akışı oluşturma](/python/examples/workflow/react_agent)
-   [İş Akışlarını Dağıtma](/python/llamaagents/llamactl/getting-started/)

**Ajanlı Bileşenlerle İnşa Etme**

İş akışınızda temel ajanlı bileşenlerden yararlanmak istiyorsanız, LlamaIndex her bir ajan alt bileşeni için sağlam soyutlamalara sahiptir.

-   **Sorgu Planlama**: [Yönlendirme (Routing)](/python/framework/module_guides/querying/router), [Alt Sorular (Sub-Questions)](/python/examples/query_engine/sub_question_query_engine), [Sorgu Dönüştürmeleri (Query Transformations)](/python/framework/optimizing/advanced_retrieval/query_transformations).
-   **Fonksiyon Çağırma (Function Calling) ve Araç Kullanımı**: Örnek olarak [OpenAI](/python/examples/llm/openai) ve [Mistral](/python/examples/llm/mistralai) kılavuzlarımıza göz atın.

## Ekosistem

-   **Topluluk Tarafından Oluşturulan Ajanlar**: Ajanınızla kullanmanız için [LlamaHub](https://llamahub.ai/)'da 40'tan fazla ajan aracı koleksiyonu sunuyoruz 🦙.