# LlamaHub

Veri bağlayıcılarımız (data connectors) [LlamaHub](https://llamahub.ai/) 🦙 aracılığıyla sunulur.
LlamaHub; herhangi bir LlamaIndex uygulamasına kolayca dahil edebileceğiniz açık kaynaklı veri bağlayıcılarının (+ Ajan Araçları ve Llama Paketleri) bir kayıt defterini içerir.

![](./../../../_static/data_connectors/llamahub.png)

## Kullanım Kalıbı

Şu şekilde başlayın:

```python
from llama_index.core import download_loader
from llama_index.readers.google import GoogleDocsReader

loader = GoogleDocsReader()
documents = loader.load_data(document_ids=[...])
```

## Yerleşik Bağlayıcı: SimpleDirectoryReader

`SimpleDirectoryReader`; `.md`, `.pdf`, `.jpg`, `.png`, `.docx` gibi çok çeşitli dosya türlerinin yanı sıra ses ve video türlerini de ayrıştırmayı destekleyebilir. LlamaIndex'in bir parçası olarak doğrudan mevcuttur:

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
```

## Mevcut Bağlayıcılar

Aşağıdakiler de dahil olmak üzere mevcut yüzlerce bağlayıcıyı görmek için doğrudan [LlamaHub](https://llamahub.ai/) adresine göz atın:

- [Notion](https://developers.notion.com/) (`NotionPageReader`)
- [Google Docs](https://developers.google.com/docs/api) (`GoogleDocsReader`)
- [Slack](https://api.slack.com/) (`SlackReader`)
- [Discord](https://discord.com/developers/docs/intro) (`DiscordReader`)
- [Apify Actors](https://llamahub.ai/l/apify-actor) (`ApifyActor`): Web'i tarayabilir, web sayfalarını kazıyabilir (scrape), metin içeriğini çıkarabilir; `.pdf`, `.jpg`, `.png`, `.docx` vb. dosyaları indirebilir.