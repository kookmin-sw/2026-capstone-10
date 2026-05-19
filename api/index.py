import sys
from pathlib import Path
from starlette.types import ASGIApp, Receive, Scope, Send

# Vercel 환경에서 app 모듈을 정상적으로 import 할 수 있도록 프로젝트 루트 경로를 시스템 경로에 추가합니다.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class StripApiPrefix:
    """
    Vercel은 /api/generate-svg 경로를 그대로 FastAPI에 전달합니다.
    FastAPI 라우트는 /generate-svg로 정의되어 있으므로,
    /api 접두사를 제거해야 정상적으로 라우팅됩니다.
    """
    def __init__(self, application: ASGIApp) -> None:
        self.app = application

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ("http", "websocket"):
            path: str = scope.get("path", "")
            if path.startswith("/api"):
                scope["path"] = path[4:] or "/"
                raw: bytes = scope.get("raw_path", b"")
                scope["raw_path"] = raw[4:] or b"/"
        await self.app(scope, receive, send)


from app.server import app as _fastapi_app

# Vercel Serverless Function 진입점
app = StripApiPrefix(_fastapi_app)

