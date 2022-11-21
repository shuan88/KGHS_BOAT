import json
import pymysql.cursors
import random
import time
import numpy as np

def connect_data_to_json():
    host='HOST_NAME'
    user='USER_NAME'
    password='PASSWORD'
    database='DATABASE_NAME'
    json_data = {"host":host, "user":user, "password":password, "database":database}
    print(json_data)
    # save json_data to json file
    json_file = open("rds_key.json", "w")
    json.dump(json_data, json_file)
    json_file.close()

# load json file rds_key.json to connection_details
connection_details = json.load(open("rds_key.json"))
# Connect to the database
connection = pymysql.connect(host=connection_details['host'],
                            user=connection_details['user'],
                            password=connection_details['password'],
                            database=connection_details['database'],
                            cursorclass=pymysql.cursors.DictCursor)


def create_table(connection):
    query = """Create table if not exists boat_data(
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            latitude float  DEFAULT 22.625266504508858,
            longitude float  DEFAULT 120.29873388752162,
            O_Hum float DEFAULT 47,
            O_Temp float DEFAULT 28,
            PH float DEFAULT 7.8,
            TDS float DEFAULT 120,
            W_Temp float DEFAULT 30,
            PRIMARY KEY (ts)
            );"""
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        
        # commit the changes
        connection.commit()
        
        
def delete_table(connection):
    query = """DROP TABLE boat_data"""
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        
        # commit the changes
        connection.commit()
    
def insert_data(connection, data):
    query = """INSERT INTO boat_data(
            latitude, longitude, O_Hum, O_Temp, PH, TDS, W_Temp
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""" %(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        
        # commit the changes
        connection.commit()
    print("insert data success")
    
def insert_data_random(connection):
    latitude,longitude= 22.625266504508858,120.29873388752162
    latitude += random.randrange(-100,100)/1E6
    longitude += random.randrange(-100,100)/1E6
    post_data= {
    "latitude": "{}".format(latitude),
    "longitude": "{}".format(longitude),
    "O_Hum": "{}".format(random.randrange(0, 100)),
    "O_Temp": "{}".format(random.randrange(16, 34)),
    "PH":  "{}".format(random.randrange(4, 10)),
    "TDS":  "{}".format(random.randrange(0, 451)),
    "W_Temp":  "{}".format(random.randrange(20, 35))
    }
    
    query = """INSERT INTO boat_data(
            latitude, longitude, O_Hum, O_Temp, PH, TDS, W_Temp
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""" %(post_data['latitude'], post_data['longitude'], post_data['O_Hum'], post_data['O_Temp'], post_data['PH'], post_data['TDS'], post_data['W_Temp'])
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        
        # commit the changes
        connection.commit()
    print("insert data success")
    
def select_all(connection):
    query = """SELECT * FROM boat_data"""
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
    return result
        
def select_last(connection):
    query = """SELECT * FROM boat_data ORDER BY ts DESC LIMIT 1"""
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
    return result

def select_last_N(connection,N=10):
    query = """SELECT * FROM boat_data ORDER BY ts DESC LIMIT %s""" %(N)
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        result = cursor.fetchall()
    
    # result is a list of dict so we need to convert it to numpy array
    result_np = np.array([list(i.values()) for i in result])    
    print(result_np)
    print(result_np.shape)
    
    return result_np


    
data = [22.625266504508858, 120.29873388752162, 47, 28, 7.8, 120, 30]
# insert_data(connection, data)


# for i in range(30):
#     insert_data_random(connection)
#     time.sleep(1)

# select_all(connection)
# select_last(connection)
select_last_N(connection, 10)

# create_table(connection)
# delete_table(connection)
connection.close()