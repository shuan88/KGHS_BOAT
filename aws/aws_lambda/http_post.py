import requests
import json
import random
from time import sleep

def http_post(url, body):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    print(requests.post(url, data=json.dumps(body), headers=headers).text)
    return response
    
def http_post_randomdata(url):
    headers = {'Content-Type': 'application/json'}
    post_data= {
    "latitude": "{}".format(random.randint(0, 180)),
    "longitude": "{}".format(random.randint(-90, 90)),
    "O_Hum": "{}".format(random.randrange(0, 100)),
    "O_Temp": "{}".format(random.randrange(0, 451)),
    "PH":  "{}".format(random.randrange(0, 7)),
    "TDS":  "{}".format(random.randrange(0, 451)),
    "W_Temp":  "{}".format(random.randrange(0, 451))
    }
    response = requests.post(url, data=json.dumps(post_data), headers=headers)
    return response


# load event.json
data = json.load(open('aws/aws_lambda/event.json'))
# url = "https://ci2fgu1na6.execute-api.ap-northeast-1.amazonaws.com/v1/boat"
url = "https://wco6y0ab82.execute-api.ap-northeast-1.amazonaws.com/default/Rds_Query"

# 回傳的訊息是 502，伺服器內部錯誤，通常這種錯誤都是後端程式執行失敗所造成，詳細輸出可以檢視下圖。
# response = http_post(url, data)

for i in range(3):
    response = http_post_randomdata(url)
    print(response.text)
    print(response)
    print(response.request.url)
    print(response.request.body)
    print(response.request.headers)
    # sleep 1 second
    sleep(1)