import json
import numpy as np

# read json file dir = json_map.json
def read_json_file(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

# Random number generator
def random_coord_generator(x,y,bound):
    random_x,random_y = np.random.uniform(-bound,bound),np.random.uniform(-bound,bound)
    return random_x,random_y

# Find the nearest point in the polygon
def return_nearest_point_index(x,y,json_map):
    nearest_point_features_index = 0
    temp_nearest_distance = 1024
    nearest_point = []
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
    print("Index of nearest point in polygon : ",nearest_point_features_index)
    return nearest_point_features_index,nearest_point
        

        
    
    

latitude,longitude = 22.625266504508858,120.29873388752162 # 緯度,經度
# latitude,longitude = random_coord_generator(latitude,longitude,0.001)
json_map = read_json_file('json_map.json')

near_index, near_coordinates = return_nearest_point_index(latitude,longitude,json_map)
print (near_index, near_coordinates)

print (json_map['features'][near_index]['geometry']['coordinates'][0])

