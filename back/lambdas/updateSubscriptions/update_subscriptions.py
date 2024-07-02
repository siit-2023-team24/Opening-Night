import json
import os
import boto3
import libs.utils as util

dynamodb = boto3.resource('dynamodb')

def update_subs(event, context):

    path_params = event.get('pathParametars', {})
    username = path_params.get('username')
    
    subs = json.loads(event['body'])

    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
            'username': username,
            'directors': subs['directors'],
            'actors': subs['actors'],
            'genres': subs['genres']
        }
    )

    return util.create_response(
        200,
        {'message': 'Successfully updated subscriptions.'} )
    

