# Import necessary packages
import os 
import ffmap
from ffmap import plugins
# import rioxarray as rxr

import earthpy as et
import earthpy.spatial as es

# http://python-visualization.github.io/folium/modules.html#folium.map.Layer

# Import data from EarthPy
data = et.data.get_data('colorado-flood')

latitude,longitude= 22.6199759,120.2816580 # 緯度,經度
bound_range = .05 #地圖範圍

# Create a map using Stamen Terrain as the basemap
m = ffmap.Map(location=[latitude,longitude],
               zoom_start=18,
               min_zoom=16,
               max_zoom=20,
               tiles = 'Stamen Terrain')

# Add marker for Boulder, CO
ffmap.Marker(
    location=[latitude,longitude], # coordinates for the marker (Earth Lab at CU Boulder)
    popup='Earth Lab at CU Boulder', # pop-up label for the marker
    icon=ffmap.Icon()
).add_to(m)



map_bounds = [[latitude*(1+bound_range), longitude*(1+bound_range)], 
              [latitude*(1-bound_range), longitude*1-bound_range]]
# Overlay raster called img using add_child() function (opacity and bounding box set)

# m.add_child(folium.raster_layers.ImageOverlay(m, 
#                                               opacity=.9,
#                                               bounds=map_bounds))

# Display map
m
