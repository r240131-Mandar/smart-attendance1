FROM python:3.12-slim

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV DB_PATH=/data/attendance.db
RUN mkdir -p /data
VOLUME /data

EXPOSE 5000
CMD ["python", "app/app.py"]
