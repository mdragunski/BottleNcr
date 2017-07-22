import arcpy
from arcpy.sa import *
import os

def init(input_shp):
    #arcpy.env.workspace = arcpy.env.scratchFolder

    arcpy.CheckOutExtension('Spatial')
    arcpy.AddMessage(arcpy.CheckExtension('Spatial'))

    # adding new shapefile to ArcMap
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

    newLayer = arcpy.mapping.Layer(input_shp)
    arcpy.ApplySymbologyFromLayer_management(newLayer, "points_new_style.lyr")
    arcpy.mapping.AddLayer(df, newLayer, "TOP")

    arcpy.env.workspace = arcpy.env.scratchGDB

    arcpy.env.workspace = arcpy.env.scratchFolder
    arcpy.AddMessage(arcpy.env.workspace)
    densityOutput = PointDensity(input_shp, 'accuracy')

    densityOutput.save('density.tif')

    densityLayer = arcpy.mapping.Layer('density.tif')

    arcpy.ApplySymbologyFromLayer_management(densityLayer, "density_style.lyr")
    arcpy.mapping.AddLayer(df, densityLayer, "TOP")
