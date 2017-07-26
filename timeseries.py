import arcpy
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import datetime as dt
import numpy as np
import time

speed_data = []
accuracy_data = []
time_data = []

def init(input_shp, outputFolder, fn):

    searchCursor = arcpy.SearchCursor(input_shp)

    for row in searchCursor:
        speed_data.append(row.getValue("bttlNcr"))
        accuracy_data.append(row.getValue("accuracy"))
        fmt = "%Y-%m-%d_%H-%M-%S"
        date = dt.datetime.strptime(row.getValue("date"), fmt)
        time_data.append(date)
    del searchCursor

    displaySpeedPlot(outputFolder, fn)
    displayAccuracyPlot(outputFolder, fn)
    displaySpeedHist(outputFolder, fn)


def displaySpeedPlot(outputFolder, fn):
    fig, ax1 = plt.subplots(nrows = 1, sharex = True)

    mean = np.mean(speed_data)
    mean_data = [mean] * len(time_data)

    # Styling
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.grid(True)
    ax1.plot(time_data, speed_data, 'r-')
    ax1.plot(time_data, mean_data, 'b-')

    # Titles
    fig.suptitle("Speed over Time")
    ax1.set_xlabel("t")
    ax1.set_ylabel("km / h")

    # Legend

    speedPatch = mpatches.Patch(color='red', label='Speed in km/h')

    labelString = "Average Speed: %s km/h" % round(mean,3)
    averagePatch = mpatches.Patch(color='blue', label=labelString)

    plt.legend(handles=[speedPatch,averagePatch])

    #save as png
    imageOut = outputFolder + os.sep + fn + "_bttlNcr_speed.png"
    fig.savefig(imageOut, dpi=fig.dpi)


def displayAccuracyPlot(outputFolder, fn):
    fig, ax1 = plt.subplots(nrows = 1, sharex = True)

    mean = np.mean(accuracy_data)
    mean_data = [mean] * len(time_data)

    # Styling
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.grid(True)
    ax1.plot(time_data, accuracy_data, 'r-')
    ax1.plot(time_data, mean_data, 'b-')

    # Titles
    fig.suptitle("Accuracy over Time")
    ax1.set_xlabel("t")
    ax1.set_ylabel("Accuracy in m")

    # Legend
    accuracyPatch = mpatches.Patch(color='red', label="Accuracy in meters")
    averagePatch = mpatches.Patch(color='blue', label="Average Accuracy")

    plt.legend(handles=[accuracyPatch,averagePatch])

    #save as png
    imageOut = outputFolder + os.sep + fn + "_bttlNcr_accuracy.png"
    fig.savefig(imageOut, dpi=fig.dpi)


def displaySpeedHist(outputFolder, fn):

    fig = plt.figure()

    # Support for dynamic histogram bin size has been added in
    # numpy v. 1.11.0
    if np.version.version < '1.11.0':
        plt.hist(speed_data, bins=5)
        arcpy.AddMessage('###UPDATE NUMPY TO GET BETTER RESULTS###')
    else:
        plt.hist(speed_data, bins='auto')

    plt.xlabel('Speed Values')
    plt.ylabel('Frequency')

    plt.title('Frequency of Speed Values')

    imageOut = outputFolder + os.sep + fn + "_bttlNcr_hist.png"
    fig.savefig(imageOut, dpi=fig.dpi)
