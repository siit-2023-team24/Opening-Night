import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')

def get_actors_and_directors(event, context):

    directors = set()
    actors = set()

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    response = table.scan()
    data = response.get('Items', [])
    for d in data:
        directors.update(d['directors'])
        actors.update(d['actors'])

    #pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data = response.get('Items', [])
        for d in data:
            directors.update(d['directors'])
            actors.update(d['actors'])
    
    directors = list(directors)
    actors = list(actors)

    body = {'directors': directors, 'actors': actors }
    return { 
        'statusCode': 200, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
        }
    