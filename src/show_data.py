import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter
# from sql_io import read_csv_data
# from sql_io import save_data_to_csv
# from sql_io import select_last_N
from sql_io import *
import datetime

'''
設備異常
    pH連續3點無變化
    導電度為0或超過5,000 μS/cm以 上（偵測極限）
水質異常
    離群值條件（時間):導電度連 續3點超出80或低於20分位
    離群值條件（空間):上下游測 站溫度同時超出80或低於20分位
    法規限值條件:pH低於6或高於9
    離群值條件可以用GMM處理
'''

def load_data(fromCSV = True , connection = None , N=100):
    if fromCSV:
        csv_file_name = "boat_data_1"
        data = read_csv_data(csv_file_name)
    else:
        # load data from database
        data = select_last_N(connection, N)
        # drop first column
        data = data[: ,1 :]
    return data

        
connection = db_connection()
data = load_data(False, connection)
connection.close()
print(data)


columns_name = ['latitude', 'longitude', 'Humidity', 'Tempture', 'PH', 'TDS', 'Water_Temp']
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
## plt the data using matplotlib
plt.figure(1) #n must be a different integer for every window
for i in range(2,7):
    plt.plot(data[:,i], label=columns_name[i],color=colors[i] , marker='o')
    # plt.scatter(np.arange(data.shape[0]),data[:,i] , color=colors[i])
    plt.legend()

plt.savefig('./img/sensor_data_multi{}.png'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
# plt.show(block=False)

## plt multiple plots using matplotlib
fig , ax = plt.subplots(2,3 , figsize=(10,7))
for i in range(2,7):
    if i < 5:
        ax_x,ax_y = 0,i-2
    else:
        ax_x,ax_y = 1,(i-2)%3
    mean = np.mean(data[:,i])
    std = np.std(data[:,i])
    lower = np.percentile(data[:,i],20)
    upper = np.percentile(data[:,i],80)
    
    ax[ax_x,ax_y].plot(data[:,i], label=columns_name[i],color=colors[i])
    ax[ax_x,ax_y].axhline(y=mean, color='g', linestyle='--') # add the mean line
    ax[ax_x,ax_y].text(data.shape[0],mean, 'Mean : {:.2f}'.format(mean), horizontalalignment='center', verticalalignment='center')
    
    ## draw the mean line and text
    if i != 4 :
        ## draw the standard deviation and text
        ax[ax_x,ax_y].axhline(y=mean+std, color='r', linestyle='--') # add the standard deviation line
        ax[ax_x,ax_y].axhline(y=mean-std, color='r', linestyle='--') # add the standard deviation line
        ax[ax_x,ax_y].text(data.shape[0],mean+std, '{:.2f}'.format(mean+std), horizontalalignment='center', verticalalignment='center')
        ax[ax_x,ax_y].text(data.shape[0],mean-std, '{:.2f}'.format(mean-std), horizontalalignment='center', verticalalignment='center')
        
        ## draw the lower 20% and upper 80% line and text
        ax[ax_x,ax_y].axhline(y=lower, color='b', linestyle='--') # add the lower 20% line
        ax[ax_x,ax_y].axhline(y=upper, color='b', linestyle='--') # add the upper 80% line
        
        ## If the data lower than the lower 20% or upper than the upper 80% , we will mark it with red color
        color_map = np.where(data[:,i] <= lower, 'r', np.where(data[:,i] >= upper, 'r', colors[i]))
        ## Draw the scatter plot
        # ax[ax_x,ax_y].scatter(np.arange(data.shape[0]),data[:,i] , color=color_map)
        ax[ax_x,ax_y].scatter(np.arange(data.shape[0]),data[:,i] , color=color_map)
        
        
    elif i == 4:
        ## draw the PH regulation limit and text
        ax[ax_x,ax_y].axhline(y=6, color='r', linestyle='--') # Regulation limit
        ax[ax_x,ax_y].axhline(y=9, color='r', linestyle='--') # Regulation limit
        ax[ax_x,ax_y].text(data.shape[0],6, '6', horizontalalignment='center', verticalalignment='center')
        ax[ax_x,ax_y].text(data.shape[0],9, '9', horizontalalignment='center', verticalalignment='center') 
        
        ## If the PH is lower than 6 or higher than 9, the color will be red else colors[i]
        color_map_PH = np.where(data[:,i] <= 6, 'red', np.where(data[:,i] >= 9, 'red', colors[i]))
        ## Draw the PH data
        ax[ax_x,ax_y].scatter(np.arange(data.shape[0]),data[:,i] , color=color_map_PH)
    
    ##titles the plot
    ax[ax_x,ax_y].set_title(columns_name[i])
    ax[ax_x,ax_y].legend(loc = 'upper left')
    
# plot the longitude and latitude using the scatter plot , no x y axis
## if the water temperature is higher than 30 degree , the color will be red
scatter_color = np.where(data[:,6] > 30, 'r', 'b')

# ax[1,2].scatter(data[:,1],data[:,0], color='b')
ax[1,2].scatter(data[:,1],data[:,0], color=scatter_color)
## lable sequencial number in every point
for i in range(data.shape[0]):
    # ax[1,2].text(data[i,1],data[i,0],i, horizontalalignment='right', verticalalignment='top')
    ax[1,2].text(data[i,1],data[i,0],i,horizontalalignment='right', verticalalignment='top')
ax[1,2].set_title('GPS location')
ax[1,2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[1,2].xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    
plt.show()

# Save the figure
fig.savefig('./img/sensor_data_multi{}.png'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))

