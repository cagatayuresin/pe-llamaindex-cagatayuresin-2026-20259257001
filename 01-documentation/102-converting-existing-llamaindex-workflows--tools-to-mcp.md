# Mevcut LlamaIndex İş Akışlarını ve Araçlarını MCP'ye Dönüştürme

Daha geniş bir ekosistem uyumluluğu için LlamaIndex araçlarınızı ve iş akışlarınızı (workflows) MCP sunucularına dönüştürün.

## İş Akışlarını (Workflows) Dönüştürme

Herhangi bir LlamaIndex İş Akışını bir [FastMCP](https://github.com/jlowin/fastmcp) sunucusuna dönüştürmek için `workflow_as_mcp` kullanın:

```python
from llama_index.core.workflow import Context, Workflow, step
from llama_index.core.workflow.events import StartEvent, StopEvent
from llama_index.tools.mcp.utils import workflow_as_mcp


class QueryEvent(StartEvent):
    query: str


class SimpleWorkflow(Workflow):
    @step
    def process_query(self, ctx: Context, ev: QueryEvent) -> StopEvent:
        result = f"İşlendi: {ev.query}"
        return StopEvent(result=result)


# MCP sunucusuna dönüştür
workflow = SimpleWorkflow()
mcp = workflow_as_mcp(workflow, start_event_model=QueryEvent)
```

Eğer doğrudan [FastMCP](https://github.com/jlowin/fastmcp) kullanıyor olsaydınız, şuna benzer görünürdü:

```python
from fastmcp import FastMCP

# İş akışı tanımı
...

mcp = FastMCP("Demo 🚀")
workflow = SimpleWorkflow()


@mcp.tool
async def run_my_workflow(input_args: QueryEvent) -> str:
    """İki sayıyı topla"""
    if isinstance(input_args, dict):
        input_args = QueryEvent.model_validate(input_args)
    result = await workflow.run(start_event=input_args)
    return str(result)


if __name__ == "__main__":
    mcp.run()
```

## Bireysel Araçları Dönüştürme

Mevcut fonksiyonları ve araçları doğrudan MCP uç noktalarına dönüştürmek için FastMCP'yi de kullanabiliriz:

```python
from fastmcp import FastMCP
from llama_index.tools.notion import NotionToolSpec

# ToolSpec'ten araçları al
tool_spec = NotionToolSpec(integration_token="your_token")
tools = tool_spec.to_tool_list()

# MCP sunucusu oluştur
mcp_server = FastMCP("Araç Sunucusu")

# Araçları kaydet
for tool in tools:
    mcp_server.tool(
        name=tool.metadata.name, description=tool.metadata.description
    )(tool.fn)
```

## MCP Sunucusunu Çalıştırma

Sunucunuzu komut satırı (CLI) üzerinden başlatabilirsiniz (bu hata ayıklama için de harikadır!):

```bash
# MCP CLI yükle
pip install "mcp[cli]"

# Sunucuyu çalıştır
mcp run sunucunuz.py
```