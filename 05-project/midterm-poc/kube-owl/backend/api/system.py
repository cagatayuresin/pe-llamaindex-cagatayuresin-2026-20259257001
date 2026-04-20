"""
KubeOps Agent — Sistem API Endpoint'leri
Health check, config bilgisi, k8s bağlantı durumu.
"""

import logging
import subprocess
import json
import os
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from dotenv import set_key

from ..config import settings
from ..core.indexer import get_all_documents, get_collection_count

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Sistem"])

class SystemConfigRequest(BaseModel):
    default_provider: Optional[str] = None
    ollama_base_url: Optional[str] = None
    ollama_model: Optional[str] = None
    ollama_embed_model: Optional[str] = None
    gemini_api_key: Optional[str] = None
    gemini_model: Optional[str] = None
    gemini_embed_model: Optional[str] = None
    claude_api_key: Optional[str] = None
    claude_model: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    ollama_cloud_url: Optional[str] = None
    ollama_cloud_model: Optional[str] = None

# Session models
class SSHSession(BaseModel):
    id: str
    name: str
    host: str
    port: int = 22
    username: str
    auth_type: str = "password" # "password" or "key"
    password: Optional[str] = None
    key_path: Optional[str] = None

class SessionActiveRequest(BaseModel):
    session_id: Optional[str]

class TerminalCommandRequest(BaseModel):
    command: str

# Global active session
_active_session_id = None



@router.get("/health")
async def health_check():
    """Sistem sağlık durumu."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/config")
async def get_config():
    """Mevcut sistem konfigürasyonu."""
    documents = get_all_documents()
    collection_count = get_collection_count()

    return {
        "default_provider": settings.default_provider,
        "available_providers": ["ollama", "gemini", "claude", "ollama-cloud"],
        "k8s_mode": "real" if settings.has_kubeconfig else "mock",
        "indexed_documents": len(documents),
        "chroma_collection_count": collection_count,
    }


@router.get("/config/raw")
async def get_raw_config():
    """Form alanlarını doldurmak için ham konfigürasyon döner (API keyleri maskelenmiş)."""
    def mask_key(k):
        return "***" if k and k != "your-api-key-here" else ""

    return {
        "default_provider": settings.default_provider,
        "ollama_base_url": settings.ollama_base_url,
        "ollama_model": settings.ollama_model,
        "ollama_embed_model": settings.ollama_embed_model,
        "gemini_api_key": mask_key(settings.gemini_api_key),
        "gemini_model": settings.gemini_model,
        "gemini_embed_model": settings.gemini_embed_model,
        "claude_api_key": mask_key(settings.claude_api_key),
        "claude_model": settings.claude_model,
        "openai_api_key": mask_key(settings.openai_api_key),
        "openai_model": settings.openai_model,
        "ollama_cloud_url": settings.ollama_cloud_url,
        "ollama_cloud_model": settings.ollama_cloud_model,
    }


@router.post("/config/update")
async def update_config(req: SystemConfigRequest):
    """Ayarları günceller ve .env dosyasına yazar."""
    # .env dosyasının kök dizindeki yolu
    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        # Fallback to example if exists
        example_path = os.path.join(os.getcwd(), ".env.example")
        if os.path.exists(example_path):
            import shutil
            shutil.copy(example_path, env_path)

    updates = req.model_dump(exclude_unset=True)

    for k, v in updates.items():
        # Maskelenmiş şifreler "değişmedi" kabul edilir ve güncellenmez
        if v is not None and v != "***" and v != "":
            # 1. settings nesnesini bellekte güncelle
            setattr(settings, k, v)
            # 2. .env dosyasına kalıcı yaz
            set_key(env_path, k.upper(), v)

    return {"status": "success", "message": "Ayarlar başarıyla güncellendi."}


@router.get("/config/providers")
async def get_providers():
    """Kullanılabilir LLM provider'larının listesi."""
    providers = [
        {
            "id": "ollama",
            "name": "Ollama (Lokal)",
            "model": settings.ollama_model,
            "embed_model": settings.ollama_embed_model,
            "base_url": settings.ollama_base_url,
            "description": "Lokal LLM — veriler dışarı çıkmaz, ücretsiz",
        },
        {
            "id": "gemini",
            "name": "Google Gemini (Cloud)",
            "model": settings.gemini_model,
            "embed_model": settings.gemini_embed_model,
            "api_key_set": bool(settings.gemini_api_key and settings.gemini_api_key != "your-api-key-here"),
            "description": "Cloud LLM — daha güçlü ve hızlı, API key gerektirir",
        },
        {
            "id": "claude",
            "name": "Anthropic Claude",
            "model": settings.claude_model,
            "embed_model": "Fallback to Ollama",
            "api_key_set": bool(settings.claude_api_key and settings.claude_api_key != "your-api-key-here"),
            "description": "Gelişmiş analitik yetenekleri sunan Claude modelleri",
        },
        {
            "id": "openai",
            "name": "OpenAI ChatGPT",
            "model": settings.openai_model,
            "embed_model": "Fallback to Ollama",
            "api_key_set": bool(settings.openai_api_key and settings.openai_api_key != "your-api-key-here"),
            "description": "En popüler AI modeli (GPT-4 vb.)",
        },
        {
            "id": "ollama-cloud",
            "name": "Ollama (Cloud)",
            "model": settings.ollama_cloud_model,
            "embed_model": settings.ollama_embed_model,
            "base_url": settings.ollama_cloud_url,
            "description": "Uzak sunucudaki Ollama instance'ı",
        },
    ]

    return {
        "default_provider": settings.default_provider,
        "providers": providers,
    }


@router.get("/config/k8s-status")
async def get_k8s_status():
    """kubectl bağlantı durumu."""
    result = {
        "mode": "real" if settings.has_kubeconfig else "mock",
        "kubeconfig_found": settings.has_kubeconfig,
        "cluster_reachable": False,
        "context": "",
    }

    if settings.has_kubeconfig:
        try:
            # Mevcut context'i al
            context_result = subprocess.run(
                ["kubectl", "config", "current-context"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if context_result.returncode == 0:
                result["context"] = context_result.stdout.strip()

            # Cluster erişilebilirliğini test et
            cluster_result = subprocess.run(
                ["kubectl", "cluster-info"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            result["cluster_reachable"] = cluster_result.returncode == 0

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"kubectl erişim kontrolü başarısız: {e}")
        except Exception as e:
            logger.error(f"kubectl durumu kontrol hatası: {e}")

    return result

# --- SSH Session Management ---

def _load_sessions() -> List[dict]:
    if not os.path.exists(settings.sessions_file):
        return []
    try:
        with open(settings.sessions_file, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Oturum dosyasi okunamadi: {e}")
        return []

def _save_sessions(sessions: List[dict]):
    try:
        os.makedirs(os.path.dirname(settings.sessions_file), exist_ok=True)
        with open(settings.sessions_file, "w") as f:
            json.dump(sessions, f, indent=4)
    except Exception as e:
        logger.error(f"Oturum dosyasi yazilamadi: {e}")

@router.get("/k8s/sessions")
async def list_sessions():
    """Kaydedilmiş SSH oturumlarını listeler."""
    sessions = _load_sessions()
    # Şifreleri dışarıya verme
    for s in sessions:
        if "password" in s:
            s["password"] = "***"
    return {"sessions": sessions, "active_session_id": _active_session_id}

@router.post("/k8s/sessions")
async def add_session(session: SSHSession):
    """Yeni bir SSH oturumu kaydeder."""
    sessions = _load_sessions()
    
    # ID çakışmasını önle
    for s in sessions:
        if s["id"] == session.id:
            s.update(session.model_dump())
            _save_sessions(sessions)
            return {"status": "updated", "id": session.id}
            
    sessions.append(session.model_dump())
    _save_sessions(sessions)
    return {"status": "created", "id": session.id}

@router.delete("/k8s/sessions/{session_id}")
async def delete_session(session_id: str):
    """Bir SSH oturumunu siler."""
    sessions = _load_sessions()
    sessions = [s for s in sessions if s["id"] != session_id]
    _save_sessions(sessions)
    
    global _active_session_id
    if _active_session_id == session_id:
        _active_session_id = None
        
    return {"status": "deleted"}

@router.post("/k8s/sessions/active")
async def set_active_session(req: SessionActiveRequest):
    """Ajanın komut çalıştıracağı aktif SSH oturumunu seçer. Local için null gönderin."""
    global _active_session_id
    _active_session_id = req.session_id
    return {"status": "success", "active_session_id": _active_session_id}

def get_active_session_details() -> Optional[dict]:
    """Backend içerisinden aktif oturum bilgilerini almak için yardımcı fonksiyon."""
    if not _active_session_id:
        return None
    sessions = _load_sessions()
    for s in sessions:
        if s["id"] == _active_session_id:
            return s
    return None

# --- Terminal Management ---

@router.post("/terminal/execute")
async def execute_terminal_command(req: TerminalCommandRequest):
    """Kullanıcının terminal arayüzünden gönderdiği komutu mevcut session'a göre çalıştırır."""
    command = req.command.strip()
    if not command:
        return {"output": ""}
        
    session = get_active_session_details()
    output = ""
    exit_code = 0
    
    try:
        if session:
            # SSH ile Uzaktan Çalıştır
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                connect_kwargs = {
                    "hostname": session["host"],
                    "port": session.get("port", 22),
                    "username": session["username"],
                }
                if session.get("auth_type") == "key" and session.get("key_path"):
                    connect_kwargs["key_filename"] = session["key_path"]
                else:
                    connect_kwargs["password"] = session.get("password")
                
                client.connect(**connect_kwargs)
                stdin, stdout, stderr = client.exec_command(command, timeout=60)
                
                out = stdout.read().decode('utf-8', errors='replace')
                err = stderr.read().decode('utf-8', errors='replace')
                
                output = out
                if err:
                    if output:
                        output += f"\n{err}"
                    else:
                        output = err
                        
                exit_code = stdout.channel.recv_exit_status()
            finally:
                client.close()
        else:
            # Lokal Çalıştır
            import shlex
            cmd_parts = shlex.split(command)
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=60,
                shell=False
            )
            exit_code = result.returncode
            output = result.stdout
            if result.stderr:
                if output:
                    output += f"\n{result.stderr}"
                else:
                    output = result.stderr
                    
        if not output:
            output = ""
            
        return {"output": output, "exit_code": exit_code}
        
    except Exception as e:
        logger.error(f"Terminal Command Error: {e}")
        return {"output": f"ERROR: {str(e)}", "exit_code": -1}

