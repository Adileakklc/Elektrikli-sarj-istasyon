# Uluslararası Güvenlik Standartları

## ISO 27001

- **Kapsam/Amaç:**  
ISO 27001, bir kuruluşun bilgi varlıklarını gizlilik, bütünlük ve erişilebilirlik (CIA) ilkelerine göre korumayı hedefleyen uluslararası bir Bilgi Güvenliği Yönetim Sistemi (BGYS) standardıdır. Amaç sadece teknik önlem değil, aynı zamanda risk temelli yönetim yaklaşımı geliştirmektir.

- **Uygulanabilir Maddeler (şarj istasyonu için):**
  - **Veri Koruma:** Kullanıcı kimlikleri, ödeme verileri ve şarj oturum bilgileri kişisel veri sayılır. Bu verilerin şifrelenmesi (AES/TLS) ve yalnızca yetkili kişilerce erişilebilir olması gerekir.  
  - **Erişim Kontrolü:** Her bileşene (istasyon, backend, operatör) rol bazlı erişim tanımlanmalı.  
  - **Loglama ve İzlenebilirlik:** Her şarj oturumu, ödeme işlemi ve firmware güncellemesi kaydedilmeli. Olay kayıtları hem hata çözümü hem de yasal uyum için saklanmalı.  
  - **Süreklilik ve Risk Yönetimi:** Olası DoS saldırısı veya bağlantı kesintisinde sistemin yeniden ayağa kalkabilmesi için iş sürekliliği planı bulunmalı.  
  - **Yama Yönetimi:** İstasyon yazılımları ve backend düzenli olarak güncellenmeli, güncellemeler doğrulanarak uygulanmalı.  

- **Projeye Etkisi:**
  - **ESP8266 tarafı:** Backend ile TLS üzerinden güvenli bağlantı kuracak, her mesaj nonce ve timestamp içerecek.  
  - **Backend tarafı:** Kullanıcı verileri GDPR/KVKK uyumlu saklanacak, loglar düzenli tutulacak.  
  - **Yönetimsel Katman:** Trello veya raporda risk analizleri, olay kaydı ve güncelleme süreçleri belgelenerek ISO 27001 mantığına uygun bir yönetim süreci gösterilecek.  

---
## IEC 62443

Şarj istasyonları her ne kadar günlük kullanım için tasarlanmış cihazlar olsa da, aslında birer endüstriyel kontrol sistemi (ICS) gibi çalışırlar. Bu yüzden yaptığım araştırmalarda IEC 62443 standardının doğrudan bu alana uygulanabileceğini gördüm. IEC 62443, endüstriyel sistemlerde siber güvenliği tanımlayan en kapsamlı standartlardan biri ve amacı, tek bir cihazın hacklenmesinin tüm sistemi etkilemesini engellemektir. Standart bu yaklaşımı “katmanlı güvenlik” (defense-in-depth) ve “zonlar & conduits” kavramlarıyla ortaya koyar.  

- **Kapsam/Amaç:**  
IEC 62443, özellikle endüstriyel otomasyon ve kontrol sistemlerinde cihaz, ağ ve yazılım güvenliğini sağlamayı amaçlar. Standardın temel hedefi, kritik altyapıların siber saldırılara karşı dirençli hale gelmesidir.  

- **Uygulanabilir Maddeler (şarj istasyonu için):**
  - **Rol Bazlı Erişim:** Farklı kullanıcı rolleri (admin, operatör, son kullanıcı) belirlenmeli ve yetkiler buna göre ayrılmalıdır.  
  - **Sertifika Tabanlı Kimlik Doğrulama:** Şarj istasyonu ve backend arasındaki iletişimde karşılıklı sertifikalar kullanılmalı.  
  - **Patch Management:** Firmware ve yazılım güncellemeleri düzenli aralıklarla yapılmalı, güncellemeler doğrulanarak sisteme uygulanmalı.  
- **Ağ Güvenliği:**
  - **Zonlar:** Şarj istasyonu, backend ve ödeme sistemleri ayrı ağ segmentlerinde konumlandırılmalı.  
  - **Conduits:** Bu zonlar arasındaki veri iletişimi TLS gibi güvenli kanallar üzerinden sağlanmalı.  
- **Katmanlı Güvenlik:**
  - Tek bir korumaya güvenmek yerine; TLS, rol bazlı erişim, loglama ve IDS/IPS gibi çoklu mekanizmalar birlikte kullanılmalı.  

- **Projeye Etkisi:**
  - **ESP8266 tarafı:** Backend ile TLS üzerinden haberleşirken backend sertifikasını doğrulayacak.  
  - **Backend tarafı:** Kullanıcı rolleri (ör. admin/operatör) tanımlanacak ve loglama sistemi bu rollere göre detaylı olacak.  
  - **Genel Sistem:** Backend, ödeme sistemi ve cihazlar ağda ayrı zonlarda düşünülerek, saldırının tüm sisteme yayılması engellenecek.  

Araştırmalarım sonucunda IEC 62443’ün sadece bir güvenlik çerçevesi değil, aynı zamanda şarj istasyonları gibi cihazlar için uygulanabilir bir “savunma mimarisi” sunduğunu gördüm. Bu standart, projemde cihazın hem donanım hem de ağ düzeyinde korunmasını sağlayacak kritik prensipler içeriyor.

---
## OCPP Security Profiles

Yaptığım araştırmalarda gördüm ki, elektrikli araç şarj istasyonları ile merkezi sistemler arasındaki iletişimde en yaygın kullanılan protokol OCPP (Open Charge Point Protocol). Bu protokol, istasyon ile backend arasındaki tüm haberleşmenin nasıl yapılacağını tanımlıyor. Ancak güvenlik konusu OCPP’nin kendi içinde “Security Profiles” adı verilen seviyelerle belirlenmiş durumda. Şarj istasyonlarının saldırılara karşı dayanıklı olabilmesi için bu profillerin doğru uygulanması kritik önem taşıyor.  

- **Kapsam/Amaç:**  
OCPP Security Profiles, şarj istasyonu ile merkezi sistem arasında iletilen mesajların güvenliğini sağlar. Burada asıl hedef, mesajların gizliliğini, bütünlüğünü ve doğruluğunu korumaktır.  

- **Profil Seviyeleri:**
  - **Profile 1:** Güvenliksiz seviye; iletişim plain WebSocket üzerinden yapılır, TLS kullanılmaz. Bu durum MITM ve replay saldırılarına açık bir yapı oluşturur.  
  - **Profile 2:** TLS kullanımı ile birlikte backend’in sertifikayla doğrulanması sağlanır. Böylece istasyon, yalnızca güvenilir bir sunucuya bağlanır.  
  - **Profile 3:** En güçlü güvenlik seviyesi; TLS’ye ek olarak karşılıklı kimlik doğrulama (mutual authentication) vardır. Hem istasyon hem de backend birbirini sertifika ile doğrular.  

- **Ek Güvenlik Mekanizmaları:**
  - **Nonce ve Timestamp:** Mesajların tekrar kullanılmasını (replay attack) engellemek için her iletişimde benzersiz bir nonce ve zaman damgası bulunur.  
  - **Hash Doğrulaması:** Mesajın bütünlüğünü garanti altına almak için hash kontrolü yapılır.  

- **Projeye Etkisi:**
  - **ESP8266 tarafı:** Flask backend’e TLS üzerinden bağlanacak. Her gönderilen JSON mesajı nonce, timestamp ve hash içerecek.  
  - **Backend tarafı:** Sunucu, gelen verinin hash doğrulamasını yapacak ve nonce’un tekrar edilmediğini kontrol edecek.  
  - **Genel Sistem:** Projede Profile 2 veya tercihen Profile 3 mantığı uygulanarak, istasyon–backend iletişimi gerçek bir şarj protokolü güvenliğiyle simüle edilecek.  

Bu araştırmadan çıkan sonuç, OCPP Security Profiles’ın aslında şarj istasyonu güvenliği için “uygulanabilir en pratik çerçeve” olduğu. Özellikle Profile 3’ün kullanılmasıyla, sadece güvenli bir bağlantı kurmakla kalınmıyor, aynı zamanda karşılıklı kimlik doğrulamasıyla istasyon ve backend arasındaki güven en üst seviyeye çıkarılıyor. Projemde de ESP8266 ile Flask backend arasındaki iletişimde bu profil mantığını taklit ederek, gerçek dünyadaki güvenlik standartlarını yakalamak mümkün olacak.
