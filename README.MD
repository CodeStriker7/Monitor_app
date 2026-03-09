#System Monitoring Tool (FastAPI + Prometheus + Grafana)

Loyiha Linux tizimi ko'rsatkichlarini (CPU, RAM, Disk) real vaqtda kuzatish uchun yaratidi

## Texnologiyalar:
- **Python (FastAPI)** - Metrikalarni yig'ish uchun.
- **Prometheus** - Ma'lumotlarni saqlash (Time-series DB).
- **Grafana** - Vizualizatsiya va Dashboardlar.
- **Docker & Compose** - Loyihani konteynerizatsiya qilish.

## 📦 Ishga tushirish:
1. Loyihani yuklab oling.
2. Terminalda loyiha papkasiga kiring.
3. Quyidagi buyruqni bering:
   ```bash
   docker-compose up -d

```

Konteynerlar muvaffaqiyatli ishga tushgach, quyidagi manzillar orqali tizimni tekshirishingiz mumkin:

Python API (Metrics): http://localhost:8000/metrics — Bu yerda xom metrikalar (Prometheus formatida) ko'rinadi.
Prometheus UI: http://localhost:9090 — Ma'lumotlar bazasining holatini va so'rovlarni (queries) tekshirish uchun.
Grafana Dashboard: http://localhost:3000 — Vizual grafiklar uchun.
Login: admin
Parol: admin