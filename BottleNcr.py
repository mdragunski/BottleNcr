import FinalScript
import validator

import arcpy


points = arcpy.GetParameterAsText(0)

validated_shapefile = validator.validateShapefile(points)
pointsNew = FinalScript.calculateSpeed(validated_shapefile)


# adding new shapefile to ArcMap 
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
newLayer = arcpy.mapping.Layer(pointsNew)
arcpy.ApplySymbologyFromLayer_management(newLayer, "points_new_style.lyr")
arcpy.mapping.AddLayer(df, newLayer, "TOP")
