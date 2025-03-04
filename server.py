from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/entity-sim", response_class=HTMLResponse)
def entity_simulation(request: Request):
    return templates.TemplateResponse("entity_simulation.html", {"request": request})

@app.get("/models")
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

@app.get("/entities")
def list_entities():
    entities = [
        {
            "entity_id": "ent-001",
            "description": "UAV Surveillance Drone",
            "is_live": True,
            "created_time": "2025-02-15T10:30:00Z",
            "ontology": {
                "platform_type": "UAV",
                "specific_type": "Surveillance"
            },
            "health": {
                "health_status": 1,
                "connection_status": 2
            },
            "location": {
                "position": {
                    "latitude_degrees": 35.123456,
                    "longitude_degrees": -117.654321,
                    "altitude_hae_meters": {"__root__": 5000.0}
                }
            },
            "sensors": {
                "sensors": [
                    {
                        "sensor_id": "sens-001",
                        "sensor_description": "EO/IR Camera",
                        "sensor_type": "OPTICAL",
                        "operational_state": 4
                    },
                    {
                        "sensor_id": "sens-002",
                        "sensor_description": "RADAR",
                        "sensor_type": "ACTIVE",
                        "operational_state": 3
                    }
                ]
            },
            "indicators": {
                "simulated": True,
                "exercise": True,
                "emergency": False
            }
        },
        {
            "entity_id": "ent-002",
            "description": "Ground Radar Station",
            "is_live": True,
            "created_time": "2025-02-10T08:15:00Z",
            "ontology": {
                "platform_type": "Fixed",
                "specific_type": "Radar"
            },
            "health": {
                "health_status": 1,
                "connection_status": 2
            },
            "location": {
                "position": {
                    "latitude_degrees": 34.987654,
                    "longitude_degrees": -118.123456,
                    "altitude_hae_meters": {"__root__": 150.0}
                }
            },
            "sensors": {
                "sensors": [
                    {
                        "sensor_id": "sens-003",
                        "sensor_description": "Long Range Radar",
                        "sensor_type": "ACTIVE",
                        "operational_state": 4
                    }
                ]
            },
            "indicators": {
                "simulated": False,
                "exercise": True,
                "emergency": False
            }
        },
        {
            "entity_id": "ent-003",
            "description": "Geospatial Alert Zone",
            "is_live": True,
            "created_time": "2025-02-20T14:45:00Z",
            "ontology": {
                "platform_type": "Geo",
                "specific_type": "Alert"
            },
            "health": {
                "health_status": 3,
                "connection_status": 2
            },
            "location": None,
            "sensors": None,
            "indicators": {
                "simulated": True,
                "exercise": True,
                "emergency": True
            }
        }
    ]
    return JSONResponse(content=entities)

if __name__ == "__main__":
    os.makedirs('static/models', exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
