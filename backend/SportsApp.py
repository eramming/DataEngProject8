from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from logging import Logger, getLogger, INFO, basicConfig
import uuid, argparse, uvicorn


basicConfig(
    level=INFO,  # root level
)
LOG: Logger = getLogger(__name__)
LOG.setLevel(INFO)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


@app.get("/")
def read_root():
    return FileResponse(FRONTEND_DIR / "index.html")



def run (host: str = "127.0.0.1", port: int = 8000, reload: bool = True) -> None:
    uvicorn.run(app, host=host, port=port, reload=reload)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Clue-Less Backend")
    parser.add_argument("--host", "-H", default="127.0.0.1", help="Host to Serve on")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to Serve on")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    args = parser.parse_args()
    run(host=args.host, port=args.port, reload= not args.no_reload)