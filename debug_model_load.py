from sentence_transformers import SentenceTransformer
import torch

EMB_MODEL = "intfloat/multilingual-e5-base"

print(f"Torch version: {torch.__version__}")

try:
    print("Attempt 1: Loading with device='cpu'")
    model = SentenceTransformer(EMB_MODEL, device="cpu", model_kwargs={"low_cpu_mem_usage": False})
    print("Success 1")
except Exception as e:
    print(f"Failed 1: {e}")

try:
    print("Attempt 2: Loading with device='cpu' and low_cpu_mem_usage=False")
    model = SentenceTransformer(EMB_MODEL, device="cpu", model_kwargs={"low_cpu_mem_usage": False})
    print("Success 2")
except Exception as e:
    print(f"Failed 2: {e}")
