"""
KubeOps Agent — Ajan Sorgulama API Endpoint'i
Ajana soru sorma ve yanıt alma.
"""

import logging
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from ..config import settings
from ..core.agent import query_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agent", tags=["Ajan"])


class QueryRequest(BaseModel):
    """Ajan sorgu isteği."""
    query: str = Field(..., description="Ajana sorulacak soru", min_length=1)
    provider: str = Field(
        default=None,
        description="LLM provider: 'ollama' veya 'gemini'. Boş bırakılırsa varsayılan kullanılır."
    )


class StepResponse(BaseModel):
    """Ajan adım yanıtı."""
    type: str
    tool: str = ""
    input: str = ""
    output: str = ""
    content: str = ""


class QueryResponse(BaseModel):
    """Ajan sorgu yanıtı."""
    answer: str
    steps: list[dict] = []
    sources: list[str] = []
    provider: str
    model: str
    duration_ms: int


@router.post("/query", response_model=QueryResponse)
async def agent_query(request: QueryRequest):
    """
    Ajana soru sorar ve yapılandırılmış yanıt döndürür.

    Ajan, runbook'larda arama yaparak ve kubectl komutları çalıştırarak
    Kubernetes sorunlarını teşhis eder ve çözüm önerir.
    """
    provider = request.provider or settings.default_provider

    logger.info(f"Ajan sorgusu alındı: '{request.query[:100]}...' (provider: {provider})")

    try:
        result = await query_agent(request.query, provider)
        return QueryResponse(**result)

    except ValueError as e:
        # Provider veya config hatası
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        # LLM bağlantı hatası
        raise HTTPException(
            status_code=503,
            detail=f"LLM servisine bağlanılamadı ({provider}): {str(e)}"
        )
    except TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail="Ajan zaman aşımına uğradı. Lütfen tekrar deneyin."
        )
    except Exception as e:
        logger.error(f"Ajan sorgu hatası: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ajan sorgusu sırasında hata oluştu: {str(e)}"
        )
