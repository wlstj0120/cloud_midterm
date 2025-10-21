# Flask API를 완성하세요.
# 요구사항:
# - 데이터 파일 경로: /app/data/expenses.json  (초기 내용: [])
# - GET  /api/records   : 저장된 데이터를 JSON으로 반환
# - POST /api/records   : {title, amount, date} 저장 (유효성 검사 포함)
# - GET  /api/summary   : {count, total} 반환
# - GET  /api/download  : expenses.json 파일 다운로드

from flask import Flask, request, jsonify, send_file # <- request, jsonify, send_file 추가/활성화
from pathlib import Path
import json, os

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

# 데이터 로드/저장 헬퍼 함수 추가
def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/healthz")
def healthz():
    return "ok", 200

# 아래 엔드포인트들을 구현하세요. ( 함수명은 임의로 지정한 내용임 )

@app.get("/api/records") # <- 주석 해제 및 구현
def get_records():
    return jsonify(load_data()), 200

@app.post("/api/records") # <- 주석 해제 및 구현
def add_record():
    try:
        record = request.get_json()
        
        # 최소한의 유효성 검사: 필수 필드 및 금액 양수 여부 확인
        if not all(k in record for k in ('title', 'amount', 'date')):
            return jsonify({"error": "Missing fields"}), 400
        
        amount = float(record['amount'])
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
            
        data = load_data()
        data.append({
            "title": record['title'].strip(),
            "amount": amount,
            "date": record['date']
        })
        save_data(data)
        
        return jsonify({"message": "Record added"}), 201
    except:
        return jsonify({"error": "Invalid data or internal error"}), 500

@app.get("/api/summary") # <- 주석 해제 및 구현
def summary():
    data = load_data()
    count = len(data)
    total = sum(item.get('amount', 0) for item in data)
    return jsonify({"count": count, "total": total}), 200

@app.get("/api/download") # <- 주석 해제 및 구현
def download_json():
    return send_file(
        DATA_PATH,
        as_attachment=True,
        mimetype='application/json',
        download_name='expenses.json'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # <- 앱 실행 코드 추가