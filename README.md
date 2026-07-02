# DarqMSG

> Telegram kanallarına otomatik mesaj ve reklam paylaşımı için geliştirilmiş bir masaüstü aracı.

## 📌 Hakkında

**DarqMSG**, belirlenen Telegram kanal ID'lerine belirli zaman aralıklarıyla mesaj göndermek amacıyla geliştirilmiş bir otomasyon uygulamasıdır.

Uygulama iki farklı paylaşım yöntemi sunar:

* 📨 Mevcut bir Telegram mesajını **Forward (İlet)** ederek paylaşma.
* 📝 Kullanıcının hazırladığı dahili metin dosyasındaki mesajları doğrudan gönderme.

Böylece çok sayıda Telegram kanalında düzenli ve otomatik içerik paylaşımı yapılabilir.

---

## ✨ Özellikler

* Forward mesaj gönderimi
* Metin dosyasından mesaj paylaşımı
* Birden fazla kanal desteği
* Kanal ID listesi ile çalışma
* Gönderimler arasında ayarlanabilir bekleme süresi
* Asenkron çalışma yapısı
* Renkli terminal arayüzü (Rich)
* Hata yakalama ve loglama
* FloodWait yönetimi
* Kullanıcı dostu konsol arayüzü

---

## ⚙️ Gereksinimler

* Python 3.10+
* Telegram API ID
* Telegram API Hash

Gerekli paketleri yüklemek için:

```bash
pip install -r requirements.txt
```

---

## 🚀 Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/kullaniciadi/DarqMSG.git
cd DarqMSG
```

Ardından gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

Programı çalıştırın:

```bash
python main.py
```

---

## 📂 Çalışma Mantığı

### 1. Forward Modu

Bu modda kullanıcı;

* Kaynak mesajın bulunduğu sohbeti,
* Mesaj ID'sini,
* Hedef kanal ID'lerini

belirler.

Program belirtilen mesajı hedef kanallara belirlenen süre aralıklarıyla iletir.

---

### 2. Metin Gönderme Modu

Bu modda kullanıcı;

* Bir mesaj dosyası oluşturur,
* Gönderim aralığını belirler,
* Hedef kanal listesini girer.

Program dosya içerisindeki mesajı belirlenen tüm kanallara otomatik olarak gönderir.

---

## 📁 Proje Yapısı

```
DarqMSG/
│
├── automessage.py
├── requirements.txt
├── README.md
├── mesaj.txt
├── log.txt
├── id.txt
├── errors.txt
├── session_auto_post.session
└── @darqsoft
```

---

## 🛡️ Hata Yönetimi

DarqMSG aşağıdaki durumları otomatik olarak yönetmeye çalışır:

* FloodWait
* Geçersiz kanal ID'leri
* RPC hataları
* Bağlantı sorunları
* Erişim izin hataları

Tüm önemli olaylar terminal üzerinden kullanıcıya bildirilir.

---

## ⚠️ Uyarı

Telegram'ın kullanım şartları ve hız limitleri bulunmaktadır.

Çok kısa aralıklarla yoğun mesaj gönderimi hesabınızın geçici veya kalıcı olarak kısıtlanmasına neden olabilir. Gönderim aralıklarını makul seviyelerde tutmanız önerilir.

---

## 📄 Lisans

Bu proje eğitim ve geliştirme amaçlı paylaşılmıştır.

Projeyi kullanırken Telegram'ın kullanım koşullarına uymanız kullanıcı sorumluluğundadır.
