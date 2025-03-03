from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
def list_models():
    models = {
        "aircraft": ["f16.glb", "b2_spirit.glb", "helicopter.glb", "commercial_airliner.glb"],
        "vehicles": ["car.glb", "truck.glb", "tank.glb", "train.glb"],
        "city": ["new_york.glb", "tokyo.glb", "london.glb", "custom_city.glb"]
    }
    return JSONResponse(content=models)

@app.get("/scenarios")
def list_scenarios():
    scenarios = [
        {"id": "city_flyover", "name": "City Flyover", "description": "Aircraft flying over a city"},
        {"id": "ground_vehicles", "name": "Ground Vehicle Simulation", "description": "Vehicles moving through city streets"},
        {"id": "military_op", "name": "Military Operation", "description": "Combined aircraft and ground vehicle operation"}
    ]
    return JSONResponse(content=scenarios)

@app.get("/load_scenario/{scenario_id}")
def load_scenario(scenario_id):
    # In a real app, this would load specific configuration
    scenario_configs = {
        "city_flyover": {
            "environment": "new_york.glb",
            "models": ["b2_spirit.glb"],
            "camera": {"position": [0, 500, 500], "target": [0, 0, 0]},
            "lighting": "day",
            "physics": "simple"
        },
        "ground_vehicles": {
            "environment": "tokyo.glb",
            "models": ["car.glb", "truck.glb"],
            "camera": {"position": [0, 100, 100], "target": [0, 0, 0]},
            "lighting": "night",
            "physics": "complex"
        },
        "military_op": {
            "environment": "custom_city.glb",
            "models": ["f16.glb", "tank.glb"],
            "camera": {"position": [0, 300, 300], "target": [0, 0, 0]},
            "lighting": "dusk",
            "physics": "complex"
        }
    }
    
    if scenario_id in scenario_configs:
        return JSONResponse(content=scenario_configs[scenario_id])
    else:
        raise HTTPException(status_code=404, detail="Scenario not found")

@app.post("/upload_model")
async def upload_model(model: UploadFile = File(...)):
    if not model.filename.endswith('.glb'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    filepath = os.path.join('static/models', model.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await model.read())
    
    return {"success": True, "filename": model.filename}

if __name__ == "__main__":
    os.makedirs('static/models', exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
