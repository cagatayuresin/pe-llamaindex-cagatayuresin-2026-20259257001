# Veri Bağlayıcılar (LlamaHub)

## Kavram

Bir veri bağlayıcı (diğer adıyla `Reader` - Okuyucu), farklı veri kaynaklarından ve veri formatlarından gelen verileri basit bir `Document` (Döküman) temsiline (metin ve basit meta veriler) dönüştürerek içeri alır.

> **İpucu:** Verilerinizi içeri aldıktan sonra üzerine bir [İndeks](/python/framework/module_guides/indexing) inşa edebilir, bir [Sorgu Motoru (Query Engine)](/python/framework/module_guides/deploying/query_engine) kullanarak sorular sorabilir ve bir [Sohbet Motoru (Chat Engine)](/python/framework/module_guides/deploying/chat_engines) ile diyalog kurabilirsiniz.

## LlamaHub

Veri bağlayıcılarımız [LlamaHub](https://llamahub.ai/) 🦙 üzerinden sunulmaktadır. LlamaHub, herhangi bir LlamaIndex uygulamasına kolayca takıp çalıştırabileceğiniz veri yükleyicileri içeren açık kaynaklı bir merkezdir.

![LlamaHub](./../../../_static/data_connectors/llamahub.png)

## Kullanım Kalıbı (Usage Pattern)

Şununla başlayın:

```python
from llama_index.core import download_loader
from llama_index.readers.google import GoogleDocsReader

loader = GoogleDocsReader()
documents = loader.load_data(document_ids=[...])
```

Daha fazla ayrıntı için tam [kullanım kalıbı kılavuzuna](/python/framework/module_guides/loading/connector/usage_pattern) bakın.

## Modüller

Bazı örnek veri bağlayıcılar:

-   Yerel dosya dizini (`SimpleDirectoryReader`). Çok çeşitli dosya türlerini ayrıştırmayı destekleyebilir: `.pdf`, `.jpg`, `.png`, `.docx` vb.
-   [Notion](https://developers.notion.com/) (`NotionPageReader`)
-   [Google Docs](https://developers.google.com/docs/api) (`GoogleDocsReader`)
-   [Slack](https://api.slack.com/) (`SlackReader`)
-   [Discord](https://discord.com/developers/docs/intro) (`DiscordReader`)
-   [Apify Aktörleri](https://llamahub.ai/l/readers/llama-index-readers-apify) (`ApifyActor`). Web'i tarayabilir, web sayfalarını kazıyabilir, metin içeriklerini ayıklayabilir, `.pdf`, `.jpg`, `.png`, `.docx` vb. dahil olmak üzere dosyaları indirebilir.

Daha fazla ayrıntı için [modül kılavuzuna](/python/framework/module_guides/loading/connector/modules) bakın.