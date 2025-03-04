# Holographic Viewer

A web-based 3D model viewer application that allows users to view, convert, and combine 3D models with animations.

## Features

- View 3D models in a web browser with realistic lighting and effects
- Convert 3D models to compatible formats
- Extract animations from 3D models
- Combine multiple models into a single scene
- Interactive entity simulation environment

## Setup and Installation

1. Clone this repository
2. Install the required dependencies (Python and JavaScript libraries)
3. Run the server with `python server.py`
4. Access the application at http://localhost:5000

## Project Structure

- `server.py` - Flask web server that handles model processing and serving
- `convert_model.py` - Utility for converting 3D models to compatible formats
- `extract_animations.py` - Extracts animations from 3D models
- `combine_models.py` - Combines multiple 3D models into a single scene
- `static/` - Contains JavaScript code and 3D models
- `templates/` - HTML templates for the web interface

## Usage

1. Upload a 3D model through the web interface
2. View the model in the 3D viewer
3. Apply transformations or extract animations as needed
4. Combine models to create complex scenes

## Entity Simulation

The application includes an entity simulation feature that allows for interactive manipulation of 3D models in a physics-based environment.