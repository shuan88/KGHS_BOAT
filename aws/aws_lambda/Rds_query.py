import time
import json
import pymysql.cursors


# def insert_data(connection, data):
#     query = """INSERT INTO boat_data(
#             latitude, longitude, O_Hum, O_Temp, PH, TDS, W_Temp
#             ) 
#             VALUES (%s, %s, %s, %s, %s, %s, %s)""" %(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
#     with connection.cursor() as cursor:
#         # execute the query
#         cursor.execute(query)
        
#         # commit the changes
#         connection.commit()

def lambda_handler(event, context):
    connection_details = json.load(open("rds_key.json"))
    connection = pymysql.connect(host=connection_details['host'],
                                user=connection_details['user'],
                                password=connection_details['password'],
                                database=connection_details['database'],
                                cursorclass=pymysql.cursors.DictCursor)
    
    # handle POST request
    if  event['httpMethod']=='POST':
        evendata=json.loads(event['body'])
        # Insert data from http request
        # insert_data(connection, evendata)
        query = """INSERT INTO boat_data(
            latitude, longitude, O_Hum, O_Temp, PH, TDS, W_Temp
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""" %(evendata['latitude'], evendata['longitude'], evendata['O_Hum'], evendata['O_Temp'], evendata['PH'], evendata['TDS'], evendata['W_Temp'])
        
        with connection.cursor() as cursor:
            # execute the query
            cursor.execute(query)
            
            # commit the changes
            connection.commit()
        response = {
        'statusCode': 200,
        'body': 'successfully created item!',
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        }   
    else :
        response = event
        # response = {
        # 'statusCode': 502,
        # 'body': 'unsuccessfully created item!',
        # 'headers': {
        #   'Content-Type': 'application/json',
        #   'Access-Control-Allow-Origin': '*'
        # },
        # } 
    connection.close()
    
    return response