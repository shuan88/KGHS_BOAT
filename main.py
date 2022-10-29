from webbrowser import get
from folium.plugins import HeatMap
import folium # 匯入 folium 套件
import numpy as np
import random
import os
import json

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
                nearest_point_features_index = 0 ;
                nearest_point = temp
    # print("Index of nearest point in polygon : ",nearest_point_features_index)
    return nearest_point_features_index,[nearest_point[1],nearest_point[0]]




# latitude,longitude= 22.6199759,120.2816580 # 緯度,經度
latitude,longitude= 22.625266504508858,120.29873388752162 # 緯度,經度

## Test when latitude and long has bias
rondom_bound = 0.001 
if rondom_bound > .0:
    latitude,longitude = random_coord_generator(latitude,longitude,rondom_bound)

## Read json file
json_map = read_json_file('json_map.json')
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



## Add heatmap in map
    # data shape ((lat,lon),weight)
data = (np.random.normal(size=(100, 3)) * 0.0001 *
    np.array([[1, 1, 1]]) +
    np.array([[latitude,longitude, 1]])).tolist()
fmap.add_child(HeatMap(data=data))


## Draw Line
points = [[latitude,longitude],
          near_coordinates]
fmap.add_child(folium.PolyLine(locations=points, # 座標List
                               weight=8,
                               color='green')) # 線條寬度



## import GeoJson or TopoJson draw range in map
    # https://github.com/topojson/topojson
    
fmap.add_child(folium.GeoJson("json_map.json", name='geojson'))

## Save the map
fmap.save('map.html')


