
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
3. 


### Use the Lambda function to connect to the RDS instance



### Handle the Lambda function from the API Gateway



## API Gateway


### Create a new API Gateway

#### REST API


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

# To do list

`src/Dynamically_plot.py` 要加入即時從資料庫抓數據更新的功能

# Reference
https://hackmd.io/DekxmXS3TmGnyCDMNO2dgA?view