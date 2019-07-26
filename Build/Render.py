import bpy
import json
import os

renderPath = bpy.path.abspath("//Renders\\")
print('Render path: ' + renderPath)
renderSettingsJsonPath = bpy.path.abspath("//render_settings.json")
print('Settings file: ' + renderSettingsJsonPath)

def ensureDirExists(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def loadRenderSettings():
    file = open(renderSettingsJsonPath,"r+")
    contents = file.read()
    file.close()
    return json.loads(contents)
        
ensureDirExists(renderPath)

renderSettings = loadRenderSettings()
print('Render settings loaded')

for obj in bpy.data.objects:
    if obj.type != "CAMERA":
        continue

    print('Camera with name "' + obj.name +'" found')
    
    renderSettingName = 'default'
    if obj.name in renderSettings:
        print('Render settings for camera found')
        renderSettingName = obj.name
    else:
        print('No settings for camera found, default settings will apply.')

    if renderSettingName not in renderSettings:
        print('No render settings for "' + renderSettingName + '" not found, skipping')
        continue;
    
    bpy.context.scene.camera = obj
    print('Active camera set to ' + obj.name)

    for renderSetting in renderSettings[renderSettingName]:
        resolution = renderSetting['resolution']
        resX = resolution['x']
        resY = resolution['y']
        samples = renderSetting['samples']
        engine = renderSetting['engine']

        fileName = obj.name + "_" + str(resX) + "x" + str(resY) + "_s" + str(samples) + ".png"
        print('Render file name: ' + fileName)

        bpy.context.scene.render.filepath = renderPath + "\\" + fileName
        bpy.context.scene.render.resolution_x = resX
        bpy.context.scene.render.resolution_y = resY
        bpy.context.scene.render.engine = engine
                
        if engine == 'CYCLES':
            bpy.context.scene.cycles.samples = samples
        elif engine == 'EEVEE':
            bpy.context.scene.eevee.taa_render_samples = samples
        print('Render engine settings set')
        
        print('Render start')
        bpy.ops.render.render(write_still=True)
        print('Render finished')