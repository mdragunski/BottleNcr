import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import time

value = range(1, 20)
ti = []

for i in range(1,20):
    ti.append(datetime.datetime.now())
    time.sleep(1)
    
fig, ax = plt.subplots()
ax.plot_date(x=ti, y=value, fmt="r-")
ax.set_xlim(ti[0], ti[len(ti)-1])
ax.grid(True)
fig.show()
