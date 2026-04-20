"""
KubeOps Agent — RAG Runbook Arama Aracı
ChromaDB'den semantic search yapan FunctionTool.
"""

import logging
from llama_index.core.tools import FunctionTool

from ..core.indexer import get_query_engine

logger = logging.getLogger(__name__)

# Aktif provider (runtime'da set edilir)
_current_provider = "ollama"


def set_provider(provider: str):
    """Arama aracının kullanacağı provider'ı ayarlar."""
    global _current_provider
    _current_provider = provider


def search_runbooks(query: str) -> str:
    """
    Kubernetes runbook'larında anlamsal arama yapar.
    Verilen sorguyla ilgili en uygun troubleshooting bilgilerini döndürür.
    Bu aracı her zaman bir sorunun çözüm adımlarını bulmak için kullan.

    Args:
        query: Aranacak sorun veya konu (örn. "CrashLoopBackOff çözümü", "OOMKilled teşhis adımları")

    Returns:
        İlgili runbook bölümlerinin metni. Her bölüm hangi dosyadan geldiğini belirtir.
    """
    logger.info(f"Runbook araması: '{query}' (provider: {_current_provider})")

    try:
        query_engine = get_query_engine(_current_provider)
        response = query_engine.query(query)

        # Sonuçları formatla
        result_parts = []

        # Ana yanıt
        if response.response:
            result_parts.append(f"Arama Sonucu:\n{response.response}")

        # Kaynak node'ları göster
        if hasattr(response, 'source_nodes') and response.source_nodes:
            result_parts.append("\n--- Kaynak Bölümler ---")
            for i, node in enumerate(response.source_nodes, 1):
                source = node.metadata.get("source_file", "bilinmeyen")
                score = getattr(node, 'score', None)
                score_str = f" (benzerlik: {score:.3f})" if score else ""
                text_preview = node.text[:500] if node.text else "İçerik yok"
                result_parts.append(
                    f"\n[Kaynak {i}: {source}{score_str}]\n{text_preview}"
                )

        result = "\n".join(result_parts) if result_parts else "Runbook'larda ilgili bilgi bulunamadı."
        logger.info(f"Runbook araması tamamlandı: {len(result)} karakter")
        return result

    except Exception as e:
        error_msg = f"Runbook araması başarısız: {str(e)}"
        logger.error(error_msg)
        return error_msg


def get_runbook_search_tool() -> FunctionTool:
    """FunctionTool olarak sarmalanmış runbook arama aracını döndürür."""
    return FunctionTool.from_defaults(
        fn=search_runbooks,
        name="search_runbooks",
        description=(
            "Kubernetes runbook'larında anlamsal arama yapar. "
            "Verilen sorguyla ilgili en uygun troubleshooting bilgilerini döndürür. "
            "Bu aracı her zaman bir sorunun çözüm adımlarını bulmak için kullan. "
            "Örnek: search_runbooks('CrashLoopBackOff çözümü') veya "
            "search_runbooks('OOMKilled teşhis adımları')"
        ),
    )
