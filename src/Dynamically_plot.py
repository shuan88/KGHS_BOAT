# https://matplotlib.org/stable/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
# https://matplotlib.org/stable/gallery/animation/index.html
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sql_io import read_csv_data
from sql_io import save_data_to_csv




def data_gen():
    for cnt in itertools.count():
        t = cnt / 10
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)




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
