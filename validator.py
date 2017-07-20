# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# validator.py
# Created on: 2017-07-17 18:17:04.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import matplotlib.pyplot as plt



# Local variables:
arcpy.env.workspace = arcpy.env.scratchFolder
points = arcpy.GetParameterAsText(0)
points_statistics = "points_statistics.dbf"
pointsNew = "points_new.shp"

mean = 0
std = 0
threshold = 0

fig, ax = plt.subplots()


# overwriting output
arcpy.env.overwriteOutput = True

arcpy.Copy_management(points, pointsNew)

# generate statistics
print "calculating statistics..."
arcpy.Statistics_analysis(points, points_statistics, [["accuracy", "MEAN"], ["accuracy", "STD"]])

# looping through statistics table and saving MEAN accuracy and STD (standard deviation) accuracy
print "getting mean and std"
rows = arcpy.SearchCursor(points_statistics)
fields = arcpy.ListFields(points_statistics)
for field in fields:
    cursor = arcpy.SearchCursor(points_statistics, "", "", field.name)
    row = cursor.next()
    field_value = row.getValue(field.name)
    del cursor
    if "MEAN" in field.name:
        mean = field_value
    if "STD" in field.name:
        std = field_value

threshold = mean + std

print "using threshold: ", threshold

# deleting rows depending on accuracy
with arcpy.da.UpdateCursor(pointsNew, "accuracy") as cursor:
    for row in cursor:
        if row[0] > threshold:
            cursor.deleteRow()

# adding new shapefile to ArcMap 
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
newLayer = arcpy.mapping.Layer(pointsNew)

arcpy.ApplySymbologyFromLayer_management(newLayer, "points_new_style.lyr")

arcpy.mapping.AddLayer(df, newLayer, "TOP")
