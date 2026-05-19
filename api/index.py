import sys
from pathlib import Path

# Vercel 환경에서 app 모듈을 정상적으로 import 할 수 있도록 프로젝트 루트 경로를 시스템 경로에 추가합니다.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# app.server 내의 FastAPI 인스턴스(app)를 가져와 Vercel Serverless Function이 진입할 수 있도록 합니다.
from app.server import app
