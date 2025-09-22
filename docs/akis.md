---
layout: page
title: Sistem Akış Diyagramı
---

#  Sistem Akış Diyagramı

Bu bölümde, ESP32 cihazından gelen verilerin sistemde nasıl işlendiği adım adım açıklanmaktadır.

## Akış Adımları

1. **ESP32 → Flask API**  
   - Cihaz, ölçüm verilerini şu formatta gönderir:  
     ```json
     {
       "userId": "...",
       "enerji": ...,
       "sure": ...,
       "voltaj": ...,
       "akim": ...,
       "timestamp": "...",
       "nonce": "...",
       "hash": "..."
     }
     ```

2. **API (Flask)**  
   - TLS sonrası HMAC doğrulaması yapılır.  
   - İmza yanlışsa **401 Unauthorized** döner.  

3. **Rate/Replay Kontrolü**  
   - Son 5 saniyede 3’ten fazla istek → **429 Too Many Requests**  
   - Nonce tekrar kullanılırsa → **409 Conflict (Replay Detected)**  

4. **Kural Motoru (Rule Engine)**  
   - Enerji (0–200 kWh), süre (0–86400 sn) aralığı kontrol edilir.  
   - Enerji/dakika oranı (≤2 kWh/dk) sınırı kontrol edilir.  
   - Hatalı durumda → **400 Bad Request**  

5. **Veritabanı (DB)**  
   - Geçerli veriler `telemetry` tablosuna eklenir.  
   - Sistem `row_id` değerini döner.  

6. **Özellik Çıkarımı (Feature Extraction)**  
   - Telemetry verisinden şu özellikler hesaplanır:  
     - `duration_min`  
     - `energy_per_min`  
     - `hour`  
     - `temperature`  
     - `vehicle_age`  

7. **Makine Öğrenmesi (ML Service)**  
   - IsolationForest modeli ile risk skoru hesaplanır:  
     - **Skor < 0** → Normal  
     - **Skor ≥ 0** → Anomali  

8. **API Yanıtı (ESP32’ye dönüş)**  
   - Cihaza şu formatta yanıt gönderilir:  
     ```json
     {
       "status": "ok",
       "id": 42,
       "riskScore": -0.025
     }
     ```

9. **Web Panel Güncellemesi**  
   - Aktif seanslar listelenir.  
   - Her seans için risk rozeti gösterilir (Düşük / Orta / Yüksek).  
   - “Seansı Durdur” butonu ile API’ye çağrı yapılabilir.  

---

📌 Bu akış sayesinde her bir telemetry kaydı, güvenlik doğrulamaları ve ML analizi sonrasında operatör paneline yansıtılır.
