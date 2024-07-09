import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def create(body, context):
    film_id = body['filmId']

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
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

    return {
            'filmId': film_id,
            'fileName' : body['fileName']
            }
