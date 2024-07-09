import json
import boto3
import os
import base64

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def get_film(event, context):
    film_id = event['pathParameters']['id']
    response = table.get_item(Key={'filmId': film_id})
    
    return {
        'statusCode': 200,
        'headers': {
        'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response['Item'])
    }
   
