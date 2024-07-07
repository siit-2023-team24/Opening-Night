import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
sns = boto3.client('sns')

def update_subs(event, context):

    path_params = event.get('pathParameters', {})
    username = path_params.get('username')
    
    subs = json.loads(event['body'])
    directors = subs['directors']
    actors = subs['actors']
    genres = subs['genres']
    
    #?
    email = subs['email']

    #write to db
    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
            'username': username,
            'directors': directors,
            'actors': actors,
            'genres': genres
        }
    )
    #write to sqs for feed calculation
    queue_url = os.environ['CUSTOM_VAR']
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=username
    )

    #subscribe
    for d in directors:
        subscribe(email, 'd' + d)
    for a in actors:
        subscribe(email, 'a' + a)
    for g in genres:
        subscribe(email, 'g' + g)

    body = {'message': 'Successfully updated subscriptions.'}

    return { 
        'statusCode': 200, 
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body, default=str)
        }

def subscribe(email, topic_name):
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']

    sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
