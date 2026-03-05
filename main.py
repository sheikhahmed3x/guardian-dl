from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
import torch
from engine import GuardianDL, string_to_tensor
import os

API_KEY = os.getenv("GUARDIAN_API_KEY", "pro-tier-key-2026")
api_key_header = APIKeyHeader(name="X-API-KEY")

app = FastAPI(
    title="Guardian-DL: Proprietary AI Security Engine",
    description="High-speed CNN-LSTM threat detection for 2026 cybersecurity infrastructure.",
    version="1.0.0"
)

# Professional Data Models for the Marketplace
class ScanRequest(BaseModel):
    data: str = Field(..., example="SELECT * FROM users", description="The raw payload to analyze")

class ScanResponse(BaseModel):
    threat_score: float = Field(..., example=0.985)
    decision: str = Field(..., example="BLOCK")
    engine: str = Field(default="Guardian-v1-CNN-LSTM")

# Load the DL Brain
model = GuardianDL()
if os.path.exists("guardian_v1.pth"):
    model.load_state_dict(torch.load("guardian_v1.pth"))
model.eval()

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Unauthorized: Get a key at guardian-dl.com")

@app.get("/", tags=["Health"])
async def root():
    return {"status": "Online", "engine": "Guardian-v1", "docs": "/docs"}

@app.post("/scan", response_model=ScanResponse, tags=["Inference"])
async def scan(request: ScanRequest, token: str = Depends(get_api_key)):
    input_tensor = string_to_tensor(request.data)
    with torch.no_grad():
        score = model(input_tensor).item()
    return {
        "threat_score": round(score, 4),
        "decision": "BLOCK" if score > 0.85 else "ALLOW",
        "engine": "Guardian-v1-CNN-LSTM"
    }
