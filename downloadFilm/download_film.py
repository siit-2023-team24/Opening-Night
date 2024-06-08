import json
import os
import boto3

# Extract environment variable
table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')

def get_one(event, context):
    # Extract data from request
    path = event['rawPath'][1:]
    # Get table instance connection
    table = dynamodb.Table(table_name)
    # Get all items from table
    response = table.get_item(
        Key={
            'name': path
        }
    )
    # Create response
    body = {
        'data': response['Item']
    }
    return { 'statusCode': 200, 'body': json.dumps(body, default=str) }
