import boto3
import json

client = boto3.client('cognito-idp')
ssm_client = boto3.client('ssm')

def login(event, context):
    body = json.loads(event['body'])

    username = body['username']
    password = body['password']

    response = ssm_client.get_parameter(
        Name='client_id'
    )
    client_id = response['Parameter']['Value']

    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Successful login!')
        }
    except client.exceptions.NotAuthorizedException as e:
        
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Wrong password')
        }
    except client.exceptions.UserNotFoundException as e:
        
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('User not found.')
        }
    except Exception as e:
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Internal server error: ' + str(e))
        }