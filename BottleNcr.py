import arcpy

import FinalScript
import validator
import timeseries
import visualizer

points = arcpy.GetParameterAsText(0)
outputFolder = arcpy.GetParameterAsText(1)
#points = "C:\\Users\\nico\\Desktop\\EoTData\\smartphone_data\\tp1_17-17-11_nach-abpfiff.shp"
#points = "C:\\Users\\n_stef05\\Desktop\\EoTData\\EoTData\\smartphone_data\\tp1_17-17-11_nach-abpfiff.shp"

validated_shapefile = validator.validateShapefile(points)
points_with_speed = FinalScript.calculateSpeed(validated_shapefile)
timeseries.init(points_with_speed, outputFolder)
visualizer.init(points_with_speed)

# adding new shapefile to ArcMap 
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
newLayer = arcpy.mapping.Layer(points_with_speed)
arcpy.ApplySymbologyFromLayer_management(newLayer, "points_new_style.lyr")
arcpy.mapping.AddLayer(df, newLayer, "TOP")

# taken from https://stackoverflow.com/a/16204023
import os
import platform
import subprocess

if platform.system() == "Windows":
    os.startfile(outputFolder)
elif platform.system() == "Darwin":
    subprocess.Popen(["open", outputFolder])
else:
    subprocess.Popen(["xdg-open", outputFolder])
