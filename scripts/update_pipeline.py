import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 📁 감시 대상 폴더
EXCEL_DIR = "data/raw_excels"
CSV_DIR = "data/raw_csv"

# 🗂 로그 및 임시 경로
LOG_PATH = "logs/update_log.txt"
JSON_PATH = "data/deposit_docs.json"

def log(msg):
    """터미널 및 로그 파일에 동시에 출력"""
    msg_full = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(msg_full)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg_full + "\n")

def run_pipeline(file_path, file_type="excel"):
    log(f"📂 새 {file_type.upper()} 파일 감지됨: {file_path}")
    log("🔄 변환 및 인덱싱 파이프라인 시작")

    # 1️⃣ 엑셀/CSV → JSON 변환
    if file_type == "excel":
        log("📄 Excel → JSON 변환 중 ...")
        os.system(f"python scripts/convert_excel_to_json.py \"{file_path}\"")
    elif file_type == "csv":
        log("📄 CSV → JSON 변환 중 ...")
        os.system(f"python scripts/convert_csv_to_json.py \"{file_path}\"")

    # 2️⃣ 인덱스 재생성
    log("🧠 벡터 인덱스 재생성 중 ...")
    os.system("python scripts/build_index.py")

    # 3️⃣ JSON 파일 삭제 (임시 캐시 제거)
    if os.path.exists(JSON_PATH):
        try:
            os.remove(JSON_PATH)
            log(f"🧹 임시 JSON 파일 삭제 완료 → {JSON_PATH}")
        except Exception as e:
            log(f"⚠️ JSON 삭제 중 오류 발생: {e}")

    # 완료 로그
    log("✅ 업데이트 완료!\n")

class DataEventHandler(FileSystemEventHandler):
    """폴더 내 .xlsx / .xls / .csv 파일 변경 감지 시 자동 실행"""
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".xlsx", ".xls")):
            run_pipeline(event.src_path, "excel")
        elif event.src_path.endswith(".csv"):
            run_pipeline(event.src_path, "csv")

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".xlsx", ".xls")):
            run_pipeline(event.src_path, "excel")
        elif event.src_path.endswith(".csv"):
            run_pipeline(event.src_path, "csv")

if __name__ == "__main__":
    os.makedirs(EXCEL_DIR, exist_ok=True)
    os.makedirs(CSV_DIR, exist_ok=True)

    log("👀 Excel & CSV 폴더 감시 시작 ... (Ctrl+C로 종료)")

    observer = Observer()
    handler = DataEventHandler()

    # 두 폴더 감시 등록
    observer.schedule(handler, path=EXCEL_DIR, recursive=False)
    observer.schedule(handler, path=CSV_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log("🛑 폴더 감시 중단됨")

    observer.join()
