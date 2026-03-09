FROM python:3.10-slim

# Ishchi katalogni yaratamiz
WORKDIR /code

# Kutubxonalarni o'rnatamiz
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodni nusxalaymiz
COPY app/ .

# Portni ochamiz va dasturni yurgizamiz
EXPOSE 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]