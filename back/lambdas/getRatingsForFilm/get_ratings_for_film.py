import os
import boto3
import json

import boto3.dynamodb.conditions

dynamodb = boto3.resource('dynamodb')

def get_ratings_for_film(event, context):

    path_params = event.get('pathParameters', {})
    filmId = path_params.get('filmId')

    table_name = os.environ['RATINGS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    try:
        items = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('filmId').eq(filmId)
        )
        status = 200
        items = items['Items']
        body = [{'username': r['username'], 'timestamp': r['timestamp'], 'stars': r['stars']} for r in items]

    except BaseException as e:
        print(e)
        status = 500
        body = []

    finally:
        return { 
            'statusCode': status, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(body, default=str)
            }
    
    