from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from engine import GuardianDL, string_to_tensor
import os

app = FastAPI(title="Guardian-DL Production API")

# Load the model once at startup
model = GuardianDL()
if os.path.exists("guardian_v1.pth"):
    model.load_state_dict(torch.load("guardian_v1.pth"))
model.eval()

class ScanRequest(BaseModel):
    data: str

@app.get("/")
def home():
    return {"message": "Guardian-DL API is Live", "status": "Ready"}

@app.post("/scan")
async def scan(request: ScanRequest):
    try:
        input_tensor = string_to_tensor(request.data)
        with torch.no_grad():
            score = model(input_tensor).item()
        
        return {
            "threat_score": f"{score:.4f}",
            "decision": "BLOCK" if score > 0.85 else "ALLOW",
            "engine": "Guardian-v1-CNN-LSTM"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
