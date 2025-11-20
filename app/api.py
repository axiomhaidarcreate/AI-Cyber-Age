
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .nmap_parser import parse_scan_file
from .agent import analyze_scan
from . import db

app = FastAPI(title="AI Cyber Agent API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")
    content = await file.read()
    parsed = parse_scan_file(content)
    if not parsed:
        raise HTTPException(status_code=400, detail="Could not parse file. Expect CSV-like: host,port,service,version")
    result = analyze_scan(parsed)
    return result

@app.get("/reports/latest")
async def latest_reports(limit: int = 100):
    rows = db.list_findings(limit=limit)
    return {"count": len(rows), "items": rows}
