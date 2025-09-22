# ⚡ Elektrikli Şarj İstasyonlarının Bilgi Güvenliği  

 Bu proje, **elektrikli şarj istasyonları** için geliştirilen bir **telemetri toplama, güvenlik analizi ve anomali tespit sistemi**dir.  
Amaç: **Endüstri standartlarının ötesinde güvenlik** sağlamak, olası saldırılara karşı sistemi korumak ve operatörlerin gerçek zamanlı olarak istasyonları yönetmesini kolaylaştırmaktır.  

---

## 🎯 Proje Kapsamı  

-  **Telemetri Toplama:** ESP üzerinden enerji, süre, voltaj ve akım verilerinin backend’e aktarımı.  
-  **Makine Öğrenmesi ile Anomali Tespit:** Isolation Forest & Logistic Regression modelleriyle karşılaştırmalı analiz.  
-  **Operatör Paneli:** Gerçek zamanlı izleme, alarm ekranı ve seans yönetimi.  
-  **Güvenlik Sertleştirme:** Replay saldırı koruması, rate limiting, girdi doğrulama, planlı TLS & JWT entegrasyonu.  
-  **Standartlar & Uyum:** ISO 27001, IEC 62443 ve OCPP Security Profiles gözetilerek tasarım.  

---

## 🚀 Kurulum  

```bash
git clone https://github.com/Adileakklc/Elektrikli-sarj-istasyon.git
cd Elektrikli-sarj-istasyon
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Çalıştırma  

```bash
python app.py
```

- Backend varsayılan olarak **http://localhost:5000** üzerinde çalışır.  
- Operatör Paneli ve API sayfaları buradan erişilebilir.  

---

## 🔌 API Uçları  

| Metot | Endpoint                | Açıklama |
|-------|-------------------------|----------|
| `POST` | `/telemetry`            | Telemetri kaydı + risk skoru döndürür |
| `POST` | `/ml`                   | Anomali tespiti için ML model skorlaması |
| `GET`  | `/sessions?limit=N`     | Son N seansı listeler |
| `POST` | `/sessions/{id}/stop`   | Belirli bir seansı durdurur (simülasyon amaçlı) |

---

## 📊 Makine Öğrenmesi Sonuçları  

| Model              | Doğruluk | Precision | Recall | F1 |
|--------------------|----------|-----------|--------|----|
| **Isolation Forest** | 1.00     | 1.00      | 1.00   | 1.00 |
| Logistic Regression | 0.742    | 0.719     | 0.982  | 0.83 |

📈 Görselleştirilmiş sonuçlar için → [ml.md](docs/ml.md)  

---

## 🖥️ Operatör Paneli  

Operatör paneli üzerinden:  

- 📊 **Ana Sayfa:** Tüm şarj istasyonlarının genel durumu  
- 🚨 **Alarm Ekranı:** Tespit edilen anormallikler ve uyarılar  

🔗 [Paneli Görüntüle](panel.html)  

---

## 🔒 Güvenlik Sertleştirme  

- HMAC + Nonce → Replay saldırılarına karşı koruma  
- Rate Limiting → DoS saldırılarını azaltma  
- Girdi Doğrulama → Veritabanı ve ML modelini koruma  

Detaylı bilgi → [sertlestirme.md](docs/sertlestirme.md)  

---

## 📚 Standartlar ve Uyum  

- **ISO 27001**: Bilgi güvenliği yönetim sistemi  
- **IEC 62443**: Endüstriyel otomasyon güvenliği  
- **OCPP Security Profiles**: Şarj istasyonu protokol güvenliği  

🔗 [Standartlar Kaynağı](kaynakca/standartlar-kaynakca.md)  

---

## 🧠 Modeller  

Makine öğrenmesi modelleri `./models/` klasöründe tutulur:  

- `scaler.pkl`  
- `iso.pkl`  

---

## 📑 Rapor ve Kaynakça  

- 📘 [Proje Raporu](docs/proje-raporu.md)  
- 📖 Kaynakçalar:  
  - [Saldırı Vakaları](kaynakca/saldiri-vakalari-kaynakca.md)  
  - [Standartlar](kaynakca/standartlar-kaynakca.md)  
  - [Yasal Uyum](kaynakca/yasal-uyum-kaynakca.md)  

---

