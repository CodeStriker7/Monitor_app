from fastapi import FastAPI, Response
import psutil
from prometheus_client import generate_latest, Gauge, CONTENT_TYPE_LATEST

app = FastAPI()

# Prometheus metrikalarini yaratamiz
CPU_USAGE = Gauge('system_cpu_usage_percent', 'CPU yuklamasi foizda')
RAM_USAGE = Gauge('system_ram_usage_percent', 'RAM yuklamasi foizda')

@app.get("/metrics")
def metrics():
    # Real vaqtda ko'rsatkichlarni yangilaymiz
    CPU_USAGE.set(psutil.cpu_percent())
    RAM_USAGE.set(psutil.virtual_memory().percent)
    
    # Ma'lumotni Prometheus tushunadigan formatda qaytaramiz
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)