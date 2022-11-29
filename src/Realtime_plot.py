import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
from matplotlib.ticker import FormatStrFormatter
from sql_io import *
from line_notify import message2line


columns_name = ['latitude', 'longitude', 'Humidity', 'Tempture', 'PH', 'TDS', 'Water_Temp']
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
abnormal_count = 0
number_data_show = 20

connection = db_connection()
data = load_data(fromCSV = False , connection = connection ,N = 20) # load data from database
print(data)
print(data.shape)



# get the standard deviation and mean of each column from data
# Index : [ 'Humidity', 'Tempture', 'PH', 'TDS', 'Water_Temp' ]
mean = np.mean(data[:,2:7], axis=0)
print(mean)
std = np.zeros(5)
for i in range(2,7):
    std[i-3] = np.std(data[:,i])
print(std)

def data_update(data):
    new_data = load_data(fromCSV = False , connection = connection , N=1)
    print(new_data)
    
    # If new_data is not same as last data , then append it to data and delete the first row
    if not np.array_equal(new_data, data[-1,:]):
        data = np.append(data, new_data, axis=0)
    else:
        print("Same data")
        data = np.append(data, new_data, axis=0)
    data = np.delete(data, 0, axis=0)
    # print(data.shape)
    return data

def abnormal_check(data , data_mean , data_std ):
    """
    @ data : input data , shape = (1,7)
    @ data_mean : mean of each column , shape = (1,5)
    @ data_std : standard deviation of each column , shape = (1,5)
    
    if data is abnormal , return True and the index of abnormal data
    else return False and -1
    abnormal define : 'Humidity', 'Tempture', 'TDS', 'Water_Temp' out of 3 std
    abnormal define : 'PH' out range [6,9]
    """
    # If data shpae is not (1,7) take the last row
    if data.shape[0] != 1:
        data_last = data[-1,:]
    else:
        data_last = data
    
    for i in range(data.shape[0]):
        # check 'Humidity', 'Tempture', 'TDS', 'Water_Temp' out of 3 std
        if (data_last[i+2] > data_mean[i] + 3*data_std[i]) or (data_last[i+2] < data_mean[i] - 3*data_std[i]):
            return True , i+2
        # if 'PH' out range [6,9]
        elif (data_last[i+2] > 9) or (data_last[i+2] < 6):
            return True , i+2
    # None of the data is abnormal
    return False , -1
    

# columns_name = ['latitude', 'longitude', 'Humidity', 'Tempture', 'PH', 'TDS', 'Water_Temp']

# err_index = 3
# error_message = """\nError Type : {} \nTime: {} \nError Value : {} \nLocation: {} , {} \nOther Info: {} \n""".format(columns_name[err_index], datetime.datetime.now(), data[-1, err_index], data[-1,0], data[-1,1], data[-1, 2:7])
# message2line(error_message)

# plt the data using matplotlib
fig = plt.figure(1) #n must be a different integer for every window

legend_counter = 0
error_counter = 0
error_counter_bound = 3

# While keyborad interrupt , close the figure
while True :
    for i in range(2,7):
        # if data row bigger than number_data_show , plot the last number_data_show row data , else plot all data
        if data.shape[0] >= number_data_show:
            plt.plot(data[-number_data_show:,i], colors[i-2], label=columns_name[i] ,marker='o')
        else:
            plt.plot(data[:,i], colors[i-2], label=columns_name[i] , marker='o')
            
        # text the last data on the plot
        # data_text1 = ax.text(0.05, 0.9, '', transform=ax.transAxes,color=colors[3])
        # data_text2 = ax.text(0.05, 0.8, '', transform=ax.transAxes,color=colors[4])
        # data_text3 = ax.text(0.05, 0.7, '', transform=ax.transAxes,color=colors[5])
        # data_text4 = ax.text(0.05, 0.6, '', transform=ax.transAxes,color=colors[6])
        plt.text(0.05, 0.9, 'Humidity : ' + str(data[-1,2]), color=colors[2], transform=plt.gca().transAxes)
        plt.text(0.05, 0.8, 'Tempture : ' + str(data[-1,3]), color=colors[3], transform=plt.gca().transAxes)
        plt.text(0.05, 0.7, 'PH : ' + str(data[-1,4]), color=colors[4], transform=plt.gca().transAxes)
        plt.text(0.05, 0.6, 'TDS : ' + str(data[-1,5]), color=colors[5], transform=plt.gca().transAxes)
        plt.text(0.05, 0.5, 'Water_Temp : ' + str(data[-1,6]), color=colors[6], transform=plt.gca().transAxes)
        
        
    
    if legend_counter == 0:
        plt.legend(loc='upper left')
        legend_counter = 1    
    
    plt.pause(1)
    data = data_update(data)
    mean = np.mean(data[:,2:7], axis=0)
    std = np.zeros(5)
    for i in range(2,7):
        std[i-3] = np.std(data[:,i])
    
    err , err_index = abnormal_check(data , mean , std)
    if err:
        error_counter += 1
        print("Abnormal data: ",columns_name[err_index], ":" ,data[err_index,:])
        
        if error_counter >= error_counter_bound:
            print("Abnormal data is over 3 times , send email")
            error_counter = 0
            error_counter_bound = error_counter_bound**2 # increase the error_counter_bound
            """
            Message to Line
            Error_message:
            \n
            Error Type : columns_name[err_index] \n
            Time: now \n
            Error Type : columns_name[err_index] \n
            Error Value : data[-1, err_index] \n
            Location: latitude , longitude \n
            Other Info: data[-1, 2:7] \n
            https://www.google.com/maps/@{latitude},{longitude},15z
            """
            
            error_message = """\nError Type : {} \nTime: {} \nError Value : {} \nLocation: {} , {} \nOther Info: {} \n"""\
                .format(columns_name[err_index], datetime.datetime.now(), data[-1, err_index], data[-1,0], data[-1,1], data[-1, 2:7])
            error_message += "url = https://www.google.com/maps/@{},{},15z"\
                .format(data[-1,0], data[-1,1])
            message2line(error_message)
            
            
        
        
        ## plot the mean line
        # plt.axhline(y=mean[i-2], color=colors[i], linestyle='--')
        ## plot the standard deviation + mean line
        # plt.axhline(y=mean[i-2]+std[i-2], color=colors[i], linestyle=':')
        # plt.axhline(y=mean[i-2]-std[i-2], color=colors[i], linestyle=':')
    # only legend in the first time

    plt.pause(0.2)
    fig.clear()
plt.show()



connection.close()