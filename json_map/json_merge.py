import json 
import os
import glob
import geojson

'''
Merge all json file from ./json_map file into .json_map.json
'''

def json_merge ():
    json_map_list = os.listdir('json_map')
    json_map = {}
    for json_file_name in json_map_list:
        print(json_file_name)
        with open(os.path.join('json_map',json_file_name),'r') as f:
            json_map[json_file_name] = json.load(f)
    # save json_map as json file
    with open('json_map.json','w') as f:
        json.dump(json_map,f)
        

def json_merge_geojson ():
    json_dir_name = "./json_map"
    json_pattern = os.path.join(json_dir_name,'*.json')
    file_list = glob.glob(json_pattern)

    collection = []
    for file in file_list:
        with open(file) as f:
            layer = geojson.load(f)
            collection.append(layer)

    geo_collection = geojson.GeometryCollection(collection)
    print(geo_collection)

    with open('test_collection.json', 'w') as f:
        geojson.dump(geo_collection, f)
    
json_merge()
json_merge_geojson()