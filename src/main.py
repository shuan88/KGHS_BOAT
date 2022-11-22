import json
import os
import random
import webbrowser
from itertools import product
from webbrowser import get

import folium  
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from descartes import PolygonPatch
from folium.plugins import HeatMap
from shapely.geometry import LineString, MultiPoint, Point, Polygon

from sql_io import *
from line_notify import message2line


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
    heat_data= np.random.normal(1,3,len(python_list))
    # append the heat_data to the heatmap array (639,2) to (639,3)
    heatmap = np.append(heatmap,heat_data.reshape(len(heat_data),1),axis=1)
    return heatmap[:,[1,0,2]]

## read json file dir = json_map.json
def read_json_file(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

## Random number generator
def random_coord_generator(x,y,bound):
    random_x,random_y = x+np.random.uniform(-bound,bound),y+np.random.uniform(-bound,bound)
    return random_x,random_y

## Find the nearest point in the polygon
def return_nearest_point_index(x,y,json_map):
    nearest_point_features_index = 0
    temp_nearest_distance = 1024
    # get the first point in the polygon    
    nearest_point = json_map['features'][0]['geometry']['coordinates'][0][0]
    for i in range(len(json_map['features'])):
        for j in range(len(json_map['features'][i]['geometry']['coordinates'][0])):
            temp = json_map['features'][i]['geometry']['coordinates'][0][j]
            # using the distance formula : d = abs(xi-x) + abs(yi-y)
            if abs(temp[0]-y)+abs(temp[1]-x) < temp_nearest_distance:
                temp_nearest_distance = abs(temp[0]-y)+abs(temp[1]-x)
                nearest_point_features_index = i ;
                nearest_point = temp
    # print("Index of nearest point in polygon : ",nearest_point_features_index)
    return nearest_point_features_index,[nearest_point[1],nearest_point[0]]


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    
    # Connect to the database
    connection = db_connection()

    # latitude,longitude= 22.6199759,120.2816580 # 緯度,經度
    latitude,longitude= 22.625266504508858,120.29873388752162 # 緯度,經度

    ## Test when latitude and long has bias
    rondom_bound = 0.01 
    if rondom_bound > .0:
        latitude,longitude = random_coord_generator(latitude,longitude,rondom_bound)

    
    ## Read json file
    json_map = read_json_file(os.path.join(root,'json_map.json'))
    ## get the nearest point in the polygon
    near_index, near_coordinates = return_nearest_point_index(latitude,longitude,json_map)

    # Create a map using Stamen Terrain as the basemap
    fmap = folium.Map(location=[latitude,longitude],
                zoom_start=18,
                min_zoom=12,
                max_zoom=20,
                tiles = 'Stamen Terrain')

    ## Add Pin in map

    ### Draw deivce location
    Device_location_Marker = folium.Marker(location=[latitude,longitude],
                    popup='<b>Device</b>',
                    icon=folium.Icon(icon="cloud"))

    fmap.add_child(child=Device_location_Marker)
    fmap.add_child(folium.Circle(location=[latitude,longitude],
                                color='green', # Circle 顏色
                                radius=40, # Circle 寬度
                                popup='Skytree', # 彈出視窗內容
                                fill=True, # 填滿中間區域
                                fill_opacity=0.5 # 設定透明度
                                ))

    ### Draw the Water location
    Crop_location_Marker= folium.Marker(location=near_coordinates,
                    popup='<b>Water</b>',
                    icon=folium.Icon(icon="red"))
    fmap.add_child(child=Crop_location_Marker)


    ## Draw Line
    points = [[latitude,longitude],
            near_coordinates]
    fmap.add_child(folium.PolyLine(locations=points, # 座標List
                                weight=8,
                                color='green')) # 線條寬度


    ## Add heatmap in map
        # data shape ((lat,lon),weight)
    data = (np.random.normal(size=(100, 3)) * 0.0001 *
        np.array([[1, 1, 1]]) +
        np.array([[latitude,longitude, 1]])).tolist()
    fmap.add_child(HeatMap(data=data))
    print(data)

    data = heatmap_generator(json_map['features'][near_index]['geometry']['coordinates'][0])
    fmap.add_child(HeatMap(data=data.tolist()))
    print(data)


    filename = 'map.html'

    ## import GeoJson or TopoJson draw range in map
        # https://github.com/topojson/topojson
    fmap.add_child(folium.GeoJson(os.path.join(root,'json_map.json'), name='geojson'))

    ## Save the map
    fmap.save(os.path.join(root,filename))

    ## Open the map.html from the browser
    webbrowser.open('file://' + os.path.realpath(filename))
    # url = 'file:///Users/msyang/shuan-code/kghs/map.html'
    # webbrowser.open(url)
    connection.close()