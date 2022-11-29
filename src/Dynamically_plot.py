import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter
from sql_io import *
import random
import itertools
fo



connection = db_connection()
data = load_data(fromCSV = True , csv_file_name ="boat_data_1129") # load data from csv
# data = load_data(fromCSV = False , connection = connection) # load data from database
connection.close()
print(data)
print(data.shape)


columns_name = ['latitude', 'longitude', 'Humidity', 'Tempture', 'PH', 'TDS', 'Water_Temp']
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

point_to_show = 10

fig, ax = plt.subplots()

line1, = ax.plot(range(point_to_show),np.zeros(point_to_show)*np.NaN, color=colors[3] ,marker='o', label=columns_name[3])
line2, = ax.plot(range(point_to_show),np.zeros(point_to_show)*np.NaN, color = colors[4],marker='o' ,label=columns_name[4])
line3, = ax.plot(range(point_to_show),np.zeros(point_to_show)*np.NaN, color = colors[5],marker='o',label=columns_name[5])
line4, = ax.plot(range(point_to_show),np.zeros(point_to_show)*np.NaN, color=colors[6],marker='o',label=columns_name[6])
data_text1 = ax.text(0.05, 0.9, '', transform=ax.transAxes,color=colors[3])
data_text2 = ax.text(0.05, 0.8, '', transform=ax.transAxes,color=colors[4])
data_text3 = ax.text(0.05, 0.7, '', transform=ax.transAxes,color=colors[5])
data_text4 = ax.text(0.05, 0.6, '', transform=ax.transAxes,color=colors[6])

ax.set_ylim(0, 100)
ax.set_xlim(0, point_to_show-1)

def update(i):
    # new_data = my_list[i:i+point_to_show]
    
    print(i)
    new_data = data[i:i+point_to_show , 3:7]
    line1.set_ydata(new_data[:,0])
    line2.set_ydata(new_data[:,1])
    line3.set_ydata(new_data[:,2]//10) # TDS is too big , so we need to scale it //10
    line4.set_ydata(new_data[:,3])
    data_text1.set_text('Tempture: {}'.format(new_data[-1,0]))
    data_text2.set_text('PH: {}'.format(new_data[-1,1]))
    data_text3.set_text('TDS: {}'.format(new_data[-1,2]))
    data_text4.set_text('Water_Temp: {}'.format(new_data[-1,3]))
    
    return line1,line2,line3,line4
# https://blog.csdn.net/weixin_43628432/article/details/105879254

ani = animation.FuncAnimation(fig,
                              update,
                              frames=data.shape[0]-point_to_show,
                              interval=200,
                              repeat = False
                              )

plt.show()

# ## Save the animation
# f= r"./animation.gif"
# writergif = animation.PillowWriter(fps=30) 
# ani.save(f, writer=writergif)