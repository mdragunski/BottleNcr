import arcpy
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime

arcpy.env.workspace = "C:/Users/n_stef05/Desktop/smartphone_data"

points = "tp1_17-17-11_nach-abpfiff.shp"

rows = arcpy.SearchCursor(points)
columns = arcpy.ListFields(points)

# locs consist of val tuples
# returns distance in km
def getDist(loc1, loc2):
    R = 6373.0
    d_lon = radians(loc2["lon"]) - radians(loc1["lon"])
    d_lat = radians(loc2["lat"]) - radians(loc1["lat"])
    a = sin(d_lat/2)**2 + cos(loc1["lat"])*cos(loc2["lat"]) * sin(d_lon/2) ** 2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

# calculate speed from distance
def getSpeed(loc1, loc2, dist):
    fmt = "%Y-%m-%d_%H-%M-%S"
    d1 = datetime.strptime(loc1["date"], fmt)
    d2 = datetime.strptime(loc2["date"], fmt)
    daysdiff = ((d2-d1).seconds) * 3600
    speed = dist/daysdiff
    #print "{} km/h".format(speed)
    return speed
    

# Get current values from shp and pollute vals variable
cursor = arcpy.SearchCursor(points)
vals = [] # will contain objects with lat, lon, date, speed attributes
for row in rows:   
    ro = cursor.next()
    lat = ro.getValue("lat")
    lon = ro.getValue("lon")
    date = ro.getValue("date")
    speed = None
    vals.append({"lat": lat, "lon": lon, "date": date, "speed": speed})

del cursor

#calculate distances and speed. Set result to attribute speed of each value
for i, val in enumerate(vals):
    if(i < len(vals)-1):
        dist = getDist(val, vals[i+1])
        val["speed"] = getSpeed(val, vals[i+1], dist)

#Update values in fields
updateCursor = arcpy.UpdateCursor(points)
i = 0
for row in updateCursor:
    if(i > len(vals)-1):
        row.setValue("speed", vals[i]["speed"])
        updateCursor.updateRow(row)
        i = i + 1
    print vals[i]

del updateCursor

# just for checking if values have been updated
cur = arcpy.SearchCursor(points)
for row in rows:
    ro = cur.next()
    print ro.getValue("speed")

del cur
