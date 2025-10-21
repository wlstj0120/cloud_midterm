FROM python:3.11

WORKDIR /app

COPY api/requirements.txt /app/requirements.txt
# SSL 오류 해결 옵션은 유지
RUN pip install --no-cache-dir -r /app/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY api/ /app/

# Flask 포트 5000 노출
EXPOSE 5000

# Flask 앱 실행
CMD ["python", "app.py"]