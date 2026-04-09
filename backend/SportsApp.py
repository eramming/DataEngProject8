from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from logging import Logger, getLogger, INFO, basicConfig
import argparse, uvicorn
from backend.PostgresClient import PostgresClient

basicConfig(
    level=INFO,
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

pg_client: PostgresClient = PostgresClient()


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/venues")
def venues():
    return pg_client.get_venues()


@app.get("/census")
def census():
    return pg_client.get_census()

@app.get("/seasons")
def seasons():
    return pg_client.get_seasons()

@app.get("/teams")
def teams():
    return pg_client.get_teams()

@app.get("/games")
def games():
    return pg_client.get_games()

@app.get("/game-teams")
def game_teams():
    return pg_client.get_game_teams()

@app.get("/view")
def game_view():
    return pg_client.get_game_view()

def run(host: str = "0.0.0.0", port: int = 8000, reload: bool = True) -> None:
    uvicorn.run(app, host=host, port=port, reload=reload)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Clue-Less Backend")
    parser.add_argument("--host", "-H", default="0.0.0.0", help="Host to Serve on")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to Serve on")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    args = parser.parse_args()

    run(host=args.host, port=args.port, reload=not args.no_reload)