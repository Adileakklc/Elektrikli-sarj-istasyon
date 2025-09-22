# Güvenlik Sertleştirme Notları 

Bu doküman, projede **uygulanan** ve **planlanan** sertleştirme adımlarını tek yerde toplar.  
Amaç: elektrikli şarj istasyonu güvenlik mimarisini **endüstri standardı ötesine** taşımak.

---

## Uygulananlar (mevcut güçlü adımlar)

- **HMAC + Nonce (Replay Koruması):**  
  `/telemetry` istekleri imzalanıyor, `nonce` tekilliği ile tekrar saldırıları (replay) otomatik reddediliyor (`409 Conflict`).  
  → Bu sayede mesaj bütünlüğü korunuyor, sahte veri enjeksiyon riski neredeyse sıfırlandı.

- **Rate Limit:**  
  Kullanıcı başına 5 saniyede 3’ten fazla istek reddediliyor (`429 Too Many Requests`).  
  → DoS saldırılarına karşı ilk savunma hattı kuruldu.

- **Girdi Doğrulama Kuralları:**  
  Enerji, süre, voltaj ve akım değerleri için limit ve format kontrolleri.  
  → Hem veritabanı hem de ML modelleri kirli verilerden korunuyor.

---

##  Planlananlar (üst seviye hedefler)

- **TLS + HSTS:**  
  Tüm endpoint’lerde HTTPS zorunlu hale getirilecek.  
  `Strict-Transport-Security` başlığı ile downgrade saldırılarına karşı ek güvenlik katmanı sağlanacak.  
  → İletişim kanallarının bütünlüğü ve gizliliği garanti altına alınacak.

- **API Key / JWT:**  
  Operatör paneli ve yönetim endpoint’lerinde **kısa ömürlü JWT** tabanlı yetkilendirme kullanılacak.  
  → Rol bazlı erişim (RBAC) sayesinde yalnızca yetkili kullanıcılar kritik uçlara erişebilecek.

- **Ek Rate Limit & IP Bazlı Koruma:**  
  Özellikle `/ml` ve `/sessions` uçlarında daha sıkı oran sınırları uygulanacak.  
  → Şüpheli IP adresleri için dinamik sınırlama devreye alınarak hizmet sürekliliği korunacak.

- **CORS Daraltma:**  
  Sadece güvenilir origin’lere izin verilecek, wildcard `*` politikası tamamen kaldırılacak.  
  → Yetkisiz alan adlarından gelen istekler engellenecek.

- **Content Security Policy (CSP):**  
  Panel için katı `script-src` ve `object-src` politikaları uygulanacak.  
  → XSS risk yüzeyi asgari seviyeye indirilecek.

---

## İleri Seviye Yol Haritası

Mevcut uygulamalar güvenlik açısından güçlü bir temel oluşturdu. Bundan sonraki aşamalar ise bu yapıyı daha da ileri taşıyacak stratejik adımlardan oluşmaktadır:

- **Gelişmiş İmza Mekanizması:**  
  Telemetri verilerinin yalnızca imzalanması değil, deterministik bir “telemetry zarfı” ile mühürlenmesi planlanmaktadır.  
  → Böylece mesaj bütünlüğü ve anahtar rotasyonu daha güvenli hale getirilecektir.

- **Uyarlanabilir Savunma:**  
  Saldırıların yalnızca engellenmesi değil, davranışa göre sistemin kendini ayarlaması sağlanacaktır.  
  → Örneğin şüpheli IP adresleri geciktirilerek (tarpit) saldırgan yıpratılacak, meşru kullanıcılar etkilenmeyecektir.

- **Risk Skoru Tabanlı Operasyon:**  
  Makine öğrenmesi tarafından üretilen risk skorları yalnızca bilgi amaçlı değil, operasyonel karar mekanizmasına entegre edilecektir.  
  → Yüksek riskli oturumlar için panelde uyarı rozetleri gösterilecek, kritik eşiklerde oturumlar otomatik sonlandırılabilecektir.

- **Denetim ve İzlenebilirlik:**  
  Kritik operasyonel adımlar hash zinciri ile mühürlenecek, böylece log kayıtlarının tahrif edilmesi engellenecektir.  
  → Bu yaklaşım, güvenlik denetimleri ve düzenleyici incelemeler için güçlü bir kanıt sağlayacaktır.

- **Kademeli mTLS Geçişi:**  
  Tüm cihazlarda bir anda zorunlu hale getirmek yerine, seçili cihaz grubunda mTLS kademeli olarak devreye alınacaktır.  
  → Böylece işletim riskleri azaltılarak geleceğe hazır bir altyapı sağlanacaktır.

---

##  Genel Değerlendirme

Bugün itibarıyla sistem; replay, DoS ve veri bütünlüğü risklerini başarıyla bertaraf edecek şekilde güçlendirilmiştir.  
Gelecek adımlar ise yalnızca güvenliği korumakla kalmayacak, aynı zamanda projeyi **örnek gösterilecek bir güvenlik mimarisi** seviyesine çıkaracaktır.
