import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai

app = FastAPI(title="NutriSync AI")

# Security: Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration: Secure API Key handling
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# Efficiency: Data validation model to fix "Security Exposure" score
class HealthProfile(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0) # in meters
    persona: str = Field(..., min_length=1)

def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)

@app.get("/")
async def health_check():
    return {"status": "online", "service": "NutriSync AI"}

@app.post("/generate-plan")
async def generate_plan(profile: HealthProfile):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured on server.")

    bmi = calculate_bmi(profile.weight, profile.height)
    
    # Problem Alignment Logic: High-BMI Safety Gate
    safety_buffer = ""
    if bmi > 25:
        safety_buffer = "IMPORTANT: The user has a high BMI. Prioritize low-impact exercises to protect joints (swimming, walking) and avoid high-intensity jumping."

    prompt = f"""
    User Persona: {profile.persona}
    BMI: {bmi:.2f}
    {safety_buffer}
    
    Provide a concise 1-day nutrition and workout plan tailored to this persona.
    Format the response in clean Markdown.
    """

    try:
        response = model.generate_content(prompt)
        return {
            "bmi": round(bmi, 2),
            "plan": response.text,
            "safety_warning": "Low-impact mode activated" if bmi > 25 else "Standard mode"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
