import json
import numpy as np
import sklearn 
import matplotlib.pyplot as plt
import random
from shapely.geometry import Polygon,LineString,MultiPoint,Point
from descartes import PolygonPatch
from itertools import product


    


def heatmap_generator(polygon_bounds):
    p =Polygon(polygon_bounds)
    xmin, ymin, xmax, ymax = p.bounds # get the bounds of the polygon
    n = 1e4 # number of points
    x = np.arange(np.floor(xmin * n) / n, np.ceil(xmax * n) / n, 1 / n)  # array([-4.857, -4.856, -4.855, -4.854, -4.853])
    y = np.arange(np.floor(ymin * n) / n, np.ceil(ymax * n) / n, 1 / n)  # array([37.174, 37.175, 37.176, 37.177, 37.178, 37.179, 37.18 , 37.181, 37.182, 37.183, 37.184, 37.185])
    points = MultiPoint(np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))]))
    result = points.intersection(p)

    ## shapely.geometry.multipoint.MultiPoint to list
    python_list = []
    for i in range(len(result)):
        python_list.append([float(x) for x in str(result[i]).replace('POINT (','').replace(')','').split(' ')])

    heatmap = np.array(python_list)
    # np.random.normal(Mean, Standard Deviation), len(python_list))
    heat_data= np.random.normal(0,1,len(python_list))
    # append the heat_data to the heatmap array (639,2) to (639,3)
    heatmap = np.append(heatmap,heat_data.reshape(len(heat_data),1),axis=1)
    return heatmap

polygon_bounds = [[120.2887400904234, 22.626811224004697], [120.28797553656432, 22.626523713702085], [120.28915068416808, 22.62320423300875], [120.28956127790883, 22.62078645056137], [120.29067979189438, 22.62081258897679], [120.2904107822007, 22.622733748945777], [120.28964622833757, 22.624955465095738], [120.28939137705146, 22.625491285381557], [120.2887400904234, 22.626811224004697]]
print(polygon_bounds[0])
a = heatmap_generator(polygon_bounds)
# print(a[:,0:1])
print(a.shape)
print(np.transpose(a).shape)

plt.scatter(a[:,0],a[:,1],a[:,-1])
plt.show()





