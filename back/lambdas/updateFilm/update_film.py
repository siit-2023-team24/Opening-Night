import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

def update(event, context):
    body = json.loads(event['body'])

    film_id = body['filmId']

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={'filmId': film_id})
    
    if 'Item' in response:
        table.delete_item(Key={'filmId': film_id})

    table.put_item(
        Item = {
                'filmId': film_id,
                'fileName': body['fileName'],
                'title' : body['title'],
                'description' : body['description'],
                'actors' : body['actors'],
                'directors' : body['directors'],
                'genres' : body['genres'],
                'isSeries': body['isSeries'],
                'series': body.get('series', None)
            }
    )

    message = {
        'message': 'Successfully updated film'
    }
    
    return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(message, default=str)
            }
