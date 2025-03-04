#!/usr/bin/env python
"""
Blender Python script to convert 3D models to GLB format
To be called from Blender's Python interpreter
"""

import bpy
import sys
import os

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

def convert_to_glb(input_path, output_path):
    """Convert a 3D model to GLB format"""
    # Clear existing scene
    clear_scene()
    
    # Get file extension
    file_ext = os.path.splitext(input_path)[1].lower()
    
    # Import based on file type
    if file_ext == '.obj':
        bpy.ops.import_scene.obj(filepath=input_path)
    elif file_ext == '.fbx':
        bpy.ops.import_scene.fbx(filepath=input_path)
    elif file_ext == '.stl':
        bpy.ops.import_mesh.stl(filepath=input_path)
    elif file_ext == '.dae':
        bpy.ops.wm.collada_import(filepath=input_path)
    elif file_ext in ['.glb', '.gltf']:
        bpy.ops.import_scene.gltf(filepath=input_path)
    else:
        print(f"Unsupported file format: {file_ext}")
        sys.exit(1)
    
    # Export as GLB
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_texcoords=True,
        export_normals=True,
        export_materials=True
    )
    
    print(f"Successfully converted {input_path} to {output_path}")

if __name__ == "__main__":
    # Get command line arguments passed after "--"
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # Get all args after "--"
    
    if len(argv) < 2:
        print("Usage: blender --background --python convert_model.py -- input_file output_file [preserve_animations]")
        sys.exit(1)
        
    input_path = argv[0]
    output_path = argv[1]
    
    # Default to preserving animations
    preserve_animations = True
    if len(argv) > 2:
        preserve_animations = argv[2].lower() == 'true'
    
    # Update export options based on animation preservation flag
    export_options = {
        'filepath': output_path,
        'export_format': 'GLB',
        'export_texcoords': True,
        'export_normals': True,
        'export_materials': True,
        'export_animations': preserve_animations
    }
    
    # Clear the scene
    clear_scene()
    
    # Get file extension
    file_ext = os.path.splitext(input_path)[1].lower()
    
    # Import based on file type
    if file_ext == '.obj':
        bpy.ops.import_scene.obj(filepath=input_path)
    elif file_ext == '.fbx':
        bpy.ops.import_scene.fbx(filepath=input_path)
    elif file_ext == '.stl':
        bpy.ops.import_mesh.stl(filepath=input_path)
    elif file_ext == '.dae':
        bpy.ops.wm.collada_import(filepath=input_path)
    elif file_ext in ['.glb', '.gltf']:
        bpy.ops.import_scene.gltf(filepath=input_path)
    elif file_ext == '.blend':
        # For .blend files, we need to append objects from the file
        with bpy.data.libraries.load(input_path) as (data_from, data_to):
            data_to.objects = data_from.objects
        
        # Link the objects to the scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    else:
        print(f"Unsupported file format: {file_ext}")
        sys.exit(1)
    
    # Export as GLB with the specified options
    bpy.ops.export_scene.gltf(**export_options)
    
    print(f"Successfully converted {input_path} to {output_path} (preserve_animations={preserve_animations})")
