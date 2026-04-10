import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class Profile(BaseModel):
    user_type: str
    bmi: float

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NutriSync AI</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
        <main class="max-w-md w-full bg-white rounded-3xl shadow-xl p-8 border border-slate-100">
            <header class="text-center mb-8">
                <h1 class="text-3xl font-extrabold text-indigo-600">NutriSync AI</h1>
                <p class="text-slate-500">Contextual Health Assistant</p>
            </header>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">I am a...</label>
                    <select id="user_type" class="w-full p-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition">
                        <option>Working Professional</option>
                        <option>Women's Health Focus</option>
                        <option>Family Caretaker</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">My BMI</label>
                    <input id="bmi" type="number" step="0.1" placeholder="e.g. 24.5" class="w-full p-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition">
                </div>
                <button onclick="getPlan()" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-indigo-200 transition duration-300">
                    Generate Smart Plan
                </button>
            </div>

            <div id="result" class="mt-8 p-4 bg-indigo-50 rounded-2xl text-slate-700 text-sm leading-relaxed hidden border border-indigo-100">
                </div>
        </main>

        <script>
            async function getPlan() {
                const resultDiv = document.getElementById('result');
                resultDiv.classList.remove('hidden');
                resultDiv.innerText = "Analyzing safety protocols and persona context...";
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_type: document.getElementById('user_type').value,
                        bmi: parseFloat(document.getElementById('bmi').value)
                    })
                });
                const data = await response.json();
                resultDiv.innerText = data.plan;
            }
        </script>
    </body>
    </html>
    """

@app.post("/generate")
async def generate_plan(data: Profile):
    # BMI Safety Logic
    safety = "low-impact / joint-safe" if data.bmi > 25 else "standard intensity"
    
    prompt = f"User: {data.user_type}, BMI: {data.bmi}. Goal: Healthier habits. Requirement: Exercises MUST be {safety}. Suggest one specific meal and one specific exercise with a short 'why' for this persona."
    
    response = model.generate_content(prompt)
    return {"plan": response.text}
