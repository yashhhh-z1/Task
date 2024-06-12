import boto3
import pymysql
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def read_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = obj['Body'].read().decode('utf-8')
        return data
    except NoCredentialsError:
        print("Credentials not available")
        return None

def write_to_rds(data, rds_host, db_user, db_password, db_name):
    try:
        connection = pymysql.connect(host=rds_host,
                                     user=db_user,
                                     password=db_password,
                                     database=db_name)
        cursor = connection.cursor()
        query = "INSERT INTO your_table_name (column1, column2) VALUES (%s, %s)"
        cursor.executemany(query, data)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return False

def write_to_glue(data, database_name, table_name):
    glue = boto3.client('glue')
    try:
        response = glue.batch_create_partition(
            DatabaseName=database_name,
            TableName=table_name,
            PartitionInputList=[{'Values': [data]}]
        )
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    bucket_name = 'my-task-bucket.com'
    file_key = 'b72186829f4efb1a3bab9478b41f3a11f209da050cb9b566d4a6eab027efda91'
    rds_host = 'rds-task.ct68uiecqwr6.ap-south-1.rds.amazonaws.com'
    db_user = 'admin'
    db_password = 'admin123'
    db_name = 'task_db'
    glue_database = 'task_glue_db'
    glue_table = 'task'

    data = read_from_s3(bucket_name, file_key)
    if data:
        success = write_to_rds(data, rds_host, db_user, db_password, db_name)
        if not success:
            write_to_glue(data, glue_database, glue_table)

if __name__ == "__main__":
    main()

