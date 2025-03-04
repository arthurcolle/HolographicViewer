from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
import subprocess
import shutil
from pathlib import Path
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

def get_supported_formats():
    """Returns a list of supported 3D model formats"""
    return ['.glb', '.gltf', '.fbx', '.obj', '.stl', '.dae']

def convert_to_glb(input_path, output_path):
    """
    Convert various 3D model formats to GLB using Blender
    Returns the path to the converted file
    """
    # Create temp directory if it doesn't exist
    os.makedirs('temp_conversions', exist_ok=True)
    
    # Get file extension
    file_ext = os.path.splitext(input_path)[1].lower()
    
    # If already GLB, just copy the file
    if file_ext == '.glb':
        shutil.copy(input_path, output_path)
        return output_path
    
    # For other formats, use Blender for conversion
    # Note: This requires Blender to be installed on the system
    try:
        # Path to the Blender Python script for conversion
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'convert_model.py')
        
        # Run Blender headless to convert the model
        cmd = [
            'blender', '--background', '--python', script_path, '--', 
            input_path, output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Conversion error: {result.stderr}")
            return None
            
        return output_path
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return None

@app.post("/upload_model")
async def upload_model(model: UploadFile = File(...), convert_to_glb_format: bool = Form(True)):
    # Get file extension
    filename = model.filename
    file_ext = os.path.splitext(filename)[1].lower()
    
    # Check if file format is supported
    supported_formats = get_supported_formats()
    if file_ext not in supported_formats:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Supported formats: {', '.join(supported_formats)}"
        )
    
    # Create temp directory for uploads
    os.makedirs('temp_uploads', exist_ok=True)
    temp_path = os.path.join('temp_uploads', filename)
    
    # Save uploaded file
    with open(temp_path, "wb") as buffer:
        buffer.write(await model.read())
    
    # Determine final filename and path
    if convert_to_glb_format and file_ext != '.glb':
        # Generate GLB filename
        base_name = os.path.splitext(filename)[0]
        glb_filename = f"{base_name}.glb"
        output_path = os.path.join('static/models', glb_filename)
        
        # Convert to GLB
        result_path = convert_to_glb(temp_path, output_path)
        if not result_path:
            # Clean up temp file
            os.remove(temp_path)
            raise HTTPException(status_code=500, detail="Failed to convert model to GLB format")
        
        # Clean up temp file
        os.remove(temp_path)
        return {"success": True, "filename": glb_filename, "converted": True}
    else:
        # Just move the file to the models directory
        final_path = os.path.join('static/models', filename)
        shutil.move(temp_path, final_path)
        return {"success": True, "filename": filename, "converted": False}

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
    # Create necessary directories
    os.makedirs('static/models', exist_ok=True)
    os.makedirs('temp_uploads', exist_ok=True)
    os.makedirs('temp_conversions', exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
