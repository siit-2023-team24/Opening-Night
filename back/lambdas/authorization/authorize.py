import jwt
import boto3
import os
import time

client = boto3.client('cognito-idp')

def authorize(event, context):
    headers = event['headers']
    authorization = headers['Authorization']
    token = authorization.split(' ')[1]

    pool_id = os.environ['POOL_ID']

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        if 'exp' in decoded_token:
            current_time = int(time.time())
            if decoded_token['exp'] < current_time:
                print(f"Token has expired: {current_time} > {decoded_token['exp']}")
                return generate_policy('user', 'Deny', event['methodArn'])
            else:
                print(f"Token is still valid: {current_time} < {decoded_token['exp']}")

        username = decoded_token.get('cognito:username')
        response = client.admin_get_user(
            UserPoolId=pool_id,
            Username=username
        )
        print(f"User exists: {response}")

        user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
        print(f"Decoded user: {user_attributes}")
        print(f"Decoded token: {decoded_token}")
        
        for key in user_attributes.keys():
            if key == 'is_viewer': key = 'custom:is_viewer'

            expected_value = user_attributes.get(key)
            decoded_value = decoded_token.get(key)

            if decoded_value is None:
                print(f"Attribute missing in decoded token: {key}")
            elif str(decoded_value).lower() != str(expected_value).lower():
                print(f"Attribute mismatch: {key} (expected {expected_value}, got {decoded_value})")
                return generate_policy('user', 'Deny', event['methodArn'])
            else:
                print(f"Valid {key}")
        is_viewer = os.environ['IS_VIEWER']
        if decoded_token.get('custom:is_viewer', '') == is_viewer or is_viewer == 'both':
            return generate_policy('user', 'Allow', event['methodArn'])
        else:
            return generate_policy('user', 'Deny', event['methodArn'])
    except jwt.ExpiredSignatureError:
        return generate_policy('user', 'Deny', event['methodArn'])
    except jwt.InvalidTokenError:
        return generate_policy('user', 'Deny', event['methodArn'])
    except client.exceptions.UserNotFoundException:
        print("User does not exist")
        return generate_policy('user', 'Deny', event['methodArn'])

def generate_policy(principal_id, effect, resource):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
    return policy
