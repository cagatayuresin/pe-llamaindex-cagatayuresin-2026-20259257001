"""
KubeOps Agent — FastAPI Ana Uygulama
CORS, router mount, startup event'leri, static files.
"""

import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .api.documents import router as documents_router
from .api.agent import router as agent_router
from .api.system import router as system_router

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama yaşam döngüsü: startup ve shutdown event'leri."""
    # ─── STARTUP ───
    logger.info("=" * 60)
    logger.info("KubeOps Agent başlatılıyor...")
    logger.info("=" * 60)

    # Data dizinlerini oluştur
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    settings.chroma_persist_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Upload dizini: {settings.upload_path}")
    logger.info(f"ChromaDB dizini: {settings.chroma_persist_path}")

    # ChromaDB bağlantısını test et
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(settings.chroma_persist_path))
        collection = client.get_or_create_collection("kubeops_runbooks")
        logger.info(f"ChromaDB bağlantısı başarılı — Koleksiyon chunk sayısı: {collection.count()}")
    except Exception as e:
        logger.error(f"ChromaDB bağlantı hatası: {e}")

    # K8s modu logla
    k8s_mode = "Gerçek (kubeconfig mevcut)" if settings.has_kubeconfig else "Mock (kubeconfig bulunamadı)"
    logger.info(f"Kubernetes modu: {k8s_mode}")
    logger.info(f"Varsayılan LLM provider: {settings.default_provider}")
    logger.info("KubeOps Agent hazır! http://localhost:8000")
    logger.info("=" * 60)

    yield

    # ─── SHUTDOWN ───
    logger.info("KubeOps Agent kapatılıyor...")


# FastAPI uygulamasını oluştur
app = FastAPI(
    title="KubeOps Agent",
    description=(
        "Kubernetes cluster'larında operasyonel sorunları otomatik teşhis eden "
        "ve çözüm öneren Agentic RAG sistemi."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router'ları mount et (static files'dan ÖNCE!)
app.include_router(documents_router)
app.include_router(agent_router)
app.include_router(system_router)


# Frontend statik dosyalarını serve et
frontend_dir = Path(__file__).parent.parent / "frontend"


@app.get("/")
async def serve_index():
    """Ana sayfayı serve et."""
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "KubeOps Agent API", "docs": "/docs"}


# Static files mount (CSS, JS dosyaları için)
if frontend_dir.exists():
    app.mount("/css", StaticFiles(directory=str(frontend_dir / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(frontend_dir / "js")), name="js")
