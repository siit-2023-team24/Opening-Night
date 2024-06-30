import os
import boto3
import base64
s3_client = boto3.client('s3')
def get_one(event, context):
    
    bucket_name = os.environ['BUCKET_NAME']

    path_parameters = event.get('pathParameters', {})
    
    name = path_parameters.get('name')

    response = s3_client.get_object(Bucket=bucket_name, Key=name)
    content = response['Body'].read()
    encoded_content = base64.b64encode(content)
    
    return {
        'statusCode': 200,
        'body': encoded_content
    }
