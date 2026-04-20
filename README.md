<div align="center">

<img src="https://raw.githubusercontent.com/run-llama/llama_index/main/docs/_static/assets/LlamaSquama.jpeg" width="100" alt="LlamaIndex Logo"/>

# LlamaIndex — Prompt Engineering Course Repository

**Çağatay Üresin · [20259257001] · Bilgisayar Mühendisliği ABD Yüksek Lisans**

[![Framework](https://img.shields.io/badge/Framework-LlamaIndex-6C63FF?style=for-the-badge&logo=python&logoColor=white)](https://www.llamaindex.ai/)
[![Course](https://img.shields.io/badge/Course-Prompt_Engineering-0EA5E9?style=for-the-badge)](.)
[![Language](https://img.shields.io/badge/Language-Python-F7C948?style=for-the-badge&logo=python&logoColor=black)](.)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22C55E?style=for-the-badge)]()

---

[English](#english) · [Türkçe](#türkçe)

---

</div>

---

## English

### About This Repository

This repository contains all course deliverables for the **Prompt Engineering** graduate course at the Department of Computer Engineering. The assigned framework is **LlamaIndex** — a powerful data framework for building LLM-powered applications with advanced RAG (Retrieval-Augmented Generation) pipelines.

### Repository Structure

```
pe-llamaindex-cagatayuresin-[STUDENTNO]/
│
├── README.md                          ← You are here (EN + TR)
├── LICENSE
├── CHANGELOG.md
│
├── 01-documentation/                  ← Turkish translation of LlamaIndex docs
│   ├── README.md
│   ├── 01-giris-ve-genel-bakis.md
│   ├── 02-kurulum-ve-ortam.md
│   ├── 03-temel-kavramlar.md
│   ├── 04-veri-yukleme-ve-indeksleme.md
│   ├── 05-sorgulama-motorlari.md
│   ├── 06-arac-ve-agentlar.md
│   ├── 07-llm-entegrasyonlari.md
│   └── 08-ileri-duzey-kullanim.md
│
├── 02-article/                        ← Selected academic article
│   ├── README.md
│   ├── original/
│   │   └── article-original.pdf          ← Original English article
│   ├── translation/
│   │   └── makale-turkce-cevirisi.md     ← Turkish translation
│   └── presentation/
│       ├── makale-sununum-notlari.md     ← Speaker notes
│       └── makale-sunumu.pptx            ← Slide deck
│
├── 03-framework-presentation/         ← LlamaIndex framework presentation
│   ├── README.md
│   ├── sunum-notlari.md                  ← Speaker script
│   └── llamaindex-sunumu.pptx
│
├── 04-social-media/                   ← X/Twitter post analysis
│   ├── README.md
│   └── tweets-analiz.md                  ← Collected tweets + TR translation + analysis
│
├── 05-project/                        ← Course project (POC → Advanced)
│   ├── README.md
│   │
│   ├── midterm-poc/                   ← Phase 1: Proof of Concept
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   ├── docker-compose.yml
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── indexer.py
│   │   │   └── query_engine.py
│   │   ├── data/
│   │   │   └── .gitkeep
│   │   └── notebooks/
│   │       └── poc-demo.ipynb
│   │
│   └── final-advanced/                ← Phase 2: Production-grade version
│       ├── README.md
│       ├── requirements.txt
│       ├── .env.example
│       ├── docker-compose.yml
│       ├── src/
│       │   ├── main.py
│       │   ├── api/
│       │   ├── agents/
│       │   ├── pipelines/
│       │   └── frontend/
│       ├── data/
│       │   └── .gitkeep
│       ├── tests/
│       └── notebooks/
│           └── final-demo.ipynb
│
└── resources/                         ← Shared resources
    ├── references.md
    └── useful-links.md
```

### Deliverables Overview

| # | Deliverable | Status | Directory |
|---|-------------|--------|-----------|
| 1 | LlamaIndex Documentation (TR) | Completed | `01-documentation/` |
| 2 | Article Translation + Presentation | Completed | `02-article/` |
| 3 | Framework Presentation | Completed | `03-framework-presentation/` |
| 4 | X/Twitter Post Analysis | Completed | `04-social-media/` |
| 5 | Midterm Project (POC) | Completed | `05-project/midterm-poc/` |
| 6 | Final Project (Advanced) | Planned | `05-project/final-advanced/` |

### Project Summary

> **KubeOps Agent** — A LlamaIndex-powered RAG system for intelligent Kubernetes troubleshooting and runbook automation. The system ingests Kubernetes documentation and operational runbooks, then answers natural language queries about cluster issues using vector search and agentic reasoning.

- **POC:** Core RAG pipeline with ChromaDB vector store. Supports multiple LLM providers (Ollama, Gemini, Claude, OpenAI) and features a dual-mode Kubernetes integration (Real vs. Mock).
- **Final:** Planned multi-agent architecture with advanced tool use, API layer, and refined web dashboard.

### Tech Stack

`LlamaIndex` · `ChromaDB` · `Ollama` · `Gemini` · `FastAPI` · `Python 3.11+` · `Docker`

---

## Türkçe

### Bu Repo Hakkında

Bu depo, Bilgisayar Mühendisliği Anabilim Dalı Yüksek Lisans programında alınan **Prompt Mühendisliği** dersinin tüm ödev teslimlerini içermektedir. Atanan framework **LlamaIndex** olup; gelişmiş RAG (Retrieval-Augmented Generation) pipeline'ları ile LLM destekli uygulamalar geliştirmeye yönelik güçlü bir veri framework'üdür.

### Depo Yapısı

Yukarıdaki İngilizce bölümde yer alan dizin ağacı aynı zamanda bu repo için de geçerlidir.

### Teslim Listesi

| # | Teslim | Durum | Dizin |
|---|--------|-------|-------|
| 1 | LlamaIndex Dokümantasyonu (TR Çeviri) | Tamamlandı | `01-documentation/` |
| 2 | Makale Çevirisi + Makale Sunumu | Tamamlandı | `02-article/` |
| 3 | Framework Sunumu | Tamamlandı | `03-framework-presentation/` |
| 4 | X/Twitter Gönderi Analizi | Tamamlandı | `04-social-media/` |
| 5 | Vize Projesi (POC) | Tamamlandı | `05-project/midterm-poc/` |
| 6 | Final Projesi (Gelişmiş Sürüm) | Planlandı | `05-project/final-advanced/` |

### Proje Özeti

> **KubeOps Agent** — LlamaIndex tabanlı bir RAG sistemi. Kubernetes sorunlarını doğal dil sorguları ile tespit edip; operasyonel runbook'ları kullanarak çözüm önerir. Vektör arama ve ajanlar aracılığıyla akıllı küme yönetimi sağlar.

- **POC:** ChromaDB vektör veritabanı ile temel RAG pipeline. Çoklu LLM sağlayıcı desteği (Ollama, Gemini, Claude, OpenAI) ve çift modlu Kubernetes entegrasyonu (Gerçek vs. Mock) içerir.
- **Final:** Araç kullanan çok-ajan mimarisi, gelişmiş API katmanı ve web arayüzü iyileştirmeleri.

### Teknoloji Yığını

`LlamaIndex` · `ChromaDB` · `Ollama` · `Gemini` · `FastAPI` · `Python 3.11+` · `Docker`

---

<div align="center">

**Çağatay Üresin** · [cagatayuresin.com](https://cagatayuresin.com) · [GitHub](https://github.com/cagatayuresin)

*Bilgisayar Mühendisliği ABD — Prompt Mühendisliği Dersi — 2025-2026*

</div>