# Kinesis to S3 Pipeline

This project implements a real-time data ingestion and processing pipeline that integrates Amazon Kinesis Data Streams with AWS Lambda and Amazon S3. The pipeline is designed to handle and store data dynamically in JSON format for further analysis and processing.
s
## Architecture

The pipeline architecture consists of the following components:

1. **Amazon Kinesis Data Generator (KDG)**:
   - Used to simulate or generate sample data streams.

2. **Amazon Kinesis Data Stream**:
   - Serves as the data ingestion layer that captures real-time streaming data.

3. **AWS Lambda**:
   - Processes incoming records from the Kinesis Data Stream.
   - Decodes base64-encoded data, converts it into JSON, and uploads it to Amazon S3.

4. **Amazon S3**:
   - Stores the processed JSON files for further use, such as analytics or integration with other AWS services.

## Data Flow

1. **Data Generation**:
   - Sample data is generated using the Kinesis Data Generator (KDG) or any other source and sent to the Kinesis Data Stream.

2. **Data Processing**:
   - The Kinesis Data Stream triggers an AWS Lambda function for each batch of records.
   - The Lambda function:
     - Decodes the base64-encoded Kinesis records.
     - Parses the records into JSON format.
     - Saves the processed data as JSON files in the `/tmp` directory.
     - Uploads the JSON files to an S3 bucket.
     - Deletes the temporary files to conserve space.

3. **Data Storage**:
   - Processed JSON files are stored in the designated Amazon S3 bucket under the `kinesis/` prefix with filenames derived from the sequence number of the Kinesis record.

## Prerequisites

- **AWS Account**: Ensure you have an active AWS account.
- **IAM Roles and Permissions**:
  - Lambda function must have permissions to read from Kinesis and write to S3.
  - Example policy includes `AmazonKinesisReadOnlyAccess` and `AmazonS3FullAccess`.
- **Amazon Kinesis Data Stream**: Set up a stream to capture real-time data.
- **Amazon S3 Bucket**: Create an S3 bucket for storing the processed JSON files.

## Deployment Steps

1. **Create an S3 Bucket**:
   - Create an S3 bucket to store processed JSON files.
   - Note the bucket name to configure in the Lambda function.

2. **Set Up Kinesis Data Stream**:
   - Create a Kinesis Data Stream to capture incoming data.

3. **Deploy Lambda Function**:
   - Use the following Python code to implement the Lambda function:

```python
import json
import base64
import os
import boto3

s3_client = boto3.resource('s3')
s3_bucket_name = "your-s3-bucket-name"

def lambda_handler(event, context):
    print("Event collected is {}".format(event))
    for record in event['Records']:
        sample_string_bytes = base64.b64decode(record['kinesis']['data'])
        sample_string = sample_string_bytes.decode("ascii")
        print("Decoded string:", sample_string)
        
        s3_file_name = "kinesis/{}.json".format(record['kinesis']['sequenceNumber'])
        local_dir_path = "/tmp/kinesis/"
        local_file_path = local_dir_path + "{}.json".format(record['kinesis']['sequenceNumber'])
        
        if not os.path.exists(local_dir_path):
            os.makedirs(local_dir_path)
        
        with open(local_file_path, 'w') as fp:
            json.dump(json.loads(sample_string), fp)
        
        s3_client.meta.client.upload_file(local_file_path, s3_bucket_name, s3_file_name)
        os.remove(local_file_path)
```

   - Replace `your-s3-bucket-name` with your actual S3 bucket name.

4. **Configure Kinesis Trigger for Lambda**:
   - Attach the Kinesis Data Stream as a trigger for the Lambda function.

5. **Generate Test Data**:
   - Use the Kinesis Data Generator (KDG) to produce sample records.

## Testing the Pipeline

1. **Send Data to Kinesis**:
   - Use KDG or any producer to send sample data to the Kinesis Data Stream.

2. **Monitor Lambda Execution**:
   - Check the Lambda function's logs in Amazon CloudWatch to ensure proper execution and debugging.

3. **Verify S3 Output**:
   - Navigate to your S3 bucket and verify that JSON files are stored correctly under the `kinesis/` prefix.

## Use Cases

- Real-time data processing and archiving.
- Integration with analytics tools for business insights.
- Building scalable ETL pipelines for streaming data.

## Cleanup

To avoid unnecessary charges:

1. Delete the S3 bucket and its contents.
2. Delete the Lambda function.
3. Delete the Kinesis Data Stream.

## Future Enhancements

- Implement retry mechanisms for failed S3 uploads.
- Add data transformation and validation steps in the Lambda function.
- Integrate with downstream analytics tools such as Amazon Athena or Redshift.

## Diagram

![Pipeline Diagram](./path-to-diagram.png)

Ensure to replace `path-to-diagram.png` with the actual path to your pipeline diagram file if included in the repository.
