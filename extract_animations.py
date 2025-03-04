#!/usr/bin/env python
"""
Blender Python script to extract animation information from a 3D model
To be called from Blender's Python interpreter
"""

import bpy
import sys
import os
import json

def clear_scene():
    """Clear the current scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Also clear mesh, material, etc. data blocks
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
            
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
            
    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)
            
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

def extract_animation_info(model_path, output_json_path):
    """Extract animation information from a model and save it to a JSON file"""
    # Clear existing scene
    clear_scene()
    
    # Get file extension
    file_ext = os.path.splitext(model_path)[1].lower()
    
    # Only GLB/GLTF files are supported for animation extraction
    if file_ext not in ['.glb', '.gltf']:
        result = {
            "supports_animation": False,
            "animations": []
        }
        with open(output_json_path, 'w') as f:
            json.dump(result, f)
        return
    
    # Import the model
    bpy.ops.import_scene.gltf(filepath=model_path)
    
    # Extract animation information
    animations = []
    
    # Check if there are any animations
    if bpy.data.actions:
        for action in bpy.data.actions:
            # Get animation duration
            frame_range = action.frame_range
            duration = frame_range[1] - frame_range[0]
            
            # Get animation name
            name = action.name
            
            # Get affected objects/bones
            affected_objects = set()
            for fcurve in action.fcurves:
                data_path = fcurve.data_path
                if "pose.bones" in data_path:
                    # Extract bone name
                    bone_name = data_path.split('"')[1]
                    affected_objects.add(f"Bone: {bone_name}")
                else:
                    # Add object name
                    affected_objects.add("Object animation")
            
            animations.append({
                "name": name,
                "duration_frames": duration,
                "affected_elements": list(affected_objects)
            })
    
    # Prepare the result
    result = {
        "supports_animation": True,
        "animations": animations
    }
    
    # Save the result to a JSON file
    with open(output_json_path, 'w') as f:
        json.dump(result, f)
    
    print(f"Successfully extracted animation information from {model_path}")

if __name__ == "__main__":
    # Get command line arguments passed after "--"
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # Get all args after "--"
    
    if len(argv) != 2:
        print("Usage: blender --background --python extract_animations.py -- model_path output_json_path")
        sys.exit(1)
    
    model_path = argv[0]
    output_json_path = argv[1]
    
    extract_animation_info(model_path, output_json_path)
