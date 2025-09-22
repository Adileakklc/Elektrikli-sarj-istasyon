# EV Telemetry Backend

Elektrikli şarj istasyonları için telemetri toplama ve anomali tespit projesi.

## 🚀 Kurulum
```bash
git clone <repo-url>
cd week2_backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Çalıştırma
```bash
cd week2_backend
python app.py
```

Varsayılan olarak `http://localhost:5000` üzerinde çalışır.

## 🔌 API Uçları
- `POST /telemetry` → veri kaydı + riskScore
- `POST /ml` → ML skor denemesi
- `GET /sessions` → son N seansı listeler
- `POST /sessions/{id}/stop` → seansı durdur (şimdilik log)

## 📑 Pages Linkleri
- [Operatör Paneli](panel.html)
- [API (Swagger)](docs/openapi.yaml)
- [Mimari](docs/mimari.md) _(eklenecek)_
- [Rapor](docs/rapor.md) _(eklenecek)_

## 🧠 Modeller
ML modelleri `./models/` klasörüne konmalı:  
- `scaler.pkl`
- `iso.pkl`

## ⚠️ Sürüm Uyarısı
Bu proje **deneme aşamasındadır**. Güvenlik sertleştirmeleri (TLS, JWT, HSTS) ilerleyen sürümlerde eklenecektir.
