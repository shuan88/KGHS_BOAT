import json
import requests
import random

def http_post_randomdata():
    latitude,longitude= 22.625266504508858,120.29873388752162 # 緯度,經度
    latitude += random.randrange(-100,100)/1E6
    longitude += random.randrange(-100,100)/1E6
    url = "https://ci2fgu1na6.execute-api.ap-northeast-1.amazonaws.com/v1/boat"
    headers = {'Content-Type': 'application/json'}
    post_data= {
    "latitude": "{}".format(latitude),
    "longitude": "{}".format(longitude),
    "O_Hum": "{}".format(random.randrange(0, 100)),
    "O_Temp": "{}".format(random.randrange(16, 34)),
    "PH":  "{}".format(random.randrange(4, 10)),
    "TDS":  "{}".format(random.randrange(0, 451)),
    "W_Temp":  "{}".format(random.randrange(20, 35))
    }
    response = requests.post(url, data=json.dumps(post_data), headers=headers)
    return response

def http_post_fromdata(input_data):
    url = "https://ci2fgu1na6.execute-api.ap-northeast-1.amazonaws.com/v1/boat"
    headers = {'Content-Type': 'application/json'}
    post_data= {
    "latitude": "{}".format(input_data['latitude']),
    "longitude": "{}".format(input_data['longitude']),
    "O_Hum": "{}".format(input_data['O_Hum']),
    "O_Temp": "{}".format(input_data['O_Temp']),
    "PH": "{}".format(input_data['PH']),
    "TDS": "{}".format(input_data['TDS']),
    "W_Temp": "{}".format(input_data['W_Temp'])
    }
    response = requests.post(url, data=json.dumps(post_data), headers=headers)
    return response

def http_get():
    url = "https://ci2fgu1na6.execute-api.ap-northeast-1.amazonaws.com/v1/boat"
    response = requests.get(url)
    return response

# response = http_get()
# print(response.text)
# print(response)

# if __name__ == '__main__':
for i in range(3):
    response = http_post_randomdata()
    print(response.text)
    print(response)