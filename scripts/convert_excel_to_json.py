import pandas as pd
import json
import os
import re
import sys

# ✅ 외부에서 파일 경로를 인자로 받음
if len(sys.argv) < 2:
    raise ValueError("❌ Excel 파일 경로를 인자로 전달해야 합니다. 예: python convert_excel_to_json_auto.py data/raw_excels/새파일.xlsx")

EXCEL_PATH = sys.argv[1]
JSON_PATH = "data/deposit_docs.json"

# ⚠️ 엑셀 임시파일(~$) 무시
if os.path.basename(EXCEL_PATH).startswith("~$"):
    print(f"⏭️ 임시파일 감지됨, 처리 생략: {EXCEL_PATH}")
    sys.exit(0)

# ============================================
# 1️⃣ 엑셀 헤더 자동 감지
# ============================================

def read_excel_auto(path):
    """엑셀 헤더 유무 자동 감지 후 DataFrame으로 로드"""
    try:
        preview = pd.read_excel(path, nrows=1, header=None)
        first_row = preview.iloc[0].tolist()
        str_ratio = sum(isinstance(x, str) for x in first_row) / len(first_row)

        if str_ratio > 0.5:
            print("✅ 헤더 감지됨 → 첫 행을 컬럼명으로 사용합니다.")
            df = pd.read_excel(path, header=0)
        else:
            print("⚠️ 헤더 없음 → 임의 컬럼명(컬럼1, 컬럼2...) 부여합니다.")
            df = pd.read_excel(path, header=None)
            df.columns = [f"컬럼{i+1}" for i in range(len(df.columns))]
    except Exception as e:
        raise RuntimeError(f"엑셀 로드 실패: {e}")
    return df.fillna("")

df = read_excel_auto(EXCEL_PATH)

# ============================================
# 2️⃣ 주요 컬럼 자동 탐지 (금리 / 은행명 / 상품명 / 기간)
# ============================================

def detect_column(columns, keywords):
    for col in columns:
        if any(kw in str(col) for kw in keywords):
            return col
    return None

col_bank = detect_column(df.columns, ["금융회사", "은행", "기관"])
col_product = detect_column(df.columns, ["상품", "예금", "펀드", "대출"])
col_rate = detect_column(df.columns, ["금리", "이율", "수익률"])
col_period = detect_column(df.columns, ["기간", "만기", "가입"])

# ============================================
# 3️⃣ 금리 숫자 변환 함수 (날짜 등 오인 방지)
# ============================================

def parse_rate(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    # 숫자 추출
    match = re.search(r"\d+(\.\d+)?", s)
    if not match:
        return None
    num = float(match.group())
    # 날짜로 인식되는 숫자(100 이상 or 연도 형태) 제외
    if num > 50 or "202" in s or "년" in s:
        return None
    return num

# ============================================
# 4️⃣ 각 행(row)을 문장 형태로 변환
# ============================================

records = []
for _, row in df.iterrows():
    text_parts = [f"{col}: {row[col]}" for col in df.columns]
    combined_text = " | ".join(text_parts)

    rate_val = parse_rate(row[col_rate]) if col_rate else None

    meta = {
        "bank": str(row[col_bank]) if col_bank else None,
        "product": str(row[col_product]) if col_product else None,
        "rate": rate_val,
        "period": str(row[col_period]) if col_period else None,
    }

    records.append({
        "source": os.path.basename(EXCEL_PATH),
        "content": combined_text,
        "meta": {k: v for k, v in meta.items() if v not in [None, ""]}
    })

# ============================================
# 5️⃣ 기존 JSON 병합 및 저장
# ============================================

if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        old_data = json.load(f)
else:
    old_data = []

source_name = os.path.basename(EXCEL_PATH)
filtered_old = [item for item in old_data if item["source"] != source_name]
new_data = filtered_old + records

os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 총 {len(records)}개의 행을 처리했습니다.")
print(f"📁 저장 위치: {JSON_PATH}")
if col_rate is None:
    print("⚠️ 금리 컬럼을 자동으로 찾지 못했습니다. rate 필드는 None으로 처리됩니다.")
