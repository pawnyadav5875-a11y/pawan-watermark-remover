import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, PlainTextResponse

app = FastAPI(title="Pawan Studio - Video Watermark Remover", docs_url=None, redoc_url=None)


@app.middleware("http")
async def isolation_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "ok"


@app.get("/")
async def index():
    return FileResponse("index.html")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
         
