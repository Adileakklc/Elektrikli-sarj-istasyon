# Saldırı Türleri ve Vaka Analizleri

## MITM (Man-in-the-Middle)

**Tanım:**  
Man-in-the-Middle (MITM) saldırısı, iki taraf arasındaki iletişim hattına gizlice girerek verilerin okunması, değiştirilmesi veya sahte verilerin enjekte edilmesiyle gerçekleşir. Kullanıcı ile sunucu arasında güvenli olmayan ya da zayıf şifrelenmiş bir bağlantı varsa, saldırgan araya girip tüm trafiği kontrol edebilir. Bu tür saldırılarla kimlik bilgileri, şifreler veya finansal veriler çalınabilir. (Kaynak: Berqnet, Imperva, Wiley)

**Şarj istasyonu özelinde etkisi:**  
Elektrikli araç şarj istasyonlarında MITM saldırısı, istasyon ile merkezi yönetim sistemi (backend) arasındaki iletişimde ciddi riskler yaratır. Örneğin, ödeme bilgilerinin iletilmesi sırasında saldırgan mesajı manipüle ederek farklı bir ücret yansıtabilir, kullanıcı kimlik bilgilerini çalabilir ya da şarj oturumlarını değiştirebilir. Beefull’un belirttiği gibi bu tür saldırılar, hizmetin kesilmesine ve istasyonun kullanıcılar için güvenilirliğini kaybetmesine yol açabilir. 

**Çözüm önerisi:**  
MITM’e karşı en önemli önlem, güçlü şifreleme ve kimlik doğrulama mekanizmalarının kullanılmasıdır. Tüm iletişim TLS/SSL protokolleri üzerinden yapılmalı ve sertifikaların doğruluğu mutlaka kontrol edilmelidir. Ayrıca mesajların bütünlüğünü sağlamak için hash algoritmaları ve dijital imzalar kullanılmalı, loglama ve izleme mekanizmalarıyla olağandışı davranışlar tespit edilmelidir. (Kaynak: Berqnet, Imperva, Beefull)

## Replay Attack

**Tanım:**
Replay Attack, daha önce geçerli şekilde gönderilmiş bir veri paketinin saldırgan tarafından yakalanıp tekrar gönderilmesiyle yapılan saldırı türüdür. Bu yöntemle sistem, eski mesajı yeniymiş gibi algılar ve tekrar işler. Saldırgan bu sayede kullanıcı kimlik doğrulama bilgilerini ya da ödeme işlemlerini yeniden kullanabilir. (Kaynak: Kaspersky, Sangfor)

**Şarj istasyonu özelinde etkisi:**
Elektrikli araç şarj istasyonlarında replay saldırısı, özellikle ödeme ve kimlik doğrulama süreçlerinde ciddi riskler taşır. Örneğin, bir kullanıcının başarılı ödeme mesajı saldırgan tarafından kaydedilirse, bu mesaj yeniden backend’e gönderilerek kullanıcı farkında olmadan ekstra oturum açtırılabilir. Bu durum hem kullanıcıya maddi kayıp yaşatır hem de sistemin güvenilirliğini zedeler.

**Çözüm önerisi:**
Replay saldırılarını önlemek için her mesaj benzersiz bir nonce (tek kullanımlık rastgele sayı) ve timestamp (zaman damgası) içermelidir. Backend tarafı, aynı nonce değerinin tekrar kullanılmasına izin vermemeli ve zaman sınırını kontrol etmelidir. Ayrıca TLS/SSL ile şifreleme, saldırganın mesajı ele geçirip yeniden kullanmasını zorlaştırır. (Kaynak: Kaspersky, Sangfor)

## DoS (Denial of Service)

**Tanım:**
DoS (Denial of Service) saldırısı, bir sistemin kaynaklarını aşırı yükleyerek gerçek kullanıcıların hizmet almasını engellemeye yönelik bir saldırı türüdür. Bu saldırı genellikle yoğun istek (trafik) gönderilerek yapılır. Dağıtık versiyonu olan DDoS’ta ise birçok farklı cihaz aynı anda saldırıyı gerçekleştirir ve sistem çok kısa sürede cevap veremez hale gelir. (Kaynak: Bulutistan, Berqnet)

**Şarj istasyonu özelinde etkisi:**
Elektrikli araç şarj istasyonlarında DoS saldırısı, istasyona veya merkezi yönetim sistemine aşırı sayıda sahte bağlantı isteği gönderilmesiyle gerçekleşebilir. Bu durumda şarj oturumları işlenemez, ödeme sistemleri devre dışı kalabilir ve kullanıcılar araçlarını şarj edemez. Cbernet’in de belirttiği gibi bu saldırılar, yalnızca kullanıcı memnuniyetini etkilemekle kalmaz, aynı zamanda enerji altyapısının istikrarını da tehdit eder.

**Çözüm önerisi:**
DoS/DDoS saldırılarını önlemek için öncelikle rate limiting (belirli süre içinde sınırlı sayıda istek kabul etme) uygulanmalıdır. Ayrıca güvenlik duvarları (firewall), IDS/IPS sistemleri ve trafik filtreleme yöntemleriyle sahte istekler ayıklanabilir. Yük dengeleme (load balancing) ile sistem kapasitesi dağıtılarak saldırının etkisi azaltılabilir. Düzenli log analizi ve anomali tespiti de saldırının erken fark edilmesini sağlar. (Kaynak: Bulutistan, Berqnet, Cbernet)

## Vakalar
### Tesla Vakası

**Tanım:**
2018’de güvenlik araştırmacıları Tesla Model S’in kablosuz anahtar sisteminde ciddi bir açık keşfettiler. Anahtarlık tarafından gönderilen sinyaller kaydedilip tekrar oynatılarak (replay/relay attack) araç açılabildi. Daha güncel olarak, 2024’te araştırmacılar Tesla’nın kablosuz anahtar ve Wi-Fi bağlantısındaki açıkları kullanarak araçları 90 saniyede hackleyebildiklerini gösterdiler. (Kaynak: BusinessInsider, İKÜ BGYS Haber)

**Etki:**
Araç sahiplerinin izinsiz erişim riski ortaya çıktı. Bu durum, elektrikli araçların güvenlik açığı nedeniyle kolayca çalınabileceğini gösterdi ve markanın güvenilirliğini sorgulattı.

**Alınan Önlem:**
Tesla, yazılım güncellemeleriyle anahtar sistemini güçlendirdi, daha güvenli algoritmalar kullandı ve “PIN-to-Drive” gibi ek güvenlik önlemleri sundu. Şarj istasyonları için buradan çıkarılacak ders, kimlik doğrulama ve ödeme mesajlarında replay saldırılarını engellemek için nonce ve timestamp kullanılmasının şart olmasıdır.

### Rusya Şarj İstasyonu Hack Olayı

**Tanım:**
2022’de Rusya’daki elektrikli araç şarj istasyonları hacklendi ve ekranlarda propaganda mesajları yayınlandı. Saldırganlar istasyonların yönetim yazılımına yetkisiz erişim sağladı. (Kaynak: ShiftDelete)

**Etki:**
Şarj hizmeti kesintiye uğradı, kullanıcılar araçlarını şarj edemedi ve istasyonlar belirli süre boyunca işlevsiz hale geldi. Bu olay, şarj altyapısının siber saldırılarla nasıl felç edilebileceğini ortaya koydu.

**Alınan Önlem:**
Olaydan sonra altyapı sağlayıcıları güvenlik yamaları yayınladı. Ağ segmentasyonu ve güçlü kimlik doğrulama ihtiyacının önemi bir kez daha vurgulandı.

### Choicejacking (USB Şarj İstasyonları Üzerinden Veri Hırsızlığı)

**Tanım:**
“Juice jacking” veya “choicejacking” olarak bilinen bu saldırıda, halka açık USB şarj istasyonları kullanılarak cihazlara kötü amaçlı yazılım yüklenir veya veriler çalınır. Kullanıcı cihazını şarj etmek isterken aslında veri hırsızlığına maruz kalabilir. (Kaynak: BilgiGüvende)

**Etki:**
Kullanıcıların kişisel verileri ve kimlik bilgileri ele geçirilebilir. Bu saldırı özellikle halka açık alanlardaki USB şarj istasyonlarını kullananlar için büyük bir risk oluşturur.

**Çözüm/Öneri:**
Kamuya açık USB şarj noktalarının kullanılmaması, bunun yerine kişisel adaptör veya “USB data blocker” cihazları tercih edilmesi önerilir. Elektrikli araç şarj istasyonları için ders, iletişim portlarının da potansiyel saldırı yüzeyi olduğu ve korunması gerektiğidir.