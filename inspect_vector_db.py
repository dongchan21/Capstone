import pickle

META_PATH = "vector_db/deposit_meta.pkl"

with open(META_PATH, "rb") as f:
    docs = pickle.load(f)

print(f"✅ 총 {len(docs)}개의 문서가 인덱스에 포함되어 있습니다.\n")

# 앞부분 몇 개만 미리보기
for i, doc in enumerate(docs[:5]):
    print(f"[{i+1}] {doc[:300]}...\n")
