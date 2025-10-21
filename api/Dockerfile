FROM python:3.11

WORKDIR /app

COPY api/requirements.txt /app/requirements.txt

# --- 이 부분을 수정하세요 ---
# SSL 인증서 오류를 우회하기 위해 pypi.org와 files.pythonhosted.org를 신뢰할 수 있는 호스트로 추가
RUN pip install --no-cache-dir -r /app/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY api/ /app/

# Flask가 리슨하는 포트를 노출하세요 (예: 5000)
EXPOSE 5000

# 컨테이너 시작 시 Flask 앱을 실행하도록 CMD를 작성하세요
CMD ["python", "app.py"]