import boto3
import json
import os

client = boto3.client('cognito-idp')

def login(event, context):
    body = json.loads(event['body'])

    username = body['username']
    password = body['password']

    client_id = os.environ['CLIENT_ID']

    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        id_token = response['AuthenticationResult']['IdToken']
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'idToken': id_token,
                'accessToken': access_token,
                'refreshToken': refresh_token
            })
        }
    except client.exceptions.NotAuthorizedException as e:
        
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Incorrect username or password.')
        }
    except client.exceptions.UserNotFoundException as e:
        
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Incorrect username or password.')
        }
    except Exception as e:
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Internal server error: ' + str(e))
        }