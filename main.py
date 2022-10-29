import folium # 匯入 folium 套件
import numpy as np
from folium.plugins import HeatMap
import random
import os

# # 建立地圖與設定位置
# fmap = folium.Map(location=[35.709635, 139.810851], zoom_start=16)
# fmap  # 在notebook中顯示地圖

# latitude,longitude= 22.6199759,120.2816580 # 緯度,經度
latitude,longitude= 22.625266504508858,120.29873388752162 # 緯度,經度
rondom_bound = 0.0 #地圖範圍
# random in range of rondom_bound
random_x,random_y = np.random.uniform(-rondom_bound,rondom_bound),np.random.uniform(-rondom_bound,rondom_bound)
print(random_x,random_y)
latitude+=random_x
longitude+=random_y

# Create a map using Stamen Terrain as the basemap
fmap = folium.Map(location=[latitude,longitude],
               zoom_start=18,
               min_zoom=12,
               max_zoom=20,
               tiles = 'Stamen Terrain')

## Add Pin in map
Device_location_Marker = folium.Marker(location=[latitude,longitude],
                   popup='<b>Device</b>',
                   icon=folium.Icon(icon="cloud"))
fmap.add_child(child=Device_location_Marker)


## Add heatmap in map
# data shape ((lat,lon),weight)
data = (np.random.normal(size=(100, 3)) * 0.02 *
        np.array([[1, 1, 1]]) +
        np.array([[latitude,longitude, 1]])).tolist()


fmap.add_child(HeatMap(data=data))


## import GeoJson or TopoJson draw range in map
#  https://github.com/topojson/topojson


# get all file name from directory {json_map}

# json_map_list = os.listdir('json_map')
# for json_file_name in json_map_list:
#     fmap.add_child(folium.GeoJson(os.path.join('json_map',json_file_name), name='geojson'))
    
fmap.add_child(folium.GeoJson("json_map.json", name='geojson'))


## Save the map
fmap.save('map.html')


