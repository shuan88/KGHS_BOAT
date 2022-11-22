import json
import pymysql.cursors
import random
import time
import numpy as np
import pandas as pd

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

def db_connection():
    connection_details = json.load(open("rds_key.json"))
    return pymysql.connect(host=connection_details['host'],
                                user=connection_details['user'],
                                password=connection_details['password'],
                                database=connection_details['database'],
                                cursorclass=pymysql.cursors.DictCursor)


def create_table(connection):
    query = """Create table if not exists boat_data(
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            latitude double  DEFAULT 22.625266504508858,
            longitude double  DEFAULT 120.29873388752162,
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
        
        
def delete_table(connection , table_name="boat_data"):
    query = """DROP TABLE %s""" %(table_name)
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
    latitude += random.randrange(-100,100)/1E4
    longitude += random.randrange(-100,100)/1E4
    post_data= {
    "latitude": "{}".format(latitude),
    "longitude": "{}".format(longitude),
    "O_Hum": "{}".format(random.randrange(30, 100)),
    "O_Temp": "{}".format(random.randrange(20, 34)),
    "PH":  "{}".format(random.randrange(5, 10)),
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
    # print("insert data success")
    
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

def save_data_to_csv(connection , name="boat_data"):
    query = """SELECT * FROM boat_data"""
    with connection.cursor() as cursor:
        # execute the query
        cursor.execute(query)
        result = cursor.fetchall()
    # Convert the result to pandas dataframe
    df = pd.DataFrame(result)
    # save the df to csv file
    df.to_csv("./csv/{}.csv".format(name), index=False)
    
def read_csv_data(name="boat_data"):
    csv_file_path = "./csv/{}.csv".format(name)
    df = pd.read_csv(csv_file_path , header=0) # header:[ ts  latitude  longitude  O_Hum  O_Temp   PH    TDS  W_Temp]    
    # remove the ts column
    df = df.drop(columns=['ts'])
    # df to numpy arrays
    results = df.to_numpy(dtype=np.float32) # results.shape: (n, 7)
    # print(type(results))
    # print(results.shape)
    return results


if __name__ == "__main__":
    connection = db_connection()

    # delete_table(connection)
    # create_table(connection)
    
    data = [22.625266504508858, 120.29873388752162, 47, 28, 7.8, 120, 30]
    
    
    insert_data(connection, data)
    time.sleep(1)
    select_all(connection)

    for i in range(60):
        try :
            insert_data_random(connection)
            print("insert data success count: {}".format(i))
            time.sleep(1)
        except:
            print("Error inserting data , try again")
            time.sleep(1)
    
    select_all(connection)
    save_data_to_csv(connection, name="boat_data_2")
    
    # select_last(connection)
    # select_last_N(connection, 10)
    # create_table(connection)
    # delete_table(connection)
    connection.close()