# Telegram Arkadaş Bildirim Botu

Bu proje, belirli bir web sayfasını periyodik olarak kontrol eden, hedeflenen kullanıcının çevrimiçi (aktif) olup olmadığını tespit eden ve durum değişikliğinde Telegram üzerinden anlık bildirim gönderen bir Python botudur. Bot, aynı zamanda kendi çalışma durumunu ve yaptığı kontrolleri anlık olarak gösteren bir web paneline sahiptir. Proje, bulut platformu Render üzerinde 7/24 çalışacak şekilde optimize edilmiştir.

## 🚀 Temel Özellikler

- **Periyodik Kontrol:** Her 5 dakikada bir hedef web sayfasını otomatik olarak ziyaret eder.
- **Akıllı Durum Tespiti:** Sayfanın HTML yapısını analiz ederek (`BeautifulSoup4` ile) kullanıcının çevrimiçi olup olmadığını kesin bir şekilde anlar.
- **Anlık Telegram Bildirimleri:** Kullanıcı aktif olduğunda, belirtilen Telegram sohbetine anında bir bildirim mesajı gönderir.
- **Canlı Durum Paneli:** Botun ne zaman kontrol yaptığını, ne sonuç aldığını ve olası hataları gösteren, web tarayıcısından erişilebilen bir durum paneli sunar.
- **Spam Önleme:** Kullanıcı aktif olduğu sürece sürekli bildirim göndermek yerine, yalnızca çevrimdışı durumdan aktif duruma geçtiğinde tek bir bildirim gönderir.
- **Bulut Uyumlu:** `gunicorn` ve bir `Flask` sunucusu ile Render'ın "Free" planında uykuya dalmadan (keep-alive) 7/24 çalışmak üzere tasarlanmıştır.

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python 3
- **Kütüphaneler:**
  - `requests`: Web sayfasına HTTP istekleri göndermek için.
  - `BeautifulSoup4`: Gelen HTML yanıtını analiz etmek ve veri çıkarmak için.
  - `python-telegram-bot`: Telegram Bot API ile etkileşim kurmak için.
  - `Flask`: Durum panelini sunan basit web sunucusu için.
  - `gunicorn`: Render üzerinde Flask uygulamasını çalıştırmak için profesyonel bir web sunucusu.

## ⚙️ Kurulum ve Yapılandırma

Projeyi yerel makinenizde veya Render'da çalıştırmak için aşağıdaki adımları izleyin.

### 1. Projeyi Klonlama

Öncelikle projeyi bilgisayarınıza klonlayın:
```bash
git clone [https://github.com/kullanici-adiniz/repository-adiniz.git](https://github.com/kullanici-adiniz/repository-adiniz.git)
cd repository-adiniz
```

### 2. Gerekli Kütüphaneleri Yükleme

Projenin ihtiyaç duyduğu kütüphaneleri `requirements.txt` dosyasını kullanarak yükleyin. Bir sanal ortam (virtual environment) kullanmanız tavsiye edilir.

```bash
# Sanal ortam oluştur (isteğe bağlı ama önerilir)
python -m venv venv
source venv/bin/activate  # macOS/Linux için
# venv\Scripts\activate    # Windows için

# Kütüphaneleri yükle
pip install -r requirements.txt
```

### 3. Ortam Değişkenleri (Environment Variables)

Bu proje, hassas bilgileri (API token gibi) doğrudan kod içinde saklamak yerine ortam değişkenleri aracılığıyla yönetir.

Aşağıdaki değişkenleri ayarlamanız gerekmektedir:

- `TELEGRAM_BOT_TOKEN`: BotFather'dan aldığınız Telegram botunuzun token'ı.
- `TELEGRAM_CHAT_ID`: Botun bildirim göndereceği sizin veya bir grubun Telegram ID'si.

Yerel testler için `app.py` dosyasındaki ilgili satırları geçici olarak doldurabilirsiniz. Ancak **Render'a yüklerken bu değişkenleri mutlaka Render'ın arayüzünden ayarlamalısınız.**

## 🚀 Render'a Yükleme (Deployment)

Bu bot, Render üzerinde bir **Web Service** olarak çalıştırılmak üzere tasarlanmıştır.

1.  Projenizi (`app.py` ve `requirements.txt` dosyalarıyla birlikte) GitHub'daki bir repository'e yükleyin.
2.  Render.com'da **"New +" -> "Web Service"** seçeneğine tıklayın.
3.  GitHub repository'nizi Render'a bağlayın.
4.  Aşağıdaki ayarları yapılandırın:
    - **Runtime:** `Python 3`
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `gunicorn app:app`
5.  **"Environment"** sekmesine gidin ve yukarıda belirtilen `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` değişkenlerini değerleriyle birlikte ekleyin.
6.  **"Free"** planını seçin ve **"Create Web Service"** butonuna tıklayın.

Render, kurulumu tamamladıktan sonra botunuzu başlatacaktır.

## 💻 Kullanım

Deployment tamamlandıktan sonra:

- Bot otomatik olarak çalışmaya başlayacak ve her 5 dakikada bir hedef sayfayı kontrol edecektir.
- Arkadaşınız çevrimiçi olduğunda Telegram üzerinden bir bildirim alacaksınız.
- Botun durumunu ve son aktivitelerini kontrol etmek için Render'ın size verdiği `https://proje-adiniz.onrender.com` adresini ziyaret edebilirsiniz.
