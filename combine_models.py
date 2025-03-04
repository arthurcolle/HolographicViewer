#!/usr/bin/env python
"""
Blender Python script to combine multiple 3D models into a single GLB file
To be called from Blender's Python interpreter
"""

import bpy
import sys
import os
import json
import math

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

def import_model(model_path):
    """Import a model based on its file extension"""
    file_ext = os.path.splitext(model_path)[1].lower()
    
    if file_ext == '.obj':
        bpy.ops.import_scene.obj(filepath=model_path)
    elif file_ext == '.fbx':
        bpy.ops.import_scene.fbx(filepath=model_path)
    elif file_ext == '.stl':
        bpy.ops.import_mesh.stl(filepath=model_path)
    elif file_ext == '.dae':
        bpy.ops.wm.collada_import(filepath=model_path)
    elif file_ext in ['.glb', '.gltf']:
        bpy.ops.import_scene.gltf(filepath=model_path)
    elif file_ext == '.blend':
        # For .blend files, we need to append objects from the file
        with bpy.data.libraries.load(model_path) as (data_from, data_to):
            data_to.objects = data_from.objects
        
        # Link the objects to the scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    else:
        print(f"Unsupported file format: {file_ext}")
        return False
    
    return True

def apply_transform(obj_idx, position_data):
    """Apply position, rotation, and scale to the selected objects"""
    if str(obj_idx) not in position_data:
        return
    
    data = position_data[str(obj_idx)]
    selected_objects = bpy.context.selected_objects
    
    for obj in selected_objects:
        # Apply position if provided
        if "position" in data and len(data["position"]) == 3:
            obj.location = (
                data["position"][0],
                data["position"][1],
                data["position"][2]
            )
        
        # Apply rotation if provided (in degrees, convert to radians)
        if "rotation" in data and len(data["rotation"]) == 3:
            obj.rotation_euler = (
                math.radians(data["rotation"][0]),
                math.radians(data["rotation"][1]),
                math.radians(data["rotation"][2])
            )
        
        # Apply scale if provided
        if "scale" in data:
            if isinstance(data["scale"], list) and len(data["scale"]) == 3:
                obj.scale = (
                    data["scale"][0],
                    data["scale"][1],
                    data["scale"][2]
                )
            elif isinstance(data["scale"], (int, float)):
                obj.scale = (
                    data["scale"],
                    data["scale"],
                    data["scale"]
                )

def combine_models(model_paths, output_path, position_data_path):
    """Combine multiple models into a single GLB file"""
    # Clear existing scene
    clear_scene()
    
    # Load position data if available
    position_data = {}
    if os.path.exists(position_data_path):
        try:
            with open(position_data_path, 'r') as f:
                position_data = json.load(f)
        except Exception as e:
            print(f"Error loading position data: {str(e)}")
    
    # Import each model and apply transformations
    for i, model_path in enumerate(model_paths):
        # Deselect all objects before importing
        bpy.ops.object.select_all(action='DESELECT')
        
        # Get current object count to identify new objects
        prev_obj_count = len(bpy.context.scene.objects)
        
        # Import the model
        success = import_model(model_path)
        if not success:
            print(f"Failed to import model: {model_path}")
            continue
        
        # Select only the newly added objects
        for obj in bpy.context.scene.objects:
            if obj not in bpy.context.selected_objects:
                if len(bpy.context.scene.objects) > prev_obj_count:
                    obj.select_set(True)
        
        # Apply transformations from position data
        apply_transform(i, position_data)
    
    # Export the combined model as GLB
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_texcoords=True,
        export_normals=True,
        export_materials=True,
        export_animations=True
    )
    
    print(f"Successfully combined models into {output_path}")

if __name__ == "__main__":
    # Get command line arguments passed after "--"
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # Get all args after "--"
    
    if len(argv) < 2:
        print("Usage: blender --background --python combine_models.py -- model_paths output_file position_data_file")
        print("model_paths should be comma-separated list of file paths")
        sys.exit(1)
    
    model_paths_str = argv[0]
    output_path = argv[1]
    position_data_path = argv[2] if len(argv) > 2 else ""
    
    # Split the comma-separated model paths
    model_paths = model_paths_str.split(',')
    
    combine_models(model_paths, output_path, position_data_path)
