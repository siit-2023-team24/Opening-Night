import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def get(event, context):
    response = table.scan(
        FilterExpression='isSeries = :is_series',
        ExpressionAttributeValues={':is_series': True},
        ProjectionExpression='series'
    )
    
    series_names = set()
    if 'Items' in response:
        for item in response['Items']:
            if 'series' in item:
                series_names.add(item['series'])

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(list(series_names))
    }
