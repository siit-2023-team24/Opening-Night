import json
import os
import boto3
import uuid

s3_client = boto3.client('s3')
sfn_client = boto3.client('stepfunctions')

def upload(event, context):
    body = json.loads(event['body'])
    file_content = body['fileContent']
    film_id = body.get('filmId', str(uuid.uuid4()))

    bucket_name = os.environ['BUCKET_NAME']
    s3_client.put_object(
        Bucket=bucket_name,
        Key=film_id + '_temp',
        Body=file_content,
        ContentType='text/html'
    )

    state_machine_arn = os.environ['CUSTOM_VAR']

    sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({
                'filmId': film_id,
                'fileName': body['fileName'],
                'title' : body['title'],
                'description' : body['description'],
                'actors' : body['actors'],
                'directors' : body['directors'],
                'genres' : body['genres'],
                'isSeries': body['isSeries'],
                'series': body.get('series', None),
                'season': body.get('season', None),
                'episode': body.get('episode', None)
            })
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'message': 'Successfully uploaded movie!'
        })
    }

