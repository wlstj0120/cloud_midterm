# Flask API를 완성하세요.
# 요구사항:
# - 데이터 파일 경로: /app/data/expenses.json  (초기 내용: [])
# - GET  /api/records   : 저장된 데이터를 JSON으로 반환
# - POST /api/records   : {title, amount, date} 저장 (유효성 검사 포함)
# - GET  /api/summary   : {count, total} 반환
# - GET  /api/download  : expenses.json 파일 다운로드

from flask import Flask, request, jsonify, send_file
from pathlib import Path
import json, os
from datetime import datetime

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

# 데이터 로드/저장 헬퍼 함수
def load_data():
    """expenses.json에서 데이터를 로드합니다."""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """데이터를 expenses.json에 저장합니다."""
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/healthz")
def healthz():
    return "ok", 200

# 아래 엔드포인트들을 구현하세요.

@app.get("/api/records")
def get_records():
    """저장된 모든 지출 기록을 JSON으로 반환합니다."""
    data = load_data()
    return jsonify(data), 200

@app.post("/api/records")
def add_record():
    """새 지출 기록을 저장합니다. (유효성 검사 포함)"""
    try:
        record = request.get_json()
        
        # 필수 필드 체크
        if not all(k in record for k in ('title', 'amount', 'date')):
            return jsonify({"error": "Missing fields: title, amount, date"}), 400
        
        title = record['title']
        amount = record['amount']
        date_str = record['date']

        # title 유효성: 비어 있지 않은 문자열
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title must be a non-empty string"}), 400
        
        # amount 유효성: 양수 (0 포함 안 함)
        try:
            amount = float(amount)
            if amount <= 0:
                 return jsonify({"error": "Amount must be a positive number"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Amount must be a valid number"}), 400
        
        # date 유효성: YYYY-MM-DD 형식
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Date must be in YYYY-MM-DD format"}), 400

        # 데이터 저장
        data = load_data()
        data.append({
            "title": title.strip(),
            "amount": amount,
            "date": date_str
        })
        save_data(data)
        
        return jsonify({"message": "Record added successfully"}), 201

    except Exception as e:
        # JSON 파싱 오류 등 기타 예외 처리
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.get("/api/summary")
def summary():
    """현재까지의 기록 수(count)와 총합(total)을 반환합니다."""
    data = load_data()
    count = len(data)
    total = sum(item.get('amount', 0) for item in data)
    return jsonify({"count": count, "total": total}), 200

@app.get("/api/download")
def download_json():
    """expenses.json 파일을 클라이언트에게 다운로드 형식으로 전송합니다."""
    return send_file(
        DATA_PATH,
        as_attachment=True,
        mimetype='application/json',
        download_name='expenses.json'
    )

if __name__ == "__main__":
    # 적절한 포트(5000)로 0.0.0.0 에서 실행
    app.run(host="0.0.0.0", port=5000)