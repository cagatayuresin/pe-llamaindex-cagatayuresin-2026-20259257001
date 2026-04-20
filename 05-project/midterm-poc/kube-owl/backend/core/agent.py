"""
KubeOps Agent — ReAct Ajan Tanımı
LlamaIndex ReActAgent (Workflow-based) ile araçları birleştiren ajan oluşturma.
"""

import logging
import re
import time

from llama_index.core.agent import ReActAgent

from ..config import settings
from .providers import get_llm, get_provider_info
from .prompts import SYSTEM_PROMPT
from ..tools.runbook_search import get_runbook_search_tool, set_provider as set_search_provider
from ..tools.kubectl_tool import get_kubectl_tool
from ..tools.kubectl_mock import get_kubectl_mock_tool

logger = logging.getLogger(__name__)


from ..api.system import get_active_session_details

def _get_kubectl_tool():
    """Config'e veya SSH session'a göre gerçek veya mock kubectl tool'unu seçer."""
    if settings.has_kubeconfig or get_active_session_details() is not None:
        logger.info("Gerçek kubectl tool'u kullanılıyor (kubeconfig veya SSH mevcut)")
        return get_kubectl_tool()
    else:
        logger.info("Mock kubectl tool'u kullanılıyor (kubeconfig veya SSH bulunamadı)")
        return get_kubectl_mock_tool()


def create_agent(provider: str = None) -> ReActAgent:
    """
    Belirtilen LLM provider ile ReAct ajanı oluşturur.

    Args:
        provider: 'ollama' veya 'gemini'. None ise config'den alınır.

    Returns:
        Hazır ReActAgent instance'ı
    """
    provider = provider or settings.default_provider

    logger.info(f"ReAct ajanı oluşturuluyor (provider: {provider})")

    # LLM'i al
    llm = get_llm(provider)

    # Runbook search provider'ını ayarla
    set_search_provider(provider)

    # Tool'ları hazırla
    runbook_tool = get_runbook_search_tool()
    kubectl_tool = _get_kubectl_tool()

    tools = [runbook_tool, kubectl_tool]

    # ReAct ajanı oluştur (LlamaIndex 0.12+ factory pattern)
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        max_iterations=30,
    )

    logger.info(f"ReAct ajanı hazır — {len(tools)} tool, max_iterations=30")
    return agent


def _parse_agent_steps(response) -> list[dict]:
    """
    Ajan response'undan düşünce ve aksiyon adımlarını parse eder.
    LlamaIndex'te ReAct tool çalıştırdığında response.sources içerisinde
    ToolOutput objeleri olarak döndürülür.
    """
    steps = []

    try:
        if hasattr(response, 'sources') and response.sources:
            for source in response.sources:
                # source bir ToolOutput nesnesidir
                tool_name = getattr(source, 'tool_name', 'unknown')
                tool_input = str(getattr(source, 'raw_input', ''))
                tool_output = str(getattr(source, 'raw_output', ''))
                
                if tool_name and tool_name != 'unknown':
                    step = {
                        "type": "action",
                        "tool": tool_name,
                        "input": tool_input,
                        "output": tool_output,
                    }
                    steps.append(step)

        # raw içinden thought parse et (Eğer düz metin olarak varsa)
        if hasattr(response, 'raw') and response.raw:
            raw_text = str(response.raw)
            thoughts = re.findall(r'Thought:\s*(.*?)(?=Action:|Observation:|$)', raw_text, re.DOTALL)
            for t in thoughts:
                t = t.strip()
                if t:
                    # Thought'u başa veya tool'dan önce ekleyebiliriz
                    # Ancak şimdilik tools listesinin başına ekleyelim
                    steps.insert(0, {"type": "thought", "content": t})

    except Exception as e:
        logger.warning(f"Adım parse hatası: {e}")

    return steps


def _extract_sources(response) -> list[str]:
    """Ajan response'undan kaynak dosya isimlerini çıkarır."""
    sources = set()

    try:
        response_text = str(getattr(response, 'response', ''))
        raw_text = str(getattr(response, 'raw', ''))
        combined = response_text + " " + raw_text

        # Dosya adlarını bul
        matches = re.findall(r'([a-zA-Z0-9_-]+\.(?:md|pdf|txt))', combined)
        sources.update(matches)

        # [Kaynak X: dosya.md] formatını da ara
        matches = re.findall(r'\[Kaynak \d+: ([^\]]+)\]', combined)
        sources.update(matches)

    except Exception as e:
        logger.warning(f"Kaynak çıkarma hatası: {e}")

    return list(sources)


async def query_agent(query: str, provider: str = None) -> dict:
    """
    Ajana soru sorar ve yapılandırılmış yanıt döndürür.

    Args:
        query: Kullanıcının sorusu
        provider: LLM provider ('ollama' veya 'gemini')

    Returns:
        dict: {
            "answer": str,
            "steps": list[dict],
            "sources": list[str],
            "provider": str,
            "model": str,
            "duration_ms": int
        }
    """
    provider = provider or settings.default_provider
    provider_info = get_provider_info(provider)

    logger.info(f"Ajan sorgusu başlatılıyor: '{query[:100]}...' (provider: {provider})")

    start_time = time.time()

    try:
        # Ajanı oluştur
        agent = create_agent(provider)

        # Asenkron olarak ajanı çalıştır
        response = await agent.aquery(query)

        duration_ms = int((time.time() - start_time) * 1000)

        # Sonuçları parse et
        answer = str(response.response) if hasattr(response, 'response') and response.response else "Ajan bir yanıt üretemedi."
        steps = _parse_agent_steps(response)
        sources = _extract_sources(response)

        result = {
            "answer": answer,
            "steps": steps,
            "sources": sources,
            "provider": provider,
            "model": provider_info.get("llm_model", "unknown"),
            "duration_ms": duration_ms,
        }

        logger.info(f"Ajan sorgusu tamamlandı — {duration_ms}ms, {len(steps)} adım")
        return result

    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(f"Ajan sorgu hatası: {e}")
        raise
