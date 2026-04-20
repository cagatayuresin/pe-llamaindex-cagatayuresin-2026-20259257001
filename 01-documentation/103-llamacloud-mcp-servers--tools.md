# LlamaCloud MCP Sunucuları ve Araçları

LlamaIndex; LlamaCloud İndeksleri ve LlamaExtract gibi LlamaCloud hizmetleriyle entegre olan resmi MCP sunucuları sağlar.

[`llamacloud-mcp`](https://github.com/run-llama/llamacloud-mcp) Python paketi; LlamaCloud indekslerini bilgi tabanı olarak ve LlamaExtract ajanlarını yapılandırılmış veri çıkarımı için kullanarak hem sorgulama hem de veri çıkarma yeteneklerini destekleyen alternatif bir uygulama sunar.

## Kurulum

```bash
pip install llamacloud-mcp
# veya
uvx llamacloud-mcp@latest
```

## Claude ile Kullanım

Claude-code gibi bir MCP hostu ile kullanmak için yapılandırma dosyanızı şu şekilde ayarlayabilirsiniz:

```json
{
  "mcpServers": {
    "llama_index_docs_server": {
      "command": "uvx",
      "args": [
        "llamacloud-mcp@latest",
        "--index",
        "indeks-adiniz:İndeksinizin açıklaması",
        "--index",
        "diger-indeks-adiniz:Diğer indeksinizin açıklaması",
        "--extract-agent",
        "veri-cikarma-ajani-adi:Veri çıkarma ajanınızın açıklaması",
        "--project-name",
        "<LlamaCloud Proje Adınız>",
        "--org-id",
        "<LlamaCloud Organizasyon Kimliğiniz (Org ID)>",
        "--api-key",
        "<LlamaCloud API Anahtarınız>"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "<filesystem aracının erişmesini istediğiniz dizin>"
      ]
    }
  }
}
```

## Genel Kullanım

Varsayılan olarak, MCP sunucusu `stdio` iletimi (transport) ile başlatılır. Bu; stdin/stdout üzerinden MCP sunucularını destekleyen Claude Masaüstü gibi hostlar için kullanışlıdır. Ancak sunucuyu, HTTP üzerinden MCP sunucularını destekleyen hostlar için yararlı olan `streamable-http` veya `sse` iletimi ile de başlatabilirsiniz.

Sunucuyu doğrudan komut satırından başlatabilirsiniz:

```bash
llamacloud-mcp --index "indeks-adi:Aciklama" --extract-agent "ad:aciklama" --org-id ORGANIZASYON_KIMLIGINIZ --project-id PROJE_KIMLIGINIZ --api-key API_ANAHTARINIZ --transport streamable-http
```