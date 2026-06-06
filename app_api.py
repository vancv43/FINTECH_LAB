"""FastAPI REST Backend — Port 8000. Docs at http://127.0.0.1:8000/docs"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from app_backend import run_analysis, get_kb_stats

app = FastAPI(title="Enterprise AI Agent API", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AnalyzeRequest(BaseModel):
    business_name: str; admin_email: str
    team_size: int=12; duration_weeks: int=8
    risk_level: str="medium"; region: str="southwest"
    issue_description: str; use_llm: bool=False

@app.get("/api/v1/health")
def health(): return {"status":"online","agents":["SemanticSearch","ML_RandomForest","FLAN_T5_Explainer"]}

@app.post("/api/v1/analyze")
def analyze(req: AnalyzeRequest): return run_analysis(**req.dict())

@app.get("/api/v1/kb-stats")
def kb_stats(): return get_kb_stats()

if __name__=="__main__": uvicorn.run(app, host="127.0.0.1", port=8000)
