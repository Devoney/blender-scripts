import os
import subprocess
from subprocess import run

openscadPath = "C:\\Program Files\\OpenSCAD\\openscad.exe"

def stlToDxf(stlFilePath):
  stlTo(stlFilePath, 'dxf')

def stlTo(stlFilePath, fileFormats):
  openscadFileContents = "projection(cut=false) {\r\nimport(\"" + stlFilePath.replace('\\', '\\\\') + "\", convexity=10);\r\n}"
  filepath = os.path.splitext(stlFilePath)[0] + '.scad'  
  f = open(filepath, "w")
  f.write(openscadFileContents)
  f.close()
  if type(fileFormats) is str:
    fileFormats = [fileFormats]
  
  for fileFormat in fileFormats:
    outputFile = (os.path.splitext(stlFilePath)[0] + '.' + fileFormat)
    _export(filepath, outputFile)

def _export(file, outputFile):
  commands = [
    openscadPath,
    "-o",
    outputFile,
    file
  ]
  rc = run(commands)