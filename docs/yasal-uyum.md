## KVKK (Kişisel Verilerin Korunması Kanunu)

**Tanım:**  
6698 sayılı KVKK, Türkiye’de kişisel verilerin işlenmesini düzenleyen temel kanundur. Amaç, kişisel verilerin işlenmesinde bireylerin temel hak ve özgürlüklerini korumak ve veri işleyen kurumlara (veri sorumlularına) sorumluluklar getirmektir.  

**Şarj istasyonu özelinde etkisi:**  
- Şarj oturum verileri (kullanıcı kimliği, ödeme bilgileri, şarj süresi, lokasyon) **kişisel veri** sayılır.  
- Bu veriler, **açık rıza** olmadan toplanamaz veya işlenemez.  
- Kullanıcılar, KVKK kapsamında verilerini görme, silme ve düzelttirme hakkına sahiptir.  
- Backend tarafında veri güvenliği yükümlülüğü gereği şifreleme (TLS, AES) ve erişim kontrolü uygulanmalıdır.  

**Çözüm/Öneriler:**  
- Sistemde yalnızca gerekli olan minimum veri toplanmalı (**veri minimizasyonu**).  
- Kullanıcıdan açık rıza alındığına dair kayıt tutulmalı.  
- Loglama ve veritabanı süreçlerinde “veriyi silme” ve “düzeltme” hakları teknik olarak desteklenmeli.  
- Verilerin yurt dışına aktarımı gerekiyorsa KVKK Kurulu’nun onayı alınmalıdır.  

## GDPR (General Data Protection Regulation)

**Tanım:**  
GDPR, Avrupa Birliği’nin 2018’de yürürlüğe giren Genel Veri Koruma Tüzüğü’dür. Amacı, bireylerin kişisel verilerinin toplanması, işlenmesi ve saklanmasında yüksek standartlarda gizlilik ve güvenlik sağlamaktır. Türkiye’de doğrudan bağlayıcı değildir; ancak AB ile iş yapan şirketler ve AB vatandaşlarının verisini işleyen sistemler için uyumluluk zorunludur.  

**Şarj istasyonu özelinde etkisi:**  
- Backend tarafında “privacy by design” ilkesiyle, sistem en baştan gizlilik gözetilerek tasarlanmalıdır. Örneğin, şarj oturum verileri anonimleştirilmeli ve yalnızca gerekli olan bilgiler saklanmalıdır.  
- Eğer şarj istasyonu sisteminde bir **veri ihlali** (ör. kullanıcı bilgilerinin sızdırılması) yaşanırsa, GDPR gereği 72 saat içinde ilgili otoritelere bildirim yapılmalıdır.  
- Kullanıcıların verilerini silme, taşıma veya görme hakkı vardır; backend bu talepleri teknik olarak desteklemelidir.  
- Kullanıcı verileri AB dışına aktarılacaksa (ör. Türkiye’deki bir sistemden Avrupa’daki bir merkeze), ek güvenlik önlemleri alınmalı ve gerekli yasal onaylar sağlanmalıdır.  

**Çözüm/Öneriler:**  
- Backend mimarisi “privacy by design” prensibine göre geliştirilmeli.  
- Kullanıcı arayüzünde verilerin hangi amaçlarla işlendiği şeffaf şekilde açıklanmalı.  
- Loglama sisteminde veri ihlali izleme ve hızlı raporlama mekanizmaları bulunmalı.  
- AB ile veri paylaşımı yapılacaksa, şifreleme ve güvenli kanal (TLS) kullanımı zorunlu olmalı.  

## eIDAS (Electronic Identification, Authentication and Trust Services)

**Tanım:**  
eIDAS, Avrupa Birliği’nin 2016’da yürürlüğe giren elektronik kimlik, kimlik doğrulama ve güven hizmetleriyle ilgili düzenlemesidir. Amaç, Avrupa genelinde güvenli elektronik işlemleri mümkün kılmak, dijital imza ve elektronik kimliklerin yasal geçerliliğini sağlamaktır.  

**Şarj istasyonu özelinde etkisi:**  
- Kullanıcıların şarj istasyonu uygulamalarına girişinde elektronik kimlik doğrulama yöntemleri (örneğin dijital sertifika, mobil kimlik) kullanılabilir.  
- eIDAS kapsamında güvenli e-imza, Avrupa genelinde yasal olarak geçerli olduğundan, şarj sözleşmeleri veya ödeme onayları dijital ortamda geçerli hale getirilebilir.  
- Sertifika sağlayıcıların yetkilendirilmiş olması gerekir; aksi takdirde elektronik kimlik veya imza yasal kabul edilmez. Bu, backend tarafında kullanılan sertifikaların güvenilir otoritelerden alınmasını zorunlu kılar.  

**Çözüm/Öneriler:**  
- Elektronik kimlik doğrulama süreçleri (örn. kullanıcı girişinde çift faktörlü doğrulama + sertifika kontrolü) uygulanmalı.  
- Backend tarafında kullanılan SSL/TLS sertifikaları, eIDAS kapsamında tanınan güven hizmet sağlayıcılarından alınmalı.  
- Ödeme ve oturum onayları için güvenli e-imza desteği entegrasyonu sağlanabilir.  
- Avrupa Birliği ile entegre olacak sistemlerde eIDAS uyumlu çözümler kullanmak yasal geçerliliği garanti eder.  
