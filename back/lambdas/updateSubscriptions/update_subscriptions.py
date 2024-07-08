import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

def update_subs(event, context):

    path_params = event.get('pathParameters', {})
    username = path_params.get('username')
    
    subs = json.loads(event['body'])

    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
            'username': username,
            'directors': subs['directors'],
            'actors': subs['actors'],
            'genres': subs['genres']
        }
    )
    queue_url = os.environ['CUSTOM_VAR']
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=username
    )

    body = {'message': 'Successfully updated subscriptions.'}

    return { 
        'statusCode': 200, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
        }
