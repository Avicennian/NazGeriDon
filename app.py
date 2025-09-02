import requests
from bs4 import BeautifulSoup
import time
import telegram
from flask import Flask
from threading import Thread
from collections import deque
import logging

# --- HATA KAYDI (LOGLAMA) KURULUMU ---
# Render'ın log ekranında daha düzenli bir çıktı için
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler() # Logları konsola yaz
    ]
)

# --- GEREKLİ BİLGİLERİ BURAYA GİRİN (VEYA RENDER'DA ORTAM DEĞİŞKENİ OLARAK AYARLAYIN) ---
import os
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'SENİN_BOT_TOKENIN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'SENİN_CHAT_IDN')
TARGET_URL = 'https://ribony.com/whydoyoul'
# ----------------------------------------------------

# --- WEB PANELİ İÇİN LOG HAFIZASI ---
# Son 50 log mesajını hafızada tutacak bir yapı.
# deque, bir liste dolduğunda en eski elemanı otomatik atar.
log_messages = deque(maxlen=50)

def add_log(message):
    """Hem konsola hem de web paneli için hafızaya log ekler."""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    logging.info(message) # Render konsolu için
    log_messages.appendleft(log_entry) # Web paneli için (en yeni en üste gelsin diye)

# --- FLASK WEB SUNUCUSU VE DURUM PANELİ ---
app = Flask('')

@app.route('/')
def status_panel():
    """Web tarayıcısında gösterilecek olan durum paneli sayfası."""
    html = """
    <html>
        <head>
            <title>Bot Durum Paneli</title>
            <meta http-equiv="refresh" content="60">
            <style>
                body { font-family: monospace; background-color: #1a1a1a; color: #dcdcdc; }
                .container { width: 80%; margin: 20px auto; padding: 20px; border: 1px solid #333; border-radius: 5px; background-color: #2a2a2a; }
                h1 { color: #4CAF50; }
                p { line-height: 1.6; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Arkadaş Kontrol Botu - Durum Paneli</h1>
                <p>Bu sayfa her 60 saniyede bir otomatik olarak yenilenir.</p>
                <hr>
                <h2>Son Kontroller:</h2>
    """
    
    for log in log_messages:
        html += f"<p>{log}</p>"
        
    html += """
            </div>
        </body>
    </html>
    """
    return html

def run_web_server():
    """Flask sunucusunu çalıştırır."""
    # Gunicorn bu adresi ve portu Render'da kendisi yönetir.
    app.run(host='0.0.0.0', port=8080)

# --- TELEGRAM BOT MANTIĞI ---
bot = None
try:
    if 'SENİN' not in TELEGRAM_BOT_TOKEN:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    else:
        add_log("HATA: Telegram Bot Token'ı ayarlanmamış!")
except Exception as e:
    add_log(f"HATA: Telegram botu başlatılamadı: {e}")

def check_friend_is_active():
    """Arkadaşın aktif olup olmadığını kontrol eder ve loglar."""
    try:
        add_log(f"Sayfa kontrol ediliyor: {TARGET_URL}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        offline_div = soup.find('div', class_='offline_head')

        if offline_div:
            add_log("Durum: Çevrimdışı (offline_head etiketi bulundu).")
            return False
        else:
            add_log("Durum: AKTİF! (offline_head etiketi bulunamadı).")
            return True

    except requests.exceptions.RequestException as e:
        add_log(f"HATA: Sayfa kontrolü sırasında bir ağ hatası oluştu: {e}")
        return False

def run_bot_logic():
    """Botun ana döngüsünü çalıştırır."""
    if not bot:
        add_log("Bot Token hatası nedeniyle bot mantığı çalıştırılmıyor.")
        return

    bildirim_gonderildi = False
    add_log("Bot başlatıldı. Kontroller başlıyor...")

    while True:
        is_active = check_friend_is_active()

        if is_active and not bildirim_gonderildi:
            add_log("Arkadaş aktif! Telegram bildirimi gönderiliyor...")
            try:
                mesaj = f"Arkadaşın şu an aktif!\nSayfayı kontrol et: {TARGET_URL}"
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj)
                bildirim_gonderildi = True
                add_log("Bildirim başarıyla gönderildi.")
            except Exception as e:
                add_log(f"HATA: Telegram mesajı gönderilemedi: {e}")

        elif not is_active:
            if bildirim_gonderildi:
                add_log("Arkadaş çevrimdışı oldu. Bildirim sistemi yeniden kuruldu.")
            bildirim_gonderildi = False

        add_log("5 dakika (300 saniye) bekleniyor...")
        time.sleep(300)

# --- ANA PROGRAM ---
if __name__ == "__main__":
    # 1. Web sunucusunu ayrı bir iş parçacığında (thread) başlat
    web_thread = Thread(target=run_web_server)
    web_thread.start()
    
    # 2. Ana iş parçacığında bot mantığını çalıştır
    run_bot_logic()
