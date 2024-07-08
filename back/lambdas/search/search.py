import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def search(event, context):
    
    path_params = event.get('pathParameters', {})
    input = path_params.get('input')

    #ako ima delimitere, radi filter kroz gsi search-index, ako nema scan
    if '|' in input:
        body = filter_search(input)
    else:
        body = scan_search(input)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body)
    }

def scan_search(input):
    result = []
    result_series_names = []

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)



    #TODO proveri da li je ok id

    data = table.scan(ProjectionExpression="filmId, title, isSeries, series, season, episode")
    items = data['Items']
    for film in items:
        if film['isSeries']:
            if film.get('series', "") in result_series_names:
                continue

        for key in film.keys():
            if input in key:
                if film['isSeries']:
                    result_series_names.append(film['series'])
                result.append(film)
                break
    return result



def filter_search(input):
    table_name = os.environ['CUSTOM_VAR']
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
        film = table.get_item(Key={'filmId': filmId})
        result.append({
            'filmId': film['filmId'],
            'title': film['title'],
            'isSeries': film.get('isSeries', ''),
            'series': film.get('series', ''),
            'season': film.get('season', ''),
            'episode': film.get('episode', '')
        })
    

    #TODO kog su tipa?




    return result