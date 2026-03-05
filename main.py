from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import torch
from engine import GuardianDL, string_to_tensor
import os

# Secure this! In production, store this in Render Environment Variables
API_KEY = os.getenv("GUARDIAN_API_KEY", "pro-tier-key-2026")
api_key_header = APIKeyHeader(name="X-API-KEY")

app = FastAPI(title="Guardian-DL Commercial API")

# Load Brain
@app.get("/")
async def root():
    return {"message": "Guardian-DL API is online", "docs": "/docs"}

model = GuardianDL()
if os.path.exists("guardian_v1.pth"):
    model.load_state_dict(torch.load("guardian_v1.pth"))
model.eval()

class ScanRequest(BaseModel):
    data: str

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Invalid API Key. Purchase access at your-site.com")

@app.post("/scan")
async def scan(request: ScanRequest, token: str = Depends(get_api_key)):
    input_tensor = string_to_tensor(request.data)
    with torch.no_grad():
        score = model(input_tensor).item()
    return {
        "threat_score": f"{score:.4f}",
        "decision": "BLOCK" if score > 0.85 else "ALLOW"
    }
