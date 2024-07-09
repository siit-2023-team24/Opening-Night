import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def get(event, context):
    result = []
    result_series_names = []
    try:
        data = table.scan(
            ProjectionExpression="filmId, title, isSeries, series, season, episode"
        )
        items = data['Items']

        for film in items:
            if film['isSeries']:
                if film.get('series', "") in result_series_names: continue
                if 'season' in film: film['season'] = int(film['season'])
                if 'episode' in film: film['episode'] = int(film['episode'])
                film['title'] = film['series']
                result_series_names.append(film['series'])
            result.append(film)
        print(result)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(result)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': str(e)})
        }
