import json
import boto3
import mysql.connector
from botocore.exceptions import ClientError
# To_Check_Alaram
count=0
def send_request():
    SENDER = "nagalakshmi.kakumani7@gmail.com"
    RECIPIENT = "nagalakshmi.kakumani7@gmail.com"
    AWS_REGION = "ap-south-1"
    SUBJECT = "Reports Status"
    if count==0:
        BODY_TEXT = ("Reports Generation Status\r\n"
                     "The Reports generation was successfull"
                     "Please Refer SQL Workbench for Reports"
                     )
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Reports Generation Status</h1>
          <h3>The Reports generation was <b>successfull!!!<b><h3>
          <p>Please Refer SQL Workbench for Reports.</p>
        </body>
        </html>
                    """
    else:
        BODY_TEXT = ("Reports Generation Status\r\n"
                     "The Reports generation was unsuccessfull!!!"
                     "Please Check the corresponding code for successfull report generation"
                     )
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Reports Generation Status</h1>
          <h3>The Reports generation was <b>unsuccessfull!!!<b><h3>
          <p>Please Check the corresponding code for successfull report generation</p>
        </body>
        </html>
                    """
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent successfully!!!")
conn = mysql.connector.connect(
    host='python-carestudy1.cedujzpqusry.ap-south-1.rds.amazonaws.com',
    user='admin',
    password='Pass_123',
    database='salesdb'
)
s3_client = boto3.client('s3')
def lambda_handler(event, context):
    global count
    try:
        # Checking_Failure_Condition_With_This_Text
        bucket_name=event["Records"][0]["s3"]["bucket"]["name"]
        print(bucket_name)
        # print("hi",conn)
        s3_file_name=event["Records"][0]["s3"]["object"]["key"]
        response=s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
        data = []
        data = response["Body"].read().decode('utf-8').splitlines()
        field_header = data[0].split(",")
        # print(field_header)
        #################################### inserting data
        crsr1 = conn.cursor()
        crsr1.execute("truncate table salesdb.totalsales;")
        crsr1.close()
        print("truncated")
        with conn.cursor() as cur:
            
            for sale in data[1::]: # Iterate over S3 csv file content and insert into MySQL database
                try:
                    sale = sale.split(",")
                    mySql_insert_query = """INSERT INTO totalsales
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                    record = (sale[0],sale[1],sale[2],sale[3],sale[4],sale[5],sale[6],sale[7],sale[8],sale[9],sale[10],sale[11],sale[12],sale[13])
                    cur.execute(mySql_insert_query, record)
                except:
                    print("exception occured")
            conn.commit()
            print("Records inserted successfully into totalsales table")
        crsr = conn.cursor()
        crsr.execute("create or replace view salesdb.repot1_view as select Region, substr(Ship_Date,4,7) as Ship_Year_Month, sum( Units_Sold) as Total_Sales , sum(Total_Revenue) as Total_Revenue , sum(Total_Profit) as Total_Profit from salesdb.totalsales group by Region, Ship_Year_Month order by Region, Ship_Year_Month;")
        print("Report1 view created")
        crsr.execute("create or replace view salesdb.repot2_view as select Region, substr(Ship_Date,7,4) as Ship_Year, sum( Units_Sold) as Total_Sales, sum(Total_Revenue) as Total_Revenue, sum(Total_Profit) as Total_Profit from salesdb.totalsales group by Region, Ship_Year order by Region, Ship_Year;")
        print("Report2 view created")
        crsr.execute("create or replace view salesdb.repot3_view as select Region, substr(Ship_Date,7,4) as Ship_Year, Sales_Channel, sum( Units_Sold) from salesdb.totalsales group by Region, Ship_Year, Sales_Channel order by Region, Ship_Year, Sales_Channel;")
        print("Report3 created")
        crsr.close()
        conn.close()
    #     ####################################
    #     # print("create table sales (" + field_header[0][1::] +" integer(100)," + field_header[1] + " varchar(30)," + field_header[2] + " varchar(30))")
    #     # crsr.execute("create table sales (" + field_header[0] +" integer(100)," + field_header[1] + " varchar(30)," + field_header[2] + " varchar(30))")
        count=0
        send_request()
        print(count)
    except Exception as err:
        count=1
        send_request()
        print(count)
        print(err)
    
    return{
            'statusCode':200,
            'body': json.dumps('Hello from Lambda!')
        }
    
