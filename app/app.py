import psutil
import os
import time
import requests
from fastapi import FastAPI, Response, BackgroundTasks
from dotenv import load_dotenv
from prometheus_client import generate_latest, Gauge, CONTENT_TYPE_LATEST

# .env faylini yuklash
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = FastAPI(title="0x1:alfa Monitoring System")

# Prometheus metrikalari
CPU_USAGE = Gauge('system_cpu_usage_percent', 'CPU yuklamasi foizda')
RAM_USAGE = Gauge('system_ram_usage_percent', 'RAM yuklamasi foizda')
DISK_USAGE = Gauge('system_disk_usage_percent', 'Disk yuklamasi foizda')

# Alertlar uchun global o'zgaruvchi (oxirgi xabar vaqtini saqlaydi)
last_alert_sent_at = 0 
ALERT_COOLDOWN = 600  # 10 daqiqa (600 soniya) ichida faqat 1 marta alert berish

def send_telegram_msg(message: str):
    """Telegramga xabar yuborish funksiyasi"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Xatolik: Telegram sozlamalari topilmadi!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🖥 *SERVER MONITORING ALERT*\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram yuborishda xatolik: {e}")

@app.get("/metrics")
async def metrics(background_tasks: BackgroundTasks):
    global last_alert_sent_at
    
    # 1. Metrikalarni yig'ish
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # 2. Prometheus ko'rsatkichlarini yangilash
    CPU_USAGE.set(cpu)
    RAM_USAGE.set(ram)
    DISK_USAGE.set(disk)
    
    # 3. Alert mantiqi (Masalan: RAM > 85% yoki CPU > 90%)
    current_time = time.time()
    if (ram > 85 or cpu > 90) and (current_time - last_alert_sent_at > ALERT_COOLDOWN):
        alert_msg = f"⚠️ *Kritik yuklama aniqlandi!*\n\n📊 RAM: {ram}%\n⚙️ CPU: {cpu}%\n💽 Disk: {disk}%"
        
        # Xabar yuborishni orqa fonga qo'shamiz (asosiy response tez qaytishi uchun)
        background_tasks.add_task(send_telegram_msg, alert_msg)
        last_alert_sent_at = current_time

    # 4. Ma'lumotni Prometheus formatida qaytarish
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def root():
    return {"message": "System Monitor is running", "endpoints": ["/metrics", "/stats"]}

@app.get("/stats")
async def get_json_stats():
    """Brauzerda JSON ko'rinishida ko'rish uchun"""
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": time.time() - psutil.boot_time()
    }