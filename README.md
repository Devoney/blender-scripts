# blender-scripts
Collection of scripts for Blender of various purposes.

## Build
### Export.py

Exports a collection of meshes/objects, with various levels of detail.

Usage:
1. Put all meshes/objects to export inside a collection. You can create multiple collections to export if you want.
2. Give the collections a meaningful name.
3. Open Export.py and set the names of the collections in the variable called *collectionNames*.
4. Set the desired levels of quality to export in the variable *qualityLevels*.
5. Run the script in blender. A local subdirectory called *Export* will be created.
