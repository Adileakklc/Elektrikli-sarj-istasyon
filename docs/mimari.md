---
layout: page
title: Sistem Mimarisi
---

# 3.1 Sistem Mimarisi

Bu bölümde elektrikli şarj istasyonlarının güvenliği için tasarlanan sistemin mimari yapısı özetlenmiştir. Sistem; cihaz tarafı (ESP32), ağ katmanı, backend (sunucu tarafı), makine öğrenmesi servisi ve operatör paneli olmak üzere beş ana bileşenden oluşmaktadır.

## Bileşenler

- **Cihaz (ESP32)**  
  - Enerji (kWh), süre (s), voltaj (V) ve akım (A) ölçümlerini toplar  
  - Nonce (tek seferlik sayı) üretir  
  - HMAC (hash tabanlı imza) ile veriyi imzalar ve API’ye gönderir  

- **Ağ Katmanı (Wi-Fi / LAN)**  
  - Telemetry verilerinin taşındığı kanal  
  - Man-in-the-Middle (MITM) ve Replay saldırılarına açıktır  

- **Backend (Flask API)**  
  - `/telemetry` → Telemetry verilerini alır  
  - `/ml` → Makine öğrenmesi risk skoru döner  
  - RateLimit + Replay Guard:  
    - Aynı nonce tekrar kullanıldığında isteği reddeder (409)  
    - 5 saniye içinde 3’ten fazla istek olursa engeller (429)  
  - Kural Motoru:  
    - Süre, enerji ve enerji/dakika sınırlarını kontrol eder  
    - Mantıksal kontroller yapar  
  - Veritabanı:  
    - Telemetry kayıtlarını SQLite / PostgreSQL üzerinde saklar  
  - Loglama:  
    - Flask erişim logları ve hata kayıtları tutulur  

- **Makine Öğrenmesi Servisi**  
  - Özellik çıkarımı yapar:  
    - `duration_min`, `energy_per_min`, `hour`, `temperature`, `vehicle_age`  
  - IsolationForest modeli (iso.pkl + scaler.pkl) ile risk skoru hesaplar  
  - Risk skoru:  
    - Negatif değer → Normal  
    - Pozitif değer → Anomali  

- **Operatör Paneli (Web Panel)**  
  - HTML/JS tabanlı basit bir arayüz  
  - Aktif seansları listeler  
  - Her seans için risk skorunu rozet şeklinde gösterir  
  - “Seansı Durdur” butonu ile backend’e API çağrısı yapar  

---

# 3.2 Veri Akışı

1. **ESP32 → API**: Cihaz, ölçtüğü verileri `{userId, enerji, süre, voltaj, akım, timestamp, nonce, hash}` formatında gönderir.  
2. **API**: TLS sonrası HMAC doğrulaması yapar. Yanlışsa 401 döner.  
3. **Rate/Replay Guard**:  
   - Nonce tekrar kullanılırsa 409 döner  
   - Çok sık istek gelirse 429 döner  
4. **Kural Motoru**: Enerji ve süre limitleri kontrol edilir. Hatalı ise 400 döner.  
5. **Veritabanı**: Telemetry verisi saklanır, `row_id` döner.  
6. **Özellik Çıkarımı**: `duration_min`, `energy_per_min`, `hour`, `temperature`, `vehicle_age` hesaplanır.  
7. **ML Servisi**: IsolationForest modeli risk skorunu üretir.  
8. **API → Cihaz**: `{status:ok, id, riskScore}` yanıtı döner.  
9. **API → Web Panel**: Aktif seanslar ve risk rozetleri güncellenir.  

---

📌 Bu yapı sayesinde sistem, hem kural tabanlı hem de makine öğrenmesine dayalı anomali tespit mekanizmaları ile güvenliği artırır.
