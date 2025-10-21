# Flask API를 완성하세요.
# 요구사항:
# - 데이터 파일 경로: /app/data/expenses.json  (초기 내용: [])
# - GET  /api/records   : 저장된 데이터를 JSON으로 반환
# - POST /api/records   : {title, amount, date} 저장 (유효성 검사 포함)
# - GET  /api/summary   : {count, total} 반환
# - GET  /api/download  : expenses.json 파일 다운로드

from flask import Flask, request, send_file, Response # <- jsonify 대신 Response를 사용
from pathlib import Path
import json, os

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

# 데이터 로드/저장 헬퍼 함수
def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Python 객체를 JSON 응답으로 변환하는 헬퍼 함수 (jsonify 대체)
def json_response(data, status=200):
    # Python 객체를 JSON 문자열로 변환
    json_string = json.dumps(data, ensure_ascii=False, indent=2)
    # Response 객체를 생성하고 Content-Type을 application/json으로 설정
    return Response(
        json_string,
        status=status,
        mimetype='application/json'
    )

@app.get("/healthz")
def healthz():
    return "ok", 200

# --- 핵심 API 엔드포인트 구현 (json_response 사용) ---

@app.get("/api/records")
def get_records():
    # load_data()는 Python 리스트를 반환하며, json_response가 JSON 문자열로 변환
    return json_response(load_data(), 200)

@app.post("/api/records")
def add_record():
    try:
        record = request.get_json()
        
        # 최소한의 유효성 검사
        if not all(k in record for k in ('title', 'amount', 'date')):
            return json_response({"error": "Missing fields"}, 400)
        
        amount = float(record['amount'])
        if amount <= 0:
            return json_response({"error": "Amount must be positive"}, 400)
            
        data = load_data()
        data.append({
            "title": record['title'].strip(),
            "amount": amount,
            "date": record['date']
        })
        save_data(data)
        
        # 성공 메시지를 JSON으로 반환
        return json_response({"message": "Record added"}, 201)
    except:
        return json_response({"error": "Invalid data or internal error"}, 500)

@app.get("/api/summary")
def summary():
    data = load_data()
    count = len(data)
    total = sum(item.get('amount', 0) for item in data)
    
    # 계산된 요약을 JSON으로 반환
    return json_response({"count": count, "total": total}, 200)

@app.get("/api/download")
def download_json():
    # 파일 다운로드는 send_file을 사용하며, 이는 JSON 데이터 반환과 목적이 다름
    return send_file(
        DATA_PATH,
        as_attachment=True,
        mimetype='application/json',
        download_name='expenses.json'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)