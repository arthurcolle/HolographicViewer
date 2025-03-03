import flask
from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/models')
def list_models():
    models = {
        "aircraft": ["f16.glb", "b2_spirit.glb", "helicopter.glb", "commercial_airliner.glb"],
        "vehicles": ["car.glb", "truck.glb", "tank.glb", "train.glb"],
        "city": ["new_york.glb", "tokyo.glb", "london.glb", "custom_city.glb"]
    }
    return jsonify(models)

@app.route('/scenarios')
def list_scenarios():
    scenarios = [
        {"id": "city_flyover", "name": "City Flyover", "description": "Aircraft flying over a city"},
        {"id": "ground_vehicles", "name": "Ground Vehicle Simulation", "description": "Vehicles moving through city streets"},
        {"id": "military_op", "name": "Military Operation", "description": "Combined aircraft and ground vehicle operation"}
    ]
    return jsonify(scenarios)

@app.route('/load_scenario/<scenario_id>')
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
        return jsonify(scenario_configs[scenario_id])
    else:
        return jsonify({"error": "Scenario not found"}), 404

@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'model' not in request.files:
        return jsonify({"error": "No model file provided"}), 400
    
    file = request.files['model']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if file and file.filename.endswith('.glb'):
        # Save the file
        filepath = os.path.join('static/models', file.filename)
        file.save(filepath)
        return jsonify({"success": True, "filename": file.filename})
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    # Ensure the models directory exists
    os.makedirs('static/models', exist_ok=True)
    app.run(debug=True)
