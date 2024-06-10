import json
import os
import boto3
import base64
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
def create(event, context):
    body = json.loads(event['body'])

    file_name = body['fileName']
    file_content = base64.b64decode(body['fileContent'])

    bucket_name = os.environ['BUCKET_NAME']
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=file_content,
        ContentType='video/mp4',
        Metadata={
            'Name': file_name,
            'Type': 'video/mp4',
            'Size': f"{len(file_content)}B",
            'Time created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Last modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    )

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
                'fileName': body['fileName'],
                'title' : body['title'],
                'description' : body['description'],
                'actors' : body['actors'],
                'directors' : body['directors'],
                'genres' : body['genres']
            }
    )

    message = {
        'message': 'Successfully uploaded film'
    }

    return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(message, default=str)
            }
