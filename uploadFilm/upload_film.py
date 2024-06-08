import json
import os
import boto3

from util.utils import create_response
# from requests import get

# Extract environment variable
table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')

def create(event, context):
    body = json.loads(event['body'])
    
    table = dynamodb.Table(table_name)
    
    response = table.put_item(
        Item = {
            'name' : body['name'], 
            'description' : body['description'],
            'actors' : body['actors'],
            'directors' : body['directors'],
            'genres' : body['genres']
        }
    )
    
    body = {
        'message': 'Successfully uploaded film'
    }
    return create_response(200, body)
