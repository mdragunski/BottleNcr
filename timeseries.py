import arcpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import time

speed_data = []
time_data = []

def plot(input_shp):
    searchCursor = arcpy.SearchCursor(input_shp)
    
    for row in searchCursor:
        speed_data.append(row.getValue("bttlNcr"))
        fmt = "%Y-%m-%d_%H-%M-%S"
        date = dt.datetime.strptime(row.getValue("date"), fmt)
        time_data.append(date)
    
    displayPlot()
    del searchCursor
    
def displayPlot():
    fig, ax1 = plt.subplots(nrows = 1, sharex = True)
    #secondLocator = mdates.SecondLocator()
    #ax1.xaxis.set_minor_locator(secondLocator)
    ax1.plot(time_data, speed_data, 'r-')

    plt.grid(True)
    plt.show()

