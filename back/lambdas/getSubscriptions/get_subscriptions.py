import os
import boto3
import libs.utils as util

dynamodb = boto3.resource('dynamodb')

def get_subs(event, context):
    
    path_params = event.get('pathParametars', {})
    username = path_params.get('username')
    

    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    subs = table.get_item(Key={'username': username})
    item = subs['Item']
    body = {'directors': [], 'actors': [], 'genres': []}
    if item:
        body['directors'] = item['directors']
        body['actors'] = item['actors']
        body['genres'] = item['genres']

        return util.create_response(200, body)
    
    return util.create_response(404, body)
    
