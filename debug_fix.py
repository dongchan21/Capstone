from sentence_transformers import SentenceTransformer
import torch

EMB_MODEL = "intfloat/multilingual-e5-base"

print("Attempting to load model with low_cpu_mem_usage=False...")
try:
    model = SentenceTransformer(EMB_MODEL, device="cpu", model_kwargs={"low_cpu_mem_usage": False})
    print("✅ Success! Model loaded on CPU.")
except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback
    traceback.print_exc()
