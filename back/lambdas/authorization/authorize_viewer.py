import jwt

def authorize(event, context):
    headers = event['headers']
    authorization = headers['Authorization']
    token = authorization.split(' ')[1]
    print(token)

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        if decoded_token.get('custom:is_viewer', '') == 'true':
            return generate_policy('user', 'Allow', event['methodArn'])
        else:
            return generate_policy('user', 'Deny', event['methodArn'])
    except jwt.ExpiredSignatureError:
        return generate_policy('user', 'Deny', event['methodArn'])
    except jwt.InvalidTokenError:
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
