
# Anaconda

1. Create a new environment `conda create --name <environment_name>`
2. Activate the environment `conda activate <environment_name>`
3. Install pip in environment `conda install pip`
4. Install requirements.txt `while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt`
5. (Optional) Export requirements.txt `conda list --explicit > requirements.txt`

## install all the requirements
You can also use the following command to install all the requirements in one go
1. Export to .yml file `conda env export > freeze.yml`
2. To reproduce `conda env create -f freeze.yml`

> https://stackoverflow.com/questions/35802939/install-only-available-packages-using-conda-install-yes-file-requirements-t



## Check if the environment is working

1. Activate conde envirements `conda activate <environment_name>`
2. Run main.py `python3 src/main.py`
3. If it works, you can deactivate the environment `conda deactivate`

---

# AWS

Select the instance type and the region
The region setup is important because it will affect the latency of the server
So this time we choose  `ap-notheast-1` (Tokyo) as the region.
![](https://d1.awsstatic.com/local/osaka-region/aws_region_osaka_banner_white_2.deaf4d377bcff96a777da5b6bd0605eaec843ce7.png)

## AWS RDS

1. Create a new RDS instance
2. Choose the database engine as `MySQL`
3. Configure VPC and subnet group as the same as the EC2 and Lambda instance
4. Add the database name, username and password
5. Connict to the database using MySQL Workbench and create the database

NOTE: The database name is case sensitive

![rds mysql](https://miro.medium.com/max/720/1*J3PxWDBSQvKYGEibertmuw.jpeg)



The final structure of the AWS will be like this. The RDS is the database that we will use to store the data. The EC2 is the server that we will use to run the code. The S3 is the storage that we will use to store the data.





### Create VPC and Subnet
- Set the security group(VPC) to allow access from your IP


![](https://docs.aws.amazon.com/zh_tw/vpc/latest/peering/images/peering-intro-diagram.png)
The VPC is the virtual private cloud that we will use to run the code.



The security group is the firewall for your RDS instance. You can set the security group to allow access from your IP. This way, you can access the database from your local machine.

![](https://blog.shikisoft.com/assets/images/post_imgs/20171023/aws-lambda-vpc-rds.png)
The image show how to set the security group to allow access from your IP.

### Connect to the RDS instance


## Lambda


![](https://dz2cdn1.dzone.com/storage/temp/12918536-1578715967542.png)



#### Install the requirements in the Lambda function
<!-- https://jumping-code.com/2021/07/28/aws-lambda-python-packages/ -->
1. Install the requirements in the Lambda function
    ```bash
    $ mkdir python
    $ cd python
    
    # Install single package
    $ pip install --target . requests
    
    # Install multiple packages
    $ pip install --target . -r requirements.txt
    ```
2. Packageing to zip
    ```bash
    $ zip -r9 ${OLDPWD}/function.zip .
    $ cd $OLDPWD
    $ zip -g function.zip lambda_function.py
    ```
3. Upload the zip file to the Lambda function


### Use the Lambda function to connect to the RDS instance


[Rds_Query](aws/aws_lambda/Rds_Query.yaml)

## API Gateway

![](https://i0.wp.com/blog.knoldus.com/wp-content/uploads/2019/04/ApiGateway.png?fit=771%2C461&ssl=1)

### Create a new API Gateway

1.  Open the API Gateway console .
2.  Choose Create API.
3.  Under HTTP API, choose Build.
4.  Choose Add integration, and then choose an AWS Lambda function or enter an HTTP endpoint.
5.  For Name, enter a name for your API.
6.  Choose Review and create.
7.  Choose Create.

#### REST API
Use the REST API to create a new API Gateway
- Reference: 
  - https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-getting-started-with-rest-apis.html
  - https://www.codecademy.com/article/what-is-rest

![What is REST](https://raw.githubusercontent.com/Codecademy/articles/0b631b51723fbb3cc652ef5f009082aa71916e63/images/rest_api.svg)

##### Making Requests

REST requires that a client make a request to the server in order to retrieve or modify data on the server. A request generally consists of:

-   an HTTP verb, which defines what kind of operation to perform
-   a _header_, which allows the client to pass along information about the request
-   a path to a resource
-   an optional message body containing data

##### HTTP Verbs

There are 4 basic HTTP verbs we use in requests to interact with resources in a REST system:

-   GET — retrieve a specific resource (by id) or a collection of resources
-   POST — create a new resource
-   PUT — update a specific resource (by id)
-   DELETE — remove a specific resource by id

---


# Run the project


## Run the GPS data show in the browser

1. Activate conde envirements `conda activate <environment_name>`
2. Run main.py `python3 src/main.py`

## Show the Sensor data
1. Activate conde envirements `conda activate <environment_name>`
2. (Option)If you want to use the database, you need to change the `load_data()` to `load_data(False , connection)` and uncomment `connection = db_connection()` in previous line
    - N is the number of data you want to load from the database
3. Run show_data.py `python3 src/show_data.py`
4. You will get result images in the img folder

### Result images

|  |  |
|:-------------------------:|:-------------------------:|
|<img src="load_data result example.png" width="400">|<img src="load_data result example2.png" width="400">|

## Show the data realtime

1. Activate conde envirements `conda activate <environment_name>`


The result will be shown like this

<img src="animation.gif" width="400">



## Query the database

### Delete or Create a new table from database

1. Uncomment `delete_table(connection)` or `create_table(connection)` in `src/sql_io.py`
2. Activate conde envirements `conda activate <environment_name>`
3. Run main.py `python3 src/sql_io.py`

### Create random data and insert into database
1. Uncomment the following code in `src/sql.py`
``` python

    for i in range(60):
        try :
            insert_data_random(connection)
            print("insert data success count: {}".format(i))
            time.sleep(2)
        except:
            print("Error inserting data , try again")
            time.sleep(1)
```
2. Activate conde envirements `conda activate <environment_name>`
3. Run main.py `python3 src/sql_io.py`

### Export data from database to csv file
1. Uncomment `save_data_to_csv(connection , name = boat_data_3)` in `src/sql_io.py`
    - You can change the name of the csv file by changing the `name` parameter
2. Activate conde envirements `conda activate <environment_name>`
3. Run main.py `python3 src/sql_io.py`

### Query last data from database
1. Uncomment `query_last_data(connection)` in `src/sql_io.py`
2. Activate conde envirements `conda activate <environment_name>`
3. Run main.py `python3 src/sql_io.py`



--- 

# MCU


## Hardware

Useing the following hardware
- ESP32
- Anyleaf Soil Moisture Sensor
- DS18B20 Digital Temperature Sensor
- DHT22 humidity and temperature sensor
- PH Sensor 
- Usb(Optinal)

## Pinout

| ESP32 | Sensor |
|:-------------------------:|:-------------------------:|
| 3v3 | VCC |
| GND | GND |
| 25 | DHT22 |
| 26 | DS18B20 |
| 34(A0) | PH Sensor |
| 13 | RXPin |
| 12 | TXPin |

### Pin Diagram 

![](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg?resize=750%2C538&quality=100&strip=all&ssl=1)


## Software

## Setup
1. Open PlatformIO plugin in VScode
2. Open the project folder `mcu`
3. Open `src/main.cpp`
4. Replace the `ssid` and `password` with your wifi ssid and password
5. Upload the code to the ESP32
   - If the update failed, you can try to change the `upload_port` in `platformio.ini` to the port of your ESP32
   - If the terminal showing Connecting.......... and took a long time to load, you can try to press the `boot` button on the ESP32 and upload the code again
6. Open the serial monitor and you will see the result
7. If you don't want to use the serial monitor, you can comment the `Serial.begin(115200)` and `Serial.println()` in `src/main.cpp`'

### Defult ini setting

``` txt
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
```

---
# To do list

`src/Dynamically_plot.py` 要加入即時從資料庫抓數據更新的功能

# Reference
https://hackmd.io/DekxmXS3TmGnyCDMNO2dgA?view