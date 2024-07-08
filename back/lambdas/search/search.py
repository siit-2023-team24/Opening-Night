import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def search(event, context):

    path_params = event.get('pathParameters', {})
    input = path_params.get('input')
    print(input)

    result = []
    result_series_names = []

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    data = table.scan(ProjectionExpression="filmId, title, isSeries, series, season, episode, genres, actors, directors")
    items = data['Items']
    for film in items:
        if film['isSeries']:
            if film.get('series', "") in result_series_names:
                continue

        print(film)
        for key in film.keys():
            if not film[key]:
                continue

            breaking = False
            if isinstance(film[key], list):
                for i in film[key]:
                    if input in i:
                        if film['isSeries']:
                            result_series_names.append(film['series'])
                        result.append(film)
                        breaking = True
                        break
                if breaking:
                    break

            elif isinstance(film[key], str) and input in film[key]:
                if film['isSeries']:
                    result_series_names.append(film['series'])
                result.append(film)
                break

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(result)
    }
