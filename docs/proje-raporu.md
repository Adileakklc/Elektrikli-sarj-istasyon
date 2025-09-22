# Elektrikli Şarj İstasyonları --- Güvenlik & Anomali Tespiti Projesi

**Kısa Özet**\
Bu proje elektrikli araç (EV) şarj istasyonu telemetrisini hedef alır.
Amaç: gerçek cihaz akışıyla (ESP8266/ESP32), kural tabanlı kontroller ve
makine öğrenmesi ile anomali tespiti yapıp operatör paneline risk
skorları sağlamaktır. Proje; veri toplama, kurallar (replay/rate/limit),
ML modelleme (IsolationForest vs LogisticRegression), backend
entegrasyonu (Flask) ve basit bir web panel prototipi içerir.

------------------------------------------------------------------------

## İçindekiler

-   Proje Hedefleri
-   Mimari
-   Veri Seti ve Ön İşleme
-   Cihaz Tarafı (ESP) Mantığı
-   Backend: API & Güvenlik Kontrolleri
-   Özellik Mühendisliği
-   ML Modelleri, Metrikler ve Sonuçlar
-   Deneysel Senaryolar
-   Çıktılar / Dosyalar
-   Çalıştırma Talimatları
-   Ekler

------------------------------------------------------------------------

## 1. Proje Hedefleri

1.  Şarj istasyonu telemetrisini güvenli şekilde almak (HMAC + nonce +
    TLS).\
2.  Kural tabanlı saldırı tespiti (replay, anormal enerji/süre, rate
    limit).\
3.  ML tabanlı anomali tespiti (IsolationForest ve LogisticRegression
    karşılaştırması).\
4.  Backend'e risk skorunu ekleyip operatör paneline sunmak.\
5.  Son rapor ve demo (savunmasız → kurallar → ML + panel ile müdahale).

------------------------------------------------------------------------

## 2. Mimari

Sistem 3 katmanlıdır:

-   **Saha (Device)**: ESP32/ESP8266 → ölçümler (enerji, süre, voltaj,
    akım), nonce + HMAC üretimi, TLS üzerinden gönderir.\
-   **Backend (Cloud / Secure Zone)**: Flask API `/telemetry` ve `/ml`.
    İçerir: HMAC doğrulama, zaman/nonce kontrol, rate limiting, kural
    motoru, DB (SQLite), feature extraction, ML skorlama, loglama.\
-   **Operatör Ağı (Panel)**: HTML/JS tabanlı web panel; aktif seans
    tablosu ve risk rozetleri, "Seansı Durdur" butonu.

------------------------------------------------------------------------

## 3. Veri Seti ve Ön İşleme

-   Kullanılan dataset: `ev_charging_patterns.csv`\
-   Öne çıkan kolonlar: `Energy Consumed (kWh)`, `Charging Duration`,
    `Temperature (°C)`, `Vehicle Age (years)`, vb.\
-   Dönüşümler:
    -   `Duration_min` = duration (saniye) / 60\
    -   `Energy_per_min` = Energy Consumed / Duration_min\
    -   `Start_Hour` = başlangıç saati\
-   Eksik değerler eğitimde temizlendi.

------------------------------------------------------------------------

## 4. Cihaz (ESP) Mantığı

Örnek JSON:

``` json
{
  "userId": "User_1",
  "enerji": 60.71,
  "sure": 2130,
  "voltaj": 220,
  "akim": 6.0,
  "timestamp": "2024-01-01 00:00:00",
  "nonce": "abc123",
  "hash": "<hmac_hex>"
}
```

-   HMAC imzası backend ile aynı `SHARED_SECRET` kullanılarak üretilir.\
-   Nonce tekilliği DB'de `UNIQUE` tanımıyla korunur.\
-   Rate-limit: aynı kullanıcı için 5 saniyede \>3 istek →
    `429 rate limited`.

------------------------------------------------------------------------

## 5. Backend (Flask)

-   `/telemetry`: timestamp, HMAC, rate, kurallar, nonce kontrolü → DB
    insert.\
-   `/ml`: JSON → özellik çıkarımı → scaler → IsolationForest scoring →
    riskScore.

Örnek `/ml` cevabı:

``` json
{"prediction": "normal", "riskScore": 0.092}
```

------------------------------------------------------------------------

## 6. Özellik Mühendisliği

Kullanılan özellikler:\
- Energy Consumed (kWh)\
- Duration_min\
- Energy_per_min\
- Start_Hour\
- Temperature (°C)\
- Vehicle Age (years)

------------------------------------------------------------------------

## 7. Modeller ve Sonuçlar

  Metric      IsolationForest   LogisticRegression
  ----------- ----------------- --------------------
  Accuracy    1.000             0.742
  Precision   1.000             0.719
  Recall      1.000             0.982
  F1          1.000             0.830

Not: IsolationForest mükemmel sonuçlar verdi; LogisticRegression daha
gerçekçi ama etiket kalitesine bağlı.

------------------------------------------------------------------------

## 8. Deneysel Senaryolar

-   Normal istek:\

``` bash
curl -sS -H "Content-Type: application/json" --data-binary "@ml.json" http://127.0.0.1:5000/ml
```

-   Replay testi: aynı nonce tekrar → `409 replay detected`.\
-   Rate-limit testi: 4 istek / 5s → `429 rate limited`.

------------------------------------------------------------------------

## 9. Çıktılar / Dosyalar

-   `app.py` --- Flask backend\
-   `models/scaler.pkl`, `models/iso.pkl` --- ML modelleri\
-   `telemetry.db` --- SQLite veritabanı\
-   `index.html`, `style.css` --- Web panel\
-   `docs/` → `ml.md`, `mimari.md`, `rapor.md`, görseller

------------------------------------------------------------------------

## 10. Çalıştırma Talimatları

### Lokal

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask pandas numpy scikit-learn
py app.py
```

Test:

``` powershell
curl.exe -sS -H "Content-Type: application/json" --data-binary "@ml.json" http://127.0.0.1:5000/ml
```

### Colab

-   Model eğitimi ve görseller Colab'da yapılır.\
-   `ml_metrics_table.csv` → `ml-result.png` grafik üretildi.

------------------------------------------------------------------------

## 11. Sonuçlar & Değerlendirme

-   Kurallar hızlı ve güvenilir; replay ve anormal enerji/süreyi
    engelliyor.\
-   ML modelleri bilinmeyen örüntüleri yakalıyor.\
-   Hibrit yaklaşım (kural + ML) en etkili çözüm.

------------------------------------------------------------------------


## Ek --- Örnek JSON

``` json
{
  "energy": 19.6,
  "duration": 3600,
  "hour": 14,
  "temperature": 25,
  "vehicle_age": 2
}
```
