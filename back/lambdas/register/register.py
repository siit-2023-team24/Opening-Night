import boto3
import json
from datetime import datetime
import os

client = boto3.client('cognito-idp')

def register(event, context):
    body = json.loads(event['body'])

    name = body['name']
    last_name = body['lastName']
    birthday = datetime.strptime(body['birthday'], '%Y-%m-%d').date().isoformat()
    username = body['username']
    email = body['email']
    password = body['password']
    is_viewer = body['isViewer']

    client_id = os.environ['CLIENT_ID']
    pool_id = os.environ['POOL_ID']

    if not is_unique(email, pool_id):
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Email already exists.')
        }

    try:
        client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {'Name': 'name', 'Value': name},
                {'Name': 'family_name', 'Value': last_name},
                {'Name': 'birthdate', 'Value': birthday},
                {'Name': 'email', 'Value': email},
                {'Name': 'custom:is_viewer', 'Value': str(is_viewer).lower()}
            ]
        )
        client.admin_confirm_sign_up(
            UserPoolId=pool_id,
            Username=username
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('User registered successfully!')
        }
    except client.exceptions.UsernameExistsException as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Username already exists.')
        }
    except client.exceptions.InvalidParameterException as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Invalid parameters: ' + str(e))
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps('Internal server error: ' + str(e))
        }

def is_unique(email, pool_id):
    try:
        response = client.list_users(
            UserPoolId=pool_id,
            Filter=f'email = "{email}"'
        )
        if response['Users']:
            return False
        return True
    
    except client.exceptions.UserNotFoundException:
        return True
    
    except Exception as e:
        raise e