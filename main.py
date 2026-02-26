import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from otel import configure_opentelemetry
from storage import Storage

configure_opentelemetry()

logger = logging.getLogger(__name__)
app = FastAPI(title="Scale23x")
FastAPIInstrumentor.instrument_app(app)

STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "demo")
STORAGE_ENDPOINT_URL = os.getenv("STORAGE_ENDPOINT_URL")

storage = Storage(bucket=STORAGE_BUCKET, endpoint_url=STORAGE_ENDPOINT_URL)

@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/upload/{key}")
async def upload(key: str, request: Request):
    data = await request.body()
    content_type = request.headers.get("content-type", "application/octet-stream")
    try:
        storage.upload_bytes(data, key=key, content_type=content_type)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"key": key, "size": len(data)}


@app.get("/download/{key}")
async def download(key: str):
    try:
        data = storage.download_bytes(key)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return Response(content=data, media_type="application/octet-stream", headers={"Content-Length": str(len(data))})
