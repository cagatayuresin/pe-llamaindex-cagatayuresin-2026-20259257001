#!/bin/bash

# KubeOps Agent — Start Script
# Bu script uygulamayı doğru ortam ayarlarıyla başlatır.

echo "------------------------------------------------------------"
echo "☸ KubeOps Agent Başlatılıyor..."
echo "------------------------------------------------------------"

# Virtual environment aktif et (varsa)
if [ -d "venv" ]; then
    echo "[1/3] Sanal ortam (venv) aktif ediliyor..."
    source venv/bin/activate
else
    echo "[!] venv klasörü bulunamadı, sistem python'ı kullanılacak."
fi

# PYTHONPATH ayarla (import hatalarını önlemek için)
echo "[2/3] PYTHONPATH ayarlanıyor..."
export PYTHONPATH=$PYTHONPATH:.

# .env kontrolü
if [ ! -f ".env" ]; then
    echo "[!] .env dosyası bulunamadı! .env.example dosyasından kopyalanıyor..."
    cp .env.example .env
    echo "[!] LÜTFEN .env DOSYASINI DÜZENLEYİN (API Key vb.)"
fi

# Servisi başlat
echo "[3/3] Uvicorn başlatılıyor: http://localhost:8000"
echo "------------------------------------------------------------"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
