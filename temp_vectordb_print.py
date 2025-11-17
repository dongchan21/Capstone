import pickle

# 메타데이터 파일 로드
with open("vector_db/deposit_meta.pkl", "rb") as f:
    meta = pickle.load(f)

print(f"총 문서 수: {len(meta)}")

# 앞부분 100개만 출력 (필요시 10, 50 등으로 바꿔도 됨)
for i, item in enumerate(meta[:100]):
    print(f"\n[{i+1}] -----------------------------")
    if isinstance(item, dict):
        print(item.get("content", "")[:300])  # 300자까지만 미리보기
        print("메타:", item.get("meta", {}))
    else:
        print(item[:300])
