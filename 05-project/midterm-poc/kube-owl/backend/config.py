"""
KubeOps Agent — Configuration Management
Pydantic Settings ile .env dosyasından konfigürasyon okuma.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Uygulama konfigürasyonu. .env dosyasından otomatik yüklenir."""

    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama API base URL")
    ollama_model: str = Field(default="qwen2.5:7b", description="Ollama LLM model adı")
    ollama_embed_model: str = Field(default="nomic-embed-text", description="Ollama embedding model adı")

    # Gemini Configuration
    gemini_api_key: str = Field(default="", description="Google Gemini API key")
    gemini_model: str = Field(default="models/gemini-2.0-flash", description="Gemini LLM model adı")
    gemini_embed_model: str = Field(default="models/text-embedding-004", description="Gemini embedding model adı")

    # Claude Configuration
    claude_api_key: str = Field(default="", description="Anthropic Claude API key")
    claude_model: str = Field(default="claude-3-5-sonnet-latest", description="Claude LLM model adı")

    # OpenAI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI LLM model adı")

    # Ollama Cloud Configuration
    ollama_cloud_url: str = Field(default="", description="Ollama Cloud API base URL")
    ollama_cloud_model: str = Field(default="qwen2.5:7b", description="Ollama Cloud LLM model adı")

    # SSH Sessions
    sessions_file: str = Field(default="./data/sessions.json", description="SSH Kubernetes sessions json file")

    # Default Provider
    default_provider: str = Field(default="ollama", description="Varsayılan LLM provider: 'ollama', 'gemini', 'claude', 'openai' veya 'ollama-cloud'")

    # ChromaDB
    chroma_persist_dir: str = Field(default="./data/chromadb", description="ChromaDB persistent storage dizini")

    # File Upload
    upload_dir: str = Field(default="./data/uploads", description="Yüklenen dosyaların saklanacağı dizin")
    max_file_size_mb: int = Field(default=10, description="Maksimum dosya boyutu (MB)")

    # Kubernetes
    kubeconfig_path: str = Field(default="~/.kube/config", description="Kubeconfig dosya yolu")

    @property
    def has_kubeconfig(self) -> bool:
        """Kubeconfig dosyası mevcut mu kontrol eder."""
        expanded_path = os.path.expanduser(self.kubeconfig_path)
        return os.path.isfile(expanded_path)

    @property
    def max_file_size_bytes(self) -> int:
        """Maksimum dosya boyutunu byte cinsinden döndürür."""
        return self.max_file_size_mb * 1024 * 1024

    @property
    def chroma_persist_path(self) -> Path:
        """ChromaDB persist dizininin tam yolunu döndürür."""
        return Path(self.chroma_persist_dir).resolve()

    @property
    def upload_path(self) -> Path:
        """Upload dizininin tam yolunu döndürür."""
        return Path(self.upload_dir).resolve()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton instance
settings = Settings()
