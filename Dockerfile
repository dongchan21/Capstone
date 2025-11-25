# Python 3.9 슬림 버전 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 라이브러리 설치 (필요시)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 데이터 복사
COPY . .

# 권한 설정 (Hugging Face Spaces에서 필요할 수 있음)
RUN chmod -R 777 /app

# 포트 설정 (Hugging Face Spaces 기본 포트)
EXPOSE 7860

# 서버 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
