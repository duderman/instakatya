FROM python:3.7.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

VOLUME /app/db

CMD ["python3", "bot.py"]
