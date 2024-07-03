import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')

def get_subs(event, context):
    
    path_params = event.get('pathParameters', {})
    username = path_params.get('username')
    

    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    subs = table.get_item(Key={'username': username})
    body = {'directors': [], 'actors': [], 'genres': []}
    status = 404
    try:    
        if subs and subs['Item']:
            item = subs['Item']
            body['directors'] = item['directors']
            body['actors'] = item['actors']
            body['genres'] = item['genres']
            status = 200
    except (KeyError):
        print('username not found error (no item found)')
    
    return { 
        'statusCode': status, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
        }
    
