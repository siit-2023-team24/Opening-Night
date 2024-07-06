import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')

def get_feed(event, context):

    path_params = event.get('pathParameters', {})
    username = path_params.get('username')

    table_name = os.environ['FEED_TABLE_NAME']
    table = dynamodb.Table(table_name)

    items = table.get_item(Key={'username': username})

    try:
        films = items['Item']
        status = 200
    except KeyError:
        films = []
        status = 404
        print('username not found in feed table')

    return {
        'statusCode': status, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(films, default=str)
    }

