import json
import os
import sys
import chardet

# ✅ 외부에서 파일 경로를 인자로 받음
if len(sys.argv) < 2:
    raise ValueError("❌ 텍스트 파일 경로를 인자로 전달해야 합니다. 예: python convert_txt_to_json.py data/raw_txt/새파일.txt")

TXT_PATH = sys.argv[1]
JSON_PATH = "data/deposit_docs.json"

def read_txt_auto(path):
    """텍스트 파일 인코딩 자동 감지 후 내용 읽기"""
    try:
        # 🔍 인코딩 자동 감지
        with open(path, "rb") as f:
            raw_data = f.read()
            encoding_info = chardet.detect(raw_data)
        
        encoding = encoding_info["encoding"] or "utf-8"
        print(f"✅ 인코딩 감지됨: {encoding}")
        
        return raw_data.decode(encoding)
    except Exception as e:
        raise RuntimeError(f"TXT 로드 실패: {e}")

# 텍스트 내용 읽기
content = read_txt_auto(TXT_PATH)

# ============================================
# JSON 데이터 생성
# ============================================

# 텍스트 파일은 전체 내용을 하나의 문서로 처리하거나, 
# 필요에 따라 단락별로 나눌 수 있습니다. 
# 여기서는 전체 내용을 하나의 'content'로 처리합니다.

record = {
    "source": os.path.basename(TXT_PATH),
    "content": content,
    "meta": {
        "type": "text_file",
        "original_path": TXT_PATH
    }
}

# ============================================
# 기존 JSON 병합 및 저장
# ============================================

if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        try:
            old_data = json.load(f)
        except json.JSONDecodeError:
            old_data = []
else:
    old_data = []

source_name = os.path.basename(TXT_PATH)
# 기존에 같은 파일명으로 처리된 데이터가 있다면 제거 (중복 방지)
filtered_old = [item for item in old_data if item.get("source") != source_name]

# 새 데이터 추가
filtered_old.append(record)

os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(filtered_old, f, ensure_ascii=False, indent=2)

print(f"\n✅ 텍스트 파일 처리 완료: {source_name}")
print(f"📁 저장 위치: {JSON_PATH}")
