import json
import base64
import os
import boto3

s3_client = boto3.resource('s3')
s3_bucket_name = "kinesis-etl-bucket"

def lambda_handler(event, context):
    print("Event collected is {}".format(event))
    for record in event['Records']:
        # Decode the Kinesis data
        sample_string_bytes = base64.b64decode(record['kinesis']['data'])
        sample_string = sample_string_bytes.decode("ascii")
        print("Decoded string:", sample_string)
        print(type(sample_string))
        
        print("Inside function to create the dynamic .json file...")
        
        # Define file and directory paths
        s3_file_name = "kinesis/{}.json".format(record['kinesis']['sequenceNumber'])
        local_dir_path = "/tmp/kinesis/"
        local_file_path = local_dir_path + "{}.json".format(record['kinesis']['sequenceNumber'])
        print("Local file path: {}".format(local_file_path))
        
        # Create the directory if it doesn't exist
        if not os.path.exists(local_dir_path):
            os.makedirs(local_dir_path)
            print(f"Directory {local_dir_path} created.")
        
        # Write the data to a local JSON file
        with open(local_file_path, 'w') as fp:
            json.dump(json.loads(sample_string), fp)
        
        print("File is stored in local .json file")
        
        # Upload the file to S3
        s3_client.meta.client.upload_file(local_file_path, s3_bucket_name, s3_file_name)
        print("File uploaded successfully...")
        
        # Delete the local file after upload
        os.remove(local_file_path)
        print("File deleted after upload to S3 bucket")

