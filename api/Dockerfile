FROM python:3.11

WORKDIR /app

COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY api/ /app/

# Flask가 리슨하는 포트를 노출하세요 (예: 5000)
EXPOSE 5000

# 컨테이너 시작 시 Flask 앱을 실행하도록 CMD를 작성하세요
CMD ["python", "app.py"]