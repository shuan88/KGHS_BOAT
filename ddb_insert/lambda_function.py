import boto3
import time
import json


def lambda_handler(event, context):
  Table_name = 'KGHS_Boat_2'
  client = boto3.client('dynamodb')
  if  event['httpMethod']=='POST':
    eventdata=json.loads(event['body'])
    data = client.put_item(
      TableName=Table_name,
      Item={
        "Data_Time": {
          "N": str(int(time.time()))
        },
        "Data_Date":{
          "N": time.strftime("%Y%m%d", time.localtime())
        },
        "latitude": {
          "N": eventdata['latitude']
        },
        "longitude": {
        "N": eventdata['longitude']
        },
        "O_Hum": {
          "N": eventdata['O_Hum']
        },
        "O_Temp": {
          "N": eventdata['O_Temp']
        },
        "PH": {
          "N": eventdata['PH']
        },
        "TDS": {
          "N": eventdata['TDS']
        },
        "W_Temp": {
          "N": eventdata['W_Temp']
        }
      }
    )
    response = {
        'statusCode': 200,
        'body': 'successfully created item!',
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
    }
  elif event['httpMethod']=='GET':
    today = time.strftime("%Y%m%d", time.localtime())
    Time =  str(int(time.time()))
    response = client.query(
      TableName = Table_name,
      # KeyConditionExpression = Key('Date').eq(today)
      KeyConditionExpression = "Data_Date = :Date_today  AND Data_Time > :Time_query",
        ExpressionAttributeValues={
        ":Date_today":{"N": today},
        ":Time_query":{"N":"{}".format(str(int(time.time()-3600)))}
      }
    )
    print(response['Items'])
    # "Time": {
    # "N": str(int(time.time()))
    # },
    # "Date":{
    # "N": time.strftime("%Y%m%d", time.localtime())
    # }
        
    # response = client.get_item(
    #   TableName = 'kghs_boat',
    #   Key = {
    #     "date":{
    #       "S": time.strftime("%Y-%m-%d", time.localtime())
    #     }
    #   }
    # )
  return response