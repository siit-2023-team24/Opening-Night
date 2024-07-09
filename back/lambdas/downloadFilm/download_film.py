import os
import boto3
import base64
import json
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

def get_one(event, context):
    
    bucket_name = os.environ['BUCKET_NAME']

    path_parameters = event.get('pathParameters', {})
    
    name = path_parameters.get('name')

    # response = s3_client.get_object(Bucket=bucket_name, Key=name)
    # content = response['Body'].read()
    # encoded_content = base64.b64encode(content)

    event = json.loads(event['body'])
    filmId = event['filmId']
    username = event['username']
    genres = event['genres']
    actors = event['actors']
    directors = event['directors']
    timestamp = datetime.now().isoformat()

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': name},
        ExpiresIn=3600  # URL expires in 1 hour
    )


    table_name = os.environ['DOWNLOADS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
            'username': username,
            'timestamp': timestamp,
            'filmId': filmId,
            'actors': actors,
            'directors': directors,
            'genres': genres
        }
    )

    queue_url = os.environ['CUSTOM_VAR']
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=username
    )

    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'url': url})
    }
