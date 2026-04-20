# İstem Verme (Prompting)

LLM'lere istem (prompt) vermek, herhangi bir LLM uygulamasının temel birimidir. Tamamen istem verme üzerine kurulu bir uygulama oluşturabilir veya RAG, ajanlar ve daha fazlasını oluşturmak için diğer modüllerle (örneğin getirme) orkestrasyon yapabilirsiniz.

LlamaIndex, karmaşık istem iş akışlarını mümkün kılmak için LLM soyutlamalarını ve basitten gelişmişe doğru istem soyutlamalarını destekler.

## LLM Entegrasyonları

LlamaIndex; OpenAI, Anthropic gibi tescilli model sağlayıcılarından Mistral, Ollama, Replicate gibi açık kaynaklı modellere/model sağlayıcılarına kadar 40'tan fazla LLM entegrasyonunu destekler. Asenkron, akış (streaming), fonksiyon çağırma dahil ancak bunlarla sınırlı olmamak üzere yaygın LLM kullanım modelleri etrafında arayüzü standartlaştırmak için tüm araçları sağlar.

İşte [LLM'ler için tam modül kılavuzu](/python/framework/module_guides/models/llms).

## İstemler (Prompts)

LlamaIndex, LLM'lerle tüm yaygın etkileşim modellerini yakalayan sağlam istem soyutlamalarına sahiptir.

İşte [istemler için tam modül kılavuzu](/python/framework/module_guides/models/prompts).

### Temel Özellikler

-   [Metin Tamamlama İstemleri (Text Completion Prompts)](/python/examples/customization/prompts/completion_prompts)
-   [Sohbet İstemleri (Chat Prompts)](/python/examples/customization/prompts/chat_prompts)

### Gelişmiş Özellikler

-   [Değişken Eşlemeleri, Fonksiyonlar, Kısmi (Partial) İstemler](/python/examples/prompts/advanced_prompts)
-   [RichPromptTemplate Özellikleri](/python/examples/prompts/rich_prompt_template_features)

## İstem Zincirleri ve İşlem Hatları (Pipelines)

LlamaIndex; sıralı istem zincirleri ve istemleri diğer herhangi bir bileşenle orkestre etmek için genel DAG'lar oluşturmak üzere sağlam soyutlamalara sahiptir. Bu; çok adımlı (multi-hop) sorgu anlama katmanlarına sahip RAG'lerin yanı sıra ajanları içeren karmaşık iş akışları oluşturmanıza olanak tanır.

Bu işlem hatları, kutudan çıktığı haliyle [gözlemlenebilirlik (observability) ortaklarıyla](/python/framework/module_guides/observability) entegre edilmiştir.