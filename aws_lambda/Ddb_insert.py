import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
  data = client.put_item(
    TableName='kghs_boat',
    Item={
      "shuan-kghs": {
        "S": "key3"
      },
      "latitude": {
        "N": "0"
      },
      "longitude": {
        "N": "0"
      },
      "O_Hum": {
        "N": "0"
      },
      "O_Temp": {
        "N": "0"
      },
      "PH": {
        "N": "7"
      },
      "TDS": {
        "N": "0"
      },
      "Time": {
        "S": "0"
      },
      "W_Temp": {
        "N": "0"
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