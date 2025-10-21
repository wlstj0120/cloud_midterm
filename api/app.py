# Flask API 간략 버전

from flask import Flask, request, jsonify, send_file
from pathlib import Path
import json

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

# 데이터 로드/저장 헬퍼 함수 (간결 유지)
def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/healthz")
def healthz():
    return "ok", 200

# GET /api/records
@app.get("/api/records")
def get_records():
    return jsonify(load_data()), 200

# POST /api/records (유효성 검사 간소화)
@app.post("/api/records")
def add_record():
    record = request.get_json()
    
    # 필수 필드만 간단히 확인 (title, amount, date)
    if not all(k in record for k in ('title', 'amount', 'date')):
        return jsonify({"error": "Missing fields"}), 400
    
    try:
        data = load_data()
        
        # amount를 숫자로 변환
        amount = float(record['amount'])

        # amount가 양수인지 간단히 확인
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
            
        data.append({
            "title": record['title'].strip(),
            "amount": amount,
            "date": record['date']
        })
        save_data(data)
        
        return jsonify({"message": "Record added"}), 201
    except:
        # 데이터 처리 중 발생할 수 있는 오류를 일반 오류로 처리
        return jsonify({"error": "Invalid data format or internal error"}), 500


# GET /api/summary
@app.get("/api/summary")
def summary():
    data = load_data()
    count = len(data)
    # amount가 없는 경우를 대비해 get() 사용
    total = sum(item.get('amount', 0) for item in data) 
    return jsonify({"count": count, "total": total}), 200

# GET /api/download
@app.get("/api/download")
def download_json():
    # send_file은 경로만 지정하면 되므로 매우 간단함
    return send_file(
        DATA_PATH,
        as_attachment=True,
        mimetype='application/json',
        download_name='expenses.json'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)