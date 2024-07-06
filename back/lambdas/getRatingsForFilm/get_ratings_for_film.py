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

        # response = table.query(
        # IndexName='author_id_timestamp-index',
        # KeyConditionExpression=boto3.dynamodb.conditions.Key('author_id').eq('your_author_id')
        # )

        status = 200
        body = items['Items']

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
    
    