# Animation
# https://vimsky.com/zh-tw/examples/detail/python-method-matplotlib.pyplot.pause.html


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from os import listdir
from os.path import isdir, isfile, join
import pandas as pd

window_size = 10240

state = ["normal","error"]
text_color = ["b","r"]


## load data from CSV
# shuan-kghs  latitude  longitude  O_Hum  O_Temp  PH  TDS  Time  W_Temp
data_name = "csv_file/results.csv"
data_read = pd.read_csv(data_name, header=0)
# data_read= data_read.dropna()
print(data_read.head())
# print(data_read[["shuan-kghs","PH"]])

# Covert pd to np array
data = data_read.to_numpy()

print(data.shape)
print(data[0][1])


## Load data from numpy
# data_name = "./realdata/needle_50.npy"
# data_read = np.load(data_name)


for i in range(data_read.shape[0]//window_size):
    
    # print(data_read.shape[:])
    plt.plot(data_read[i*window_size : (i+1)*window_size , :] ,label='cubic')
    
    plt.title("data{} state:{}".format(i,state[i%2]),color=text_color[i%2])
    # plt.legend()
    
    # plt.plot(data_read[: 1024 ,0], color = 'b')
    # plt.plot(data_read[: 5120 ,1], color = 'g')
    # plt.plot(data_read[: 5120 ,2], color = 'b')
    plt.pause(0.5)
    plt.clf()


plt.show()