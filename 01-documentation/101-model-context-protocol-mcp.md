# Model Bağlam Protokolü (Model Context Protocol - MCP)

Model Bağlam Protokolü (MCP), Büyük Dil Modellerinin (LLM'ler) yapılandırılmış API çağrıları aracılığıyla harici araçlar ve veri kaynaklarıyla etkileşime girmesini sağlayan açık kaynaklı standart bir protokoldür.

MCP, AI uygulamalarının araçlar, veritabanları ve önceden tanımlanmış şablonlar gibi harici hizmetlerle etkili bir şekilde iletişim kurması için bir standardizasyon katmanı görevi görür. MCP'yi AI uygulamaları için bir "USB-C bağlantı noktası" gibi düşünün; çeşitli araçların, platformların ve veri kaynaklarının AI modellerine bağlanması için standartlaştırılmış bir yol sağlar.

## Mimari

MCP, bir istemci-sunucu mimarisi üzerinden çalışır:

-   **MCP Host'ları**: Claude Masaüstü, IDE'ler veya MCP aracılığıyla verilere erişmek isteyen AI araçları gibi uygulamalar.
-   **MCP İstemcileri (Clients)**: MCP sunucularıyla 1:1 bağlantı sürdüren protokol istemcileri.
-   **MCP Sunucuları (Servers)**: Yetenekleri (araçlar, kaynaklar, istemler) standartlaştırılmış protokol aracılığıyla sunan hafif hizmetler.

## Temel Yetenekler

MCP üç ana yetenek türünü destekler:

1.  **Araçlar (Tools)**: Yapılandırılmış girdilerle çağrılabilen fonksiyonlar.
2.  **Kaynaklar (Resources)**: Okunabilen veri kaynakları (dosyalar, veritabanları vb.).
3.  **İstemler (Prompts)**: Parametreli, yeniden kullanılabilir istem (prompt) şablonları.

## LlamaIndex ile Kullanım

LlamaIndex ile MCP sunucularını kullanmanın pek çok yolu vardır; bu da agentic (ajan tabanlı) iş akışlarınıza ek kaynaklar ve işlevsellik kazandırmanıza olanak tanır.

-   **Mevcut MCP sunucu araçlarını LlamaIndex iş akışlarıyla kullanın**: Mevcut MCP sunucuları aracılığıyla sunulan harici kaynaklardan veri alın.
-   **LlamaIndex iş akışlarını MCP sunucusu olarak sunun**: Kendi özel LlamaIndex iş akışlarınızı MCP sunucularına dönüştürebilirsiniz.
-   **LlamaIndex iş akışları içinde LlamaCloud hizmetlerini kullanın**: LlamaExtract veya LlamaParse gibi LlamaCloud işlevlerini sunan MCP sunucularımızdan birini (hem Python hem de Typescript) LlamaIndex iş akışları dahil olmak üzere MCP sunucularıyla iletişim kuran diğer herhangi bir uygulama içinde çalıştırın.

## Sonraki Adımlar

-   [LlamaIndex ile MCP Araçlarını Kullanma](/python/framework/module_guides/mcp/llamaindex_mcp)
-   [LlamaCloud API'lerini MCP Araçları/Sunucuları Olarak Kullanma](/python/framework/module_guides/mcp/llamacloud_mcp)
-   [Mevcut LlamaIndex İş Akışını/Aracını MCP Aracı/Sunucusu Olarak Kullanma](/python/framework/module_guides/mcp/convert_existing)