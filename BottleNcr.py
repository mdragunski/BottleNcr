import arcpy
import os
import platform
import subprocess

import FinalScript
import validator
import timeseries
import visualizer

points = arcpy.GetParameterAsText(0)
outputFolder = arcpy.GetParameterAsText(1)
#points = "C:\\Users\\nico\\Desktop\\EoTData\\smartphone_data\\tp1_17-17-11_nach-abpfiff.shp"
#points = "C:\\Users\\n_stef05\\Desktop\\EoTData\\EoTData\\smartphone_data\\tp1_17-17-11_nach-abpfiff.shp"

def getFileName(path):
    fn = os.path.basename(path)
    fn = fn[:len(fn)-4]
    return fn

filename = getFileName(points)
validated_shapefile = validator.validateShapefile(points)
points_with_speed = FinalScript.calculateSpeed(validated_shapefile)
timeseries.init(points_with_speed, outputFolder, filename)
visualizer.init(points_with_speed)

# taken from https://stackoverflow.com/a/16204023
if platform.system() == "Windows":
    os.startfile(outputFolder)
elif platform.system() == "Darwin":
    subprocess.Popen(["open", outputFolder])
else:
    subprocess.Popen(["xdg-open", outputFolder])

