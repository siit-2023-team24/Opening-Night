import json
import boto3
import os
import base64

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)
bucket_name = os.environ['BUCKET_NAME']

def get_film(event, context):
    film_id = event['pathParameters']['id']
    response = table.get_item(Key={'filmId': film_id})
    
    if 'Item' in response:
        file_name = response['Item']['fileName']

        try:
            s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
            file_content = base64.b64encode(s3_response['Body'].read()).decode('utf-8')
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': str(e)})
            }
        
        response['Item']['fileContent'] = file_content
        
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': 'Film not found'})
        }
