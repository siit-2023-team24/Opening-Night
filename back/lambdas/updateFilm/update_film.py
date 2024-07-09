import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

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

    remove_from_feed(film_id)
    
    return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(message, default=str)
            }



def remove_from_feed(filmId):
    table_name = os.environ['FEED_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    queue_url = os.environ['CUSTOM_VAR']

    items = table.scan()
    items = items.get('Items', [])

    for item in items:
        for film in item['films']:
            if filmId == film['filmId']:
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=item['username']
                )
                break