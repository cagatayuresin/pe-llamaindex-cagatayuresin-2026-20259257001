# ☸ KubeOps Agent — Agentic RAG for Kubernetes Operations

Kubernetes cluster'larında yaşanan operasyonel sorunları **otomatik teşhis eden ve çözüm öneren** bir yapay zeka ajanıdır.

## 🎯 Ne Yapar?

KubeOps Agent, organizasyonun kendi runbook'larını (troubleshooting rehberlerini) öğrenir ve bu bilgiyi gerçek zamanlı cluster verileriyle birleştirerek:

1. **Runbook'ları indexler** — PDF, Markdown, TXT formatındaki troubleshooting dokümanlarını vektörleştirir
2. **Sorunları teşhis eder** — ReAct pattern ile düşünür, araçlar kullanır, gözlemler
3. **Çözüm önerir** — Runbook bilgisi + cluster verisini birleştirerek somut adımlar sunar

## 🏗️ Mimari

```
┌──────────────┐     ┌─────────────────────────────────────┐
│  Web UI      │────▶│  FastAPI Backend                     │
│  Bulma CSS   │     │  ┌───────────────────────────────┐  │
│  Vanilla JS  │     │  │  ReAct Agent (LlamaIndex)     │  │
└──────────────┘     │  │  ┌─────────┐  ┌───────────┐  │  │
                     │  │  │ RAG     │  │ kubectl   │  │  │
                     │  │  │ Search  │  │ (real/    │  │  │
                     │  │  │         │  │  mock)    │  │  │
                     │  │  └────┬────┘  └─────┬─────┘  │  │
                     │  └───────┼──────────────┼────────┘  │
                     │          ▼              ▼           │
                     │  ┌───────────┐  ┌──────────────┐   │
                     │  │ ChromaDB  │  │ K8s Cluster  │   │
                     │  └───────────┘  └──────────────┘   │
                     │          ▼                          │
                     │  ┌─────────────────────────┐       │
                     │  │ Ollama / Gemini LLM     │       │
                     │  └─────────────────────────┘       │
                     └─────────────────────────────────────┘
```

## 🚀 Kurulum

### Gereksinimler

- Python 3.11+
- Ollama (lokal LLM için) ve/veya Google Gemini API key

### Adımlar

```bash
# 1. Python virtual environment oluştur
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 2. Bağımlılıkları kur
pip install -r requirements.txt

# 3. Environment dosyasını hazırla
cp .env.example .env
# .env dosyasını düzenle (Gemini API key, Ollama ayarları)

# 4. Ollama modelleri (lokal LLM kullanacaksan)
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

# 5. Uygulamayı başlat
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 6. Tarayıcıda aç
# http://localhost:8000
```

## 📖 Kullanım

1. **Runbook Yükle:** Sidebar'dan `.pdf`, `.md`, `.txt` formatında troubleshooting dokümanlarınızı yükleyin
2. **Provider Seç:** Header'dan Ollama (lokal) veya Gemini (cloud) seçin
3. **Soru Sorun:** Chat alanına Kubernetes sorununuzu yazın
4. **Teşhis Alın:** Ajan düşünce adımlarıyla birlikte teşhis ve çözüm önerir

## 🔌 API Endpoint'leri

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `POST` | `/api/documents/upload` | Runbook dosyası yükle |
| `GET` | `/api/documents` | Yüklü dokümanları listele |
| `GET` | `/api/documents/{id}` | Doküman detayı |
| `DELETE` | `/api/documents/{id}` | Doküman sil |
| `POST` | `/api/agent/query` | Ajana soru sor |
| `GET` | `/api/health` | Sistem sağlık durumu |
| `GET` | `/api/config` | Konfigürasyon bilgisi |
| `GET` | `/api/config/providers` | Kullanılabilir LLM'ler |
| `GET` | `/api/config/k8s-status` | kubectl bağlantı durumu |

Swagger UI: `http://localhost:8000/docs`

## 🛡️ Güvenlik

- kubectl komutları **read-only whitelist** ile sınırlıdır (`get`, `describe`, `logs`, `top`)
- Write/destructive komutlar engellenir (`delete`, `apply`, `exec`, vb.)
- Pipe, redirect ve chain operatörleri yasaklanmıştır
- Yüklenen dosyalar tip ve boyut kontrolünden geçer (max 10MB)

## 🧰 Teknolojiler

| Katman | Teknoloji |
|--------|-----------|
| Backend | FastAPI (Python) |
| RAG Framework | LlamaIndex |
| Vector DB | ChromaDB |
| LLM (Lokal) | Ollama (qwen2.5:7b) |
| LLM (Cloud) | Google Gemini (2.0 Flash) |
| Frontend | HTML + Vanilla JS + Bulma CSS |
| İkonlar | Tabler Icons |

## 📁 Proje Yapısı

```
├── backend/
│   ├── main.py              # FastAPI entrypoint
│   ├── config.py             # Konfigürasyon
│   ├── api/                  # REST API endpoint'leri
│   ├── core/                 # RAG, Agent, Provider mantığı
│   ├── tools/                # kubectl ve runbook search araçları
│   └── utils/                # Güvenlik, dosya işlemleri
├── frontend/
│   ├── index.html            # Ana sayfa
│   ├── css/app.css           # Stiller
│   └── js/                   # Uygulama mantığı
├── runbooks/                 # Örnek runbook'lar
├── data/                     # ChromaDB + uploads (runtime)
├── requirements.txt
└── .env.example
```

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmektedir.
