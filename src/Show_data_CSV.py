import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sql_io import read_csv_data
from sql_io import save_data_to_csv




data = read_csv_data()
columns_name = ['latitude', 'longitude', 'O_Hum', 'O_Temp', 'PH', 'TDS', 'W_Temp']
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

# # plt the data using matplotlib
# for i in range(2,7):
#     plt.plot(data[:,i], label=columns_name[i],color=colors[i])
#     plt.scatter(np.arange(data.shape[0]),data[:,i] , color=colors[i])
#     plt.legend()
# plt.show()


    
'''
水質異常
    離群值條件（時間）：導電度連續3點超出80或低於20分位
    離群值條件（空間）：上下游測站溫度同時超出80或低於20分位
    法規限值條件 ： pH低於6或高於9
'''
## plt multiple plots using matplotlib
fig , ax = plt.subplots(2,3 , figsize=(15,10))




for i in range(2,7):
    if i < 5:
        ax_x,ax_y = 0,i-2
    else:
        ax_x,ax_y = 1,(i-2)%3
    ax[ax_x,ax_y].plot(data[:,i], label=columns_name[i],color=colors[i])
    ax[ax_x,ax_y].scatter(np.arange(data.shape[0]),data[:,i] , color=colors[i])
    ## draw the mean line and text
    mean = np.mean(data[:,i])
    ax[ax_x,ax_y].axhline(y=mean, color='g', linestyle='--') # add the mean line
    ax[ax_x,ax_y].text(data.shape[0],mean, 'Mean : {:.2f}'.format(mean), horizontalalignment='center', verticalalignment='center')
    
    if i != 4 :
        ## draw the standard deviation and text
        std = np.std(data[:,i])
        ax[ax_x,ax_y].axhline(y=mean+std, color='r', linestyle='--') # add the standard deviation line
        ax[ax_x,ax_y].axhline(y=mean-std, color='r', linestyle='--') # add the standard deviation line
        ax[ax_x,ax_y].text(data.shape[0],mean+std, '{:.2f}'.format(mean+std), horizontalalignment='center', verticalalignment='center')
        ax[ax_x,ax_y].text(data.shape[0],mean-std, '{:.2f}'.format(mean-std), horizontalalignment='center', verticalalignment='center')
        
        ## draw the lower 20% and upper 80% line and text
        lower = np.percentile(data[:,i],20)
        upper = np.percentile(data[:,i],80)
        ax[ax_x,ax_y].axhline(y=lower, color='b', linestyle='--') # add the lower 20% line
        ax[ax_x,ax_y].axhline(y=upper, color='b', linestyle='--') # add the upper 80% line
        
    elif i == 4:
        ## draw the PH regulation limit and text
        ax[ax_x,ax_y].axhline(y=6, color='r', linestyle='--') # Regulation limit
        ax[ax_x,ax_y].axhline(y=9, color='r', linestyle='--') # Regulation limit
        ax[ax_x,ax_y].text(data.shape[0],6, '6', horizontalalignment='center', verticalalignment='center')
        ax[ax_x,ax_y].text(data.shape[0],9, '9', horizontalalignment='center', verticalalignment='center')    
    
    # titles the plot
    ax[ax_x,ax_y].set_title(columns_name[i])
    ax[ax_x,ax_y].legend(loc = 'upper left')
    
# plot the longitude and latitude using the scatter plot
ax[1,2].scatter(data[:,1],data[:,0], color='b')
        
    
plt.show()

