# blender-scripts
Collection of scripts for Blender of various purposes.

## Build
### Export.py

Exports a collection of meshes/objects, with various levels of detail. The level of detail is altered by setting the levels of the subdivision modifier. If an object has none, this is skipped. If there are no objects with a subdvision modifier inside a collection, this step is skipped as well.
For now STL and FBX is supported.

Usage:
1. Put all meshes/objects to export inside a collection. You can create multiple collections to export if you want.
2. Give the collections a meaningful name.
3. Open Export.py and set the names of the collections in the variable called *collectionNames*.
4. Set the desired levels of quality to export in the variable *qualityLevels*.
5. Set the file types you wish to export in *exportFileTypes*, currently FBX, OBJ and STL are supported.
6. Run the script in blender. A local subdirectory called *Export* will be created.
