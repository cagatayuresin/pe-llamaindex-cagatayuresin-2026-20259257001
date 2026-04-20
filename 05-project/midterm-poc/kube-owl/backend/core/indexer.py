"""
KubeOps Agent — Doküman İndeksleme Pipeline
Dokümanları chunking, embedding ve ChromaDB'ye yazma.
"""

import logging
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import chromadb
from llama_index.core import (
    Document,
    StorageContext,
    VectorStoreIndex,
    Settings as LlamaSettings,
)
from llama_index.core.node_parser import (
    MarkdownNodeParser,
    SentenceSplitter,
)
from llama_index.vector_stores.chroma import ChromaVectorStore

from ..config import settings
from .providers import get_embed_model

logger = logging.getLogger(__name__)

# Doküman metadata'sını saklamak için JSON dosya yolu
DOCUMENTS_JSON = Path(settings.upload_dir).resolve() / ".." / "documents.json"


def _get_documents_db_path() -> Path:
    """documents.json dosyasının yolunu döndürür."""
    path = Path(settings.upload_dir).resolve().parent / "documents.json"
    return path


def _load_documents_db() -> dict:
    """Doküman metadata veritabanını yükler."""
    db_path = _get_documents_db_path()
    if db_path.exists():
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning("documents.json okunamadı, yeni oluşturulacak.")
    return {"documents": []}


def _save_documents_db(db: dict):
    """Doküman metadata veritabanını kaydeder."""
    db_path = _get_documents_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2, default=str)


def _get_chroma_client():
    """ChromaDB persistent client döndürür."""
    persist_dir = str(settings.chroma_persist_path)
    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=persist_dir)


def _get_chroma_collection(client=None):
    """ChromaDB koleksiyonunu döndürür veya oluşturur."""
    if client is None:
        client = _get_chroma_client()
    return client.get_or_create_collection("kubeops_runbooks")


def _read_document(file_path: str) -> list[Document]:
    """
    Dosyayı okur ve LlamaIndex Document listesine dönüştürür.
    PDF, MD ve TXT formatlarını destekler.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        try:
            from llama_index.readers.file import PDFReader
            reader = PDFReader()
            documents = reader.load_data(file=path)
        except ImportError:
            # Fallback: basit metin okuma
            logger.warning("PDFReader bulunamadı, metin olarak okumaya çalışılıyor.")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            documents = [Document(text=text, metadata={"source": path.name})]
    elif suffix in (".md", ".txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        documents = [Document(text=text, metadata={"source": path.name})]
    else:
        raise ValueError(f"Desteklenmeyen dosya formatı: {suffix}")

    # Her document'a kaynak metadata ekle
    for doc in documents:
        doc.metadata["source_file"] = path.name
        doc.metadata["file_type"] = suffix.lstrip(".")

    return documents


def _chunk_documents(documents: list[Document], file_type: str) -> list:
    """
    Dokümanları chunk'lara ayırır.
    Markdown dosyaları başlık bazlı, diğerleri token bazlı bölünür.
    """
    if file_type == "md":
        parser = MarkdownNodeParser()
    else:
        parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)

    nodes = parser.get_nodes_from_documents(documents)

    # Her node'a ek metadata ekle
    for node in nodes:
        node.metadata["indexed_at"] = datetime.now(timezone.utc).isoformat()

    logger.info(f"{len(documents)} doküman → {len(nodes)} chunk'a ayrıldı")
    return nodes


def index_document(file_path: str, provider: str = None) -> dict:
    """
    Bir dosyayı indexler: okur, chunk'lar, embedding yapar, ChromaDB'ye yazar.

    Args:
        file_path: İndekslenecek dosyanın yolu
        provider: Kullanılacak embedding provider ('ollama' veya 'gemini')

    Returns:
        dict: {"id": "...", "filename": "...", "chunks": N, "status": "indexed", ...}
    """
    provider = provider or settings.default_provider
    path = Path(file_path)

    logger.info(f"Doküman indexleniyor: {path.name} (provider: {provider})")

    # 1. Dosyayı oku
    documents = _read_document(file_path)

    # 2. Chunk'lara ayır
    file_type = path.suffix.lower().lstrip(".")
    nodes = _chunk_documents(documents, file_type)

    if not nodes:
        raise ValueError(f"Dosyadan chunk oluşturulamadı: {path.name}")

    # 3. Doküman ID oluştur
    doc_id = f"doc_{uuid.uuid4().hex[:12]}"

    # Her node'a doküman ID'si ekle
    for node in nodes:
        node.metadata["doc_id"] = doc_id
        node.metadata["provider"] = provider

    # 4. Embedding modeli al ve ayarla
    embed_model = get_embed_model(provider)
    LlamaSettings.embed_model = embed_model

    # 5. ChromaDB'ye yaz
    chroma_client = _get_chroma_client()
    chroma_collection = _get_chroma_collection(chroma_client)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    # 6. Metadata kaydet
    doc_info = {
        "id": doc_id,
        "filename": path.name,
        "file_path": str(path),
        "file_size": path.stat().st_size,
        "file_type": file_type,
        "chunks": len(nodes),
        "provider": provider,
        "status": "indexed",
        "indexed_at": datetime.now(timezone.utc).isoformat(),
    }

    db = _load_documents_db()
    db["documents"].append(doc_info)
    _save_documents_db(db)

    logger.info(f"Doküman başarıyla indexlendi: {path.name} → {len(nodes)} chunk")
    return doc_info


def delete_document(doc_id: str) -> bool:
    """
    Bir dokümanın tüm chunk'larını ChromaDB'den ve metadata'dan siler.

    Args:
        doc_id: Silinecek dokümanın ID'si

    Returns:
        bool: Başarılı ise True
    """
    logger.info(f"Doküman siliniyor: {doc_id}")

    # Metadata'dan bul
    db = _load_documents_db()
    doc_info = None
    for doc in db["documents"]:
        if doc["id"] == doc_id:
            doc_info = doc
            break

    if not doc_info:
        logger.warning(f"Doküman bulunamadı: {doc_id}")
        return False

    # ChromaDB'den sil
    try:
        chroma_client = _get_chroma_client()
        chroma_collection = _get_chroma_collection(chroma_client)

        # doc_id metadata'sı ile eşleşen tüm chunk'ları bul ve sil
        results = chroma_collection.get(
            where={"doc_id": doc_id}
        )
        if results and results["ids"]:
            chroma_collection.delete(ids=results["ids"])
            logger.info(f"ChromaDB'den {len(results['ids'])} chunk silindi")
    except Exception as e:
        logger.error(f"ChromaDB'den silme hatası: {e}")

    # Upload dosyasını sil
    try:
        file_path = Path(doc_info.get("file_path", ""))
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Dosya silindi: {file_path}")
    except Exception as e:
        logger.error(f"Dosya silme hatası: {e}")

    # Metadata'dan kaldır
    db["documents"] = [d for d in db["documents"] if d["id"] != doc_id]
    _save_documents_db(db)

    logger.info(f"Doküman başarıyla silindi: {doc_id}")
    return True


def get_all_documents() -> list[dict]:
    """Tüm indexlenmiş dokümanların listesini döndürür."""
    db = _load_documents_db()
    return db.get("documents", [])


def get_document(doc_id: str) -> Optional[dict]:
    """Tek bir dokümanın bilgilerini döndürür."""
    db = _load_documents_db()
    for doc in db.get("documents", []):
        if doc["id"] == doc_id:
            return doc
    return None


def get_query_engine(provider: str = None):
    """
    Verilen provider'ın embedding modeli ile uyumlu query engine döndürür.

    Args:
        provider: 'ollama' veya 'gemini'

    Returns:
        LlamaIndex QueryEngine instance
    """
    provider = provider or settings.default_provider
    embed_model = get_embed_model(provider)

    chroma_client = _get_chroma_client()
    chroma_collection = _get_chroma_collection(chroma_client)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )

    query_engine = index.as_query_engine(
        similarity_top_k=5,
        embed_model=embed_model,
    )

    return query_engine


def get_collection_count() -> int:
    """ChromaDB koleksiyonundaki toplam chunk sayısını döndürür."""
    try:
        chroma_client = _get_chroma_client()
        chroma_collection = _get_chroma_collection(chroma_client)
        return chroma_collection.count()
    except Exception:
        return 0
