import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def search_filter(event, context):

    path_params = event.get('pathParameters', {})
    input = path_params.get('input')
    
    print(input)

    table_name = os.environ['SEARCH_TABLE_NAME']
    table = dynamodb.Table(table_name)

    items = table.query(
        IndexName='search-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('data').eq(input)
    )
    filmIds = items['Items']
    print(filmIds)

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    result = []
    for filmId in filmIds:
        print(filmId)
        film = table.get_item(Key={'filmId': filmId['filmId']})['Item']
        print(film)
        result.append({
            'filmId': film['filmId'],
            'title': film['title'],
            'isSeries': film.get('isSeries', ''),
            'series': film.get('series', ''),
            'season': film.get('season', 0),
            'episode': film.get('episode', 0)
        })

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(result)
    }


