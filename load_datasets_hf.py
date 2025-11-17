from datasets import load_dataset

# 기본 로드 (스플릿이 있으면 자동으로 가져옵니다)
ds = load_dataset("BCCard/BCCard-Finance-Kor-QnA")
print(ds)                 # 전체 요약
print(ds["train"][0])     # 첫 샘플 확인

# CSV/Parquet로 저장하기 (원하면)
df = ds["train"].to_pandas()
df.to_csv("BCCard-Finance-Kor-QnA_train.csv", index=False)
# 또는: ds["train"].to_parquet("BCCard-Finance-Kor-QnA_train.parquet")