import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
sqs = boto3.client('sqs')

def delete(event, context):
    
    path_params = event.get('pathParameters', {})
    filmId = path_params.get('id')
    
    try:
        remove_from_films(filmId)
        remove_from_search_table(filmId)
        remove_from_bucket(filmId)
        remove_from_ratings(filmId)
        remove_from_feed(filmId)
        status = 200
        message = 'Film deleted: ' + filmId
    except BaseException as e:
        print(e)
        status = 500
        message = 'Error while deleting film ' + filmId
    
    response_body = {'message': message}
    return { 
        'statusCode': status, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response_body, default=str)
    }


def remove_from_films(filmId):
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.delete_item(Key={'filmId': filmId})


def remove_from_search_table(filmId):
    table_name = os.environ['SEARCH_TABLE_NAME']
    table = dynamodb.Table(table_name)

    items = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('filmId').eq(filmId))
    films = items['Items']
    with table.batch_writer() as batch:
        for film in films:
            batch.delete_item(Key={
                'filmId': film['filmId'],
                'data': film['data']
            })


def remove_from_bucket(filmId):
    bucket_name = os.environ['BUCKET_NAME']
    files = [
        {'Key': filmId},
        {'Key': filmId + '_360p'},
        {'Key': filmId + '_144p'},
    ]
    s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': files})


def remove_from_ratings(filmId):
    table_name = os.environ['RATINGS_TABLE_NAME']
    table = dynamodb.Table(table_name)

    items = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('filmId').eq(filmId))
    ratings = items['Items']
    with table.batch_writer() as batch:
        for rating in ratings:
            batch.delete_item(Key={
                'filmId': rating['filmId'],
                'username': rating['username']
            })


def remove_from_feed(filmId):
    table_name = os.environ['FEED_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    queue_url = os.environ['CUSTOM_VAR']

    items = table.scan()
    items = items.get('Items', [])

    for item in items:
        for film in item['films']:
            if filmId == film[0]['filmId']:
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=item['username']
                )
                break
