import arcpy

import FinalScript
import validator
import timeseries

#points = arcpy.GetParameterAsText(0)
points = "C:\\Users\\nico\\Desktop\\EoTData\\smartphone_data\\tp1_17-17-11_nach-abpfiff.shp"

validated_shapefile = validator.validateShapefile(points)
points_with_speed = FinalScript.calculateSpeed(validated_shapefile)
timeseries.plot(points_with_speed)

# adding new shapefile to ArcMap 
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
newLayer = arcpy.mapping.Layer(points_with_speed)
arcpy.ApplySymbologyFromLayer_management(newLayer, "points_new_style.lyr")
arcpy.mapping.AddLayer(df, newLayer, "TOP")
