import arcpy
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime

arcpy.env.workspace = arcpy.env.scratchFolder


# locs consist of val tuples
# returns distance in km
# shamelessly taken from: https://stackoverflow.com/a/19412565
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
    daysdiff = ((d2-d1).seconds) / 3600.0
    
    try:
        speed = dist/daysdiff
    except ZeroDivisionError:
        speed = 0
    #print "{} km/h".format(speed)
    return speed

def calculateSpeed(points):
    # Get current values from shp and pollute vals variable
    rows = arcpy.SearchCursor(points)
    cursor = arcpy.SearchCursor(points)
    vals = [] # will contain objects with lat, lon, date, speed attributes
    for row in rows:   
        ro = cursor.next()
        lat = ro.getValue("lat")
        lon = ro.getValue("lon")
        date = ro.getValue("date")
        speed = None
        vals.append({"lat": lat, "lon": lon, "date": date, "speed": speed})

    del rows
    del row
    del cursor



    #calculate distances and speed. Set result to attribute speed of each value
    for i, val in enumerate(vals):
        if(i < len(vals)-1):
            dist = getDist(val, vals[i+1])
            val["speed"] = getSpeed(val, vals[i+1], dist)

    arcpy.AddField_management(points, "bttlNcr", "FLOAT")

    #update values
    updatecursor = arcpy.UpdateCursor(points)
    index = 0
    for row in updatecursor:
        if(index < len(vals)-1):
            row.bttlNcr = long(vals[index]["speed"])
            #print vals[index]
        index += 1
        updatecursor.updateRow(row)

    del row
    del updatecursor


    # just for checking if values have been updated
    cursor = arcpy.SearchCursor(points)
    for row in cursor:
        ro = cursor.next()
        #print ro.getValue("FID")
        #print ro.getValue("speed")

    del cursor
    del row

    return points

        

