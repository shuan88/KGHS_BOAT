import boto3
import time
import json

client = boto3.client('dynamodb')

def lambda_handler(event, context):
  data = client.put_item(
    TableName='kghs_boat',
    eventdata=json.loads(event['body'])
    Item={
      "shuan-kghs": {
        "S": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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
  
  return response