import json
import os
import boto3
import base64

# from requests import get

# Extract environment variable
# table_name = os.environ['TABLE_NAME']
# dynamodb = boto3.resource('dynamodb')

s3_client = boto3.client('s3')
def create(event, context):
    body = json.loads(event['body'])

    file_name = body['fileName']
    file_content = base64.b64decode(body['fileContent'])
# paziv datoteke, tip datoteke, veličinu
# datoteke, vreme nastanka i vreme poslednje izmene

    bucket_name = os.environ['BUCKET_NAME']
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=file_content,
        ContentType='video/mp4'  # Adjust the content type as needed
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


    # table = dynamodb.Table(table_name)

    # response = s3_client.put_item(
    #     Item = {
    #         # 'name' : body['name'],
    #         # 'description' : body['description'],
    #         # 'actors' : body['actors'],
    #         # 'directors' : body['directors'],
    #         # 'genres' : body['genres']
    #     }
    # )
    
    # body = {
    #     'message': 'Successfully uploaded film'
    # }
    # return create_response(200, body)
