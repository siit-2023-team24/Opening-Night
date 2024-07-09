import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def get_episodes_by_series(event, context):
    series_name = event['pathParameters']['seriesName']
    
    response = table.scan(
        FilterExpression='series = :series_name',
        ExpressionAttributeValues={':series_name': series_name},
    )
    
    episodes = []
    if 'Items' in response:
        for item in response['Items']:
            if 'isSeries' in item and item['isSeries']:
                episodes.append({
                    'filmId': item['filmId'],
                    'title': item['title'],
                    'episode': int(item.get('episode', None)),
                    'season': int(item.get('season', None))
                })

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(episodes)
    }
