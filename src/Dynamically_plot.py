# https://matplotlib.org/stable/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
# https://matplotlib.org/stable/gallery/animation/index.html
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sql_io import read_csv_data
from sql_io import save_data_to_csv

import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter
from sql_io import read_csv_data
from sql_io import save_data_to_csv



csv_file_name = "boat_data_1"
data = read_csv_data(csv_file_name)
columns_name = ['latitude', 'longitude', 'Humidity', 'Tempture', 'PH', 'TDS', 'Water_Temp']
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
print(data.shape)

# ## plt the data using matplotlib
# plt.figure(1) #n must be a different integer for every window
# for i in range(2,7):
#     plt.plot(data[:,i], label=columns_name[i],color=colors[i])
#     plt.scatter(np.arange(data.shape[0]),data[:,i] , color=colors[i])
#     plt.legend()





## Gets new data from the csv file
csv_file_name_2 = "boat_data_2"
new_data = read_csv_data(csv_file_name_2)
## remove first len(data) rows from new_data
new_data = new_data[len(data):,:]


## make plot animation using matplotlib




fig, ax = plt.subplots()
sensor_data = read_csv_data()
print(sensor_data.shape)
x = np.arange(0, sensor_data.shape[0], 1)
line, = ax.plot(x, sensor_data[:,0], lw=2)

def animate(i):
    # if i > sensor_data.shape[0] then generate new data
    if i > sensor_data.shape[0]:
        np.random.seed(19680801)
        line.set_ydata(np.random.rand(100))
        return line,
    line.set_ydata(sensor_data[i,0])  # update the data
    return line,

# ani = animation.FuncAnimation(fig, run, data_gen, interval=100, init_func=init)

# Plot the animation from the sensor data
ani = animation.FuncAnimation(fig, animate , interval=20, blit=True)
plt.show()
